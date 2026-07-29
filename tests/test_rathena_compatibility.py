import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "wp4a" / "verify_rathena_compatibility.py"
SPEC = importlib.util.spec_from_file_location("verify_rathena_compatibility", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

COMMIT = "0c3ca757ad35fff003130a8441a10f27cccd0ed9"
HASHES = {"login-server": "a" * 64, "char-server": "b" * 64, "map-server": "c" * 64}


def contract():
    profile = {
        "schema": "roweb-rathena-compatibility/v1",
        "risk_id": "R-COMPAT-001",
        "status": "VERIFIED_CLOSED",
        "runtime_smoke": {
            "result": "PASS_RATHENA_AUTHORITATIVE_COMPATIBILITY_SMOKE",
            "running_binary_identity_required": True,
            "cleanup_required": True,
        },
        "canonical_source": {"commit": COMMIT},
        "build": {
            "packetver": 20211103,
            "binaries": {
                name: {"sha256": digest, "elf_build_id": name + "-build-id"}
                for name, digest in HASHES.items()
            },
        },
        "protocol": {
            "packetver": 20211103,
            "client_family": "RagexeRE",
            "gameplay_mode": "Renewal",
            "packet_shuffle_active": False,
            "map_connection_packet": {
                "id": "0x0436",
                "length": 23,
                "parser": "clif_parse_WantToConnection",
                "field_offsets": [2, 6, 10, 14, 22],
            },
            "packet_obfuscation": {"active": False, "keys": ["0x00000000"] * 3},
            "ports": {"login": 6900, "character": 6121, "map": 5121},
        },
        "bypass": {
            "force_allowed": False,
            "compatibility_bypass_allowed": False,
            "prohibited_environment_variables": ["FORCE", "RATHENA_COMPATIBILITY_BYPASS"],
        },
    }
    observed = {
        "commit": COMMIT,
        "tracked_clean": True,
        "packetver_source": 20211103,
        "packetver_build": 20211103,
        "client_family": "RagexeRE",
        "packet_shuffle_active": False,
        "map_connection_rule": True,
        "renewal": True,
        "binary_sha256": HASHES.copy(),
        "ports": {"login": 6900, "character": 6121, "map": 5121},
        "utf8mb4": True,
        "web_auth_token": True,
        "zero_obfuscation_rule": True,
    }
    evidence = {
        "schema": "roweb-rathena-binary-provenance/v1",
        "source_commit": COMMIT,
        "clean_rebuild_exit_code": 0,
        "runtime_smoke_exit_code": 0,
        "runtime_smoke_force_or_bypass_used": False,
        "force_or_bypass_used": False,
        "tracked_source_clean": True,
        "binaries": {
            name: {
                "pre_rebuild_sha256": digest,
                "post_rebuild_sha256": digest,
                "runtime_smoke_sha256": digest,
                "byte_identical": True,
                "elf_build_id": name + "-build-id",
            }
            for name, digest in HASHES.items()
        },
    }
    return profile, evidence, observed


class CompatibilityContractTests(unittest.TestCase):
    def assert_rejected(self, mutator, pattern):
        profile, evidence, observed = contract()
        mutator(profile, evidence, observed)
        with self.assertRaisesRegex(MODULE.CompatibilityError, pattern):
            MODULE.validate_contract(profile, evidence, observed, {})

    def test_accepts_matching_authoritative_profile(self):
        MODULE.validate_contract(*contract(), {})

    def test_rejects_commit_drift(self):
        self.assert_rejected(lambda p, e, o: o.update(commit="7" * 40), "commit mismatch")

    def test_rejects_packetver_drift(self):
        self.assert_rejected(lambda p, e, o: o.update(packetver_build=20211104), "PACKETVER mismatch")

    def test_rejects_protocol_drift(self):
        self.assert_rejected(
            lambda p, e, o: p["protocol"]["packet_obfuscation"].update(active=True),
            "obfuscation state mismatch",
        )

    def test_rejects_missing_binary_provenance(self):
        self.assert_rejected(lambda p, e, o: e.update(clean_rebuild_exit_code=None), "clean rebuild")

    def test_rejects_binary_hash_drift(self):
        self.assert_rejected(
            lambda p, e, o: e["binaries"]["map-server"].update(post_rebuild_sha256="d" * 64),
            "post-rebuild hash mismatch",
        )

    def test_rejects_force_or_compatibility_bypass(self):
        profile, evidence, observed = contract()
        with self.assertRaisesRegex(MODULE.CompatibilityError, "bypass enabled"):
            MODULE.validate_contract(profile, evidence, observed, {"FORCE": "1"})
        with self.assertRaisesRegex(MODULE.CompatibilityError, "bypass enabled"):
            MODULE.validate_contract(
                profile,
                evidence,
                observed,
                {"RATHENA_COMPATIBILITY_BYPASS": "true"},
            )

    def test_rejects_profile_that_is_not_verified_closed(self):
        self.assert_rejected(
            lambda p, e, o: p.update(status="BLOCKER_NOW"),
            "not VERIFIED_CLOSED",
        )

    def test_canonical_compatibility_controls_do_not_contain_obsolete_pin(self):
        root = Path(__file__).resolve().parents[1]
        controlled = [
            root / "config" / "rathena-compatibility.json",
            root / "tools" / "wp4a" / "verify_rathena_compatibility.py",
        ]
        for path in controlled:
            self.assertNotIn("7f080871", path.read_text(encoding="utf-8"), path)


if __name__ == "__main__":
    unittest.main()
