# Player-visible content scanner

## Goal

Scan only content that players actually see: UI images, item names/descriptions/icons, and player-facing text tables. The default profile avoids a full traversal of the roughly 300,000-file asset tree.

## Profiles

- `player-visible`: UI + items + player-facing text
- `ui`: UI image references from `src/UI`
- `items`: `itemInfo.lua` records and item icon matching
- `text`: message, map, quest, skill, and achievement text files

## Targeted roots

The scanner indexes known high-value roots first:

- `System`
- item image directories
- `유저인터페이스`
- `À¯ÀúÀÎÅÍÆäÀÌ½º`
- `interface`

It does not walk every map/model/effect directory by default.

## Run

```powershell
Set-Location C:\RO-WEB-V1\ROWEB-unified-workbench
powershell -ExecutionPolicy Bypass -File tools\player-ui\build_player_visible_catalog.ps1
```

Specific profiles:

```powershell
powershell -ExecutionPolicy Bypass -File tools\player-ui\build_player_visible_catalog.ps1 -Profile ui
powershell -ExecutionPolicy Bypass -File tools\player-ui\build_player_visible_catalog.ps1 -Profile items
powershell -ExecutionPolicy Bypass -File tools\player-ui\build_player_visible_catalog.ps1 -Profile text
```

## Output

`apps/admin-studio/mockup/player-visible-content-catalog.json`

The JSON contains:

- scan scope and indexed file count
- UI image references with matched/ambiguous/missing status
- item ID, display name, resource name, description lines, slot count, class number, icon matches, encoding, and warnings
- player-facing text source paths, encoding, size, line count, and warnings

## Safety

The scanner is read-only. It never modifies `roBrowserLegacy`, `private-assets`, rAthena, or MariaDB.
