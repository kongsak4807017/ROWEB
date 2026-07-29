---
name: mmorpg-game-systems
description: Use for game loop, classes, combat, progression, economy, quests, drops, crafting, party, guild, social, or live-content design.
version: 1.0.0
owners: [ROWEB]
tags: [mmorpg, gameplay, economy]
---

# MMORPG Game Systems

## Principles

Design for server authority, long-term economy health, understandable player choices, operational observability, and incremental rollout. Preserve the approved Ragnarok pre-renewal baseline unless a documented product decision changes it.

## Workflow

1. Define player problem, target cohort, core loop, success metric, guardrails, and non-goals.
2. Map state ownership and dependencies across client, rAthena, database, content, and operations.
3. Model formulas and tables for progression, combat, rewards, sources/sinks, drop rates, cooldowns, and social effects.
4. Evaluate abuse, botting, duplication, inflation, monopolies, power creep, and new-player impact.
5. Implement behind a reversible configuration or staged content release where possible.
6. Test normal, boundary, adversarial, persistence, rollback, and migration scenarios.
7. Instrument participation, completion, retention proxy, economy flow, error, and exploit indicators.

## Required outputs

Design specification, formulas/tables, data changes, content changes, balance simulation assumptions, test matrix, metrics, rollout, rollback, and post-launch review criteria.

## Economy gate

Every currency/item change must identify faucets, sinks, velocity, stock accumulation, price/inflation indicators, exploit paths, and recovery options.