from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path


_PROMPT_ROOT = Path(__file__).resolve().parent / "prompts"


@lru_cache(maxsize=None)
def load_patent_prompt_template(name: str) -> str:
    normalized = str(name or "").strip()
    if not normalized:
        raise ValueError("prompt template name is required")
    if "/" in normalized or "\\" in normalized or normalized in {".", ".."}:
        raise ValueError(f"invalid prompt template name: {normalized!r}")
    return _PROMPT_ROOT.joinpath(normalized).read_text(encoding="utf-8")


@lru_cache(maxsize=1)
def load_patent_intent_tag_descriptions() -> dict[str, str]:
    path = _PROMPT_ROOT / "intent_tags.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("intent_tags.json must be a JSON object")
    return {str(k): str(v) for k, v in data.items()}
