# ADR-023: Engine-neutral asset catalog

- Status: Accepted
- Date: 2026-08-01

## Context

The current asset pipeline serves roBrowser runtime paths, but future clients must reuse identity, provenance, dependencies, and publishing evidence without inheriting roBrowser-specific storage assumptions.

## Decision

Asset IDs, source metadata, hashes, provenance, and dependency relationships are engine-neutral. Target-specific mappings are isolated under `targets.robrowser` and `targets.unity`. The Unity target may remain unimplemented while its schema boundary is preserved.

## Alternatives considered

- Use roBrowser paths as global asset identity: rejected because runtime paths are not stable cross-engine identifiers.
- Build a separate future Unity catalog: rejected because it would duplicate scanning, provenance, and content governance.

## Consequences

- Current tools must emit stable asset IDs separately from target paths.
- Validation can reject catalogs that omit required roBrowser mappings while Unity is still planned.
- Future Unity conversion and Addressables metadata can be added without changing source identity.

## Reversal conditions

The catalog model may be replaced only after migration tooling proves that all identities, hashes, provenance, dependencies, and target mappings can be preserved without ambiguity.

## Evidence

- Approved design: `docs/superpowers/specs/2026-08-01-roweb-long-term-handoff-design.md`
- Asset policy: `docs/ASSET_DELIVERY_AND_PATCHING.md`

## Owner

ROWEB repository owner and maintainers.
