# Coordination templates

Read this file when creating worker briefs, maintaining a durable session board, or collecting final task results.

## Worker task brief

```markdown
# Task

## Outcome
Describe the independently verifiable result.

## Benefit
State why this work belongs in a durable task instead of the controller or a native subagent.

## Context / Sources
- Required project facts:
- Required files, URLs, datasets, or decisions:

## Ownership
- Responsible for:
- May modify:
- Must not modify:
- External sources allowed:

You are not alone in the project. Other tasks may run concurrently. Preserve unrelated changes and do not revert work you do not own.

## Dependencies
- Inputs available now:
- Prerequisites:
- Downstream consumers:

## Deliverables
- Required artifact or change:
- Required documentation:
- Required evidence:

## Environment
- Execution surface: Local | Worktree | Read-only
- Branch or Worktree identity:

## Subagent policy
- Mode: disabled | allowed
- Permitted Team Mode roles:
- Maximum children:
- Write boundary:
- Concurrency budget:

## Verification
- Commands or checks:
- Acceptance criteria:

## Stop when
- Completion threshold:
- Blocker or decision threshold:

## Communication
Report shared-file conflicts, scope expansion, missing authority, or blockers to the controller immediately. Do not create more user-owned tasks.

## Completion report
Return:
1. outcome;
2. changed files or sources;
3. verification evidence;
4. child Agents or durable tasks created;
5. unresolved risks;
6. recommended controller action.
```

## Controller session board

Store at `.codex/session-board.md` only for projects that benefit from a durable ledger. Only the controller edits this file.

```markdown
# Codex session board

## Project objective

## Definition of done

## Shared constraints

## Tasks

| Order | Task | Task ID | Environment | Ownership | Dependencies | Child policy | Status | Evidence |
|---:|---|---|---|---|---|---|---|---|
| 10 | Requirements | pending | Read-only | PRD | None | disabled | planned | |

Allowed status values:
`planned`, `dispatched`, `running`, `attention`, `blocked`, `complete`, `verified`, `integrated`, `rejected`.

## Decisions

| Date | Decision | Reason | Affected tasks |
|---|---|---|---|

## Integration order

## Remaining risks
```

## Controller progress update

```markdown
Current result:
- Completed:
- Running:
- Needs attention:

Evidence:
- Tests or checks:
- Integrated work:

Next:
- Immediate action:
- Waiting on:
```

## Worker completion report

```markdown
Outcome:

Changed files or sources:

Child Agents or durable tasks created:

Verification performed:

Acceptance criteria:
- [ ] Criterion 1

Unresolved risks:

Recommended controller action:
```
