# Unified Player Experience Workbench Handoff

## Status

Implemented on branch:

```text
feature/unified-player-experience-workbench
```

## Entry point

```text
apps/admin-studio/mockup/index.html
```

The entry point redirects to:

```text
apps/admin-studio/mockup/unified-workbench.html
```

## Included

- existing Command Center, Player Operations, Economy Studio, and Anti-abuse views;
- Player UI Studio;
- Desktop, Mobile Landscape, and Mobile Portrait previews;
- scene and EP01–EP17 selectors;
- component inspector;
- Mobile Control Studio;
- checked-in profile JSON;
- local draft, validation, publish, rollback, and Unified Audit workflows;
- smoke tests and JavaScript syntax validation test.

## Verification command

```powershell
python -m pytest tests/test_admin_studio_mockup.py tests/test_unified_player_experience_workbench.py -q
```

## Local run after merge or checkout

```powershell
py -m http.server 4173 --directory apps/admin-studio/mockup
```

Open:

```text
http://127.0.0.1:4173/
```

## Safety boundary

This is a static operational MVP. It stores edits and audit events only in browser localStorage and does not mutate rAthena, MariaDB, roBrowserLegacy, or private assets.