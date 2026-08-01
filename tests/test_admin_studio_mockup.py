from pathlib import Path
import re

ROOT = Path(__file__).parents[1] / "apps" / "admin-studio" / "mockup"
ENTRY_HTML = ROOT / "index.html"
WORKBENCH_HTML = ROOT / "unified-workbench.html"


def test_mockup_files_exist():
    assert ENTRY_HTML.is_file()
    assert WORKBENCH_HTML.is_file()


def test_entrypoint_redirects_to_unified_workbench():
    html = ENTRY_HTML.read_text(encoding="utf-8")
    assert "unified-workbench.html" in html


def test_mockup_declares_simulated_read_only_boundary():
    html = WORKBENCH_HTML.read_text(encoding="utf-8")
    assert "SIMULATED DATA" in html
    assert "localStorage" in html
    assert "No rAthena, MariaDB, roBrowserLegacy, or private-asset mutation occurs." in html


def test_navigation_targets_have_matching_views():
    html = WORKBENCH_HTML.read_text(encoding="utf-8")
    for view in re.findall(r'data-view="([a-z-]+)"', html):
        assert f'id="{view}"' in html


def test_only_local_profile_fetch_is_present():
    html = WORKBENCH_HTML.read_text(encoding="utf-8")
    fetch_targets = re.findall(r"fetch\(\s*['\"]([^'\"]+)['\"]", html)
    assert fetch_targets == ["player-ui-profiles.json"]


def test_no_production_connection_primitives_are_present():
    html = WORKBENCH_HTML.read_text(encoding="utf-8")
    forbidden = [
        "WebSocket(",
        "XMLHttpRequest",
        "mysql.connect",
        "atcommand(",
        "fetch('http",
        'fetch("http',
        "fetch('//",
        'fetch("//',
    ]
    for token in forbidden:
        assert token not in html
