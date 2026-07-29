# rAthena Capacity Plan — Target 5,000 Concurrent Players

## 1. Status of the target

5,000 CCU is a capacity objective, not an assumed capability. Approval requires measured evidence on the exact ROWEB, wsProxy, rAthena, scripts, database, maps, and infrastructure used in production.

## 2. Separate traffic classes

```text
Assets: Browser → HTTPS/CDN
Gameplay: Browser → WSS → wsProxy → rAthena
Persistence: rAthena → MariaDB
```

Asset traffic must not consume rAthena, wsProxy, or gameplay database capacity.

## 3. Scale units

Plan independent scale units:

- WSS load balancer
- wsProxy instances
- login-server
- char-server
- map-server processes
- MariaDB
- static asset hosting/CDN

The map-server path is expected to be the primary gameplay constraint; wsProxy and SQL can independently become bottlenecks and must be measured.

## 4. Map-server strategy

Investigate multiple map-server processes partitioned by map groups, for example:

```text
map-server-a: Prontera + novice + nearby fields
map-server-b: Payon region
map-server-c: Geffen region
map-server-d: dungeons/instances/events
```

Before production, verify cross-server behavior for:

- map transfer
- party and guild
- whispers and global communication
- world variables
- vending
- instances
- persistence and reconnect

Do not assume legacy multi-map-server behavior is complete for the selected fork.

## 5. Resource reduction program

### Content and scripts

- load only enabled maps and NPC scripts
- remove test/debug/duplicate events
- detect `query_sql` in timers and loops
- cache or batch repeated lookups
- remove global broadcasts where area scope is sufficient
- budget monster density and AI timers per map
- stagger periodic saves

### Logging

- disable packet/movement debug logging in production
- retain critical economy, GM, trade, storage, and error logs
- use asynchronous rotation and separate log I/O

### Database

- use NVMe-backed InnoDB
- size buffer pool from measured working set
- verify indexes from slow-query evidence
- separate or control high-volume log tables
- avoid synchronized autosave bursts
- test backup/restore under load

### Gateway

- multiple wsProxy instances
- sticky connections
- explicit backpressure and queue limits
- ping/pong and idle timeout
- graceful draining
- connection, packet, byte, queue, and event-loop metrics

## 6. Performance budgets

Initial engineering objectives, subject to benchmark refinement:

```text
sustained CPU per critical process: < 70%
short spike ceiling: < 85%
internal gateway latency p99: < 30 ms
critical SQL latency p99: < 50 ms
map/gameplay processing p99: < 50 ms
unexpected disconnect rate: < 0.5%
```

These are program targets, not rAthena guarantees.

## 7. Load model

A valid test must simulate behavior, not idle sockets.

Suggested mix:

```text
20% town/idle/chat
25% walking and map movement
15% single-target combat
15% AoE combat
10% NPC/shop/storage
5% vending
5% login/character switching
5% warp/map transitions
```

Hotspot scenarios:

- 1,000 users in Prontera
- large AoE event
- mass reconnect after gateway restart
- vending concentration
- party/guild/global communication burst
- SQL slowdown and recovery

## 8. Staged capacity ladder

```text
250
500
1,000
2,000
3,500
5,000
6,500–7,500 overload validation
```

At each stage:

- ramp gradually
- hold 30–60 minutes minimum
- record p50/p95/p99
- capture CPU, memory, I/O, DB, gateway, and gameplay metrics
- identify the first saturated component
- change one variable at a time

After 5,000 passes, run an 8–24 hour soak test.

## 9. Observability requirements

### rAthena/game

- online users by service and map
- CPU/RSS per process
- timer/script latency
- packet rates
- save latency and errors
- entity and monster counts
- map transfer and disconnect failures

### wsProxy

- active WebSockets
- connections and reconnects per second
- event-loop lag
- queue depth/backpressure
- upstream TCP latency
- packet and byte rates

### MariaDB

- queries per second
- slow queries
- buffer-pool hit ratio
- active connections
- lock waits
- disk latency
- replication status if used

### Browser

- FPS/frame time
- memory
- asset load latency/cache hit rate
- network RTT
- disconnect/reconnect outcomes

## 10. Failure and recovery tests

Capacity approval also requires:

- restart one wsProxy while traffic continues
- drain gateway connections
- restart one map-server group in a controlled test
- inject database latency
- simulate asset-manifest rollback
- simulate mass reconnect
- verify persistence integrity after shutdown/recovery

## 11. Infrastructure baseline for testing

A reasonable initial load lab may separate:

- game compute node(s)
- database node
- gateway node
- static asset/CDN service

Select high single-thread performance for map-server processes, sufficient cores for process isolation, adequate RAM, and NVMe storage. Final sizing must follow benchmark evidence rather than a generic hardware list.

## 12. Approval record

A 5,000 CCU release must publish:

```text
ROWeb build:
roBrowserLegacy commit:
rAthena commit/PACKETVER:
asset version:
infrastructure specification:
configuration hashes:
load generator/scenario:
test duration:
p50/p95/p99:
peak CPU/memory/I/O:
errors/disconnects:
recovery outcomes:
known limits:
approval:
```
