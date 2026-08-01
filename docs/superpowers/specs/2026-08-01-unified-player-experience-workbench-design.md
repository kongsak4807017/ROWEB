# Unified Player Experience Workbench Integration

- Status: Owner-approved scope
- Repository: `kongsak4807017/ROWEB`
- Target branch: `feature/unified-player-experience-workbench`
- Canonical shell: `apps/admin-studio/mockup/`

## Decision

Keep the existing rAthena Admin Studio and integrate Player Experience tooling into the same navigation, state, release, validation, and audit shell. The standalone `apps/workbench/` prototype remains a reference implementation until the unified shell reaches feature parity.

## Placement

```text
apps/admin-studio/
├── mockup/
│   ├── index.html                  # default unified entry after acceptance
│   └── unified-workbench.html      # canonical implementation during integration
└── player-experience/
    ├── player-ui-studio.js
    ├── player-ui-studio.css
    ├── ui-profile-store.js
    ├── validation.js
    └── README.md

apps/workbench/
└── ...                             # temporary prototype/reference

config/player-ui/
└── player-ui-profiles.json         # canonical desktop/mobile profile data
```

## Required behavior

1. Preserve all current Admin Studio views and dry-run safety behavior.
2. Add a `Player Experience` navigation group.
3. Add `Player UI Studio`, `Mobile Controls`, `Scene Preview`, and `UI Profiles` views.
4. Support Desktop, Mobile Landscape, and Mobile Portrait preview modes.
5. Provide a scene selector for Login, Character Select, Main HUD, Combat, Inventory, NPC Dialog, and Settings.
6. Provide a component inspector for visibility, anchor, X, Y, width, height, scale, opacity, and touch-target size.
7. Load `player-ui-profiles.json` as the baseline profile dataset.
8. Save draft state in browser-local storage for the static MVP.
9. Validate profile structure, required components, safe areas, touch sizes, and profile/device consistency.
10. Route Save, Validate, Publish, and Rollback through the existing release state and unified audit ledger.
11. Keep all mutations simulated/dry-run in this phase.
12. Change the default `index.html` entry to the unified shell only after tests pass.

## Navigation

```text
Overview
└── Command Center

Player Experience
├── Player UI Studio
├── Mobile Controls
├── Scene Preview
└── UI Profiles

Client & Assets
├── Source Scanner
├── Asset Catalog
├── Mapping Review
├── Episode Manager
└── Release Manager

Server Operations
├── Player Operations
├── Economy Studio
├── Anti-abuse
└── Runtime Services

Governance
├── Validation Center
├── Unified Audit
└── Settings
```

## Data flow

```text
player-ui-profiles.json
→ profile loader
→ editable Workbench state
→ live Desktop/Mobile preview
→ validation
→ draft/release record
→ unified audit event
→ exported profile JSON
```

The static MVP does not write directly to roBrowserLegacy, private assets, rAthena, MariaDB, or production endpoints.

## Error handling

- Missing or invalid profile JSON falls back to an embedded safe desktop profile and records a validation error.
- Invalid numeric values are rejected and do not update the preview.
- Publish remains blocked when validation has error-severity findings.
- Failed import preserves the current state.
- Every attempted save, validation, publish, rollback, and import records an audit event.

## Verification

Required tests:

- existing Admin Studio views remain present;
- Player Experience navigation targets exist;
- Desktop/Mobile profile switching updates preview classes;
- scene selector exposes all required scenes;
- inspector controls update selected components;
- profile JSON schema/version validation works;
- publish is blocked by validation errors;
- save/validate/publish/rollback append unified audit events;
- static JavaScript syntax check passes;
- no `fetch`, WebSocket, SQL, shell, or raw AtCommand is introduced;
- default index points to unified shell only after all checks pass.

## Acceptance

The integration is accepted when one URL opens the existing Command Center and allows the administrator to navigate into Player UI Studio, switch Desktop/Mobile modes, edit a component visually, validate it, create a simulated release, and see the complete action trail in Unified Audit without losing any existing Admin Studio capability.

## Rollback

Revert the integration commit and restore `apps/admin-studio/mockup/index.html` as the original Admin Studio entry. The standalone `apps/workbench/` prototype remains available, and no server, database, asset, or roBrowserLegacy state is modified.