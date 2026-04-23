from __future__ import annotations

from pydantic_ai import Agent
from pydantic_ai_github import GitHubCapability, GitHubConfig, create_github_agent


def test_github_capability_instructions_reflect_repo_and_write_policy() -> None:
    capability = GitHubCapability(
        config=GitHubConfig(owner='pydantic', repo='pydantic-ai', allow_writes=False)
    )
    instructions = capability.get_instructions()
    assert 'pydantic/pydantic-ai' in instructions
    assert 'GitHub write operations as opt-in' in instructions


def test_github_capability_is_spec_friendly() -> None:
    agent = Agent.from_spec(
        {
            'model': 'test',
            'capabilities': [
                {
                    'GitHubCapability': {
                        'config': {
                            'owner': 'pydantic',
                            'repo': 'pydantic-ai',
                            'allow_writes': True,
                        }
                    }
                }
            ],
        },
        custom_capability_types=[GitHubCapability],
    )
    assert agent.model is not None


def test_create_github_agent_is_import_safe() -> None:
    agent = create_github_agent(model='test')
    assert agent.model is not None
