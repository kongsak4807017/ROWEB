#!/usr/bin/env python3
"""Build a targeted catalog of player-visible UI images, item data, and texts.

The scanner is source-driven and intentionally avoids a full asset walk.
It indexes known UI/System/item roots first, resolves references by relative path
and filename, and records diagnostics explaining empty results.
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
IMAGE_SUFFIX = r"(?:bmp|png|jpe?g|gif|tga|webp|svg)"
CLIENT_CALL_RE = re.compile(r"Client\.loadFile\(\s*(.+?)\s*,", re.S)
CSS_URL_RE = re.compile(r"url\(\s*['\"]?([^)'\"]+\.(?:" + IMAGE_SUFFIX + r"))['\"]?\s*\)", re.I)
HTML_ASSET_RE = re.compile(
    r"(?:src|href|data-background|data-hover|data-down|data-src)\s*=\s*['\"]([^'\"]+\.(?:"
    + IMAGE_SUFFIX
    + r"))['\"]",
    re.I,
)
QUOTED_IMAGE_RE = re.compile(r"['\"]([^'\"]+\.(?:" + IMAGE_SUFFIX + r"))['\"]", re.I)
TEMPLATE_IMAGE_RE = re.compile(r"`([^`]+\.(?:" + IMAGE_SUFFIX + r"))`", re.I)
STRING_RE = re.compile(r'"((?:\\.|[^"])*)"|\'((?:\\.|[^\'])*)\'')
ITEM_START_RE = re.compile(r"\[\s*(\d+)\s*\]\s*=\s*\{")


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
        ["System", "SystemEN", "item", "유저인터페이스", "À¯ÀúÀÎÅÍÆäÀÌ½º", "interface"],
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


def norm(value: str) -> str:
    return value.replace("\\", "/").replace("//", "/").strip().lstrip("./")


def build_index(files: list[Path], asset_root: Path) -> tuple[dict[str, list[Path]], dict[str, list[Path]]]:
    by_name: dict[str, list[Path]] = {}
    by_rel: dict[str, list[Path]] = {}
    for path in files:
        by_name.setdefault(path.name.casefold(), []).append(path)
        try:
            rel = norm(path.relative_to(asset_root).as_posix())
            by_rel.setdefault(rel.casefold(), []).append(path)
            if rel.casefold().startswith("data/"):
                by_rel.setdefault(rel[5:].casefold(), []).append(path)
        except ValueError:
            pass
    return by_name, by_rel


def match_status(matches: list[Path]) -> str:
    unique = {str(path) for path in matches}
    if len(unique) == 1:
        return "matched"
    if unique:
        return "ambiguous"
    return "missing"


def clean_expression(expression: str) -> str:
    value = expression.strip().strip("`'\"")
    value = re.sub(r"^DB\.INTERFACE_PATH\s*\+\s*", "", value)
    value = value.replace("${DB.INTERFACE_PATH}", "")
    value = value.replace("${DB.ITEM_PATH}", "item/")
    value = re.sub(r"\$\{[^}]+\}", "*", value)
    value = re.sub(r"['\"]\s*\+\s*", "", value)
    value = re.sub(r"\s*\+\s*['\"]", "", value)
    return norm(value)


def extract_ui_references(text: str) -> list[str]:
    found: list[str] = []
    for call in CLIENT_CALL_RE.finditer(text):
        argument = call.group(1).strip()
        candidates = []
        candidates.extend(match.group(1) for match in TEMPLATE_IMAGE_RE.finditer(argument))
        candidates.extend(match.group(1) for match in QUOTED_IMAGE_RE.finditer(argument))
        for candidate in candidates:
            found.append(clean_expression(candidate))
    found.extend(clean_expression(match.group(1)) for match in CSS_URL_RE.finditer(text))
    found.extend(clean_expression(match.group(1)) for match in HTML_ASSET_RE.finditer(text))
    return list(dict.fromkeys(value for value in found if value))


def resolve_expression(expression: str, by_name: dict[str, list[Path]], by_rel: dict[str, list[Path]]) -> list[Path]:
    if "*" in expression:
        regex = re.compile("^" + re.escape(expression).replace(r"\*", ".+") + "$", re.I)
        matches: list[Path] = []
        for rel, paths in by_rel.items():
            if regex.match(rel):
                matches.extend(paths)
        return list(dict.fromkeys(matches))
    candidates = [expression, f"texture/{expression}"]
    matches: list[Path] = []
    for candidate in candidates:
        matches.extend(by_rel.get(candidate.casefold(), []))
    if not matches:
        matches.extend(by_name.get(Path(expression).name.casefold(), []))
    return list(dict.fromkeys(matches))


def scan_ui(source_root: Path, by_name: dict[str, list[Path]], by_rel: dict[str, list[Path]]) -> tuple[list[dict], int]:
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
        source = path.relative_to(source_root).as_posix()
        for expression in extract_ui_references(text):
            key = (source, expression)
            if key in seen:
                continue
            seen.add(key)
            matches = resolve_expression(expression, by_name, by_rel)
            rows.append(
                {
                    "source": source,
                    "expression": expression,
                    "status": match_status(matches),
                    "matches": [str(item) for item in matches[:20]],
                }
            )
    return rows, files_scanned


def balanced_item_blocks(text: str):
    for match in ITEM_START_RE.finditer(text):
        item_id = int(match.group(1))
        start = match.end() - 1
        depth = 0
        quote = None
        escaped = False
        for index in range(start, len(text)):
            char = text[index]
            if quote:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == quote:
                    quote = None
                continue
            if char in {'"', "'"}:
                quote = char
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    yield item_id, text[start + 1 : index]
                    break


def lua_string_field(body: str, name: str) -> str:
    match = re.search(rf"\b{name}\s*=\s*(['\"])((?:\\.|(?!\1).)*)\1", body, re.S)
    return match.group(2) if match else ""


def lua_number_field(body: str, name: str):
    match = re.search(rf"\b{name}\s*=\s*(-?\d+)", body)
    return int(match.group(1)) if match else None


def lua_array_field(body: str, name: str) -> list[str]:
    match = re.search(rf"\b{name}\s*=\s*\{{", body)
    if not match:
        return []
    start = match.end() - 1
    depth = 0
    quote = None
    escaped = False
    end = None
    for index in range(start, len(body)):
        char = body[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {'"', "'"}:
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                end = index
                break
    if end is None:
        return []
    values = []
    for string_match in STRING_RE.finditer(body[start + 1 : end]):
        value = string_match.group(1) if string_match.group(1) is not None else string_match.group(2)
        values.append(value.replace("\\n", "\n"))
    return values


def item_info_candidates(asset_root: Path) -> list[Path]:
    return [
        path
        for path in asset_root.rglob("*")
        if path.is_file()
        and "iteminfo" in path.name.casefold()
        and path.suffix.lower() in {".lua", ".txt"}
    ]


def scan_items(asset_root: Path, by_name: dict[str, list[Path]]) -> tuple[list[dict], int]:
    items: list[dict] = []
    candidates = item_info_candidates(asset_root)
    seen_ids: set[tuple[int, str]] = set()
    for path in candidates:
        text, encoding, used_replacement = read_text(path)
        for item_id, body in balanced_item_blocks(text):
            name = lua_string_field(body, "identifiedDisplayName")
            resource_name = lua_string_field(body, "identifiedResourceName")
            if not (name or resource_name):
                continue
            dedupe = (item_id, str(path))
            if dedupe in seen_ids:
                continue
            seen_ids.add(dedupe)
            icon_matches: list[Path] = []
            for extension in IMAGE_EXTS:
                icon_matches.extend(by_name.get((resource_name + extension).casefold(), []))
            warnings = []
            if used_replacement or "�" in text:
                warnings.append("replacement-characters")
            items.append(
                {
                    "itemId": item_id,
                    "identifiedName": name,
                    "identifiedResourceName": resource_name,
                    "identifiedDescription": lua_array_field(body, "identifiedDescriptionName"),
                    "slotCount": lua_number_field(body, "slotCount"),
                    "classNumber": lua_number_field(body, "ClassNum"),
                    "iconStatus": match_status(icon_matches),
                    "iconMatches": [str(item) for item in dict.fromkeys(icon_matches)][:20],
                    "sourceFile": str(path),
                    "encoding": encoding,
                    "warnings": warnings,
                }
            )
    return items, len(candidates)


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
    by_name, by_rel = build_index(indexed_files, args.assets)
    if args.profile in {"player-visible", "ui"}:
        ui_images, ui_files_scanned = scan_ui(args.source, by_name, by_rel)
    else:
        ui_images, ui_files_scanned = [], 0
    if args.profile in {"player-visible", "items"}:
        items, item_candidates = scan_items(args.assets, by_name)
    else:
        items, item_candidates = [], 0
    player_texts = scan_texts(args.assets) if args.profile in {"player-visible", "text"} else []

    diagnostics = []
    if args.profile in {"player-visible", "ui"} and not ui_images:
        diagnostics.append("No UI references extracted; verify --source points to roBrowserLegacy/src and contains UI files.")
    if args.profile in {"player-visible", "items"} and not items:
        diagnostics.append(
            "No text itemInfo entries parsed. Check itemInfoCandidates; .lub-only sources require decompilation or runtime export."
        )

    payload = {
        "schemaVersion": 2,
        "profile": args.profile,
        "scan": {
            "fullAssetWalk": False,
            "targetedFilesIndexed": len(indexed_files),
            "targetRoots": ["System", "SystemEN", "item", "유저인터페이스", "À¯ÀúÀÎÅÍÆäÀÌ½º", "interface"],
            "uiSourceFilesScanned": ui_files_scanned,
            "itemInfoCandidates": item_candidates,
            "diagnostics": diagnostics,
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
    print(json.dumps({**payload["stats"], **payload["scan"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
