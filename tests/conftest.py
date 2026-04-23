from __future__ import annotations

import sys

import pytest
from pydantic_ai.mcp import MCPServerStdio


@pytest.fixture
def partner_test_server() -> MCPServerStdio:
    return MCPServerStdio(
        sys.executable,
        ['-m', 'tests.mcp_partner_server'],
        include_instructions=True,
    )


@pytest.fixture
def browser_test_server() -> MCPServerStdio:
    return MCPServerStdio(
        sys.executable,
        ['-m', 'tests.mcp_browser_server'],
        include_instructions=True,
    )
