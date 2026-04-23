from __future__ import annotations

from pydantic_ai import Agent
from pydantic_ai_logfire import LogfireCapability, LogfireConfig, create_logfire_agent


def test_logfire_capability_instructions_reflect_config() -> None:
    capability = LogfireCapability(
        config=LogfireConfig(project_name='ecosystem-tests', environment='ci', trace_content=True)
    )
    instructions = capability.get_instructions()
    assert 'ecosystem-tests' in instructions
    assert 'ci' in instructions
    assert 'Sensitive content may appear in traces' in instructions


def test_logfire_capability_is_spec_friendly() -> None:
    agent = Agent.from_spec(
        {
            'model': 'test',
            'capabilities': [
                {
                    'LogfireCapability': {
                        'config': {
                            'project_name': 'ecosystem-tests',
                            'environment': 'ci',
                            'trace_content': False,
                        }
                    }
                }
            ],
        },
        custom_capability_types=[LogfireCapability],
    )
    assert agent.model is not None


def test_create_logfire_agent_is_import_safe() -> None:
    agent = create_logfire_agent(model='test')
    assert agent.model is not None
