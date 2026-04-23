from __future__ import annotations

import json
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def discover_package_matrix() -> list[dict[str, str]]:
    repo_root = _repo_root()
    packages_dir = repo_root / 'packages'
    tests_dir = repo_root / 'tests'

    matrix: list[dict[str, str]] = []
    for package_dir in sorted(path for path in packages_dir.iterdir() if path.is_dir()):
        test_dir = tests_dir / package_dir.name
        if not test_dir.exists():
            continue
        matrix.append(
            {
                'package': package_dir.name,
                'test_dir': str(test_dir.relative_to(repo_root)),
            }
        )
    return matrix


def main() -> int:
    print(json.dumps({'include': discover_package_matrix()}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
