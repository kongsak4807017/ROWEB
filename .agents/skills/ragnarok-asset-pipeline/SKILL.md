---
name: ragnarok-asset-pipeline
description: Use for GRF inspection, CP949 paths, extraction manifests, map/sprite/model/effect/audio conversion, publishing, caching, or missing-asset diagnosis.
version: 1.0.0
owners: [ROWEB]
tags: [ragnarok, assets, grf]
---

# Ragnarok Asset Pipeline

## Hard boundary

No licensed asset bytes may enter Git, test fixtures, logs, reports, or public artifacts. Use approved local roots and synthetic fixtures. Store only code, schemas, hashes, provenance, and non-sensitive reports.

## Workflow

1. Record approved source snapshot, provenance, tool versions, encoding, and destination policy.
2. Inventory paths without modifying source; decode CP949 deterministically and retain raw-name evidence privately.
3. Normalize separators/case safely; reject traversal, absolute paths, ambiguous aliases, collisions, hash mismatch, and unsupported formats.
4. Publish immutable hash-addressed objects plus path/alias manifests and dependency reports.
5. Validate format-specific relationships:
   - RSW/GND/GAT maps and walkability
   - SPR/ACT/PAL frames, directions, anchors, timing
   - RSM/RSM2 models and textures
   - STR/effects and audio/BGM references
6. Test missing, corrupt, duplicate, collision, cache, patch, and rollback scenarios with synthetic data.
7. Verify browser retrieval, cache reuse, changed-file-only patching, and no routing through rAthena/wsProxy.

## Deliverables

Manifest schema, provenance registry, conversion report, missing dependency report, collision report, cache headers, patch/rollback plan, and asset leak scan.