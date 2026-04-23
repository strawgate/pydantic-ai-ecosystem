from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _metadata_version

from ._capability import LocalStackCapability, create_localstack_agent, create_localstack_mcp_server

__all__ = (
    'LocalStackCapability',
    'create_localstack_agent',
    'create_localstack_mcp_server',
    '__version__',
)

try:
    __version__ = _metadata_version('pydantic-ai-localstack')
except PackageNotFoundError:  # pragma: no cover
    __version__ = '0.0.0'
