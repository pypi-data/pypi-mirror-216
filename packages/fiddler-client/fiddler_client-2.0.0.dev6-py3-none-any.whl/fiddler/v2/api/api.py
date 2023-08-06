from urllib.parse import urljoin

from fiddler._version import __version__
from fiddler.libs.http_client import RequestClient
from fiddler.utils import logging
from fiddler.v2.api.alert_mixin import AlertMixin
from fiddler.v2.api.baseline_mixin import BaselineMixin
# @todo: This is v1 implementation needs to have a proper v2 approach
from fiddler.v2.api.dataset_mixin import DatasetMixin
from fiddler.v2.api.events_mixin import EventsMixin
from fiddler.v2.api.explainability_mixin import ExplainabilityMixin
from fiddler.v2.api.job_mixin import JobMixin
from fiddler.v2.api.model_deployment_mixin import ModelDeploymentMixin
from fiddler.v2.api.model_mixin import ModelMixin
from fiddler.v2.api.project_mixin import ProjectMixin
from fiddler.v2.constants import CURRENT_API_VERSION, FIDDLER_CLIENT_VERSION_HEADER
from fiddler.v2.schema.server_info import ServerInfo
from fiddler.v2.utils.helpers import match_semver, raise_not_supported

logger = logging.getLogger(__name__)


class FiddlerClient(
    ModelMixin,
    DatasetMixin,
    ProjectMixin,
    EventsMixin,
    JobMixin,
    BaselineMixin,
    AlertMixin,
    ExplainabilityMixin,
    ModelDeploymentMixin,
):
    def __init__(
        self,
        url: str,
        organization_name: str,
        auth_token: str,
        timeout: int = None,
        verify: bool = True,
    ) -> None:
        self.url = (
            url
            if url.endswith(CURRENT_API_VERSION)
            else urljoin(url, CURRENT_API_VERSION)
        )
        self.auth_token = auth_token
        self.organization_name = organization_name
        self.request_headers = {'Authorization': f'Bearer {auth_token}'}
        self.request_headers.update({FIDDLER_CLIENT_VERSION_HEADER: f'{__version__}'})
        self.timeout = timeout
        self.client = RequestClient(
            base_url=self.url, headers=self.request_headers, verify=verify
        )

        self.server_info: ServerInfo = self._get_server_info()
        self._check_server_version()

    def _get_server_info(self) -> ServerInfo:
        response = self.client.get(
            url='server-info',
            params={'organization_name': self.organization_name},
        )

        return ServerInfo(**response.json().get('data'))

    def _check_server_version(self) -> bool:
        if match_semver(
            self.server_info.server_version,
            '<23.2.0',
        ):
            raise_not_supported(
                compatible_client_version='1.8',
                client_version=__version__,
                server_version=self.server_info.server_version,
            )
