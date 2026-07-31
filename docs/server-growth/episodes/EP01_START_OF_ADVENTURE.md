# EP01 — Start of Adventure

- **Document status:** Draft for owner review
- **Episode ID:** `EP01`
- **Default service pack:** `SP01.0`
- **Purpose:** Establish the initial playable world, first-job progression, foundational economy, essential services, and the asset baseline for all later Episodes.
- **Authority:** The server owner controls inclusion, exclusion, customization, release timing, EXP, drops, spawns, shops, quests, and economy parameters.

## 1. Episode intent

EP01 is the smallest complete production slice of ROWEB. A new player must be able to create a character, enter the world, learn basic controls, choose a first job, level, obtain and trade early equipment, use storage and transport services, form a party, join or create a guild when enabled, and return safely after reconnecting.

EP01 is not defined by one historical server snapshot. It is an owner-controlled launch baseline assembled from the pinned rAthena and Modernized roBrowserLegacy compatibility profile. Every enabled component must be proven against the actual local repositories and asset roots before activation.

## 2. Canonical data roots

The Episode inventory is generated from three read-only roots:

```text
Consumer source root
C:\Ragnarok-Prontera\HermesWorkSpace\roBrowserLegacy

Canonical extracted asset root
C:\Ragnarok-Prontera\assets\data

Published runtime asset root
C:\Ragnarok-Prontera\HermesWorkSpace\roBrowserLegacy\roBrowserLegacy-RemoteClient-PHP\data
```

The canonical product repository is:

```text
C:\Ragnarok-Prontera\HermesWorkSpace\ROWEB
```

No licensed asset bytes are committed to Git. Git stores only manifests, metadata, hashes, mappings, validation reports, schemas, and source code.

## 3. Launch outcomes

EP01 is complete only when all outcomes below pass in staging:

1. Account handoff reaches character selection without browser-visible credentials.
2. Character creation and selection work against the pinned compatibility profile.
3. A new character enters an approved EP01 start location.
4. Every approved EP01 map loads terrain, objects, textures, minimap, music, effects, NPCs, monsters, and collision data.
5. All approved warps resolve to approved maps and cannot enter locked Episodes.
6. Essential NPC services are available and audited.
7. First-job progression works for every enabled launch class.
8. Item icons, equipment sprites, effects, names, descriptions, and server records agree.
9. Reconnect, map change, storage, trade, party, death, respawn, and save-point flows pass.
10. EP01 can be rolled back to the previous release pointer without deleting immutable assets.

## 4. Owner-controlled launch profile

Every content record has one disposition:

- `included`
- `excluded`
- `customized`
- `deferred`
- `staging-only`
- `admin-only`

Recommended initial control groups:

| Group | Default disposition | Owner decision required |
|---|---|---|
| Core towns | Included | Confirm exact maps |
| Beginner fields | Included | Confirm level bands |
| Early dungeons | Customized | Confirm floors and bosses |
| First jobs | Included | Confirm enabled jobs |
| Guild creation | Customized | Confirm cost and timing |
| WoE | Deferred | Separate Episode gate |
| Transcendent jobs | Excluded | EP09 gate |
| Later-world travel | Excluded | Episode dependency |
| Cash-shop systems | Excluded | Separate commercial policy |
| Custom launch quests | Customized | Owner-authored |

## 5. Content domains

### 5.1 Maps

The exact map inventory must be generated from rAthena map lists, NPC scripts, warp scripts, spawn data, and the three-way asset mapper. Do not infer availability from asset presence alone.

Candidate launch families for owner review:

- Prontera and approved surrounding fields
- Izlude and approved surrounding fields
- Geffen and approved surrounding fields
- Payon and approved surrounding fields
- Morroc and approved surrounding fields
- Alberta and approved surrounding fields
- approved beginner/training maps
- approved early dungeons
- approved indoor service maps

Each map record must contain:

```yaml
mapId: prontera
disposition: included
serverSources: []
warpSources: []
spawnSources: []
assetBundle:
  rsw: null
  gnd: null
  gat: null
  minimap: null
  textures: []
  models: []
  effects: []
  bgm: []
validation:
  serverRegistered: false
  bundleComplete: false
  published: false
  browserRendered: false
  collisionPassed: false
reloadPolicy: map-reentry
```

Map bundle validation requires `.rsw`, `.gnd`, and `.gat` as one atomic dependency group. A map may not be promoted when one member is missing, mismatched, or from a different release.

### 5.2 Warp graph

Every warp is treated as a directed edge:

```yaml
warpId: ep01.prontera.to.prt_fild08
sourceMap: prontera
sourceCell: null
targetMap: prt_fild08
targetCell: null
condition: none
disposition: included
sourceScript: null
validation:
  sourceMapEnabled: false
  targetMapEnabled: false
  targetCellWalkable: false
  returnPathReviewed: false
```

Required checks:

- source and target maps are enabled in the same or earlier Episode;
- target coordinates are walkable;
- no edge bypasses a locked Episode;
- one-way edges are explicitly approved;
- save points and respawn routes cannot trap a player;
- transport NPCs and scripted warps are included in the same graph;
- the graph has no orphan launch map unless explicitly approved.

### 5.3 NPC and services

Minimum service categories:

- start/tutorial guidance;
- Kafra or equivalent storage/save service;
- healer or recovery policy;
- tool, weapon, armor, and consumable shops approved for launch;
- job-change services for enabled jobs;
- transport services;
- guild/party-related services if enabled;
- quest and information NPCs;
- owner-created onboarding and transparency NPCs.

Each NPC must record script source, map, coordinates, sprite asset, dialogue/localization dependency, service permissions, reload policy, and rollback owner.

NPC scripts may use controlled hot reload only after parser validation and staging execution. NPC reload must never be implemented as unrestricted shell or raw AtCommand input from the browser.

### 5.4 Jobs and progression

EP01 may enable Novice and owner-approved first jobs. For each enabled job, validate:

- job-change quest and NPC path;
- skill tree data;
- skill icons and descriptions;
- required weapons/ammunition;
- save/respawn behavior;
- stat and skill reset policy;
- party roles and early progression viability;
- disabled later-job transitions remain inaccessible.

EXP curves, job levels, stat limits, and progression pacing are owner parameters and are not hard-coded into the Episode document.

### 5.5 Monsters and spawns

Every spawn record must identify:

- monster ID and server database source;
- map and spawn region;
- count, delay, and variance;
- aggression and AI profile;
- level/progression band;
- drops and economic role;
- sprite/ACT/palette/sound/effect dependencies;
- MVP or boss classification;
- owner disposition.

Required dependency group:

```text
monster database record
+ spawn record
+ sprite .spr
+ animation .act
+ palette where required
+ hit/death effects
+ name/localization
+ drop references
```

A monster can be staging-only even when its assets exist. Asset existence never activates gameplay content automatically.

### 5.6 Items, drops, shops, and equipment

Each item requires cross-system identity:

```text
rAthena item ID
↔ item database record
↔ icon
↔ collection image
↔ equipment view sprite where applicable
↔ name/description localization
↔ drop/shop/quest references
↔ client data table
```

Validation must detect:

- server item without icon;
- icon without server item;
- equipment without view sprite;
- drop pointing to disabled item;
- shop selling an excluded item;
- duplicate item IDs or logical IDs;
- canonical/published hash mismatch;
- later-Episode item leaking into EP01.

The owner sets availability, prices, drop rates, refine rules, weight, trade restrictions, vending policy, and sink/source behavior.

### 5.7 Quests and access rules

EP01 quests include onboarding, job progression, essential services, and owner-approved early stories. Every quest must declare prerequisites, NPCs, maps, monsters, items, rewards, localization, client indicators, and rollback behavior.

No quest may reference a disabled map, NPC, monster, item, skill, or later Episode without an explicit deferred dependency.

### 5.8 Social systems

Owner-controlled systems may include:

- party creation and sharing rules;
- guild creation;
- guild storage if supported and approved;
- trade;
- vending;
- chat channels;
- ignore/block;
- friend system;
- mail only when supported by the selected compatibility profile.

Each system must have abuse limits, audit events, and economy implications documented.

## 6. Asset control model

### 6.1 Asset categories

EP01 inventory covers:

- map bundles;
- map textures and models;
- minimaps;
- NPC sprites and animations;
- monster sprites and animations;
- player/job sprites and equipment views;
- item icons and collection images;
- effects;
- UI windows, frames, buttons, icons, cursors, fonts, and localization;
- BGM and sound effects;
- Lua/XML/JSON/data tables used by the browser client.

### 6.2 Asset record

```yaml
logicalId: ui.basic.status-window.background
episodeId: EP01
disposition: included
category: UI
legacyPath: null
normalizedPath: null
consumerSources: []
canonical:
  relativePath: null
  exists: false
  size: null
  sha256: null
published:
  relativePath: null
  exists: false
  size: null
  sha256: null
mappingStatus: missing
mappingConfidence: low
dependencies: []
editorCapability: replace-preview
reloadPolicy: hot
releaseId: null
```

### 6.3 Reload policies

Allowed policies:

- `hot`: reload without leaving the current state;
- `ui-reopen`: close and reopen the affected window;
- `entity-respawn`: recreate affected entity instances;
- `map-reentry`: leave and re-enter the map;
- `page-refresh`: refresh the browser client;
- `reconnect`: reconnect the game session;
- `maintenance`: controlled server/client maintenance.

The Workbench must show the highest required policy for a release before promotion.

## 7. UI baseline

EP01 player UI must include or explicitly defer:

- login/launch handoff;
- character selection and creation;
- basic information window;
- HP/SP/EXP/weight/zeny display;
- chat;
- hotbar;
- minimap;
- inventory;
- equipment;
- status and skills;
- party and guild panels when enabled;
- NPC dialogue and shop UI;
- storage and trade UI;
- settings and asset reload status;
- patch notes/server-growth indicator.

UI Manager must identify every UI component, asset dependency, data source, permission, device profile, and reload scope. New dashboard-style UI must use registered APIs/data sources rather than direct browser database access.

## 8. Economy launch controls

EP01 must establish a measurable baseline:

- starting currency policy;
- monster/NPC/quest Zeny sources;
- shop, storage, warp, refine, guild, and service sinks;
- item supply and concentration;
- vending/trade rules;
- bot/farming signals;
- owner target bands for inflation and net injection.

Before launch, produce a simulation and expected 7-day/30-day ranges. After launch, compare actual data to the baseline without automatically punishing players.

## 9. Release waves

Recommended structure:

```text
SP01.0-A  Technical launch and onboarding
SP01.0-B  Core towns and beginner fields
SP01.0-C  First-job progression
SP01.0-D  Early dungeons and economy expansion
SP01.0-E  Social/guild features approved for launch
```

Each wave has its own immutable server content manifest, client asset manifest, validation evidence, approval, activation time, and rollback target.

## 10. Validation gates

EP01 cannot reach `Live` until all applicable gates pass:

- compatibility profile gate;
- server configuration gate;
- map registration gate;
- map bundle gate;
- warp graph gate;
- NPC script parser gate;
- job progression gate;
- monster/spawn gate;
- item cross-reference gate;
- client asset mapping gate;
- canonical/published hash gate;
- UI interaction gate;
- localization gate;
- economy simulation gate;
- security and abuse gate;
- backup gate;
- staging playtest gate;
- browser E2E gate;
- rollback rehearsal gate;
- owner approval gate.

## 11. Browser E2E scenarios

Minimum evidence scenarios:

1. New account launch handoff.
2. Character create/select.
3. Enter approved start map.
4. Walk, collide, rotate/zoom within approved limits.
5. Speak to onboarding NPC.
6. Save and use storage.
7. Buy/sell an approved item.
8. Fight an approved monster and receive an approved drop.
9. Equip an item and verify visual asset.
10. Change map through an approved warp.
11. Form party and exchange chat.
12. Disconnect and reconnect safely.
13. Publish a hot-reloadable UI asset and use Reload Assets.
14. Publish a map-reentry asset and verify policy warning.
15. Roll back the client manifest and verify previous assets.

## 12. Rollback

Rollback never deletes immutable assets or overwrites prior manifests. It changes active pointers to the last approved release.

Rollback package must include:

- previous server content release;
- previous client asset release;
- previous UI schema/theme release;
- database migration reversal or compensating action when applicable;
- cache invalidation instruction;
- player communication template;
- post-rollback verification checklist.

## 13. Evidence directory

Generated evidence remains outside Git when it contains licensed bytes, production data, or machine-local absolute paths. Sanitized summaries may be committed.

Recommended local location:

```text
C:\Ragnarok-Prontera\Generated\server-growth\EP01\
```

Expected reports:

```text
map-inventory.json
warp-graph.json
npc-inventory.json
monster-spawn-inventory.json
item-cross-reference.json
asset-mapping.json
asset-dependency-issues.json
economy-baseline.json
browser-e2e-summary.json
rollback-rehearsal.json
owner-approval.json
```

## 14. Completion definition

EP01 is complete when the owner can use ROWEB Operations Workbench to:

1. see every included, excluded, customized, deferred, and staging-only EP01 component;
2. locate every mapped client asset and its consumers;
3. validate canonical and published files;
4. stage a complete Episode Service Pack;
5. inspect dependency, economy, and reload-policy impact;
6. approve and activate an immutable release;
7. verify the player experience in Modernized roBrowserLegacy;
8. reload supported assets from the browser;
9. audit every administrative action; and
10. execute a tested rollback.

Until these conditions pass, EP01 remains `Building` or `Validating`, not `Live`.