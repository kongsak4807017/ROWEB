# ADR-020: Client product strategy

- Status: Accepted
- Date: 2026-08-01

## Context

ROWEB needs a production client that can ship now and a durable path toward a more modern client later. The current roBrowserLegacy track already implements browser delivery and Ragnarok-compatible behavior, while a Unity client would require a new implementation and validation cycle.

## Decision

roBrowserLegacy is the ROWEB Production Classic Client and remains the active delivery priority. Unity is a future ROWEB Enhanced Client and must not displace the roBrowser production work before the approved start gate passes.

## Alternatives considered

- Stop roBrowser and restart as Unity-first: rejected because it creates two unfinished clients and delays production evidence.
- Keep Unity permanently out of scope: rejected because Unity remains valuable for multi-platform rendering and long-term modernization.

## Consequences

- Current engineering effort remains concentrated on the roBrowser vertical slice.
- Shared contracts must be engine-neutral so future Unity work can reuse them.
- Unity progress is measured as a separate product track rather than a rewrite of the current client.

## Reversal conditions

This decision may change only after the roBrowser production gate is complete and comparative evidence shows that another client strategy provides a safer and higher-value production path.

## Evidence

- Approved design: `docs/superpowers/specs/2026-08-01-roweb-long-term-handoff-design.md`
- Current product direction: `README.md`
- Repository operating contract: `AGENTS.md`

## Owner

ROWEB repository owner and maintainers.
