# ROWeb Operations Workbench — Design Specification

- **Status:** Approved
- **Approved date:** 2026-07-30
- **Repository:** `kongsak4807017/ROWEB`
- **Target:** Admin-only Web Application for roBrowserLegacy/rAthena operations
- **Initial deployment:** Local Windows development, then Singapore VPS staging/production

## 1. Executive Summary

ROWeb Operations Workbench is a private administrative Web application for controlling client assets, UI themes, release manifests, service status, and operational audit history for the ROWEB platform.

It is intentionally separated from:

1. the player-facing website and account portal;
2. the roBrowserLegacy WebGL client;
3. the WebSocket gateway;
4. the rAthena login, character, and map servers;
5. the rAthena MariaDB database; and
6. the public asset CDN.

The first release is an operational MVP. It proves the complete workflow from asset registration through theme selection, manifest generation, release promotion, rollback, and audit logging without granting destructive control over production rAthena services.

## 2. Goals

The MVP must provide a usable control plane for the following tasks:

- view high-level service health;
- catalog client assets using logical asset identifiers;
- preview and classify UI, map, entity, effect, and audio assets;
- configure login background and theme profiles without modifying hard-coded JavaScript paths;
- generate a versioned asset manifest;
- create, validate, promote, and roll back releases;
- export and import Workbench configuration;
- record every administrative change in an audit log;
- support local, Singapore staging, and Singapore production environment profiles; and
- remain deployable as a static Web application during the MVP phase.

## 3. Non-Goals for MVP

The MVP will not:

- restart rAthena processes;
- ban or modify player accounts;
- write directly to rAthena MariaDB;
- modify or rebuild GRF archives;
- deploy map geometry while players are online;
- expose an unauthenticated public admin API;
- store production secrets or passwords;
- replace rAthena gameplay authority;
- provide a complete map, monster, NPC, item, or skill editor; or
- implement Kubernetes orchestration.

These capabilities require production authentication, role-based access control, immutable audit storage, approval workflows, and dedicated control adapters.

## 4. Users and Roles

The MVP uses a single local administrator identity. The production architecture must support these roles:

| Role | Primary responsibilities |
|---|---|
| Owner | Full system and release authority |
| Server Administrator | Runtime services, backup, configuration |
| Game Master | Player and live-operations tools |
| Asset Manager | Asset catalog, manifests, releases |
| UI Designer | Themes and presentation assets |
| Viewer | Read-only dashboards and reports |

Role enforcement is deferred from the static MVP but all screens and actions must be designed so permission checks can be inserted later without redesigning the application.

## 5. Information Architecture

The primary navigation contains:

1. **Dashboard**
2. **Assets**
3. **Themes**
4. **Releases**
5. **Runtime**
6. **Audit**
7. **Settings**

### 5.1 Dashboard

Shows:

- selected environment;
- current production asset release;
- Web client, asset service, gateway, rAthena, database, and CDN status;
- online-player placeholder metric;
- missing-asset count;
- recent release activity;
- recent audit events; and
- key performance placeholders such as asset errors, cache-hit ratio, and latency.

MVP service values may be simulated, but each card must expose a typed interface that can later receive real health-check data.

### 5.2 Asset Catalog

Each asset record includes:

- logical asset ID;
- display name;
- category;
- asset type;
- legacy source path;
- published URL or object key;
- format;
- version;
- content hash;
- file size;
- preview URL;
- release status;
- tags;
- consumer references;
- provenance/license note;
- fallback logical asset ID;
- created and updated timestamps.

Initial categories:

- UI;
- map;
- entity;
- effect;
- audio; and
- data.

Example logical IDs:

- `ui.login.background`
- `ui.inventory.frame`
- `entity.monster.1002.sprite`
- `map.prontera.minimap`
- `audio.bgm.prontera`

The UI supports search, filtering, adding, editing, previewing, and marking missing assets. Deletion is soft deletion in the MVP to preserve audit history.

### 5.3 Theme Studio

A theme profile contains:

- profile ID;
- display name;
- base profile;
- target device;
- compatibility profile;
- login background asset ID;
- primary and secondary color tokens;
- window opacity;
- HUD scale;
- UI density;
- font profile;
- optional icon pack;
- status; and
- version.

Initial profiles:

- Classic Desktop;
- Modern Desktop;
- Mobile Friendly; and
- High Contrast.

The Theme Studio produces configuration data. It must never edit `Background.js`, CSS files, or other source files directly.

### 5.4 Release Manager

Release states:

```text
Draft → Validated → Staging → Production → Superseded
                                      ↘ Rolled Back
```

A release contains:

- release ID;
- environment;
- asset manifest version;
- selected theme profile;
- changed asset list;
- release notes;
- validation results;
- creator;
- timestamps;
- previous production release; and
- rollback target.

Release validation checks:

- logical IDs are unique;
- required asset IDs exist;
- fallbacks resolve without a cycle;
- published URLs are syntactically valid;
- hashes are present for published assets;
- theme assets exist;
- no asset is marked both missing and production-ready; and
- manifest schema is valid.

Promotion to Production updates the environment pointer only. Physical asset objects remain immutable.

Rollback changes the Production pointer to a previously validated release. It does not overwrite or delete objects.

### 5.5 Runtime

The MVP Runtime page provides read-only service cards and placeholders for future telemetry:

- Web client;
- asset service;
- WSS gateway;
- rAthena login server;
- rAthena character server;
- rAthena map server;
- MariaDB;
- CDN; and
- Workbench API.

Future metrics include:

- player count;
- asset request and failure totals;
- cache-hit ratio;
- download bytes;
- decode duration;
- gateway connection count;
- packet errors;
- process uptime;
- SQL latency; and
- service readiness.

No destructive runtime command is included in the MVP.

### 5.6 Audit Log

Every state-changing action records:

- audit event ID;
- timestamp;
- actor;
- environment;
- action;
- target type;
- target ID;
- previous value summary;
- new value summary;
- result;
- correlation ID; and
- optional release ID.

Audit records are append-only from the application perspective. Local storage may be cleared by the browser during MVP development; production requires server-side immutable persistence.

### 5.7 Settings

Environment profiles:

- Local Development;
- Singapore Staging; and
- Singapore Production.

Each profile stores non-secret endpoints:

- player portal URL;
- game client URL;
- WSS gateway URL;
- asset API URL;
- CDN base URL;
- admin API URL;
- health endpoint base URL; and
- status page URL.

Secrets are never stored in the static application configuration.

## 6. Technical Architecture

### 6.1 MVP Architecture

```text
Admin Browser
    │
    ▼
React + TypeScript + Vite Workbench
    │
    ├── Typed domain services
    ├── Local repository adapters
    ├── Validation service
    ├── Manifest generator
    ├── Release state machine
    └── Audit event service
            │
            ▼
Browser localStorage + JSON import/export
```

The architecture uses ports and adapters so local browser persistence can later be replaced by HTTP APIs without rewriting screen components.

### 6.2 Production Architecture

```text
Admin Browser
    │ HTTPS + MFA/Zero Trust
    ▼
ROWeb Workbench Frontend
    │
    ▼
Workbench Control API
    ├── Authentication/RBAC
    ├── Asset Registry
    ├── Theme Service
    ├── Manifest Service
    ├── Release Service
    ├── Audit Service
    └── Runtime Read Models
        │
        ├── PostgreSQL
        ├── Object Storage
        ├── CDN
        ├── Metrics/Event Stores
        └── Safe rAthena/Gateway adapters
```

### 6.3 Player-Facing Boundary

```text
Player Browser
    ├── HTTPS → Portal and roBrowserLegacy
    ├── HTTPS → CDN assets
    └── WSS   → Gateway → private rAthena network
```

The Workbench is not part of the player request path. Workbench failure must not disconnect players or stop rAthena.

## 7. Frontend Structure

Recommended project structure:

```text
apps/workbench/
├── src/
│   ├── app/
│   ├── components/
│   ├── features/
│   │   ├── dashboard/
│   │   ├── assets/
│   │   ├── themes/
│   │   ├── releases/
│   │   ├── runtime/
│   │   ├── audit/
│   │   └── settings/
│   ├── domain/
│   ├── services/
│   ├── repositories/
│   ├── validation/
│   ├── storage/
│   ├── styles/
│   └── tests/
├── public/
├── Dockerfile
└── README.md
```

The exact directory may be adjusted to match the repository’s established conventions during implementation.

## 8. Domain Model

Core entities:

- `AssetRecord`
- `ThemeProfile`
- `EnvironmentProfile`
- `Release`
- `ReleaseValidationResult`
- `ServiceHealth`
- `AuditEvent`
- `WorkbenchState`

All persisted data uses explicit schema versions so future migrations are deterministic.

Example root state:

```json
{
  "schemaVersion": 1,
  "selectedEnvironmentId": "local",
  "assets": [],
  "themes": [],
  "releases": [],
  "auditEvents": [],
  "environments": []
}
```

## 9. Manifest Contract

Generated manifests are immutable release artifacts.

Minimum structure:

```json
{
  "manifestVersion": 1,
  "releaseId": "roweb-assets-2026.07.30.1",
  "environment": "staging",
  "themeProfile": "modern-desktop",
  "generatedAt": "2026-07-30T00:00:00Z",
  "assets": {
    "ui.login.background": {
      "type": "image",
      "version": "1.0.0",
      "hash": "sha256:...",
      "url": "https://assets.example.com/objects/...",
      "fallback": "ui.login.background.classic"
    }
  }
}
```

The roBrowserLegacy integration will eventually request logical asset IDs through an `AssetRegistry`/`AssetResolver` rather than hard-coded physical paths.

## 10. Data Flow

### 10.1 Asset Change

```text
Admin edits asset
→ validate record
→ save draft state
→ append audit event
→ include asset in next draft release
```

### 10.2 Theme Change

```text
Admin selects logical asset and tokens
→ validate referenced assets
→ save theme profile
→ append audit event
→ release references theme profile version
```

### 10.3 Production Promotion

```text
Admin validates draft release
→ validation passes
→ promote to staging
→ promote to production
→ update environment release pointer
→ append audit event
→ export production manifest
```

### 10.4 Rollback

```text
Admin selects prior validated release
→ confirm rollback
→ update environment pointer
→ append audit event
→ export previous manifest as active
```

## 11. Error Handling

The application distinguishes:

- form validation errors;
- manifest validation errors;
- storage read/write errors;
- import schema errors;
- invalid release-state transitions;
- missing preview assets;
- unresolved logical asset references; and
- service-health fetch failures.

Rules:

- failed writes do not partially update state;
- failed imports preserve the current state;
- release promotion is blocked on validation failure;
- errors are shown with an actionable cause;
- no destructive operation is triggered by a failed UI request; and
- audit events record failed administrative attempts where appropriate.

## 12. Security Design

### MVP

- development-only local administrator mode;
- no production credentials;
- no direct rAthena/database access;
- no destructive service commands;
- no secrets in source or exported JSON.

### Production Requirements

- MFA;
- role-based access control;
- Owner IP allowlist or Zero Trust access;
- short-lived sessions;
- re-authentication for high-impact actions;
- server-side immutable audit logs;
- secret manager;
- CSRF protection;
- restrictive CORS;
- Content Security Policy;
- rate limiting;
- two-person approval for critical production releases; and
- encrypted backup and restore procedures.

## 13. Deployment Design

### Local Development

- Windows-native workspace;
- Vite development server;
- optional Docker Desktop for dependent services;
- static mock data and local storage.

### Singapore Closed Alpha

```text
Singapore VPS
├── reverse proxy
├── player portal/client
├── WSS gateway
├── rAthena
├── MariaDB
├── Workbench static frontend
└── automated backup

External object storage/CDN
└── client and asset files
```

The Workbench should be protected by VPN or Zero Trust access rather than exposed as a normal public site.

### Public Production

- separate public and admin entry points;
- managed or dedicated database;
- external object storage and CDN;
- redundant gateway instances when justified;
- separate observability and backup services; and
- private network connectivity to rAthena.

## 14. Testing Strategy

### Unit Tests

- asset validation;
- logical ID uniqueness;
- fallback-cycle detection;
- theme-reference validation;
- release-state transitions;
- manifest generation;
- import/export migrations;
- audit event creation.

### Component Tests

- asset form;
- theme editor;
- release validation display;
- rollback confirmation;
- environment switcher;
- filtering and search.

### End-to-End Tests

1. create an asset;
2. select it as login background;
3. create a draft release;
4. validate it;
5. promote to staging;
6. promote to production;
7. export the manifest;
8. roll back to the previous release; and
9. verify audit history.

### Quality Gates

- TypeScript strict mode;
- lint and formatting pass;
- unit and component tests pass;
- production build succeeds;
- no secrets in build output;
- responsive at desktop and tablet widths;
- keyboard-accessible primary navigation;
- import/export round-trip test passes.

## 15. Acceptance Criteria

The MVP is complete when:

1. Dashboard works on desktop and tablet.
2. Assets can be created, edited, previewed, searched, and filtered.
3. Login background and theme profile can be changed without editing source files.
4. A schema-valid manifest JSON can be generated.
5. Releases can be created and promoted through valid states.
6. Production can be rolled back to a prior validated release.
7. Every state-changing action creates an audit record.
8. Configuration can be exported and imported safely.
9. A static production build succeeds.
10. A Docker image or equivalent static hosting package is available.
11. The architecture permits replacing local repositories with server APIs.
12. No MVP action can directly damage rAthena or its database.

## 16. Future Extensions

After the MVP and security foundation:

- real authentication and RBAC;
- PostgreSQL persistence;
- object-storage upload and provenance scanning;
- CDN purge and release pointer automation;
- roBrowserLegacy AssetResolver integration;
- live gateway and rAthena metrics;
- map and entity preview studios;
- server configuration adapters;
- GM tools;
- economy monitoring;
- safe script reload;
- backup/restore workflows;
- approval workflows; and
- multi-region deployment support.

## 17. Final Architectural Decision

ROWeb Operations Workbench will be implemented as a private React/TypeScript Web application with a local adapter-based persistence layer for the MVP. It will manage logical assets, themes, immutable manifests, releases, rollback pointers, environment profiles, runtime read models, and audit history.

It will not directly control destructive game-server operations until authentication, authorization, audit, approval, and safe server adapters are implemented. The design prioritizes a complete and testable asset-release workflow over a broad but unsafe administrative dashboard.
