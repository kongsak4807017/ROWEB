from pathlib import Path
import json
import re
import shutil
import subprocess

ROOT = Path(__file__).parents[1]
HTML = ROOT / "apps" / "admin-studio" / "mockup" / "unified-workbench.html"
PROFILE = ROOT / "apps" / "admin-studio" / "mockup" / "player-ui-profiles.json"
INDEX = ROOT / "apps" / "admin-studio" / "mockup" / "index.html"


def test_unified_workbench_contains_required_views():
    text = HTML.read_text(encoding="utf-8")
    for view in [
        "command",
        "players",
        "economy",
        "security",
        "player-ui",
        "mobile-controls",
        "releases",
        "audit",
    ]:
        assert f'data-view="{view}"' in text
        assert f'id="{view}"' in text


def test_existing_admin_studio_capabilities_are_preserved():
    text = HTML.read_text(encoding="utf-8")
    for label in [
        "Command Center",
        "Player Operations",
        "Economy Studio",
        "Anti-abuse",
        "Unified Audit",
    ]:
        assert label in text


def test_player_experience_editor_controls_exist():
    text = HTML.read_text(encoding="utf-8")
    for element_id in [
        "scene",
        "device",
        "episode",
        "propX",
        "propY",
        "propWidth",
        "propScale",
        "propOpacity",
        "propAnchor",
        "propVisible",
        "virtualJoystick",
        "mobileActionButtons",
    ]:
        assert f'id="{element_id}"' in text
    for device in ["desktop-v1", "mobile-landscape-v1", "mobile-portrait-v1"]:
        assert device in text


def test_profile_json_has_all_device_profiles_and_runtime_bindings():
    data = json.loads(PROFILE.read_text(encoding="utf-8"))
    assert data["schemaVersion"] == 1
    assert set(data["profiles"]) == {
        "desktop-v1",
        "mobile-landscape-v1",
        "mobile-portrait-v1",
    }
    for profile in data["profiles"].values():
        assert profile["safeArea"] is True
        assert profile["touchTarget"] >= 44
        assert "basicInfo" in profile["components"]
        assert "miniMap" in profile["components"]
    assert data["bindings"]["attackButton"] == "attackSelectedTarget"
    assert data["validation"]["damageMissBinding"]
    assert data["validation"]["attackSoundBinding"]
    assert data["validation"]["itemInfoSource"]


def test_release_and_audit_workflow_is_present():
    text = HTML.read_text(encoding="utf-8")
    for function in [
        "function saveDraft(",
        "function validate(",
        "function publish(",
        "function rollback(",
        "function appendAudit(",
    ]:
        assert function in text
    assert "localStorage" in text
    assert "Publish ถูกบล็อก" in text


def test_safe_static_boundary_remains_explicit():
    text = HTML.read_text(encoding="utf-8")
    assert "SIMULATED DATA" in text
    assert "No rAthena, MariaDB, roBrowserLegacy, or private-asset mutation occurs" in text
    assert "WebSocket(" not in text
    assert "XMLHttpRequest" not in text
    assert "SELECT " not in text
    assert "atcommand" not in text.lower()


def test_embedded_javascript_has_valid_syntax(tmp_path):
    if not shutil.which("node"):
        return
    text = HTML.read_text(encoding="utf-8")
    scripts = re.findall(r"<script>(.*?)</script>", text, re.S)
    assert scripts
    js = tmp_path / "unified-workbench.js"
    js.write_text(scripts[-1], encoding="utf-8")
    subprocess.run(["node", "--check", str(js)], check=True, capture_output=True, text=True)


def test_default_entry_redirects_to_unified_workbench():
    text = INDEX.read_text(encoding="utf-8")
    assert "unified-workbench.html" in text
