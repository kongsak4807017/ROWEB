# Automatic Asset Delivery and Patching

## 1. Production rule

Players must never upload or select GRF files. Assets are prepared and published by the operator.

```text
approved GRF/data source
→ extraction/build pipeline
→ canonical files + hashes
→ static asset storage/CDN
→ browser cache
```

## 2. Source and publication boundary

Source assets remain outside Git. The publisher reads approved GRF/data sources and produces a deployable static tree or content-addressed objects.

Example source workspace:

```text
C:\Ragnarok-Prontera\assets\data
```

The exact production path is environment configuration, not a hard-coded repository requirement.

## 3. Manifest model

Bootstrap manifest:

```json
{
  "clientBuild": "roweb-2026.07.29.1",
  "assetVersion": "assets-2026.07.29.1",
  "packetProfile": "pre-renewal-pinned",
  "assetManifestUrl": "/manifests/assets-2026.07.29.1.json"
}
```

Asset manifest entry:

```json
{
  "logicalPath": "data/prt_fild08.rsw",
  "sha256": "...",
  "size": 12345,
  "contentUrl": "/objects/ab/cd/<sha256>",
  "contentType": "application/octet-stream"
}
```

Map bundle manifest:

```json
{
  "map": "prt_fild08",
  "required": [
    "data/prt_fild08.rsw",
    "data/prt_fild08.gnd",
    "data/prt_fild08.gat"
  ],
  "dependencies": [
    "data/model/...",
    "data/texture/..."
  ],
  "optional": [
    "data/wav/...",
    "data/texture/.../minimap/..."
  ]
}
```

## 4. Cache policy

Content-addressed assets:

```text
Cache-Control: public, max-age=31536000, immutable
```

Bootstrap and live manifests:

```text
Cache-Control: no-cache
ETag: enabled
```

The browser compares hashes and downloads only missing or changed content.

## 5. Browser storage

Use layered caching:

1. HTTP cache for immutable URLs
2. Cache Storage for application-controlled fetches
3. IndexedDB only where binary lookup or metadata indexing materially helps

Do not duplicate every asset into multiple stores without a measured need.

## 6. Loading strategy

### Bootstrap/common

Preload only what is needed for login, character select, common UI, and the current character appearance.

### Map entry

Preload the dependency closure for the destination map before transitioning.

### Entities

Lazy-load monster, NPC, equipment, and effect assets on first reference, then cache them.

### Predictive prefetch

Prefetch adjacent warp destinations only after the current map is stable and within a bandwidth/memory budget.

## 7. Patch workflow

```text
change custom data/GRF
→ run publisher
→ scan and normalize paths
→ hash changed files
→ publish immutable objects
→ create new manifests
→ validate dependency closures
→ promote assetVersion
```

Rollback is performed by repointing the bootstrap manifest to the previous known-good asset version.

## 8. Production serving

Prefer static serving from Nginx/object storage/CDN. Runtime GRF extraction is acceptable for development or controlled fallback, not the default production path.

The production server must:

- normalize path separators and case policy
- reject traversal (`..`)
- allow only published manifest entries
- disable directory listing
- set explicit content types
- support range requests where useful
- provide access logs and metrics

## 9. Verification gates

A patch cannot be promoted unless:

- every manifest hash matches content
- required map dependencies resolve
- no path is ambiguous after normalization
- `prt_fild08` clean-cache load passes
- warm-cache reload passes
- unchanged assets are not downloaded again
- rollback to the previous manifest succeeds
- no licensed bytes entered Git history

## 10. First implementation slice

Build the publisher and delivery path for only:

- bootstrap/common client files
- one player appearance set required for the test account
- `prt_fild08` dependency closure
- Poring
- one NPC

Expand only after the clean-cache and patch-delta tests pass.