# ROWEB — Ragnarok Online in the Browser

ROWEB is the production web-client program for a Ragnarok Online-compatible experience built around **roBrowserLegacy + rAthena**, with modern UI, automatic asset delivery, browser caching, production deployment, and a measured path toward 5,000 concurrent players.

## Product decision

The primary client lane is now:

```text
roBrowserLegacy runtime
+ modern DOM UI/UX
+ automatic server-managed assets
+ WebSocket gateway
+ rAthena authoritative game servers
+ production observability and load testing
```

Unity WebGL is no longer the primary delivery lane. It may remain an R&D/reference track, but ROWEB will not reimplement Ragnarok map, model, SPR/ACT, packet, and entity behavior from zero when roBrowserLegacy already contains a working browser implementation.

## North Star

A first-time player opens one URL and can:

1. Load the web client without selecting or uploading a GRF.
2. Download only required, pre-extracted assets from the server.
3. Cache immutable assets in the browser.
4. Log in through WSS → wsProxy → rAthena.
5. Select a character and enter `prt_fild08`.
6. See terrain, models, player, NPCs, and monsters rendered correctly.
7. Refresh and resume with cache reuse.
8. Receive future patches by downloading only changed files.

## Architecture

```text
Player Browser
├── HTTPS → ROWEB web client
├── HTTPS → asset manifest + static asset server/CDN
└── WSS   → gateway/load balancer
              └── wsProxy pool
                    └── rAthena
                        ├── login-server
                        ├── char-server
                        ├── map-server pool
                        └── MariaDB
```

## Core principles

- **rAthena is authoritative** for accounts, characters, movement, combat, NPCs, monsters, items, maps, and persistence.
- **roBrowserLegacy is the client runtime baseline** for Ragnarok-compatible rendering and behavior.
- **Assets are server-managed.** Players never upload GRFs in production.
- **Assets are pre-extracted and statically served.** Runtime GRF extraction is development/fallback only.
- **Asset traffic never passes through rAthena or wsProxy.**
- **Modern UI uses DOM/CSS over the WebGL canvas.**
- **No licensed assets are committed to Git.**
- **5,000 CCU is an evidence-gated target**, not a configuration claim.

## Repository documents

- [`AGENTS.md`](AGENTS.md) — operating contract for AI agents and developers
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — target system architecture
- [`docs/ASSET_DELIVERY_AND_PATCHING.md`](docs/ASSET_DELIVERY_AND_PATCHING.md) — automatic asset delivery, cache, and patch model
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — phased implementation roadmap
- [`docs/IMPLEMENTATION_PLAYBOOK.md`](docs/IMPLEMENTATION_PLAYBOOK.md) — executable work packages and acceptance gates
- [`docs/RATHENA_5000_CCU_PLAN.md`](docs/RATHENA_5000_CCU_PLAN.md) — capacity, optimization, observability, and load-test plan
- [`docs/SECURITY_AND_IP_BOUNDARY.md`](docs/SECURITY_AND_IP_BOUNDARY.md) — security and asset boundary
- [`docs/DECISION_LOG.md`](docs/DECISION_LOG.md) — architecture decision record

## Initial acceptance milestone

The first milestone is complete only when a clean browser profile can:

```text
open ROWEB
→ load bootstrap manifest
→ download required common assets
→ connect through WSS
→ log into rAthena
→ select a character
→ enter prt_fild08
→ render the map and entities correctly
→ reload using browser cache
```

No additional map, UI feature, or content expansion should outrank this vertical slice.