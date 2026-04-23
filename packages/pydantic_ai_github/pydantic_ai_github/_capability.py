from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, cast

from pydantic_ai import Agent
from pydantic_ai.tools import AgentDepsT
from pydantic_ai_partner_mcp import MCPPartnerCapability, MCPPartnerConfig


@dataclass(frozen=True)
class GitHubConfig(MCPPartnerConfig):
    owner: str | None = None
    repo: str | None = None
    allow_writes: bool = False


@dataclass(init=False)
class GitHubCapability(MCPPartnerCapability[AgentDepsT]):
    """Provide GitHub-specific instructions and safety defaults."""

    partner_name: ClassVar[str] = 'GitHub'

    def __init__(
        self,
        config: GitHubConfig | None = None,
        *,
        extra_instructions: tuple[str, ...] = (),
    ) -> None:
        super().__init__(config=config or GitHubConfig(), extra_instructions=extra_instructions)

    @classmethod
    def config_from_mapping(cls, config: Mapping[str, object]) -> MCPPartnerConfig:
        base = super().config_from_mapping(config)
        owner = cls._read_optional_str(config, 'owner')
        repo = cls._read_optional_str(config, 'repo')
        allow_writes = cls._read_bool(config, 'allow_writes', default=False)
        return GitHubConfig(
            url=base.url,
            id=base.id,
            authorization_token=base.authorization_token,
            headers=base.headers,
            allowed_tools=base.allowed_tools,
            description=base.description,
            owner=owner,
            repo=repo,
            allow_writes=allow_writes,
        )

    def is_readonly_by_default(self) -> bool:
        return not cast(GitHubConfig, self.config).allow_writes

    def get_partner_instructions(self) -> tuple[str, ...]:
        config = cast(GitHubConfig, self.config)
        parts = [
            'Scope GitHub operations to the configured repository when one is provided.',
        ]
        if config.owner and config.repo:
            parts.append(f'The default repository is `{config.owner}/{config.repo}`.')
        if config.allow_writes:
            parts.append('Write operations are allowed when they are clearly requested.')
        return tuple(parts)


def create_github_agent(
    model: str = 'openai:gpt-5.2',
    *,
    instructions: str = 'Help the user inspect and manage GitHub work.',
    capability: GitHubCapability | None = None,
) -> Agent[None, str]:
    return Agent(
        model,
        instructions=instructions,
        capabilities=[capability or GitHubCapability()],
    )
