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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail when a generated copy is stale or missing.")
    args = parser.parse_args()

    expected = expected_files()
    stale = [path for path, content in expected.items() if not path.is_file() or path.read_bytes() != content]
    if args.check:
        if stale:
            for path in stale:
                print(f"stale: {path.relative_to(ROOT)}", file=sys.stderr)
            return 1
        print("Bundled Skill resources are synchronized.")
        return 0

    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        print(f"updated: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
