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


def test_ci_matrix_discovers_existing_package_tests() -> None:
    module = _load_script('ci_matrix')

    matrix = module.discover_package_matrix()
    package_names = {item['package'] for item in matrix}

    assert 'pydantic_ai_github' in package_names
    assert 'pydantic_ai_localstack' in package_names
    assert 'pydantic_ai_partner_mcp' in package_names
