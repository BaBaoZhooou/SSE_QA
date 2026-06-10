#!/usr/bin/env bash
# Fail if git tree or npm pack would include agent dirs, secret env values, or API keys.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLI_DIR="$ROOT_DIR/packages/sse-qa-cli"
FAILED=0

fail() {
  echo "[audit] FAIL: $1" >&2
  FAILED=1
}

git_files() {
  cd "$ROOT_DIR" && git ls-files | sed 's/^"//;s/"$//'
}

echo "[audit] checking git tracked paths..."
while IFS= read -r path; do
  [[ -z "$path" ]] && continue
  fail "git tracks forbidden path: $path"
done < <(git_files | rg -i '(^|/)\.(cursor|claude|codex|superpowers)(/|$)|(^|/)\.cursor/|(^|/)\.claude/|(^|/)\.codex$|(^|/)\.superpowers/' || true)

while IFS= read -r path; do
  [[ -z "$path" ]] && continue
  [[ "$path" == *.secret.env.example ]] && continue
  fail "git tracks secret env (non-example): $path"
done < <(git_files | rg '\.secret\.env$' | rg -v '\.example$' || true)

echo "[audit] scanning tracked files for API key patterns..."
while IFS= read -r path; do
  [[ -z "$path" ]] && continue
  [[ -f "$ROOT_DIR/$path" ]] || continue
  if rg -q 'sk-[a-f0-9]{20,}' "$ROOT_DIR/$path" 2>/dev/null; then
    fail "API key pattern in git file: $path"
  fi
done < <(git_files)

echo "[audit] checking npm pack contents..."
if [[ -d "$CLI_DIR" ]]; then
  PACK_LIST="$(cd "$CLI_DIR" && npm pack --dry-run 2>&1 | rg '^npm notice [0-9]' | sed -E 's/^npm notice [0-9.]+[kMG]?B //' || true)"
  while IFS= read -r path; do
    [[ -z "$path" ]] && continue
    if rg -qi '(^|/)\.(cursor|claude|codex|superpowers)(/|$)|/\.codex$' <<< "$path"; then
      fail "npm pack includes agent path: $path"
    fi
    if rg -q '\.secret\.env$' <<< "$path" && ! rg -q '\.example$' <<< "$path"; then
      file="$CLI_DIR/$path"
      if [[ -f "$file" ]] && rg -q '^[A-Z0-9_]+=[^[:space:]]+' "$file" 2>/dev/null; then
        fail "npm pack includes non-empty secret env: $path"
      fi
    fi
    file="$CLI_DIR/$path"
    if [[ -f "$file" ]] && rg -q 'sk-[a-f0-9]{20,}' "$file" 2>/dev/null; then
      fail "API key pattern in npm pack file: $path"
    fi
  done <<< "$PACK_LIST"
fi

if [[ "$FAILED" -ne 0 ]]; then
  echo "[audit] release safety check failed" >&2
  exit 1
fi

echo "[audit] OK — no .cursor/.claude/.codex/.superpowers or API keys detected"
