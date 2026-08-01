# ROWEB Long-Term Handoff Design

**Date:** 2026-08-01  
**Status:** Approved design; implementation plan pending  
**Repository:** `kongsak4807017/ROWEB`

## 1. Purpose

This design preserves the highest-value long-term path for ROWEB while keeping the current execution priority unchanged:

1. Finish and release the modernized `roBrowserLegacy` production client first.
2. Keep optimized `rAthena` as the authoritative MMORPG server.
3. Prepare shared contracts, evidence, fixtures, documentation, and handoff materials now so a future team can build the ROWEB Enhanced Client without depending on historical ChatGPT conversations or the original maintainer.
4. Defer Unity runtime implementation until the roBrowser production vertical slice passes its release gate.

The deliverable is a GitHub-native handoff package that allows another developer or AI agent to understand, run, test, deploy, extend, and eventually start the Unity client track from repository evidence alone.

## 2. Product decision

### Current production track

```text
Modernized roBrowserLegacy
+ server-managed browser assets
+ WSS gateway
+ optimized rAthena
= ROWEB Production Classic Client
```

### Long-term enhanced track

```text
ROWEB Unity Enhanced Client
+ shared ROWEB contracts
+ engine-neutral asset catalog
+ Athena protocol adapter
+ optimized rAthena
= strategic next-generation client
```

### Permanent server decision

`rAthena` remains authoritative for accounts, characters, maps, movement, combat, skills, items, NPCs, parties, guilds, economy, persistence, and server administration.

The custom .NET server in `RagnarokRebuildTcp` is a research reference only. It is not the planned production replacement for rAthena.

## 3. Reference-source roles

### roBrowserLegacy

Role:

- current production client baseline
- browser rendering and behavior reference
- Athena packet coverage reference
- source of golden runtime observations

### optimized rAthena

Role:

- authoritative game server
- compatibility baseline
- performance and observability baseline
- long-term shared backend for both clients

### UnityRO

Role:

- Athena protocol reference for a Unity client
- RO-format rendering reference
- historical implementation reference

Constraints:

- upstream release reference: `0.6.1`
- old Unity baseline
- runtime-GRF architecture is not the target ROWEB delivery model
- AGPL-3.0 boundary must be reviewed before reuse
- not a production dependency by default

### RagnarokRebuildTcp

Role:

- modern Unity project and rendering reference
- asset-import pipeline reference
- Addressables, map processing, lighting, minimap, sprite, icon, and effect tooling reference
- concurrency and custom protocol research reference

Constraints:

- its custom .NET server is research-only for ROWEB
- its client does not directly implement the rAthena protocol
- no assumption that changing endpoints will make it rAthena-compatible

## 4. Recommended approach

Use a **contract-first handoff** strategy:

```text
Finish roBrowser Alpha
+ create shared contracts during current work
+ capture golden packet fixtures from the working system
+ document operations and decisions
+ defer Unity runtime code
```

This approach creates reusable foundations without splitting delivery effort across two unfinished clients.

## 5. Work required now

### 5.1 Architecture Decision Records

Create ADRs covering:

- client product strategy
- rAthena remaining authoritative
- dual-client boundary
- engine-neutral asset catalog
- reference-source and licensing policy
- Unity start gate

Each ADR must contain context, decision, alternatives, consequences, reversal conditions, evidence, date, and owner.

### 5.2 Source Reference Registry

Create `research/source-registry.yaml` containing, for every external or forked source:

- repository
- upstream repository
- exact commit or tag
- license
- assigned role
- allowed use
- prohibited use
- production dependency status
- last review date

The registry must include at least:

- `kongsak4807017/roBrowserLegacy`
- `kongsak4807017/rathena`
- `kongsak4807017/unityro`
- `guilhermelhr/unityro` tag `0.6.1`
- `kongsak4807017/RagnarokRebuildTcp`

### 5.3 Engine-neutral Asset Catalog

The current asset-catalog work must not encode only roBrowser runtime paths.

Required schema direction:

```json
{
  "assetId": "map.prontera.world",
  "assetType": "map",
  "source": {
    "rsw": "data/prontera.rsw",
    "gnd": "data/prontera.gnd",
    "gat": "data/prontera.gat"
  },
  "dependencies": [],
  "targets": {
    "robrowser": {
      "runtimePath": "data/prontera.rsw"
    },
    "unity": {
      "addressableKey": "maps/prontera",
      "conversionProfile": "ro-map-v1"
    }
  }
}
```

The Unity target may remain unimplemented initially, but the schema must preserve the target boundary.

Planned files:

```text
contracts/asset-catalog.schema.json
contracts/asset-manifest.schema.json
contracts/asset-dependency.schema.json
tools/validation/
tests/contracts/
```

### 5.4 Shared Compatibility Profile

Create one machine-readable profile specifying:

- exact rAthena commit
- gameplay mode
- PACKETVER
- client family
- packet-obfuscation policy
- encoding policy
- supported clients
- conformance level per client

Example direction:

```yaml
profile_id: ROWEB_CLASSIC_PRE_RE_V1
server:
  repository: kongsak4807017/rathena
  commit: <exact-sha>
  gameplay_mode: pre-renewal
protocol:
  packetver: 20211103
  client_family: main
  packet_obfuscation: true
  encoding: cp949-utf8-bridge
clients:
  robrowser:
    supported: true
    conformance_level: production
  unity:
    supported: false
    conformance_level: planned
```

The exact values must come from the active compatibility lock rather than this example.

### 5.5 Golden Packet Fixtures

Capture deterministic packet fixtures from the working roBrowser-to-rAthena vertical slice.

Minimum fixture groups:

- login accepted
- character list
- character selected
- map-server handoff
- map entered
- entity spawn
- entity movement
- NPC dialog
- inventory list
- item added
- skill list
- combat damage
- map change
- disconnect

Each fixture must include:

- raw bytes
- direction
- packet ID
- PACKETVER
- decoded representation
- expected ROWEB domain event
- source test scenario

Proposed location:

```text
protocol/fixtures/login/
protocol/fixtures/character/
protocol/fixtures/map/
protocol/fixtures/inventory/
protocol/fixtures/combat/
protocol/fixtures/npc/
```

No credentials, personal data, or licensed game assets may be stored in fixtures.

### 5.6 Domain Event Contract

Clients should not bind presentation code directly to Athena packets.

Define stable ROWEB domain events such as:

```text
session.login.accepted
session.character.list.received
session.character.selected
world.map.entered
world.entity.spawned
world.entity.moved
combat.damage.applied
inventory.item.added
npc.dialog.opened
party.member.updated
```

Target flow:

```text
Athena packet
→ protocol adapter
→ ROWEB domain event
→ client state
→ roBrowser or Unity presentation
```

roBrowser does not need a full immediate rewrite. The first implementation should cover only the production vertical slice.

### 5.7 Shared Launch-Ticket and Gateway Contract

Both clients must use the same session-entry model:

```text
Portal
→ one-time launch ticket
→ WSS gateway
→ rAthena session
```

Required contracts:

```text
contracts/launch-ticket.schema.json
contracts/gateway-session.schema.json
contracts/gateway-error.schema.json
docs/security/LAUNCH_TICKET_FLOW.md
```

Security requirements include expiration, one-time use, replay prevention, origin validation, audit correlation, and no plaintext account password handoff to the game client.

### 5.8 Shared Telemetry Contract

Define telemetry that can compare clients objectively:

```text
client.boot.started
client.boot.completed
asset.request.started
asset.request.failed
gateway.connected
session.login.completed
map.load.started
map.load.completed
client.frame.performance
client.memory.snapshot
client.error
```

Required common fields:

- `client_type`: `robrowser` or `unity`
- client version
- compatibility profile
- session correlation ID
- timestamp
- device profile

Telemetry must exclude passwords, session secrets, private chat content, and unnecessary personal data.

## 6. Handoff documentation

### 6.1 Developer onboarding

Create:

```text
docs/handoff/START_HERE.md
docs/handoff/REPOSITORY_MAP.md
docs/handoff/LOCAL_DEVELOPMENT.md
docs/handoff/WINDOWS_WORKSPACE.md
docs/handoff/HOW_TO_RUN_ROBROWSER.md
docs/handoff/HOW_TO_RUN_RATHENA.md
docs/handoff/HOW_TO_RUN_FULL_STACK.md
docs/handoff/DEBUGGING_GUIDE.md
docs/handoff/COMMON_FAILURES.md
```

`START_HERE.md` must state:

- authoritative repositories
- canonical Windows workspace
- asset boundary
- branch workflow
- bootstrap commands
- validation commands
- current work package
- Definition of Done
- first suitable issue for a new contributor

### 6.2 Architecture documentation

Create or consolidate:

```text
docs/architecture/SYSTEM_CONTEXT.md
docs/architecture/CONTAINER_ARCHITECTURE.md
docs/architecture/CLIENT_SERVER_BOUNDARY.md
docs/architecture/ASSET_DATA_FLOW.md
docs/architecture/LOGIN_SESSION_FLOW.md
docs/architecture/CLIENT_STRATEGY.md
docs/architecture/FUTURE_UNITY_ARCHITECTURE.md
```

Use GitHub-renderable Mermaid diagrams plus textual explanations.

### 6.3 Operational runbooks

Create:

```text
docs/runbooks/DEPLOY_CLIENT.md
docs/runbooks/DEPLOY_ASSETS.md
docs/runbooks/DEPLOY_RATHENA.md
docs/runbooks/ROLLBACK.md
docs/runbooks/BACKUP_RESTORE.md
docs/runbooks/CACHE_INVALIDATION.md
docs/runbooks/INCIDENT_RESPONSE.md
docs/runbooks/RELEASE_CHECKLIST.md
```

A successor must be able to deploy and roll back without private oral instructions.

## 7. Work explicitly deferred

Do not begin these tasks before the Unity start gate:

- create a production Unity client repository
- upgrade UnityRO to Unity 6
- port UnityRO packet code
- connect RagnarokRebuildTcp directly to rAthena
- build Unity WSS transport
- convert production maps into Unity scenes
- create Unity UI
- publish production Unity Addressables
- benchmark Unity Web builds
- write a replacement .NET MMORPG server
- replace rAthena

Research documentation and source pinning are allowed. Production Unity runtime implementation is not.

## 8. roBrowser production gate

Unity implementation may begin only after a clean browser profile can complete:

```text
open portal
→ receive launch ticket
→ connect through WSS
→ login
→ select character
→ enter map
→ render terrain, player, NPC, and monster
→ move
→ fight
→ receive an item
→ open inventory
→ change map
→ refresh and reuse browser cache
```

Additional gate conditions:

- no critical blocker
- packet profile locked
- vertical-slice golden fixtures captured
- asset catalog validation passes
- deployment and rollback are repeatable
- baseline telemetry works
- missing-asset rate is below the approved threshold
- handoff documentation passes a dry run

## 9. Future Unity work packages

### U0 — Research Freeze

- pin exact source commits
- perform license review
- create feature inventory
- create protocol crosswalk
- create asset-pipeline crosswalk
- produce no production Unity code

### U1 — Clean Foundation

- create a new Unity 6 LTS project
- define assembly boundaries
- establish CI builds
- add unit tests
- create an asset-free Web build shell
- initialize telemetry

### U2 — Athena Protocol Vertical Slice

- WSS transport
- login session
- character session
- map session
- golden-fixture conformance
- domain events
- disconnect and reconnect handling

### U3 — Prontera Rendering Slice

- map conversion/import
- terrain and model rendering
- player, NPC, and monster sprites
- camera and movement
- Addressables/CDN delivery

### U4 — Gameplay Slice

- combat
- item pickup
- inventory
- skills
- NPC dialog
- map transition

### U5 — Comparative Evaluation

Compare Unity and roBrowser using:

- time to first playable
- download size
- peak memory
- FPS and frame-time distribution
- crash and disconnect rates
- map-transition latency
- developer effort
- asset-processing time
- UI implementation effort

Unity becomes an official Enhanced Client only after passing approved evidence gates.

## 10. Target repository structure

```text
ROWEB/
├── README.md
├── AGENTS.md
├── CONTRIBUTING.md
├── SECURITY.md
├── compatibility.lock.json
├── contracts/
│   ├── asset-catalog.schema.json
│   ├── compatibility-profile.schema.json
│   ├── domain-event.schema.json
│   ├── launch-ticket.schema.json
│   └── telemetry-event.schema.json
├── protocol/
│   ├── profiles/
│   ├── fixtures/
│   └── crosswalk/
├── research/
│   ├── source-registry.yaml
│   ├── unityro/
│   └── ragnarok-rebuild-tcp/
├── docs/
│   ├── adr/
│   ├── architecture/
│   ├── handoff/
│   ├── runbooks/
│   ├── security/
│   └── roadmap/
├── tools/
│   ├── asset-catalog/
│   ├── protocol-fixtures/
│   └── validation/
└── tests/
    ├── contracts/
    ├── e2e/
    ├── security/
    └── handoff/
```

## 11. Definition of handoff complete

The project is considered transferable when a developer unfamiliar with the project can, using GitHub documentation alone:

1. identify the authoritative repositories;
2. bootstrap the canonical workspace;
3. run the relevant tests;
4. start the local full stack;
5. complete the production vertical slice;
6. understand the private-asset boundary;
7. publish a changed asset safely;
8. deploy and roll back;
9. explain the principal system boundaries;
10. select and begin an approved issue without private guidance;
11. explain when Unity work may start and what is prohibited before the gate;
12. validate completion using evidence rather than subjective statements.

The handoff must be tested by asking a developer who has not worked on ROWEB to follow `START_HERE.md` without oral assistance. Every point of confusion becomes a documentation or automation defect.

## 12. Acceptance criteria for this design

This design is accepted when:

- it is committed to a dedicated branch;
- a reviewable pull request exists;
- it does not change the current priority of finishing roBrowser;
- it explicitly keeps rAthena authoritative;
- it defines reusable work that should be implemented now;
- it defines the Unity start gate;
- it defines handoff completion in reproducible terms;
- it contains no unresolved placeholders except exact values intentionally delegated to the active compatibility lock.

## 13. Next step after review

After this specification is reviewed and approved in GitHub, create a separate implementation plan that decomposes the work into small, testable pull requests. The first implementation wave should contain only shared contracts, ADRs, source registry, fixture format, and onboarding skeletons. It must not start Unity runtime implementation.
