import json
import os
import tempfile
import time
from http import HTTPStatus
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import yaml
from requests_toolbelt.multipart.encoder import MultipartEncoder

from fiddler.core_objects import DatasetInfo, DEFAULT_MAX_INFERRED_CARDINALITY
from fiddler.exceptions import FiddlerAPIHTTPException
from fiddler.libs.http_client import RequestClient
from fiddler.utils import logging
from fiddler.v2.api.helpers import multipart_upload
from fiddler.v2.constants import FileType, UploadType
from fiddler.v2.schema.dataset import Dataset, DatasetIngest
from fiddler.v2.utils.decorators import handle_api_error_response
from fiddler.v2.utils.response_handler import (
    APIResponseHandler,
    PaginatedResponseHandler,
)
from fiddler.v2.validators.dataset_validator import (
    validate_dataset_columns,
    validate_dataset_info,
    validate_dataset_shape,
)

DEFAULT_NROWS_PER_CHUNK = 100000
DEFAULT_SAMPLE_SIZE = 20000
logger = logging.getLogger(__name__)


class DatasetMixin:
    client: RequestClient
    organization_name: str

    @handle_api_error_response
    def get_datasets(self, project_name: str) -> List[Dataset]:
        """
        Get all the datasets in a project

        :param project_name:    The project for which you want to get the datasets
        :returns:               A list containing `Dataset` objects.
        """
        response = self.client.get(
            url='datasets',
            params={
                'organization_name': self.organization_name,
                'project_name': project_name,
            },
        )
        items = PaginatedResponseHandler(response).get_pagination_items()
        datasets = [Dataset.from_dict(item) for item in items]
        return datasets

    @handle_api_error_response
    def get_dataset_names(self, project_name: str) -> List[str]:
        """List the names of all datasets in the organization.

        :param project_name: The project for which you want to get the datasets
        :returns: List of strings containing the names of each dataset.
        """
        datasets = self.get_datasets(project_name=project_name)
        return [d.name for d in datasets]

    @handle_api_error_response
    def get_dataset(self, project_name: str, dataset_name: str) -> Dataset:
        """
        Get all the details for a given dataset

        :param project_name:    The project to which the dataset belongs to
        :param dataset_name:    The dataset name of which you need the details

        :returns: Dataset object which contains the details
        """

        response = self.client.get(
            url=f'datasets/{self.organization_name}:{project_name}:{dataset_name}',
        )
        response_handler = APIResponseHandler(response)
        return Dataset.deserialize(response_handler)

    @handle_api_error_response
    def get_dataset_info(self, project_name: str, dataset_name: str) -> DatasetInfo:
        """
        Get DatasetInfo for a dataset.

        :param project_name:    The project to which the dataset belongs to
        :param dataset_name:    The dataset name of which you need the details

        :returns: A fiddler.DatasetInfo object describing the dataset.
        """
        dataset = self.get_dataset(project_name, dataset_name)
        return dataset.info

    @handle_api_error_response
    def add_dataset(
        self,
        name: str,
        project_name: str,
        info: Optional[DatasetInfo] = None,
    ) -> Dataset:
        request_body = dict(
            name=name,
            project_name=project_name,
            organization_name=self.organization_name,
            info=info,
        )

        response = self.client.post(
            url='datasets',
            data=request_body,
        )
        logger.info(f'{name} dataset created')
        return Dataset.deserialize(APIResponseHandler(response))

    @handle_api_error_response
    def delete_dataset(self, project_name: str, dataset_name: str) -> None:
        """
        Delete a dataset

        :param project_name:    The project to which the dataset belongs to
        :param dataset_name:    The dataset name which you want to delete

        :returns: None
        """

        response = self.client.delete(
            url=f'datasets/{self.organization_name}:{project_name}:{dataset_name}',
        )
        if response.status_code == HTTPStatus.OK:
            logger.info(f'{dataset_name} deleted successfully.')
        else:
            # @TODO: Handle non 200 status response
            logger.info('Delete unsuccessful')

    @handle_api_error_response
    def upload_dataset(
        self,
        project_name: str,
        dataset_name: str,
        files: Dict[str, Path],
        info: DatasetInfo,
        file_type: Optional[FileType] = None,
        file_schema: Optional[dict] = None,
        is_sync: Optional[bool] = True,
    ) -> Dict[str, str]:
        """
        Upload a dataset.

        :param project_name:   The project to which the dataset belongs to
        :param dataset_name:   Dataset name used for upload
        :param files:          A dictionary of file name and key and file path as value.
                               Eg `{'train': pathlib.Path('datasets/train.csv')}`
        :param info:           DatasetInfo object
        :param file_type:      FileType which specifices the filetype csv etc.
        :param file_schema:    <TBD>
        :param is_sync:        A boolean value which determines if the upload method
                               works in synchronous mode or async mode

        :returns:              Dictionary containing details of the job used to publish
                               events incase of 202 response from the server.
        """
        validate_dataset_info(info)
        validate_dataset_shape(files)

        file_names = []
        for _, file_path in files.items():
            _, file_name = os.path.split(file_path)
            validate_dataset_columns(info, file_path)
            response = multipart_upload(
                client=self.client,
                organization_name=self.organization_name,
                project_name=project_name,
                identifier=dataset_name,
                upload_type=UploadType.DATASET.value,
                file_path=str(file_path),
                file_name=file_name,
            )
            file_names.append(response.get('file_name'))

        request_body = DatasetIngest(
            name=dataset_name,
            file_name=file_names,
            info=info,
            file_type=file_type,
            file_schema=file_schema,
        ).to_dict()
        response = self.client.post(
            url=f'datasets/{self.organization_name}:{project_name}:{dataset_name}/ingest',
            data=json.dumps(request_body),
        )
        # @TODO: Handle invalid file path exception
        if response.status_code == HTTPStatus.ACCEPTED:
            resp = APIResponseHandler(response).get_data()
            if is_sync:
                job_uuid = resp['job_uuid']
                job_name = f'Dataset[{project_name}/{dataset_name}] - Upload dataset'
                logger.info(
                    'Dataset[%s/%s] - Submitted job (%s) for uploading dataset',
                    project_name,
                    dataset_name,
                    job_uuid,
                )

                job = self.wait_for_job(uuid=job_uuid, job_name=job_name).get_data()
                job.pop('extras', None)
                time.sleep(20)
                return job
            else:
                return resp
        else:
            # raising a generic FiddlerAPIHTTPException
            logger.error(f'Failed to upload dataset {dataset_name}.')
            raise FiddlerAPIHTTPException(
                response.status_code,
                error_code=response.status_code,
                message=response.content,
                errors=[],
            )

    @handle_api_error_response
    def upload_dataset_csv(
        self,
        project_name: str,
        dataset_name: str,
        files: Dict[str, Path],
        info: Optional[DatasetInfo] = None,
        file_schema: Optional[dict] = None,
        is_sync: Optional[bool] = True,
    ) -> Dict[str, str]:
        """
        Upload dataset as csv file

        :param project_name:    The project to which the dataset belongs to
        :param dataset_name:    Dataset name used for upload
        :param files:           A dictionary of pathlib.Path as value and name as key. Eg `{'train': pathlib.Path('datasets/train.csv')}`
        :param info:            DatasetInfo object
        :param is_sync:         A boolean value which determines if the upload method works in synchronous mode or async mode

        :returns:               Dictionary containing details of the job used to publish events incase of 202 response from the server.
        """
        if not files:
            raise ValueError('`files` is empty. Please enter a valid input')

        return self.upload_dataset(
            project_name, dataset_name, files, info, FileType.CSV, file_schema, is_sync
        )

    @handle_api_error_response
    def upload_dataset_from_dataframe(
        self,
        project_name: str,
        dataset_name: str,
        datasets: Dict[str, pd.DataFrame],
        info: Optional[DatasetInfo] = None,
        wait: Optional[bool] = True,
    ) -> Dict[str, str]:
        """
        Upload dataset as pd.DataFrame

        :param project_name:    The project to which the dataset belongs to
        :param dataset_name:    Dataset name used for upload
        :param datasets:        A dictionary of dataframe as value and name as key. Eg `{'train': train_df}`
        :param info:            DatasetInfo object
        :param wait:         A boolean value which determines if the upload method works in synchronous mode or async mode

        :returns:               Dictionary containing details of the job used to publish events incase of 202 response from the server.
        """
        if not datasets:
            raise ValueError('`datasets` is empty. Please enter a valid dataset')

        # will throw FiddlerAPIHTTPException if project does not exist
        self.client.get(url=f'projects/{self.organization_name}:{project_name}')

        with tempfile.TemporaryDirectory() as tmp:
            files = {}
            file_type = FileType.CSV
            for name, df in datasets.items():
                file_path = Path(tmp) / f'{name}{file_type.value}'
                df.to_csv(file_path, index=False)
                files[name] = file_path

            return self.upload_dataset(
                project_name,
                dataset_name,
                files=files,
                info=info,
                file_type=file_type,
                is_sync=wait,
            )

    @handle_api_error_response
    def upload_dataset_from_dir(
        self,
        project_name: str,
        dataset_name: str,
        dataset_dir: Path,
        file_type: FileType = FileType.CSV,
        file_schema: Optional[dict] = None,
        is_sync: bool = True,
    ) -> Dict[str, str]:
        """
        Upload dataset artefacts (data file and dataset info yaml) from a directory

        :param project_name:    The project to which the dataset belongs to
        :param dataset_name:    Dataset name used for upload
        :param dataset_dir:     pathlib.Path pointing to the dataset dir to be uploaded
        :param file_type:       FileType
        :param file_schema:     <TBD>
        :param is_sync:         A boolean value which determines if the upload method works in synchronous mode or async mode

        :returns:               Dictionary containing details of the job used to publish events incase of 202 response from the server.
        """
        # @TODO: Move repetative input validation used accross different methods to utils

        if file_type != FileType.CSV:
            raise NotImplementedError('Only CSV filetype is supported')

        if not dataset_dir.is_dir():
            raise ValueError(f'{dataset_dir} is not a directory')

        files = {
            data_file.name: data_file
            for data_file in dataset_dir.glob(f'*{file_type.value}')
        }

        if not files:
            raise ValueError(f'No data files found in {dataset_dir}.')

        info_yaml = dataset_dir / f'{dataset_name}.yaml'

        if not info_yaml.exists():
            raise ValueError(f'DatasetInfo yaml ({info_yaml}) not found.')

        with open(info_yaml) as f:
            info = DatasetInfo.from_dict(yaml.safe_load(f))

        return self.upload_dataset(
            project_name=project_name,
            dataset_name=dataset_name,
            files=files,
            info=info,
            file_schema=file_schema,
            is_sync=is_sync,
        )

    @handle_api_error_response
    def infer_dataset_info(
        self,
        file_path: str,
        display_name: str,
        dataset_id: Optional[str],
        max_inferred_cardinality: Optional[int] = DEFAULT_MAX_INFERRED_CARDINALITY,
        sample_size: Optional[int] = DEFAULT_SAMPLE_SIZE,
        chunk_size: Optional[int] = DEFAULT_NROWS_PER_CHUNK,
    ) -> DatasetInfo:
        """
        Derives DatasetInfo from the given csv file

        :param file_path:       Relative or absolute path of the file in string format, for example, 'datasets/train.csv'
        :param display_name:    A name for user-facing display (different from an id).
        :param dataset_id:      Dataset Id

        :returns:               DatasetInfo derived from the input file_path
        """
        if not file_path:
            raise ValueError('`file_path` is empty. Please enter a valid input.')

        file_path = Path(file_path)

        if not file_path.exists():
            raise ValueError('`file_path` does not exist. Please enter a valid input.')

        # TODO (pradhuman): Read from dir

        dataset_infos:List[DatasetInfo] = []
        # 1. read file
        with pd.read_csv(file_path, chunksize=chunk_size) as reader:
            for df in reader:
                logger.info(f'Read a chunk from input {df.shape}')
                # 2. take random sample
                if df.shape[0] > sample_size:
                    random_sample = df.sample(sample_size)
                    temp_dir = tempfile.TemporaryDirectory()
                    sample_file_path = os.path.join(temp_dir.name, file_path.name)
                    random_sample.to_csv(sample_file_path, index=False)
                    file_path_server_inference = Path(sample_file_path)
                else:
                    file_path_server_inference = file_path

                # 3. detect type
                files_encoders: Dict[str, MultipartEncoder] = {
                    'file': MultipartEncoder(
                        fields={
                            'file': (
                                file_path_server_inference.name,
                                open(file_path_server_inference, 'rb'),
                                'text/plain',
                            ),
                        }
                    )
                }
                request_body = dict(
                    name=display_name
                )
                response = self.client.post(
                    url='infer-data-types', data=request_body, files_encoders=files_encoders
                )
                api_response = APIResponseHandler(response)
                logger.info(api_response.get_status_code)
                dataset_infos.append(DatasetInfo.from_dict(api_response.get_data()))
        logger.info(f'combining {len(dataset_infos)} DatasetInfo objects')
        return DatasetInfo.as_combination(infos=dataset_infos, display_name=display_name)
