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
import tempfile
from pathlib import Path
from typing import Union

import azure.ai.ml as azureml
from azure.ai.ml.entities import BatchDeployment
from azure.ai.ml.entities import BatchEndpoint
from azure.ai.ml.entities import BatchRetrySettings
from azure.ai.ml.entities import CodeConfiguration
from azure.ai.ml.entities import Environment
from azure.core.exceptions import ResourceNotFoundError

from bosun.plugin.azureml.client.base_endpoint_client import BaseEndpointClient
from bosun.plugin.azureml.client.scoring_snippets import AzureMLBatchEndpointScoringSnippet
from bosun.plugin.azureml.config.azureml_client_config import EndpointConfig
from bosun.plugin.azureml.config.azureml_client_config import Key
from bosun.plugin.azureml.config.config_keys import EndpointType


class BatchEndpointClient(BaseEndpointClient):
    ENDPOINT_TYPE = EndpointType.BATCH
    SNIPPET_GENERATOR = AzureMLBatchEndpointScoringSnippet

    def __init__(self, config: EndpointConfig):
        super().__init__(config)

    def create_or_update_endpoint(self):
        endpoint_tags = {
            Key.DATAROBOT_DEPLOYMENT_ID.value: self.datarobot_deployment_id,
            Key.DATAROBOT_ENVIRONMENT_ID.value: self.datarobot_environment_id,
        }
        endpoint_tags.update(self.prediction_environment_tags)
        endpoint = azureml.entities.BatchEndpoint(name=self.endpoint_name, tags=endpoint_tags)
        # TODO assert status
        self._client.batch_endpoints.begin_create_or_update(endpoint).result(
            self.config[Key.ENDPOINT_CREATION_TIMEOUT]
        )

    def get_endpoint(self) -> BatchEndpoint:
        return self._client.batch_endpoints.get(self.endpoint_name)

    def create_deployment(self, deployment_name: str, model, environment: Environment):
        model_filename = Path(model.path).name
        scoring_script_name = "batch_driver.py"
        deployment_tags = {
            Key.DATAROBOT_ENVIRONMENT_ID.value: self.datarobot_environment_id,
            Key.DATAROBOT_DEPLOYMENT_ID.value: self.datarobot_deployment_id,
            Key.DATAROBOT_MODEL_ID.value: self.datarobot_model_id,
        }
        deployment_tags.update(self.prediction_environment_tags)
        with tempfile.TemporaryDirectory() as scoring_code_dir, open(
            Path(scoring_code_dir) / scoring_script_name, "w"
        ) as scoring_code_file:
            scoring_code_file.write(self.get_scoring_snippet(model_filename))
            scoring_code_file.flush()
            self.copy_feature_types(scoring_code_dir)

            deployment = BatchDeployment(
                name=deployment_name or self.deployment_name,
                endpoint_name=self.endpoint_name,
                model=model,
                code_configuration=CodeConfiguration(
                    code=str(scoring_code_dir), scoring_script=scoring_script_name
                ),
                environment=environment,
                compute=self.config[Key.COMPUTE_CLUSTER],
                instance_count=self.config[Key.COMPUTE_CLUSTER_INSTANCE_COUNT],
                max_concurrency_per_instance=self.config[Key.MAX_CONCURRENCY_PER_INSTANCE],
                mini_batch_size=self.config[Key.MINI_BATCH_SIZE],
                output_file_name=self.config[Key.OUTPUT_FILE_NAME],
                output_action=self.config[Key.OUTPUT_ACTION],
                error_threshold=self.config[Key.ERROR_THRESHOLD],
                retry_settings=BatchRetrySettings(
                    max_retries=self.config[Key.MAX_RETRIES],
                    timeout=self.config[Key.SCORING_TIMEOUT_SECONDS],
                ),
                logging_level=self.config[Key.LOGGING_LEVEL],
                environment_variables=self._get_env_vars(model_filename),
                tags=deployment_tags,
            )
            # TODO check status of deployment
            # TODO make `skip_script_validation` configurable
            self._client.batch_deployments.begin_create_or_update(
                deployment, skip_script_validation=True
            ).result(self.config[Key.ENDPOINT_DEPLOYMENT_TIMEOUT])

        # ensure deployment is default in batch endpoint
        self.make_default(deployment.name)

    def make_default(self, deployment_name, await_results=True):
        endpoint: BatchEndpoint = self._client.batch_endpoints.get(self.endpoint_name)
        endpoint.defaults.deployment_name = deployment_name
        poller = self._client.batch_endpoints.begin_create_or_update(endpoint)
        if await_results:
            # TODO: the poller is returning the wrong object type
            # (azure.ai.ml._restclient.v2022_05_01.models._models_py3.BatchEndpointData)
            # which doesn't have a provisioning state. For now I'm just going to assume
            # the operation succeeded.
            poller.result(self.config[Key.ENDPOINT_UPDATE_TIMEOUT])
            self.logger.info(
                "Default deployment for endpoint '%s' updated to: %s",
                self.deployment_name,
                self.endpoint_name,
            )

    def delete_endpoint(self):
        self._client.batch_endpoints.begin_delete(name=self.endpoint_name).result(
            self.config[Key.ENDPOINT_DELETION_TIMEOUT]
        )

    def delete_deployment(self, deployment_to_delete: str = None):
        deployment_name = deployment_to_delete or self.deployment_name
        self._client.batch_deployments.begin_delete(
            name=deployment_name, endpoint_name=self.endpoint_name
        ).result(self.config[Key.DEPLOYMENT_DELETION_TIMEOUT])

    def deployment_logs(self):
        return ""  # NOOP batch endpoint does not provide logs

    def deployment_status(self) -> Union[None, str]:
        try:
            endpoint: BatchEndpoint = self._client.batch_endpoints.get(name=self.endpoint_name)
            deployment: BatchDeployment = self._client.batch_deployments.get(
                name=self.deployment_name, endpoint_name=self.endpoint_name
            )
        except ResourceNotFoundError:
            endpoint, deployment = None, None

        if endpoint is None or deployment is None:
            return None  # status unknown

        return self.map_state(endpoint.provisioning_state)
