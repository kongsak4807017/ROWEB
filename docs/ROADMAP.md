# ROWEB Roadmap

## Phase 0 — Repository and compatibility lock

Deliverables:

- pin roBrowserLegacy upstream commit and provenance
- pin rAthena fork/commit and PACKETVER
- define environment configuration
- define asset snapshot/version policy
- establish build, lint, unit-test, and license-boundary checks

Exit criteria:

- reproducible local build
- exact client/server compatibility profile documented
- no licensed assets in Git

## Phase 1 — Local playable baseline

Goal: establish a known-good browser client before modernization.

Deliverables:

- roBrowserLegacy production application starts locally
- pre-extracted asset server serves by canonical path
- wsProxy connects to local rAthena
- login, character select, and map transition work
- `prt_fild08` renders with player, Poring, and one NPC
- camera zoom is clamped and resettable

Exit criteria:

- clean browser profile reaches `prt_fild08`
- map/model/entity behavior matches roBrowserLegacy baseline
- no player GRF upload required

## Phase 2 — Automatic assets and patching

Deliverables:

- asset publisher
- content hashes and manifests
- map dependency manifests
- service worker/cache policy
- progress UI
- clean-cache and warm-cache tests
- rollback to prior asset version

Exit criteria:

- unchanged files are not re-downloaded
- one-file patch downloads only the changed object and manifest
- failed/corrupt content is rejected by hash verification

## Phase 3 — Runtime/UI separation

Deliverables:

- legacy runtime adapter
- normalized domain/UI state
- command adapter
- modern DOM shell over WebGL canvas
- error boundary and diagnostics

Exit criteria:

- UI does not directly manipulate renderer internals
- runtime can emit stable state/events consumed by the UI
- legacy UI can be disabled feature by feature

## Phase 4 — Core Ragnarok UI modernization

Order:

1. launcher/login
2. character select with sprite preview
3. basic HUD: HP/SP/EXP/Zeny/weight
4. hotbar
5. chat
6. minimap
7. inventory/equipment
8. skill window
9. NPC dialog/shop/storage
10. party/guild/settings

Exit criteria:

- keyboard mappings and window behavior are documented and tested
- layout works on supported desktop resolutions and 200% zoom
- UI persists safe window preferences

## Phase 5 — Mobile and accessibility

Deliverables:

- responsive HUD
- touch target sizing
- tap-to-move and optional virtual controls
- pinch zoom with limits
- landscape/portrait policy
- reduced-effects and low-memory profiles
- keyboard-only and screen-reader support for non-canvas UI

Exit criteria:

- agreed Android/iOS browser matrix passes
- gameplay remains usable without accidental browser gestures

## Phase 6 — Production hardening

Deliverables:

- HTTPS/WSS deployment
- static asset CDN/object storage
- gateway health checks, draining, and reconnect behavior
- secrets/config management
- security headers and CSP
- metrics, logs, dashboards, and alerts
- backup/restore drills

Exit criteria:

- production-like environment survives gateway restart and asset rollback
- critical gameplay/persistence paths have operational runbooks

## Phase 7 — Capacity program to 5,000 CCU

Load stages:

```text
250 → 500 → 1,000 → 2,000 → 3,500 → 5,000 → 6,500+
```

Deliverables:

- realistic simulated clients
- map hotspot scenarios
- map-server partition experiments
- wsProxy pool and WSS load balancer
- MariaDB profiling/tuning
- script/static analysis and hotspot removal
- soak and recovery tests

Exit criteria:

- 5,000 CCU SLO passes on documented infrastructure
- overload behavior is controlled
- no data corruption during failure/recovery tests

## Phase 8 — Content expansion

Only after the first vertical slice and operations baseline are stable:

- additional towns/fields/dungeons
- quests and events
- broader equipment/monster/effect coverage
- administrative and account portal features

## Program rule

A phase may begin in limited parallel only when it does not bypass acceptance criteria of the active critical path. Visual expansion must not hide failures in automatic assets, map rendering, gameplay connectivity, persistence, or observability.