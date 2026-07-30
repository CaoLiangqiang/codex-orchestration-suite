#!/usr/bin/env python3
"""Validate the suite's standalone Skill structure without external packages."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


NAME_PATTERN = re.compile(r"^[a-z0-9-]+$")


def quoted_value(text: str, key: str) -> str | None:
    match = re.search(rf'^\s*{re.escape(key)}:\s*"([^"]*)"\s*$', text, re.MULTILINE)
    return match.group(1) if match else None


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    metadata_file = skill_dir / "agents" / "openai.yaml"
    if not skill_file.is_file():
        return ["SKILL.md is missing"]

    lines = skill_file.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return ["SKILL.md must start with YAML frontmatter"]
    try:
        closing = lines.index("---", 1)
    except ValueError:
        return ["SKILL.md frontmatter is not closed"]

    fields: dict[str, str] = {}
    for line in lines[1:closing]:
        key, separator, value = line.partition(":")
        if not separator or not key.strip() or not value.strip():
            errors.append(f"invalid frontmatter line: {line!r}")
            continue
        key = key.strip()
        if key in fields:
            errors.append(f"duplicate frontmatter key: {key}")
        fields[key] = value.strip().strip('"')

    if set(fields) != {"name", "description"}:
        errors.append("frontmatter must contain exactly name and description")
    name = fields.get("name", "")
    description = fields.get("description", "")
    if name != skill_dir.name:
        errors.append(f"skill name {name!r} must match directory {skill_dir.name!r}")
    if len(name) > 64 or not NAME_PATTERN.fullmatch(name):
        errors.append("skill name must be at most 64 lowercase letters, digits, or hyphens")
    if not description or "TODO" in description:
        errors.append("skill description must be complete")
    if not any(line.strip() for line in lines[closing + 1 :]):
        errors.append("SKILL.md body is empty")

    if not metadata_file.is_file():
        errors.append("agents/openai.yaml is missing")
        return errors
    metadata = metadata_file.read_text(encoding="utf-8")
    display_name = quoted_value(metadata, "display_name")
    short_description = quoted_value(metadata, "short_description")
    default_prompt = quoted_value(metadata, "default_prompt")
    if not display_name:
        errors.append("interface.display_name is missing")
    if not short_description or not 25 <= len(short_description) <= 64:
        errors.append("interface.short_description must be 25-64 characters")
    if not default_prompt or f"${name}" not in default_prompt:
        errors.append(f"interface.default_prompt must mention ${name}")
    if "allow_implicit_invocation: true" not in metadata:
        errors.append("policy.allow_implicit_invocation must be explicit")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dirs", nargs="+", type=Path)
    args = parser.parse_args()

    failed = False
    for skill_dir in args.skill_dirs:
        errors = validate_skill(skill_dir)
        if errors:
            failed = True
            for error in errors:
                print(f"{skill_dir}: {error}")
        else:
            print(f"valid: {skill_dir}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
