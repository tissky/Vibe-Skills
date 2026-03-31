#!/usr/bin/env bash
set -euo pipefail

VM_ROOT="${HOME}/.cache/vibeskills-vm/windows-proof"

if [[ "${1:-}" == "--help" ]]; then
  cat <<'EOF'
Usage: bash ./scripts/setup/stop-windows-proof-vm.sh [--vm-root PATH]
EOF
  exit 0
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --vm-root)
      VM_ROOT="${2:-}"
      shift 2
      ;;
    *)
      echo "[ERROR] Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

PIDFILE="${VM_ROOT}/qemu.pid"
TPM_PIDFILE="${VM_ROOT}/swtpm.pid"

if [[ -f "${PIDFILE}" ]]; then
  PID="$(cat "${PIDFILE}")"
  if kill -0 "${PID}" >/dev/null 2>&1; then
    kill "${PID}"
    echo "[OK] Stopped QEMU pid ${PID}"
  else
    echo "[WARN] QEMU pid ${PID} is not running"
  fi
  rm -f "${PIDFILE}"
else
  echo "[WARN] No QEMU pidfile found at ${PIDFILE}"
fi

if [[ -f "${TPM_PIDFILE}" ]]; then
  TPM_PID="$(cat "${TPM_PIDFILE}" 2>/dev/null || true)"
  if [[ -n "${TPM_PID}" ]] && kill -0 "${TPM_PID}" >/dev/null 2>&1; then
    kill "${TPM_PID}"
    echo "[OK] Stopped swtpm pid ${TPM_PID}"
  elif [[ -n "${TPM_PID}" ]]; then
    echo "[WARN] swtpm pid ${TPM_PID} is not running"
  else
    echo "[WARN] swtpm pidfile vanished before it could be read"
  fi
  rm -f "${TPM_PIDFILE}"
fi
