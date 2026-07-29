# Architecture Decision Log

## ADR-001 — Use roBrowserLegacy as the primary client runtime

**Status:** Accepted  
**Date:** 2026-07-29

### Context

The Unity WebGL client lane required ROWEB to independently recreate Ragnarok-specific map parsing, model placement, coordinate transforms, SPR/ACT behavior, entity action profiles, camera-relative directions, equipment composition, packet semantics, and asset lookup.

The resulting runtime showed incorrect map/model/entity behavior and imposed a high reverse-engineering and verification burden.

roBrowserLegacy already implements the relevant browser-side Ragnarok behavior, including:

- RSW/GND/GAT loading
- RSM model instances and transforms
- SPR/ACT entity rendering
- player/monster/NPC action profiles
- weapon-dependent attack actions
- camera-relative sprite direction
- WebSocket-to-rAthena integration

### Decision

ROWEB will use roBrowserLegacy as its primary client runtime and invest in:

- modern DOM UI/UX
- automatic server-managed asset delivery
- browser caching and patching
- mobile support
- production security and deployment
- rAthena/wsProxy/database scaling and observability

Unity WebGL becomes an optional R&D/reference lane rather than the critical production path.

### Consequences

Positive:

- faster path to a faithful playable browser client
- lower behavioral risk
- existing map/entity/network implementation can be tested and improved rather than recreated
- engineering effort shifts to product UX, delivery, operations, and capacity

Trade-offs:

- legacy code and coupling require controlled modernization
- upstream provenance and changes must be managed
- tests are needed before refactoring high-knowledge runtime code
- runtime parsing remains part of the client unless selectively optimized later

### Guardrail

Do not rewrite stable map/entity behavior without:

1. a demonstrated defect or measurable limitation
2. a golden test or behavioral oracle
3. an incremental replacement plan
4. a rollback path

---

## ADR-002 — Pre-extract and statically publish assets

**Status:** Accepted  
**Date:** 2026-07-29

### Decision

Production users will not upload GRFs. Approved assets will be extracted/published by the operator and delivered through HTTPS using hashes, manifests, immutable caching, and map dependency closures.

Runtime GRF extraction remains a development or fallback tool only.

### Consequences

- faster repeat visits and patch deltas
- scalable CDN/static delivery
- simpler browser UX
- requires an asset build/publish pipeline and clear distribution rights

---

## ADR-003 — Keep gameplay authoritative in rAthena

**Status:** Accepted  
**Date:** 2026-07-29

### Decision

rAthena remains authoritative for gameplay, account/character state, economy, NPCs, monsters, skills, combat, and persistence. The browser performs presentation, input, caching, and interpolation only.

---

## ADR-004 — Treat 5,000 CCU as an evidence-gated target

**Status:** Accepted  
**Date:** 2026-07-29

### Decision

No release or documentation may claim 5,000 concurrent-player support until realistic staged load, hotspot, soak, and recovery tests pass on documented infrastructure and configuration.
