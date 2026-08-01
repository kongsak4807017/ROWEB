# ROWEB Handoff Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the GitHub-native handoff foundation that lets a new developer or AI agent continue ROWEB safely without historical chat context, while preserving roBrowser-first delivery and deferring Unity runtime coding.

**Architecture:** Add governance records, a pinned source registry, machine-readable shared contracts, a small Python validation CLI, synthetic protocol-fixture conventions, and a single onboarding entrypoint. All deliverables are asset-free, testable in isolation, and compatible with the current `compatibility.lock.json`; Unity remains a declared future target only.

**Tech Stack:** Markdown, YAML, JSON Schema Draft 2020-12, Python 3.11+, `jsonschema`, `PyYAML`, `pytest`, PowerShell-compatible command examples, GitHub Actions-compatible test commands.

## Global Constraints

- `roBrowserLegacy` remains the primary production browser client until the production gate passes.
- Optimized `rAthena` remains the authoritative server for gameplay and persistence.
- Do not create, port, or upgrade Unity runtime code in this plan.
- Do not commit GRF archives or extracted Ragnarok asset bytes.
- Do not store credentials, launch tickets, session secrets, private chat, personal data, or licensed game assets in fixtures.
- Exact PACKETVER and compatibility values must be read from `compatibility.lock.json`; do not guess missing values.
- Keep UnityRO and RagnarokRebuildTcp as research references, not production dependencies.
- Every implementation task must include an independently testable deliverable and a focused commit.

---

## Planned File Map

```text
docs/adr/
├── ADR-020-client-product-strategy.md
├── ADR-021-rathena-authority.md
├── ADR-022-dual-client-contract-boundary.md
├── ADR-023-engine-neutral-asset-catalog.md
├── ADR-024-reference-source-and-license-policy.md
└── ADR-025-unity-start-gate.md

research/
└── source-registry.yaml

contracts/
├── source-registry.schema.json
├── asset-catalog.schema.json
├── compatibility-profile.schema.json
├── domain-event.schema.json
├── launch-ticket.schema.json
├── gateway-session.schema.json
├── gateway-error.schema.json
├── telemetry-event.schema.json
└── protocol-fixture.schema.json

protocol/
├── README.md
└── fixtures/
    └── synthetic/
        └── login-accepted.example.json

tools/validation/
├── __init__.py
├── common.py
├── validate_json.py
├── validate_yaml.py
└── validate_handoff.py

tests/contracts/
├── test_source_registry.py
├── test_asset_catalog_schema.py
├── test_compatibility_profile_schema.py
├── test_domain_event_schema.py
├── test_gateway_contracts.py
├── test_telemetry_schema.py
└── test_protocol_fixture_schema.py

tests/handoff/
├── test_adr_set.py
├── test_start_here_links.py
└── test_validate_handoff_cli.py

docs/handoff/
└── START_HERE.md

requirements-handoff.txt
```

Each file has one responsibility: ADRs record decisions; schemas define stable machine interfaces; validators provide repeatable checks; tests prove the contracts; `START_HERE.md` is the single successor entrypoint.

---

### Task 1: Record the six architecture decisions

**Files:**
- Create: `docs/adr/ADR-020-client-product-strategy.md`
- Create: `docs/adr/ADR-021-rathena-authority.md`
- Create: `docs/adr/ADR-022-dual-client-contract-boundary.md`
- Create: `docs/adr/ADR-023-engine-neutral-asset-catalog.md`
- Create: `docs/adr/ADR-024-reference-source-and-license-policy.md`
- Create: `docs/adr/ADR-025-unity-start-gate.md`
- Test: `tests/handoff/test_adr_set.py`

**Interfaces:**
- Consumes: approved design in `docs/superpowers/specs/2026-08-01-roweb-long-term-handoff-design.md`
- Produces: six stable decision records referenced by later onboarding and governance documents

- [ ] **Step 1: Write the failing ADR inventory test**

Create `tests/handoff/test_adr_set.py`:

```python
from pathlib import Path

ADR_ROOT = Path("docs/adr")
EXPECTED = {
    "ADR-020-client-product-strategy.md",
    "ADR-021-rathena-authority.md",
    "ADR-022-dual-client-contract-boundary.md",
    "ADR-023-engine-neutral-asset-catalog.md",
    "ADR-024-reference-source-and-license-policy.md",
    "ADR-025-unity-start-gate.md",
}
REQUIRED_HEADINGS = {
    "## Context",
    "## Decision",
    "## Alternatives considered",
    "## Consequences",
    "## Reversal conditions",
    "## Evidence",
    "## Owner",
}


def test_required_adr_files_exist() -> None:
    actual = {path.name for path in ADR_ROOT.glob("ADR-*.md")}
    assert EXPECTED <= actual


def test_required_adr_sections_exist() -> None:
    for filename in EXPECTED:
        content = (ADR_ROOT / filename).read_text(encoding="utf-8")
        missing = REQUIRED_HEADINGS - set(content.splitlines())
        assert not missing, f"{filename} missing headings: {sorted(missing)}"
        assert "Status: Accepted" in content
        assert "Date: 2026-08-01" in content
```

- [ ] **Step 2: Run the ADR test and verify failure**

Run:

```bash
python -m pytest tests/handoff/test_adr_set.py -v
```

Expected: FAIL because `docs/adr/` and the six files do not yet exist.

- [ ] **Step 3: Create the ADR files with concrete decisions**

Use this exact header and section structure in each file:

```markdown
# ADR-0XX: Decision title

- Status: Accepted
- Date: 2026-08-01

## Context

Concrete project context and the problem being decided.

## Decision

A direct, testable decision statement.

## Alternatives considered

- Alternative and why it was rejected.

## Consequences

- Positive and negative consequences.

## Reversal conditions

The evidence required before this decision may change.

## Evidence

- Approved design: `docs/superpowers/specs/2026-08-01-roweb-long-term-handoff-design.md`
- Repository evidence or compatibility lock used by this decision.

## Owner

ROWEB repository owner and maintainers.
```

Required decision text:

- ADR-020: roBrowser is the production classic client; Unity is a future enhanced client.
- ADR-021: rAthena remains authoritative; no replacement .NET MMORPG server is planned.
- ADR-022: both clients share launch-ticket, gateway, compatibility, domain-event, telemetry, and asset-catalog contracts.
- ADR-023: asset IDs are engine-neutral; target-specific mappings live under `targets.robrowser` and `targets.unity`.
- ADR-024: UnityRO and RagnarokRebuildTcp are pinned research sources; code reuse requires license review and explicit approval.
- ADR-025: Unity runtime coding starts only after the roBrowser production gate and all additional gate conditions pass.

- [ ] **Step 4: Run the ADR test and verify pass**

Run:

```bash
python -m pytest tests/handoff/test_adr_set.py -v
```

Expected: 2 tests PASS.

- [ ] **Step 5: Commit the ADR set**

```bash
git add docs/adr tests/handoff/test_adr_set.py
git commit -m "docs: record ROWEB long-term architecture decisions"
```

---

### Task 2: Add the pinned source reference registry

**Files:**
- Create: `research/source-registry.yaml`
- Create: `contracts/source-registry.schema.json`
- Create: `tests/contracts/test_source_registry.py`
- Create: `requirements-handoff.txt`

**Interfaces:**
- Consumes: exact roBrowser and rAthena SHAs from `compatibility.lock.json`
- Produces: `research/source-registry.yaml` validated by `contracts/source-registry.schema.json`

- [ ] **Step 1: Add validation dependencies**

Create `requirements-handoff.txt`:

```text
jsonschema==4.23.0
PyYAML==6.0.2
pytest==8.3.5
```

- [ ] **Step 2: Write the failing source-registry tests**

Create `tests/contracts/test_source_registry.py`:

```python
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_source_registry_matches_schema() -> None:
    schema = load_json("contracts/source-registry.schema.json")
    registry = yaml.safe_load((ROOT / "research/source-registry.yaml").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(registry)


def test_production_source_shas_match_compatibility_lock() -> None:
    lock = load_json("compatibility.lock.json")
    registry = yaml.safe_load((ROOT / "research/source-registry.yaml").read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in registry["sources"]}
    assert by_id["robrowser-legacy"]["ref"] == lock["client"]["commit"]
    assert by_id["rathena"]["ref"] == lock["server"]["commit"]
    assert by_id["robrowser-legacy"]["production_dependency"] is True
    assert by_id["rathena"]["production_dependency"] is True
    assert by_id["unityro"]["production_dependency"] is False
    assert by_id["ragnarok-rebuild-tcp"]["production_dependency"] is False
```

- [ ] **Step 3: Run tests and verify failure**

Run:

```bash
python -m pip install -r requirements-handoff.txt
python -m pytest tests/contracts/test_source_registry.py -v
```

Expected: FAIL because the schema and registry do not exist.

- [ ] **Step 4: Create the source-registry schema**

Create `contracts/source-registry.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://roweb.local/contracts/source-registry.schema.json",
  "type": "object",
  "required": ["schema_version", "reviewed_at", "sources"],
  "additionalProperties": false,
  "properties": {
    "schema_version": {"const": 1},
    "reviewed_at": {"type": "string", "format": "date"},
    "sources": {
      "type": "array",
      "minItems": 4,
      "items": {
        "type": "object",
        "required": [
          "id", "repository", "ref", "ref_type", "license",
          "roles", "allowed_use", "prohibited_use", "production_dependency"
        ],
        "additionalProperties": false,
        "properties": {
          "id": {"type": "string", "pattern": "^[a-z0-9-]+$"},
          "repository": {"type": "string", "pattern": "^[^/]+/[^/]+$"},
          "upstream": {"type": "string", "pattern": "^[^/]+/[^/]+$"},
          "ref": {"type": "string", "minLength": 3},
          "ref_type": {"enum": ["commit", "tag"]},
          "license": {"type": "string", "minLength": 1},
          "roles": {"type": "array", "minItems": 1, "items": {"type": "string"}},
          "allowed_use": {"type": "array", "minItems": 1, "items": {"type": "string"}},
          "prohibited_use": {"type": "array", "minItems": 1, "items": {"type": "string"}},
          "production_dependency": {"type": "boolean"}
        }
      }
    }
  }
}
```

- [ ] **Step 5: Create the source registry with exact current pins**

Create `research/source-registry.yaml` using these values:

```yaml
schema_version: 1
reviewed_at: 2026-08-01
sources:
  - id: robrowser-legacy
    repository: kongsak4807017/roBrowserLegacy
    ref: e84bfdcdadb791ba18fb501943e8e992ba8f646a
    ref_type: commit
    license: review-required-before-public-release
    roles:
      - production-client-baseline
      - browser-behavior-reference
      - golden-runtime-evidence-source
    allowed_use:
      - pinned-production-runtime
      - compatibility-analysis
    prohibited_use:
      - unreviewed-public-release
    production_dependency: true

  - id: rathena
    repository: kongsak4807017/rathena
    ref: 0c3ca757ad35fff003130a8441a10f27cccd0ed9
    ref_type: commit
    license: GPL-3.0
    roles:
      - authoritative-game-server
      - compatibility-baseline
    allowed_use:
      - production-server
      - protocol-evidence
    prohibited_use:
      - replacement-by-unapproved-custom-server
    production_dependency: true

  - id: unityro
    repository: kongsak4807017/unityro
    upstream: guilhermelhr/unityro
    ref: 0.6.1
    ref_type: tag
    license: AGPL-3.0
    roles:
      - unity-athena-protocol-reference
      - ro-format-rendering-reference
    allowed_use:
      - research
      - behavior-comparison
    prohibited_use:
      - production-dependency-without-license-review
      - direct-copy-without-approval
    production_dependency: false

  - id: ragnarok-rebuild-tcp
    repository: kongsak4807017/RagnarokRebuildTcp
    ref: 8b6ea97bcd23a7e60cc9abc27df6911ae19b423d
    ref_type: commit
    license: repository-license-review-required
    roles:
      - unity-asset-pipeline-reference
      - rendering-reference
      - custom-protocol-research
    allowed_use:
      - research
      - architecture-comparison
    prohibited_use:
      - replacing-rathena
      - assuming-direct-rathena-compatibility
    production_dependency: false
```

- [ ] **Step 6: Run source-registry tests and verify pass**

Run:

```bash
python -m pytest tests/contracts/test_source_registry.py -v
```

Expected: 2 tests PASS.

- [ ] **Step 7: Commit the registry and dependency lock**

```bash
git add requirements-handoff.txt research/source-registry.yaml contracts/source-registry.schema.json tests/contracts/test_source_registry.py
git commit -m "feat: add pinned source reference registry"
```

---

### Task 3: Define the engine-neutral asset catalog contract

**Files:**
- Create: `contracts/asset-catalog.schema.json`
- Create: `tests/contracts/test_asset_catalog_schema.py`

**Interfaces:**
- Consumes: stable asset IDs and target boundaries from ADR-023
- Produces: JSON Schema for catalog producers and future roBrowser/Unity target adapters

- [ ] **Step 1: Write failing schema tests with valid and invalid examples**

Create `tests/contracts/test_asset_catalog_schema.py`:

```python
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[2]


def validator() -> Draft202012Validator:
    schema = json.loads((ROOT / "contracts/asset-catalog.schema.json").read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def valid_asset() -> dict:
    return {
        "schemaVersion": 1,
        "assetId": "map.prontera.world",
        "assetType": "map",
        "source": {
            "rsw": "data/prontera.rsw",
            "gnd": "data/prontera.gnd",
            "gat": "data/prontera.gat"
        },
        "dependencies": ["audio.map.prontera"],
        "targets": {
            "robrowser": {"runtimePath": "data/prontera.rsw"},
            "unity": {
                "addressableKey": "maps/prontera",
                "conversionProfile": "ro-map-v1"
            }
        }
    }


def test_valid_engine_neutral_asset_passes() -> None:
    validator().validate(valid_asset())


def test_missing_robrowser_target_fails() -> None:
    asset = valid_asset()
    del asset["targets"]["robrowser"]
    with pytest.raises(ValidationError):
        validator().validate(asset)


def test_asset_id_rejects_paths() -> None:
    asset = valid_asset()
    asset["assetId"] = "../data/prontera.rsw"
    with pytest.raises(ValidationError):
        validator().validate(asset)
```

- [ ] **Step 2: Run tests and verify failure**

Run:

```bash
python -m pytest tests/contracts/test_asset_catalog_schema.py -v
```

Expected: FAIL because `contracts/asset-catalog.schema.json` does not exist.

- [ ] **Step 3: Implement the schema**

Create `contracts/asset-catalog.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://roweb.local/contracts/asset-catalog.schema.json",
  "type": "object",
  "required": ["schemaVersion", "assetId", "assetType", "source", "dependencies", "targets"],
  "additionalProperties": false,
  "properties": {
    "schemaVersion": {"const": 1},
    "assetId": {"type": "string", "pattern": "^[a-z0-9]+(?:[._-][a-z0-9]+)+$"},
    "assetType": {"enum": ["map", "texture", "model", "sprite", "effect", "audio", "ui", "data", "font"]},
    "source": {
      "type": "object",
      "minProperties": 1,
      "additionalProperties": {"type": "string", "pattern": "^(?!.*\\.\\.).+$"}
    },
    "dependencies": {
      "type": "array",
      "uniqueItems": true,
      "items": {"type": "string", "pattern": "^[a-z0-9]+(?:[._-][a-z0-9]+)+$"}
    },
    "targets": {
      "type": "object",
      "required": ["robrowser"],
      "additionalProperties": false,
      "properties": {
        "robrowser": {
          "type": "object",
          "required": ["runtimePath"],
          "additionalProperties": false,
          "properties": {
            "runtimePath": {"type": "string", "pattern": "^(?!.*\\.\\.).+$"}
          }
        },
        "unity": {
          "type": "object",
          "required": ["addressableKey", "conversionProfile"],
          "additionalProperties": false,
          "properties": {
            "addressableKey": {"type": "string", "pattern": "^(?!/)(?!.*\\.\\.).+$"},
            "conversionProfile": {"type": "string", "pattern": "^[a-z0-9-]+$"}
          }
        }
      }
    }
  }
}
```

- [ ] **Step 4: Run schema tests and verify pass**

Run:

```bash
python -m pytest tests/contracts/test_asset_catalog_schema.py -v
```

Expected: 3 tests PASS.

- [ ] **Step 5: Commit the asset contract**

```bash
git add contracts/asset-catalog.schema.json tests/contracts/test_asset_catalog_schema.py
git commit -m "feat: define engine-neutral asset catalog contract"
```

---

### Task 4: Define the compatibility profile and domain-event contracts

**Files:**
- Create: `contracts/compatibility-profile.schema.json`
- Create: `contracts/domain-event.schema.json`
- Create: `tests/contracts/test_compatibility_profile_schema.py`
- Create: `tests/contracts/test_domain_event_schema.py`

**Interfaces:**
- Consumes: `compatibility.lock.json`
- Produces: validated client conformance profile and packet-independent event envelope

- [ ] **Step 1: Write the failing compatibility-profile tests**

Create `tests/contracts/test_compatibility_profile_schema.py`:

```python
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[2]


def schema_validator() -> Draft202012Validator:
    schema = json.loads((ROOT / "contracts/compatibility-profile.schema.json").read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def profile_from_lock() -> dict:
    lock = json.loads((ROOT / "compatibility.lock.json").read_text(encoding="utf-8"))
    return {
        "schemaVersion": 1,
        "profileId": "ROWEB_CLASSIC_PRE_RE_V1",
        "server": {
            "repository": "kongsak4807017/rathena",
            "commit": lock["server"]["commit"],
            "gameplayMode": lock["server"]["profile"]
        },
        "protocol": {
            "packetverStatus": lock["server"]["packetver"]["status"],
            "packetver": lock["server"]["packetver"]["value"],
            "encoding": "cp949-utf8-bridge"
        },
        "clients": {
            "robrowser": {"supported": True, "conformanceLevel": "production"},
            "unity": {"supported": False, "conformanceLevel": "planned"}
        }
    }


def test_profile_allows_unresolved_packetver_when_status_is_pending() -> None:
    schema_validator().validate(profile_from_lock())


def test_verified_packetver_requires_integer() -> None:
    profile = profile_from_lock()
    profile["protocol"]["packetverStatus"] = "verified"
    profile["protocol"]["packetver"] = None
    with pytest.raises(ValidationError):
        schema_validator().validate(profile)
```

- [ ] **Step 2: Write the failing domain-event tests**

Create `tests/contracts/test_domain_event_schema.py`:

```python
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[2]


def validator() -> Draft202012Validator:
    schema = json.loads((ROOT / "contracts/domain-event.schema.json").read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def event() -> dict:
    return {
        "schemaVersion": 1,
        "eventId": "018f8f8f-5c58-7a58-a1e1-123456789abc",
        "eventType": "world.entity.spawned",
        "occurredAt": "2026-08-01T09:30:00Z",
        "correlationId": "session-test-001",
        "source": "athena-protocol-adapter",
        "payload": {"entityType": "player", "entityId": 1001}
    }


def test_domain_event_passes() -> None:
    validator().validate(event())


def test_event_type_must_be_namespaced() -> None:
    value = event()
    value["eventType"] = "spawn"
    with pytest.raises(ValidationError):
        validator().validate(value)
```

- [ ] **Step 3: Run both test files and verify failure**

Run:

```bash
python -m pytest tests/contracts/test_compatibility_profile_schema.py tests/contracts/test_domain_event_schema.py -v
```

Expected: FAIL because both schemas are missing.

- [ ] **Step 4: Implement the compatibility-profile schema**

Create `contracts/compatibility-profile.schema.json` with a conditional PACKETVER rule:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://roweb.local/contracts/compatibility-profile.schema.json",
  "type": "object",
  "required": ["schemaVersion", "profileId", "server", "protocol", "clients"],
  "additionalProperties": false,
  "properties": {
    "schemaVersion": {"const": 1},
    "profileId": {"type": "string", "pattern": "^ROWEB_[A-Z0-9_]+$"},
    "server": {
      "type": "object",
      "required": ["repository", "commit", "gameplayMode"],
      "additionalProperties": false,
      "properties": {
        "repository": {"const": "kongsak4807017/rathena"},
        "commit": {"type": "string", "pattern": "^[0-9a-f]{40}$"},
        "gameplayMode": {"enum": ["pre-renewal", "renewal"]}
      }
    },
    "protocol": {
      "type": "object",
      "required": ["packetverStatus", "packetver", "encoding"],
      "additionalProperties": false,
      "properties": {
        "packetverStatus": {"enum": ["pending-runtime-verification", "verified"]},
        "packetver": {"type": ["integer", "null"], "minimum": 20000101, "maximum": 20991231},
        "encoding": {"enum": ["cp949-utf8-bridge", "utf-8"]}
      },
      "allOf": [
        {
          "if": {"properties": {"packetverStatus": {"const": "verified"}}},
          "then": {"properties": {"packetver": {"type": "integer"}}}
        }
      ]
    },
    "clients": {
      "type": "object",
      "required": ["robrowser", "unity"],
      "additionalProperties": false,
      "properties": {
        "robrowser": {"$ref": "#/$defs/client"},
        "unity": {"$ref": "#/$defs/client"}
      }
    }
  },
  "$defs": {
    "client": {
      "type": "object",
      "required": ["supported", "conformanceLevel"],
      "additionalProperties": false,
      "properties": {
        "supported": {"type": "boolean"},
        "conformanceLevel": {"enum": ["planned", "experimental", "production"]}
      }
    }
  }
}
```

- [ ] **Step 5: Implement the domain-event schema**

Create `contracts/domain-event.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://roweb.local/contracts/domain-event.schema.json",
  "type": "object",
  "required": ["schemaVersion", "eventId", "eventType", "occurredAt", "correlationId", "source", "payload"],
  "additionalProperties": false,
  "properties": {
    "schemaVersion": {"const": 1},
    "eventId": {"type": "string", "format": "uuid"},
    "eventType": {"type": "string", "pattern": "^[a-z]+(?:\\.[a-z]+){2,}$"},
    "occurredAt": {"type": "string", "format": "date-time"},
    "correlationId": {"type": "string", "minLength": 1, "maxLength": 128},
    "source": {"enum": ["athena-protocol-adapter", "gateway", "asset-service", "client"]},
    "payload": {"type": "object"}
  }
}
```

- [ ] **Step 6: Run both test files and verify pass**

Run:

```bash
python -m pytest tests/contracts/test_compatibility_profile_schema.py tests/contracts/test_domain_event_schema.py -v
```

Expected: 4 tests PASS.

- [ ] **Step 7: Commit compatibility and event contracts**

```bash
git add contracts/compatibility-profile.schema.json contracts/domain-event.schema.json tests/contracts/test_compatibility_profile_schema.py tests/contracts/test_domain_event_schema.py
git commit -m "feat: define compatibility and domain event contracts"
```

---

### Task 5: Define launch-ticket, gateway-session, error, and telemetry contracts

**Files:**
- Create: `contracts/launch-ticket.schema.json`
- Create: `contracts/gateway-session.schema.json`
- Create: `contracts/gateway-error.schema.json`
- Create: `contracts/telemetry-event.schema.json`
- Create: `tests/contracts/test_gateway_contracts.py`
- Create: `tests/contracts/test_telemetry_schema.py`

**Interfaces:**
- Consumes: portal → one-time ticket → WSS gateway flow
- Produces: stable session-entry and client-comparison event envelopes

- [ ] **Step 1: Write failing gateway contract tests**

Create `tests/contracts/test_gateway_contracts.py` with one valid example per schema and these mandatory rejection cases:

```python
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[2]


def load_validator(name: str) -> Draft202012Validator:
    schema = json.loads((ROOT / "contracts" / name).read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def test_launch_ticket_accepts_opaque_one_time_ticket() -> None:
    value = {
        "schemaVersion": 1,
        "ticket": "opaque-ticket-value",
        "expiresAt": "2026-08-01T09:35:00Z",
        "gatewayUrl": "wss://game.example.invalid/session",
        "compatibilityProfile": "ROWEB_CLASSIC_PRE_RE_V1"
    }
    load_validator("launch-ticket.schema.json").validate(value)


def test_launch_ticket_rejects_plaintext_password() -> None:
    value = {
        "schemaVersion": 1,
        "ticket": "opaque-ticket-value",
        "expiresAt": "2026-08-01T09:35:00Z",
        "gatewayUrl": "wss://game.example.invalid/session",
        "compatibilityProfile": "ROWEB_CLASSIC_PRE_RE_V1",
        "password": "secret"
    }
    with pytest.raises(ValidationError):
        load_validator("launch-ticket.schema.json").validate(value)


def test_gateway_session_requires_correlation_id() -> None:
    value = {
        "schemaVersion": 1,
        "sessionId": "session-001",
        "correlationId": "corr-001",
        "clientType": "robrowser",
        "compatibilityProfile": "ROWEB_CLASSIC_PRE_RE_V1"
    }
    load_validator("gateway-session.schema.json").validate(value)


def test_gateway_error_is_machine_readable() -> None:
    value = {
        "schemaVersion": 1,
        "code": "TICKET_EXPIRED",
        "message": "Launch ticket expired.",
        "retryable": False,
        "correlationId": "corr-001"
    }
    load_validator("gateway-error.schema.json").validate(value)
```

- [ ] **Step 2: Write failing telemetry tests**

Create `tests/contracts/test_telemetry_schema.py`:

```python
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[2]


def validator() -> Draft202012Validator:
    schema = json.loads((ROOT / "contracts/telemetry-event.schema.json").read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def telemetry() -> dict:
    return {
        "schemaVersion": 1,
        "eventType": "map.load.completed",
        "occurredAt": "2026-08-01T09:30:00Z",
        "clientType": "robrowser",
        "clientVersion": "test",
        "compatibilityProfile": "ROWEB_CLASSIC_PRE_RE_V1",
        "correlationId": "corr-001",
        "deviceProfile": {"platform": "web", "memoryClassMb": 4096},
        "measurements": {"durationMs": 1250}
    }


def test_telemetry_event_passes() -> None:
    validator().validate(telemetry())


def test_telemetry_rejects_secret_fields() -> None:
    value = telemetry()
    value["password"] = "secret"
    with pytest.raises(ValidationError):
        validator().validate(value)
```

- [ ] **Step 3: Run tests and verify failure**

Run:

```bash
python -m pytest tests/contracts/test_gateway_contracts.py tests/contracts/test_telemetry_schema.py -v
```

Expected: FAIL because the four schemas are missing.

- [ ] **Step 4: Implement all four schemas**

Use JSON Schema Draft 2020-12, `additionalProperties: false` at the top level, and these exact required fields:

- `launch-ticket`: `schemaVersion`, `ticket`, `expiresAt`, `gatewayUrl`, `compatibilityProfile`; `gatewayUrl` pattern must begin `wss://`.
- `gateway-session`: `schemaVersion`, `sessionId`, `correlationId`, `clientType`, `compatibilityProfile`; `clientType` enum is `robrowser|unity`.
- `gateway-error`: `schemaVersion`, `code`, `message`, `retryable`, `correlationId`; `code` pattern is `^[A-Z][A-Z0-9_]+$`.
- `telemetry-event`: fields shown in `telemetry()`; `eventType` enum must include the twelve events from the approved design; `measurements` must accept numeric/string/boolean values only.

For telemetry, use this event enum:

```json
[
  "client.boot.started",
  "client.boot.completed",
  "asset.request.started",
  "asset.request.failed",
  "gateway.connected",
  "session.login.completed",
  "map.load.started",
  "map.load.completed",
  "client.frame.performance",
  "client.memory.snapshot",
  "client.error"
]
```

- [ ] **Step 5: Run gateway and telemetry tests and verify pass**

Run:

```bash
python -m pytest tests/contracts/test_gateway_contracts.py tests/contracts/test_telemetry_schema.py -v
```

Expected: all tests PASS.

- [ ] **Step 6: Commit gateway and telemetry contracts**

```bash
git add contracts/launch-ticket.schema.json contracts/gateway-session.schema.json contracts/gateway-error.schema.json contracts/telemetry-event.schema.json tests/contracts/test_gateway_contracts.py tests/contracts/test_telemetry_schema.py
git commit -m "feat: define gateway and telemetry contracts"
```

---

### Task 6: Define the synthetic protocol-fixture format

**Files:**
- Create: `contracts/protocol-fixture.schema.json`
- Create: `protocol/README.md`
- Create: `protocol/fixtures/synthetic/login-accepted.example.json`
- Create: `tests/contracts/test_protocol_fixture_schema.py`

**Interfaces:**
- Consumes: known packet metadata and expected ROWEB domain events
- Produces: a safe, asset-free fixture format for future captured packets

- [ ] **Step 1: Write failing fixture-schema tests**

Create `tests/contracts/test_protocol_fixture_schema.py`:

```python
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[2]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_synthetic_fixture_matches_schema() -> None:
    schema = load("contracts/protocol-fixture.schema.json")
    fixture = load("protocol/fixtures/synthetic/login-accepted.example.json")
    Draft202012Validator(schema).validate(fixture)


def test_fixture_rejects_non_hex_packet_bytes() -> None:
    schema = load("contracts/protocol-fixture.schema.json")
    fixture = load("protocol/fixtures/synthetic/login-accepted.example.json")
    fixture["rawHex"] = "contains-secret-text"
    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(fixture)
```

- [ ] **Step 2: Run fixture tests and verify failure**

Run:

```bash
python -m pytest tests/contracts/test_protocol_fixture_schema.py -v
```

Expected: FAIL because the schema and example fixture are missing.

- [ ] **Step 3: Create the protocol-fixture schema**

Create `contracts/protocol-fixture.schema.json` with these required fields:

```json
{
  "schemaVersion": 1,
  "fixtureId": "login.accepted.synthetic.v1",
  "synthetic": true,
  "direction": "server_to_client",
  "packetId": "0x0000",
  "packetverStatus": "pending-runtime-verification",
  "packetver": null,
  "rawHex": "00000000",
  "decoded": {},
  "expectedEvent": {
    "eventType": "session.login.accepted",
    "payload": {}
  },
  "scenario": "Synthetic contract example; not captured from a player session."
}
```

Schema requirements:

- `fixtureId` pattern `^[a-z0-9]+(?:[._-][a-z0-9]+)+$`
- `synthetic` boolean
- `direction` enum `client_to_server|server_to_client`
- `packetId` pattern `^0x[0-9A-Fa-f]{4}$`
- conditional PACKETVER rule identical to the compatibility profile
- `rawHex` pattern `^(?:[0-9A-Fa-f]{2})+$`
- `decoded` object
- `expectedEvent.eventType` namespaced pattern
- `scenario` non-empty string
- `additionalProperties: false`

- [ ] **Step 4: Add protocol capture policy**

Create `protocol/README.md` stating:

```markdown
# ROWEB Protocol Fixtures

Fixtures are compatibility evidence, not production secrets.

Allowed:
- raw packet bytes from controlled test accounts
- direction, packet ID, verified PACKETVER
- deterministic decoded JSON
- expected ROWEB domain event
- synthetic identifiers

Forbidden:
- account names or passwords
- launch tickets or session secrets
- private chat content
- personal data
- licensed asset bytes

Captured fixtures must be sanitized, reproducible, and linked to a named test scenario. Until PACKETVER is verified in `compatibility.lock.json`, fixtures must keep `packetverStatus: pending-runtime-verification` and `packetver: null`.
```

- [ ] **Step 5: Add the synthetic example and run tests**

Create `protocol/fixtures/synthetic/login-accepted.example.json` using the exact object shown in Step 3.

Run:

```bash
python -m pytest tests/contracts/test_protocol_fixture_schema.py -v
```

Expected: 2 tests PASS.

- [ ] **Step 6: Commit the fixture contract**

```bash
git add contracts/protocol-fixture.schema.json protocol/README.md protocol/fixtures/synthetic/login-accepted.example.json tests/contracts/test_protocol_fixture_schema.py
git commit -m "feat: define safe protocol fixture format"
```

---

### Task 7: Build the reusable handoff validation CLI

**Files:**
- Create: `tools/validation/__init__.py`
- Create: `tools/validation/common.py`
- Create: `tools/validation/validate_json.py`
- Create: `tools/validation/validate_yaml.py`
- Create: `tools/validation/validate_handoff.py`
- Create: `tests/handoff/test_validate_handoff_cli.py`

**Interfaces:**
- Consumes: schema path and JSON/YAML document path
- Produces: exit code `0` on valid handoff state, exit code `1` with actionable stderr on failure

- [ ] **Step 1: Write failing CLI tests**

Create `tests/handoff/test_validate_handoff_cli.py`:

```python
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_validate_handoff_command_passes() -> None:
    result = run("-m", "tools.validation.validate_handoff")
    assert result.returncode == 0, result.stderr
    assert "handoff validation passed" in result.stdout.lower()


def test_validate_json_reports_missing_file() -> None:
    result = run(
        "-m", "tools.validation.validate_json",
        "contracts/asset-catalog.schema.json",
        "missing.json",
    )
    assert result.returncode == 1
    assert "missing.json" in result.stderr
```

- [ ] **Step 2: Run CLI tests and verify failure**

Run:

```bash
python -m pytest tests/handoff/test_validate_handoff_cli.py -v
```

Expected: FAIL because the validation modules do not exist.

- [ ] **Step 3: Implement focused validation helpers**

Create `tools/validation/common.py` with these exact public functions:

```python
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    """Load UTF-8 JSON and raise ValueError with the path on parse failure."""


def load_yaml(path: Path) -> Any:
    """Load UTF-8 YAML with safe_load and raise ValueError with the path on failure."""


def validate_document(schema: dict, document: Any) -> list[str]:
    """Return sorted human-readable Draft 2020-12 validation errors."""
```

Implementation requirements:

- use `json.loads`, `yaml.safe_load`, and `Draft202012Validator`
- format each validation error as `path.to.field: message`; use `<root>` for root errors
- never call `sys.exit` from `common.py`

- [ ] **Step 4: Implement the JSON and YAML command modules**

`validate_json.py` command:

```text
python -m tools.validation.validate_json <schema.json> <document.json>
```

`validate_yaml.py` command:

```text
python -m tools.validation.validate_yaml <schema.json> <document.yaml>
```

Both commands must:

- return `1` for missing files, parse failures, or schema failures
- print one error per line to stderr
- print `valid: <document>` on success

- [ ] **Step 5: Implement the aggregate handoff validator**

`validate_handoff.py` must validate:

1. `research/source-registry.yaml` against `contracts/source-registry.schema.json`
2. every JSON file under `protocol/fixtures/synthetic/` against `contracts/protocol-fixture.schema.json`
3. all six ADR files exist
4. `compatibility.lock.json` production SHAs match the source registry

On success, print:

```text
handoff validation passed
```

- [ ] **Step 6: Run CLI tests and full handoff validator**

Run:

```bash
python -m pytest tests/handoff/test_validate_handoff_cli.py -v
python -m tools.validation.validate_handoff
```

Expected: tests PASS and CLI prints `handoff validation passed`.

- [ ] **Step 7: Commit the validation CLI**

```bash
git add tools/validation tests/handoff/test_validate_handoff_cli.py
git commit -m "feat: add ROWEB handoff validation CLI"
```

---

### Task 8: Create the successor entrypoint and link checks

**Files:**
- Create: `docs/handoff/START_HERE.md`
- Create: `tests/handoff/test_start_here_links.py`
- Modify: `README.md`
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: ADRs, registry, contracts, validators, existing architecture and playbook documents
- Produces: one authoritative onboarding path for humans and AI agents

- [ ] **Step 1: Write failing onboarding-link tests**

Create `tests/handoff/test_start_here_links.py`:

```python
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
START = ROOT / "docs/handoff/START_HERE.md"


def markdown_paths(text: str) -> set[str]:
    return {
        target.split("#", 1)[0]
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text)
        if not target.startswith(("http://", "https://", "mailto:"))
    }


def test_start_here_exists_and_has_required_sections() -> None:
    content = START.read_text(encoding="utf-8")
    for heading in [
        "## Product direction",
        "## Repository map",
        "## Canonical workspace",
        "## Asset boundary",
        "## Bootstrap and validation",
        "## Current delivery gate",
        "## First contribution",
        "## Unity deferral rule",
    ]:
        assert heading in content


def test_start_here_local_links_exist() -> None:
    content = START.read_text(encoding="utf-8")
    for target in markdown_paths(content):
        resolved = (START.parent / target).resolve()
        assert resolved.exists(), f"Broken local link: {target}"


def test_readme_and_agents_link_to_start_here() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "docs/handoff/START_HERE.md" in readme
    assert "docs/handoff/START_HERE.md" in agents
```

- [ ] **Step 2: Run link tests and verify failure**

Run:

```bash
python -m pytest tests/handoff/test_start_here_links.py -v
```

Expected: FAIL because `START_HERE.md` does not exist and README/AGENTS do not link to it.

- [ ] **Step 3: Create `START_HERE.md` with concrete commands**

Required content:

```markdown
# START HERE — ROWEB Handoff

## Product direction
roBrowser first; optimized rAthena authoritative; Unity runtime deferred.

## Repository map
Links to ROWEB, roBrowserLegacy, and rAthena responsibilities.

## Canonical workspace
Use `C:\RO-WEB-V1` as the current canonical workspace. Explain `ROWEB`, `roBrowserLegacy`, `rathena`, `private-assets`, `BGM`, and `runtime` boundaries.

## Asset boundary
Repeat the no-GRF/no-extracted-assets-in-Git rule and link to `../SECURITY_AND_IP_BOUNDARY.md`.

## Bootstrap and validation
```powershell
python -m pip install -r requirements-handoff.txt
python -m pytest tests/contracts tests/handoff -v
python -m tools.validation.validate_handoff
```

## Current delivery gate
Link to the approved design and describe the roBrowser vertical slice.

## First contribution
Start with one failing contract or handoff test; do not start Unity code.

## Unity deferral rule
Link ADR-025 and list the gate conditions.
```

Use valid relative links from `docs/handoff/START_HERE.md`, including:

- `../../AGENTS.md`
- `../ARCHITECTURE.md`
- `../IMPLEMENTATION_PLAYBOOK.md`
- `../SECURITY_AND_IP_BOUNDARY.md`
- `../superpowers/specs/2026-08-01-roweb-long-term-handoff-design.md`
- `../adr/ADR-025-unity-start-gate.md`

- [ ] **Step 4: Link README and AGENTS to the entrypoint**

Add to README's repository documents section:

```markdown
- [`docs/handoff/START_HERE.md`](docs/handoff/START_HERE.md) — authoritative successor and contributor entrypoint
```

Add `docs/handoff/START_HERE.md` as item 2 in `AGENTS.md` section `## 2. Read before work`, renumbering the remaining items.

- [ ] **Step 5: Run link tests and complete validation suite**

Run:

```bash
python -m pytest tests/contracts tests/handoff -v
python -m tools.validation.validate_handoff
```

Expected: all tests PASS and aggregate validation succeeds.

- [ ] **Step 6: Commit onboarding entrypoint**

```bash
git add docs/handoff/START_HERE.md README.md AGENTS.md tests/handoff/test_start_here_links.py
git commit -m "docs: add authoritative ROWEB handoff entrypoint"
```

---

### Task 9: Add CI enforcement for the handoff foundation

**Files:**
- Create: `.github/workflows/handoff-contracts.yml`

**Interfaces:**
- Consumes: `requirements-handoff.txt`, contract tests, handoff tests, aggregate validator
- Produces: required repeatable GitHub Actions evidence for every relevant pull request

- [ ] **Step 1: Create the workflow**

Create `.github/workflows/handoff-contracts.yml`:

```yaml
name: Handoff Contracts

on:
  pull_request:
    paths:
      - "contracts/**"
      - "research/source-registry.yaml"
      - "protocol/**"
      - "tools/validation/**"
      - "tests/contracts/**"
      - "tests/handoff/**"
      - "docs/adr/**"
      - "docs/handoff/**"
      - "compatibility.lock.json"
      - "requirements-handoff.txt"
      - ".github/workflows/handoff-contracts.yml"
  push:
    branches: [main]
    paths:
      - "contracts/**"
      - "research/source-registry.yaml"
      - "protocol/**"
      - "tools/validation/**"
      - "tests/contracts/**"
      - "tests/handoff/**"
      - "docs/adr/**"
      - "docs/handoff/**"
      - "compatibility.lock.json"
      - "requirements-handoff.txt"
      - ".github/workflows/handoff-contracts.yml"

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip
      - run: python -m pip install -r requirements-handoff.txt
      - run: python -m pytest tests/contracts tests/handoff -v
      - run: python -m tools.validation.validate_handoff
```

- [ ] **Step 2: Validate workflow syntax locally**

Run:

```bash
python - <<'PY'
from pathlib import Path
import yaml
path = Path('.github/workflows/handoff-contracts.yml')
data = yaml.safe_load(path.read_text(encoding='utf-8'))
assert data['name'] == 'Handoff Contracts'
assert 'validate' in data['jobs']
print('workflow syntax valid')
PY
```

Expected: `workflow syntax valid`.

- [ ] **Step 3: Run the complete local validation suite**

Run:

```bash
python -m pytest tests/contracts tests/handoff -v
python -m tools.validation.validate_handoff
```

Expected: all tests PASS.

- [ ] **Step 4: Commit CI enforcement**

```bash
git add .github/workflows/handoff-contracts.yml
git commit -m "ci: enforce ROWEB handoff contracts"
```

---

## Final Verification Gate

- [ ] Install from a clean Python environment:

```bash
python -m venv .venv-handoff
. .venv-handoff/bin/activate  # PowerShell: .venv-handoff\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-handoff.txt
```

- [ ] Run all plan tests:

```bash
python -m pytest tests/contracts tests/handoff -v
```

Expected: all tests PASS with no skipped tests.

- [ ] Run the aggregate validator:

```bash
python -m tools.validation.validate_handoff
```

Expected: `handoff validation passed`.

- [ ] Check forbidden asset extensions are absent from the change set:

```bash
git diff --name-only main...HEAD | python -c "import sys; bad={'.grf','.rsw','.gnd','.gat','.rsm','.rsm2','.spr','.act','.pal','.str'}; files=[p.strip() for p in sys.stdin if p.strip()]; hits=[p for p in files if any(p.lower().endswith(ext) for ext in bad)]; assert not hits, f'Forbidden asset files: {hits}'; print('asset boundary passed')"
```

Expected: `asset boundary passed`.

- [ ] Confirm no Unity runtime files were introduced:

```bash
git diff --name-only main...HEAD | python -c "import sys; files=[p.strip().lower() for p in sys.stdin if p.strip()]; hits=[p for p in files if p.endswith(('.unity','.prefab','.asset','.asmdef')) or '/unityclient/' in p or p.startswith('clients/roweb-unity/')]; assert not hits, f'Unity runtime files introduced: {hits}'; print('unity deferral passed')"
```

Expected: `unity deferral passed`.

- [ ] Review commits: each task has one focused commit, no unrelated files, and no licensed assets or secrets.

## Execution Order and Pull Request Boundaries

Implement as three reviewable pull requests after the design PR is merged:

1. **PR-H1 Governance and source pins** — Tasks 1-2.
2. **PR-H2 Shared contracts and fixtures** — Tasks 3-6.
3. **PR-H3 Validation, onboarding, and CI** — Tasks 7-9.

Do not combine these with current roBrowser runtime changes. The three PRs may be executed while roBrowser work continues because they do not introduce Unity runtime code or alter gameplay behavior.
