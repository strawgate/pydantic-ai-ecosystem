from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _metadata_version

from ._capability import GitHubCapability, GitHubConfig, create_github_agent

__all__ = (
    'GitHubCapability',
    'GitHubConfig',
    'create_github_agent',
    '__version__',
)

try:
    __version__ = _metadata_version('pydantic-ai-github')
except PackageNotFoundError:  # pragma: no cover
    __version__ = '0.0.0'
