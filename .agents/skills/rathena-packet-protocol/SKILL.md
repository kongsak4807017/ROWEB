---
name: rathena-packet-protocol
description: Use for PACKETVER, login/char/map handshakes, opcodes, binary framing, packet parsing, disconnects, or client/server compatibility.
version: 1.0.0
owners: [ROWEB]
tags: [rathena, protocol, packets]
---

# rAthena Packet Protocol

## Non-negotiable rules

- Resolve PACKETVER from pinned source and runtime configuration; never guess.
- Capture only authorized test traffic and redact credentials/tokens.
- Preserve byte order, packet boundaries, lengths, state transitions, and server authority.

## Workflow

1. Reproduce with exact client/server/gateway commits and configuration.
2. Identify session phase: account login, server list, character login, character select, map handoff, or gameplay.
3. Trace opcode and structure in pinned rAthena and roBrowserLegacy sources.
4. Capture sanitized hex fixtures for request, response, fragmentation, coalescing, malformed length, and disconnect.
5. Build deterministic parser/serializer golden tests.
6. Verify direct TCP baseline where possible, then WSS/wsProxy equivalence.
7. Document compatibility matrix and failure classification.

## Deliverables

Protocol trace, verified PACKETVER, packet fixture inventory, state machine, tests, redaction statement, and rollback.