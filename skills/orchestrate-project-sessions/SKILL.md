---
name: orchestrate-project-sessions
description: Establish the current Codex task as a project controller and coordinate multiple user-visible Codex tasks in the same project. Use when the user asks to create a controller task, manage several project tasks or chats, split work across Local and Git worktrees, track other Codex tasks, send follow-up instructions, wait for results, integrate parallel work, or run a one-controller-plus-many-workers workflow.
---

# Orchestrate Project Sessions

Use one controller task to plan, dispatch, monitor, verify, and integrate work performed by separate Codex tasks in the same project.

## Operating model

- Treat the current task as the controller unless the user explicitly asks to create a separate controller.
- Create user-visible Codex tasks for durable, independently steerable work.
- Use native subagents only for bounded work whose separate history does not need to appear in the project task list.
- Keep the controller responsible for task creation, cross-task communication, integration, and final verification.
- Do not let worker tasks create more user-owned tasks unless the user explicitly delegates that authority.
- Keep mandatory project rules in `AGENTS.md` or checked-in documentation. Do not rely on memory alone.

## Team Mode integration

Keep Project Sessions and Team Mode independently invocable. Read [coordination-contract.md](references/coordination-contract.md) when selecting an execution surface or allowing native subagents inside a durable worker.

- Keep short, tightly coupled, or decision-heavy work in the controller.
- Use `$team-mode` for bounded work that can return inside the current task and does not need durable user-visible history.
- Create a Local, Worktree, or read-only task when the work needs independent steering, durable history, long-running follow-up, or an isolated checkout.
- Never treat Team Mode activation as authority to create a user-visible Codex task.

For every durable worker, set `Subagent policy` to `disabled` or `allowed`. When allowed, state the permitted Team Mode roles, maximum children, write boundary, and concurrency budget. Treat a missing policy as `disabled`. A worker must report every child session and its artifacts and verification evidence to the controller.

## Phase 1: Ground the controller

1. Confirm the current project root and working directory.
2. Read applicable `AGENTS.md` files and project documentation before dispatching work.
3. Inspect Git status, current branch, relevant plans, and existing task or progress files.
4. Discover the current Codex task-management tools when they are not already callable. Look for:
   - task creation or forking;
   - task listing and reading;
   - waiting for task progress;
   - sending messages or follow-up prompts;
   - task title, pin, archive, and handoff operations.
5. List recent project tasks before creating new ones. Reuse a clearly matching active task instead of duplicating it.
6. State the project objective, constraints, definition of done, and unresolved blockers.

If the request is materially ambiguous, ask only the one question that changes task boundaries or architecture. Otherwise inspect the project and continue automatically.

## Phase 2: Build the task graph

Split work by independently verifiable outcomes, not by arbitrary file counts.

For every proposed worker task, define:

- title and desired outcome;
- owned files, directories, components, or responsibility;
- forbidden or shared areas;
- dependencies and required inputs;
- exact deliverables;
- verification commands or review criteria;
- the completion report expected by the controller;
- Local or Worktree execution environment.

Also include the shared contract's `Benefit`, `Context / Sources`, `Stop when`, `Return`, and `Subagent policy` fields. Set every native child's own `Subagent policy` to `disabled` so Team Mode fan-out remains owned by the durable worker that was explicitly authorized to use it.

Run tasks in parallel only when their inputs and write scopes are independent. Run dependent tasks sequentially.

Never assign two concurrent tasks write access to the same file or external source. If overlap is unavoidable, assign one owner and make the other task read-only, or sequence the tasks.

Use the brief template in [session-templates.md](references/session-templates.md) when dispatching tasks.

## Phase 3: Choose task and workspace type

Choose the lightest safe execution surface:

- Use a native subagent for a short, bounded investigation or review returned in the current controller turn.
- Create a separate Codex task when the work needs a visible history, independent steering, long runtime, or separate user follow-up.
- Fork the controller task only when the worker genuinely needs most of the controller conversation. Otherwise create a fresh task with a self-contained brief.
- Use Local for the controller, integration, and work that must use the user's active checkout.
- Use a Git Worktree for concurrent code-writing tasks.
- Use a read-only task for review, architecture, research, or verification that must not edit project files.
- Use Handoff when a completed or blocked Worktree task needs to continue in Local.

Do not invent tool arguments. Fetch the current schema, preserve opaque task and host identifiers exactly, and follow the active Codex surface's task-creation rules.

Creating tasks is authorized only when the user explicitly invokes this skill or clearly asks to start or manage multiple Codex tasks. Otherwise produce the task graph without creating tasks.

## Phase 4: Dispatch

1. Give the controller a stable title beginning with `00-` when title tools are available.
2. Give worker tasks ordered, outcome-based titles such as:
   - `10-Requirements`;
   - `20-Backend implementation`;
   - `30-Frontend implementation`;
   - `40-Independent verification`;
   - `50-Integration`.
3. Create only tasks that are ready to run. Do not dispatch a task whose prerequisite is unfinished.
4. Leave one concurrency slot available for the controller when the platform exposes a limit.
5. Dispatch no more than four workers at once unless the user requests broader parallelism or the platform clearly supports it safely.
6. Record each returned task identifier exactly.
7. Send each task its complete brief, including the instruction that other work may be happening concurrently and that it must not revert unrelated changes.
8. Tell each worker to report blockers early and return evidence, not only a completion claim.

Count allowed Team Mode children against the same known runtime capacity as durable workers. Preserve the controller's slot, and reduce durable parallelism when nested native children would otherwise exceed the shared concurrency budget.

Maintain a controller-owned task ledger in the controller context. For long-running projects, create or update `.codex/session-board.md` only when doing so is within the user's requested project scope. Only the controller edits this ledger. Use the ledger template in [session-templates.md](references/session-templates.md).

## Phase 5: Monitor and steer

1. Wait on active tasks using the product's compact multi-task wait mechanism.
2. Reuse returned cursors so already-delivered final text is not repeated.
3. Prefer one bounded wait covering all active tasks over repeated full task reads.
4. Do not narrate unchanged snapshots.
5. When a worker requests attention:
   - read its request;
   - answer directly when the decision is already established by project rules;
   - send a scoped correction when the worker drifted;
   - surface the decision to the user when it is destructive, externally consequential, or materially branching.
6. When a worker fails:
   - identify whether the failure is local, shared, or caused by a missing prerequisite;
   - retry with a narrower instruction when recovery is safe;
   - sequence or reassign the work when scopes conflict;
   - do not silently reduce the requested deliverable.
7. Apply newer user instructions to the affected task branch and preserve unrelated standing constraints.

## Phase 6: Verify worker results

For each completed worker task:

1. Read its final result and claimed evidence.
2. Inspect the actual files, Git state, or connected source affected by the work.
3. Confirm the task stayed within its ownership boundary.
4. Run or review the relevant tests, build, lint, typecheck, or domain-specific checks.
5. Mark the task complete only when the evidence proves its acceptance criteria.
6. Send a repair prompt to the same task when its context is still useful; create a replacement task only when the original task cannot recover.

When a durable worker used Team Mode, verify that its child roles, session traces, write boundaries, concurrency use, changed artifacts, and checks match the worker's `Subagent policy`.

Do not treat a worker's word `complete` as sufficient verification.

## Phase 7: Integrate and close

1. Wait until all prerequisite tasks are terminal.
2. Handoff or merge Worktree work in dependency order.
3. Resolve conflicts in the controller or a dedicated integration task.
4. Run project-level verification after integration.
5. Update project documentation and the session ledger when they are in scope.
6. Report:
   - tasks created or reused;
   - work completed by each task;
   - integrated files or branches;
   - verification evidence;
   - remaining risks or blocked decisions.
7. Archive worker tasks only after their results are integrated or intentionally rejected. Keep the controller task available for future coordination unless the user asks to archive it.

Include native child Agents used by each durable task in the final project report; do not collapse child completion into the worker's unverified completion claim.

## Fallbacks and boundaries

- If native task-management tools are unavailable, do not pretend that separate tasks were created. Use native subagents for bounded work or provide ready-to-dispatch briefs and explain the limitation.
- Do not start OMX Team automatically. Use `$team` only when the user explicitly requests OMX/tmux orchestration and the session is running under the OMX CLI runtime.
- Do not use memory as the authoritative task ledger.
- Do not expose secrets or copy credentials into task briefs, ledgers, or messages.
- Do not commit, push, merge, publish, or change external systems unless those actions are within the user's requested scope.

- If Team Mode returns `Durable task required:`, let the controller decide whether existing user authority covers creating that task; Team Mode never creates it itself.
