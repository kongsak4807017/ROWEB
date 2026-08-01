# ADR-025: Unity start gate

- Status: Accepted
- Date: 2026-08-01

## Context

Starting Unity runtime development before the current production client is stable would divide engineering effort and leave two incomplete delivery tracks.

## Decision

Production Unity runtime coding starts only after a clean browser profile completes the approved roBrowser production vertical slice and all additional conditions pass: no critical blocker, locked packet profile, captured vertical-slice golden fixtures, validated asset catalog, repeatable deployment and rollback, baseline telemetry, approved missing-asset threshold, and a successful handoff dry run.

## Alternatives considered

- Start Unity immediately in parallel: rejected because it competes with the production-critical vertical slice.
- Defer all Unity-related work: rejected because source pinning, contracts, fixtures, and research documents are reusable and low-risk now.

## Consequences

- Research freeze and shared-contract work are allowed before the gate.
- Creating, porting, upgrading, or publishing Unity runtime code is prohibited before the gate.
- Gate evidence must be stored or linked from GitHub.

## Reversal conditions

The gate may be modified only by an accepted ADR that identifies the changed evidence, resource allocation, delivery impact, and rollback strategy.

## Evidence

- Approved design: `docs/superpowers/specs/2026-08-01-roweb-long-term-handoff-design.md`
- Production milestone: `README.md`
- Implementation playbook: `docs/IMPLEMENTATION_PLAYBOOK.md`

## Owner

ROWEB repository owner and maintainers.
