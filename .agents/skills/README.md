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

## Skill catalog

### Routing and skill engineering

- `roweb-skill-router`
- `roweb-skill-author`
- `roweb-repository-orientation`
- `roweb-verification-gate`

### Architecture and server

- `roweb-system-architecture`
- `rathena-server-engineering`
- `rathena-npc-script-engineering`
- `rathena-skill-system-engineering`
- `rathena-packet-protocol`
- `rathena-database-migrations`

### Browser client and gateway

- `robrowser-client-engineering`
- `roweb-wss-gateway`
- `roweb-ui-ux`
- `browser-performance-and-cache`

### Asset pipeline

- `ragnarok-grf-asset-pipeline`
- `ragnarok-map-pipeline`
- `ragnarok-sprite-act-pipeline`
- `ragnarok-model-effect-audio-pipeline`
- `asset-license-boundary`

### Game systems

- `mmorpg-game-design`
- `mmorpg-combat-and-progression`
- `mmorpg-economy-balancing`
- `mmorpg-content-pipeline`
- `mmorpg-social-systems`

### Quality, security, and operations

- `protocol-conformance-testing`
- `gameplay-e2e-testing`
- `mmorpg-load-testing`
- `mmorpg-security`
- `roweb-observability`
- `roweb-production-deployment`
- `roweb-liveops-and-incident-response`

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

See `SKILL_AUTHORING_STANDARD.md` and `templates/SKILL.template.md`.