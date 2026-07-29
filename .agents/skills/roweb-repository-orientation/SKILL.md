---
name: roweb-repository-orientation
description: Use when an agent is new to ROWEB, the task crosses directories, or the current implementation state is unclear.
version: 1.0.0
owners: [ROWEB]
tags: [roweb, repository, orientation]
---

# ROWEB Repository Orientation

## Workflow

1. Read the mandatory documents listed in `/AGENTS.md`.
2. Record default branch, current branch, HEAD, dirty files, recent commits, open PR context, and active work package.
3. Read `compatibility.lock.json`; record pinned roBrowserLegacy/rAthena commits, packet status, workspace roots, and asset policy.
4. Map relevant directories, entrypoints, scripts, tests, generated files, local-only runtime paths, and deeper contracts.
5. Trace the requested behavior end to end before changing anything.
6. Identify authoritative source, external dependencies, unknowns, and acceptance evidence.
7. Produce a scope map: files likely to change, files explicitly out of scope, risks, and selected skills.

## Constraints

- Do not modify vendor checkouts or assets unless the task explicitly requires a reproducible upstream patch workflow.
- Do not confuse local runtime state with Git-tracked source.
- Do not infer completion from documentation status.

## Deliverable

A concise orientation report containing refs, architecture path, affected contracts, unknowns, risks, selected skills, and next executable action.