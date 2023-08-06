import os
import tarfile
import tempfile
from pathlib import Path

import requests

from fiddler.connection import Connection
from fiddler.core_objects import ModelInfo
from fiddler.utils.general_checks import type_enforce


class Model:
    def __init__(self, connection: Connection, project_id: str, model_id):
        self.connection = connection
        self.project_id = project_id
        self.model_id = model_id

    def get_info(self) -> ModelInfo:
        """Get ModelInfo for a model in a certain project.

        :returns: A fiddler.ModelInfo object describing the model.
        """
        # Type enforcement
        project_id = type_enforce('project_id', self.project_id, str)
        model_id = type_enforce('model_id', self.model_id, str)

        path = ['model_info', self.connection.org_id, project_id, model_id]
        res = self.connection.call(path, is_get_request=True)
        return ModelInfo.from_dict(res)

    def delete(self, delete_prod=False, delete_pred=True):
        """Permanently delete a model.

        :param delete_prod: Boolean value to delete the production table.
            By default this table is not dropped.
        :param delete_pred: Boolean value to delete the prediction table.
            By default this table is dropped.

        :returns: Server response for deletion action.
        """
        # Type enforcement
        project_id = type_enforce('project_id', self.project_id, str)
        model_id = type_enforce('model_id', self.model_id, str)

        payload = {
            'project_id': project_id,
            'model_id': model_id,
            'delete_prod': delete_prod,
            'delete_pred': delete_pred,
        }

        path = ['delete_model', self.connection.org_id, project_id, model_id]
        try:
            result = self.connection.call(path, json_payload=payload)
        except Exception:
            # retry on error
            result = self.connection.call(path, json_payload=payload)

        self._delete_artifacts()

        # wait for ES to come back healthy
        for i in range(3):
            try:
                self.connection.call_executor_service(
                    ['deploy', self.connection.org_id], is_get_request=True
                )
                break
            except Exception:
                pass

        return result

    def _delete_artifacts(self):
        """Permanently delete a model artifacts.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.

        :returns: Server response for deletion action.
        """
        # delete from executor service cache
        # Type enforcement
        project_id = type_enforce('project_id', self.project_id, str)
        model_id = type_enforce('model_id', self.model_id, str)

        path = ['delete_model_artifacts', self.connection.org_id, project_id, model_id]
        result = self.connection.call_executor_service(path)

        return result

    def download(self, output_dir: Path):
        """
        download the model binary, package.py and model.yaml to the given
        output dir.

        :param output_dir: output directory
        :return: model artifacts
        """
        # Type enforcement
        project_id = type_enforce('project_id', self.project_id, str)
        model_id = type_enforce('model_id', self.model_id, str)
        output_dir = type_enforce('output_dir', output_dir, Path)

        if output_dir.exists():
            raise ValueError(f'output dir already exists {output_dir}')

        headers = dict()
        headers.update(self.connection.auth_header)

        _, tfile = tempfile.mkstemp('.tar.gz')
        url = f'{self.connection.url}/get_model/{self.connection.org_id}/{project_id}/{model_id}'

        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(tfile, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    f.write(chunk)

        tar = tarfile.open(tfile)
        output_dir.mkdir(parents=True)
        tar.extractall(path=output_dir)
        tar.close()
        os.remove(tfile)
        return True

    def _trigger_model_predictions(self, dataset_id: str):
        """Makes the Fiddler service compute and cache model predictions on a
        dataset."""
        # Type enforcement
        project_id = type_enforce('project_id', self.project_id, str)
        model_id = type_enforce('model_id', self.model_id, str)
        dataset_id = type_enforce('dataset_id', dataset_id, str)

        return self.connection.call_executor_service(
            ['dataset_predictions', self.connection.org_id, project_id],
            dict(model=model_id, dataset=dataset_id),
        )
