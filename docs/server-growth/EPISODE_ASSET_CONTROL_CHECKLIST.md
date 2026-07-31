# Episode Asset Control Checklist

## Purpose

This checklist is mandatory for every EP01–EP17 detailed specification. It connects roBrowserLegacy source references, canonical extracted assets, published runtime assets and Episode ownership.

## Three-Way Roots

```text
Consumer source root
C:\Ragnarok-Prontera\HermesWorkSpace\roBrowserLegacy

Canonical extracted asset root
C:\Ragnarok-Prontera\assets\data

Published runtime asset root
C:\Ragnarok-Prontera\HermesWorkSpace\roBrowserLegacy\roBrowserLegacy-RemoteClient-PHP\data
```

These external roots are read-only. Generated metadata and reports belong under `ROWEB/artifacts` and must not contain committed licensed asset bytes.

## Required Inventory Per Episode

### Maps

- map logical ID;
- `.rsw/.gnd/.gat` bundle status;
- minimap image;
- model and texture dependencies;
- walkability/collision evidence;
- client load test;
- server map registration;
- Episode access state;
- reload policy.

### Warps and Navigation

- source and destination coordinates;
- destination map availability;
- NPC/quest/item requirements;
- world-map/navigation entry;
- unintended early-access test;
- closure behavior before activation.

### UI and Interface Assets

- window/background images;
- buttons/icons/cursors;
- layout/CSS/UI schema consumers;
- Desktop and Mobile profiles;
- localization strings;
- hot-reload scope;
- fallback asset;
- browser cache version.

### Entities

- `.spr/.act` pair;
- palette;
- directional frames;
- animation timing;
- sounds/effects;
- monster/NPC/job database identity;
- spawn or script consumers;
- map-reentry requirements.

### Items

- item database identity;
- icon and collection image;
- description/localization;
- drop/shop/quest references;
- storage/trade/economy policy;
- client-data compatibility;
- controlled reload evidence.

### Effects, Models and Textures

- effect logical ID;
- model and texture graph;
- alpha/blend/material behavior;
- renderer compatibility;
- missing dependency report;
- preview evidence;
- hot/map-reentry/page-refresh policy.

### Audio

- BGM and sound logical IDs;
- map/NPC/effect consumers;
- codec/browser compatibility;
- volume/loop metadata;
- fallback behavior;
- hot-reload evidence.

### Data and Scripts

- JSON/XML/Lua/YAML/script identity;
- schema validation;
- source-to-runtime mapping;
- server/client ownership;
- unsafe command scan;
- reload adapter;
- rollback artifact.

## Mapping Statuses

Every asset record must use one primary status:

- `matched`
- `canonical-only`
- `published-only`
- `missing`
- `case-mismatch`
- `encoding-alias`
- `duplicate`
- `collision`
- `hash-mismatch`
- `unreferenced-published`
- `dependency-incomplete`

## Required Asset Record

```json
{
  "episodeId": "EP05",
  "servicePackId": "SP05.1",
  "logicalId": "map.yuno.minimap",
  "category": "Map",
  "originalReference": "data/texture/map/yuno.bmp",
  "normalizedPath": "data/texture/map/yuno.bmp",
  "consumers": ["src/..."],
  "canonicalExists": true,
  "publishedExists": true,
  "canonicalHash": "sha256:...",
  "publishedHash": "sha256:...",
  "mappingStatus": "matched",
  "reloadPolicy": "hot",
  "activationDisposition": "included",
  "validationStatus": "pass"
}
```

## Full Editor Classification

Each asset type declares its supported editing mode:

- `metadata-only`
- `replace-and-preview`
- `visual-editor`
- `specialized-editor-required`
- `external-tool-roundtrip`

Initial Workbench scope may provide replacement, preview, dependency validation, versioning, release and rollback before a specialized visual editor exists.

## Player Reload Contract

Every released asset declares:

- reload policy;
- affected module/scope;
- cache key/version;
- disposal procedure;
- re-render/rebind procedure;
- player-visible instruction;
- fallback on reload failure.

Workbench must summarize a release as:

```text
Hot reload: N
Map re-entry: N
Page refresh: N
Maintenance/restart: N
```

## Episode Completion Evidence

An Episode asset pack is complete only when:

- all included records are mapped;
- no unresolved required collision remains;
- required dependencies are complete;
- canonical and published differences are approved;
- all changed assets have versions and hashes;
- client preview/load tests pass;
- reload policies are proven in staging;
- previous release can be restored;
- licensed asset bytes remain outside Git;
- Owner approval is recorded.