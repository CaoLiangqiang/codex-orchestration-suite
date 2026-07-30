---
name: orchestrate-project-sessions
description: Establish the current Codex task as a project controller and coordinate durable, user-visible Codex tasks across Local and Git worktree environments. Use when the user explicitly asks to create or manage multiple project tasks, preserve independently steerable histories, monitor long-running work, coordinate task dependencies, hand off worktrees, integrate parallel changes, or run a controller-plus-workers workflow. Route short bounded work to Team Mode when available instead of creating unnecessary durable tasks.
---

# Orchestrate Project Sessions

Lead the project from the current task. Choose the lightest safe execution surface, create durable tasks only with explicit user authority, and retain responsibility for integration and final acceptance.

## Ground The Controller

1. Confirm the project root and working directory.
2. Read applicable `AGENTS.md`, project documentation, Git status, branch, and existing progress artifacts.
3. Discover the active task-management capabilities: create or fork, list, read, wait, message, title, handoff, archive, and Worktree support.
4. List recent project tasks when possible and reuse a clearly matching active task.
5. State the objective, constraints, definition of done, concurrency limit, and unresolved decisions.

Do not invent task-tool arguments. Inspect the current schema and preserve opaque task, host, cursor, and Worktree identifiers exactly.

## Select The Execution Surface

Read [references/coordination-contract.md](references/coordination-contract.md) before building the task graph. Apply its surface table and dispatch contract.

- Keep short, tightly coupled, or decision-heavy work in the controller.
- Use `$team-mode` for bounded work that can return inside the current task and does not need durable user-visible history.
- Create a Local task for work needing independent steering, long runtime, visible history, or later follow-up.
- Create a Worktree task for independent concurrent code writing.
- Create a read-only task for durable research, architecture, or verification.

Task creation is authorized only when the user explicitly invokes this Skill or clearly asks to start or manage multiple Codex tasks. Team Mode activation never grants authority to create durable tasks.

If Team Mode is unavailable or its required profiles are not runtime-ready, keep bounded work in the controller or use another authorized surface. Do not claim a custom role was used when runtime metadata cannot prove it.

## Build The Task Graph

Split by independently verifiable outcomes, not arbitrary file counts. For every worker, define the complete dispatch packet from the coordination contract plus:

- ordered title and durable task purpose;
- owned files, components, branches, or systems;
- forbidden and shared areas;
- prerequisites and downstream consumers;
- Local, Worktree, or Read-only environment;
- exact integration order;
- whether Team Mode is `disabled` or `allowed` inside the worker.

When `Subagent policy` is allowed, specify permitted Team Mode roles, maximum children, write boundary, and concurrency budget. Treat missing policy as `disabled`. Worker tasks must report every child session they created.

Run independent tasks in parallel and dependent tasks sequentially. Never give two concurrent tasks write access to the same file or mutable external source. Use separate Worktrees for concurrent writers.

Read [references/session-templates.md](references/session-templates.md) when writing worker briefs or a durable ledger.

## Dispatch Ready Work

1. Give the controller a stable `00-` title when title tools exist.
2. Use ordered outcome titles such as `10-Requirements`, `20-Backend`, `30-Frontend`, `40-Independent verification`, and `50-Integration`.
3. Create only tasks whose prerequisites are satisfied.
4. Reserve one concurrency slot for the controller when the platform exposes a limit.
5. Start no more than `min(4, runtime capacity minus one)` durable workers at once. Use a lower limit when Team Mode children share the same capacity.
6. Count allowed Team Mode children against the controller's known global budget when they share the same runtime limit.
7. Record returned task identifiers exactly.
8. Send each worker a complete brief and require blockers, evidence, and scope conflicts to be reported early.

Maintain task state in controller context. For projects needing durable tracking, create `.codex/session-board.md` only when it is within scope, and let only the controller edit it.

## Monitor And Steer

- Prefer one bounded multi-task wait over repeated full reads.
- Reuse cursors so delivered final text is not repeated.
- Do not narrate unchanged snapshots.
- Apply newer user instructions to affected task branches without dropping unrelated constraints.
- Answer worker questions directly when project rules already decide them.
- Return destructive, externally consequential, architectural, or materially branching decisions to the user.
- Reuse the same worker for bounded repair while its context remains useful.

On failure, identify whether the cause is local, shared, a missing prerequisite, or a scope conflict. Inspect artifacts before retrying. Do not silently reduce the deliverable.

## Verify And Integrate

For every completed worker:

1. Read its report and inspect the actual files, branch, task metadata, and connected sources.
2. Confirm ownership and `Subagent policy` were respected.
3. Run or review relevant tests, builds, linters, type checks, or domain checks.
4. Mark it `verified` only when evidence proves the acceptance criteria.
5. Hand off or merge Worktree results in dependency order.
6. Run project-level checks after integration.

For a concrete consequential residual risk, use a fresh read-only task or Team Mode Reviewer with the review extension from the coordination contract. Do not create an automatic review stage.

Archive workers only after their results are integrated or intentionally rejected. Keep the controller available for future coordination unless the user asks to archive it.

## Close The Project

Report:

- tasks created or reused and their terminal states;
- work completed and any child Agents used by each task;
- branches, Worktrees, files, or systems integrated;
- verification evidence;
- remaining risks, rejected work, and blocked decisions.

## Fallbacks And Boundaries

- If durable task tools are unavailable, do not pretend tasks were created. Use Team Mode for bounded work when authorized and ready, or return ready-to-dispatch briefs.
- Do not let workers create user-visible tasks unless the user explicitly delegates that authority.
- Do not start OMX or tmux orchestration unless explicitly requested in a compatible runtime.
- Keep mandatory project rules in `AGENTS.md` or checked-in documentation, not memory alone.
- Do not expose secrets in briefs, ledgers, or messages.
- Do not commit, push, merge, publish, deploy, or change external systems outside the user's explicit scope.
