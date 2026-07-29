# ROWEB Implementation Playbook

This playbook converts the roadmap into executable work packages. Each package must produce code, tests, evidence, and a clear handoff.

## WP0 — Baseline intake

Inputs:

- `kongsak4807017/roBrowserLegacy`
- approved rAthena repository/fork
- approved local asset source

Tasks:

1. Record upstream URLs, commits, licenses, and modifications.
2. Build roBrowserLegacy unchanged.
3. Run the Map Viewer and browser application.
4. Capture current configuration and compatibility assumptions.
5. Add a reproducible local start/stop/status workflow.

Outputs:

- compatibility lock file
- build/run instructions
- baseline screenshots and machine-readable environment report

Acceptance:

- fresh checkout builds and starts
- no source assets are committed

## WP1 — Production application mode

Tasks:

1. Add environment-driven endpoints for assets, WSS, registration, and telemetry.
2. Disable GRF/data drop UI in production mode.
3. Retain viewers and local drop capability only under developer routes/flags.
4. Add bootstrap error states and retry behavior.

Acceptance:

- production build never asks a player to select assets
- development Map/GRF/Model viewers remain available

## WP2 — Pre-extracted static asset server

Tasks:

1. Define canonical logical-path normalization.
2. Serve only published entries.
3. Add traversal and extension controls.
4. Add immutable cache headers.
5. Add health and metrics endpoints.

Acceptance:

- roBrowser can request required files by path
- missing/forbidden paths return deterministic errors
- asset traffic is independent of rAthena and wsProxy

## WP3 — Asset publisher and manifests

Tasks:

1. Scan approved extracted data.
2. Hash and publish content-addressed objects.
3. Create bootstrap, asset, and map-bundle manifests.
4. Validate dependency closures.
5. Produce a diff report between asset versions.

Acceptance:

- `prt_fild08` dependency closure is complete
- one-file source change produces a minimal patch delta
- rollback manifest works

## WP4 — Local game stack

Tasks:

1. Start MariaDB.
2. Start rAthena login, char, and map services.
3. Start wsProxy.
4. Start asset server.
5. Start ROWEB frontend.
6. Add ordered shutdown and PID/log capture.

Acceptance:

- one command starts the stack
- one command stops it without orphan processes
- status and smoke scripts identify the failed component

## WP5 — First vertical slice

Scenario:

```text
clean browser
→ automatic bootstrap/assets
→ login
→ character select
→ enter prt_fild08
→ see player + Poring + NPC
```

Tasks:

- pin camera defaults and zoom limits
- verify terrain/models/entity behavior
- verify warm-cache reload
- verify disconnect/reconnect behavior

Acceptance:

- no manual GRF interaction
- no corrupted/missing resource placeholder in the scenario
- screenshots and structured logs are retained as evidence

## WP6 — Runtime adapter and modern UI shell

Tasks:

1. Inventory current legacy UI/event coupling.
2. Define normalized client-side state contracts.
3. Emit runtime events through an adapter.
4. Route UI commands through a command boundary.
5. Mount a DOM overlay above the WebGL canvas.

Acceptance:

- one modern HUD feature is driven only through the adapter
- legacy renderer can evolve independently of DOM UI

## WP7 — Core UI migration

Migrate one window/system at a time:

- HUD
- hotbar
- chat
- minimap
- inventory/equipment
- skills
- NPC dialog/shop/storage

For each system:

- document keyboard/mouse/touch behavior
- preserve gameplay semantics
- add responsive and accessibility tests
- provide a rollback flag until stable

## WP8 — Production platform

Tasks:

- HTTPS/WSS ingress
- CSP/security headers
- gateway pool and sticky sessions
- static asset CDN/storage
- secrets management
- metrics/log dashboards
- backups and restore drill

Acceptance:

- production-like deployment is reproducible
- gateway restart and asset rollback have tested runbooks

## WP9 — Capacity and optimization

Tasks:

- implement realistic load clients
- profile rAthena scripts/timers/SQL
- benchmark wsProxy event-loop and queue depth
- test map-server partitioning
- tune DB from measured working set
- run staged, hotspot, soak, and recovery tests

Acceptance:

- capacity claims are backed by reports, hardware, configuration, and p95/p99 results

## Required evidence for every WP

```text
status: PASS | FAIL | BLOCKED
commit/ref:
tests executed:
results:
artifacts/reports:
known limitations:
next executable action:
```

## Prohibited shortcuts

- Do not copy licensed assets into the repository.
- Do not replace missing assets with arbitrary sprites and call the feature complete.
- Do not bypass rAthena authority with browser-only gameplay state.
- Do not claim production or 5K readiness from a local demo.
- Do not rewrite stable roBrowser map/entity behavior before a test proves the need.