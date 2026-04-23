from __future__ import annotations

from typing import cast

import pytest
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.test import TestModel
from pydantic_ai.toolsets import AbstractToolset
from pydantic_ai_partner_mcp import MCPPartnerCapability, MCPPartnerConfig


def test_partner_mcp_capability_builds_instructions_and_tools() -> None:
    capability = MCPPartnerCapability(
        config=MCPPartnerConfig(
            url='https://example.com/mcp',
            id='example-mcp',
            authorization_token='Bearer test-token',
            allowed_tools=['search_docs'],
            description='Example MCP partner',
        ),
        extra_instructions=('Prefer documented tools first.',),
    )

    instructions = capability.get_instructions()
    assert 'Partner MCP tools' in instructions
    assert 'configured MCP server' in instructions
    assert 'Prefer documented tools first.' in instructions

    assert capability.get_toolset() is not None
    assert len(capability.get_builtin_tools()) == 1


def test_partner_mcp_capability_is_spec_friendly() -> None:
    agent = Agent.from_spec(
        {
            'model': 'test',
            'capabilities': [
                {
                    'MCPPartnerCapability': {
                        'config': {
                            'url': 'https://example.com/mcp',
                            'allowed_tools': ['search_docs'],
                        },
                        'extra_instructions': ['Prefer documented tools first.'],
                    }
                }
            ],
        },
        custom_capability_types=[MCPPartnerCapability],
    )

    assert agent.model is not None


@pytest.mark.asyncio
async def test_partner_mcp_capability_filters_allowed_tools(
    partner_test_server: MCPServerStdio,
) -> None:
    capability = MCPPartnerCapability(
        config=MCPPartnerConfig(
            url='http://example.test/mcp',
            allowed_tools=['read_document'],
        ),
        local_toolset=partner_test_server,
    )

    toolset = capability.get_toolset()
    assert toolset is not None
    abstract_toolset = cast(AbstractToolset[None], toolset)

    async with abstract_toolset:
        tools = await abstract_toolset.get_tools(None)  # pyright: ignore[reportArgumentType]

    assert set(tools.keys()) == {'read_document'}


@pytest.mark.asyncio
async def test_partner_mcp_capability_agent_trace_includes_tool_roundtrip(
    partner_test_server: MCPServerStdio,
) -> None:
    capability = MCPPartnerCapability(
        config=MCPPartnerConfig(url='http://example.test/mcp'),
        local_toolset=partner_test_server,
    )
    agent = Agent(TestModel(call_tools=['search_workspace']), capabilities=[capability])

    result = await agent.run('Search the workspace for onboarding notes.')
    messages = result.all_messages()

    assert isinstance(result.output, str)
    assert 'Alpha Doc' in result.output
    assert len(messages) == 4
    assert messages[1].parts[0].part_kind == 'tool-call'
    assert messages[2].parts[0].part_kind == 'tool-return'
    assert messages[1].parts[0].tool_name == 'search_workspace'
    assert messages[2].parts[0].tool_name == 'search_workspace'
