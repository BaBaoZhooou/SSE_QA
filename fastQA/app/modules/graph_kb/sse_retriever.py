"""SSE knowledge graph retrieval integrated with fastQA graph_kb RAG."""

from __future__ import annotations

import hashlib
import logging
import time
from typing import Any

from app.modules.graph_kb.client import _query_graph_with_timeout
from app.modules.graph_kb.metadata import build_graph_route_metadata
from app.modules.graph_kb.models import GraphRagPayload, GraphRoutingResult
from app.modules.graph_kb.sse_graph_queries import build_sse_query_plan, rows_to_facts


logger = logging.getLogger(__name__)


def _extract_dois(rows: list[dict[str, Any]]) -> tuple[str, ...]:
    seen: set[str] = set()
    ordered: list[str] = []
    for row in rows:
        doi = str(row.get("doi") or "").strip()
        if not doi or doi in seen:
            continue
        seen.add(doi)
        ordered.append(doi)
    return tuple(ordered)


def _execute_sse_plan(
    *,
    plan: dict[str, Any],
    neo4j_client: Any,
    max_rows: int,
    timeout_ms: int,
) -> list[dict[str, Any]]:
    graph = getattr(neo4j_client, "graph", None)
    if graph is None or not bool(getattr(neo4j_client, "available", False)):
        return []

    cypher = str(plan.get("cypher") or "")
    params = dict(plan.get("params") or {})
    rows = _query_graph_with_timeout(graph=graph, cypher=cypher, params=params, timeout_ms=int(timeout_ms or 0))
    if rows is None:
        if hasattr(graph, "query"):
            raw = graph.query(cypher, params)
        else:
            raw = graph.run(cypher, **params).data()
        rows = [dict(item) for item in list(raw or []) if isinstance(item, dict)]
    return list(rows or [])[: max(1, int(max_rows or 1))]


def route_sse_graph_kb(
    *,
    question: str,
    neo4j_client: Any,
    max_rows: int,
    timeout_ms: int = 3000,
) -> GraphRoutingResult:
    started = time.perf_counter()
    diagnostics: dict[str, Any] = {
        "graph_pipeline_version": "sse-v1",
        "graph_schema": "sse",
        "graph_attempted": True,
        "graph_ready": bool(getattr(neo4j_client, "graph", None) is not None and getattr(neo4j_client, "available", False)),
        "neo4j_client": "neo4jgraph",
    }

    if not diagnostics["graph_ready"]:
        diagnostics["graph_fallback_reason"] = "neo4j_unavailable"
        diagnostics["latency_ms"] = round((time.perf_counter() - started) * 1000.0, 3)
        return GraphRoutingResult(mode="skip_graph", diagnostics=diagnostics)

    plan = build_sse_query_plan(question, limit=max_rows)
    diagnostics["graph_strategy"] = str(plan.get("strategy") or "")
    diagnostics["graph_intent"] = diagnostics["graph_strategy"]

    try:
        rows = _execute_sse_plan(
            plan=plan,
            neo4j_client=neo4j_client,
            max_rows=max_rows,
            timeout_ms=timeout_ms,
        )
    except TimeoutError:
        diagnostics["graph_fallback_reason"] = "timeout"
        diagnostics["latency_ms"] = round((time.perf_counter() - started) * 1000.0, 3)
        return GraphRoutingResult(mode="skip_graph", diagnostics=diagnostics)
    except Exception as exc:
        logger.warning("sse graph retrieval failed: %s", exc)
        diagnostics["graph_fallback_reason"] = "query_error"
        diagnostics["graph_error"] = str(exc)
        diagnostics["latency_ms"] = round((time.perf_counter() - started) * 1000.0, 3)
        return GraphRoutingResult(mode="skip_graph", diagnostics=diagnostics)

    facts = rows_to_facts(rows)
    dois = _extract_dois(rows)
    diagnostics["graph_result_count"] = len(rows)
    diagnostics["graph_doi_candidates_count"] = len(dois)
    diagnostics.update(
        build_graph_route_metadata(
            route_family="semantic",
            tri_state_mode="graph_for_rag",
            strategy=str(plan.get("strategy") or ""),
            intent=str(plan.get("strategy") or ""),
            result_count=len(rows),
            rag_injection_enabled=True,
            rag_injected=bool(facts),
            doi_source="graph" if dois else "none",
            graph_pipeline_version="sse-v1",
        )
    )
    diagnostics["latency_ms"] = round((time.perf_counter() - started) * 1000.0, 3)

    if not facts:
        diagnostics["graph_fallback_reason"] = "empty_result"
        return GraphRoutingResult(mode="skip_graph", diagnostics=diagnostics)

    context_lines = [
        f"sse_graph_strategy: {plan.get('strategy')}",
        "sse_graph_facts:",
        *[f"- {fact}" for fact in facts[:20]],
    ]
    rag_payload = GraphRagPayload(
        stage1_context_block="\n".join(context_lines),
        stage2_doi_candidates=dois[:20],
        stage2_entity_hints={
            "materials": tuple(
                dict.fromkeys(
                    str(row.get("material") or row.get("label") or "").strip()
                    for row in rows
                    if str(row.get("material") or row.get("label") or "").strip()
                )
            )[:10],
            "formulas": tuple(
                dict.fromkeys(str(row.get("formula") or "").strip() for row in rows if str(row.get("formula") or "").strip())
            )[:10],
        },
        stage4_fact_block="\n".join(
            [
                "SSE knowledge graph facts (cite DOI/source_json when used):",
                *[f"- {fact}" for fact in facts[:20]],
            ]
        ),
        cache_fingerprint=hashlib.sha256("\n".join(facts[:20]).encode("utf-8")).hexdigest()[:16],
    )
    return GraphRoutingResult(mode="graph_for_rag", rag_payload=rag_payload, diagnostics=diagnostics)
