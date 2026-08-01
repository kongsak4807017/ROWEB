import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / "contracts/domain-event.schema.json").read_text(encoding="utf-8"))


def event() -> dict:
    return {
        "schema_version": 1,
        "event_id": "11111111-1111-4111-8111-111111111111",
        "event_type": "world.entity.spawned",
        "occurred_at": "2026-08-01T09:00:00Z",
        "session_correlation_id": "22222222-2222-4222-8222-222222222222",
        "sequence": 12,
        "payload": {"entity_id": 1001, "entity_type": "player"},
    }


def test_known_event_passes() -> None:
    Draft202012Validator(SCHEMA).validate(event())


def test_unknown_event_type_fails() -> None:
    value = event()
    value["event_type"] = "packet.0x9999.received"
    with pytest.raises(ValidationError):
        Draft202012Validator(SCHEMA).validate(value)


def test_transport_fields_are_not_allowed_at_root() -> None:
    value = event()
    value["packet_id"] = "0x09ff"
    with pytest.raises(ValidationError):
        Draft202012Validator(SCHEMA).validate(value)
