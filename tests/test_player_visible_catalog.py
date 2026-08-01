import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "tools" / "player-ui" / "build_player_visible_catalog.py"
STUDIO = Path(__file__).parents[1] / "apps" / "admin-studio" / "mockup" / "player-visible-content-studio.html"


def run_scan(tmp_path, profile="player-visible", item_source=None, use_legacy=False):
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
    (ui / "Inventory.css").write_text(".window{background-image:url('basic_interface/window_bg.bmp')}", encoding="utf-8")
    (ui / "Inventory.html").write_text('<button data-background="basic_interface/window_bg.bmp"></button>', encoding="utf-8")

    system = assets / "System"
    system.mkdir(parents=True)
    if use_legacy:
        (assets / "idnum2itemdisplaynametable.txt").write_text("501#Red Potion#\n", encoding="utf-8")
        (assets / "idnum2itemresnametable.txt").write_text("501#item_501#\n", encoding="utf-8")
        (assets / "idnum2itemdesctable.txt").write_text("501#Restores HP\\nFor players#\n", encoding="utf-8")
        (assets / "itemslotcounttable.txt").write_text("501#0#\n", encoding="utf-8")
    else:
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
    (assets / "msgstringtable.txt").write_text("Welcome to ROWEB\nSecond line", encoding="utf-8")

    subprocess.run([sys.executable, str(SCRIPT), "--source", str(src), "--assets", str(assets), "--out", str(out), "--profile", profile], check=True)
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


def test_legacy_item_tables_are_used_when_iteminfo_is_absent(tmp_path):
    data = run_scan(tmp_path, "items", use_legacy=True)
    assert data["stats"]["items"] == 1
    assert data["items"][0]["identifiedName"] == "Red Potion"
    assert data["items"][0]["identifiedDescription"] == ["Restores HP", "For players"]
    assert data["items"][0]["sourceFormat"] == "legacy-text-tables"
    assert data["scan"]["legacyItemTables"]["name"].endswith("idnum2itemdisplaynametable.txt")


def test_player_text_rows_include_preview(tmp_path):
    data = run_scan(tmp_path, "text")
    assert "Welcome to ROWEB" in data["playerTexts"][0]["preview"]


def test_studio_has_square_previews_and_file_actions():
    html = STUDIO.read_text(encoding="utf-8")
    assert "object-fit:contain" in html
    assert "/asset?path=" in html
    assert 'data-action="reveal"' in html
    assert 'data-action="open"' in html


def test_catalog_reports_item_source_candidates(tmp_path):
    data = run_scan(tmp_path)
    assert data["scan"]["itemInfoCandidates"] >= 1
    assert data["scan"]["uiSourceFilesScanned"] >= 3
