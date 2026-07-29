# ROWEB AI Handoff - WP4A Closed, WP4B Next

Date: 2026-07-29  
Intended successor: Kimi K3 or another autonomous coding agent  
Current canonical WP4A branch: `codex/wp4a-authoritative-compatibility`  
Current canonical WP4A commit: `e161075640e4af6edfaaf1f04d929f57d5795544`

## Read this first

The immediate next package is WP4B: authenticated Portal session to rAthena
character lobby and browser-visible character list.

Do not begin by redesigning assets, changing PACKETVER, or implementing
browser-side username/password handling. WP3 is accepted for the login-screen
gate and WP4A has closed the authoritative rAthena mismatch.

Before editing:

1. Read every applicable `AGENTS.md`.
2. Read `docs/COMPATIBILITY_PROFILE.md` and `docs/RISK_REGISTER.md` from the
   WP4A branch.
3. Inspect all worktrees and dirty state.
4. Preserve the dirty main ROWEB checkout and all existing worktree WIP.
5. Create an isolated branch/worktree for any new integration lane.

## Canonical paths

| Purpose | Path |
| --- | --- |
| Product workspace | `C:\Ragnarok-Prontera\HermesWorkSpace\ROWEB` |
| WP4A verified worktree | `C:\Ragnarok-Prontera\HermesWorkSpace\.worktrees\roweb-wp4a-compatibility` |
| Legacy production client lane | `C:\Ragnarok-Prontera\HermesWorkSpace\.worktrees\roweb-wp0-legacy-baseline` |
| WP2/WP3 asset-server lane | `C:\Ragnarok-Prontera\HermesWorkSpace\.worktrees\roweb-wp2-asset-server` |
| Portal/gateway reference lane | `C:\Ragnarok-Prontera\HermesWorkSpace\.worktrees\roweb-portal-ticket-bff` |
| Legacy client reference | `C:\Ragnarok-Prontera\HermesWorkSpace\roBrowserLegacy` |
| Authoritative rAthena | `C:\Ragnarok-Prontera\rathena` |
| Generated evidence/assets | `C:\Ragnarok-Prontera\Generated` |

## Workspace state at handoff

### Canonical ROWEB main

- Branch: `main`
- Commit: `d8a044e80627518423d2c51c431f38efda055927`
- Dirty Foundation WIP exists.
- Modified: `README.md`, `docs/ARCHITECTURE.md`,
  `docs/IMPLEMENTATION_PLAYBOOK.md`.
- Untracked Foundation files include `.gitignore`, `baselines`, `config`,
  compatibility/migration docs, tests, and tools.
- Treat this checkout as read-only until its owner reconciles the WIP.

### WP4A compatibility lane

- Branch: `codex/wp4a-authoritative-compatibility`
- Commit: `e161075640e4af6edfaaf1f04d929f57d5795544`
- Worktree clean at handoff.
- This is the approved source for the active compatibility profile and risk
  register.

### Legacy production client lane

- Branch: `codex/wp1-production-mode`
- Commit before WIP: `e84bfdcdadb791ba18fb501943e8e992ba8f646a`
- Contains uncommitted WP1 production configuration, gateway transport,
  production app, tests, and TLS runner work.
- Do not reset, discard, or overwrite this worktree.

### WP2/WP3 asset lane

- Branch: `codex/wp2-asset-server`
- Commit before WIP: `d8a044e80627518423d2c51c431f38efda055927`
- Contains uncommitted asset server, WP3 publisher, tests, and documentation.
- Published assets are external to Git.
- Do not republish or reopen WP3 unless browser character/map rendering proves
  a specific missing dependency.

### Portal/gateway reference lane

- Branch: `codex/wp1-portal-ticket-bff`
- Commit before current WIP: `1270cd6657a6dd650b59aafa905182984af03269`
- Modified files:
  - `03-server/portal/Ragnarok.Portal.Launch/Program.cs`
  - `03-server/portal/Ragnarok.Portal.Launch.IntegrationTests/IntegrationTestProgram.cs`
  - `progress.md`
- The browser-safe launch-ticket BFF work is not committed in this lane.
- Older tests and reports in this repository may still reference rAthena
  `7f080871...`. That profile is historical and must not be used as WP4B
  authority.

### Authoritative rAthena

- Path: `C:\Ragnarok-Prontera\rathena`
- State: detached HEAD, tracked-clean, shallow checkout
- Commit: `0c3ca757ad35fff003130a8441a10f27cccd0ed9`
- `origin/master` and public `rathena/rathena master` resolved to this commit at
  WP4A verification time.
- MariaDB smoke service was still listening on loopback port `3307` at handoff.
- Login, character, and map servers were stopped after smoke; ports 6900, 6121,
  and 5121 had no remaining listeners.

## Completed packages

### WP0 - reproducible legacy baseline

- Isolated roBrowserLegacy baseline and Map Viewer build were established
  without modifying the original WIP.

### WP1 - production application mode foundation

- Environment-driven asset/WSS configuration exists in the legacy production
  client lane.
- GRF-selection UI is disabled only in production mode.
- Development Map Viewer remains available.
- Gateway transport uses `/gateway?destination=...&ticket=...` and subprotocol
  `ragnarok-web.v1`.
- Portal browser launch-ticket endpoint work exists as uncommitted WIP.

### WP2 - asset server

- Manifest-published external asset root.
- HTTPS-capable local server.
- Exact-origin CORS, immutable ETag, byte-range support, traversal rejection,
  startup size/hash validation, health and bounded metrics.

### WP3 - published asset closure

- Accepted as complete for the login-screen gate.
- Bootstrap/login UI and Prontera plus `prt_fild08` dependencies were published
  from an external asset workspace.
- Raw and licensed assets remain outside Git.
- No fake placeholder assets were introduced.
- WP2 manifest validation and strict `prt_fild08` closure passed.
- Browser production mode reached the real login UI.

Key evidence:

- `C:\Ragnarok-Prontera\Generated\wp3-e2e-evidence\production-login-ui.png`
- `C:\Ragnarok-Prontera\Generated\wp3-prontera-prt_fild08-20260729\manifest.json`
- `C:\Ragnarok-Prontera\Generated\wp3-prontera-prt_fild08-20260729\asset-registry.json`
- `C:\Ragnarok-Prontera\Generated\wp3-prt_fild08-20260729\manifest.json`

### WP4A - authoritative compatibility reconciliation

Risk `R-COMPAT-001` is `VERIFIED_CLOSED`.

Approved protocol:

| Field | Approved value |
| --- | --- |
| Source commit | `0c3ca757ad35fff003130a8441a10f27cccd0ed9` |
| PACKETVER | `20211103` |
| Client family | kRO `RagexeRE` |
| Gameplay | full Renewal |
| Packet shuffle | inactive |
| Packet obfuscation | macro defined, effective keys all zero, inactive |
| Map admission | `0x0436`, length 23, offsets `2,6,10,14,22` |
| Login port | `127.0.0.1:6900` |
| Character port | `127.0.0.1:6121` |
| Map port | `127.0.0.1:5121` |
| Database/codepage | MariaDB, `utf8mb4`, observed `utf8mb4_unicode_ci` |
| Character-name wire field | 24 bytes including null, 23-byte payload |
| Client text encoding | not explicitly pinned by rAthena |
| Game authentication | standard rAthena username/password |
| Web auth token | enabled, not a game-login replacement |

Approved binary identity:

| Binary | SHA-256 | ELF BuildID |
| --- | --- | --- |
| login-server | `9dc1c96f92ab2fd6f9d8fc70a9174ca62d6b8d9cfbd52270304e608c2e9f5f29` | `9ce3b11d2a8229892ffc7134cf27e77f6eee34eb` |
| char-server | `ecd6d13c249cd9ee9dc7535b0646982900323a4fc036c50f2cba8f06dab7fe2d` | `fe8de7e2e17c1e14892601735fd939848ce882f4` |
| map-server | `33cbd5b8d82b7b10dd7a47a64d425f7f1afe0608ad374d7820401e19e7c93b30` | `eaf07397bfb59069ed593f5143fda6c04f8b633e` |

WP4A evidence:

- `C:\Ragnarok-Prontera\Generated\wp4a-compatibility\rathena-binary-provenance.json`
- `C:\Ragnarok-Prontera\Generated\wp4a-compatibility\controlled-rebuild-final.stdout.log`
- `C:\Ragnarok-Prontera\Generated\wp4a-compatibility\rathena-runtime-smoke-final.log`

The final runtime smoke:

- verified the exact prebuilt hashes before startup;
- opened loopback ports 6900, 6121, and 5121;
- observed char-server registration with login-server;
- observed map-server ready;
- used no `FORCE` or compatibility bypass;
- identity-safely stopped all three servers.

## Primary next objective - WP4B

Implement the smallest secure authenticated lobby path that renders the real
character list in the actual ROWEB browser.

Do not implement a broad gameplay session framework before the following
contract is proven.

### Required acceptance criteria

1. An unauthenticated launch request returns HTTP 401.
2. An authenticated Portal session is required.
3. One Portal session is bound to exactly one rAthena account.
4. The browser never receives the game password.
5. The issuer capability remains server-side.
6. The character list returned to the browser is sanitized.
7. Character ownership is validated server-side.
8. A map capability is one-time, short-lived, audience-bound, and
   character-bound.
9. Replaying a consumed capability fails.
10. An expired capability fails.
11. Logs contain no game credentials, issuer secrets, launch tickets, or
    authentication tokens.
12. The real character list is shown in the actual production-mode browser.

### Required server-side session fields

The design should explicitly define and test at least:

- Portal session ID or opaque session handle;
- authenticated Portal subject ID;
- bound rAthena account ID;
- authorization/session creation and expiration timestamps;
- server-side rAthena credential or credential reference;
- character-lobby state;
- selected character ID;
- destination/audience;
- one-shot capability ID;
- capability issuance, expiration, and consumption state;
- correlation ID safe for logs.

Do not expose internal account/session keys in browser DTOs.

### Sanitized character DTO

Define the minimum browser DTO needed by the real character-selection UI, for
example:

- public character ID or opaque character handle;
- slot;
- display name;
- class/job;
- base/job levels;
- sex/body/hair presentation fields required for rendering;
- last map display information only when safe;
- selection eligibility.

Exclude account ID, login IDs, session tokens, password material, map auth
tokens, database fields, and operator-only state.

### One-shot map capability

The capability must be:

- generated and retained server-side;
- random and unguessable;
- single-use with atomic consume semantics;
- short-lived;
- bound to the authenticated Portal session;
- bound to the rAthena account;
- bound to exactly one owned character;
- audience-bound to the intended gateway/map transition;
- unusable after logout or session revocation;
- redacted from logs.

The browser may receive only the opaque one-shot handle required to continue
the authorized transition. It must never receive the capability issuer secret
or game password.

## Security blocker to address first

Stock rAthena `src/web/auth.cpp` logs the submitted web-auth token when token
verification fails:

```text
ShowWarning("Request with AID %d and token %s unverified\n", account_id, token);
```

Do not use this endpoint with production credentials until the logging path is
redacted or the WP4B architecture avoids sending a credential through it.

Any rAthena modification must be a narrow, reviewed change against the
authoritative commit. Do not alter PACKETVER, packet layout, gameplay mode, or
unrelated rAthena work.

## Prohibited actions

- Do not use `FORCE=1` or any compatibility bypass.
- Do not change PACKETVER to make tests pass.
- Do not reset or discard any dirty checkout.
- Do not clone a different rAthena checkout.
- Do not send username/password from browser JavaScript.
- Do not place game passwords, gateway issuer keys, database credentials, or
  web-auth tokens in runtime environment files served to the browser.
- Do not return raw rAthena character/account structures to the browser.
- Do not trust browser-supplied account ID or character ownership.
- Do not make map capabilities reusable or long-lived.
- Do not log secrets in success or failure paths.
- Do not modify raw or licensed assets.
- Do not reopen WP3 without direct missing-asset evidence from character/map
  rendering.
- Do not claim production E2E playability until the browser visibly completes
  login, character selection, map entry, and rendering.

## Compatibility verification commands

Run from:

```text
C:\Ragnarok-Prontera\HermesWorkSpace\.worktrees\roweb-wp4a-compatibility
```

Contract tests:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected:

```text
Ran 9 tests
OK
```

Authoritative validator:

```powershell
python tools\wp4a\verify_rathena_compatibility.py `
  --profile config\rathena-compatibility.json `
  --rathena C:\Ragnarok-Prontera\rathena `
  --evidence C:\Ragnarok-Prontera\Generated\wp4a-compatibility\rathena-binary-provenance.json
```

Expected:

```text
PASS_RATHENA_AUTHORITATIVE_COMPATIBILITY
```

Explicit bypass rejection:

```powershell
$env:FORCE = "1"
python tools\wp4a\verify_rathena_compatibility.py `
  --profile config\rathena-compatibility.json `
  --rathena C:\Ragnarok-Prontera\rathena `
  --evidence C:\Ragnarok-Prontera\Generated\wp4a-compatibility\rathena-binary-provenance.json
Remove-Item Env:\FORCE
```

Expected failure:

```text
FAIL_RATHENA_AUTHORITATIVE_COMPATIBILITY: compatibility bypass enabled: FORCE
```

## Suggested WP4B test order

1. Lock existing Portal and gateway behavior with their current executable
   integration tests.
2. Add contract tests for 401 and authenticated session binding.
3. Add server-side account binding and sanitized DTO tests.
4. Add ownership rejection tests before character selection implementation.
5. Add one-shot capability tests: valid consume, replay, expiry, wrong
   audience, wrong character, wrong Portal session, logout/revocation.
6. Add automated log scanning with planted canary secrets.
7. Integrate with the authoritative rAthena profile and disposable MariaDB.
8. Run production Portal HTTPS and gateway WSS with secrets held server-side.
9. Connect the legacy production client through the Portal endpoint.
10. Use a clean browser profile and capture visible character-list evidence.
11. Only after the real character list passes, proceed to map capability
    consumption and browser map-entry/render evidence.

## Definition of WP4B done

WP4B is complete only when all required acceptance criteria pass with command
output and browser evidence, compatibility validation still passes, no bypass
is enabled, logs are proven credential-free, cleanup is complete, and the
central risk register is updated.

Passing server-side tests alone is not proof that the browser character list is
working. Passing character selection alone is not proof that the game is
production E2E playable.

## Copy-paste prompt for the next AI

```text
Continue ROWEB from the verified WP4A handoff:

C:\Ragnarok-Prontera\HermesWorkSpace\.worktrees\roweb-wp4a-compatibility\docs\AI_HANDOFF_WP4A_TO_WP4B_2026-07-29.md

Primary objective: implement WP4B secure authenticated Portal lobby against
rAthena commit 0c3ca757ad35fff003130a8441a10f27cccd0ed9 and PACKETVER
20211103.

Read all applicable AGENTS.md files first. Preserve every dirty worktree. Do
not use FORCE or a compatibility bypass. Do not expose game credentials or
issuer secrets to browser code. Use an isolated branch/worktree.

Acceptance criteria:
- unauthenticated launch returns 401;
- authenticated Portal session required;
- Portal session bound to one rAthena account;
- browser never receives game password;
- issuer capability remains server-side;
- character list sanitized;
- character ownership validated server-side;
- map capability one-time, short-lived, audience-bound, character-bound;
- replay fails;
- expiry fails;
- logs contain no credentials;
- real character list appears in the actual production-mode browser.

Run the WP4A validator before implementation and again after implementation.
Do not reopen WP3 except for direct evidence of missing character/map assets.
Do not declare production E2E playable until browser login, character
selection, map entry, and rendering are all visibly proven.
```
