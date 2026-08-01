import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "tools" / "player-ui" / "build_player_visible_catalog.py"


def run_scan(tmp_path, profile="player-visible", item_source=None):
    src = tmp_path / "src"
    assets = tmp_path / "assets"
    out = tmp_path / "out"
    ui = src / "UI" / "Components" / "Inventory"
    ui.mkdir(parents=True)
    (ui / "Inventory.js").write_text(
        "Client.loadFile(`${DB.INTERFACE_PATH}item/item_501.bmp`, cb);\n"
        "Client.loadFile(DB.INTERFACE_PATH + 'basic_interface/window_bg.bmp', cb);\n",
        encoding="utf-8",
    )
    (ui / "Inventory.css").write_text(
        ".window{background-image:url('basic_interface/window_bg.bmp')}", encoding="utf-8"
    )
    (ui / "Inventory.html").write_text(
        '<button data-background="basic_interface/window_bg.bmp"></button>', encoding="utf-8"
    )

    system = assets / "System"
    system.mkdir(parents=True)
    if item_source is None:
        item_source = '''tbl = {
  [501] = {
    unidentifiedDisplayName = "Potion",
    unidentifiedResourceName = "item_501",
    identifiedDisplayName = "Red Potion",
    identifiedResourceName = "item_501",
    identifiedDescriptionName = {
      "Restores HP",
      "For players"
    },
    slotCount = 0,
    ClassNum = 0,
  },
}
'''
    (system / "itemInfo.lua").write_text(item_source, encoding="utf-8")

    item_dir = assets / "texture" / "À¯ÀúÀÎÅÍÆäÀÌ½º" / "item"
    item_dir.mkdir(parents=True)
    (item_dir / "item_501.bmp").write_bytes(b"BM")
    basic = assets / "texture" / "À¯ÀúÀÎÅÍÆäÀÌ½º" / "basic_interface"
    basic.mkdir(parents=True)
    (basic / "window_bg.bmp").write_bytes(b"BM")
    (assets / "msgstringtable.txt").write_text("Welcome to ROWEB", encoding="utf-8")

    subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--source",
            str(src),
            "--assets",
            str(assets),
            "--out",
            str(out),
            "--profile",
            profile,
        ],
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


def test_ui_profile_extracts_template_concat_css_and_html_references(tmp_path):
    data = run_scan(tmp_path, "ui")
    assert data["items"] == []
    assert data["playerTexts"] == []
    expressions = {row["expression"] for row in data["uiImages"]}
    assert "item/item_501.bmp" in expressions
    assert "basic_interface/window_bg.bmp" in expressions
    assert any(row["status"] == "matched" for row in data["uiImages"])
    assert data["scan"]["fullAssetWalk"] is False


def test_item_parser_handles_compact_table_and_trailing_commas(tmp_path):
    compact = '''tbl={[502]={identifiedDisplayName="Blue Potion",identifiedResourceName="item_501",identifiedDescriptionName={"Restores SP","Blue"},slotCount=0,ClassNum=0,},}'''
    data = run_scan(tmp_path, "items", compact)
    assert data["items"][0]["itemId"] == 502
    assert data["items"][0]["identifiedName"] == "Blue Potion"
    assert data["items"][0]["identifiedDescription"] == ["Restores SP", "Blue"]


def test_catalog_reports_item_source_candidates(tmp_path):
    data = run_scan(tmp_path)
    assert data["scan"]["itemInfoCandidates"] >= 1
    assert data["scan"]["uiSourceFilesScanned"] >= 3
