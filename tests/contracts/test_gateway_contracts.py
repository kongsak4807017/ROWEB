import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[2]


def load(name: str) -> dict:
    return json.loads((ROOT / "contracts" / name).read_text(encoding="utf-8"))


def test_launch_ticket_contains_no_password_field() -> None:
    ticket = {
        "schema_version": 1,
        "ticket_id": "11111111-1111-4111-8111-111111111111",
        "issued_at": "2026-08-01T09:00:00Z",
        "expires_at": "2026-08-01T09:01:00Z",
        "audience": "roweb-wss-gateway",
        "client_type": "robrowser",
        "session_correlation_id": "22222222-2222-4222-8222-222222222222",
        "nonce": "0123456789abcdef0123456789abcdef",
        "compatibility_profile": "ROWEB_CLASSIC_PRE_RE_V1",
    }
    Draft202012Validator(load("launch-ticket.schema.json")).validate(ticket)
    ticket["password"] = "must-not-be-accepted"
    with pytest.raises(ValidationError):
        Draft202012Validator(load("launch-ticket.schema.json")).validate(ticket)


def test_gateway_session_supports_both_client_types() -> None:
    schema = load("gateway-session.schema.json")
    for client_type in ("robrowser", "unity"):
        Draft202012Validator(schema).validate({
            "schema_version": 1,
            "session_id": "33333333-3333-4333-8333-333333333333",
            "session_correlation_id": "22222222-2222-4222-8222-222222222222",
            "client_type": client_type,
            "state": "ticket-validated",
            "connected_at": "2026-08-01T09:00:01Z",
        })


def test_gateway_error_uses_bounded_error_codes() -> None:
    value = {
        "schema_version": 1,
        "error_code": "ticket.replayed",
        "message": "Launch ticket has already been consumed.",
        "retryable": False,
        "occurred_at": "2026-08-01T09:00:02Z",
        "session_correlation_id": "22222222-2222-4222-8222-222222222222",
    }
    Draft202012Validator(load("gateway-error.schema.json")).validate(value)
    value["error_code"] = "internal.stack.trace"
    with pytest.raises(ValidationError):
        Draft202012Validator(load("gateway-error.schema.json")).validate(value)
