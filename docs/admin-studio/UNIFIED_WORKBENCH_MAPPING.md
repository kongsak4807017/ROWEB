# Unified ROWeb Operations Workbench and Mapping Pipeline

The Workbench now contains two module groups in one shell:

- Client & Asset Operations: scanner, catalog, mapping review, themes and releases.
- rAthena Admin Studio: command center, player operations, economy, anti-abuse and unified audit.

## Run the mockup

```bash
python -m http.server 4173 --directory apps/admin-studio/mockup
```

Open `http://localhost:4173`.

## Scan a real roBrowserLegacy checkout

```bash
python tools/asset-mapping/scan_robrowser_assets.py \
  C:/Ragnarok-Prontera/HermesWorkSpace/roBrowserLegacy \
  --output roweb-asset-mapping.json
```

Import `roweb-asset-mapping.json` through the Workbench Import action, or scan a browser-export HTML/source directory in the Source Scanner.

The mapping output contains logical IDs, legacy paths, categories, source consumers, reference counts, inferred rAthena domains, confidence and logical-ID collisions. It never modifies source files or licensed assets.
