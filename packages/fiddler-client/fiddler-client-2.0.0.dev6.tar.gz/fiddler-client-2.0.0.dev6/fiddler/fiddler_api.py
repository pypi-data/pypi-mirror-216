# TODO: Add License
import json
from collections import namedtuple
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from deprecated import deprecated

from fiddler import constants
from fiddler.connection import Connection
from fiddler.core_objects import (
    DatasetInfo,
    FiddlerTimestamp,
    ModelInfo,
    MonitoringViolation,
    MonitoringViolationType,
)
from fiddler.monitoring_validator import MonitoringValidator
from fiddler.project import Project
from fiddler.utils import cast_input_data
from fiddler.utils import logging
from fiddler.utils.general_checks import do_not_proceed, safe_name_check, type_enforce
from fiddler.utils.pandas import df_size_exceeds

LOG = logging.getLogger(__name__)

SUCCESS_STATUS = Connection.SUCCESS_STATUS
FAILURE_STATUS = Connection.FAILURE_STATUS
FIDDLER_ARGS_KEY = Connection.FIDDLER_ARGS_KEY
STREAMING_HEADER_KEY = Connection.STREAMING_HEADER_KEY
AUTH_HEADER_KEY = Connection.AUTH_HEADER_KEY
ROUTING_HEADER_KEY = Connection.ROUTING_HEADER_KEY
ADMIN_SERVICE_PORT = 4100
DATASET_MAX_ROWS = 50_000

# A PredictionEventBundle represents a batch of inferences and their input
# features. All of these share schema, latency, and success status. A bundle
# can consist just one event as well.
PredictionEventBundle = namedtuple(
    'PredictionEventBundle',
    [
        'prediction_status',  # typeof: int # 0 for success, failure otherwise
        'prediction_latency',  # typeof: float # Latency in seconds.
        'input_feature_bundle',  # list of feature vectors.
        'prediction_bundle',  # list of prediction vectors.
        # TODO: Support sending schema as well.
    ],
)

_protocol_version = 1


class FiddlerApi:
    """Broker of all connections to the Fiddler API.
    Conventions:
        - Exceptions are raised for FAILURE reponses from the backend.
        - Methods beginning with `list` fetch lists of ids (e.g. all model ids
            for a project) and do not alter any data or state on the backend.
        - Methods beginning with `get` return a more complex object but also
            do not alter data or state on the backend.
        - Methods beginning with `run` invoke model-related execution and
            return the result of that computation. These do not alter state,
            but they can put a heavy load on the computational resources of
            the Fiddler engine, so they should be paralellized with care.
        - Methods beginning with `delete` permanently, irrevocably, and
            globally destroy objects in the backend. Think "rm -rf"
        - Methods beginning with `upload` convert and transmit supported local
            objects to Fiddler-friendly formats loaded into the Fiddler engine.
            Attempting to upload an object with an identifier that is already
            in use will result in an exception being raised, rather than the
            existing object being overwritten. To update an object in the
            Fiddler engine, please call both the `delete` and `upload` methods
            pertaining to the object in question.

    :param url: The base URL of the API to connect to. Usually either
        https://dev.fiddler.ai (cloud) or http://localhost:4100 (onebox)
    :param org_id: The name of your organization in the Fiddler platform
    :param auth_token: Token used to authenticate. Your token can be
        created, found, and changed at <FIDDLER URL>/settings/credentials.
    :param proxies: optionally, a dict of proxy URLs. e.g.,
                    proxies = {'http' : 'http://proxy.example.com:1234',
                               'https': 'https://proxy.example.com:5678'}
    :param verbose: if True, api calls will be logged verbosely,
                    *warning: all information required for debugging will be
                    logged including the auth_token.
    :param verify: if False, certificate verification will be disabled when
        establishing an SSL connection.
    """

    def __init__(
        self,
        url=None,
        org_id=None,
        auth_token=None,
        proxies=None,
        verbose=False,
        timeout: int = None,
        verify=True,
    ):
        self.org_id = org_id
        self.strict_mode = True
        self.connection = Connection(
            url, org_id, auth_token, proxies, verbose, timeout, verify=verify
        )

        self.monitoring_validator = MonitoringValidator()

    def __getattr__(self, function_name):
        """
        Overriding allows us to point unrecognized use cases to the documentation page
        """

        def method(*args, **kwargs):
            # This is a method that is not recognized
            error_msg = (
                f'Function `{function_name}` not found.\n'
                f'Please consult Fiddler documentation at `https://api.fiddler.ai/`'
            )
            raise RuntimeError(error_msg)

        return method

    @staticmethod
    def _abort_dataset_upload(
        dataset: Dict[str, pd.DataFrame], size_check_enabled: bool, max_len: int
    ):
        """
        This method checks if any of the dataframes exeeds size limit.
        In case the size limit is exceeded and size_check_enabled is True
        a warning is issued and the user is required to confirm if they'd
        like to proceed with the upload
        """
        # check if the dataset exceeds size limits
        warn_and_query = size_check_enabled and df_size_exceeds(dataset, max_len)
        if warn_and_query:
            LOG.warning(
                f'The dataset contains more than {max_len} datapoints. '
                f'Please allow for additional time to upload the dataset '
                f'and calculate statistical metrics. '
                f'To disable this message set the flag size_check_enabled to False. '
                f'\n\nAlternately, consider sampling the dataset. '
                f'If you plan to sample the dataset please ensure that the '
                f'representative sample captures all possible '
                f'categorical features, labels and numerical ranges that '
                f'would be encountered during deployment.'
                f'\n\nFor details on how datasets are used and considerations '
                f'for when large datasets are necessary, please refer to '
                f'https://docs.fiddler.ai/pages/user-guide/administration-concepts/project-structure/#dataset'
            )
            user_query = 'Would you like to proceed with the upload (y/n)? '
            return do_not_proceed(user_query)
        return False

    def _check_connection(self, check_client_version=True, check_server_version=True):
        return self.connection.check_connection(
            check_client_version, check_server_version
        )

    def _call_executor_service(
        self,
        path: List[str],
        json_payload: Any = None,
        files: Optional[List[Path]] = None,
        is_get_request: bool = False,
        stream: bool = False,
    ):
        return self.connection.call_executor_service(
            path, json_payload, files, is_get_request, stream
        )

    def _call(
        self,
        path: List[str],
        json_payload: Any = None,
        files: Optional[List[Path]] = None,
        is_get_request: bool = False,
        stream: bool = False,
        timeout: Optional[int] = None,
        num_tries: int = 1,
    ):
        """Issues a request to the API and returns the result,
        logigng and handling errors appropriately.

        Raises a RuntimeError if the response is a failure or cannot be parsed.
        Does not handle any ConnectionError exceptions thrown by the `requests`
        library.

        Note: Parameters `timeout` and `num_tries` are currently only utilized in a workaround
        for a bug involving Mac+Docker communication. See: https://github.com/docker/for-mac/issues/3448
        """
        return self.connection.call(
            path, json_payload, files, is_get_request, stream, timeout, num_tries
        )

    @deprecated(
        reason='Please use get_datasets, this method will be removed in future versions'
    )
    def list_datasets(self, project_id: str) -> List[str]:
        """List the ids of all datasets in the organization.

        :returns: List of strings containing the ids of each dataset.
        """
        return self.project(project_id).list_datasets()

    @deprecated(
        reason='Please use get_projects, this method will be removed in future versions'
    )
    def list_projects(self, get_project_details: bool = False) -> List[str]:
        """List the ids of all projects in the organization.

        :returns: List of strings containing the ids of each project.
        """
        path = ['list_projects', self.org_id]

        payload = {
            'project_details': get_project_details,
        }

        return self._call(path, json_payload=payload)['projects']

    def project(self, project_id):
        return Project(self.connection, project_id)

    @deprecated(
        reason='Please use get_models, this method will be removed in future versions'
    )
    def list_models(self, project_id: str) -> List[str]:
        """List the names of all models in a project.

        :param project_id: The unique identifier of the project on the Fiddler
            engine.
        :returns: List of strings containing the ids of each model in the
            specified project.
        """
        return self.project(project_id).list_models()

    @deprecated(
        reason='Please use get_dataset, this method will be removed in future versions'
    )
    def get_dataset_info(self, project_id: str, dataset_id: str) -> DatasetInfo:
        """Get DatasetInfo for a dataset.

        :param dataset_id: The unique identifier of the dataset on the Fiddler
            engine.

        :returns: A fiddler.DatasetInfo object describing the dataset.
        """
        return self.project(project_id).dataset(dataset_id).get_info()

    @deprecated(
        reason='Please use get_model, this method will be removed in future versions'
    )
    def get_model_info(self, project_id: str, model_id: str) -> ModelInfo:
        """Get ModelInfo for a model in a certain project.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.

        :returns: A fiddler.ModelInfo object describing the model.
        """
        return self.project(project_id).model(model_id).get_info()

    def _query_dataset(
        self,
        project_id: str,
        dataset_id: str,
        fields: List[str],
        max_rows: int,
        split: Optional[str] = None,
        sampling=False,
        sampling_seed=0.0,
    ):
        return (
            self.project(project_id)
            .dataset(dataset_id)
            ._query_dataset(fields, max_rows, split, sampling, sampling_seed)
        )

    @deprecated(
        reason='Please use get_slice, this method will be removed in future versions'
    )
    def get_dataset(
        self,
        project_id: str,
        dataset_id: str,
        max_rows: int = 1_000,
        splits: Optional[List[str]] = None,
        sampling=False,
        dataset_info: Optional[DatasetInfo] = None,
        include_fiddler_id=False,
    ) -> Dict[str, pd.DataFrame]:
        """Fetches data from a dataset on Fiddler.

        :param project_id: The unique identifier of the project on the Fiddler
            engine.
        :param dataset_id: The unique identifier of the dataset on the Fiddler
            engine.
        :param max_rows: Up to this many rows will be fetched from eash split
            of the dataset.
        :param splits: If specified, data will only be fetched for these
            splits. Otherwise, all splits will be fetched.
        :param sampling: If True, data will be sampled up to max_rows. If
            False, rows will be returned in order up to max_rows. The seed
            will be fixed for sampling.∂
        :param dataset_info: If provided, the API will skip looking up the
            DatasetInfo (a necessary precursor to requesting data).
        :param include_fiddler_id: Return the Fiddler engine internal id
            for each row. Useful only for debugging.

        :returns: A dictionary of str -> DataFrame that maps the name of
            dataset splits to the data in those splits. If len(splits) == 1,
            returns just that split as a dataframe, rather than a dataframe.
        """
        return (
            self.project(project_id)
            .dataset(dataset_id)
            .download(max_rows, splits, sampling, dataset_info, include_fiddler_id)
        )

    def delete_dataset(self, project_id: str, dataset_id: str):
        """Permanently delete a dataset.

        :param project_id: The unique identifier of the project on the Fiddler
            engine.
        :param dataset_id: The unique identifier of the dataset on the Fiddler
            engine.

        :returns: Server response for deletion action.
        """
        return self.project(project_id).dataset(dataset_id).delete()

    def delete_model(
        self, project_id: str, model_id: str, delete_prod=True, delete_pred=True
    ):
        """Permanently delete a model.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.
        :param delete_prod: Boolean value to delete the production table.
            By default this table is dropped.
        :param delete_pred: Boolean value to delete the prediction table.
            By default this table is dropped.

        :returns: Server response for deletion action.
        """
        return self.project(project_id).model(model_id).delete(delete_prod, delete_pred)

    def _delete_model_artifacts(self, project_id: str, model_id: str):
        """Permanently delete a model artifacts.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.

        :returns: Server response for deletion action.
        """
        return self.project(project_id).model(model_id)._delete_artifacts()

    def delete_project(self, project_id: str):
        """Permanently delete a project.

        :param project_id: The unique identifier of the project on the Fiddler
            engine.

        :returns: Server response for deletion action.
        """
        # Type enforcement
        return self.project(project_id).delete()

    ##### Start: Methods related to uploading dataset #####

    def _upload_dataset_files(
        self,
        project_id: str,
        dataset_id: str,
        file_paths: List[Path],
        dataset_info: Optional[DatasetInfo] = None,
    ):
        """Uploads data files to the Fiddler platform."""
        safe_name_check(dataset_id, constants.MAX_ID_LEN, self.strict_mode)

        payload: Dict[str, Any] = dict(dataset_name=dataset_id)

        if dataset_info is not None:
            if self.strict_mode:
                dataset_info.validate()

            payload['dataset_info'] = dict(dataset=dataset_info.to_dict())

        payload['split_test'] = False
        path = ['dataset_upload', self.org_id, project_id]

        LOG.info(f'Uploading the dataset {dataset_id} ...')

        result = self._call(path, json_payload=payload, files=file_paths)

        return result

    def get_mutual_information(
        self,
        project_id: str,
        dataset_id: str,
        features: list,
        normalized: Optional[bool] = False,
        slice_query: Optional[str] = None,
        sample_size: Optional[int] = None,
        seed: Optional[float] = 0.25,
    ):
        """
        The Mutual information measures the dependency between two random variables.
        It's a non-negative value. If two random variables are independent MI is equal to zero.
        Higher MI values means higher dependency.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param dataset_id: The unique identifier of the dataset in the
            Fiddler engine.
        :param features: list of features to compute mutual information with respect to all the variables in the dataset.
        :param normalized: If set to True, it will compute Normalized Mutual Information (NMI)
        :param slice_query: Optional slice query
        :param sample_size: Optional sample size for the selected dataset
        :param seed: Optional seed for sampling
        :return: a dictionary of mutual information w.r.t the given features.
        """
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)
        dataset_id = type_enforce('dataset_id', dataset_id, str)

        if isinstance(features, str):
            features = [features]
        if not isinstance(features, list):
            raise ValueError(
                f'Invalid type: {type(features)}. Argument features has to be a list'
            )
        correlation = {}
        for col_name in features:
            payload = dict(
                col_name=col_name,
                normalized=normalized,
                slice_query=slice_query,
                sample_size=sample_size,
                seed=seed,
            )
            path = ['dataset_mutual_information', self.org_id, project_id, dataset_id]
            res = self._call(path, json_payload=payload)
            correlation[col_name] = res
        return correlation

    @deprecated(
        reason='Please use add_project, this method will be removed in future versions'
    )
    def create_project(self, project_id: str):
        """Create a new project.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine. Must be a short string without whitespace.

        :returns: Server response for creation action.
        """
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)

        safe_name_check(project_id, constants.MAX_ID_LEN, self.strict_mode)
        res = None
        try:
            path = ['new_project', self.org_id, project_id]
            res = self._call(path)
        except Exception as e:
            if 'already exists' in str(e):
                LOG.error(
                    'Project name already exists, please try with a different name (You may not have access to all the projects)'
                )
            else:
                raise e

        return res

    ##### Start: Methods related to publishing event #####

    def _basic_drift_checks(self, project_id, model_info, model_id):
        # Lets make sure prediction table is created and has prediction data by
        # just running the slice query
        violations = []
        try:
            query_str = f'select * from "{model_info.datasets[0]}.{model_id}" limit 1'
            df = self.get_slice(
                query_str,
                project_id=project_id,
            )
            for index, row in df.iterrows():
                for out_col in model_info.outputs:
                    if out_col.name not in row:
                        msg = f'Drift error: {out_col.name} not in predictions table. Please delete and re-register your model.'
                        violations.append(
                            MonitoringViolation(MonitoringViolationType.WARNING, msg)
                        )
        except RuntimeError:
            msg = 'Drift error: Predictions table does not exists. Please run trigger_pre_computation for an existing model, or use register_model to register a new model.'
            violations.append(MonitoringViolation(MonitoringViolationType.WARNING, msg))
            return violations

        return violations

    def publish_event(
        self,
        project_id: str,
        model_id: str,
        event: dict,
        event_id: Optional[str] = None,
        update_event: Optional[bool] = None,
        event_timestamp: Optional[int] = None,
        timestamp_format: FiddlerTimestamp = FiddlerTimestamp.INFER,
        casting_type: Optional[bool] = False,
        dry_run: Optional[bool] = False,
    ):
        """
        Publishes an event to Fiddler Service.
        :param project_id: The project to which the model whose events are being published belongs
        :param model_id: The model whose events are being published
        :param dict event: Dictionary of event details, such as features and predictions.
        :param event_id: Unique str event id for the event
        :param update_event: Bool indicating if the event is an update to a previously published row
        :param event_timestamp: The UTC timestamp of the event in epoch milliseconds (e.g. 1609462800000)
        :param timestamp_format:   Format of timestamp within batch object. Can be one of:
                                - FiddlerTimestamp.INFER
                                - FiddlerTimestamp.EPOCH_MILLISECONDS
                                - FiddlerTimestamp.EPOCH_SECONDS
                                - FiddlerTimestamp.ISO_8601
        :param casting_type: Bool indicating if fiddler should try to cast the data in the event with
        the type referenced in model info. Default to False.
        :param dry_run: If true, the event isnt published and instead the user gets a report which shows
        IF the event along with the model would face any problems with respect to monitoring

        """
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)
        model_id = type_enforce('model_id', model_id, str)
        event = type_enforce('event', event, dict)
        if event_id:
            event_id = type_enforce('event_id', event_id, str)

        if casting_type:
            try:
                model_info = self.get_model_info(project_id, model_id)
            except RuntimeError:
                raise RuntimeError(
                    f'Did not find ModelInfo for project "{project_id}" and model "{model_id}".'
                )
            event = cast_input_data(event, model_info)

        if not timestamp_format or timestamp_format not in FiddlerTimestamp:
            raise ValueError('Please specify a valid timestamp_format')

        assert timestamp_format is not None, 'timestamp_format unexpectedly None'
        event['__timestamp_format'] = timestamp_format.value

        if update_event:
            event['__event_type'] = 'update_event'
            event['__updated_at'] = event_timestamp
            if event_id is None:
                raise ValueError('An update event needs an event_id')
        else:
            event['__event_type'] = 'execution_event'
            event['__occurred_at'] = event_timestamp

        if event_id is not None:
            event['__event_id'] = event_id

        if dry_run:
            violations = self._pre_flight_monitoring_check(project_id, model_id, event)
            violations_list = []
            LOG.info('\n****** publish_event dry_run report *****')
            LOG.info(f'Found {len(violations)} Violations:')
            for violation in violations:
                violations_list.append(
                    {'type': violation.type.value, 'desc': violation.desc}
                )
                LOG.info(f'Type: {violation.type.value: <11}{violation.desc}')
            result = json.dumps(violations_list)
        else:
            path = ['external_event', self.org_id, project_id, model_id]
            # The ._call uses `timeout` and `num_tries` logic due to an issue with Mac/Docker.
            # This is only enabled using the env variable `FIDDLER_RETRY_PUBLISH`; otherwise it
            # is a normal ._call function
            result = self._call(path, event, timeout=2, num_tries=5)

        return result

    def _pre_flight_monitoring_check(self, project_id, model_id, event):
        violations = []
        violations += self._basic_monitoring_tests(project_id, model_id)
        if len(violations) == 0:
            model_info = self.get_model_info(project_id, model_id)
            dataset_info = self.get_dataset_info(project_id, model_info.datasets[0])
            violations += self._basic_drift_checks(project_id, model_info, model_id)
            violations += self.monitoring_validator.pre_flight_monitoring_check(
                event, model_info, dataset_info
            )
        return violations

    def _basic_monitoring_tests(self, project_id, model_id):
        """Basic checks which would prevent monitoring from working altogether."""
        violations = []
        try:
            model_info = self.get_model_info(project_id, model_id)
        except RuntimeError:
            msg = f'Error: Model:{model_id} in project:{project_id} does not exist'
            violations.append(MonitoringViolation(MonitoringViolationType.FATAL, msg))
            return violations

        try:
            _ = self.get_dataset_info(project_id, model_info.datasets[0])
        except RuntimeError:
            msg = f'Error: Dataset:{model_info.datasets[0]} does not exist'
            violations.append(MonitoringViolation(MonitoringViolationType.FATAL, msg))
            return violations

        return violations

    def get_model(self, project_id: str, model_id: str, output_dir: Path):
        """
        download the model binary, package.py and model.yaml to the given
        output dir.

        :param project_id: project id
        :param model_id: model id
        :param output_dir: output directory
        :return: model artifacts
        """
        return self.project(project_id).model(model_id).download(output_dir)
