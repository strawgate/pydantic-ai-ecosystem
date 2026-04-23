from __future__ import annotations

from pydantic_ai import Agent
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
