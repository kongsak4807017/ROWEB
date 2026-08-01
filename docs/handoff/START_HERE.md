# ROWEB Handoff — Start Here

This is the first document for a developer or AI agent taking over ROWEB.

## Product direction

- Finish the modernized `roBrowserLegacy` production client first.
- Keep optimized `rAthena` authoritative for gameplay and persistence.
- Do not begin Unity runtime implementation until the accepted Unity start gate passes.
- Treat UnityRO and RagnarokRebuildTcp as pinned research references, not production dependencies.

Read these files before changing code:

1. `README.md`
2. `AGENTS.md`
3. `compatibility.lock.json`
4. `research/source-registry.yaml`
5. `docs/superpowers/specs/2026-08-01-roweb-long-term-handoff-design.md`
6. `docs/superpowers/plans/2026-08-01-roweb-handoff-foundation.md`
7. `docs/adr/ADR-020-client-product-strategy.md`
8. `docs/adr/ADR-021-rathena-authority.md`
9. `docs/adr/ADR-022-dual-client-contract-boundary.md`
10. `docs/adr/ADR-023-engine-neutral-asset-catalog.md`
11. `docs/adr/ADR-024-reference-source-and-license-policy.md`
12. `docs/adr/ADR-025-unity-start-gate.md`

## Authoritative repositories

| Role | Repository |
|---|---|
| Integration, contracts, portal, tools, documentation | `kongsak4807017/ROWEB` |
| Production browser runtime | `kongsak4807017/roBrowserLegacy` |
| Authoritative game server | `kongsak4807017/rathena` |
| Unity/Athena research reference | `kongsak4807017/unityro` |
| Modern Unity pipeline research reference | `kongsak4807017/RagnarokRebuildTcp` |

Exact accepted refs are recorded in `compatibility.lock.json` and `research/source-registry.yaml`. Do not silently update a source pin.

## Canonical Windows workspace

The current workspace convention is:

```text
C:\RO-WEB-V1\
├── ROWEB\
├── roBrowserLegacy\
├── rathena\
├── private-assets\data\
├── BGM\
└── runtime\
```

`ROWEB\vendor\roBrowserLegacy` and `ROWEB\vendor\rathena` may be directory junctions to the sibling repositories. Licensed assets, BGM, logs, caches, builds, database dumps, and runtime output remain outside Git.

The older paths still present in `compatibility.lock.json` are historical baseline metadata and must be reconciled through a reviewed compatibility-lock update rather than edited casually.

## Bootstrap the handoff checks

From the ROWEB repository root:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-handoff.txt
python -m tools.validation.validate_handoff
python -m pytest tests/contracts tests/handoff -v
```

Expected result:

- every JSON Schema is structurally valid;
- source pins match `compatibility.lock.json`;
- all required ADRs exist;
- synthetic fixtures match the protocol-fixture contract;
- onboarding references exist;
- tests report no failures.

## Asset and secret boundary

Never commit:

- GRF archives or extracted Ragnarok asset bytes;
- RSW, GND, GAT, RSM, RSM2, SPR, ACT, PAL, STR, textures, sprites, audio, minimaps, or fonts from licensed client data;
- passwords, API keys, launch tickets, session secrets, private chat, identifying production account data, or database dumps.

Allowed evidence includes schemas, hashes, manifests without asset bytes, synthetic fixtures, sanitized packet metadata, tests, and legally approved screenshots.

## Current delivery sequence

```text
H1 governance and source pins
→ H2 shared contracts and synthetic fixtures
→ H3 validation, onboarding, and CI
→ finish roBrowser production gate
→ capture sanitized golden runtime fixtures
→ only then consider Unity U0/U1 work
```

## Definition of done for the handoff foundation

The foundation is complete only when:

1. `python -m tools.validation.validate_handoff` passes.
2. `python -m pytest tests/contracts tests/handoff -v` passes.
3. GitHub Actions runs the same checks successfully.
4. No asset or secret boundary violation exists in the diff.
5. A new contributor can identify the repositories, source pins, current priority, first commands, and Unity prohibition from this document alone.
6. The PR remains Draft until the automated checks have produced evidence.

## First suitable task after handoff foundation

Continue the active roBrowser production vertical slice. Do not start a Unity client. Select the highest-priority open issue that advances:

```text
portal launch ticket
→ WSS connection
→ login
→ character selection
→ map entry
→ correct terrain/entities
→ cache reuse
```

Any change to product direction requires a new ADR or an accepted revision to the existing ADR set.
