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
class PlaywrightConfig(MCPPartnerConfig):
    base_url: str | None = None
    browser_name: str | None = None
    allow_form_actions: bool = False


@dataclass(init=False)
class PlaywrightCapability(MCPPartnerCapability[AgentDepsT]):
    """Provide Playwright-specific instructions and safety defaults."""

    partner_name: ClassVar[str] = 'Playwright'

    def __init__(
        self,
        config: PlaywrightConfig | None = None,
        *,
        extra_instructions: tuple[str, ...] = (),
        local_toolset: MCPServer | FastMCPToolset[AgentDepsT] | None = None,
    ) -> None:
        super().__init__(
            config=config or PlaywrightConfig(),
            extra_instructions=extra_instructions,
            local_toolset=local_toolset,
        )

    @classmethod
    def config_from_mapping(cls, config: Mapping[str, object]) -> MCPPartnerConfig:
        base = super().config_from_mapping(config)
        base_url = cls._read_optional_str(config, 'base_url')
        browser_name = cls._read_optional_str(config, 'browser_name')
        allow_form_actions = cls._read_bool(config, 'allow_form_actions', default=False)
        return PlaywrightConfig(
            url=base.url,
            id=base.id,
            authorization_token=base.authorization_token,
            headers=base.headers,
            allowed_tools=base.allowed_tools,
            description=base.description,
            base_url=base_url,
            browser_name=browser_name,
            allow_form_actions=allow_form_actions,
        )

    def is_readonly_by_default(self) -> bool:
        return not cast(PlaywrightConfig, self.config).allow_form_actions

    def get_partner_instructions(self) -> tuple[str, ...]:
        config = cast(PlaywrightConfig, self.config)
        parts = [
            (
                'Prefer inspecting and snapshotting pages before clicking, typing, '
                'or submitting forms.'
            ),
        ]
        if config.base_url:
            parts.append(f'The default site is `{config.base_url}`.')
        if config.browser_name:
            parts.append(
                f'Prefer the `{config.browser_name}` browser when the MCP server offers it.'
            )
        if config.allow_form_actions:
            parts.append('Form actions are allowed when they are clearly requested.')
        return tuple(parts)


def create_playwright_agent(
    model: str = 'openai:gpt-5.2',
    *,
    instructions: str = (
        'Help the user inspect pages and automate browser flows with '
        'Playwright MCP tools.'
    ),
    capability: PlaywrightCapability | None = None,
) -> Agent[None, str]:
    return Agent(
        model,
        instructions=instructions,
        capabilities=[capability or PlaywrightCapability()],
    )
