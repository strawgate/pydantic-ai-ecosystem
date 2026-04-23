from __future__ import annotations

import functools
import http.server
import json
import os
import socketserver
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pytest
from mcp.types import Tool
from pydantic_ai import (
    Agent,
    ModelMessage,
    ModelResponse,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    UserPromptPart,
)
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.function import AgentInfo, FunctionModel
from pydantic_ai.models.test import TestModel
from pydantic_ai_playwright import PlaywrightCapability, PlaywrightConfig, create_playwright_agent

EXPECTED_BROWSER_TEST_TOOL_NAMES = {'navigate_page', 'snapshot_page'}
EXPECTED_REAL_PLAYWRIGHT_TOOL_NAMES = {
    'browser_navigate',
    'browser_snapshot',
    'browser_click',
}


class _TestTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


@contextmanager
def _static_site(root: Path) -> Iterator[str]:
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
    httpd = _TestTCPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{httpd.server_address[1]}/'
    finally:
        httpd.shutdown()
        thread.join(timeout=2)


def _playwright_mcp_model(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
    tool_names = {tool.name for tool in info.function_tools}
    assert 'browser_navigate' in tool_names

    last = messages[-1].parts[-1]
    if isinstance(last, UserPromptPart):
        assert isinstance(last.content, str)
        return ModelResponse(
            parts=[ToolCallPart('browser_navigate', json.dumps({'url': last.content}))]
        )
    if isinstance(last, ToolReturnPart) and last.tool_name == 'browser_navigate':
        return ModelResponse(parts=[TextPart(str(last.content))])

    raise AssertionError(f'Unexpected message part: {last!r}')


def _tool_by_name(tools: list[Tool], name: str) -> Tool:
    for tool in tools:
        if tool.name == name:
            return tool
    raise AssertionError(f'Missing expected tool: {name}')


def test_playwright_capability_instructions_reflect_base_url_and_action_policy() -> None:
    capability = PlaywrightCapability(
        config=PlaywrightConfig(
            base_url='https://example.com',
            browser_name='chromium',
            allow_form_actions=False,
        )
    )
    instructions = capability.get_instructions()
    assert 'https://example.com' in instructions
    assert 'chromium' in instructions
    assert 'Playwright write operations as opt-in' in instructions


def test_playwright_capability_is_spec_friendly() -> None:
    agent = Agent.from_spec(
        {
            'model': 'test',
            'capabilities': [
                {
                    'PlaywrightCapability': {
                        'config': {
                            'base_url': 'https://example.com',
                            'browser_name': 'firefox',
                            'allow_form_actions': True,
                        }
                    }
                }
            ],
        },
        custom_capability_types=[PlaywrightCapability],
    )
    assert agent.model is not None


def test_create_playwright_agent_is_import_safe() -> None:
    agent = create_playwright_agent(model='test')
    assert agent.model is not None


@pytest.mark.asyncio
async def test_playwright_capability_lists_tools_from_local_browser_server(
    browser_test_server: MCPServerStdio,
) -> None:
    capability = PlaywrightCapability(
        config=PlaywrightConfig(url='http://example.test/mcp'),
        local_toolset=browser_test_server,
    )

    toolset = capability.get_toolset()
    assert isinstance(toolset, MCPServerStdio)

    async with toolset:
        tools = await toolset.list_tools()

    assert {tool.name for tool in tools} == EXPECTED_BROWSER_TEST_TOOL_NAMES
    navigate_tool = _tool_by_name(tools, 'navigate_page')
    assert navigate_tool.description is not None
    assert 'Navigate' in navigate_tool.description
    assert navigate_tool.inputSchema['required'] == ['url']


@pytest.mark.asyncio
async def test_playwright_capability_supports_agent_tool_use(
    browser_test_server: MCPServerStdio,
) -> None:
    capability = PlaywrightCapability(
        config=PlaywrightConfig(url='http://example.test/mcp'),
        local_toolset=browser_test_server,
    )
    agent = Agent(TestModel(call_tools=['navigate_page']), capabilities=[capability])
    result = await agent.run('Open the example page and tell me its title.')
    messages = result.all_messages()
    output = result.output

    assert isinstance(output, str)
    assert 'Example Page' in output
    assert 'navigate_page' in output
    assert len(messages) == 4
    assert messages[1].parts[0].part_kind == 'tool-call'
    assert messages[2].parts[0].part_kind == 'tool-return'
    assert messages[1].parts[0].tool_name == 'navigate_page'
    assert messages[2].parts[0].tool_name == 'navigate_page'


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skipif(
    os.getenv('PYDANTIC_AI_RUN_PLAYWRIGHT_MCP_TESTS') != '1',
    reason='Set PYDANTIC_AI_RUN_PLAYWRIGHT_MCP_TESTS=1 to run Playwright MCP integration tests.',
)
async def test_playwright_capability_roundtrip_against_real_mcp_server(tmp_path: Path) -> None:
    index_html = tmp_path / 'index.html'
    index_html.write_text(
        '<html><head><title>Playwright Test Page</title></head>'
        '<body><h1>Hello Browser</h1><p>Smoke test page.</p></body></html>'
    )

    with _static_site(tmp_path) as site_url:
        server = MCPServerStdio(
            'npx',
            ['-y', '@playwright/mcp@latest', '--browser=firefox', '--headless'],
        )
        capability = PlaywrightCapability(
            config=PlaywrightConfig(url='http://example.test/mcp'),
            local_toolset=server,
        )

        toolset = capability.get_toolset()
        assert isinstance(toolset, MCPServerStdio)

        async with toolset:
            tools = await toolset.list_tools()

        assert EXPECTED_REAL_PLAYWRIGHT_TOOL_NAMES.issubset({tool.name for tool in tools})
        navigate_tool = _tool_by_name(tools, 'browser_navigate')
        assert navigate_tool.description is not None
        assert navigate_tool.inputSchema['required'] == ['url']

        agent = Agent(
            FunctionModel(_playwright_mcp_model),
            capabilities=[capability],
        )
        result = await agent.run(site_url)
        messages = result.all_messages()

        assert 'Playwright Test Page' in result.output
        assert site_url in result.output
        assert len(messages) == 4
        assert messages[1].parts[0].part_kind == 'tool-call'
        assert messages[2].parts[0].part_kind == 'tool-return'
        assert messages[1].parts[0].tool_name == 'browser_navigate'
        assert messages[2].parts[0].tool_name == 'browser_navigate'
