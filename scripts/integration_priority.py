from __future__ import annotations

import argparse
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

CiMode = Literal[
    'local_fixture',
    'public_read_only',
    'service_token',
    'oauth_sandbox',
    'manual_only',
]
AuthMode = Literal['none', 'local', 'service_token', 'oauth_user']
Implementation = Literal['mcp_baseline', 'opinionated_capability', 'full_backend']
IntegrationKind = Literal['partner', 'generic_mcp', 'platform']
ToolTestLevel = Literal[
    'spec_only',
    'transport_smoke',
    'inventory',
    'read_roundtrip',
    'write_roundtrip',
]

_CI_MODE_SCORES: dict[CiMode, int] = {
    'local_fixture': 40,
    'public_read_only': 32,
    'service_token': 24,
    'oauth_sandbox': 8,
    'manual_only': 0,
}
_AUTH_MODE_SCORES: dict[AuthMode, int] = {
    'none': 20,
    'local': 20,
    'service_token': 12,
    'oauth_user': -10,
}
_TOOL_TEST_LEVEL_SCORES: dict[ToolTestLevel, int] = {
    'spec_only': 0,
    'transport_smoke': 8,
    'inventory': 14,
    'read_roundtrip': 24,
    'write_roundtrip': 30,
}
_IMPLEMENTATION_SCORES: dict[Implementation, int] = {
    'mcp_baseline': 4,
    'opinionated_capability': 8,
    'full_backend': 6,
}
_KIND_SCORES: dict[IntegrationKind, int] = {
    'partner': 8,
    'generic_mcp': -18,
    'platform': 4,
}


@dataclass(frozen=True)
class IntegrationCandidate:
    name: str
    package_name: str
    kind: IntegrationKind
    implementation: Implementation
    transport: str
    auth_mode: AuthMode
    ci_mode: CiMode
    tool_test_level: ToolTestLevel
    official_server: bool
    strategic_fit: int
    scaffold_present: bool
    notes: tuple[str, ...]

    @property
    def priority_score(self) -> int:
        return (
            _CI_MODE_SCORES[self.ci_mode]
            + _AUTH_MODE_SCORES[self.auth_mode]
            + _TOOL_TEST_LEVEL_SCORES[self.tool_test_level]
            + _IMPLEMENTATION_SCORES[self.implementation]
            + _KIND_SCORES[self.kind]
            + (self.strategic_fit * 4)
            + (8 if self.official_server else 0)
            + (6 if self.scaffold_present else 0)
        )

    @property
    def wave(self) -> str:
        if self.priority_score >= 95:
            return 'wave_1'
        if self.priority_score >= 70:
            return 'wave_2'
        return 'incubating'


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _catalog_path() -> Path:
    return _repo_root() / 'catalog' / 'integrations.toml'


def load_candidates(catalog_path: Path | None = None) -> list[IntegrationCandidate]:
    path = catalog_path or _catalog_path()
    with path.open('rb') as file:
        raw_data = tomllib.load(file)

    candidates: list[IntegrationCandidate] = []
    for item in raw_data['integrations']:
        candidates.append(
            IntegrationCandidate(
                name=item['name'],
                package_name=item['package_name'],
                kind=item['kind'],
                implementation=item['implementation'],
                transport=item['transport'],
                auth_mode=item['auth_mode'],
                ci_mode=item['ci_mode'],
                tool_test_level=item['tool_test_level'],
                official_server=item['official_server'],
                strategic_fit=item['strategic_fit'],
                scaffold_present=item['scaffold_present'],
                notes=tuple(item.get('notes', [])),
            )
        )
    return candidates


def rank_candidates(candidates: list[IntegrationCandidate]) -> list[IntegrationCandidate]:
    return sorted(
        candidates,
        key=lambda candidate: (-candidate.priority_score, candidate.name),
    )


def render_report(candidates: list[IntegrationCandidate], *, limit: int = 10) -> str:
    lines = [
        '| Rank | Integration | Score | Wave | CI Mode | Tool Test | Package |',
        '| --- | --- | ---: | --- | --- | --- | --- |',
    ]
    for index, candidate in enumerate(rank_candidates(candidates)[:limit], start=1):
        lines.append(
            '| '
            f'{index} | {candidate.name} | {candidate.priority_score} | {candidate.wave} | '
            f'{candidate.ci_mode} | {candidate.tool_test_level} | {candidate.package_name} |'
        )
    return '\n'.join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Rank ecosystem integration candidates by automated-testability-first priority.'
    )
    parser.add_argument('--top', type=int, default=10, help='Number of candidates to show.')
    args = parser.parse_args()

    print(render_report(load_candidates(), limit=args.top))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
