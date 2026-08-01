#!/usr/bin/env python3
"""Build a targeted catalog of player-visible UI images, item data, and texts.

The scanner is source-driven and intentionally avoids a full asset-tree walk.
It indexes known UI/System/item roots, resolves UI image references, parses modern
itemInfo text files, and falls back to the legacy client item text tables used by
roBrowserLegacy.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

IMAGE_EXTS = {".bmp", ".png", ".jpg", ".jpeg", ".gif", ".tga", ".webp", ".svg"}
TEXT_NAMES = ("msgstringtable", "mapnametable", "questid2display", "questinfo", "skillinfo", "skilldescript", "achievement")
LEGACY_ITEM_TABLES = {
    "name": "idnum2itemdisplaynametable.txt",
    "resource": "idnum2itemresnametable.txt",
    "description": "idnum2itemdesctable.txt",
    "slot": "itemslotcounttable.txt",
}
LOAD_PATTERNS = [
    re.compile(r"Client\.loadFile\(\s*(?:DB\.INTERFACE_PATH\s*\+\s*)?['\"]([^'\"]+\.(?:bmp|png|jpe?g|gif|tga|webp|svg))['\"]", re.I),
    re.compile(r"Client\.loadFile\(\s*`(?:\$\{DB\.INTERFACE_PATH\})?([^`]+\.(?:bmp|png|jpe?g|gif|tga|webp|svg))`", re.I),
    re.compile(r"url\(\s*['\"]?([^)'\"]+\.(?:bmp|png|jpe?g|gif|tga|webp|svg))['\"]?\s*\)", re.I),
    re.compile(r"(?:src|data-background|data-hover|data-down|data-src)\s*=\s*['\"]([^'\"]+\.(?:bmp|png|jpe?g|gif|tga|webp|svg))['\"]", re.I),
]


def field_re(name: str) -> re.Pattern[str]:
    return re.compile(rf"{name}\s*=\s*[\"']((?:\\.|[^\"'])*)[\"']", re.S)


def read_text(path: Path) -> tuple[str, str, bool]:
    for encoding in ("utf-8-sig", "utf-8", "cp949", "latin-1"):
        try:
            return path.read_text(encoding=encoding), encoding, False
        except UnicodeDecodeError:
            pass
    return path.read_text(encoding="utf-8", errors="replace"), "utf-8-replace", True


def find_dirs(root: Path, names: list[str]) -> list[Path]:
    wanted = {name.casefold() for name in names}
    return [p for p in root.rglob("*") if p.is_dir() and p.name.casefold() in wanted]


def targeted_files(asset_root: Path) -> list[Path]:
    roots = find_dirs(asset_root, ["System", "item", "유저인터페이스", "À¯ÀúÀÎÅÍÆäÀÌ½º", "interface"])
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


def build_index(files: list[Path], asset_root: Path) -> tuple[dict[str, list[Path]], dict[str, list[Path]]]:
    by_name: dict[str, list[Path]] = {}
    by_relative: dict[str, list[Path]] = {}
    for path in files:
        by_name.setdefault(path.name.casefold(), []).append(path)
        try:
            rel = path.relative_to(asset_root).as_posix().casefold()
            by_relative.setdefault(rel, []).append(path)
        except ValueError:
            pass
    return by_name, by_relative


def match_status(matches: list[Path]) -> str:
    return "matched" if len(matches) == 1 else "ambiguous" if matches else "missing"


def unique_paths(paths: list[Path]) -> list[Path]:
    return list(dict.fromkeys(paths))


def resolve_image(expression: str, by_name: dict[str, list[Path]], by_relative: dict[str, list[Path]]) -> list[Path]:
    clean = expression.replace("\\", "/").lstrip("./")
    candidates = [clean.casefold()]
    if clean.startswith("data/"):
        candidates.append(clean[5:].casefold())
    matches: list[Path] = []
    for candidate in candidates:
        matches.extend(by_relative.get(candidate, []))
        suffix = "/" + candidate
        for rel, values in by_relative.items():
            if rel.endswith(suffix):
                matches.extend(values)
    if not matches:
        matches.extend(by_name.get(Path(clean).name.casefold(), []))
    return unique_paths(matches)


def scan_ui(source_root: Path, by_name: dict[str, list[Path]], by_relative: dict[str, list[Path]]) -> tuple[list[dict], int]:
    rows: list[dict] = []
    files_scanned = 0
    ui_root = source_root / "UI"
    if not ui_root.exists():
        return rows, files_scanned
    seen: set[tuple[str, str]] = set()
    for path in ui_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".js", ".html", ".css"}:
            continue
        files_scanned += 1
        text, _, _ = read_text(path)
        for pattern in LOAD_PATTERNS:
            for match in pattern.finditer(text):
                expression = match.group(1).replace("\\", "/")
                key = (path.as_posix(), expression)
                if key in seen:
                    continue
                seen.add(key)
                matches = resolve_image(expression, by_name, by_relative)
                rows.append({"source": path.relative_to(source_root).as_posix(), "expression": expression, "status": match_status(matches), "matches": [str(item) for item in matches[:20]]})
    return rows, files_scanned


def find_iteminfo_candidates(asset_root: Path) -> tuple[list[Path], list[Path]]:
    text_files: list[Path] = []
    bytecode_files: list[Path] = []
    for path in asset_root.rglob("*"):
        if not path.is_file() or not path.name.casefold().startswith("iteminfo"):
            continue
        if path.suffix.lower() in {".lua", ".txt"}:
            text_files.append(path)
        elif path.suffix.lower() == ".lub":
            bytecode_files.append(path)
    return text_files, bytecode_files


def extract_balanced_entries(text: str) -> list[tuple[int, str]]:
    entries: list[tuple[int, str]] = []
    start_re = re.compile(r"\[(\d+)\]\s*=\s*\{")
    for start in start_re.finditer(text):
        depth, quote, escaped = 1, None, False
        i = start.end()
        while i < len(text) and depth:
            ch = text[i]
            if quote:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == quote:
                    quote = None
            else:
                if ch in {'"', "'"}:
                    quote = ch
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
            i += 1
        if depth == 0:
            entries.append((int(start.group(1)), text[start.end():i - 1]))
    return entries


def extract_description(body: str) -> list[str]:
    marker = re.search(r"identifiedDescriptionName\s*=\s*\{", body)
    if not marker:
        return []
    depth, quote, escaped, i = 1, None, False, marker.end()
    while i < len(body) and depth:
        ch = body[i]
        if quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
        else:
            if ch in {'"', "'"}:
                quote = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
        i += 1
    content = body[marker.end():i - 1]
    values = re.findall(r"[\"']((?:\\.|[^\"'])*)[\"']", content, re.S)
    return [v.replace("\\n", "\n").replace("\\\"", '"').replace("\\'", "'") for v in values]


def icon_matches(resource_name: str, by_name: dict[str, list[Path]]) -> list[Path]:
    matches: list[Path] = []
    if resource_name:
        for extension in IMAGE_EXTS:
            matches.extend(by_name.get((resource_name + extension).casefold(), []))
    return unique_paths(matches)


def scan_iteminfo(text_files: list[Path], by_name: dict[str, list[Path]]) -> list[dict]:
    items: dict[int, dict] = {}
    for path in text_files:
        text, encoding, used_replacement = read_text(path)
        for item_id, body in extract_balanced_entries(text):
            name_match = field_re("identifiedDisplayName").search(body)
            resource_match = field_re("identifiedResourceName").search(body)
            if not (name_match or resource_match):
                continue
            resource = resource_match.group(1) if resource_match else ""
            matches = icon_matches(resource, by_name)
            slot_match = re.search(r"slotCount\s*=\s*(\d+)", body)
            class_match = re.search(r"ClassNum\s*=\s*(\d+)", body)
            items[item_id] = {
                "itemId": item_id, "identifiedName": name_match.group(1) if name_match else "",
                "identifiedResourceName": resource, "identifiedDescription": extract_description(body),
                "slotCount": int(slot_match.group(1)) if slot_match else None,
                "classNumber": int(class_match.group(1)) if class_match else None,
                "iconStatus": match_status(matches), "iconMatches": [str(item) for item in matches[:20]],
                "sourceFile": str(path), "sourceFormat": "itemInfo", "encoding": encoding,
                "warnings": ["replacement-characters"] if used_replacement or "�" in text else [],
            }
    return list(items.values())


def parse_legacy_table(path: Path) -> dict[int, str]:
    text, _, _ = read_text(path)
    rows: dict[int, str] = {}
    for raw in text.splitlines():
        line = raw.strip().lstrip("\ufeff")
        if not line or line.startswith("//") or line.startswith("#"):
            continue
        parts = line.split("#")
        if len(parts) < 2:
            continue
        try:
            item_id = int(parts[0].strip())
        except ValueError:
            continue
        rows[item_id] = "#".join(parts[1:]).strip().rstrip("#").replace("\\n", "\n")
    return rows


def scan_legacy_items(asset_root: Path, by_name: dict[str, list[Path]]) -> tuple[list[dict], dict[str, str]]:
    paths: dict[str, Path] = {}
    for kind, filename in LEGACY_ITEM_TABLES.items():
        candidates = [p for p in asset_root.rglob(filename) if p.is_file()]
        if candidates:
            paths[kind] = candidates[0]
    tables = {kind: parse_legacy_table(path) for kind, path in paths.items()}
    ids: set[int] = set()
    for table in tables.values():
        ids.update(table)
    items: list[dict] = []
    for item_id in sorted(ids):
        resource = tables.get("resource", {}).get(item_id, "")
        matches = icon_matches(resource, by_name)
        description = tables.get("description", {}).get(item_id, "")
        slot = tables.get("slot", {}).get(item_id)
        items.append({
            "itemId": item_id, "identifiedName": tables.get("name", {}).get(item_id, ""),
            "identifiedResourceName": resource, "identifiedDescription": description.splitlines() if description else [],
            "slotCount": int(slot) if slot and slot.isdigit() else None, "classNumber": None,
            "iconStatus": match_status(matches), "iconMatches": [str(item) for item in matches[:20]],
            "sourceFile": str(paths.get("name") or paths.get("resource") or ""),
            "sourceFormat": "legacy-text-tables", "encoding": "mixed", "warnings": [],
        })
    return items, {kind: str(path) for kind, path in paths.items()}


def scan_texts(asset_root: Path) -> list[dict]:
    rows: list[dict] = []
    for path in asset_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".txt", ".lua"}:
            continue
        lowered = path.name.casefold()
        if not any(token in lowered for token in TEXT_NAMES):
            continue
        text, encoding, used_replacement = read_text(path)
        preview = "\n".join(line for line in text.splitlines()[:12] if line.strip())[:1200]
        rows.append({"path": str(path), "encoding": encoding, "bytes": path.stat().st_size, "lineCount": text.count("\n") + 1, "preview": preview, "warnings": ["replacement-characters"] if used_replacement or "�" in text else []})
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--assets", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--profile", choices=["player-visible", "ui", "items", "text"], default="player-visible")
    args = parser.parse_args()

    indexed_files = targeted_files(args.assets)
    by_name, by_relative = build_index(indexed_files, args.assets)
    ui_images, ui_files_scanned = scan_ui(args.source, by_name, by_relative) if args.profile in {"player-visible", "ui"} else ([], 0)
    text_iteminfo, lub_iteminfo = find_iteminfo_candidates(args.assets)
    legacy_paths: dict[str, str] = {}
    items: list[dict] = []
    if args.profile in {"player-visible", "items"}:
        items = scan_iteminfo(text_iteminfo, by_name)
        if not items:
            items, legacy_paths = scan_legacy_items(args.assets, by_name)
    player_texts = scan_texts(args.assets) if args.profile in {"player-visible", "text"} else []
    diagnostics: list[str] = []
    if args.profile in {"player-visible", "items"} and not items:
        diagnostics.append("Only compiled itemInfo .lub files were found and no legacy item text tables could be parsed." if lub_iteminfo and not text_iteminfo else "No item records parsed from itemInfo or legacy item text tables.")

    payload = {
        "schemaVersion": 2, "profile": args.profile,
        "scan": {
            "fullAssetWalk": False, "targetedFilesIndexed": len(indexed_files),
            "targetRoots": ["System", "item", "유저인터페이스", "À¯ÀúÀÎÅÍÆäÀÌ½º", "interface"],
            "uiSourceFilesScanned": ui_files_scanned, "itemInfoCandidates": len(text_iteminfo),
            "compiledItemInfoCandidates": len(lub_iteminfo), "legacyItemTables": legacy_paths, "diagnostics": diagnostics,
        },
        "stats": {"uiImages": len(ui_images), "items": len(items), "playerTexts": len(player_texts)},
        "uiImages": ui_images, "items": items, "playerTexts": player_texts,
    }
    args.out.mkdir(parents=True, exist_ok=True)
    output = args.out / "player-visible-content-catalog.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({**payload["stats"], **payload["scan"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
