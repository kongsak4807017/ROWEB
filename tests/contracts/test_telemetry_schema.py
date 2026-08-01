import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / "contracts/telemetry-event.schema.json").read_text(encoding="utf-8"))


def event() -> dict:
    return {
        "schema_version": 1,
        "event_type": "map.load.completed",
        "occurred_at": "2026-08-01T09:00:00Z",
        "client_type": "robrowser",
        "client_version": "0.1.0",
        "compatibility_profile": "ROWEB_CLASSIC_PRE_RE_V1",
        "session_correlation_id": "22222222-2222-4222-8222-222222222222",
        "device_profile": {
            "platform": "Windows",
            "browser_family": "Chromium",
            "memory_class_mb": 8192,
        },
        "measurements": {"duration_ms": 1234.5, "cache_hit": True},
    }


def test_telemetry_supports_both_clients() -> None:
    for client_type in ("robrowser", "unity"):
        value = event()
        value["client_type"] = client_type
        Draft202012Validator(SCHEMA).validate(value)


def test_secret_fields_are_rejected() -> None:
    value = event()
    value["password"] = "secret"
    with pytest.raises(ValidationError):
        Draft202012Validator(SCHEMA).validate(value)


def test_unknown_event_type_is_rejected() -> None:
    value = event()
    value["event_type"] = "player.private-chat.captured"
    with pytest.raises(ValidationError):
        Draft202012Validator(SCHEMA).validate(value)
