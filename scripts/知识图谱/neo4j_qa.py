#!/usr/bin/env python3
"""Graph retrieval QA over the SSE Neo4j knowledge graph."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from neo4j import GraphDatabase

ROOT = Path(__file__).resolve().parents[2]
FASTQA_ROOT = ROOT / "fastQA"
if str(FASTQA_ROOT) not in sys.path:
    sys.path.insert(0, str(FASTQA_ROOT))

from app.modules.graph_kb.sse_graph_queries import build_sse_query_plan, rows_to_facts


def _env(name: str, default: str = "") -> str:
    return str(os.getenv(name, default) or default).strip()


def _run_query(session, plan: dict[str, Any]) -> list[dict[str, Any]]:
    result = session.run(plan["cypher"], **plan.get("params", {}))
    return [dict(record) for record in result]


def _maybe_llm_answer(question: str, facts: list[str]) -> str:
    base_url = _env("OPENAI_BASE_URL") or _env("LLM_BASE_URL")
    model = _env("OPENAI_MODEL") or _env("LLM_MODEL")
    api_key = _env("OPENAI_API_KEY") or _env("LLM_API_KEY")
    if not base_url or not model or not api_key:
        return ""

    try:
        from openai import OpenAI
    except ImportError:
        return ""

    client = OpenAI(base_url=base_url, api_key=api_key)
    context = "\n".join(f"- {fact}" for fact in facts[:30])
    prompt = (
        "你是固态电解质知识图谱问答助手。只能根据给定检索结果回答，"
        "无法从检索结果推出时明确说不知道。引用时保留 DOI 或 source_json。\n\n"
        f"问题：{question}\n\n检索结果：\n{context}"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return str(response.choices[0].message.content or "").strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="SSE Neo4j graph QA")
    parser.add_argument("question")
    parser.add_argument("--uri", default=_env("NEO4J_URI", "bolt://127.0.0.1:7698"))
    parser.add_argument("--user", default=_env("NEO4J_USER", "neo4j"))
    parser.add_argument("--password", default=_env("NEO4J_PASSWORD", "sse-kg-password"))
    parser.add_argument("--database", default=_env("NEO4J_DATABASE", "neo4j"))
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--no-llm", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    plan = build_sse_query_plan(args.question, limit=args.limit)
    driver = GraphDatabase.driver(args.uri, auth=(args.user, args.password))
    try:
        with driver.session(database=args.database) as session:
            rows = _run_query(session, plan)
    finally:
        driver.close()

    facts = rows_to_facts(rows)
    answer = "" if args.no_llm else _maybe_llm_answer(args.question, facts)
    payload = {
        "question": args.question,
        "strategy": plan.get("strategy"),
        "row_count": len(rows),
        "facts": facts,
        "rows": rows[: args.limit],
        "answer": answer,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if answer:
            print(answer)
        else:
            print("\n".join(facts[:20]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
