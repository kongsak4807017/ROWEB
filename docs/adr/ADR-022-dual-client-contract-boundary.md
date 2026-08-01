# ADR-022: Dual-client contract boundary

- Status: Accepted
- Date: 2026-08-01

## Context

ROWEB must avoid duplicating authentication, compatibility, asset, telemetry, and gameplay-state semantics across the current roBrowser client and a future Unity client.

## Decision

Both clients share versioned ROWEB contracts for launch tickets, gateway sessions and errors, compatibility profiles, domain events, telemetry events, protocol fixtures, and the engine-neutral asset catalog. Client-specific presentation and rendering remain outside these contracts.

## Alternatives considered

- Let each client define independent contracts: rejected because it would produce incompatible login, observability, and content pipelines.
- Expose raw Athena packets directly to all presentation code: rejected because packet changes would propagate through client UI and state layers.

## Consequences

- Contracts require schemas, fixtures, conformance tests, and explicit versioning.
- Protocol adapters translate Athena packets into stable domain events.
- Client-specific optimizations remain possible behind the shared boundary.

## Reversal conditions

A contract may split only when measured platform constraints make a shared contract impossible and a replacement ADR documents compatibility and migration behavior.

## Evidence

- Approved design: `docs/superpowers/specs/2026-08-01-roweb-long-term-handoff-design.md`
- Compatibility lock: `compatibility.lock.json`

## Owner

ROWEB repository owner and maintainers.
