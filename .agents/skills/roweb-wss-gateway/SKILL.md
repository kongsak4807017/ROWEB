---
name: roweb-wss-gateway
description: Use for browser WSS, wsProxy, TCP bridging, session binding, backpressure, reconnect, TLS, or login-to-map handoff.
version: 1.0.0
owners: [ROWEB]
tags: [websocket, gateway, networking]
---

# ROWEB WSS Gateway

## Invariants

The gateway transports gameplay packets; it does not own gameplay state. Asset traffic never traverses it. Binary payloads must remain byte-exact unless an explicitly tested protocol adapter requires transformation.

## Workflow

1. Map browser → TLS termination → gateway/load balancer → wsProxy → rAthena process transitions.
2. Define session identity, destination selection, lifecycle, heartbeat, timeout, reconnect, and map-server handoff.
3. Test fragmentation, coalescing, partial TCP reads, backpressure, slow consumer, abrupt close, upstream reset, and retry limits.
4. Add per-stage metrics and structured logs without credentials or packet secrets.
5. Validate direct baseline against proxied behavior with golden fixtures.
6. Run connection churn, sustained traffic, and fault-injection tests.
7. Document deployment, health checks, graceful drain, rollback, and capacity limits.

## Security requirements

TLS in production, origin policy, authentication binding, connection/rate limits, bounded buffers, input length validation, redaction, and denial-of-service controls.

## Evidence

Protocol equivalence tests, reconnect/handoff E2E, load profile, latency percentiles, memory behavior, failure recovery, and rollback drill.