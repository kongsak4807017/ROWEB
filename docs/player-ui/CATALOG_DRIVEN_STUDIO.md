# Catalog-driven Player UI Studio

## Purpose

Build a searchable inventory of the real `roBrowserLegacy/src/UI/Components` tree and map source-level asset references to files under the private extracted asset folder.

The scanner is read-only. It does not edit `roBrowserLegacy`, `rAthena`, MariaDB, or private assets.

## Windows workspace

Expected paths:

```text
C:\RO-WEB-V1\ROWEB
C:\RO-WEB-V1\roBrowserLegacy\src
C:\RO-WEB-V1\private-assets\data
```

## Build the catalog

From `C:\RO-WEB-V1\ROWEB`:

```powershell
powershell -ExecutionPolicy Bypass -File tools\player-ui\build_catalog.ps1
```

Explicit paths:

```powershell
powershell -ExecutionPolicy Bypass -File tools\player-ui\build_catalog.ps1 `
  -Source "C:\RO-WEB-V1\roBrowserLegacy\src" `
  -Assets "C:\RO-WEB-V1\private-assets\data" `
  -Output "C:\RO-WEB-V1\ROWEB\apps\admin-studio\mockup"
```

Generated files:

```text
apps/admin-studio/mockup/player-ui-catalog.json
apps/admin-studio/mockup/asset-usage-manifest.json
```

## Open the Studio

```powershell
py -m http.server 4173 --directory apps\admin-studio\mockup
```

Open:

```text
http://127.0.0.1:4173/
```

Choose **Catalog-driven Player UI Studio**, or open directly:

```text
http://127.0.0.1:4173/player-ui-catalog-studio.html
```

## What is indexed

- UI component groups under `src/UI/Components`
- `.js`, `.html`, and `.css` source files
- variant subdirectories such as `InventoryV0`–`InventoryV3`
- imports and `UIVersionManager` usage
- literal and dynamic `Client.loadFile(...)` references
- HTML asset attributes
- CSS `url(...)` references
- global source references outside UI components
- matching files in the private asset tree

## Asset status

- `matched`: one physical asset matched
- `ambiguous`: multiple files matched; manual review required
- `missing`: no physical file matched

Dynamic expressions are retained as expressions and converted to wildcard candidates. They are not silently treated as exact mappings.

## Validation

```powershell
python -m pytest tests/test_player_ui_catalog_builder.py -q
```

Run the existing Workbench tests as well:

```powershell
python -m pytest `
  tests/test_admin_studio_mockup.py `
  tests/test_unified_player_experience_workbench.py `
  tests/test_player_ui_catalog_builder.py `
  -q
```

## Safety boundary

Generated catalog and manifest files may contain local source and asset paths. Review them before publishing outside the private repository. The scanner never copies asset binaries into Git.
