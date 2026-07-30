# rAthena Admin Studio — M1 Mockup

## Purpose

Demonstrate the information architecture and guarded interaction model for the proposed admin-only one-stop rAthena control plane.

## Included views

1. **Command Center** — process health, player load, map distribution, releases and operational signals.
2. **Player Operations** — synthetic account/character lookup and guarded administrative actions.
3. **Economy Studio** — Zeny sources, sinks, net injection and review indicators.
4. **Anti-abuse** — top continuous farmers with investigator-led review rather than automatic sanctions.
5. **Audit Ledger** — simulated append-only administrative action history.

## Safety boundary

The M1 mockup contains no API client, WebSocket client, SQL connector, shell command or raw AtCommand integration. All data is synthetic. Every mutating interaction is a typed dry-run preview that writes only to the in-memory mock audit table.

## Verification

```bash
python -m pytest tests/test_admin_studio_mockup.py -q
```

Manual smoke test:

```bash
python -m http.server 4173 --directory apps/admin-studio/mockup
```

Then open `http://localhost:4173` and verify navigation, responsive layout, player action dialogs, investigation dialogs and audit insertion.

## Rollback

The mockup is isolated under `apps/admin-studio/mockup`. Rollback is deletion of that directory plus this document and its smoke test. It does not modify roBrowserLegacy, rAthena, gateway or production deployment configuration.

## Next implementation slice

M2 should preserve this UI and replace one read-only panel at a time with authenticated Admin API contracts in staging, beginning with:

1. service health;
2. online session counts;
3. map population;
4. immutable read-audit events.

No mutating production command should be enabled until identity, MFA, capability policy, validation and audit persistence exist.