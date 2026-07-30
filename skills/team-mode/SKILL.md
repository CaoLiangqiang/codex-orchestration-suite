---
name: team-mode
description: Coordinate the smallest useful set of native custom subagents inside one Codex task for substantial development, research, analysis, planning, document, data, and content work. Use when bounded work benefits from focused context, lower-cost execution, safe parallelism, or fresh independent review and can return without a durable user-visible task. Respect any enclosing Project Sessions Subagent policy, never create durable tasks, and leave unresolved decisions and final acceptance in the current main thread.
---

# Team Mode

Lead the task in the current main thread. Use only the native children that provide more value than their briefing, monitoring, inspection, and rework cost.

## Respect The Enclosing Controller

Team Mode never creates user-visible Codex tasks, Worktrees, branches, handoffs, or descendants. When running inside a durable Project Sessions worker:

- Treat a missing `Subagent policy` as `disabled` unless the user explicitly overrides it.
- When disabled, do not spawn; complete the bounded work directly or report the blocker.
- When allowed, obey its permitted roles, maximum children, write boundary, and concurrency budget.
- Report every child session, role, changed artifact, and verification result to the durable task controller.

If work needs durable history, independent user steering, long-running follow-up, or an isolated writable checkout, return `Durable task required:` with the reason and required ownership. Do not create that task yourself.

## Dispatch Gate

Every native spawn must explicitly pass `agent_type` as exactly `Explorer`, `Executor`, `Complex Executor`, or `Reviewer`.

- Never omit `agent_type` and never pass `default` during normal work.
- `task_name` labels a child; it does not select a profile.
- The `default` profile is a fail-closed behavioral guard, not a working Agent or an operating-system boundary.
- If the intended profile is unavailable, keep the work in the main thread or report the readiness problem. Do not silently use a generic child.
- Reject output whose trace shows `default`, `subagent/unknown`, or the wrong runtime model for the requested custom role.

Read [references/custom-agents.md](references/custom-agents.md) only when installing, repairing, customizing, or explicitly verifying profiles and the guard.

## Build The Dispatch Packet

Read [references/coordination-contract.md](references/coordination-contract.md) before the first spawn. Give every child its complete required packet, including `Outcome`, `Benefit`, `Context / Sources`, `Scope / Ownership`, `Dependencies`, `Deliverables`, `Environment`, `Checks`, `Stop when`, `Return`, and `Subagent policy`.

Set every child's `Subagent policy` to `disabled`; standard Team Mode fan-out remains owned by the current main thread.

Keep the work in the main thread when the packet is incomplete or the benefit does not exceed coordination cost. With `fork_turns="none"`, assume the child knows nothing from the parent conversation and name every factual source explicitly.

For Reviewer, also include `Unresolved risk`, `Evidence`, `Checks already passed`, and `Do not repeat`. Start every new Reviewer from fresh context.

## Route The Work

- `Explorer` (Luna Medium, read-only): substantial evidence gathering across current web sources, documents, data, code, APIs, logs, and configuration.
- `Executor` (Luna High, workspace-write): localized, reversible, low-risk work with deterministic checks.
- `Complex Executor` (Terra High, workspace-write): substantial conventional implementation after architecture, scope, safety boundaries, and checks are fixed.
- Main thread: novel architecture, incomplete intent, weak or visual verification, export or compiler design, consequential security or rollback judgment, and final acceptance.
- `Reviewer` (Sol High, read-only): fresh judgment on one concrete important residual risk.

Do not turn these roles into a mandatory pipeline. Team Mode may activate without starting a child.

## Coordinate Children

- Use `fork_turns="none"` by default and always for a new Reviewer.
- Keep all fan-out in the main thread. Children must not create descendants.
- Parallelize only independent inputs and write scopes.
- Keep one writer per shared file, artifact, worktree, or mutable system.
- Reuse an Explorer or executor while its topic and artifact context remain useful.
- Start fresh when independence matters or prior context is stale.
- Do not give an Explorer an expected conclusion or a Reviewer the desired verdict.
- Reserve capacity required by an enclosing Project Sessions controller.

## Verify Returns

Inspect actual sources, files, diffs, runtime metadata, and verification output before accepting delegated work. A child completion marker is not proof of correctness.

If a child errors, times out, or is interrupted, inspect shared artifacts before retrying. Retry a transient failure at most once and only when no usable result exists. Request one bounded partial verdict from an overdue Reviewer, then interrupt and recover in the main thread.

Keep unresolved product, architecture, editorial, safety, and rollback decisions in the main thread.

## Inspect Local Usage

When the user asks for model or child consumption, run `python3 scripts/usage_by_model.py`. For the active task use `--task-id current --by-agent --by-session`; use `--json` for structured output.

Report processed, uncached input, cached input, output, reasoning output, estimated Standard credits, terminal status, effective sandbox, and depth. Explain that local logs exclude unavailable or ephemeral sessions, configured rates do not detect mixed Fast usage, and Codex `/usage` remains authoritative for account limits.

When evaluating routing value, read [references/evaluation.md](references/evaluation.md) before designing the trial.

## Guardrails

- Preserve unrelated work and obey project instructions.
- Treat the parent task's live permission mode as the effective child permission; TOML is only a profile default.
- Delegation does not expand authority to commit, publish, deploy, message, or modify external systems.
- Prefer primary sources for current factual research and distinguish fact from inference.
- Return one coherent result to the user after validating delegated evidence.
