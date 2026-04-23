from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _metadata_version

from ._capability import SlackCapability, SlackConfig, create_slack_agent

__all__ = (
    'SlackCapability',
    'SlackConfig',
    'create_slack_agent',
    '__version__',
)

try:
    __version__ = _metadata_version('pydantic-ai-slack')
except PackageNotFoundError:  # pragma: no cover
    __version__ = '0.0.0'
