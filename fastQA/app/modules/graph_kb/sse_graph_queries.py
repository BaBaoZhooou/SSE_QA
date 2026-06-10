"""Cypher query planning for the SSE solid-state electrolyte knowledge graph."""

from __future__ import annotations

import re
from typing import Any

_DOI_PATTERN = re.compile(r"(10\.\d+/[A-Za-z0-9._\-()/]+)", re.IGNORECASE)
_TOKEN_SPLIT = re.compile(r"[^\w\u4e00-\u9fff+\-/]+")


def _normalized_question(question: str) -> str:
    return " ".join(str(question or "").split()).strip()


def _contains_any(text: str, hints: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(hint.lower() in lowered for hint in hints)


def _fulltext_query(question: str) -> str:
    tokens = [token for token in _TOKEN_SPLIT.split(_normalized_question(question)) if len(token) >= 2]
    if not tokens:
        return "solid electrolyte"
    quoted = [f'"{token}"' if re.search(r"[\u4e00-\u9fff]", token) else token for token in tokens[:8]]
    return " OR ".join(quoted)


def _material_type_hint(question: str) -> str:
    text = question.lower()
    if _contains_any(text, ("硫化物", "sulfide", "thio", "lgps", "li3ps4", "li2s")):
        return "sulfide"
    if _contains_any(text, ("氧化物", "oxide", "llzo", "garnet", "nasicon", "latp")):
        return "oxide"
    if _contains_any(text, ("聚合物", "polymer", "peo", "pvdf")):
        return "polymer"
    if _contains_any(text, ("卤化物", "halide")):
        return "halide"
    if _contains_any(text, ("复合", "composite")):
        return "composite"
    return ""


def build_sse_query_plan(question: str, *, limit: int = 20) -> dict[str, Any]:
    text = _normalized_question(question)
    safe_limit = max(1, min(int(limit or 20), 100))

    doi_match = _DOI_PATTERN.search(text)
    if doi_match:
        return {
            "strategy": "lookup_doi",
            "cypher": (
                "MATCH (p:Paper {doi: $doi}) "
                "OPTIONAL MATCH (p)-[:REPORTS_MATERIAL]->(m:MaterialInstance) "
                "OPTIONAL MATCH (m)-[:HAS_PROPERTY]->(prop:PropertyRecord) "
                "RETURN p.doi AS doi, p.title AS title, p.sse_family AS sse_family, "
                "m.label AS material, m.formula AS formula, m.material_type AS material_type, "
                "prop.property_category AS property_category, prop.value_raw AS value_raw, "
                "prop.source_json AS source_json "
                "LIMIT $limit"
            ),
            "params": {"doi": doi_match.group(1), "limit": safe_limit},
        }

    if _contains_any(text, ("合成", "制备", "工艺", "前驱体", "synthesis", "precursor", "route", "milling", "sintering")):
        material_hint = _material_type_hint(text)
        return {
            "strategy": "synthesis_routes",
            "cypher": (
                "MATCH (m:MaterialInstance)-[:MADE_BY]->(r:SynthesisRoute) "
                "WHERE ($material_hint = '' OR toLower(coalesce(m.material_type, '')) CONTAINS toLower($material_hint) "
                "OR toLower(coalesce(m.formula, '')) CONTAINS toLower($material_hint) "
                "OR toLower(coalesce(m.label, '')) CONTAINS toLower($material_hint)) "
                "OPTIONAL MATCH (r)-[:HAS_PROCESS_TAG]->(tag:ProcessTag) "
                "OPTIONAL MATCH (r)-[:USES_PRECURSOR]->(precursor:Precursor) "
                "RETURN m.label AS material, m.formula AS formula, m.material_type AS material_type, "
                "r.process_summary AS process_summary, r.final_form AS final_form, "
                "collect(DISTINCT tag.label)[0..5] AS process_tags, "
                "collect(DISTINCT precursor.label)[0..5] AS precursors, "
                "m.source_json AS source_json "
                "LIMIT $limit"
            ),
            "params": {"material_hint": material_hint, "limit": safe_limit},
        }

    if _contains_any(
        text,
        (
            "电导率",
            "conductivity",
            "离子电导",
            "ionic",
            "最高",
            "排名",
            "top",
            "多少",
            "数值",
        ),
    ):
        material_hint = _material_type_hint(text)
        return {
            "strategy": "ionic_conductivity_ranking",
            "cypher": (
                "MATCH (m:MaterialInstance)-[:HAS_PROPERTY]->(p:PropertyRecord) "
                "WHERE p.property_category = 'ionic_conductivity_rt' "
                "AND p.numeric_value IS NOT NULL "
                "AND ($material_hint = '' OR toLower(coalesce(m.material_type, '')) CONTAINS toLower($material_hint) "
                "OR toLower(coalesce(m.formula, '')) CONTAINS toLower($material_hint)) "
                "OPTIONAL MATCH (paper:Paper)-[:REPORTS_MATERIAL]->(m) "
                "RETURN m.label AS material, m.formula AS formula, m.material_type AS material_type, "
                "p.value_raw AS value_raw, p.numeric_value AS numeric_value, p.numeric_unit AS numeric_unit, "
                "paper.doi AS doi, coalesce(p.source_json, m.source_json) AS source_json "
                "ORDER BY toFloat(p.numeric_value) DESC "
                "LIMIT $limit"
            ),
            "params": {"material_hint": material_hint, "limit": safe_limit},
        }

    if _contains_any(text, ("界面", "interface", "稳定性", "stability", "窗口", "window")):
        return {
            "strategy": "interface_or_stability",
            "cypher": (
                "MATCH (m:MaterialInstance)-[:HAS_PROPERTY]->(p:PropertyRecord) "
                "WHERE toLower(coalesce(p.property_category, '')) CONTAINS 'interface' "
                "OR toLower(coalesce(p.property_category, '')) CONTAINS 'stability' "
                "OR toLower(coalesce(p.property_category, '')) CONTAINS 'window' "
                "OPTIONAL MATCH (paper:Paper)-[:REPORTS_MATERIAL]->(m) "
                "RETURN m.label AS material, m.formula AS formula, p.property_category AS property_category, "
                "p.value_raw AS value_raw, paper.doi AS doi, coalesce(p.source_json, m.source_json) AS source_json "
                "LIMIT $limit"
            ),
            "params": {"limit": safe_limit},
        }

    fulltext = _fulltext_query(text)
    return {
        "strategy": "fulltext",
        "cypher": (
            "CALL db.index.fulltext.queryNodes('kg_node_fulltext', $q) "
            "YIELD node, score "
            "RETURN node.kind AS kind, node.label AS label, node.formula AS formula, "
            "node.title AS title, node.doi AS doi, node.material_type AS material_type, "
            "node.property_category AS property_category, node.value_raw AS value_raw, "
            "node.source_json AS source_json, score "
            "ORDER BY score DESC "
            "LIMIT $limit"
        ),
        "params": {"q": fulltext, "limit": safe_limit},
    }


def rows_to_facts(rows: list[dict[str, Any]]) -> list[str]:
    facts: list[str] = []
    for row in rows:
        parts: list[str] = []
        for key in (
            "material",
            "label",
            "formula",
            "material_type",
            "property_category",
            "value_raw",
            "numeric_value",
            "numeric_unit",
            "process_summary",
            "process_tags",
            "precursors",
            "doi",
            "title",
            "sse_family",
            "kind",
        ):
            value = row.get(key)
            if value in (None, "", [], ()):
                continue
            if isinstance(value, list):
                rendered = ", ".join(str(item) for item in value if item)
                if rendered:
                    parts.append(f"{key}={rendered}")
            else:
                parts.append(f"{key}={value}")
        source_json = str(row.get("source_json") or "").strip()
        if source_json:
            parts.append(f"source_json={source_json}")
        if parts:
            facts.append("; ".join(parts))
    return facts
