from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def _load_priority_module() -> ModuleType:
    module_path = (
        Path(__file__).resolve().parent.parent / 'scripts' / 'integration_priority.py'
    )
    spec = importlib.util.spec_from_file_location('integration_priority', module_path)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_candidate_catalog_has_enough_entries() -> None:
    module = _load_priority_module()
    candidates = module.load_candidates()

    assert len(candidates) >= 20


def test_priority_ranking_favors_automatable_candidates() -> None:
    module = _load_priority_module()
    ranked = module.rank_candidates(module.load_candidates())
    top_names = [candidate.name for candidate in ranked[:6]]

    assert top_names[:2] == ['localstack', 'playwright']
    assert {'github', 'logfire', 'notion'}.issubset(top_names)
    assert 'filesystem' not in top_names
    assert 'context7' not in top_names


def test_wave_one_candidates_do_not_require_manual_auth() -> None:
    module = _load_priority_module()
    ranked = module.rank_candidates(module.load_candidates())
    wave_one = [candidate for candidate in ranked if candidate.wave == 'wave_1']

    assert wave_one
    assert all(candidate.ci_mode != 'manual_only' for candidate in wave_one)
    assert all(candidate.auth_mode != 'oauth_user' for candidate in wave_one)
    assert all(
        candidate.tool_test_level in {'read_roundtrip', 'write_roundtrip'} for candidate in wave_one
    )


def test_rendered_report_contains_expected_columns() -> None:
    module = _load_priority_module()
    report = module.render_report(module.load_candidates(), limit=5)

    assert '| Rank | Integration | Score | Wave | CI Mode | Tool Test | Package |' in report
    assert '| 1 | localstack |' in report
