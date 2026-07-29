---
name: roweb-operations
description: Use for observability, deployment, configuration, backup, restore, live operations, maintenance, rollback, or incident response.
version: 1.0.0
owners: [ROWEB]
tags: [operations, observability, deployment]
---

# ROWEB Operations

## Workflow

1. Define service inventory, dependencies, owners, SLOs, health signals, configuration, and data stores.
2. Instrument browser bootstrap, asset delivery, WSS/gateway, login/char/map servers, and database with correlated metrics, structured logs, and traces where practical.
3. Build dashboards and alerts around user-visible failure, saturation, error budget, packet/session failures, map tick delay, DB latency, asset/cache errors, and deployment health.
4. Deploy through staged environments with immutable versions, compatibility checks, graceful gateway drain, database backup/migration gates, and automated smoke tests.
5. Validate rollback, restore, restart ordering, reconnect behavior, and disaster recovery objectives.
6. For live events, define schedule, feature/config toggles, economy impact, monitoring, abuse controls, and reversal.
7. For incidents, preserve evidence, contain impact, communicate status, recover service/data, and write corrective actions.

## Required evidence

Environment manifest, release ref, config diff, migration/backup record, smoke/E2E results, dashboards/alerts, rollback result, known limitations, and operator runbook.

## Safety

Never store secrets or licensed assets in logs, dashboards, images, backups committed to Git, or incident reports.