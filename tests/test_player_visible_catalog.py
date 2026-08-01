import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "tools" / "player-ui" / "build_player_visible_catalog.py"


def run_scan(tmp_path, profile="player-visible"):
    src = tmp_path / "src"
    assets = tmp_path / "assets"
    out = tmp_path / "out"
    (src / "UI" / "Components" / "Inventory").mkdir(parents=True)
    (src / "UI" / "Components" / "Inventory" / "Inventory.js").write_text(
        "Client.loadFile(DB.INTERFACE_PATH + 'item/item_501.bmp', cb);", encoding="utf-8"
    )
    system = assets / "System"
    system.mkdir(parents=True)
    (system / "itemInfo.lua").write_text(
        'tbl = {\n[501] = {\nidentifiedDisplayName = "Red Potion",\nidentifiedResourceName = "item_501",\nidentifiedDescriptionName = { "Restores HP", "For players" },\nslotCount = 0,\nClassNum = 0\n}\n}\n',
        encoding="utf-8",
    )
    item_dir = assets / "texture" / "À¯ÀúÀÎÅÍÆäÀÌ½º" / "item"
    item_dir.mkdir(parents=True)
    (item_dir / "item_501.bmp").write_bytes(b"BM")
    (assets / "msgstringtable.txt").write_text("Welcome to ROWEB", encoding="utf-8")
    subprocess.run(
        [sys.executable, str(SCRIPT), "--source", str(src), "--assets", str(assets), "--out", str(out), "--profile", profile],
        check=True,
    )
    return json.loads((out / "player-visible-content-catalog.json").read_text(encoding="utf-8"))


def test_player_visible_profile_extracts_item_and_icon(tmp_path):
    data = run_scan(tmp_path)
    assert data["stats"]["items"] == 1
    item = data["items"][0]
    assert item["itemId"] == 501
    assert item["identifiedName"] == "Red Potion"
    assert item["identifiedDescription"] == ["Restores HP", "For players"]
    assert item["iconStatus"] == "matched"


def test_items_profile_excludes_ui_and_text(tmp_path):
    data = run_scan(tmp_path, "items")
    assert data["uiImages"] == []
    assert data["playerTexts"] == []
    assert data["items"][0]["itemId"] == 501


def test_ui_profile_scans_only_targeted_asset_roots(tmp_path):
    data = run_scan(tmp_path, "ui")
    assert data["items"] == []
    assert data["playerTexts"] == []
    assert any(row["status"] == "matched" for row in data["uiImages"])
    assert data["scan"]["fullAssetWalk"] is False
