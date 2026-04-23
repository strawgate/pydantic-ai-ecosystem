from __future__ import annotations

import pytest
from mcp.types import Tool
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.test import TestModel
from pydantic_ai_notion import NotionCapability, NotionConfig, create_notion_agent

EXPECTED_PARTNER_TEST_TOOL_NAMES = {'search_workspace', 'read_document'}


def _tool_by_name(tools: list[Tool], name: str) -> Tool:
    for tool in tools:
        if tool.name == name:
            return tool
    raise AssertionError(f'Missing expected tool: {name}')


def test_notion_capability_instructions_reflect_workspace_and_write_policy() -> None:
    capability = NotionCapability(
        config=NotionConfig(workspace_name='Team Workspace', allow_writes=False)
    )
    instructions = capability.get_instructions()
    assert 'Team Workspace' in instructions
    assert 'Notion write operations as opt-in' in instructions


def test_notion_capability_is_spec_friendly() -> None:
    agent = Agent.from_spec(
        {
            'model': 'test',
            'capabilities': [
                {
                    'NotionCapability': {
                        'config': {
                            'workspace_name': 'Team Workspace',
                            'allow_writes': True,
                        }
                    }
                }
            ],
        },
        custom_capability_types=[NotionCapability],
    )
    assert agent.model is not None


def test_create_notion_agent_is_import_safe() -> None:
    agent = create_notion_agent(model='test')
    assert agent.model is not None


@pytest.mark.asyncio
async def test_notion_capability_lists_tools_from_local_mcp_server(
    partner_test_server: MCPServerStdio,
) -> None:
    capability = NotionCapability(
        config=NotionConfig(url='http://example.test/mcp'),
        local_toolset=partner_test_server,
    )

    toolset = capability.get_toolset()
    assert isinstance(toolset, MCPServerStdio)

    async with toolset:
        tools = await toolset.list_tools()

    assert {tool.name for tool in tools} == EXPECTED_PARTNER_TEST_TOOL_NAMES
    read_tool = _tool_by_name(tools, 'read_document')
    assert read_tool.description is not None
    assert 'document' in read_tool.description
    assert read_tool.inputSchema['required'] == ['document_id']


@pytest.mark.asyncio
async def test_notion_capability_supports_agent_tool_use(
    partner_test_server: MCPServerStdio,
) -> None:
    capability = NotionCapability(
        config=NotionConfig(url='http://example.test/mcp'),
        local_toolset=partner_test_server,
    )
    agent = Agent(TestModel(call_tools=['search_workspace']), capabilities=[capability])
    result = await agent.run('Search the workspace for onboarding notes.')
    messages = result.all_messages()
    output = result.output
    assert isinstance(output, str)
    assert 'Alpha Doc' in output
    assert 'search_workspace' in output
    assert len(messages) == 4
    assert messages[1].parts[0].part_kind == 'tool-call'
    assert messages[2].parts[0].part_kind == 'tool-return'
    assert messages[1].parts[0].tool_name == 'search_workspace'
    assert messages[2].parts[0].tool_name == 'search_workspace'
