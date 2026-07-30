# rAthena Admin Studio M1 Mockup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a dependency-free interactive M1 mockup of the admin-only rAthena control plane without connecting to production services.

**Architecture:** A static HTML/CSS/JavaScript application under `apps/admin-studio/mockup`. Synthetic datasets drive all views; mutations are represented only as typed dry-run commands appended to an in-memory audit ledger.

**Tech Stack:** HTML5, CSS, vanilla JavaScript and Python/pytest smoke tests.

## Global Constraints

- rAthena remains authoritative for gameplay and persistence.
- No browser-to-rAthena, browser-to-MariaDB, SQL console, shell console or unrestricted AtCommand.
- All operational data is explicitly marked simulated.
- No licensed Ragnarok assets are committed.
- The mockup runs from a static HTTP server without package installation.

---

### Task 1: Static application shell

**Files:**
- Create: `apps/admin-studio/mockup/index.html`
- Test: `tests/test_admin_studio_mockup.py`

- [x] Build responsive navigation and dashboard layouts.
- [x] Add Command Center, Player Operations, Economy, Anti-abuse and Audit views.
- [x] Add explicit simulated/read-only safety copy.

### Task 2: Synthetic data and guarded interactions

**Files:**
- Modify: `apps/admin-studio/mockup/index.html`
- Test: `tests/test_admin_studio_mockup.py`

- [x] Render service, map, economy, player activity and audit data from synthetic fixtures.
- [x] Implement typed dry-run command previews.
- [x] Append confirmed dry-runs only to the in-memory audit table.
- [x] Verify the mockup has no network or database connection primitive.

### Task 3: Documentation and verification

**Files:**
- Create: `apps/admin-studio/mockup/README.md`
- Create: `docs/admin-studio/M1_MOCKUP.md`

- [x] Document local run and verification commands.
- [x] Document safety boundaries and rollback.
- [x] Run four Python smoke tests locally.
- [x] Run JavaScript syntax validation locally.
- [x] Publish on a feature branch and open a pull request.
