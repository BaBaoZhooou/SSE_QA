#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENT_YAML="${SYSTEM_YAML:-$ROOT_DIR/config/system.agent.yaml}"

export QA_SERVICES="${QA_SERVICES:-fastQA highThinkingQA gateway}"
SYSTEM_YAML="$AGENT_YAML" bash "$ROOT_DIR/scripts/stop_all.sh"
