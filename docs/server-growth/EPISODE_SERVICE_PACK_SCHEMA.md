# Episode Service Pack Schema

## Purpose

This document defines the canonical data contract used by ROWEB Operations Workbench to build, validate, stage, release and roll back Episode content.

## Canonical Manifest

```yaml
episodeId: EP05
servicePackId: SP05.1
name: Yuno - Forgotten Legacy
version: 1.0.0
status: planned
environment: staging
requires:
  episodes: [EP01, EP02, EP03, EP04]
  servicePacks: []
ownerControls:
  expPolicy: customized
  dropPolicy: customized
  spawnPolicy: customized
  economyPolicy: customized
content:
  maps: []
  mapBundles: []
  warps: []
  npcs: []
  scripts: []
  monsters: []
  spawns: []
  items: []
  drops: []
  shops: []
  quests: []
  skills: []
  classes: []
  systems: []
client:
  assetManifest: manifests/assets/ep05-sp05-1.json
  uiSchemas: []
  navigation: []
  localization: []
validation:
  requiredChecks: []
  evidence: []
release:
  reloadPolicies: {}
  maintenanceRequired: false
  previousRelease: null
  rollbackTarget: null
approval:
  owner: pending
  content: pending
  technical: pending
```

## Required Content Records

Every record must include:

- stable logical ID;
- Episode and Service Pack ownership;
- source path or database identity;
- runtime/published identity;
- dependency list;
- activation disposition;
- reload policy;
- validation status;
- provenance note;
- owner override status;
- version and content hash where applicable.

## Map Bundle Rule

A Ragnarok map is never treated as a single file. A map bundle records at minimum:

```yaml
logicalId: map.yuno.bundle
files:
  rsw: data/yuno.rsw
  gnd: data/yuno.gnd
  gat: data/yuno.gat
optional:
  minimap: data/texture/map/yuno.bmp
  models: []
  textures: []
  effects: []
reloadPolicy: maintenance
```

The validator must report missing `.rsw`, `.gnd` or `.gat` members as an incomplete map bundle.

## Entity Bundle Rule

Sprites and animations are paired:

```yaml
logicalId: entity.monster.example
files:
  sprite: data/sprite/monster/example.spr
  animation: data/sprite/monster/example.act
optional:
  palette: null
  sounds: []
reloadPolicy: map-reentry
```

## Warp and Access Graph

Every warp record declares:

- source map and coordinates;
- destination map and coordinates;
- access condition;
- required quest/flag/item;
- Episode dependency;
- enabled environments;
- fallback or closure behavior.

The graph validator must detect missing destination maps, dead ends, unintended early access and circular access requirements.

## Activation Disposition

Each content unit uses one value:

```text
included
excluded
customized
deferred
staging-only
scheduled-later
```

No unspecified content may be activated automatically.

## Validation Result

```json
{
  "checkId": "warp.destination.exists",
  "target": "warp.ep05.prontera-yuno",
  "result": "pass",
  "severity": "error",
  "evidence": "map.yuno.bundle validated",
  "correlationId": "..."
}
```

## Release Contract

Promotion to Live must:

1. freeze the validated manifest;
2. create database/content backup references;
3. publish immutable client assets;
4. update server content through approved adapters;
5. update client manifest pointer;
6. run post-release health checks;
7. record one correlation ID across all operations;
8. retain a tested rollback target.

## Safety Boundary

The Episode system must not expose unrestricted SQL, shell commands or raw AtCommands. Server changes are performed only through typed, allowlisted adapters with RBAC, approval, audit and environment restrictions.