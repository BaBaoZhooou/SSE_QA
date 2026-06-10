#!/usr/bin/env python3
"""
Ingest SSE structured markdown (*/vlm/*.md) into Chroma stores used by @sse-qa/cli:

  - fastQA summary store:  {out}/fastqa_vector  collection lfp_papers
  - fastQA MD store:       {out}/fastqa_md      collection md_papers
  - highThinkingQA store:  {out}/thinking       collection sse_literature

Resumes by skipping DOIs already present in the thinking collection.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HTQA = ROOT / "highThinkingQA"
if str(HTQA) not in sys.path:
    sys.path.insert(0, str(HTQA))

logger = logging.getLogger("ingest_sse_md")

DOI_RE = re.compile(r"\b(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)\b", re.IGNORECASE)
TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def load_dotenv(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def setup_embedding_env(secrets: dict[str, str]) -> None:
    key = (
        secrets.get("HIGHTHINKINGQA_EMBEDDING_API_KEY")
        or secrets.get("EMBEDDING_API_KEY")
        or secrets.get("LLM_API_KEY")
        or secrets.get("DASHSCOPE_API_KEY")
        or ""
    )
    base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    os.environ["HIGHTHINKINGQA_EMBEDDING_API_KEY"] = key
    os.environ["EMBEDDING_API_KEY"] = key
    os.environ["LLM_API_KEY"] = key
    os.environ["EMBEDDING_BASE_URL"] = base
    os.environ["EMBEDDING_MODEL"] = "text-embedding-v4"
    os.environ["HIGHTHINKINGQA_EMBEDDING_MODEL"] = "text-embedding-v4"
    os.environ["HIGHTHINKINGQA_EMBEDDING_DIMENSIONS"] = "2048"
    os.environ["HIGHTHINKINGQA_EMBEDDING_CONCURRENCY"] = os.environ.get(
        "HIGHTHINKINGQA_EMBEDDING_CONCURRENCY", "2"
    )
    os.environ["HIGHTHINKINGQA_EMBEDDING_BATCH_SIZE"] = os.environ.get(
        "HIGHTHINKINGQA_EMBEDDING_BATCH_SIZE", "10"
    )


def extract_doi(text: str, fallback: str) -> str:
    m = DOI_RE.search(text[:8000])
    if m:
        return m.group(1).strip().rstrip(".)")
    slug = fallback.replace(".repaired", "")
    parts = slug.split("_", 1)
    if len(parts) == 2 and parts[0].startswith("10."):
        return f"{parts[0]}/{parts[1]}"
    return slug


def extract_title(text: str, fallback: str) -> str:
    m = TITLE_RE.search(text[:4000])
    if m:
        return m.group(1).strip()
    return fallback.replace("_", " ")


def discover_md_files(source: Path) -> list[Path]:
    vlm = sorted(source.glob("**/vlm/*.md"))
    if vlm:
        return vlm
    return sorted(source.glob("**/*.md"))


def chunk_id_safe(doi: str, idx: int) -> str:
    base = re.sub(r"[^A-Za-z0-9._-]+", "_", doi)[:180]
    return f"{base}__chunk_{idx}"


class ChromaWriter:
    def __init__(self, persist_dir: Path, collection_name: str):
        import chromadb

        persist_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(persist_dir))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        self.name = collection_name
        self.path = persist_dir

    def indexed_dois(self) -> set[str]:
        out: set[str] = set()
        try:
            got = self.collection.get(include=["metadatas"])
            for meta in got.get("metadatas") or []:
                if isinstance(meta, dict):
                    doi = str(meta.get("doi") or meta.get("DOI") or "").strip()
                    if doi:
                        out.add(doi)
        except Exception as exc:
            logger.warning("indexed_dois failed for %s: %s", self.name, exc)
        return out

    def upsert_batch(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        documents: list[str],
        metadatas: list[dict[str, Any]],
    ) -> None:
        batch = 400
        for i in range(0, len(ids), batch):
            j = min(i + batch, len(ids))
            self.collection.upsert(
                ids=ids[i:j],
                embeddings=embeddings[i:j],
                documents=documents[i:j],
                metadatas=metadatas[i:j],
            )


def process_one_paper(
    md_path: Path,
    source_root: Path,
    writers: dict[str, ChromaWriter],
    embed_client,
) -> dict[str, Any]:
    from ingest.chunker import chunk_document
    from ingest.embedder import embed_texts

    rel = md_path.relative_to(source_root)
    slug = md_path.parent.parent.name if md_path.parent.name == "vlm" else md_path.stem
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    if not text.strip():
        return {"file": str(rel), "status": "empty"}

    doi = extract_doi(text, slug)
    title = extract_title(text, slug)
    rel_str = str(rel)

    def _embed_fn(batch: list[str]):
        return embed_texts(batch, client=embed_client)

    chunks = chunk_document(
        markdown_text=text,
        doi=doi,
        title=title,
        embedding_func=_embed_fn,
    )
    if not chunks:
        return {"file": str(rel), "status": "no_chunks", "doi": doi}

    texts = [c.text for c in chunks]
    embeddings = embed_texts(texts, client=embed_client)
    valid = [(c, e) for c, e in zip(chunks, embeddings) if any(v != 0.0 for v in e[:3])]
    if not valid:
        return {"file": str(rel), "status": "embed_failed", "doi": doi}

    ids_th, docs_th, metas_th, embs = [], [], [], []
    ids_lfp, metas_lfp = [], []
    ids_md, metas_md = [], []

    for chunk, emb in valid:
        cid = chunk_id_safe(doi, chunk.chunk_index)
        ids_th.append(cid)
        docs_th.append(chunk.text)
        embs.append(emb)
        meta_th = chunk.to_metadata()
        meta_th["title"] = title
        meta_th["source_file"] = rel_str
        metas_th.append(meta_th)

        ids_lfp.append(cid)
        metas_lfp.append(
            {
                "doi": doi,
                "title": title,
                "source_file": rel_str,
                "chunk_id": str(chunk.chunk_index),
                "data_quality": "md_ingest",
            }
        )

        ids_md.append(cid)
        metas_md.append(
            {
                "doi": doi,
                "document_name": f"{slug}.md",
                "filename": rel_str,
                "chunk_id": str(chunk.chunk_index),
                "is_full_document": False,
                "title": title,
            }
        )

    writers["thinking"].upsert_batch(ids_th, embs, docs_th, metas_th)
    writers["lfp"].upsert_batch(ids_lfp, embs, docs_th, metas_lfp)
    writers["md"].upsert_batch(ids_md, embs, docs_th, metas_md)

    return {
        "file": str(rel),
        "status": "ok",
        "doi": doi,
        "title": title[:120],
        "chunks": len(valid),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest SSE markdown into Chroma for sse-qa")
    parser.add_argument(
        "--source",
        default="/home/lwb/projects/结构化文献/固态电解质_筛选通过",
    )
    parser.add_argument(
        "--out",
        default=str(Path.home() / ".sse-qa" / "data" / "chroma"),
    )
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--secrets", default=str(Path.home() / ".sse-qa" / "secrets.env"))
    parser.add_argument("--state", default=str(Path.home() / ".sse-qa" / "ingest_sse_md_state.json"))
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    source = Path(args.source).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()
    if not source.is_dir():
        logger.error("source not found: %s", source)
        return 1

    secrets = load_dotenv(Path(args.secrets))
    if not (
        secrets.get("LLM_API_KEY")
        or secrets.get("EMBEDDING_API_KEY")
        or secrets.get("HIGHTHINKINGQA_EMBEDDING_API_KEY")
    ):
        logger.error("missing embedding API key in %s", args.secrets)
        return 1

    setup_embedding_env(secrets)
    from ingest.embedder import get_embedding_client

    writers = {
        "thinking": ChromaWriter(out / "thinking", "sse_literature"),
        "lfp": ChromaWriter(out / "fastqa_vector", "lfp_papers"),
        "md": ChromaWriter(out / "fastqa_md", "md_papers"),
    }
    indexed = writers["thinking"].indexed_dois()
    logger.info("thinking collection already has %s distinct DOIs", len(indexed))

    files = discover_md_files(source)
    if args.start:
        files = files[args.start :]
    if args.limit and args.limit > 0:
        files = files[: args.limit]

    todo: list[Path] = []
    for md_path in files:
        slug = md_path.parent.parent.name if md_path.parent.name == "vlm" else md_path.stem
        try:
            preview = md_path.read_text(encoding="utf-8", errors="ignore")[:8000]
        except OSError:
            continue
        doi = extract_doi(preview, slug)
        if doi in indexed:
            continue
        todo.append(md_path)

    logger.info(
        "source=%s total_md=%s to_ingest=%s out=%s workers=%s",
        source,
        len(files),
        len(todo),
        out,
        args.workers,
    )
    if not todo:
        logger.info("nothing to ingest")
        return 0

    stats = {"ok": 0, "failed": 0, "chunks": 0}
    stats_lock = threading.Lock()
    state_path = Path(args.state)

    def _worker(md_path: Path) -> dict[str, Any]:
        client = get_embedding_client()
        return process_one_paper(md_path, source, writers, client)

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {pool.submit(_worker, p): p for p in todo}
        for i, fut in enumerate(as_completed(futures), 1):
            md_path = futures[fut]
            try:
                res = fut.result()
            except Exception as exc:
                res = {"file": str(md_path), "status": "error", "error": str(exc)}
                logger.exception("failed %s", md_path)
            with stats_lock:
                if res.get("status") == "ok":
                    stats["ok"] += 1
                    stats["chunks"] += int(res.get("chunks") or 0)
                else:
                    stats["failed"] += 1
            if i % 10 == 0 or i == len(todo):
                elapsed = time.time() - t0
                logger.info(
                    "progress %s/%s ok=%s chunks=%s failed=%s elapsed=%.0fs",
                    i,
                    len(todo),
                    stats["ok"],
                    stats["chunks"],
                    stats["failed"],
                    elapsed,
                )
                state_path.write_text(
                    json.dumps({"stats": stats, "elapsed": elapsed, "out": str(out)}, indent=2),
                    encoding="utf-8",
                )

    summary = {
        "source": str(source),
        "out": str(out),
        "ingested_papers": stats["ok"],
        "failed_papers": stats["failed"],
        "total_chunks": stats["chunks"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    state_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if stats["failed"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
