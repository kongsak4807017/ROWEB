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
        "schema_version": 1,
        "asset_id": "map.prontera.world",
        "asset_type": "map",
        "source": {
            "rsw": "data/prontera.rsw",
            "gnd": "data/prontera.gnd",
            "gat": "data/prontera.gat",
        },
        "dependencies": ["texture.prontera.*", "model.prontera.*"],
        "targets": {
            "robrowser": {"runtime_path": "data/prontera.rsw"},
            "unity": {
                "addressable_key": "maps/prontera",
                "conversion_profile": "ro-map-v1",
            },
        },
    }


def test_valid_engine_neutral_asset_passes() -> None:
    validator().validate(valid_asset())


def test_robrowser_target_is_required() -> None:
    value = valid_asset()
    del value["targets"]["robrowser"]
    with pytest.raises(ValidationError):
        validator().validate(value)


def test_target_specific_fields_do_not_leak_to_root() -> None:
    value = valid_asset()
    value["runtime_path"] = "data/prontera.rsw"
    with pytest.raises(ValidationError):
        validator().validate(value)
