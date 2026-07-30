#!/usr/bin/env python3
"""Synchronize resources that standalone Skills must bundle locally."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
CONTRACT_SOURCE = ROOT / "shared" / "coordination-contract.md"
CONTRACT_DESTINATIONS = (
    ROOT / "skills" / "orchestrate-project-sessions" / "references" / "coordination-contract.md",
    ROOT / "skills" / "team-mode" / "references" / "coordination-contract.md",
)
PROFILE_SOURCE = ROOT / "agents"
PROFILE_DESTINATION = ROOT / "skills" / "team-mode" / "assets" / "agent-profiles"


def expected_files() -> dict[Path, bytes]:
    result = {path: CONTRACT_SOURCE.read_bytes() for path in CONTRACT_DESTINATIONS}
    for source in sorted(PROFILE_SOURCE.glob("*.toml")):
        result[PROFILE_DESTINATION / source.name] = source.read_bytes()
    return result


def unexpected_files(directory: Path, expected_names: set[str]) -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted(path for path in directory.iterdir() if path.is_file() and path.name not in expected_names)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail when a generated copy is stale or missing.")
    args = parser.parse_args()

    expected = expected_files()
    stale = [path for path, content in expected.items() if not path.is_file() or path.read_bytes() != content]
    expected_profile_names = {path.name for path in expected if path.parent == PROFILE_DESTINATION}
    unexpected = unexpected_files(PROFILE_DESTINATION, expected_profile_names)
    if args.check:
        if stale or unexpected:
            for path in stale:
                print(f"stale: {path.relative_to(ROOT)}", file=sys.stderr)
            for path in unexpected:
                print(f"unexpected: {path.relative_to(ROOT)}", file=sys.stderr)
            return 1
        print("Bundled Skill resources are synchronized.")
        return 0

    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        print(f"updated: {path.relative_to(ROOT)}")
    if unexpected:
        for path in unexpected:
            print(f"unexpected: {path.relative_to(ROOT)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
