import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_source_registry_matches_schema() -> None:
    schema = load_json("contracts/source-registry.schema.json")
    registry = yaml.safe_load(
        (ROOT / "research/source-registry.yaml").read_text(encoding="utf-8")
    )
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(registry)


def test_production_source_shas_match_compatibility_lock() -> None:
    lock = load_json("compatibility.lock.json")
    registry = yaml.safe_load(
        (ROOT / "research/source-registry.yaml").read_text(encoding="utf-8")
    )
    by_id = {item["id"]: item for item in registry["sources"]}

    assert by_id["robrowser-legacy"]["ref"] == lock["client"]["commit"]
    assert by_id["rathena"]["ref"] == lock["server"]["commit"]
    assert by_id["robrowser-legacy"]["production_dependency"] is True
    assert by_id["rathena"]["production_dependency"] is True
    assert by_id["unityro"]["production_dependency"] is False
    assert by_id["ragnarok-rebuild-tcp"]["production_dependency"] is False
