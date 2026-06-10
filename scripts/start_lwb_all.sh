#!/usr/bin/env bash
# lwb 独立栈：后端服务 + Vite 前端（依赖 config/system.yaml）
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT_DIR/scripts/_service_common.sh"

if [[ ! -f "$CONFIG_DIR/system.yaml" ]]; then
  echo "[error] missing $CONFIG_DIR/system.yaml — cp config/system.yaml.example config/system.yaml" >&2
  exit 1
fi

export FRONTEND_PORT="${FRONTEND_PORT:-5174}"
export VITE_PROXY_TARGET="${VITE_PROXY_TARGET:-${BACKEND_PROXY_TARGET:-http://127.0.0.1:18101}}"
export BACKEND_PROXY_TARGET="${BACKEND_PROXY_TARGET:-$VITE_PROXY_TARGET}"

echo "[lwb] gateway :${GATEWAY_PORT:-18101}  frontend :$FRONTEND_PORT  proxy -> $VITE_PROXY_TARGET"

bash "$ROOT_DIR/scripts/start_all.sh"

FRONTEND_DIR="$ROOT_DIR/frontend-vue"
if [[ ! -d "$FRONTEND_DIR/node_modules" ]]; then
  echo "[warn] run: cd frontend-vue && npm install" >&2
fi

if command -v lsof >/dev/null 2>&1 && lsof -iTCP:"$FRONTEND_PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
  echo "[skip] frontend already on :$FRONTEND_PORT"
else
  echo "[start] frontend dev on :$FRONTEND_PORT"
  (
    cd "$FRONTEND_DIR"
    exec env FRONTEND_PORT="$FRONTEND_PORT" VITE_PROXY_TARGET="$VITE_PROXY_TARGET" \
      npm run dev -- --host 0.0.0.0 --port "$FRONTEND_PORT"
  ) &
  echo "[info] frontend pid $!"
fi

echo "lwb stack ready — http://127.0.0.1:$FRONTEND_PORT"
