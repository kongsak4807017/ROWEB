# ROWEB Protocol Evidence

This directory stores machine-readable protocol evidence for the pinned roBrowserLegacy and rAthena compatibility profile.

## Fixture classes

- `fixtures/synthetic/` contains fabricated, non-production examples used to validate schemas and tooling.
- Future verified captures must be stored under scenario-specific directories such as `fixtures/login/`, `fixtures/character/`, `fixtures/map/`, `fixtures/inventory/`, `fixtures/combat/`, and `fixtures/npc/`.

## Mandatory fields

Every fixture records direction, packet ID, PACKETVER, raw hexadecimal bytes, decoded representation, expected ROWEB domain event, source scenario, and whether it is synthetic.

## Security and asset boundary

Fixtures must never contain passwords, launch tickets, session secrets, private chat, personal data, licensed game assets, database dumps, or identifying production account values. Verified captures must be sanitized before commit and linked to a reproducible test scenario.

## Compatibility rule

Do not guess PACKETVER. Synthetic fixtures may use `null`; verified runtime fixtures require the value established in `compatibility.lock.json` after runtime verification.

## Intended use

The fixtures are conformance evidence for protocol adapters. They are not a replacement for rAthena source behavior, runtime integration tests, or the compatibility lock.
