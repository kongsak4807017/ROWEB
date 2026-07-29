---
name: roweb-system-architecture
description: Use when changing component boundaries, data flow, authority, scaling topology, or deployment architecture across ROWEB.
version: 1.0.0
owners: [ROWEB]
tags: [architecture, mmorpg, roweb]
---

# ROWEB System Architecture

## Invariants

- roBrowserLegacy is the browser runtime baseline.
- rAthena owns gameplay and persistence.
- HTTPS asset delivery is separate from WSS gameplay transport.
- Browser UI displays server state and may predict presentation, but never creates authoritative outcomes.
- Licensed assets stay outside Git.

## Workflow

1. Describe the current and proposed end-to-end path from browser to assets, gateway, rAthena, and database.
2. Identify trust boundaries, authority, state ownership, failure domains, scaling units, and compatibility contracts.
3. Evaluate at least two alternatives against correctness, migration cost, operability, security, latency, and rollback.
4. Record an ADR for consequential decisions.
5. Define interface contracts, failure behavior, observability, migration stages, and acceptance tests.
6. Validate the smallest vertical slice before broad expansion.

## Required outputs

- context and decision
- component/interface diagram in text or Mermaid
- authority and data-flow table
- risks and mitigations
- phased migration and rollback
- test and evidence plan

## Architecture rejection criteria

Reject proposals that route asset bytes through rAthena/wsProxy, restart a Unity-first rewrite without an approved ADR, add a second source of gameplay truth, or claim capacity without measured evidence.