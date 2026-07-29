---
name: roweb-testing
description: Use for unit, integration, protocol, browser E2E, gameplay, visual regression, accessibility, or release acceptance testing.
version: 1.0.0
owners: [ROWEB]
tags: [testing, e2e, protocol]
---

# ROWEB Testing

## Test pyramid

1. Pure unit tests for parsers, normalization, state transitions, and formulas.
2. Contract tests for manifests, packets, database, and component interfaces.
3. Integration tests across browser/gateway/rAthena/database boundaries.
4. E2E tests for the production vertical slice.
5. Load, soak, fault, security, accessibility, and recovery tests.

## Mandatory vertical slice

Clean browser → bootstrap → automatic assets → WSS login → character select → enter `prt_fild08` → render terrain/entities → reload with cache reuse.

## Workflow

1. Convert each requirement and failure mode into an observable assertion.
2. Use synthetic assets and sanitized packet fixtures.
3. Make fixtures deterministic and versioned against pinned commits.
4. Capture command, environment, seed, duration, result, logs, metrics, and evidence paths.
5. Test fresh profile, cache hit, reconnect, server restart, missing/corrupt asset, malformed packet, resize, keyboard-only, and representative mobile viewport.
6. Quarantine only with owner, reason, expiry, and linked repair issue.

## Completion rule

Code inspection, screenshots alone, or a single happy path are insufficient. A PASS requires relevant tests plus actual runtime exercise and no asset/secret leakage.