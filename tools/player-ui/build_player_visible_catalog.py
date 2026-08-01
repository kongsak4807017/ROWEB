#!/usr/bin/env python3
"""Build a targeted catalog of player-visible UI images, item data, and texts.

The scanner is source-driven and intentionally avoids a full 300k-file walk.
It indexes known UI/System/item roots first, then resolves references by filename.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

IMAGE_EXTS = {".bmp", ".png", ".jpg", ".jpeg", ".gif", ".tga", ".webp", ".svg"}
TEXT_NAMES = (
    "msgstringtable",
    "mapnametable",
    "questid2display",
    "questinfo",
    "skillinfo",
    "skilldescript",
    "achievement",
)
ITEM_RE = re.compile(r"\[(\d+)\]\s*=\s*\{(.*?)\n\s*\}", re.S)
DESC_RE = re.compile(r"identifiedDescriptionName\s*=\s*\{(.*?)\}", re.S)
STRING_RE = re.compile(r'"((?:\\.|[^"])*)"')
LOAD_RE = re.compile(
    r"Client\.loadFile\(\s*(?:DB\.INTERFACE_PATH\s*\+\s*)?['\"]([^'\"]+\.(?:bmp|png|jpe?g|gif|tga|webp|svg))['\"]",
    re.I,
)


def field_re(name: str) -> re.Pattern[str]:
    return re.compile(rf'{name}\s*=\s*"((?:\\.|[^"])*)"', re.S)


def read_text(path: Path) -> tuple[str, str, bool]:
    for encoding in ("utf-8-sig", "utf-8", "cp949", "latin-1"):
        try:
            return path.read_text(encoding=encoding), encoding, False
        except UnicodeDecodeError:
            pass
    return path.read_text(encoding="utf-8", errors="replace"), "utf-8-replace", True


def find_dirs(root: Path, names: list[str]) -> list[Path]:
    wanted = {name.casefold() for name in names}
    return [path for path in root.rglob("*") if path.is_dir() and path.name.casefold() in wanted]


def targeted_files(asset_root: Path) -> list[Path]:
    roots = find_dirs(
        asset_root,
        ["System", "item", "유저인터페이스", "À¯ÀúÀÎÅÍÆäÀÌ½º", "interface"],
    )
    roots.append(asset_root)
    seen: set[Path] = set()
    files: list[Path] = []
    for root in roots:
        iterator = root.iterdir() if root == asset_root else root.rglob("*")
        for path in iterator:
            if path.is_file() and path not in seen:
                seen.add(path)
                files.append(path)
    return files


def build_index(files: list[Path]) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for path in files:
        index.setdefault(path.name.casefold(), []).append(path)
    return index


def match_status(matches: list[Path]) -> str:
    if len(matches) == 1:
        return "matched"
    if matches:
        return "ambiguous"
    return "missing"


def scan_ui(source_root: Path, index: dict[str, list[Path]]) -> list[dict]:
    rows: list[dict] = []
    ui_root = source_root / "UI"
    if not ui_root.exists():
        return rows
    for path in ui_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".js", ".html", ".css"}:
            continue
        text, _, _ = read_text(path)
        for match in LOAD_RE.finditer(text):
            expression = match.group(1).replace("\\", "/")
            matches = index.get(Path(expression).name.casefold(), [])
            rows.append(
                {
                    "source": path.relative_to(source_root).as_posix(),
                    "expression": expression,
                    "status": match_status(matches),
                    "matches": [str(item) for item in matches[:20]],
                }
            )
    return rows


def scan_items(asset_root: Path, index: dict[str, list[Path]]) -> list[dict]:
    items: list[dict] = []
    candidates = [
        path
        for path in asset_root.rglob("*")
        if path.is_file()
        and path.name.casefold().startswith("iteminfo.")
        and path.suffix.lower() in {".lua", ".txt"}
    ]
    for path in candidates:
        text, encoding, used_replacement = read_text(path)
        for match in ITEM_RE.finditer(text):
            item_id = int(match.group(1))
            body = match.group(2)
            name_match = field_re("identifiedDisplayName").search(body)
            resource_match = field_re("identifiedResourceName").search(body)
            if not (name_match or resource_match):
                continue
            description_match = DESC_RE.search(body)
            descriptions = (
                [value.replace("\\n", "\n") for value in STRING_RE.findall(description_match.group(1))]
                if description_match
                else []
            )
            resource_name = resource_match.group(1) if resource_match else ""
            icon_matches: list[Path] = []
            for extension in IMAGE_EXTS:
                icon_matches.extend(index.get((resource_name + extension).casefold(), []))
            slot_match = re.search(r"slotCount\s*=\s*(\d+)", body)
            class_match = re.search(r"ClassNum\s*=\s*(\d+)", body)
            warnings = []
            if used_replacement or "�" in text:
                warnings.append("replacement-characters")
            items.append(
                {
                    "itemId": item_id,
                    "identifiedName": name_match.group(1) if name_match else "",
                    "identifiedResourceName": resource_name,
                    "identifiedDescription": descriptions,
                    "slotCount": int(slot_match.group(1)) if slot_match else None,
                    "classNumber": int(class_match.group(1)) if class_match else None,
                    "iconStatus": match_status(icon_matches),
                    "iconMatches": [str(item) for item in icon_matches[:20]],
                    "sourceFile": str(path),
                    "encoding": encoding,
                    "warnings": warnings,
                }
            )
    return items


def scan_texts(asset_root: Path) -> list[dict]:
    rows: list[dict] = []
    for path in asset_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".txt", ".lua"}:
            continue
        lowered = path.name.casefold()
        if not any(token in lowered for token in TEXT_NAMES):
            continue
        text, encoding, used_replacement = read_text(path)
        warnings = []
        if used_replacement or "�" in text:
            warnings.append("replacement-characters")
        rows.append(
            {
                "path": str(path),
                "encoding": encoding,
                "bytes": path.stat().st_size,
                "lineCount": text.count("\n") + 1,
                "warnings": warnings,
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--assets", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--profile",
        choices=["player-visible", "ui", "items", "text"],
        default="player-visible",
    )
    args = parser.parse_args()

    indexed_files = targeted_files(args.assets)
    asset_index = build_index(indexed_files)
    ui_images = scan_ui(args.source, asset_index) if args.profile in {"player-visible", "ui"} else []
    items = scan_items(args.assets, asset_index) if args.profile in {"player-visible", "items"} else []
    player_texts = scan_texts(args.assets) if args.profile in {"player-visible", "text"} else []

    payload = {
        "schemaVersion": 1,
        "profile": args.profile,
        "scan": {
            "fullAssetWalk": False,
            "targetedFilesIndexed": len(indexed_files),
            "targetRoots": ["System", "item", "유저인터페이스", "À¯ÀúÀÎÅÍÆäÀÌ½º", "interface"],
        },
        "stats": {
            "uiImages": len(ui_images),
            "items": len(items),
            "playerTexts": len(player_texts),
        },
        "uiImages": ui_images,
        "items": items,
        "playerTexts": player_texts,
    }
    args.out.mkdir(parents=True, exist_ok=True)
    output = args.out / "player-visible-content-catalog.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload["stats"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
