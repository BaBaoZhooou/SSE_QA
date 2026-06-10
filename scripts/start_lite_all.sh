#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LITE_YAML="${SYSTEM_YAML:-$ROOT_DIR/config/system.lite.yaml}"

if [[ ! -f "$LITE_YAML" ]]; then
  echo "[error] missing lite config: $LITE_YAML" >&2
  echo "        cp config/system.lite.yaml.example config/system.lite.yaml" >&2
  exit 1
fi

echo "[lite] starting backend services only (no frontend, no MinIO)"
SYSTEM_YAML="$LITE_YAML" bash "$ROOT_DIR/scripts/start_all.sh"
