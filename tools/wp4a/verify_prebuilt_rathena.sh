#!/usr/bin/env bash
set -euo pipefail

for name in FORCE RATHENA_FORCE RATHENA_COMPATIBILITY_BYPASS ROWEB_COMPATIBILITY_BYPASS; do
  value="${!name:-}"
  case "${value,,}" in
    ""|0|false|no) ;;
    *) echo "FAIL_RATHENA_AUTHORITATIVE_COMPATIBILITY: compatibility bypass enabled: ${name}" >&2; exit 1 ;;
  esac
done

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
roweb_root="$(cd -- "${script_dir}/../.." && pwd)"
rathena_root="${RATHENA_SOURCE_DIR:?RATHENA_SOURCE_DIR is required}"
evidence="${RATHENA_BINARY_EVIDENCE:-/mnt/c/Ragnarok-Prontera/Generated/wp4a-compatibility/rathena-binary-provenance.json}"

python3 "${script_dir}/verify_rathena_compatibility.py" \
  --profile "${roweb_root}/config/rathena-compatibility.json" \
  --rathena "${rathena_root}" \
  --evidence "${evidence}"

echo "PASS_PREBUILT_RATHENA_BINARY_IDENTITY"
