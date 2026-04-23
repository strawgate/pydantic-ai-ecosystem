from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _metadata_version

from ._capability import MCPPartnerCapability, MCPPartnerConfig

__all__ = (
    'MCPPartnerCapability',
    'MCPPartnerConfig',
    '__version__',
)

try:
    __version__ = _metadata_version('pydantic-ai-partner-mcp')
except PackageNotFoundError:  # pragma: no cover
    __version__ = '0.0.0'
