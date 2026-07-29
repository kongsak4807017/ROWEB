---
name: mmorpg-load-testing
description: Use for CCU targets, gateway/rAthena/database capacity, hotspot simulations, soak tests, latency, or scaling claims.
version: 1.0.0
owners: [ROWEB]
tags: [load-testing, capacity, performance]
---

# MMORPG Load Testing

## Capacity rule

Never claim 5,000 CCU from configuration, synthetic idle sockets, or short tests. Approval requires realistic behavior, documented hardware, sustained evidence, percentiles, failures, and recovery.

## Workflow

1. Define workload mix: login bursts, character select, movement, chat, NPC, combat, loot, party/guild, map transitions, reconnect, and idle.
2. Define geography: distributed maps plus Prontera/hotspot concentration.
3. Establish baseline hardware, topology, software commits, configuration, database size, and network limits.
4. Ramp through stepped targets with warm-up, steady state, spike, churn, soak, and recovery phases.
5. Measure success rate, p50/p95/p99 latency, disconnects, queue/backpressure, tick delay, CPU, memory, GC, sockets, bandwidth, DB locks/queries, and asset/CDN traffic separately.
6. Inject gateway loss, map-server loss, DB slowdown, deployment drain, and reconnect storm.
7. Identify saturation point and recommend evidence-based capacity per component plus headroom.

## Required artifacts

Scenario definition, load-generator code, anonymized dataset, environment manifest, raw metrics, charts, bottleneck analysis, failure timeline, tuning diff, rerun comparison, and capacity statement with confidence and limitations.