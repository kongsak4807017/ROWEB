---
name: replace-with-kebab-case
description: Use when the agent must ...
version: 1.0.0
owners: [ROWEB]
tags: [roweb]
---

# Skill title

## Purpose

State the outcome this skill produces.

## Use when

- Observable trigger.

## Do not use when

- Route to another named skill.

## Required context

- Files, commits, runtime state, credentials, or tools required.

## Non-negotiable constraints

- Inherit `/AGENTS.md`.
- Add domain-specific safety and architecture rules.

## Workflow

1. Inspect the current state.
2. Record assumptions and unknowns.
3. Design the smallest valid change.
4. Implement in isolated units.
5. Run verification.
6. Record evidence and rollback.

## Deliverables

- Exact files or artifacts.
- Machine-readable report when practical.
- Documentation update.

## Verification

```text
command:
expected result:
evidence path:
```

## Failure and rollback

- Stop conditions.
- Safe rollback procedure.
- Data recovery requirements.

## Handoff

```text
status: PASS | FAIL | BLOCKED
scope:
commit/ref:
checks executed:
results:
evidence:
known limitations:
rollback:
next executable action:
```

## References

- Primary and pinned sources only where possible.