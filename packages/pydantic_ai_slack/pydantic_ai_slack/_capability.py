from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, cast

from pydantic_ai import Agent
from pydantic_ai.tools import AgentDepsT
from pydantic_ai_partner_mcp import MCPPartnerCapability, MCPPartnerConfig

if TYPE_CHECKING:
    from pydantic_ai.mcp import MCPServer
    from pydantic_ai.toolsets.fastmcp import FastMCPToolset


@dataclass(frozen=True)
class SlackConfig(MCPPartnerConfig):
    workspace_name: str | None = None
    default_channel: str | None = None
    allow_posting: bool = False


@dataclass(init=False)
class SlackCapability(MCPPartnerCapability[AgentDepsT]):
    """Provide Slack-specific instructions and safety defaults."""

    partner_name: ClassVar[str] = 'Slack'

    def __init__(
        self,
        config: SlackConfig | None = None,
        *,
        extra_instructions: tuple[str, ...] = (),
        local_toolset: MCPServer | FastMCPToolset[AgentDepsT] | None = None,
    ) -> None:
        super().__init__(
            config=config or SlackConfig(),
            extra_instructions=extra_instructions,
            local_toolset=local_toolset,
        )

    @classmethod
    def config_from_mapping(cls, config: Mapping[str, object]) -> MCPPartnerConfig:
        base = super().config_from_mapping(config)
        workspace_name = cls._read_optional_str(config, 'workspace_name')
        default_channel = cls._read_optional_str(config, 'default_channel')
        allow_posting = cls._read_bool(config, 'allow_posting', default=False)
        return SlackConfig(
            url=base.url,
            id=base.id,
            authorization_token=base.authorization_token,
            headers=base.headers,
            allowed_tools=base.allowed_tools,
            description=base.description,
            workspace_name=workspace_name,
            default_channel=default_channel,
            allow_posting=allow_posting,
        )

    def is_readonly_by_default(self) -> bool:
        return not cast(SlackConfig, self.config).allow_posting

    def get_partner_instructions(self) -> tuple[str, ...]:
        config = cast(SlackConfig, self.config)
        parts = [
            'Prefer replying in the existing thread when one is available.',
        ]
        if config.workspace_name:
            parts.append(f'The default workspace is `{config.workspace_name}`.')
        if config.default_channel:
            parts.append(f'The default channel is `{config.default_channel}`.')
        if config.allow_posting:
            parts.append('Posting messages is allowed when it is useful and clearly requested.')
        return tuple(parts)


def create_slack_agent(
    model: str = 'openai:gpt-5.2',
    *,
    instructions: str = 'Help the user work with Slack conversations and workflows.',
    capability: SlackCapability | None = None,
) -> Agent[None, str]:
    return Agent(
        model,
        instructions=instructions,
        capabilities=[capability or SlackCapability()],
    )
