---
name: robrowser-client-engineering
description: Use for roBrowserLegacy bootstrap, map/entity rendering, input, animation, packet handlers, audio, camera, HUD integration, or browser runtime failures.
version: 1.0.0
owners: [ROWEB]
tags: [robrowser, browser, webgl]
---

# roBrowserLegacy Client Engineering

## Constraints

Work from the pinned roBrowserLegacy commit. Prefer adapting verified runtime behavior over reimplementation. Keep modern UI in DOM/CSS where practical. Do not make the browser authoritative or require player GRF uploads in production.

## Workflow

1. Reproduce in a clean browser profile and record URL, browser, commit, console, network, and visual evidence.
2. Trace bootstrap, resource path, packet handler, entity state, renderer, input, and UI ownership.
3. Classify the failure: asset, protocol, state, render, timing, browser compatibility, cache, or UI overlay.
4. Implement the smallest isolated change.
5. Add deterministic unit tests plus browser E2E or visual regression for the affected path.
6. Test fresh load, cached reload, reconnect, resize, keyboard, and representative desktop/mobile viewport.
7. Record performance impact and rollback.

## Acceptance evidence

Build output, test output, console/network logs, before/after screenshots using approved or synthetic content, cache behavior, and exact runtime path exercised.