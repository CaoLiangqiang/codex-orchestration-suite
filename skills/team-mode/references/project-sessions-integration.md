# Project Sessions Integration

Read this reference only when Team Mode runs inside a durable task controlled by `orchestrate-project-sessions`, or when bounded work may need escalation to a durable task. Do not load it for ordinary standalone Team Mode routing.

## Preserve Independent Entry Points

- Invoke Team Mode directly for bounded native-subagent coordination inside the current Codex task.
- Invoke Project Sessions directly for durable, user-visible tasks, Local or Worktree execution, independent steering, monitoring, and integration.
- Installing both Skills does not make either one a mandatory wrapper around the other.
- Team Mode never creates user-visible tasks, Worktrees, branches, handoffs, or durable descendants.

## Obey The Durable Worker Policy

The Project Sessions controller must include a `Subagent policy` in every durable worker brief:

- `Mode`: `disabled` or `allowed`.
- `Permitted Team Mode roles`: any allowed subset of `Explorer`, `Executor`, `Complex Executor`, and `Reviewer`.
- `Maximum children`: the worker's direct-child limit.
- `Write boundary`: files, artifacts, Worktree, and external systems the children may touch.
- `Concurrency budget`: capacity reserved for the controller, durable workers, and native children.

When the context identifies the current task as a durable Project Sessions worker but the policy is missing, treat it as `disabled`. This fail-closed rule does not apply to a standalone Team Mode invocation outside Project Sessions.

Every child brief must set its own `Subagent policy` to `disabled`; standard Team Mode children do not create descendants. Keep one writer per shared artifact and do not let nested native work cross the durable worker's ownership or authority.

## Report And Escalate

Return each child session, role, changed artifact or source, verification result, unresolved risk, and consumed concurrency slot to the durable worker. The durable worker reports that evidence to the controller, which retains integration and final acceptance.

When bounded native work becomes unsuitable because it needs durable history, long-running or independent user steering, or an isolated writable checkout, stop and return:

```text
Durable task required: <reason, desired environment, ownership, and prerequisite>
```

Do not create, fork, title, hand off, archive, or otherwise manage the durable task from Team Mode.
