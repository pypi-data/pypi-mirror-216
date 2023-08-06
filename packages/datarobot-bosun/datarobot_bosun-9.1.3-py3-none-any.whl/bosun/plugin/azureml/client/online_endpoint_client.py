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
import typing
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Union

from azure.ai.ml._restclient.v2022_02_01_preview.models import OnlineEndpointData
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import CodeConfiguration
from azure.ai.ml.entities import Environment
from azure.ai.ml.entities import IdentityConfiguration
from azure.ai.ml.entities import ManagedIdentityConfiguration
from azure.ai.ml.entities import ManagedOnlineDeployment
from azure.ai.ml.entities import ManagedOnlineEndpoint
from azure.ai.ml.entities import Model
from azure.ai.ml.entities import OnlineDeployment
from azure.ai.ml.entities import OnlineEndpoint
from azure.ai.ml.entities import OnlineRequestSettings
from azure.ai.ml.entities import SystemData
from azure.ai.ml.exceptions import LocalEndpointInFailedStateError
from azure.ai.ml.exceptions import LocalEndpointNotFoundError
from azure.ai.ml.operations import OnlineEndpointOperations
from azure.core.exceptions import HttpResponseError
from azure.core.exceptions import ResourceNotFoundError

from bosun.plugin.azureml.client.base_endpoint_client import BaseEndpointClient
from bosun.plugin.azureml.client.scoring_snippets import AzureMLOnlineEndpointScoringSnippet
from bosun.plugin.azureml.config.azureml_client_config import AZURE_BASE_ENVIRONMENT
from bosun.plugin.azureml.config.azureml_client_config import AZURE_TEMPLATE_DIR
from bosun.plugin.azureml.config.azureml_client_config import EndpointConfig
from bosun.plugin.azureml.config.config_keys import Constants
from bosun.plugin.azureml.config.config_keys import EndpointType
from bosun.plugin.azureml.config.config_keys import Key
from bosun.plugin.azureml.config.config_keys import ProvisioningState
from bosun.plugin.constants import DeploymentState


class OnlineEndpointClient(BaseEndpointClient):
    ENDPOINT_TYPE = EndpointType.ONLINE
    SNIPPET_GENERATOR = AzureMLOnlineEndpointScoringSnippet

    def __init__(self, config: EndpointConfig):
        super().__init__(config)
        self.compute_virtual_machine = self.config[Key.COMPUTE_VIRTUAL_MACHINE]
        self.compute_instance_count = self.config[Key.COMPUTE_INSTANCE_COUNT]

    def create_or_update_endpoint(self):
        endpoint_tags = {
            Key.DATAROBOT_DEPLOYMENT_ID.value: self.datarobot_deployment_id,
            Key.DATAROBOT_ENVIRONMENT_ID.value: self.datarobot_environment_id,
        }
        endpoint_tags.update(self.prediction_environment_tags)
        user_identity = (
            None
            if not self.config.is_monitoring_enabled
            else IdentityConfiguration(
                type=Constants.USER_ASSIGNED_IDENTITY.value,
                user_assigned_identities=[
                    ManagedIdentityConfiguration(
                        resource_id=self.config[Key.AZURE_MANAGED_IDENTITY_ID]
                    )
                ],
            )
        )

        endpoint = None
        with suppress(ResourceNotFoundError, LocalEndpointNotFoundError):
            # try to get an existing endpoint to preserve traffic settings during update
            endpoint = self.get_endpoint()

        if endpoint:
            endpoint.tags.update(endpoint_tags)
            endpoint.identity = user_identity
        else:
            endpoint = ManagedOnlineEndpoint(
                name=self.endpoint_name,
                auth_mode=Constants.AUTH_MODE_KEY.value,
                tags=endpoint_tags,
                identity=user_identity,
            )

        result = self._client.online_endpoints.begin_create_or_update(endpoint, local=self._local)
        if not self._local:
            result: OnlineEndpoint = result.result(self.config[Key.ENDPOINT_CREATION_TIMEOUT])

        if result.provisioning_state == ProvisioningState.SUCCEEDED.value:
            self.logger.info("Endpoint %s is successfully created.", self.endpoint_name)
        elif self._local:
            # For local, if there was no exception then it was a success
            self.logger.info("Local Endpoint %s is successfully created.", self.endpoint_name)
        else:
            message = (
                f"Failed to create endpoint {endpoint.name}. Status: {result.provisioning_state}"
            )
            self.logger.error(message)
            raise RuntimeError(message)

    def get_endpoint(self) -> OnlineEndpoint:
        return self._client.online_endpoints.get(self.endpoint_name, local=self._local)

    def get_endpoint_traffic_settings(
        self,
    ) -> typing.Optional[typing.Tuple[datetime, dict]]:

        endpoints_api: OnlineEndpointOperations = self._client.online_endpoints

        if self._local:
            modified_at = None
            endpoint: OnlineEndpoint = endpoints_api.get(
                name=self.endpoint_name, **self.local_parameter
            )
            return modified_at, endpoint.traffic

        # Read JSON response from an endpoint public API in order to get lastModifiedAt field
        # which is not exposed by the OnlineEndpoint entity. API returns UTC datetime string
        # in ISO 8601 format: e.g. 2020-01-01T12:34:56.999Z
        endpoint: OnlineEndpointData = endpoints_api._online_operation.get(
            resource_group_name=self.config[Key.AZURE_RESOURCE_GROUP],
            workspace_name=self.config[Key.AZURE_WORKSPACE],
            endpoint_name=self.endpoint_name,
            **endpoints_api._init_kwargs,
        )
        self.logger.info("Found existing endpoint %s.", self.endpoint_name)
        system_data: SystemData = endpoint.system_data
        azure_endpoint_created_at = system_data.created_at if system_data else None
        azure_endpoint_last_modified_at = system_data.last_modified_at if system_data else None
        self.logger.info(
            f"Azure endpoint created_at: {azure_endpoint_created_at}, "
            f"modified_at: {azure_endpoint_last_modified_at}"
        )
        return (
            azure_endpoint_last_modified_at,
            endpoint.properties.traffic,
        )

    def create_deployment(self, deployment_name: str, model, environment: Environment):
        model_filename = Path(model.path).name
        scoring_script_name = "score.py"
        deployment_tags = {
            Key.DATAROBOT_ENVIRONMENT_ID.value: self.datarobot_environment_id,
            Key.DATAROBOT_DEPLOYMENT_ID.value: self.datarobot_deployment_id,
            Key.DATAROBOT_MODEL_ID.value: self.datarobot_model_id,
        }
        deployment_tags.update(self.prediction_environment_tags)

        with ScratchDir(cleanup=not self._local) as scoring_code_dir:
            scoring_code_file = scoring_code_dir / scoring_script_name
            scoring_code_file.write_text(self.get_scoring_snippet(model_filename))
            # Fix permissions when running in self._local (e.g. docker bind mount) mode
            scoring_code_dir.chmod(0o755)
            scoring_code_file.chmod(0o644)

            # SDK requires scoring timeout to be in millis
            scoring_timeout_ms = self.config[Key.SCORING_TIMEOUT_SECONDS] * 1000
            deployment = ManagedOnlineDeployment(
                name=deployment_name or self.deployment_name,
                endpoint_name=self.endpoint_name,
                model=model,
                environment=environment,
                code_configuration=CodeConfiguration(
                    code=str(scoring_code_dir), scoring_script=scoring_script_name
                ),
                request_settings=OnlineRequestSettings(request_timeout_ms=scoring_timeout_ms),
                instance_type=self.compute_virtual_machine,
                instance_count=self.compute_instance_count,
                environment_variables=self._get_env_vars(model_filename),
                tags=deployment_tags,
            )

            try:
                result = self._client.online_deployments.begin_create_or_update(
                    # TODO: make `skip_script_validation` configurable
                    deployment=deployment,
                    local=self._local,
                    skip_script_validation=True,
                )
            except LocalEndpointInFailedStateError as e:
                self.logger.error("Failed to create local deployment: %s", e)
                result = ManagedOnlineDeployment(
                    **deployment._to_dict(), provisioning_state=ProvisioningState.FAILED.value
                )

        if not self._local:
            result = result.result(self.config[Key.ENDPOINT_DEPLOYMENT_TIMEOUT])

        if result.provisioning_state == ProvisioningState.SUCCEEDED.value:
            self.logger.info("Deployment %s is successfully created.", self.deployment_name)
        else:
            msg = (
                f"Failed to create deployment {deployment.name}"
                f" (endpoint={self.endpoint_name};model={model.name})."
                f" Status: {result.provisioning_state}"
            )
            self.logger.error(msg)
            try:
                logs = self._client.online_deployments.get_logs(
                    name=result.name,
                    endpoint_name=result.endpoint_name,
                    lines=60,  # hopefully this is enough context w/o dumping a ton of text
                    local=self._local,
                )
                self.logger.debug("deployment container logs: %s", logs)
                msg += f"\n\nDeployment Logs:\n{logs}"
            except Exception as e:
                self.logger.warning(
                    "Failed to fetch logs for deployment %s (endpoint=%s): %s",
                    result.name,
                    result.endpoint_name,
                    e,
                )
            raise RuntimeError(msg)

        return result

    def delete_endpoint(self):
        self.logger.info("Deleting online endpoint %s...", self.endpoint_name)
        timeout_seconds = self.config[Key.ENDPOINT_DELETION_TIMEOUT]
        try:
            result = self._client.online_endpoints.begin_delete(
                self.endpoint_name, local=self._local
            )
        except LocalEndpointNotFoundError:
            # To be idempotent, if the endpoint is already gone then just ignore.
            pass
        else:
            if not self._local:
                result.result(timeout_seconds)

    def delete_deployment(self, deployment_to_delete: str = None):
        deployment_name = deployment_to_delete or self.deployment_name

        self.logger.info(
            "Deleting deployment %s from online endpoint %s...",
            deployment_name,
            self.endpoint_name,
        )
        result = self._client.online_deployments.begin_delete(
            name=deployment_name, endpoint_name=self.endpoint_name, local=self._local
        )
        if not self._local:
            result.result(self.config[Key.DEPLOYMENT_DELETION_TIMEOUT])

    def deployment_logs(self) -> str:
        return self._client.online_deployments.get_logs(
            name=self.deployment_name,
            endpoint_name=self.endpoint_name,
            lines=self.config[Key.DEPLOYMENT_LOG_LINES_COUNT],
            local=self._local,
        )

    def deployment_status(self) -> Union[None, str]:
        try:
            endpoint: OnlineEndpoint = self._client.online_endpoints.get(
                name=self.endpoint_name, local=self._local
            )
            deployment: OnlineDeployment = self._client.online_deployments.get(
                name=self.deployment_name, endpoint_name=self.endpoint_name, local=self._local
            )
        except (LocalEndpointNotFoundError, ResourceNotFoundError):
            endpoint = None
            deployment = None

        if endpoint is None or deployment is None:
            return None  # status unknown

        deployment_state = self.map_online_deployment_state(
            endpoint_state=endpoint.provisioning_state,
            deployment_state=deployment.provisioning_state,
        )

        return deployment_state

    @staticmethod
    def map_online_deployment_state(endpoint_state, deployment_state):
        # (endpoint_state, deployment_state) -> DR deployment_state
        state_map = {
            (  # deployment creation
                ProvisioningState.UPDATING.value,
                ProvisioningState.UPDATING.value,
            ): DeploymentState.LAUNCHING,
            (  # endpoint traffic update
                ProvisioningState.UPDATING.value,
                ProvisioningState.SUCCEEDED.value,
            ): DeploymentState.LAUNCHING,
            (  # deployment deletion. this should be an API bug?
                ProvisioningState.SUCCEEDED.value,
                ProvisioningState.UPDATING.value,
            ): DeploymentState.SHUTTING_DOWN,
            (  # endpoint deletion
                ProvisioningState.DELETING.value,
                ProvisioningState.DELETING.value,
            ): DeploymentState.SHUTTING_DOWN,
            (
                ProvisioningState.SUCCEEDED.value,
                ProvisioningState.SUCCEEDED.value,
            ): DeploymentState.READY,
        }

        return state_map.get((endpoint_state, deployment_state), DeploymentState.UNKNOWN)

    def get_traffic_settings_set_by_user(self) -> typing.Dict[str, str]:
        traffic_settings = {}

        try:
            datarobot_traffic_last_modified_at = self.config[Key.ENDPOINT_TRAFFIC_LAST_MODIFIED_AT]
            azure_endpoint_last_modified_at, _ = self.get_endpoint_traffic_settings()
            if self._local or datarobot_traffic_last_modified_at > azure_endpoint_last_modified_at:
                traffic_settings = self.config[Key.ENDPOINT_TRAFFIC]
            else:
                self.logger.info(
                    "Traffic settings are stale. Skipping traffic update for the endpoint '%s'."
                    "DataRobot traffic modified_at: %s, AzureML endpoint modified_at %s.",
                    self.endpoint_name,
                    datarobot_traffic_last_modified_at,
                    azure_endpoint_last_modified_at,
                )

        except (ResourceNotFoundError, LocalEndpointNotFoundError):
            # for a new endpoint, always apply the traffic settings set by user on DataRobot UI
            traffic_settings = self.config[Key.ENDPOINT_TRAFFIC]
            self.logger.warning(
                "Endpoint %s not found. A new one will be created.", self.endpoint_name
            )

        except HttpResponseError:
            # do not apply traffic changes if we unsure on it's current state
            # do not fail the flow of deployment creation/update or deletion
            self.logger.error("Can't get endpoint %s", self.endpoint_name, exc_info=True)
        except AttributeError:
            self.logger.error(
                "Can't get 'lastModifiedAt' timestamp for endpoint %s",
                self.endpoint_name,
                exc_info=True,
            )

        return traffic_settings

    def update_deployment_traffic(self, endpoint, traffic_settings, await_results=True):
        endpoint.traffic.update(traffic_settings)
        result = self._client.online_endpoints.begin_create_or_update(endpoint, local=self._local)

        if await_results and not self._local:
            result = result.result(self.config[Key.ENDPOINT_UPDATE_TIMEOUT])
            if result.provisioning_state == ProvisioningState.SUCCEEDED.value:
                self.logger.info("Endpoint traffic is updated to %s.", str(traffic_settings))
            else:
                msg = f"Failed to update traffic for the endpoint {self.endpoint_name}. "
                f"Status: {result.provisioning_state}."
                self.logger.error(msg)
                raise RuntimeError(msg)

    def get_latest_environment(self):
        # Override base method because local mode is only supported for online
        # endpoints currently.
        if self._local:
            return Environment(
                conda_file=AZURE_TEMPLATE_DIR / "conda.yml", image=AZURE_BASE_ENVIRONMENT
            )
        return super().get_latest_environment()

    def register_model(self, model_path):
        if self._local:
            self.logger.info("Skipping local model registration")
            return Model(
                name=self.datarobot_model_name, path=model_path, type=AssetTypes.CUSTOM_MODEL
            )
        return super().register_model(model_path)

    def archive_model(self):
        if self._local:
            self.logger.info("Skipping local model deletion")
            return
        super().archive_model()


class ScratchDir(TemporaryDirectory):
    """
    When running in local mode, AzureML bind mounts the scoring script into the container
    so we can't use an actual temporary file/dir. We will still create the dir/file in
    the temp location so hopefully the OS will cleanup the files for us.
    """

    def __init__(self, cleanup=True, **kwargs):
        super().__init__(**kwargs)
        self._do_cleanup = cleanup
        if not cleanup:
            # If we aren't doing cleanup, detach the finalizer that the parent class sets
            self._finalizer.detach()

    def __enter__(self):
        return Path(self.name)

    def cleanup(self):
        if self._do_cleanup:
            super().cleanup()
