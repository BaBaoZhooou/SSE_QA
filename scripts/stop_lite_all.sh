#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LITE_YAML="${SYSTEM_YAML:-$ROOT_DIR/config/system.lite.yaml}"

echo "[lite] stopping backend services only"
SYSTEM_YAML="$LITE_YAML" bash "$ROOT_DIR/scripts/stop_all.sh"
