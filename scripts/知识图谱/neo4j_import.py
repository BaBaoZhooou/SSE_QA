#!/usr/bin/env python3
"""Import SSE knowledge graph JSON into Neo4j."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

from neo4j import GraphDatabase


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JSON = PROJECT_ROOT / "知识图谱" / "sse_knowledge_graph_full.json"

INDEX_STATEMENTS = (
    "CREATE CONSTRAINT kg_node_id IF NOT EXISTS FOR (n:KGNode) REQUIRE n.id IS UNIQUE",
    "CREATE INDEX kg_node_kind IF NOT EXISTS FOR (n:KGNode) ON (n.kind)",
    "CREATE INDEX kg_paper_id IF NOT EXISTS FOR (n:Paper) ON (n.paper_id)",
    "CREATE INDEX kg_material_formula IF NOT EXISTS FOR (n:MaterialInstance) ON (n.formula)",
    "CREATE INDEX kg_material_type IF NOT EXISTS FOR (n:MaterialInstance) ON (n.material_type)",
    "CREATE INDEX kg_property_category IF NOT EXISTS FOR (n:PropertyRecord) ON (n.property_category)",
    "CREATE INDEX kg_route_id IF NOT EXISTS FOR (n:SynthesisRoute) ON (n.route_id)",
    """CREATE FULLTEXT INDEX kg_node_fulltext IF NOT EXISTS
FOR (n:KGNode)
ON EACH [n.label, n.formula, n.title, n.doi, n.material_type, n.value_raw, n.process_summary, n.property_category, n.material_name]""",
)


def _env(name: str, default: str = "") -> str:
    return str(os.getenv(name, default) or default).strip()


def _scalar(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _node_props(node: dict[str, Any]) -> dict[str, Any]:
    props: dict[str, Any] = {}
    for key, value in node.items():
        if key == "id":
            continue
        converted = _scalar(value)
        if converted is None or converted == "":
            continue
        props[key] = converted
    return props


def _load_graph(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    nodes = list(payload.get("nodes") or [])
    edges = list(payload.get("edges") or [])
    if not nodes:
        raise ValueError(f"no nodes found in {path}")
    return nodes, edges


def _chunks(items: list[Any], size: int):
    for index in range(0, len(items), size):
        yield items[index : index + size]


def _clear_graph(session) -> None:
    session.run("MATCH (n) DETACH DELETE n")


def _ensure_indexes(session) -> None:
    for statement in INDEX_STATEMENTS:
        session.run(statement)


def _import_nodes(session, nodes: list[dict[str, Any]], batch_size: int) -> None:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in nodes:
        node_id = str(node.get("id") or "").strip()
        if not node_id:
            continue
        kind = str(node.get("kind") or "Entity").strip() or "Entity"
        grouped[kind].append({"id": node_id, "props": _node_props(node)})

    for kind, rows in grouped.items():
        label = "".join(ch if ch.isalnum() else "_" for ch in kind)
        if not label or label[0].isdigit():
            label = f"Kind_{label or 'Entity'}"
        cypher = (
            f"UNWIND $rows AS row "
            f"MERGE (n:KGNode:{label} {{id: row.id}}) "
            f"SET n += row.props"
        )
        total = len(rows)
        for index, batch in enumerate(_chunks(rows, batch_size), start=1):
            session.run(cypher, rows=batch)
            print(f"  nodes[{kind}] batch {index}: {min(index * batch_size, total)}/{total}")


def _import_edges(session, edges: list[dict[str, Any]], batch_size: int) -> None:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in edges:
        source = str(edge.get("source") or "").strip()
        target = str(edge.get("target") or "").strip()
        relation = str(edge.get("relation") or "RELATED_TO").strip() or "RELATED_TO"
        relation = "".join(ch if ch.isalnum() else "_" for ch in relation)
        if not source or not target or not relation:
            continue
        grouped[relation].append(
            {
                "source": source,
                "target": target,
                "edge_id": str(edge.get("id") or ""),
                "support_count": _scalar(edge.get("support_count")),
            }
        )

    for relation, rows in grouped.items():
        cypher = (
            f"UNWIND $rows AS row "
            f"MATCH (s:KGNode {{id: row.source}}) "
            f"MATCH (t:KGNode {{id: row.target}}) "
            f"MERGE (s)-[r:{relation}]->(t) "
            f"SET r.edge_id = row.edge_id, r.support_count = row.support_count"
        )
        total = len(rows)
        for index, batch in enumerate(_chunks(rows, batch_size), start=1):
            session.run(cypher, rows=batch)
            print(f"  edges[{relation}] batch {index}: {min(index * batch_size, total)}/{total}")


def _count_graph(session) -> dict[str, int]:
    node_count = session.run("MATCH (n:KGNode) RETURN count(n) AS c").single()["c"]
    rel_count = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
    return {"nodes": int(node_count), "relationships": int(rel_count)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Import SSE knowledge graph into Neo4j")
    parser.add_argument("--json-path", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--uri", default=_env("NEO4J_URI", "bolt://127.0.0.1:7698"))
    parser.add_argument("--user", default=_env("NEO4J_USER", "neo4j"))
    parser.add_argument("--password", default=_env("NEO4J_PASSWORD", "sse-kg-password"))
    parser.add_argument("--database", default=_env("NEO4J_DATABASE", "neo4j"))
    parser.add_argument("--batch-size", type=int, default=1000)
    parser.add_argument("--clear", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    json_path = args.json_path.resolve()
    if not json_path.exists():
        print(f"graph json not found: {json_path}", file=sys.stderr)
        return 1

    print(f"loading graph from {json_path}")
    nodes, edges = _load_graph(json_path)
    print(f"loaded nodes={len(nodes)} edges={len(edges)}")

    if args.dry_run:
        kinds = sorted({str(node.get('kind') or '') for node in nodes})
        relations = sorted({str(edge.get('relation') or '') for edge in edges})
        print("dry-run ok")
        print(f"  node kinds ({len(kinds)}): {', '.join(kinds[:12])}{'...' if len(kinds) > 12 else ''}")
        print(f"  relations ({len(relations)}): {', '.join(relations[:12])}{'...' if len(relations) > 12 else ''}")
        return 0

    started = time.time()
    driver = GraphDatabase.driver(args.uri, auth=(args.user, args.password))
    try:
        with driver.session(database=args.database) as session:
            if args.clear:
                print("clearing existing graph...")
                _clear_graph(session)
            print("creating indexes...")
            _ensure_indexes(session)
            print("importing nodes...")
            _import_nodes(session, nodes, max(100, args.batch_size))
            print("importing edges...")
            _import_edges(session, edges, max(100, args.batch_size))
            counts = _count_graph(session)
    finally:
        driver.close()

    elapsed = time.time() - started
    print(f"import complete in {elapsed:.1f}s: nodes={counts['nodes']} relationships={counts['relationships']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
