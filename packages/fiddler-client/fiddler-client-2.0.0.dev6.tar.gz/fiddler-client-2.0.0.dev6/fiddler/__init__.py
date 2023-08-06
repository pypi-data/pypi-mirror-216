"""
Fiddler Client Module
=====================

A Python client for Fiddler service.

TODO: Add Licence.
"""

from fiddler import utils
from fiddler._version import __version__
from fiddler.client import Fiddler, PredictionEventBundle
from fiddler.core_objects import (
    ArtifactStatus,
    BaselineType,
    BatchPublishType,
    Column,
    CustomFeature,
    DatasetInfo,
    DataType,
    DeploymentType,
    ExplanationMethod,
    FiddlerPublishSchema,
    FiddlerTimestamp,
    ModelInfo,
    ModelInputType,
    ModelTask,
    WeightingParams,
    WindowSize,
)
from fiddler.exceptions import NotSupported
from fiddler.fiddler_api import FiddlerApi as FiddlerApiV1
from fiddler.packtools import gem
from fiddler.utils import ColorLogger
from fiddler.v2.api.api import FiddlerClient
from fiddler.v2.api.explainability_mixin import (
    DatasetDataSource,
    RowDataSource,
    SqlSliceQueryDataSource,
)
from fiddler.v2.constants import CSV_EXTENSION, FileType
from fiddler.v2.schema.alert import (
    AlertCondition,
    AlertType,
    BinSize,
    ComparePeriod,
    CompareTo,
    Metric,
    Priority,
)
from fiddler.v2.schema.job import JobStatus
from fiddler.v2.schema.model_deployment import DeploymentParams, ModelDeployment
from fiddler.v2.utils.helpers import match_semver, raise_not_supported
from fiddler.validator import (
    PackageValidator,
    ValidationChainSettings,
    ValidationModule,
)

logger = utils.logging.getLogger(__name__)

SUPPORTED_API_VERSIONS = ['v2']


__all__ = [
    '__version__',
    'BatchPublishType',
    'Column',
    'CustomFeature',
    'ColorLogger',
    'DatasetInfo',
    'DataType',
    'Fiddler',
    'FiddlerClient',
    'FiddlerTimestamp',
    'FiddlerPublishSchema',
    'gem',
    'ModelInfo',
    'ModelInputType',
    'ModelTask',
    'WeightingParams',
    'ExplanationMethod',
    'PredictionEventBundle',
    'PackageValidator',
    'ValidationChainSettings',
    'ValidationModule',
    'utils',
    # Exposing constants
    'CSV_EXTENSION',
]
