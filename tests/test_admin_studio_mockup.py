from pathlib import Path
import re

ROOT = Path(__file__).parents[1] / "apps" / "admin-studio" / "mockup"
HTML = ROOT / "index.html"


def test_mockup_file_exists():
    assert HTML.is_file()


def test_mockup_declares_simulated_read_only_boundary():
    html = HTML.read_text(encoding="utf-8")
    assert "SIMULATED DATA" in html
    assert "read-only" in html
    assert "dry-run" in html


def test_navigation_targets_have_matching_views():
    html = HTML.read_text(encoding="utf-8")
    for view in re.findall(r'data-view="([a-z-]+)"', html):
        assert f'id="{view}"' in html


def test_no_production_connection_primitives_are_present():
    html = HTML.read_text(encoding="utf-8")
    forbidden = ["fetch(", "WebSocket(", "XMLHttpRequest", "mysql.connect", "atcommand("]
    for token in forbidden:
        assert token not in html
