# ROWEB Risk Register

## R-COMPAT-001 — Authoritative rAthena compatibility mismatch

| Field | Value |
| --- | --- |
| Classification | `BLOCKER_NOW` |
| Status | `VERIFIED_CLOSED` |
| Approved source | `C:\Ragnarok-Prontera\rathena` |
| Approved commit | `0c3ca757ad35fff003130a8441a10f27cccd0ed9` |
| Profile | `config/rathena-compatibility.json` |
| Binary evidence | `C:\Ragnarok-Prontera\Generated\wp4a-compatibility\rathena-binary-provenance.json` |
| Runtime evidence | `C:\Ragnarok-Prontera\Generated\wp4a-compatibility\rathena-runtime-smoke-final.log` |

### Closure evidence

- The authoritative checkout was tracked-clean at the approved detached HEAD.
- Fork and upstream `master` resolved to the approved commit.
- A `--clean-first` CMake rebuild with `PACKETVER=20211103` reproduced the
  pre-existing SHA-256 and ELF BuildID of all three server binaries.
- The exact hashed binaries started on loopback ports 6900, 6121, and 5121,
  completed peer registration, and were identity-safely stopped.
- Validator and runtime smoke ran without `FORCE` or a compatibility bypass.

Reopen this blocker if the source commit, PACKETVER, protocol settings, runtime
overlay, binary hashes, or BuildIDs change.
