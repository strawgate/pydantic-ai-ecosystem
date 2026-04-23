from __future__ import annotations

import os
from dataclasses import dataclass, field

from pydantic_ai import Agent
from pydantic_ai.capabilities import AbstractCapability
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.tools import AgentDepsT
from pydantic_ai.toolsets import AgentToolset

DEFAULT_LOCALSTACK_MCP_ARGS = ['-y', '@localstack/localstack-mcp-server']


def create_localstack_mcp_server(
    *,
    region: str = 'us-east-1',
    auth_token: str | None = None,
    persistence: bool = True,
    debug: bool = False,
    env: dict[str, str] | None = None,
    inherit_parent_env: bool = True,
    command: str = 'npx',
    args: list[str] | None = None,
    cwd: str | None = None,
    tool_prefix: str | None = None,
    timeout: float = 20,
    read_timeout: float = 5 * 60,
    include_server_instructions: bool = True,
    server_id: str | None = 'localstack',
) -> MCPServerStdio:
    merged_env = dict(os.environ) if inherit_parent_env else {}
    merged_env.update(env or {})
    merged_env.setdefault('AWS_DEFAULT_REGION', region)
    if persistence:
        merged_env.setdefault('PERSISTENCE', '1')
    if debug:
        merged_env.setdefault('DEBUG', '1')
    if auth_token:
        merged_env['LOCALSTACK_AUTH_TOKEN'] = auth_token

    return MCPServerStdio(
        command,
        args=list(args or DEFAULT_LOCALSTACK_MCP_ARGS),
        env=merged_env,
        cwd=cwd,
        tool_prefix=tool_prefix,
        timeout=timeout,
        read_timeout=read_timeout,
        include_instructions=include_server_instructions,
        id=server_id,
    )


@dataclass(init=False)
class LocalStackCapability(AbstractCapability[AgentDepsT]):
    """Attach LocalStack MCP tools with LocalStack-specific guidance."""

    region: str
    auth_token: str | None
    persistence: bool
    debug: bool
    env: dict[str, str]
    inherit_parent_env: bool
    command: str
    args: list[str]
    cwd: str | None
    tool_prefix: str | None
    timeout: float
    read_timeout: float
    include_server_instructions: bool
    destructive_operations_require_confirmation: bool
    server_id: str | None
    _server: MCPServerStdio = field(init=False, repr=False)

    def __init__(
        self,
        *,
        region: str = 'us-east-1',
        auth_token: str | None = None,
        persistence: bool = True,
        debug: bool = False,
        env: dict[str, str] | None = None,
        inherit_parent_env: bool = True,
        command: str = 'npx',
        args: list[str] | None = None,
        cwd: str | None = None,
        tool_prefix: str | None = None,
        timeout: float = 20,
        read_timeout: float = 5 * 60,
        include_server_instructions: bool = True,
        destructive_operations_require_confirmation: bool = True,
        server_id: str | None = 'localstack',
    ) -> None:
        self.region = region
        self.auth_token = auth_token
        self.persistence = persistence
        self.debug = debug
        self.env = dict(env or {})
        self.inherit_parent_env = inherit_parent_env
        self.command = command
        self.args = list(args or DEFAULT_LOCALSTACK_MCP_ARGS)
        self.cwd = cwd
        self.tool_prefix = tool_prefix
        self.timeout = timeout
        self.read_timeout = read_timeout
        self.include_server_instructions = include_server_instructions
        self.destructive_operations_require_confirmation = (
            destructive_operations_require_confirmation
        )
        self.server_id = server_id
        self._server = create_localstack_mcp_server(
            region=self.region,
            auth_token=self.auth_token,
            persistence=self.persistence,
            debug=self.debug,
            env=self.env,
            inherit_parent_env=self.inherit_parent_env,
            command=self.command,
            args=self.args,
            cwd=self.cwd,
            tool_prefix=self.tool_prefix,
            timeout=self.timeout,
            read_timeout=self.read_timeout,
            include_server_instructions=self.include_server_instructions,
            server_id=self.server_id,
        )

    def get_instructions(self) -> str:
        parts = [
            'You can use LocalStack MCP tools to manage a local AWS-like environment.',
            'Treat LocalStack as a local emulator, not a production AWS account.',
            f'Use `{self.region}` as the default AWS region unless the user asks for another one.',
            (
                'Before deploying or mutating infrastructure, check whether the LocalStack '
                'container is running and start it if needed.'
            ),
            (
                'After deployments, verify created resources and inspect LocalStack logs '
                'for infrastructure-related errors.'
            ),
        ]
        if self.destructive_operations_require_confirmation:
            parts.append(
                'Ask for confirmation before destructive actions such as resets, teardown, '
                'Cloud Pod restores, or chaos faults.'
            )
        return ' '.join(parts)

    def get_toolset(self) -> AgentToolset[AgentDepsT] | None:
        return self._server


def create_localstack_agent(
    model: str = 'openai:gpt-5.2',
    *,
    instructions: str = 'Help the user develop and validate AWS infrastructure locally.',
    capability: LocalStackCapability | None = None,
) -> Agent[None, str]:
    return Agent(
        model,
        instructions=instructions,
        capabilities=[capability or LocalStackCapability()],
    )
