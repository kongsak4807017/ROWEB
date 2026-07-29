# ROWEB Target Architecture

## 1. System context

ROWEB is a browser MMORPG client and production delivery platform built around roBrowserLegacy and rAthena.

```text
Browser
├── Web application shell
├── roBrowserLegacy runtime
├── modern DOM UI
├── service worker/cache
└── WebSocket client

Platform
├── static web hosting
├── asset manifest service
├── immutable static asset storage/CDN
├── WSS load balancer
├── wsProxy pool
├── rAthena login/char/map services
├── MariaDB
└── metrics/logging stack
```

## 2. Responsibility boundaries

### Browser client

Responsible for:

- rendering RSW/GND/GAT/RSM/RSM2 content
- rendering SPR/ACT/PAL entities and effects
- camera, input, UI, local interpolation, and presentation
- resolving server IDs into client resources
- downloading and caching approved assets

Not authoritative for:

- account validity
- character persistence
- item ownership
- movement legality
- combat results
- monster/NPC state
- rewards or economy

### Asset platform

Responsible for:

- publishing pre-extracted approved files
- canonical path resolution
- content hashes and manifests
- immutable caching
- patch version publication
- map dependency bundles and preload hints

It must not execute gameplay logic.

### Gateway

Responsible for:

- WSS termination
- WebSocket-to-TCP forwarding
- session stickiness
- backpressure
- connection limits
- health checks and graceful draining

It must not serve assets or query gameplay SQL.

### rAthena

Authoritative for:

- login/account
- character selection and persistence
- maps, NPCs, monsters, items, skills, combat
- party, guild, storage, vending, quests, and world state

## 3. Production data flow

### Bootstrap

```text
GET web client
→ register service worker
→ GET bootstrap manifest
→ compare client/asset versions
→ preload common resources
→ present login
```

### Login and gameplay

```text
Browser WSS
→ load balancer
→ sticky wsProxy instance
→ rAthena TCP
```

### Map load

```text
rAthena packet: map = prt_fild08
→ client resolves map bundle
→ HTTPS assets from cache/CDN
→ roBrowserLegacy map loader
→ render world
```

### Entity spawn

```text
rAthena packet: class/view/appearance/state
→ client DB/crosswalk resolution
→ cached or lazy-loaded SPR/ACT/PAL
→ action + direction + camera-relative render
```

## 4. Repository strategy

ROWEB should initially import or vendor a pinned roBrowserLegacy baseline with provenance and license notices, then isolate custom work into clear layers:

```text
src/
├── legacy/          # pinned/upstream-derived runtime
├── adapters/        # stable boundary around legacy state/events
├── domain/          # normalized client-side view state
├── ui/              # modern DOM UI
├── platform/        # bootstrap/cache/config/telemetry
└── applications/    # production client and developer viewers
```

Avoid broad rewrites of map and entity rendering until golden tests exist.

## 5. UI architecture

Use the WebGL canvas for the world and DOM/CSS for application UI:

```text
Game root
├── WebGL canvas
└── DOM overlay
    ├── HUD
    ├── chat
    ├── hotbar
    ├── minimap
    ├── windows
    ├── dialogs
    └── mobile controls
```

Introduce an adapter/event boundary:

```text
Legacy runtime events
→ normalized domain store
→ DOM UI

DOM commands
→ command adapter
→ legacy/network runtime
```

The UI must not reach into renderer internals directly.

## 6. Environment separation

### Development

- local GRF/data drop may remain available
- viewers and inspectors enabled
- verbose diagnostics allowed
- local asset server or Remote Client allowed

### Production

- no GRF upload/drop UI
- fixed server-managed asset endpoints
- WSS only
- immutable asset URLs
- controlled diagnostics
- secrets supplied by environment

## 7. Deployment topology

Initial production topology:

```text
CDN/static hosting: web client + assets
Gateway node(s): Nginx/HAProxy + wsProxy
Game node(s): login/char/map-server processes
Database node: MariaDB
Observability: Prometheus-compatible metrics + logs + dashboards
```

Scale components independently. Asset delivery must remain horizontally cacheable and independent from gameplay capacity.

## 8. Compatibility lock

Every release must pin and record:

- roBrowserLegacy commit
- rAthena commit/fork
- PACKETVER/client family
- database schema revision
- asset snapshot/version
- GRF precedence used to publish assets
- ROWEB client build ID

A release is invalid when these versions are ambiguous.