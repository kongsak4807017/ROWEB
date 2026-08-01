import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_validate_handoff_cli_passes() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "tools.validation.validate_handoff"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS ADRs" in result.stdout
    assert "PASS source registry" in result.stdout
    assert "PASS JSON schemas" in result.stdout
    assert "PASS synthetic fixtures" in result.stdout
    assert "PASS handoff entrypoint" in result.stdout


def test_json_validator_rejects_repository_escape() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "tools.validation.validate_json", "../outside.json", "contracts/domain-event.schema.json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "path escapes repository root" in result.stderr
