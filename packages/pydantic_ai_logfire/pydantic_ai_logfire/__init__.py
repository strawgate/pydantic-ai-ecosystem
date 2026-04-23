from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _metadata_version

from ._capability import LogfireCapability, LogfireConfig, create_logfire_agent

__all__ = (
    'LogfireCapability',
    'LogfireConfig',
    'create_logfire_agent',
    '__version__',
)

try:
    __version__ = _metadata_version('pydantic-ai-logfire')
except PackageNotFoundError:  # pragma: no cover
    __version__ = '0.0.0'
