import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[2]
LOCK = json.loads((ROOT / "compatibility.lock.json").read_text(encoding="utf-8"))
SCHEMA = json.loads((ROOT / "contracts/compatibility-profile.schema.json").read_text(encoding="utf-8"))


def profile() -> dict:
    packetver = LOCK["server"]["packetver"]
    return {
        "schema_version": 1,
        "profile_id": "ROWEB_CLASSIC_PRE_RE_V1",
        "server": {
            "repository": "kongsak4807017/rathena",
            "commit": LOCK["server"]["commit"],
            "gameplay_mode": LOCK["server"]["profile"],
        },
        "protocol": {
            "packetver_status": packetver["status"],
            "packetver": packetver["value"],
            "client_family": "unknown",
            "packet_obfuscation": None,
            "encoding": "cp949-utf8-bridge",
        },
        "clients": {
            "robrowser": {"supported": True, "conformance_level": "production"},
            "unity": {"supported": False, "conformance_level": "planned"},
        },
    }


def test_pending_profile_matches_schema() -> None:
    Draft202012Validator(SCHEMA).validate(profile())


def test_verified_profile_requires_integer_packetver() -> None:
    value = profile()
    value["protocol"]["packetver_status"] = "verified"
    with pytest.raises(ValidationError):
        Draft202012Validator(SCHEMA).validate(value)


def test_server_commit_matches_lock() -> None:
    assert profile()["server"]["commit"] == LOCK["server"]["commit"]
