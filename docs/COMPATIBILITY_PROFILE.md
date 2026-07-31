# Authoritative rAthena Compatibility Profile

WP4A locks ROWEB to `C:\Ragnarok-Prontera\rathena` at
`0c3ca757ad35fff003130a8441a10f27cccd0ed9`. The tracked checkout is clean,
shallow, and at detached HEAD; fork and upstream `master` resolve to that commit.

The machine-readable source of truth is
[`config/rathena-compatibility.json`](../config/rathena-compatibility.json).

## Effective protocol

- PACKETVER: `20211103` in source and CMake cache.
- Client family: kRO `RagexeRE`.
- Gameplay: full Renewal.
- Packet shuffle: inactive.
- Packet obfuscation: compile macro defined, but effective keys are three zero
  values, so packet-header obfuscation is inactive.
- Map admission: packet `0x0436`, length 23.
- Loopback ports: login 6900, character 6121, map 5121.
- Character names: fixed 24-byte null-terminated field, maximum 23 payload
  bytes. rAthena does not explicitly pin the client text encoding.
- Effective database connections use `utf8mb4`; observed database collation is
  `utf8mb4_unicode_ci`.

## Authentication and schema

There are no tracked custom-auth changes. Standard game username/password login
remains active. rAthena web-auth-token support is enabled and is not a game
login replacement.

New databases require `main.sql` and `web.sql`; log schema is optional.
Existing databases require applicable upgrades through
`upgrade_20260225.sql`. The disposable database contains the required web-token
columns.

WP4B must address the stock failed-web-token logging path before using tokens as
credentials: `src/web/auth.cpp` can log the submitted token on failure.

## Binary provenance

The controlled build was:

```text
cmake --build . --target login-server char-server map-server --clean-first -- -j2
```

All rebuilt artifacts were byte-identical to their pre-rebuild SHA-256 and ELF
BuildIDs. Exact values are locked in the JSON profile. `--version` output is not
accepted as provenance because rAthena may read the current Git ref at runtime.

Verification:

```powershell
python tools\wp4a\verify_rathena_compatibility.py `
  --profile config\rathena-compatibility.json `
  --rathena C:\Ragnarok-Prontera\rathena `
  --evidence C:\Ragnarok-Prontera\Generated\wp4a-compatibility\rathena-binary-provenance.json
```

The runtime smoke must use `tools/wp4a/verify_prebuilt_rathena.sh` as its build
hook. This fail-closed hook verifies the already-proven binaries immediately
before startup, preventing an incremental relink from changing the executable
identity between provenance capture and the port/peer-registration smoke.
