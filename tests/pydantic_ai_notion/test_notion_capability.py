from __future__ import annotations

from pydantic_ai import Agent
from pydantic_ai_notion import NotionCapability, NotionConfig, create_notion_agent


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
