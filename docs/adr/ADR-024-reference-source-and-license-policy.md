# ADR-024: Reference-source and license policy

- Status: Accepted
- Date: 2026-08-01

## Context

ROWEB studies UnityRO and RagnarokRebuildTcp for protocol, rendering, asset-pipeline, and architecture evidence. Their licenses, age, server assumptions, and production suitability differ from ROWEB.

## Decision

UnityRO and RagnarokRebuildTcp are pinned research sources, not production dependencies by default. Reusing code requires an explicit license review, provenance record, architectural fit assessment, and approval. Concepts and observed behavior may inform clean ROWEB implementations when legally and technically appropriate.

## Alternatives considered

- Copy reference implementations directly into ROWEB: rejected because it creates license, maintenance, and architecture coupling.
- Ignore the projects entirely: rejected because they contain valuable evidence and reduce research risk.

## Consequences

- A machine-readable source registry records exact refs, roles, licenses, allowed use, and prohibited use.
- Research conclusions must cite the pinned source version.
- Production code must not silently acquire AGPL or unknown-license obligations.

## Reversal conditions

A reference may become an approved dependency only after documented legal review, technical review, security review, and a new architecture decision.

## Evidence

- Approved design: `docs/superpowers/specs/2026-08-01-roweb-long-term-handoff-design.md`
- Security and IP boundary: `docs/SECURITY_AND_IP_BOUNDARY.md`

## Owner

ROWEB repository owner and maintainers.
