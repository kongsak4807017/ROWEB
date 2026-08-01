import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
START_HERE = ROOT / "docs/handoff/START_HERE.md"


def test_start_here_exists_and_names_required_commands() -> None:
    content = START_HERE.read_text(encoding="utf-8")
    assert "python -m tools.validation.validate_handoff" in content
    assert "python -m pytest tests/contracts tests/handoff -v" in content
    assert "Do not start a Unity client" in content


def test_backtick_repository_paths_exist() -> None:
    content = START_HERE.read_text(encoding="utf-8")
    candidates = set(re.findall(r"`((?:docs|research|contracts|protocol)/[^`]+|compatibility\.lock\.json|AGENTS\.md|README\.md)`", content))
    missing = [value for value in sorted(candidates) if not (ROOT / value).exists()]
    assert not missing, f"missing referenced repository paths: {missing}"


def test_start_here_identifies_authoritative_repositories() -> None:
    content = START_HERE.read_text(encoding="utf-8")
    for repository in (
        "kongsak4807017/ROWEB",
        "kongsak4807017/roBrowserLegacy",
        "kongsak4807017/rathena",
        "kongsak4807017/unityro",
        "kongsak4807017/RagnarokRebuildTcp",
    ):
        assert repository in content
