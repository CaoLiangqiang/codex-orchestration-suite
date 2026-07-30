# Repository Guidelines

- Keep `orchestrate-project-sessions` and `team-mode` as separate skill entrypoints.
- Treat `shared/coordination-contract.md` and root `agents/*.toml` as canonical shared resources. After editing them, run `python3 scripts/sync_suite_resources.py`.
- Do not edit generated coordination-contract or bundled Agent-profile copies directly.
- Preserve explicit authorization before creating user-visible Codex tasks.
- Preserve the `agent_type` dispatch gate and the fixed Team Mode role boundaries.
- Run `python3 scripts/sync_suite_resources.py --check`, `python3 scripts/validate_skills.py skills/orchestrate-project-sessions skills/team-mode`, both official skill-creator validators when available, and `python3 -m unittest discover -s tests -v` before reporting completion.
