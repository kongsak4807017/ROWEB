# EP01 Discovery and Asset-Control Plan

## Goal

Produce an evidence-backed EP01 inventory from the pinned local rAthena, Modernized roBrowserLegacy source, canonical extracted assets, and published runtime asset tree. The result becomes the first real Episode Service Pack managed by ROWEB Operations Workbench.

## Inputs

```text
ROWEB repository
C:\Ragnarok-Prontera\HermesWorkSpace\ROWEB

roBrowserLegacy source
C:\Ragnarok-Prontera\HermesWorkSpace\roBrowserLegacy

rAthena source/runtime configuration
C:\Ragnarok-Prontera\rathena

Canonical extracted assets
C:\Ragnarok-Prontera\assets\data

Published runtime assets
C:\Ragnarok-Prontera\HermesWorkSpace\roBrowserLegacy\roBrowserLegacy-RemoteClient-PHP\data
```

All external inputs are read-only. Generated evidence goes under:

```text
C:\Ragnarok-Prontera\Generated\server-growth\EP01
```

## Work packages

### EP01-D1 — Server content discovery

Discover and normalize:

- registered maps;
- map-cache/map-list inputs;
- warp NPCs and scripted transports;
- NPC scripts and coordinates;
- monster database records;
- map spawn records;
- item database records;
- drops, shops, rewards, and quest references;
- enabled jobs and skill data;
- relevant battle/config settings.

Output sanitized identifiers and source-relative paths, never secrets or database credentials.

### EP01-D2 — Client consumer discovery

Scan Modernized roBrowserLegacy for:

- map asset loads;
- sprite/ACT loads;
- item icons and collection images;
- equipment view sprites;
- model/effect/texture references;
- BGM and sound references;
- UI assets;
- localization and data tables;
- runtime fallback and alias behavior.

Record exact consumer files and line references when practical.

### EP01-D3 — Three-way asset matching

For each normalized legacy path compare:

1. source reference;
2. canonical extracted asset;
3. published runtime asset.

Classify as:

- matched;
- canonical-only;
- published-only;
- missing;
- case-mismatch;
- encoding-alias;
- duplicate;
- collision;
- hash-mismatch.

### EP01-D4 — Dependency graph

Build atomic groups:

- `.rsw + .gnd + .gat`;
- `.spr + .act`;
- item record + icon + collection image + equipment view;
- model/effect + referenced textures;
- NPC + sprite + localization + script;
- map + warps + spawns + BGM + minimap.

A dependency group is promoted together or not at all.

### EP01-D5 — Owner disposition review

Workbench presents each discovered record for owner classification:

- included;
- excluded;
- customized;
- deferred;
- staging-only;
- admin-only.

Bulk rules may suggest classifications, but activation always requires explicit manifest state and owner approval.

### EP01-D6 — Editor capability registry

Assign one capability to each asset type:

- metadata-only;
- replace-preview;
- image-editor;
- UI-layout-editor;
- sprite-ACT-editor;
- map-editor;
- effect-editor;
- model-viewer/editor;
- audio-editor;
- structured-data-editor.

The registry also defines validation and reload policy.

### EP01-D7 — Release construction

Generate:

- server-content manifest;
- client-asset manifest;
- UI/theme manifest;
- dependency report;
- reload impact report;
- economy baseline;
- rollback manifest.

The release uses immutable object versions and environment pointers.

### EP01-D8 — Staging verification

Run focused validation and browser E2E. Capture evidence for:

- login-to-map;
- core map rendering;
- warp graph;
- NPC services;
- first-job progression;
- combat/drop/equipment;
- storage/trade/party;
- hot asset reload;
- map-reentry policy;
- manifest rollback.

## Workbench pages required

```text
Server Growth
├── Episode Overview
├── EP01 Content Inventory
├── Map & Warp Graph
├── NPC & Script Inventory
├── Monster & Spawn Inventory
├── Item/Drop/Shop Cross-reference
├── Asset Control
├── UI and Reload Policies
├── Economy Baseline
├── Validation Evidence
├── Release Waves
└── Rollback
```

## Data contracts

### Episode content record

```json
{
  "episodeId": "EP01",
  "domain": "map",
  "recordId": "prontera",
  "disposition": "included",
  "sourceRefs": [],
  "dependencies": [],
  "validationState": "pending",
  "releaseWave": "SP01.0-B"
}
```

### Asset control record

```json
{
  "logicalId": "map.prontera.geometry.rsw",
  "episodeId": "EP01",
  "legacyPath": "data/prontera.rsw",
  "consumerSources": [],
  "canonical": {"exists": false, "sha256": null},
  "published": {"exists": false, "sha256": null},
  "mappingStatus": "missing",
  "editorCapability": "map-editor",
  "reloadPolicy": "map-reentry",
  "releaseWave": "SP01.0-B"
}
```

## Safety gates

- No asset bytes in Git.
- No direct mutation of rAthena or external asset roots during discovery.
- No unrestricted SQL, shell, or AtCommand execution.
- No production command execution before M3 Safe Typed Command Bus.
- No Episode activation without backup and rollback evidence.
- No browser database connection; dashboards use registered APIs/data sources.
- No symlink/junction traversal outside approved roots.

## Definition of done

This plan is complete when EP01 has a reproducible inventory, explicit owner dispositions, complete dependency graph, validated asset mappings, release-wave manifests, browser E2E evidence, economy baseline, and tested rollback—visible from the unified Workbench.