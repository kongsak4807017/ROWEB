# ROWEB MMORPG AI Skill Pack

This directory is the canonical, vendor-neutral skill source for AI agents working on ROWEB.

## Mandatory reading order

1. `/AGENTS.md`
2. `/README.md`
3. `/.agents/skills/roweb-skill-router/SKILL.md`
4. The selected domain skill
5. Any deeper `AGENTS.md` in the modified directory

## Core rules

- roBrowserLegacy is the primary browser runtime.
- rAthena is authoritative for gameplay and persistence.
- Never commit licensed Ragnarok asset bytes.
- Never guess PACKETVER, packet semantics, file formats, or runtime behavior.
- Prefer pinned source, captured evidence, tests, and synthetic fixtures.
- Do not claim 5,000 CCU without evidence from realistic sustained load tests.
- Every implementation must define acceptance evidence and rollback behavior.

## Implemented skill catalog

### Routing and skill engineering

- `roweb-skill-router` — mandatory task routing and stop conditions
- `roweb-skill-author` — lets agents create and improve further ROWEB skills
- `roweb-repository-orientation` — repository, branch, contract, and dependency discovery
- `roweb-verification-gate` — evidence gate before completion claims

### Architecture and runtime

- `roweb-system-architecture` — component boundaries, authority, data flow, ADRs
- `rathena-server-engineering` — server source/config/scripts/content/database behavior
- `rathena-packet-protocol` — PACKETVER, handshake, framing, fixtures, compatibility
- `robrowser-client-engineering` — browser runtime, rendering, input, entities, UI integration
- `roweb-wss-gateway` — WSS/TCP bridge, session handoff, backpressure, reconnect

### Assets and gameplay

- `ragnarok-asset-pipeline` — GRF/path/CP949/map/sprite/model/effect/audio publishing
- `mmorpg-game-systems` — game loop, combat, progression, economy, content, social systems

### Quality, security, and operations

- `roweb-testing` — unit, contract, integration, browser E2E, visual and accessibility testing
- `mmorpg-load-testing` — realistic CCU, hotspot, soak, fault and capacity evidence
- `mmorpg-security` — authentication, abuse, duplication, injection and threat modeling
- `roweb-operations` — observability, deployment, backup, rollback, liveops and incidents

Broad skills intentionally contain domain checklists and may be split by `roweb-skill-author` when a workflow becomes independently complex. This avoids dozens of overlapping low-quality prompts while keeping every major MMORPG engineering area covered.

## Portability

`.agents/skills` is canonical. Agent-specific mirrors may be generated into `.claude/skills`, `.github/skills`, `.codex/skills`, or editor rule directories, but generated mirrors must not be edited manually.

## Definition of a usable skill

A skill is not only prose. It must define:

- trigger conditions
- required context
- non-negotiable constraints
- ordered workflow
- expected deliverables
- validation commands or evidence
- failure and rollback behavior
- handoff format

See `SKILL_AUTHORING_STANDARD.md`, `registry.json`, and `templates/SKILL.template.md`.