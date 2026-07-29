---
name: roweb-skill-author
description: Use when creating, splitting, merging, reviewing, or upgrading an AI skill for ROWEB.
version: 1.0.0
owners: [ROWEB]
tags: [roweb, skills, governance]
---

# ROWEB Skill Author

## Required context

Read `/AGENTS.md`, the skill catalog, authoring standard, template, router, and adjacent skills.

## Workflow

1. Search existing skill names, triggers, outputs, and references for overlap.
2. Decide whether to extend, split, merge, or create; prefer extending unless triggers and outputs are materially different.
3. Define one observable trigger and one primary outcome.
4. Write required context, constraints, ordered workflow, deliverables, verification, rollback, and handoff.
5. Include ROWEB invariants: rAthena authority, roBrowser baseline, no asset bytes, no guessed protocol, evidence-gated capacity.
6. Add routing and catalog entries.
7. Run the quality gate in `SKILL_AUTHORING_STANDARD.md`.
8. Validate with at least one positive invocation and one negative routing example.

## Deliverables

- `SKILL.md`
- catalog/router update
- invocation examples
- version and rationale

## Rejection criteria

Reject skills that are generic prompt collections, duplicate an existing workflow, lack executable verification, permit unsupported claims, or conflict with `/AGENTS.md`.