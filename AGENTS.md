# AGENTS.md — ROWEB Operating Contract

This file is the highest-priority repository-local operating contract for AI agents and developers.

## 1. Product direction

ROWEB uses **roBrowserLegacy as the primary browser client runtime** and **rAthena as the authoritative game server**.

Do not restart a Unity-first rewrite of Ragnarok rendering, map loading, entity behavior, or packet semantics unless an explicit architecture decision approves it.

## 2. Read before work

Before changing code or documentation, read:

1. `README.md`
2. `docs/ARCHITECTURE.md`
3. `docs/ROADMAP.md`
4. `docs/IMPLEMENTATION_PLAYBOOK.md`
5. `docs/SECURITY_AND_IP_BOUNDARY.md`
6. `.agents/skills/roweb-skill-router/SKILL.md`, then every domain skill selected by the router
7. Any deeper `AGENTS.md` in the directory being modified

The canonical skill catalog is `.agents/skills/README.md`; machine-readable discovery is available in `.agents/skills/registry.json`.

## 3. Source of truth

Precedence for behavior:

1. Pinned roBrowserLegacy source and verified runtime behavior
2. Pinned rAthena source/configuration and protocol behavior
3. Exact client data/Lua/Lub tables from the approved asset snapshot
4. Automated tests and captured golden evidence
5. Documentation and community references
6. Assumptions

Never replace verified behavior with a guess.

## 4. Asset boundary

Never commit or push:

- GRF archives
- extracted Ragnarok assets
- RSW/GND/GAT/RSM/RSM2/SPR/ACT/PAL/STR files
- textures, sprites, audio, minimaps, or licensed artwork
- database dumps containing licensed asset payloads

Allowed in Git:

- source code
- configuration templates without secrets
- schemas
- manifests without asset bytes
- hashes
- provenance
- tests with synthetic fixtures
- reports and screenshots only when legally approved

## 5. Runtime boundaries

- Asset requests use HTTPS to a static asset server/CDN.
- Gameplay packets use WSS through wsProxy to rAthena.
- Asset traffic must not traverse wsProxy or rAthena.
- rAthena remains authoritative for gameplay and persistence.
- Browser UI must not fabricate gameplay state.
- Production must not ask players to upload GRFs.

## 6. Change discipline

Every implementation change must include:

- scope and affected contract
- tests or machine-readable verification
- failure behavior
- rollback notes where operationally relevant
- no licensed asset leakage

Do not mark work complete from code inspection alone. Run the relevant build, test, smoke, and integration checks.

## 7. Milestone discipline

Work vertically. The first production slice is:

```text
clean browser
→ bootstrap
→ automatic assets
→ WSS login
→ character select
→ prt_fild08
→ correct map/entities
→ cache reuse
```

Do not expand to many maps or systems while this slice is unstable.

## 8. Capacity claims

Do not claim 5,000 CCU support without load-test evidence. Capacity approval requires:

- realistic simulated behavior
- hotspot scenarios
- sustained test duration
- p95/p99 latency
- CPU/memory/DB/gateway metrics
- failure and recovery tests
- documented hardware and configuration

## 9. Preferred delivery flow

Use a branch and pull request for substantive implementation. Documentation bootstrap may be committed directly when explicitly authorized by the repository owner.

## 10. Definition of done

A task is done only when:

- acceptance criteria pass
- tests and build pass
- relevant runtime path was exercised
- documentation reflects the result
- no secret or licensed asset was introduced
- evidence is linked or stored in an approved form