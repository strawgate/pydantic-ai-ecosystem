from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar, cast

from pydantic_ai.capabilities import MCP, AbstractCapability
from pydantic_ai.tools import AgentBuiltinTool, AgentDepsT
from pydantic_ai.toolsets import AgentToolset

if TYPE_CHECKING:
    from pydantic_ai.mcp import MCPServer
    from pydantic_ai.toolsets.fastmcp import FastMCPToolset


def _empty_headers() -> dict[str, str]:
    return {}


@dataclass(frozen=True)
class MCPPartnerConfig:
    url: str | None = None
    id: str | None = None
    authorization_token: str | None = None
    headers: dict[str, str] = field(default_factory=_empty_headers)
    allowed_tools: list[str] | None = None
    description: str | None = None


@dataclass
class MCPPartnerCapability(AbstractCapability[AgentDepsT]):
    """Shared capability base for partner packages built primarily on top of MCP."""

    config: MCPPartnerConfig = field(default_factory=MCPPartnerConfig)
    extra_instructions: tuple[str, ...] = ()
    local_toolset: MCPServer | FastMCPToolset[AgentDepsT] | None = None

    partner_name: ClassVar[str] = 'Partner'
    readonly_by_default: ClassVar[bool] = True

    @classmethod
    def from_spec(cls, *args: Any, **kwargs: Any) -> MCPPartnerCapability[Any]:
        config = kwargs.get('config')
        if isinstance(config, Mapping):
            kwargs['config'] = cls.config_from_mapping(cast(Mapping[str, object], config))
        extra_instructions = kwargs.get('extra_instructions')
        if isinstance(extra_instructions, list):
            extra_items = cast(list[object], extra_instructions)
            kwargs['extra_instructions'] = tuple(
                item for item in extra_items if isinstance(item, str)
            )
        return cls(*args, **kwargs)

    @classmethod
    def config_from_mapping(cls, config: Mapping[str, object]) -> MCPPartnerConfig:
        return MCPPartnerConfig(
            url=cls._read_optional_str(config, 'url'),
            id=cls._read_optional_str(config, 'id'),
            authorization_token=cls._read_optional_str(config, 'authorization_token'),
            headers=cls._read_headers(config, 'headers'),
            allowed_tools=cls._read_optional_str_list(config, 'allowed_tools'),
            description=cls._read_optional_str(config, 'description'),
        )

    @staticmethod
    def _read_optional_str(config: Mapping[str, object], key: str) -> str | None:
        value = config.get(key)
        return value if isinstance(value, str) else None

    @staticmethod
    def _read_bool(config: Mapping[str, object], key: str, *, default: bool = False) -> bool:
        value = config.get(key)
        return value if isinstance(value, bool) else default

    @staticmethod
    def _read_headers(config: Mapping[str, object], key: str) -> dict[str, str]:
        value = config.get(key)
        if not isinstance(value, Mapping):
            return {}
        value_mapping = cast(Mapping[object, object], value)
        return {
            header_key: header_value
            for header_key, header_value in value_mapping.items()
            if isinstance(header_key, str) and isinstance(header_value, str)
        }

    @staticmethod
    def _read_optional_str_list(config: Mapping[str, object], key: str) -> list[str] | None:
        value = config.get(key)
        if not isinstance(value, Sequence) or isinstance(value, str):
            return None
        value_sequence = cast(Sequence[object], value)
        items = [item for item in value_sequence if isinstance(item, str)]
        return items or None

    def is_readonly_by_default(self) -> bool:
        return self.readonly_by_default

    def get_partner_instructions(self) -> tuple[str, ...]:
        return ()

    def _build_mcp_capability(self) -> MCP[AgentDepsT] | None:
        if self.config.url is None:
            return None
        return MCP(
            self.config.url,
            builtin=False if self.local_toolset is not None else True,
            local=self.local_toolset,
            id=self.config.id,
            authorization_token=self.config.authorization_token,
            headers=self.config.headers or None,
            allowed_tools=self.config.allowed_tools,
            description=self.config.description,
        )

    def get_instructions(self) -> str:
        parts = [
            f'You can use {self.partner_name} MCP tools when they help.',
        ]
        if self.config.url:
            parts.append('Prefer the configured MCP server over ad hoc API calls when possible.')
        if self.is_readonly_by_default():
            parts.append(
                f'Treat {self.partner_name} write operations as opt-in and wait for '
                'explicit user intent.'
            )
        parts.extend(self.get_partner_instructions())
        parts.extend(item for item in self.extra_instructions if item)
        return ' '.join(parts)

    def get_builtin_tools(self) -> Sequence[AgentBuiltinTool[AgentDepsT]]:
        mcp_capability = self._build_mcp_capability()
        return [] if mcp_capability is None else mcp_capability.get_builtin_tools()

    def get_toolset(self) -> AgentToolset[AgentDepsT] | None:
        mcp_capability = self._build_mcp_capability()
        return None if mcp_capability is None else mcp_capability.get_toolset()
