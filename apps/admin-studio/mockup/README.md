# ROWeb Operations Workbench — Unified Static MVP

Dependency-free admin-only prototype combining the existing rAthena Admin Studio with Player Experience controls.

## Run locally

```powershell
Set-Location C:\RO-WEB-V1\ROWEB
py -m http.server 4173 --directory apps/admin-studio/mockup
```

Open:

```text
http://127.0.0.1:4173/
```

`index.html` redirects to `unified-workbench.html`.

## Included views

### Server Operations

- Command Center
- Player Operations
- Economy Studio
- Anti-abuse review

### Player Experience

- Player UI Studio
- Scene selector
- EP01–EP17 selector
- Desktop preview
- Mobile Landscape preview
- Mobile Portrait preview
- Component Inspector for X/Y, width, scale, opacity, anchor, and visibility
- Mobile Control Studio

### Change Control

- Save Draft
- Validation Center
- Local MVP Publish
- Rollback
- Unified Audit Ledger

## Profile data

The static MVP loads:

```text
player-ui-profiles.json
```

The file contains Desktop, Mobile Landscape, and Mobile Portrait profiles plus mobile input bindings and client validation references.

## Safety boundary

All operational metrics are synthetic. Configuration changes, releases, and audit events are stored only in browser `localStorage`.

The static MVP does not:

- connect to rAthena or MariaDB;
- edit roBrowserLegacy source;
- write to private assets;
- send shell, SQL, WebSocket, or raw AtCommand requests;
- claim that a local profile publish is a production asset release.

Production adapters require authentication, RBAC, immutable server-side audit storage, validation, approval, and rollback controls.