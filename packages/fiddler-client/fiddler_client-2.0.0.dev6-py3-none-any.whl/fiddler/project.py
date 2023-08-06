from typing import List

from fiddler.connection import Connection
from fiddler.dataset import Dataset
from fiddler.model import Model
from fiddler.utils.general_checks import type_enforce


class Project:
    def __init__(self, connection: Connection, project_id: str):
        self.connection = connection
        self.project_id = project_id

    def list_models(self) -> List[str]:
        """List the names of all models in a project.

        :returns: List of strings containing the ids of each model in the
            specified project.
        """
        project_id = type_enforce('project_id', self.project_id, str)
        path = ['list_models', self.connection.org_id, project_id]
        res = self.connection.call(path, is_get_request=True)
        return res

    def delete(self):
        """Permanently delete a project.
        :returns: Server response for deletion action.
        """
        # Type enforcement
        project_id = type_enforce('project_id', self.project_id, str)
        path = ['delete_project', self.connection.org_id, project_id]
        result = self.connection.call(path)
        return result

    def list_datasets(self) -> List[str]:
        """List the ids of all datasets in the organization.

        :returns: List of strings containing the ids of each dataset.
        """
        # Type enforcement
        project_id = type_enforce('project_id', self.project_id, str)

        path = ['list_datasets', self.connection.org_id, project_id]
        res = self.connection.call(path, is_get_request=True)

        return res

    def model(self, model_id: str) -> Model:
        return Model(self.connection, self.project_id, model_id)

    def dataset(self, dataset_id: str) -> Dataset:
        return Dataset(self.connection, self.project_id, dataset_id)
