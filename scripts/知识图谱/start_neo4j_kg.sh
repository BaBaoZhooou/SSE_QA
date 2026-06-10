#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_FILE="${ROOT}/知识图谱/neo4j/compose.yaml"
NEO4J_URI="${NEO4J_URI:-bolt://127.0.0.1:7698}"
NEO4J_USER="${NEO4J_USER:-neo4j}"
NEO4J_PASSWORD="${NEO4J_PASSWORD:-sse-kg-password}"
NEO4J_DATABASE="${NEO4J_DATABASE:-neo4j}"
IMPORT_BATCH_SIZE="${IMPORT_BATCH_SIZE:-1000}"

cd "${ROOT}"

echo "[sse-kg] starting neo4j via ${COMPOSE_FILE}"
docker compose -f "${COMPOSE_FILE}" up -d

echo "[sse-kg] waiting for bolt ${NEO4J_URI}"
python3 - <<'PY'
import os
import sys
import time

from neo4j import GraphDatabase

uri = os.environ.get("NEO4J_URI", "bolt://127.0.0.1:7698")
user = os.environ.get("NEO4J_USER", "neo4j")
password = os.environ.get("NEO4J_PASSWORD", "sse-kg-password")
database = os.environ.get("NEO4J_DATABASE", "neo4j")

deadline = time.time() + 180
last_error = ""
while time.time() < deadline:
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session(database=database) as session:
            session.run("RETURN 1").single()
        driver.close()
        print("[sse-kg] neo4j is ready")
        sys.exit(0)
    except Exception as exc:
        last_error = str(exc)
        time.sleep(3)

print(f"[sse-kg] neo4j not ready after timeout: {last_error}", file=sys.stderr)
sys.exit(1)
PY

echo "[sse-kg] importing knowledge graph"
NEO4J_URI="${NEO4J_URI}" \
NEO4J_USER="${NEO4J_USER}" \
NEO4J_PASSWORD="${NEO4J_PASSWORD}" \
NEO4J_DATABASE="${NEO4J_DATABASE}" \
python3 "${ROOT}/scripts/知识图谱/neo4j_import.py" --clear --batch-size "${IMPORT_BATCH_SIZE}"

echo "[sse-kg] done"
echo "  Browser: http://127.0.0.1:7476"
echo "  Bolt:    ${NEO4J_URI}"
echo "  User:    ${NEO4J_USER}"
