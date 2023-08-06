#  ---------------------------------------------------------------------------------
#  Copyright (c) 2023 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2023.
#
#  DataRobot, Inc. Confidential.
#  This is proprietary source code of DataRobot, Inc. and its affiliates.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.
#  ---------------------------------------------------------------------------------
import logging
from typing import Union

from azure.ai.ml.exceptions import LocalEndpointNotFoundError
from azure.core.exceptions import ResourceNotFoundError

from bosun.plugin.action_status import ActionDataFields
from bosun.plugin.action_status import ActionStatus
from bosun.plugin.action_status import ActionStatusInfo
from bosun.plugin.azureml.azureml_status_reporter import MLOpsStatusReporter
from bosun.plugin.azureml.client.base_endpoint_client import ListOnlyEndpointClient
from bosun.plugin.azureml.client.batch_endpoint_client import BatchEndpointClient
from bosun.plugin.azureml.client.online_endpoint_client import OnlineEndpointClient
from bosun.plugin.azureml.config.azureml_client_config import AZURE_CUSTOM_ENVIRONMENT
from bosun.plugin.azureml.config.azureml_client_config import EndpointConfig
from bosun.plugin.azureml.config.config_keys import EndpointType
from bosun.plugin.azureml.config.config_keys import Key
from bosun.plugin.bosun_plugin_base import BosunPluginBase
from bosun.plugin.constants import DeploymentState
from bosun.plugin.deployment_info import DeploymentInfo


class AzureMLPlugin(BosunPluginBase):
    AZURE_CLIENTS = {
        EndpointType.ONLINE: OnlineEndpointClient,
        EndpointType.BATCH: BatchEndpointClient,
        EndpointType.UNKNOWN: ListOnlyEndpointClient,
    }

    def __init__(self, plugin_config, private_config_file, pe_info, dry_run):
        super().__init__(plugin_config, private_config_file, pe_info, dry_run)
        http_logger = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
        http_logger.setLevel(logging.WARNING)

    def get_azure_client(
        self,
    ) -> Union[OnlineEndpointClient, BatchEndpointClient, ListOnlyEndpointClient]:
        assert self._pe_info is not None
        config = EndpointConfig.read_config(
            parent_config=self._plugin_config,
            config_file_path=self._private_config_file,
            prediction_environment=self._pe_info,
            deployment=self._deployment_info,
        )
        config.validate_config()
        endpoint_type = config.deduce_endpoint_type_by_config()
        self._logger.info("Configuring AzureML client %s...", endpoint_type.name)
        azure_client_cls = self.AZURE_CLIENTS[endpoint_type]
        return azure_client_cls(config)

    def deployment_list(self):
        azure_client = self.get_azure_client()
        datarobot_model_deployments = azure_client.list_deployments()

        status_msg = (
            (f"Found {len(datarobot_model_deployments)} deployment(s)")
            if len(datarobot_model_deployments) > 0
            else "No deployments found"
        )

        self._logger.info(status_msg)

        deployments_map = {
            deployment_id: ActionStatusInfo(ActionStatus.OK, state=deployment_state).to_dict()
            for deployment_id, deployment_state in datarobot_model_deployments.items()
        }

        return ActionStatusInfo(ActionStatus.OK, msg=status_msg, data=deployments_map)

    def deployment_start(
        self,
        di: DeploymentInfo,
        is_model_replacement: bool = False,
        deployment_name: str = None,
        traffic_settings: dict = None,
        reporter: MLOpsStatusReporter = None,
    ):
        self._logger.info("Deployment start action invoked for the deployment %s...", di.id)
        if di.model_artifact is None or not di.model_artifact.exists():
            return ActionStatusInfo(
                ActionStatus.ERROR,
                "Model must be pulled from DataRobot deployment, before pushing it to AzureML.",
            )

        try:
            azure_client = self.get_azure_client()
            reporter = reporter or MLOpsStatusReporter(
                self._plugin_config, di, azure_client.ENDPOINT_TYPE
            )

            reporter.report_deployment("Registering the model...")
            model = azure_client.register_model(di.model_artifact)

            if azure_client.ENDPOINT_TYPE == EndpointType.ONLINE and not is_model_replacement:
                # Traffic settings should be calculated prior to any modifications done to the
                # endpoint. Otherwise, traffic settings passed from the UI will be considered as
                # stale and then ignored.
                traffic_settings = azure_client.get_traffic_settings_set_by_user()

            endpoint_name = azure_client.config[Key.ENDPOINT_NAME]
            if not is_model_replacement:
                reporter.report_deployment(f"Configuring the endpoint '{endpoint_name}'...")
                azure_client.create_or_update_endpoint()

            reporter.report_deployment(
                f"Searching for custom environment: '{AZURE_CUSTOM_ENVIRONMENT}'..."
            )
            environment = azure_client.get_latest_environment()

            reporter.report_deployment(
                "Creating a new deployment. This action may take up to 20 minutes. "
                "For more details check the https://ml.azure.com/endpoints page."
            )

            azure_client.create_deployment(deployment_name, model, environment)

            # Need to fetch the endpoint after creating the deployment because it
            # seems otherwise it won't always have the scoring_uri filled in.
            endpoint = azure_client.get_endpoint()
            if azure_client.ENDPOINT_TYPE == EndpointType.ONLINE:
                if traffic_settings:
                    reporter.report_deployment("Updating the deployment traffic...")
                    self._logger.info(
                        "New traffic configuration: %s for the endpoint: %s",
                        str(traffic_settings),
                        endpoint_name,
                    )
                    azure_client.update_deployment_traffic(endpoint, traffic_settings)
        except Exception as e:
            self._logger.exception("Failed to start the deployment %s", di.id)
            return ActionStatusInfo(ActionStatus.ERROR, msg=str(e))

        self._logger.info("Scoring code model is successfully deployed to AzureML.")
        status = self.deployment_status(di)
        status.data = {
            ActionDataFields.PREDICTION_URL: endpoint.scoring_uri,
            ActionDataFields.DASHBOARD_URL: azure_client.make_console_url(endpoint),
        }
        return status

    def deployment_stop(self, deployment_id: str):
        try:
            azure_client = self.get_azure_client()
            deployments = azure_client.list_deployments_by_endpoint()
            deployments_in_endpoint = len(deployments)
            if deployments_in_endpoint == 1:
                # delete endpoint only if it has one deployment at maximum
                azure_client.delete_endpoint()
            else:
                azure_client.delete_deployment()
        except (ResourceNotFoundError, LocalEndpointNotFoundError):
            # nothing to do
            self._logger.warning(
                "Deployment does not exist: %s. Skipping deployment stop.", deployment_id
            )
        except Exception as e:
            # Deployment can't be deleted if endpoint has multiple deployments and
            # the deployment traffic settings are not set to zero.
            #
            # Deployment traffic can't be set to zero prior to deletion,
            # since traffic must be redistributed to make sum of all deployment traffic settings
            # be equal to either 0 or 100.
            self._logger.exception("Error stopping deployment")
            return ActionStatusInfo(ActionStatus.ERROR, msg=str(e))

        return ActionStatusInfo(ActionStatus.OK, state=DeploymentState.STOPPED)

    def deployment_replace_model(self, deployment_info: DeploymentInfo):
        """
        Do model replacement using a blue-green deployment strategy:
        - old model continues to serve realtime traffic
        - a new model is deployed with a new unique deployment name suffix
        - endpoint traffic is flipped from old deployment to the new one
        - old deployment is stopped
        """
        azure_client = self.get_azure_client()
        traffic_settings = None
        old_deployment_name = azure_client.get_deployment_name_by_id(deployment_info.id)
        new_deployment_name = azure_client.config.new_deployment_name

        if azure_client.ENDPOINT_TYPE == EndpointType.ONLINE:
            (
                azure_endpoint_last_modified_at,
                current_traffic_settings,
            ) = azure_client.get_endpoint_traffic_settings()

            # switch traffic from the old deployment to the new one
            traffic_settings = dict(**current_traffic_settings)
            old_deployment_traffic_value = traffic_settings.get(old_deployment_name)
            if not old_deployment_traffic_value:
                self._logger.warning(
                    "No traffic settings found for the deployment %s",
                    old_deployment_name,
                )

            traffic_settings[old_deployment_name] = 0
            traffic_settings[new_deployment_name] = old_deployment_traffic_value or 0

        reporter = MLOpsStatusReporter(
            self._plugin_config, deployment_info, azure_client.ENDPOINT_TYPE
        )
        deployment_start_status = self.deployment_start(
            deployment_info,
            is_model_replacement=True,
            # model replacement requires a new unique deployment name
            deployment_name=new_deployment_name,
            traffic_settings=traffic_settings,
            reporter=reporter,
        )

        reporter.report_deployment(f"Removing the old deployment '{old_deployment_name}'...")
        azure_client.delete_deployment(old_deployment_name)

        return deployment_start_status

    def pe_status(self):
        try:
            azure_client = self.get_azure_client()
            azure_client.list_deployments()
            status = ActionStatus.OK
            status_msg = "Azure connection successful"
        except Exception:
            status = ActionStatus.ERROR
            status_msg = "Azure connection failed"
            self._logger.exception(status_msg)

        return ActionStatusInfo(status=status, msg=status_msg)

    def deployment_status(self, deployment_info: DeploymentInfo):
        azure_client = self.get_azure_client()
        try:
            deployment_status = azure_client.deployment_status()
            if deployment_status is None:
                return ActionStatusInfo(ActionStatus.UNKNOWN, state=DeploymentState.STOPPED)

            self._logger.info(
                "Deployment '%s' (%s) has status '%s'",
                deployment_info.name,
                deployment_info.id,
                deployment_status,
            )
            return ActionStatusInfo(ActionStatus.OK, state=deployment_status)
        except Exception as e:
            self._logger.exception("Error checking deployment status")
            return ActionStatusInfo(ActionStatus.ERROR, msg=str(e))

    def plugin_start(self):
        """
        Builds a new Custom environment if one does not exist.
        AzureML internally blocks a deployment until a custom environment is successfully created,
        so we don't need to introduce deployment blocks on our side.

        The deployment timeout must include the time needed for image build (>= 10minutes).
        """
        azure_client = self.get_azure_client()
        azure_client.get_latest_environment()
        return ActionStatusInfo(ActionStatus.OK)

    def plugin_stop(self):
        # NOOP
        return ActionStatusInfo(ActionStatus.OK)
