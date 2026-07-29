---
name: roweb-skill-router
description: Use before any substantive ROWEB task to select the minimum set of repository skills and required evidence.
version: 1.0.0
owners: [ROWEB]
tags: [roweb, router, mmorpg]
---

# ROWEB Skill Router

## Purpose

Route work to the smallest correct skill set while preserving the roBrowserLegacy, rAthena, asset, security, and verification contracts.

## Mandatory first actions

1. Read `/AGENTS.md`, `/README.md`, architecture, roadmap, playbook, security boundary, and deeper `AGENTS.md` files.
2. Inspect the current branch, diff, active work package, pinned commits, and compatibility lock.
3. State the selected skills and why each applies.
4. Do not implement until task boundaries and acceptance evidence are explicit.

## Routing table

- Repository discovery or unfamiliar area → `roweb-repository-orientation`
- New or changed agent skill → `roweb-skill-author`
- Cross-component architecture → `roweb-system-architecture`
- rAthena runtime, configuration, source, NPC, item, mob, skill, or persistence → `rathena-server-engineering`
- Packet, PACKETVER, handshake, opcode, framing, or disconnect → `rathena-packet-protocol`
- roBrowser rendering, entities, input, UI integration, or bootstrap → `robrowser-client-engineering`
- WSS/wsProxy/session handoff/backpressure → `roweb-wss-gateway`
- GRF, path encoding, manifest, extraction, publishing, cache, map, sprite, model, effect, or audio → `ragnarok-asset-pipeline`
- Game loop, classes, combat, progression, economy, quest, party, guild, or content → `mmorpg-game-systems`
- Protocol fixtures, browser flow, gameplay regression, visual checks → `roweb-testing`
- CCU, hotspot, soak, latency, or capacity → `mmorpg-load-testing`
- Authentication, abuse, duplication, injection, secrets, or threat modeling → `mmorpg-security`
- Metrics, logs, traces, alerting, deploy, backup, rollback, live event, or incident → `roweb-operations`
- Any completion claim → `roweb-verification-gate`

## Multi-skill ordering

Use this order when several skills apply:

1. repository orientation
2. architecture or game-system design
3. domain implementation skill
4. security and IP boundary review
5. testing or load testing
6. operations and deployment
7. verification gate

## Stop conditions

Stop and report BLOCKED when:

- required source or runtime evidence is unavailable
- PACKETVER or protocol behavior would be guessed
- a change would add licensed asset bytes or secrets to Git
- the requested behavior makes the browser authoritative
- unrelated working-tree changes cannot be isolated
- validation cannot exercise the affected runtime path

## Required handoff

Return status, selected skills, scope, changed paths, checks, evidence, limitations, rollback, and next executable action.