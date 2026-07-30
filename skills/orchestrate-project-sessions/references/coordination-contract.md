# Coordination Contract

Use this contract whenever work leaves the current main thread, whether it goes to a native subagent or a durable Codex task.

## Select The Execution Surface

Choose the lightest surface that satisfies the work's actual needs.

| Surface | Use when | Do not use when |
|---|---|---|
| Main thread | The work is short, decision-heavy, tightly coupled to current context, or cheaper to do directly | A focused isolated context or durable independent history has clear value |
| Native subagent | The work is bounded, can return in the current task, and benefits from focused context, lower cost, parallelism, or independent review | It needs user-visible history, long-running steering, or a separate writable checkout |
| Durable Local task | The work needs visible history, independent steering, long runtime, or later user follow-up | Concurrent writers need filesystem isolation |
| Durable Worktree task | A code-writing task can run independently and needs an isolated checkout | Its prerequisites or architecture are unresolved |
| Read-only task | Long-running research, architecture, or verification needs visible independent history | A short native Explorer or Reviewer can return in the current task |

Do not delegate merely to complete a role sequence. Count briefing, monitoring, inspection, waiting, and rework as coordination cost.

## Required Dispatch Packet

Define these fields before every dispatch:

- `Outcome`: independently verifiable result.
- `Benefit`: material advantage over keeping the slice in the current thread.
- `Context / Sources`: every path, URL, dataset, decision, or raw artifact required for factual work.
- `Scope / Ownership`: allowed reads and writes, the single writer, exclusions, and external-action authority.
- `Dependencies`: prerequisites, available inputs, and downstream consumers.
- `Deliverables`: exact artifacts, changes, documentation, and evidence required.
- `Environment`: Main, Native subagent, Local, Worktree, or Read-only.
- `Checks`: acceptance criteria and validation owned by the worker.
- `Stop when`: completion, blocker, decision conflict, or evidence threshold that ends the work.
- `Return`: concise completion report format.
- `Subagent policy`: `disabled` or `allowed`; when allowed, include permitted roles, maximum children, write boundary, and concurrency budget.

Do not dispatch if the outcome, sources, ownership, checks, or stop condition are incomplete. Resolve product, architecture, editorial, safety, and rollback decisions in the controller first.

## Review Extension

For independent review, also provide:

- `Unresolved risk`: one concrete risk that fresh judgment can resolve.
- `Evidence`: exact stable artifacts to inspect.
- `Checks already passed`: trustworthy validation that should be reused.
- `Do not repeat`: broad checks or debate the reviewer must not redo.

Require findings ordered by severity and a usable partial verdict when the stop condition arrives. A completion marker proves only that a worker stopped; the controller still verifies quality.

## Concurrency And Ownership

- Keep one writer per file, artifact, worktree, or mutable external system.
- Parallelize only work with independent inputs and write scopes.
- Reserve capacity for the controller when the runtime exposes a limit.
- Treat nested Team Mode children as part of the parent worker's concurrency and cost budget.
- A worker must not create user-visible tasks unless the user explicitly delegated that authority.
- A worker may use Team Mode only when its dispatch packet sets `Subagent policy: allowed`.
- Child Agents must not create descendants under standard Team Mode.

Route concurrent code writers to separate worktrees. Keep a shared-checkout Team Mode invocation to one writer even when several read-only children run in parallel.

## Lifecycle And Evidence

Use these states when durable tracking is valuable:

`planned`, `dispatched`, `running`, `attention`, `blocked`, `complete`, `verified`, `integrated`, `rejected`.

`complete` means the worker returned. `verified` means the controller checked the artifact and acceptance evidence. `integrated` means dependent project-level verification passed after handoff or merge.

The completion report must include:

1. outcome;
2. changed files, sources, branches, or systems;
3. verification performed and results;
4. child Agents or durable tasks created, if any;
5. remaining risks, skipped checks, and recovery considerations;
6. the controller action required next.

## Failure And Recovery

- Inspect shared artifacts and Git state before retrying an interrupted worker.
- Reuse the same worker when its context is useful and recovery remains bounded.
- Retry a transient failure at most once unless new evidence changes the plan.
- Do not silently reduce deliverables or replace the requested outcome with an easier proxy.
- Return unresolved decisions to the controller instead of inventing requirements.
- Verify actual runtime role, model, permissions, task identity, and terminal state from available metadata rather than worker self-report.

## Authority Boundary

Delegation does not expand authority. Do not commit, push, merge, publish, deploy, send messages, migrate data, or change external systems unless those actions are explicitly within the user's request. Never copy secrets into dispatch packets or ledgers.
