# ADR-021: rAthena remains authoritative

- Status: Accepted
- Date: 2026-08-01

## Context

ROWEB already depends on optimized rAthena for MMORPG gameplay, persistence, operational behavior, and compatibility. Reference projects include custom server implementations, but replacing rAthena would recreate mature systems and introduce substantial integrity and operational risk.

## Decision

Optimized rAthena remains authoritative for accounts, characters, maps, movement, combat, skills, items, NPCs, parties, guilds, economy, persistence, and server administration. No replacement .NET MMORPG server is planned for ROWEB.

## Alternatives considered

- Adopt the RagnarokRebuildTcp custom .NET server: rejected because its protocol, gameplay model, persistence, and feature coverage are separate from ROWEB's rAthena baseline.
- Maintain two authoritative servers: rejected because it would split content, operations, tests, and economy integrity.

## Consequences

- Both current and future clients must conform to the approved rAthena compatibility profile.
- Custom server code may be studied for architecture ideas but is not a production dependency.
- Server optimization and observability investments remain reusable across clients.

## Reversal conditions

Replacement may be considered only through a new architecture decision supported by full feature parity, migration, persistence-integrity, security, load, recovery, and operational evidence.

## Evidence

- Approved design: `docs/superpowers/specs/2026-08-01-roweb-long-term-handoff-design.md`
- Compatibility baseline: `compatibility.lock.json`
- System architecture: `docs/ARCHITECTURE.md`

## Owner

ROWEB repository owner and maintainers.
