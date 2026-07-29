# WP0 Baseline Intake Runbook

## Scope

WP0 establishes a reproducible, pinned baseline for:

- `kongsak4807017/roBrowserLegacy`
- `kongsak4807017/rathena`
- the approved local asset root
- the browser demo and Map Viewer

WP0 does not yet implement production asset delivery, wsProxy integration, login, or the first playable vertical slice.

## Locked local paths

```text
ROWEB repository:
C:\Ragnarok-Prontera\HermesWorkSpace\ROWEB

Vendor checkouts:
C:\Ragnarok-Prontera\HermesWorkSpace\ROWEB\vendor

Approved asset source:
C:\Ragnarok-Prontera\assets\data

Runtime reports/logs/PIDs:
C:\Ragnarok-Prontera\runtime
```

Licensed asset bytes must remain outside Git.

## Prerequisites

- Windows PowerShell 5.1 or PowerShell 7+
- Git
- Node.js and npm compatible with the pinned roBrowserLegacy baseline
- Build dependencies required by the pinned rAthena repository
- Approved extracted assets at the configured asset root

## Bootstrap

From the ROWEB repository root:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\bootstrap-wp0.ps1
```

The script:

1. Reads `compatibility.lock.json`.
2. Creates the local vendor/runtime directories.
3. Clones roBrowserLegacy and rAthena when missing.
4. Checks out the exact pinned commits in detached-HEAD mode.
5. Installs roBrowserLegacy dependencies.
6. Runs `npm run build:all`.
7. Writes `C:\Ragnarok-Prontera\runtime\wp0-environment-report.json`.

To validate checkouts without reinstalling or rebuilding:

```powershell
.\scripts\bootstrap-wp0.ps1 -SkipInstall -SkipBuild
```

## Status check

```powershell
.\scripts\status-wp0.ps1
```

The status command exits non-zero until all mandatory checks pass. PACKETVER is intentionally blocking until verified from the pinned runtime configuration; it must not be guessed.

## Browser verification

After a successful build:

```powershell
cd .\vendor\roBrowserLegacy
npm run live
```

Exercise both:

- browser demo/application
- Map Viewer with approved local assets

Required evidence:

```text
runtime/wp0-environment-report.json
runtime/logs/robrowser-live.log
local screenshot: browser demo
local screenshot: Map Viewer
exact URL exercised
exact Node/npm/Git versions
exact pinned commits
```

Screenshots containing licensed art remain local unless separately approved for publication.

## Compatibility decisions still required

Before WP0 can become PASS:

1. Verify the PACKETVER/client date compatible with the pinned rAthena build.
2. Record the exact wsProxy implementation and commit intended for WP4.
3. Confirm roBrowserLegacy license obligations and attribution for public distribution.
4. Confirm the approved asset snapshot provenance and distribution rights.
5. Run the browser demo and Map Viewer on the target workstation.

## Acceptance record

Use this evidence block in the PR or handoff:

```text
status: PASS | FAIL | BLOCKED
commit/ref:
tests executed:
results:
artifacts/reports:
known limitations:
next executable action:
```

WP0 is PASS only when a fresh checkout builds and starts, the Map Viewer runs, the browser application runs, compatibility values are verified, and no asset bytes enter Git.
