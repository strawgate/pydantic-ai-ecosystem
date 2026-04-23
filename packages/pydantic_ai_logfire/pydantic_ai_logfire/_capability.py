from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, cast

from pydantic_ai import Agent
from pydantic_ai.tools import AgentDepsT
from pydantic_ai_partner_mcp import MCPPartnerCapability, MCPPartnerConfig


@dataclass(frozen=True)
class LogfireConfig(MCPPartnerConfig):
    project_name: str | None = None
    environment: str | None = None
    trace_content: bool = False


@dataclass(init=False)
class LogfireCapability(MCPPartnerCapability[AgentDepsT]):
    """Provide Logfire-oriented instructions and MCP defaults."""

    partner_name: ClassVar[str] = 'Logfire'
    readonly_by_default: ClassVar[bool] = False

    def __init__(
        self,
        config: LogfireConfig | None = None,
        *,
        extra_instructions: tuple[str, ...] = (),
    ) -> None:
        super().__init__(config=config or LogfireConfig(), extra_instructions=extra_instructions)

    @classmethod
    def config_from_mapping(cls, config: Mapping[str, object]) -> MCPPartnerConfig:
        base = super().config_from_mapping(config)
        project_name = cls._read_optional_str(config, 'project_name')
        environment = cls._read_optional_str(config, 'environment')
        trace_content = cls._read_bool(config, 'trace_content', default=False)
        return LogfireConfig(
            url=base.url,
            id=base.id,
            authorization_token=base.authorization_token,
            headers=base.headers,
            allowed_tools=base.allowed_tools,
            description=base.description,
            project_name=project_name,
            environment=environment,
            trace_content=trace_content,
        )

    def get_partner_instructions(self) -> tuple[str, ...]:
        config = cast(LogfireConfig, self.config)
        parts = [
            'Use Logfire data to inspect traces, spans, tool calls, and agent runs.',
            'Keep investigations precise so the resulting queries and traces stay readable.',
        ]
        if config.project_name:
            parts.append(f'The default Logfire project is `{config.project_name}`.')
        if config.environment:
            parts.append(f'The default Logfire environment is `{config.environment}`.')
        if config.trace_content:
            parts.append(
                'Sensitive content may appear in traces, so handle queried trace content carefully.'
            )
        return tuple(parts)


def create_logfire_agent(
    model: str = 'openai:gpt-5.2',
    *,
    instructions: str = 'Help the user build observable agent workflows.',
    capability: LogfireCapability | None = None,
) -> Agent[None, str]:
    return Agent(
        model,
        instructions=instructions,
        capabilities=[capability or LogfireCapability()],
    )
