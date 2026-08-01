#!/usr/bin/env python3
"""Build the Catalog-driven Player UI Studio data files.

Scans a roBrowserLegacy src tree and an extracted Ragnarok asset data tree.
Outputs:
  - player-ui-catalog.json: UI components, variants, source files and dependencies
  - asset-usage-manifest.json: every detected asset reference and its resolved file

The scanner is read-only. It never modifies roBrowserLegacy or private assets.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable

TEXT_EXTS = {".js", ".html", ".css", ".json", ".lua", ".lub", ".txt"}
ASSET_EXTS = {
    ".bmp", ".png", ".jpg", ".jpeg", ".gif", ".tga", ".spr", ".act", ".wav", ".mp3",
    ".ogg", ".rsw", ".gnd", ".gat", ".rsm", ".gr2", ".str", ".pal", ".ebm", ".xml",
    ".lua", ".lub", ".txt", ".json", ".otf", ".ttf", ".webp", ".svg",
}
CATEGORY_RULES = [
    ("Boot & Session", {"Intro", "WinLogin", "PincodeWindow", "CharSelect", "CharCreate", "Error", "WinPopup", "WinPrompt"}),
    ("Main HUD", {"BasicInfo", "StatusIcons", "MiniMap", "MapName", "ChatBox", "ShortCut", "ShortCuts", "Announce", "FPS", "PvPCount", "PvPTimer", "PCGoldTimer", "EntitySignboard"}),
    ("Character", {"WinStats", "Equipment", "Inventory", "ItemInfo", "ItemCompare", "ItemPreview", "SkillList", "SkillDescription", "SwitchEquip", "CartItems", "PetInformations", "HomunInformations", "MercenaryInformations"}),
    ("Social", {"PartyFriends", "Guild", "Clan", "ChatRoom", "ChatRoomCreate", "WhisperBox", "ContextMenu", "Emoticons", "EntityRoom"}),
    ("NPC & Economy", {"NpcBox", "NpcMenu", "NpcStore", "Trade", "Vending", "VendingShop", "VendingReport", "Storage", "Bank", "CashShop", "Mail", "Rodex", "Refine", "Enchant", "ItemReform", "ItemSelection", "MakeArrowSelection", "MakeItemSelection"}),
    ("Progression", {"Quest", "Achievement", "CheckAttendance", "Reputation", "PetEvolution", "EnchantGrade", "LaphineSys", "LaphineUpg", "Roulette"}),
    ("System", {"Escape", "GraphicsOption", "SoundOption", "ShortCutOption", "ChatBoxSettings", "WorldMap", "Navigation", "WinList", "InputBox", "Captcha"}),
    ("Mobile", {"MobileUI", "JoystickUI"}),
    ("Developer Tools", {"GrfViewer", "MapViewer", "ModelViewer", "GrannyModelViewer", "StrViewer", "EffectViewer", "CardIllustration"}),
]

LOAD_PATTERNS = [
    re.compile(r"Client\.loadFile\(\s*([`'\"])(.+?)\1", re.S),
    re.compile(r"(?:src|href|data-background|data-hover|data-down|data-src)\s*=\s*['\"]([^'\"]+)['\"]", re.I),
    re.compile(r"url\(\s*['\"]?([^)'\"]+)['\"]?\s*\)", re.I),
]
IMPORT_RE = re.compile(r"(?:import\s+.+?\s+from\s+|import\s*)['\"]([^'\"]+)['\"]")
VARIANT_RE = re.compile(r"import\s+(\w+)\s+from\s+['\"]([^'\"]+)['\"]")
VERSION_RE = re.compile(r"(?:default|common|re|prere)\s*:\s*\{?", re.M)
EXT_RE = re.compile(r"\.(?:bmp|png|jpe?g|gif|tga|spr|act|wav|mp3|ogg|rsw|gnd|gat|rsm|gr2|str|pal|ebm|xml|lua|lub|txt|json|otf|ttf|webp|svg)\b", re.I)


def norm(path: str) -> str:
    return path.replace("\\", "/").replace("//", "/").lstrip("./")


def category_for(name: str) -> str:
    for category, names in CATEGORY_RULES:
        if name in names:
            return category
    return "Other"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1", errors="replace")


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT_EXTS:
            yield path


def build_asset_index(asset_root: Path | None) -> dict[str, list[str]]:
    index: dict[str, list[str]] = defaultdict(list)
    if not asset_root or not asset_root.exists():
        return index
    for path in asset_root.rglob("*"):
        if not path.is_file():
            continue
        rel = norm(path.relative_to(asset_root).as_posix())
        index[rel.casefold()].append(rel)
        index[path.name.casefold()].append(rel)
    return index


def extract_asset_refs(text: str) -> list[dict]:
    refs: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for pattern in LOAD_PATTERNS:
        for match in pattern.finditer(text):
            raw = match.group(match.lastindex or 1).strip()
            if pattern is LOAD_PATTERNS[0]:
                raw = match.group(2).strip()
            if raw.startswith(("data:", "blob:", "http://", "https://", "#")):
                continue
            if not EXT_RE.search(raw):
                continue
            kind = "dynamic" if any(token in raw for token in ("${", "+", "{", "}")) else "literal"
            key = (raw, kind)
            if key not in seen:
                seen.add(key)
                refs.append({"expression": raw, "kind": kind})
    return refs


def candidate_paths(expression: str) -> list[str]:
    value = expression.strip("`'\"")
    value = value.replace("${DB.INTERFACE_PATH}", "data/texture/À¯ÀúÀÎÅÍÆäÀÌ½º/")
    value = value.replace("DB.INTERFACE_PATH + ", "data/texture/À¯ÀúÀÎÅÍÆäÀÌ½º/")
    value = value.replace("${DB.ITEM_PATH}", "data/texture/À¯ÀúÀÎÅÍÆäÀÌ½º/item/")
    value = re.sub(r"\$\{[^}]+\}", "*", value)
    value = value.replace("' + ", "").replace(" + '", "").replace('" + ', '').replace(' + "', '')
    value = norm(value)
    out = [value]
    if value.startswith("data/"):
        out.append(value[5:])
    return list(dict.fromkeys(out))


def resolve_ref(expression: str, asset_index: dict[str, list[str]]) -> dict:
    candidates = candidate_paths(expression)
    matches: list[str] = []
    for candidate in candidates:
        if "*" in candidate:
            regex = re.compile("^" + re.escape(candidate).replace("\\*", ".+") + "$", re.I)
            for key, values in asset_index.items():
                if "/" in key and regex.match(key):
                    matches.extend(values)
        else:
            matches.extend(asset_index.get(candidate.casefold(), []))
            matches.extend(asset_index.get(Path(candidate).name.casefold(), []))
    unique = sorted(set(matches))
    return {
        "candidates": candidates,
        "matches": unique[:200],
        "status": "matched" if len(unique) == 1 else "ambiguous" if len(unique) > 1 else "missing",
    }


def component_catalog(src_root: Path, asset_index: dict[str, list[str]]) -> tuple[list[dict], list[dict]]:
    component_root = src_root / "UI" / "Components"
    components: list[dict] = []
    usage: list[dict] = []
    if not component_root.exists():
        raise SystemExit(f"UI component directory not found: {component_root}")

    for comp_dir in sorted((p for p in component_root.iterdir() if p.is_dir()), key=lambda p: p.name.casefold()):
        files = sorted(p for p in comp_dir.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_EXTS)
        variants = []
        source_files = []
        imports: set[str] = set()
        component_assets = []
        has_version_manager = False
        for path in files:
            rel = norm(path.relative_to(src_root).as_posix())
            text = read_text(path)
            source_files.append({"path": rel, "type": path.suffix.lower().lstrip("."), "bytes": path.stat().st_size})
            imports.update(IMPORT_RE.findall(text))
            has_version_manager = has_version_manager or "UIVersionManager" in text
            for ref in extract_asset_refs(text):
                resolved = resolve_ref(ref["expression"], asset_index)
                row = {"component": comp_dir.name, "source": rel, **ref, **resolved}
                usage.append(row)
                component_assets.append(row)

        for child in sorted((p for p in comp_dir.iterdir() if p.is_dir()), key=lambda p: p.name.casefold()):
            variant_files = sorted(norm(p.relative_to(src_root).as_posix()) for p in child.rglob("*") if p.is_file() and p.suffix.lower() in {".js", ".html", ".css"})
            if variant_files:
                variants.append({"name": child.name, "files": variant_files})

        components.append({
            "id": comp_dir.name,
            "name": comp_dir.name,
            "category": category_for(comp_dir.name),
            "root": norm(comp_dir.relative_to(src_root).as_posix()),
            "files": source_files,
            "variants": variants,
            "usesUIVersionManager": has_version_manager,
            "imports": sorted(imports),
            "assetSummary": {
                "total": len(component_assets),
                "matched": sum(1 for x in component_assets if x["status"] == "matched"),
                "ambiguous": sum(1 for x in component_assets if x["status"] == "ambiguous"),
                "missing": sum(1 for x in component_assets if x["status"] == "missing"),
            },
        })
    return components, usage


def scan_global_usage(src_root: Path, asset_index: dict[str, list[str]], existing: list[dict]) -> list[dict]:
    seen = {(x["source"], x["expression"]) for x in existing}
    usage = list(existing)
    for path in iter_text_files(src_root):
        rel = norm(path.relative_to(src_root).as_posix())
        text = read_text(path)
        for ref in extract_asset_refs(text):
            key = (rel, ref["expression"])
            if key in seen:
                continue
            seen.add(key)
            top = rel.split("/", 1)[0]
            resolved = resolve_ref(ref["expression"], asset_index)
            usage.append({"component": None, "domain": top, "source": rel, **ref, **resolved})
    return usage


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path, help="roBrowserLegacy src directory")
    parser.add_argument("--assets", type=Path, help="extracted asset root, usually private-assets/data")
    parser.add_argument("--out", type=Path, default=Path("apps/admin-studio/mockup"))
    args = parser.parse_args()

    src_root = args.source.resolve()
    asset_root = args.assets.resolve() if args.assets else None
    asset_index = build_asset_index(asset_root)
    components, component_usage = component_catalog(src_root, asset_index)
    usage = scan_global_usage(src_root, asset_index, component_usage)

    catalog = {
        "schemaVersion": 2,
        "generatedBy": "tools/player-ui/build_catalog.py",
        "sourceRoot": str(src_root),
        "assetRoot": str(asset_root) if asset_root else None,
        "stats": {
            "components": len(components),
            "variants": sum(len(x["variants"]) for x in components),
            "sourceFiles": sum(len(x["files"]) for x in components),
            "assetReferences": len(usage),
            "matchedAssets": sum(1 for x in usage if x["status"] == "matched"),
            "ambiguousAssets": sum(1 for x in usage if x["status"] == "ambiguous"),
            "missingAssets": sum(1 for x in usage if x["status"] == "missing"),
        },
        "categories": [name for name, _ in CATEGORY_RULES] + ["Other"],
        "components": components,
    }
    manifest = {
        "schemaVersion": 2,
        "sourceRoot": str(src_root),
        "assetRoot": str(asset_root) if asset_root else None,
        "references": usage,
    }
    write_json(args.out / "player-ui-catalog.json", catalog)
    write_json(args.out / "asset-usage-manifest.json", manifest)
    print(json.dumps(catalog["stats"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
