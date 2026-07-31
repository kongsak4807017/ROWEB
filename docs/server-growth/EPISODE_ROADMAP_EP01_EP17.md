# ROWEB Server Growth Roadmap — EP01 to EP17

## Purpose

This roadmap defines the **content-growth axis** of the ROWEB server. It is separate from the Admin Studio platform-maturity roadmap (M0–M6).

- **M0–M6** = maturity of control, safety, APIs, editors, audit, deployment and production operations.
- **EP01–EP17** = staged growth of playable game content delivered as controlled Episode Service Packs.

The server owner retains authority over detailed EXP, drop, spawn, item, NPC, quest, economy and schedule settings inside each Episode.

## Operating Model

Each Episode is packaged as an immutable, versioned Service Pack containing coordinated server content and client assets.

```text
Episode
└── Service Pack
    ├── Maps and map groups
    ├── Warp/access graph
    ├── NPC/script packs
    ├── Monster/spawn packs
    ├── Item/drop/shop packs
    ├── Quest/story packs
    ├── Classes/skills/systems
    ├── Client assets and UI
    ├── Localization/navigation
    ├── Economy policy
    ├── Reload policy
    ├── Validation evidence
    └── Rollback manifest
```

Episode lifecycle:

```text
Planned → Building → Validating → Staging → Scheduled → Live → Superseded
                                                       ↘ Rolled Back
```

## Episode Roadmap

| Episode | Direction of growth | Major content focus | Default activation model |
|---|---|---|---|
| EP01 | Start of Adventure | Core towns, first jobs, foundational fields/dungeons, Kafra, party/guild basics | Launch baseline |
| EP02 | Lutie | Snow town, Toy Factory, seasonal framework | Additive pack |
| EP03 | Comodo | Comodo region, beach/cave content, new routes and items | Additive pack |
| EP04 | WoE and Turtle Island | Guild competition, castles, guild dungeons, Turtle Island | Scheduled/feature-gated |
| EP05 | Yuno | Yuno/Juno, Magma content, world transport and expanded lore | Additive pack |
| EP06 | Beyond Midgard | Amatsu, Kunlun/Gonryun, Louyang, Ayothaya and regional packs | Modular sub-packs |
| EP07 | Umbala | Umbala region, tribal content, progression route to Nifflheim | Dependency pack |
| EP08 | Nifflheim | Realm of the Dead, quests, monsters, equipment progression | Requires EP07 |
| EP09 | Rebirth | Transcendent progression, skills, EXP and endgame reset loop | Migration pack |
| EP10 | Schwarzwald | Einbroch, Lighthalzen, Noghalt, Hugel and high-level systems | Multi-wave pack |
| EP11 | Arunafeltz | Rachel, Veins, Thor Volcano, Nameless Island | Multi-wave pack |
| EP12 | Satan Morroc | World-state change, Dimensional Gorge, major competitive/endgame systems | World mutation |
| EP13 | New World | Ash Vacuum, Manuk/Splendide, El Dicastes and faction progression | Multi-wave pack |
| EP14 | Bifrost and Eclage | Mora, Bifrost, Eclage and decisive-battle progression | Multi-wave pack |
| EP15 | Phantasmagorika | Verus, laboratories, industrial/story instances | Multi-wave pack |
| EP16 | Royal Banquet | Royal Banquet and Terra Gloria political/story progression | Multi-wave pack |
| EP17 | Illusion and Wise One | Rudus/Cor/Varmundt-era content and later progression | Multi-wave pack |

## Recommended Sub-Pack Structure

Large Episodes must be divisible into Service Packs and release waves.

```text
EP10
├── SP10.1 Einbroch
├── SP10.2 Lighthalzen
├── SP10.3 Noghalt
└── SP10.4 Hugel
```

Every feature inside a pack has one owner-controlled disposition:

- `included`
- `excluded`
- `customized`
- `deferred`
- `staging-only`
- `scheduled-later`

## Episode Control Page

ROWeb Operations Workbench must provide:

- current Episode and active Service Pack;
- next planned Episode;
- readiness percentage;
- validated map, warp, NPC, monster, item, quest and asset counts;
- unresolved dependencies;
- economy-impact assessment;
- reload/restart requirements;
- staging test evidence;
- backup and rollback readiness;
- owner approval and schedule;
- live monitoring after activation.

## Promotion Gate

No Episode may become Live until all required gates pass:

```text
Content schema validation       PASS
Map bundle validation           PASS
Warp graph validation           PASS
NPC/script validation           PASS
Item/monster/drop references    PASS
Client asset manifest           PASS
Localization/navigation         PASS
Economy review                  PASS
Staging playtest                PASS
Backup                          PASS
Rollback rehearsal              PASS
Owner approval                  PASS
```

## Reload Policy

Each changed unit declares one of:

- `hot`: safe runtime reload;
- `controlled-reload`: server subsystem reload through typed command bus;
- `map-reentry`: players must leave/re-enter affected maps;
- `page-refresh`: browser client refresh required;
- `maintenance`: maintenance window required;
- `restart-required`: process restart required.

## Rollback Model

Rollback changes active release pointers and restores server content from a validated previous pack. It must not delete immutable asset objects or overwrite historical manifests.

Each Episode must retain:

- previous live Episode pointer;
- database/content backup reference;
- previous client manifest;
- rollback command plan;
- post-rollback validation checklist;
- audit correlation ID.

## Documentation Plan

Detailed specifications will be created under:

```text
docs/server-growth/episodes/
├── EP01_START_OF_ADVENTURE.md
├── EP02_LUTIE.md
├── EP03_COMODO.md
├── EP04_WOE_TURTLE_ISLAND.md
├── EP05_YUNO.md
├── EP06_BEYOND_MIDGARD.md
├── EP07_UMBALA.md
├── EP08_NIFFLHEIM.md
├── EP09_REBIRTH.md
├── EP10_SCHWARTZWALD.md
├── EP11_ARUNAFELTZ.md
├── EP12_SATAN_MORROC.md
├── EP13_NEW_WORLD.md
├── EP14_BIFROST_ECLAGE.md
├── EP15_PHANTASMAGORIKA.md
├── EP16_ROYAL_BANQUET.md
└── EP17_ILLUSION_WISE_ONE.md
```

Each detailed Episode specification must inventory maps, map bundles, warps, NPCs, monsters, spawns, items, drops, shops, quests, skills/classes, client assets, UI, localization, dependencies, economy controls, reload policy, validation, staging tests and rollback.