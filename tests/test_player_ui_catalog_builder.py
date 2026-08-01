from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "tools" / "player-ui" / "build_catalog.py"
STUDIO = ROOT / "apps" / "admin-studio" / "mockup" / "player-ui-catalog-studio.html"


def test_catalog_studio_contract():
    html = STUDIO.read_text(encoding="utf-8")
    for token in [
        "Component Catalog",
        "Source Files",
        "Variants",
        "Asset Usage",
        "Dependency Inspector",
        "player-ui-catalog.json",
        "asset-usage-manifest.json",
        "Mobile Landscape",
        "Mobile Portrait",
    ]:
        assert token in html


def test_builder_scans_components_variants_and_assets(tmp_path: Path):
    src = tmp_path / "src"
    assets = tmp_path / "assets"
    out = tmp_path / "out"
    comp = src / "UI" / "Components" / "Inventory"
    variant = comp / "InventoryV1"
    variant.mkdir(parents=True)
    assets.joinpath("data", "texture", "interface", "item").mkdir(parents=True)
    assets.joinpath("data", "texture", "interface", "item", "apple.bmp").write_bytes(b"bmp")

    comp.joinpath("Inventory.js").write_text(
        "import UIVersionManager from 'UI/UIVersionManager.js';\n"
        "Client.loadFile('data/texture/interface/item/apple.bmp', data => {});\n",
        encoding="utf-8",
    )
    variant.joinpath("InventoryV1.html").write_text("<div></div>", encoding="utf-8")
    variant.joinpath("InventoryV1.css").write_text(".x{background:url('data/texture/interface/item/apple.bmp')}", encoding="utf-8")
    variant.joinpath("InventoryV1.js").write_text("export default {};", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--source", str(src), "--assets", str(assets), "--out", str(out)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr

    catalog = json.loads((out / "player-ui-catalog.json").read_text(encoding="utf-8"))
    manifest = json.loads((out / "asset-usage-manifest.json").read_text(encoding="utf-8"))
    inventory = next(c for c in catalog["components"] if c["id"] == "Inventory")

    assert inventory["usesUIVersionManager"] is True
    assert [v["name"] for v in inventory["variants"]] == ["InventoryV1"]
    assert inventory["assetSummary"]["matched"] >= 1
    assert any(r["status"] == "matched" and r["component"] == "Inventory" for r in manifest["references"])
