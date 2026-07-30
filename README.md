# Codex Orchestration Suite

Two independently invocable, composable Codex Skills for coordinating work at different scales:

- `orchestrate-project-sessions` manages durable, user-visible Codex tasks, Local checkouts, Git worktrees, monitoring, integration, and final project verification.
- `team-mode` manages short-lived native subagents inside one task with explicit Explorer, Executor, Complex Executor, and Reviewer profiles.

The project controller chooses the lightest safe execution surface instead of forcing every work item through the same workflow. Team Mode also remains a complete standalone entry point for users who only need bounded native-subagent coordination.

```text
Project controller
|- main thread: short or decision-heavy work
|- Team Mode: bounded work that can return inside the current task
|- Local task: durable work needing independent history or steering
`- Worktree task: concurrent code writing with filesystem isolation
```

## Design

Both Skills use the same dispatch and verification contract. The canonical source is [`shared/coordination-contract.md`](shared/coordination-contract.md); standalone copies are synchronized into each Skill so either Skill remains self-contained when installed separately.

The important boundary is authorization: Team Mode may activate implicitly for substantial work, but it never creates user-visible tasks. Project Sessions creates those tasks only after the user explicitly requests multi-task orchestration.

## Upstream preservation

The Team Mode Skill preserves the complete behavior and supporting resources from [`oil-oil/codex-team-mode`](https://github.com/oil-oil/codex-team-mode) commit `37e524f590f4f2bc68845c681a38e4bacfaadf74`. Suite-specific coordination is appended after an explicit marker and kept in a separate reference; upstream onboarding, dispatch, routing, context reuse, finding handling, usage analysis, evaluation guidance, tests, and Agent profiles remain intact.

Project Sessions starts from the user's original Skill and adds the cross-layer execution-surface decision, fail-closed worker `Subagent policy`, shared concurrency accounting, child reporting, and durable-task escalation boundary. Neither Skill is a reduced wrapper around the other.

## Layout

```text
agents/                         Team Mode custom Agent profiles
shared/coordination-contract.md Canonical cross-skill contract
skills/orchestrate-project-sessions/
skills/team-mode/
scripts/sync_suite_resources.py
tests/
```

## Local installation

Install or copy both Skill directories into the active Codex skills directory. Team Mode additionally requires the five TOML profiles under `agents/` or `skills/team-mode/assets/agent-profiles/` to be copied to `~/.codex/agents/` or a trusted project's `.codex/agents/` directory. Inspect existing same-named files before replacing them, then open a new Codex task or restart Codex.

## Development

```bash
python3 scripts/sync_suite_resources.py --check
python3 scripts/validate_skills.py skills/orchestrate-project-sessions skills/team-mode
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/orchestrate-project-sessions
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/team-mode
python3 -m unittest discover -s tests -v
```

MIT License.
