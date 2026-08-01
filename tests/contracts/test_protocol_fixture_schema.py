import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / "contracts/protocol-fixture.schema.json").read_text(encoding="utf-8"))
EXAMPLE = json.loads((ROOT / "protocol/fixtures/synthetic/login-accepted.example.json").read_text(encoding="utf-8"))


def test_synthetic_fixture_matches_schema() -> None:
    Draft202012Validator(SCHEMA).validate(EXAMPLE)


def test_fixture_must_be_marked_synthetic() -> None:
    value = dict(EXAMPLE)
    value["synthetic"] = False
    with pytest.raises(ValidationError):
        Draft202012Validator(SCHEMA).validate(value)


def test_raw_hex_rejects_non_hex_content() -> None:
    value = dict(EXAMPLE)
    value["raw_hex"] = "password=secret"
    with pytest.raises(ValidationError):
        Draft202012Validator(SCHEMA).validate(value)


def test_fixture_contains_no_forbidden_keys() -> None:
    forbidden = {"password", "launch_ticket", "session_secret", "private_chat", "email"}
    assert forbidden.isdisjoint(EXAMPLE)
