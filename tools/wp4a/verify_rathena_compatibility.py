#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any


class CompatibilityError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CompatibilityError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _run(*args: str, cwd: Path) -> str:
    return subprocess.run(args, cwd=cwd, check=True, text=True, capture_output=True).stdout.strip()


def _source_define(path: Path, name: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"^\s*#define\s+{re.escape(name)}(?:\s+([^\s/]+))?", text, re.MULTILINE)
    require(match is not None, f"source define missing: {name}")
    return match.group(1) or ""


def _config_integer(path: Path, name: str) -> int:
    match = re.search(rf"^{re.escape(name)}:\s*(\d+)\s*$", path.read_text(encoding="utf-8"), re.MULTILINE)
    require(match is not None, f"runtime config missing: {name}")
    return int(match.group(1))


def collect_observed(rathena: Path) -> dict[str, Any]:
    cache = (rathena / "build/ragnarok-web-smoke/CMakeCache.txt").read_text(encoding="utf-8")
    cache_packetver = re.search(r"^PACKETVER:STRING=(\d+)$", cache, re.MULTILINE)
    require(cache_packetver is not None, "CMake PACKETVER evidence missing")
    import_config = (rathena / "conf/import/inter_conf.txt").read_text(encoding="utf-8")
    packetver_source = int(_source_define(rathena / "src/config/packets.hpp", "PACKETVER"))
    shuffle = (rathena / "src/map/clif_shuffle.hpp").read_text(encoding="utf-8")
    return {
        "commit": _run("git", "rev-parse", "HEAD", cwd=rathena),
        "tracked_clean": _run("git", "status", "--porcelain=v1", cwd=rathena) == "",
        "packetver_source": packetver_source,
        "packetver_build": int(cache_packetver.group(1)),
        "client_family": "RagexeRE" if 20200902 <= packetver_source <= 20211118 else "unsupported",
        "packet_shuffle_active": packetver_source <= 20180307,
        "map_connection_rule": bool(
            re.search(
                r"parseable_packet\(\s*0x0436,\s*23,\s*clif_parse_WantToConnection,\s*2,\s*6,\s*10,\s*14,\s*22\s*\)",
                shuffle,
            )
        ),
        "renewal": _source_define(rathena / "src/config/renewal.hpp", "RENEWAL") == "",
        "binary_sha256": {
            name: sha256(rathena / name)
            for name in ("login-server", "char-server", "map-server")
        },
        "ports": {
            "login": _config_integer(rathena / "conf/import/login_conf.txt", "login_port"),
            "character": _config_integer(rathena / "conf/import/char_conf.txt", "char_port"),
            "map": _config_integer(rathena / "conf/import/map_conf.txt", "map_port"),
        },
        "utf8mb4": all(
            re.search(rf"^{key}:\s*utf8mb4\s*$", import_config, re.MULTILINE)
            for key in ("login_codepage", "ipban_codepage", "log_codepage")
        ),
        "web_auth_token": bool(
            re.search(
                r"^use_web_auth_token:\s*yes\s*$",
                (rathena / "conf/login_athena.conf").read_text(encoding="utf-8"),
                re.MULTILINE,
            )
        ),
        "zero_obfuscation_rule": "packet_keys(0x00000000,0x00000000,0x00000000)"
        in (rathena / "src/map/clif_obfuscation.hpp").read_text(encoding="utf-8"),
    }


def validate_contract(
    profile: dict[str, Any],
    evidence: dict[str, Any],
    observed: dict[str, Any],
    environment: dict[str, str],
) -> None:
    require(profile.get("schema") == "roweb-rathena-compatibility/v1", "compatibility profile schema mismatch")
    require(profile.get("risk_id") == "R-COMPAT-001", "compatibility risk ID mismatch")
    require(profile.get("status") == "VERIFIED_CLOSED", "compatibility profile is not VERIFIED_CLOSED")
    runtime_smoke = profile.get("runtime_smoke", {})
    require(
        runtime_smoke.get("result") == "PASS_RATHENA_AUTHORITATIVE_COMPATIBILITY_SMOKE",
        "runtime smoke profile result mismatch",
    )
    require(runtime_smoke.get("running_binary_identity_required") is True, "runtime binary identity is not required")
    require(runtime_smoke.get("cleanup_required") is True, "runtime cleanup is not required")

    bypass_names = profile["bypass"]["prohibited_environment_variables"]
    enabled = [
        name
        for name in bypass_names
        if environment.get(name, "").strip().lower() not in ("", "0", "false", "no")
    ]
    require(not enabled, f"compatibility bypass enabled: {', '.join(enabled)}")
    require(profile["bypass"]["force_allowed"] is False, "FORCE must remain forbidden")
    require(profile["bypass"]["compatibility_bypass_allowed"] is False, "compatibility bypass must remain forbidden")

    approved = profile["canonical_source"]["commit"]
    require(observed["commit"] == approved, "authoritative commit mismatch")
    require(observed["tracked_clean"] is True, "authoritative tracked worktree is dirty")
    require(profile["protocol"]["packetver"] == observed["packetver_source"], "source PACKETVER mismatch")
    require(profile["build"]["packetver"] == observed["packetver_build"], "binary build PACKETVER mismatch")
    require(observed["packetver_source"] == observed["packetver_build"], "source/build PACKETVER mismatch")
    require(profile["protocol"]["client_family"] == observed["client_family"], "client family mismatch")
    require(profile["protocol"]["gameplay_mode"] == "Renewal" and observed["renewal"], "Renewal mode mismatch")
    obfuscation = profile["protocol"]["packet_obfuscation"]
    require(obfuscation["active"] is False, "packet obfuscation state mismatch")
    require(obfuscation["keys"] == ["0x00000000"] * 3, "packet obfuscation keys mismatch")
    require(observed["zero_obfuscation_rule"], "zero-key source rule missing")
    require(profile["protocol"]["packet_shuffle_active"] == observed["packet_shuffle_active"], "packet shuffle mismatch")
    map_connection = profile["protocol"]["map_connection_packet"]
    require(
        map_connection
        == {
            "id": "0x0436",
            "length": 23,
            "parser": "clif_parse_WantToConnection",
            "field_offsets": [2, 6, 10, 14, 22],
        },
        "map connection packet mismatch",
    )
    require(observed["map_connection_rule"], "map connection packet source rule missing")
    require(profile["protocol"]["ports"]["login"] == observed["ports"]["login"], "login port mismatch")
    require(profile["protocol"]["ports"]["character"] == observed["ports"]["character"], "character port mismatch")
    require(profile["protocol"]["ports"]["map"] == observed["ports"]["map"], "map port mismatch")
    require(observed["utf8mb4"], "runtime database codepage mismatch")
    require(observed["web_auth_token"], "web-auth-token configuration mismatch")

    require(evidence.get("schema") == "roweb-rathena-binary-provenance/v1", "binary provenance evidence missing")
    require(evidence.get("source_commit") == approved, "binary provenance commit mismatch")
    require(evidence.get("clean_rebuild_exit_code") == 0, "controlled clean rebuild was not demonstrated")
    require(evidence.get("runtime_smoke_exit_code") == 0, "runtime smoke was not demonstrated")
    require(evidence.get("runtime_smoke_force_or_bypass_used") is False, "runtime smoke used a bypass")
    require(evidence.get("force_or_bypass_used") is False, "binary provenance used a bypass")
    require(evidence.get("tracked_source_clean") is True, "binary provenance source was dirty")
    binaries = evidence.get("binaries")
    require(isinstance(binaries, dict), "binary provenance records missing")
    for name, expected in profile["build"]["binaries"].items():
        record = binaries.get(name)
        require(isinstance(record, dict), f"binary provenance missing: {name}")
        require(record.get("pre_rebuild_sha256") == expected["sha256"], f"pre-rebuild hash mismatch: {name}")
        require(record.get("post_rebuild_sha256") == expected["sha256"], f"post-rebuild hash mismatch: {name}")
        require(record.get("runtime_smoke_sha256") == expected["sha256"], f"runtime-smoke hash mismatch: {name}")
        require(record.get("byte_identical") is True, f"binary was not reproducible: {name}")
        require(record.get("elf_build_id") == expected["elf_build_id"], f"ELF BuildID mismatch: {name}")
        require(observed["binary_sha256"][name] == expected["sha256"], f"current binary provenance mismatch: {name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--rathena", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    try:
        profile = json.loads(args.profile.read_text(encoding="utf-8"))
        evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
        validate_contract(profile, evidence, collect_observed(args.rathena), dict(os.environ))
    except (CompatibilityError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"FAIL_RATHENA_AUTHORITATIVE_COMPATIBILITY: {exc}")
        return 1
    print("PASS_RATHENA_AUTHORITATIVE_COMPATIBILITY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
