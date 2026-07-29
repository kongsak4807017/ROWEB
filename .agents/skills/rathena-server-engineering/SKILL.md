---
name: rathena-server-engineering
description: Use for rAthena source, configuration, NPC, item, mob, skill, map, party, guild, instance, persistence, or pre-renewal behavior changes.
version: 1.0.0
owners: [ROWEB]
tags: [rathena, server, mmorpg]
---

# rAthena Server Engineering

## Constraints

Use the pinned rAthena commit and pre-renewal profile. Preserve server authority. Never edit generated/vendor state without a reproducible patch. Never guess database fields, script commands, or runtime behavior.

## Workflow

1. Identify affected server process: login, char, map, inter-server, SQL, or script engine.
2. Trace configuration/source/database/script flow at the pinned commit.
3. Define compatibility impact: PACKETVER, schema, client data, restart/reload, and persistence.
4. Implement the smallest change with explicit errors and safe defaults.
5. Add unit/script/schema/integration tests using synthetic data.
6. Exercise startup, login, character load, relevant gameplay path, shutdown, and restart persistence.
7. Record migration, reload/restart, rollback, and data recovery steps.

## Domain checklists

- NPC: variable scope, event labels, timers, duplicate names, map placement, reload behavior.
- Skills: IDs, tree, cast/cooldown/range, damage/status, packet/client tables, effects.
- Items/mobs: stable IDs, drops, scripts, trade/storage flags, spawn impact.
- Database: forward migration, backward compatibility, indexes, backup, rollback.

## Evidence

Build output, server logs, exact configs, SQL migration result, gameplay reproduction, persistence check, and asset/IP scan.