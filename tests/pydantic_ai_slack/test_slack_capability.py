from __future__ import annotations

from pydantic_ai import Agent
from pydantic_ai_slack import SlackCapability, SlackConfig, create_slack_agent


def test_slack_capability_instructions_reflect_channel_and_post_policy() -> None:
    capability = SlackCapability(
        config=SlackConfig(
            workspace_name='pydantic',
            default_channel='eng-agents',
            allow_posting=False,
        )
    )
    instructions = capability.get_instructions()
    assert 'pydantic' in instructions
    assert 'eng-agents' in instructions
    assert 'Slack write operations as opt-in' in instructions


def test_slack_capability_is_spec_friendly() -> None:
    agent = Agent.from_spec(
        {
            'model': 'test',
            'capabilities': [
                {
                    'SlackCapability': {
                        'config': {
                            'workspace_name': 'pydantic',
                            'default_channel': 'eng-agents',
                            'allow_posting': True,
                        }
                    }
                }
            ],
        },
        custom_capability_types=[SlackCapability],
    )
    assert agent.model is not None


def test_create_slack_agent_is_import_safe() -> None:
    agent = create_slack_agent(model='test')
    assert agent.model is not None
