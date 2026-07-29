---
name: mmorpg-security
description: Use for authentication, authorization, abuse, botting, packet validation, item duplication, injection, secrets, privacy, or threat modeling.
version: 1.0.0
owners: [ROWEB]
tags: [security, abuse, mmorpg]
---

# MMORPG Security

## Trust model

Treat browser input, packets, asset paths, filenames, uploaded/admin content, and external callbacks as untrusted. rAthena validates authoritative actions. Security controls must not depend on hidden client code.

## Workflow

1. Identify assets, actors, entrypoints, trust boundaries, privileges, and worst credible impact.
2. Threat-model account takeover, replay, session fixation, packet tampering, speed/movement abuse, duplication, race conditions, SQL/script injection, path traversal, cache poisoning, denial of service, GM abuse, and secret leakage.
3. Add server-side validation, least privilege, bounded inputs/buffers, idempotency/transaction controls, rate limits, audit logs, and secure defaults.
4. Test positive, negative, boundary, concurrent, replay, malformed, and recovery cases in an authorized environment.
5. Redact credentials, tokens, personal data, packet secrets, and licensed content from evidence.
6. Define detection, containment, rollback, account/item recovery, and disclosure path.

## Deliverables

Threat model, security requirements, tests, abuse telemetry, residual risk, operational response, and verification that no secrets or licensed assets entered Git.