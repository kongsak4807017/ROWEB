# ROWEB Skill Authoring Standard

## Purpose

This standard allows an AI agent to create or extend ROWEB skills without producing vague prompt collections.

## Required front matter

```yaml
---
name: kebab-case-name
description: Use when ...
version: 1.0.0
owners: [ROWEB]
tags: [roweb]
---
```

The description must state observable triggers. Avoid descriptions such as "helps with games".

## Required sections

1. Purpose
2. Use when
3. Do not use when
4. Required context
5. Non-negotiable constraints
6. Workflow
7. Deliverables
8. Verification
9. Failure and rollback
10. Handoff
11. References

## Workflow design rules

- Use numbered, executable steps.
- Separate investigation, design, implementation, and verification.
- Name the evidence that proves each acceptance criterion.
- Require exact paths, versions, commits, commands, and runtime observations where relevant.
- Prefer deterministic scripts and machine-readable reports.
- Do not allow "looks correct" as verification.
- Use synthetic fixtures for copyrighted formats and content.

## ROWEB-specific safety rules

Every skill touching Ragnarok data or runtime must inherit these rules:

- No GRF or extracted licensed assets in Git.
- No secrets, account credentials, private keys, or production database dumps.
- rAthena remains authoritative.
- Browser code does not fabricate authoritative state.
- Asset traffic remains separate from gameplay traffic.
- PACKETVER and protocol behavior are verified, not inferred.
- Capacity claims require measured evidence.

## Skill quality gate

Before adding or changing a skill, verify:

- Trigger is specific and non-overlapping.
- Inputs and outputs are explicit.
- Workflow can be executed by an unfamiliar agent.
- Validation is reproducible.
- Destructive steps have rollback.
- References are primary or pinned where possible.
- No instruction conflicts with `/AGENTS.md`.
- No placeholders, TODOs, or unsupported claims remain.

## Versioning

- Patch: wording, examples, non-behavioral corrections.
- Minor: backward-compatible workflow or validation additions.
- Major: changed triggers, required outputs, or incompatible workflow.

## Creating another skill

1. Read `/AGENTS.md`, this standard, the router, and adjacent skills.
2. Search for overlap before creating a new directory.
3. Use `templates/SKILL.template.md`.
4. Add the skill to the catalog and router.
5. Add a realistic invocation example.
6. Self-review against the quality gate.
7. Open a PR with scope, rationale, validation, and rollback notes.