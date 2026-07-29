---
name: roweb-verification-gate
description: Use immediately before claiming any ROWEB task, work package, release, fix, or skill is complete.
version: 1.0.0
owners: [ROWEB]
tags: [verification, completion, evidence]
---

# ROWEB Verification Gate

## Rule

Evidence before assertion. Do not say complete, fixed, production-ready, compatible, secure, or capable of a stated CCU unless the affected runtime path has been exercised and the evidence supports that exact claim.

## Workflow

1. Restate scope, acceptance criteria, changed contracts, and exclusions.
2. Inspect the final diff for unrelated changes, placeholders, dead links, secrets, credentials, and licensed asset patterns.
3. Run the narrow tests first, then relevant build, integration, E2E, security, performance, migration, and recovery checks.
4. Exercise the actual affected runtime path with pinned versions and record commands/environment.
5. Compare observed results to every acceptance criterion; classify each PASS, FAIL, or BLOCKED.
6. Verify documentation, compatibility lock, runbooks, and rollback reflect reality.
7. Re-read failure logs and report limitations without minimizing them.

## Mandatory handoff

```text
status: PASS | FAIL | BLOCKED
scope:
commit/ref:
acceptance criteria:
commands/checks executed:
observed results:
evidence paths/links:
asset and secret scan:
known limitations:
rollback status:
next executable action:
```

## Prohibited completion shortcuts

- code inspection only
- unexecuted test plans
- screenshots without logs or assertions
- idle socket counts as MMORPG capacity
- guessed PACKETVER/protocol behavior
- local success without version/environment record
- documentation claiming a future capability as current state