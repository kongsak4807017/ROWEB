# Unified Player Experience Workbench Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Merge the existing rAthena Admin Studio and Player Experience editor into one static, testable Operations Workbench entry point.

**Architecture:** Keep the current Admin Studio screens and simulated safety boundary, add Player Experience views to the same navigation shell, and persist UI-profile drafts and audit events in browser localStorage. The static MVP loads the checked-in profile JSON, previews desktop/mobile layouts, validates profile data, and records publish/rollback actions without mutating rAthena, MariaDB, roBrowserLegacy, or private assets.

**Tech Stack:** HTML5, CSS, vanilla JavaScript, JSON, Python pytest smoke tests.

## Global Constraints

- Preserve all existing Admin Studio views and dry-run behavior.
- Add no production API, SQL, WebSocket, shell, or unrestricted AtCommand integration.
- Keep licensed assets outside Git.
- Support Desktop, Mobile Landscape, and Mobile Portrait previews.
- Every profile mutation must create a Unified Audit record.
- `apps/admin-studio/mockup/index.html` becomes the unified entry point only after tests pass.

---

### Task 1: Unified application shell

**Files:**
- Create: `apps/admin-studio/mockup/unified-workbench.html`
- Test: `tests/test_unified_player_experience_workbench.py`

**Interfaces:**
- Produces navigation targets `command`, `players`, `economy`, `security`, `player-ui`, `mobile-controls`, `releases`, and `audit`.

- [ ] Write smoke tests asserting every navigation target has a matching view.
- [ ] Assert the existing Admin Studio labels remain present.
- [ ] Implement the unified sidebar and preserve the simulated-data notice.
- [ ] Run `python -m pytest tests/test_unified_player_experience_workbench.py -q`.
- [ ] Commit `feat: add unified operations workbench shell`.

### Task 2: Player UI Studio and device preview

**Files:**
- Modify: `apps/admin-studio/mockup/unified-workbench.html`
- Create: `apps/admin-studio/mockup/player-ui-profiles.json`
- Test: `tests/test_unified_player_experience_workbench.py`

**Interfaces:**
- Consumes profile keys `desktop-v1`, `mobile-landscape-v1`, and `mobile-portrait-v1`.
- Produces `loadProfile(profileId)`, `applyInspector()`, and `renderDevicePreview()`.

- [ ] Add tests for device selector, scene selector, component inspector, and profile JSON schema.
- [ ] Add Desktop, Mobile Landscape, and Mobile Portrait profiles.
- [ ] Implement component selection, X/Y, width, scale, opacity, anchor, and visibility controls.
- [ ] Implement HUD, minimap, target, chat, hotbar, joystick, and mobile action-button previews.
- [ ] Run focused tests and commit `feat: integrate player UI studio`.

### Task 3: Mobile Control Studio

**Files:**
- Modify: `apps/admin-studio/mockup/unified-workbench.html`
- Test: `tests/test_unified_player_experience_workbench.py`

**Interfaces:**
- Produces mobile binding records for movement, target, attack, skills, camera rotate, and camera zoom.

- [ ] Add tests asserting all required mobile controls are represented.
- [ ] Implement control enable/disable, size, opacity, skill count, and binding preview.
- [ ] Keep all interactions presentation-only and packet-compatible by description.
- [ ] Run focused tests and commit `feat: add mobile control studio`.

### Task 4: Draft, validation, release, rollback, and audit

**Files:**
- Modify: `apps/admin-studio/mockup/unified-workbench.html`
- Test: `tests/test_unified_player_experience_workbench.py`

**Interfaces:**
- Produces `saveDraft()`, `validateProfile()`, `publishProfile()`, `rollbackProfile()`, and `appendAudit()`.

- [ ] Add tests for buttons, validation checklist, release history, rollback, and audit ledger.
- [ ] Persist drafts, releases, and audit events in localStorage.
- [ ] Validate required components, touch target size, safe area, Damage/MISS binding, attack-sound binding, and ItemInfo source.
- [ ] Block publish when validation fails.
- [ ] Record every state change in Unified Audit.
- [ ] Run focused tests and commit `feat: add UI profile release workflow`.

### Task 5: Default entry point and verification

**Files:**
- Modify: `apps/admin-studio/mockup/index.html`
- Modify: `apps/admin-studio/mockup/README.md`
- Test: `tests/test_unified_player_experience_workbench.py`

**Interfaces:**
- `index.html` redirects to `unified-workbench.html` while retaining a direct legacy link.

- [ ] Add tests asserting the default entry points to the unified page.
- [ ] Update local run instructions.
- [ ] Run `python -m pytest tests/test_admin_studio_mockup.py tests/test_unified_player_experience_workbench.py -q`.
- [ ] Run JavaScript syntax validation with `node --check` on extracted scripts when Node is available.
- [ ] Run `git diff --check` and inspect changed files for secrets and licensed assets.
- [ ] Commit `feat: make unified workbench the admin entry point`.

## Completion Gate

The feature is complete only when the original Admin Studio views remain available, Player Experience can switch among all three device profiles, the inspector visibly updates components, Mobile Controls are editable, draft/validate/publish/rollback operate locally, all mutations appear in Unified Audit, the default URL opens the unified page, and the smoke tests pass.