from __future__ import annotations

import os
import shutil
from collections.abc import Sequence

import pytest
from mcp.types import Tool
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai_localstack import LocalStackCapability, create_localstack_agent

EXPECTED_LOCALSTACK_TOOL_NAMES = {
    'localstack-aws-client',
    'localstack-chaos-injector',
    'localstack-cloud-pods',
    'localstack-deployer',
    'localstack-docs',
    'localstack-ephemeral-instances',
    'localstack-extensions',
    'localstack-iam-policy-analyzer',
    'localstack-logs-analysis',
    'localstack-management',
    'localstack-snowflake-client',
}


def _tool_by_name(tools: Sequence[Tool], name: str) -> Tool:
    for tool in tools:
        if tool.name == name:
            return tool
    raise AssertionError(f'Missing expected tool: {name}')


def test_localstack_capability_builds_stdio_server() -> None:
    capability = LocalStackCapability(
        region='eu-west-1',
        env={'DEBUG': '0', 'EXTRA_FLAG': 'yes'},
        debug=True,
        server_id='localstack-test',
    )

    instructions = capability.get_instructions()
    assert 'eu-west-1' in instructions
    assert 'LocalStack' in instructions
    assert 'Ask for confirmation before destructive actions' in instructions

    toolset = capability.get_toolset()
    assert isinstance(toolset, MCPServerStdio)
    assert toolset.command == 'npx'
    assert list(toolset.args) == ['-y', '@localstack/localstack-mcp-server']
    assert toolset.id == 'localstack-test'
    assert toolset.include_instructions is True
    assert toolset.env is not None
    assert toolset.env['AWS_DEFAULT_REGION'] == 'eu-west-1'
    assert toolset.env['DEBUG'] == '0'
    assert toolset.env['EXTRA_FLAG'] == 'yes'
    assert toolset.env['PERSISTENCE'] == '1'


def test_localstack_capability_is_spec_friendly() -> None:
    agent = Agent.from_spec(
        {
            'model': 'test',
            'capabilities': [
                {
                    'LocalStackCapability': {
                        'region': 'us-west-2',
                        'env': {'PERSISTENCE': '0'},
                        'destructive_operations_require_confirmation': False,
                    }
                }
            ],
        },
        custom_capability_types=[LocalStackCapability],
    )

    assert agent.model is not None


def test_create_localstack_agent_is_import_safe() -> None:
    agent = create_localstack_agent(model='test')
    assert agent.model is not None


@pytest.mark.asyncio
@pytest.mark.integration
async def test_localstack_mcp_server_lists_tools() -> None:
    if os.getenv('PYDANTIC_AI_RUN_LOCALSTACK_MCP_TESTS') != '1':
        pytest.skip('Set PYDANTIC_AI_RUN_LOCALSTACK_MCP_TESTS=1 to run LocalStack MCP smoke tests.')
    if shutil.which('npx') is None:
        pytest.skip('npx is required to launch the LocalStack MCP server.')

    capability = LocalStackCapability(
        env={
            'AWS_ACCESS_KEY_ID': 'test',
            'AWS_SECRET_ACCESS_KEY': 'test',
        },
        timeout=30,
        read_timeout=30,
    )
    server = capability.get_toolset()
    assert isinstance(server, MCPServerStdio)

    async with server:
        tools = await server.list_tools()

    tool_names = {tool.name for tool in tools}
    assert len(tools) == len(EXPECTED_LOCALSTACK_TOOL_NAMES)
    assert tool_names == EXPECTED_LOCALSTACK_TOOL_NAMES

    aws_client = _tool_by_name(tools, 'localstack-aws-client')
    aws_client_description = aws_client.description
    aws_client_schema = aws_client.inputSchema
    assert aws_client_description is not None
    assert 'awslocal' in aws_client_description
    assert aws_client_schema['required'] == ['command']
    assert aws_client_schema['properties']['command']['type'] == 'string'

    docs_tool = _tool_by_name(tools, 'localstack-docs')
    docs_tool_description = docs_tool.description
    docs_tool_schema = docs_tool.inputSchema
    assert docs_tool_description is not None
    assert 'LocalStack documentation' in docs_tool_description
    assert docs_tool_schema['required'] == ['query']
    assert docs_tool_schema['properties']['limit']['default'] == 5

    management_tool = _tool_by_name(tools, 'localstack-management')
    management_tool_description = management_tool.description
    management_tool_schema = management_tool.inputSchema
    assert management_tool_description is not None
    assert 'LocalStack lifecycle' in management_tool_description
    assert management_tool_schema['required'] == ['action']
    assert management_tool_schema['properties']['action']['enum'] == [
        'start',
        'stop',
        'restart',
        'status',
    ]
    assert management_tool_schema['properties']['service']['default'] == 'aws'
