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
class NotionConfig(MCPPartnerConfig):
    workspace_name: str | None = None
    allow_writes: bool = False


@dataclass(init=False)
class NotionCapability(MCPPartnerCapability[AgentDepsT]):
    """Provide Notion-specific instructions and safety defaults."""

    partner_name: ClassVar[str] = 'Notion'

    def __init__(
        self,
        config: NotionConfig | None = None,
        *,
        extra_instructions: tuple[str, ...] = (),
        local_toolset: MCPServer | FastMCPToolset[AgentDepsT] | None = None,
    ) -> None:
        super().__init__(
            config=config or NotionConfig(),
            extra_instructions=extra_instructions,
            local_toolset=local_toolset,
        )

    @classmethod
    def config_from_mapping(cls, config: Mapping[str, object]) -> MCPPartnerConfig:
        base = super().config_from_mapping(config)
        workspace_name = cls._read_optional_str(config, 'workspace_name')
        allow_writes = cls._read_bool(config, 'allow_writes', default=False)
        return NotionConfig(
            url=base.url,
            id=base.id,
            authorization_token=base.authorization_token,
            headers=base.headers,
            allowed_tools=base.allowed_tools,
            description=base.description,
            workspace_name=workspace_name,
            allow_writes=allow_writes,
        )

    def is_readonly_by_default(self) -> bool:
        return not cast(NotionConfig, self.config).allow_writes

    def get_partner_instructions(self) -> tuple[str, ...]:
        config = cast(NotionConfig, self.config)
        parts = [
            'Prefer updating existing pages and databases before creating new ones.',
        ]
        if config.workspace_name:
            parts.append(f'The default workspace is `{config.workspace_name}`.')
        if config.allow_writes:
            parts.append('Write operations are allowed when they are clearly requested.')
        return tuple(parts)


def create_notion_agent(
    model: str = 'openai:gpt-5.2',
    *,
    instructions: str = 'Help the user work with Notion content and workspace knowledge.',
    capability: NotionCapability | None = None,
) -> Agent[None, str]:
    return Agent(
        model,
        instructions=instructions,
        capabilities=[capability or NotionCapability()],
    )
