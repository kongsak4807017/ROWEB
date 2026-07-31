# EP01 Discovery Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reproducible, read-only EP01 discovery pipeline that inventories rAthena content, Modernized roBrowserLegacy consumers, canonical extracted assets, and published runtime assets, then emits deterministic sanitized JSON for ROWEB Operations Workbench.

**Architecture:** Implement independent Python discovery modules behind one CLI. Each module reads only approved external roots, returns normalized records, and writes reports under an explicit output directory. A final aggregator joins server records, client consumers, asset matches, dependency groups, reload policies, and owner dispositions without copying licensed asset bytes into Git.

**Tech Stack:** Python 3.11+, standard library, PyYAML only where already available, pytest, JSON/YAML fixtures, static HTML/JavaScript Workbench mockup.

## Global Constraints

- ROWEB is the canonical product repository.
- `C:\Ragnarok-Prontera\rathena`, `C:\Ragnarok-Prontera\HermesWorkSpace\roBrowserLegacy`, `C:\Ragnarok-Prontera\assets\data`, and the RemoteClient-PHP data tree are read-only.
- Generated runtime evidence defaults to `C:\Ragnarok-Prontera\Generated\server-growth\EP01` and is not committed unless sanitized.
- Do not follow symlinks or junctions outside approved roots.
- Do not commit licensed Ragnarok asset bytes, credentials, absolute local paths in fixtures, or production data.
- No SQL writes, shell passthrough, raw AtCommand execution, or server mutation.
- Output ordering must be deterministic.
- Non-ASCII and Korean paths must remain lossless.
- EP01 membership is evidence-backed and owner-controlled; asset presence alone never activates content.

---

## Planned file structure

- Create `tools/server-growth/ep01_discovery.py` — CLI orchestration and output writing.
- Create `tools/server-growth/path_policy.py` — approved-root validation, relative-path sanitization, junction/symlink rejection.
- Create `tools/server-growth/rathena_inventory.py` — maps, scripts, warps, NPCs, monsters, spawns, items, shops, drops, quests, jobs, skills, and relevant config references.
- Create `tools/server-growth/client_inventory.py` — Modernized roBrowserLegacy asset-consumer discovery.
- Create `tools/server-growth/asset_inventory.py` — canonical/published indexing, optional hashing, case and encoding aliases.
- Create `tools/server-growth/dependency_graph.py` — map, entity, item, NPC, effect/model, and UI dependency groups.
- Create `tools/server-growth/episode_manifest.py` — deterministic EP01 aggregate schema and owner-disposition overlay.
- Create `tools/server-growth/schemas/ep01-discovery.schema.json` — machine-readable output contract.
- Create `config/server-growth/ep01-discovery.example.json` — portable configuration without machine-specific paths.
- Create `tests/fixtures/server-growth/` — synthetic, license-safe mini trees.
- Create `tests/test_ep01_path_policy.py`.
- Create `tests/test_ep01_rathena_inventory.py`.
- Create `tests/test_ep01_client_inventory.py`.
- Create `tests/test_ep01_asset_inventory.py`.
- Create `tests/test_ep01_dependency_graph.py`.
- Create `tests/test_ep01_manifest.py`.
- Create `tests/test_ep01_discovery_cli.py`.
- Modify `apps/admin-studio/mockup/unified-workbench.html` only after the JSON contract is stable.
- Modify `docs/server-growth/episodes/EP01_DISCOVERY_AND_ASSET_CONTROL_PLAN.md` with the final command and generated report index.

---

### Task 1: Approved-root and path-safety foundation

**Files:**
- Create: `tools/server-growth/path_policy.py`
- Create: `tests/test_ep01_path_policy.py`
- Create: `tests/fixtures/server-growth/path-policy/allowed/.gitkeep`

**Interfaces:**
- Produces: `ApprovedRoot(label: str, path: Path)`
- Produces: `validate_input_path(path: Path, roots: Sequence[ApprovedRoot]) -> tuple[str, str]`
- Produces: `safe_walk(root: Path, excluded_names: set[str]) -> Iterator[Path]`

- [ ] Write tests proving normal files resolve to `(root_label, portable_relative_path)`.
- [ ] Write tests rejecting missing roots, paths outside roots, and symlink/junction escapes.
- [ ] Run `python -m pytest tests/test_ep01_path_policy.py -q` and verify failure before implementation.
- [ ] Implement root resolution without mutating input directories.
- [ ] Preserve Unicode using Python `str`/`Path` without lossy encoding conversion.
- [ ] Run the focused test and commit `feat: add EP01 discovery path safety`.

### Task 2: Deterministic output contract

**Files:**
- Create: `tools/server-growth/schemas/ep01-discovery.schema.json`
- Create: `tools/server-growth/episode_manifest.py`
- Create: `tests/test_ep01_manifest.py`

**Interfaces:**
- Produces: `build_ep01_manifest(server_records, client_consumers, assets, dependency_groups, warnings) -> dict`
- Produces schema keys: `schemaVersion`, `episodeId`, `generatedAt`, `scanRoots`, `summary`, `content`, `assets`, `dependencyGroups`, `missingReferences`, `collisions`, `warnings`.

- [ ] Add failing tests for stable sort order and portable relative source references.
- [ ] Add a test ensuring generated time can be injected for reproducible fixtures.
- [ ] Implement canonical sorting by domain, record ID, normalized path, then logical ID.
- [ ] Ensure `generatedAt` is excluded from equality-sensitive deterministic payload hashing or supplied explicitly.
- [ ] Run `python -m pytest tests/test_ep01_manifest.py -q`.
- [ ] Commit `feat: define deterministic EP01 discovery contract`.

### Task 3: rAthena server-content inventory

**Files:**
- Create: `tools/server-growth/rathena_inventory.py`
- Create synthetic fixtures under `tests/fixtures/server-growth/rathena/`
- Create: `tests/test_ep01_rathena_inventory.py`

**Interfaces:**
- Produces: `discover_rathena(root: Path, mode: str) -> list[dict]`
- Record domains: `map`, `warp`, `npc`, `monster`, `spawn`, `item`, `drop`, `shop`, `quest`, `job`, `skill`, `config`.

- [ ] Write fixtures representing YAML DB records, map spawn lines, NPC/warp scripts, shops, quest references, and config imports.
- [ ] Write failing tests for identifiers, source-relative paths, coordinates, and cross-references.
- [ ] Implement tolerant readers that report unsupported constructs as warnings rather than silently dropping them.
- [ ] Never execute scripts, connect to SQL, or import rAthena runtime modules.
- [ ] Run focused tests and commit `feat: inventory EP01 rAthena content`.

### Task 4: Modernized roBrowserLegacy consumer inventory

**Files:**
- Create: `tools/server-growth/client_inventory.py`
- Create synthetic client fixtures under `tests/fixtures/server-growth/client/`
- Create: `tests/test_ep01_client_inventory.py`

**Interfaces:**
- Produces: `discover_client_consumers(root: Path) -> list[dict]`
- Each record contains `originalReference`, `normalizedPath`, `consumerSource`, `line`, `category`, and inferred `rathenaDomains`.

- [ ] Add failing tests for JavaScript, TypeScript, HTML, CSS, JSON, XML, Lua, and shader references.
- [ ] Test Windows and POSIX separators, query strings, fragments, repeated separators, and non-ASCII paths.
- [ ] Exclude `.git`, `node_modules`, caches, generated reports, and `roBrowserLegacy-RemoteClient-PHP/data` from source-code scanning.
- [ ] Implement deterministic extraction and duplicate-reference aggregation.
- [ ] Run focused tests and commit `feat: discover roBrowserLegacy asset consumers`.

### Task 5: Canonical and published asset indexing

**Files:**
- Create: `tools/server-growth/asset_inventory.py`
- Create fixtures under `tests/fixtures/server-growth/assets/canonical/` and `published/`
- Create: `tests/test_ep01_asset_inventory.py`

**Interfaces:**
- Produces: `index_asset_root(root: Path, hash_mode: str, max_hash_bytes: int) -> dict[str, dict]`
- Produces: `match_asset(reference: dict, canonical_index: dict, published_index: dict) -> dict`
- Mapping states: `matched`, `canonical-only`, `published-only`, `missing`, `case-mismatch`, `encoding-alias`, `duplicate`, `collision`, `hash-mismatch`.

- [ ] Write failing tests for all mapping states.
- [ ] Add tests for `.gat/.gnd/.rsw`, `.spr/.act`, images, audio, and Korean filenames using tiny synthetic text payloads with representative extensions.
- [ ] Implement optional SHA-256 modes: `none`, `referenced`, `all`.
- [ ] Record byte size and hash but never include file bytes in output.
- [ ] Run focused tests and commit `feat: add three-way EP01 asset matching`.

### Task 6: Dependency graph and reload-policy inference

**Files:**
- Create: `tools/server-growth/dependency_graph.py`
- Create: `tests/test_ep01_dependency_graph.py`

**Interfaces:**
- Produces: `build_dependency_groups(content_records: list[dict], asset_records: list[dict]) -> list[dict]`
- Reload policies: `hot`, `ui-reopen`, `entity-respawn`, `map-reentry`, `page-refresh`, `reconnect`, `maintenance`.

- [ ] Add failing tests for map triples, SPR/ACT pairs, item presentation sets, NPC/script/sprite/localization sets, and map bundles.
- [ ] Verify incomplete groups are surfaced as `dependencyIssues`.
- [ ] Implement conservative reload inference; ambiguous records default to the safer policy.
- [ ] Run focused tests and commit `feat: build EP01 dependency and reload graph`.

### Task 7: Unified CLI and report set

**Files:**
- Create: `tools/server-growth/ep01_discovery.py`
- Create: `config/server-growth/ep01-discovery.example.json`
- Create: `tests/test_ep01_discovery_cli.py`

**Interfaces:**
- CLI arguments: `--rathena-root`, `--client-root`, `--canonical-assets`, `--published-assets`, `--output-dir`, `--hash-mode`, `--max-hash-bytes`, `--generated-at`.
- Outputs: `ep01-discovery.json`, `map-inventory.json`, `warp-graph.json`, `npc-inventory.json`, `monster-spawn-inventory.json`, `item-cross-reference.json`, `asset-mapping.json`, `dependency-issues.json`, `reload-impact.json`, `warnings.json`.

- [ ] Add an end-to-end failing test using only synthetic fixtures.
- [ ] Verify the CLI refuses an output directory nested inside any read-only input root.
- [ ] Implement atomic writes through temporary files followed by rename.
- [ ] Make repeated runs produce byte-identical JSON when `--generated-at` is fixed.
- [ ] Run `python -m pytest tests/test_ep01_discovery_cli.py -q`.
- [ ] Commit `feat: add EP01 discovery CLI and reports`.

### Task 8: Workbench import and EP01 views

**Files:**
- Modify: `apps/admin-studio/mockup/unified-workbench.html`
- Create or modify: `tests/test_unified_workbench.py`
- Create: `tests/fixtures/server-growth/ep01-discovery.sample.json`

**Interfaces:**
- Consumes: the stable EP01 discovery schema from Task 2.
- Produces UI views: Episode Overview, Content Inventory, Map & Warp Graph, NPC/Script Inventory, Monster/Spawn Inventory, Item/Drop/Shop Cross-reference, Asset Control, Reload Policies, Validation Evidence, Release Waves, Rollback.

- [ ] Add tests asserting file import, schema-version rejection, summary metrics, filtering, missing references, collisions, consumers, domains, and dependency issues.
- [ ] Implement browser-local import only; do not connect directly to a database or local filesystem path.
- [ ] Render owner disposition as editable in-memory state with export, not server mutation.
- [ ] Run focused Workbench tests and JavaScript syntax validation.
- [ ] Commit `feat: render EP01 discovery in Operations Workbench`.

### Task 9: Full verification, safety scan, and documentation

**Files:**
- Modify: `docs/server-growth/episodes/EP01_DISCOVERY_AND_ASSET_CONTROL_PLAN.md`
- Create: `docs/server-growth/episodes/EP01_DISCOVERY_RUNBOOK.md`

- [ ] Run `python -m pytest tests/test_ep01_*.py tests/test_unified_workbench.py -q`.
- [ ] Run the repository's full Python test command documented in `AGENTS.md` or `README.md`.
- [ ] Run `git diff --check`.
- [ ] Inspect tracked files for forbidden extensions and absolute machine-specific paths.
- [ ] Document the PowerShell command using the four approved local roots.
- [ ] Document expected report files, failure handling, runtime cost, hash modes, and rollback (delete generated output only).
- [ ] Commit `docs: add EP01 discovery runbook`.

## Completion gate

The implementation is complete only when synthetic-fixture tests pass, the local read-only scan completes without changing any external root, deterministic reports are generated, the Workbench imports the report, and the Git diff contains no licensed assets, secrets, or unsanitized absolute paths.
