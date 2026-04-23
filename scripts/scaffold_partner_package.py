from __future__ import annotations

import argparse
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _camel_case(value: str) -> str:
    return ''.join(part.capitalize() for part in value.replace('-', '_').split('_'))


def _render_template(template_text: str, replacements: dict[str, str]) -> str:
    result = template_text
    for key, value in replacements.items():
        result = result.replace(f'{{{{ {key} }}}}', value)
    return result


def scaffold_partner_package(
    *,
    slug: str,
    display_name: str,
    partner_instruction: str,
    agent_instructions: str,
) -> list[Path]:
    repo_root = _repo_root()
    templates_dir = repo_root / 'templates' / 'partner_mcp'

    import_name = f'pydantic_ai_{slug}'
    distribution_name = import_name.replace('_', '-')
    capability_class_name = f'{_camel_case(slug)}Capability'
    config_class_name = f'{_camel_case(slug)}Config'
    factory_function_name = f'create_{slug}_agent'

    replacements = {
        'slug': slug,
        'display_name': display_name,
        'import_name': import_name,
        'distribution_name': distribution_name,
        'capability_class_name': capability_class_name,
        'config_class_name': config_class_name,
        'factory_function_name': factory_function_name,
        'partner_instruction': partner_instruction,
        'agent_instructions': agent_instructions,
    }

    targets = {
        templates_dir / 'README.md.tmpl': (
            repo_root / 'packages' / import_name / 'README.md'
        ),
        templates_dir / 'pyproject.toml.tmpl': (
            repo_root / 'packages' / import_name / 'pyproject.toml'
        ),
        templates_dir / 'package___init__.py.tmpl': (
            repo_root / 'packages' / import_name / import_name / '__init__.py'
        ),
        templates_dir / 'package__capability.py.tmpl': (
            repo_root / 'packages' / import_name / import_name / '_capability.py'
        ),
        templates_dir / 'test_capability.py.tmpl': (
            repo_root / 'tests' / import_name / f'test_{slug}_capability.py'
        ),
    }

    written_files: list[Path] = []
    for template_path, target_path in targets.items():
        target_path.parent.mkdir(parents=True, exist_ok=True)
        rendered = _render_template(template_path.read_text(), replacements)
        target_path.write_text(rendered)
        written_files.append(target_path)

    py_typed_path = repo_root / 'packages' / import_name / import_name / 'py.typed'
    py_typed_path.write_text('')
    written_files.append(py_typed_path)
    return written_files


def main() -> int:
    parser = argparse.ArgumentParser(description='Scaffold a new MCP-first partner package.')
    parser.add_argument('--slug', required=True, help='Short slug such as notion or vercel.')
    parser.add_argument('--display-name', required=True, help='User-facing partner name.')
    parser.add_argument(
        '--partner-instruction',
        required=True,
        help='Primary partner-specific instruction sentence.',
    )
    parser.add_argument(
        '--agent-instructions',
        required=True,
        help='Default instructions for the generated convenience factory.',
    )
    args = parser.parse_args()

    for path in scaffold_partner_package(
        slug=args.slug,
        display_name=args.display_name,
        partner_instruction=args.partner_instruction,
        agent_instructions=args.agent_instructions,
    ):
        print(path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
