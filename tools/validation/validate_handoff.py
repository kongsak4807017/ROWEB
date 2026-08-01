from __future__ import annotations

import json
from pathlib import Path

from tools.validation.common import ROOT, read_json, read_yaml, validate_instance

ADR_FILES = [
    "ADR-020-client-product-strategy.md",
    "ADR-021-rathena-authority.md",
    "ADR-022-dual-client-contract-boundary.md",
    "ADR-023-engine-neutral-asset-catalog.md",
    "ADR-024-reference-source-and-license-policy.md",
    "ADR-025-unity-start-gate.md",
]
REQUIRED_ADR_HEADINGS = [
    "## Context",
    "## Decision",
    "## Alternatives considered",
    "## Consequences",
    "## Reversal conditions",
    "## Evidence",
    "## Owner",
]


def validate_adrs() -> None:
    for filename in ADR_FILES:
        path = ROOT / "docs" / "adr" / filename
        if not path.is_file():
            raise FileNotFoundError(path)
        content = path.read_text(encoding="utf-8")
        for heading in REQUIRED_ADR_HEADINGS:
            if heading not in content:
                raise ValueError(f"{filename} missing {heading}")


def validate_registry() -> None:
    validate_instance(
        read_yaml(ROOT / "research" / "source-registry.yaml"),
        ROOT / "contracts" / "source-registry.schema.json",
    )
    lock = read_json(ROOT / "compatibility.lock.json")
    registry = read_yaml(ROOT / "research" / "source-registry.yaml")
    by_id = {source["id"]: source for source in registry["sources"]}
    if by_id["robrowser-legacy"]["ref"] != lock["client"]["commit"]:
        raise ValueError("roBrowser source pin does not match compatibility.lock.json")
    if by_id["rathena"]["ref"] != lock["server"]["commit"]:
        raise ValueError("rAthena source pin does not match compatibility.lock.json")


def validate_schemas() -> None:
    for path in sorted((ROOT / "contracts").glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        from jsonschema import Draft202012Validator

        Draft202012Validator.check_schema(schema)


def validate_synthetic_fixtures() -> None:
    schema_path = ROOT / "contracts" / "protocol-fixture.schema.json"
    for path in sorted((ROOT / "protocol" / "fixtures" / "synthetic").glob("*.json")):
        validate_instance(read_json(path), schema_path)


def validate_start_here() -> None:
    path = ROOT / "docs" / "handoff" / "START_HERE.md"
    if not path.is_file():
        raise FileNotFoundError(path)
    content = path.read_text(encoding="utf-8")
    required = [
        "compatibility.lock.json",
        "research/source-registry.yaml",
        "docs/adr/ADR-020-client-product-strategy.md",
        "python -m pytest tests/contracts tests/handoff -v",
        "python -m tools.validation.validate_handoff",
    ]
    for value in required:
        if value not in content:
            raise ValueError(f"START_HERE.md missing required reference: {value}")


def main() -> int:
    checks = [
        ("ADRs", validate_adrs),
        ("source registry", validate_registry),
        ("JSON schemas", validate_schemas),
        ("synthetic fixtures", validate_synthetic_fixtures),
        ("handoff entrypoint", validate_start_here),
    ]
    for name, check in checks:
        check()
        print(f"PASS {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
