#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENT_YAML="${SYSTEM_YAML:-$ROOT_DIR/config/system.agent.yaml}"

if [[ ! -f "$AGENT_YAML" ]]; then
  echo "[error] missing agent config: $AGENT_YAML" >&2
  echo "        cp config/system.agent.yaml.example config/system.agent.yaml" >&2
  exit 1
fi

echo "[agent] starting SSE QA backend (no MySQL, no public-service, no frontend)"
# QA_SERVICES 优先从 system.agent.yaml 的 agent 段读取；未配置时默认不含 patent
export QA_SERVICES="${QA_SERVICES:-fastQA highThinkingQA gateway}"
SYSTEM_YAML="$AGENT_YAML" bash "$ROOT_DIR/scripts/start_all.sh"
