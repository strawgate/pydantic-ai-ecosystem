from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def _load_script(module_name: str) -> ModuleType:
    module_path = Path(__file__).resolve().parent.parent / 'scripts' / f'{module_name}.py'
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_scaffold_partner_package_renders_expected_files(tmp_path: Path) -> None:
    module = _load_script('scaffold_partner_package')

    templates_dir = tmp_path / 'templates' / 'partner_mcp'
    templates_dir.mkdir(parents=True)
    (templates_dir / 'README.md.tmpl').write_text('README {{ display_name }}')
    (templates_dir / 'pyproject.toml.tmpl').write_text('name = "{{ distribution_name }}"')
    (templates_dir / 'package___init__.py.tmpl').write_text('{{ capability_class_name }}')
    (templates_dir / 'package__capability.py.tmpl').write_text('{{ partner_instruction }}')
    (templates_dir / 'test_capability.py.tmpl').write_text('{{ factory_function_name }}')

    original_repo_root = getattr(module, '_repo_root')
    setattr(module, '_repo_root', lambda: tmp_path)
    try:
        written_files = module.scaffold_partner_package(
            slug='notion',
            display_name='Notion',
            partner_instruction='Prefer existing pages.',
            agent_instructions='Help with Notion content.',
        )
    finally:
        setattr(module, '_repo_root', original_repo_root)

    assert len(written_files) == 6
    assert (
        tmp_path / 'packages' / 'pydantic_ai_notion' / 'README.md'
    ).read_text() == 'README Notion'
    assert (
        tmp_path / 'packages' / 'pydantic_ai_notion' / 'pyproject.toml'
    ).read_text() == 'name = "pydantic-ai-notion"'
    assert (
        tmp_path / 'packages' / 'pydantic_ai_notion' / 'pydantic_ai_notion' / '_capability.py'
    ).read_text() == 'Prefer existing pages.'
