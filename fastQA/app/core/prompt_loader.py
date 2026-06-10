from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path


_PACKAGE_PROMPTS = Path(__file__).resolve().parents[2] / "prompts"


def resolve_prompt_root() -> Path:
    explicit = str(os.getenv("PROMPTS_DIR") or os.getenv("FASTQA_PROMPTS_DIR") or "").strip()
    if explicit:
        path = Path(explicit)
        if not path.is_absolute():
            asset_root = str(os.getenv("FASTQA_SERVICE_ASSET_ROOT") or os.getenv("SERVICE_ASSET_ROOT") or "").strip()
            if asset_root:
                path = Path(asset_root) / path
            else:
                path = _PACKAGE_PROMPTS.parent / path
        resolved = path.resolve()
        if resolved.is_dir():
            return resolved
    if _PACKAGE_PROMPTS.is_dir():
        return _PACKAGE_PROMPTS.resolve()
    return _PACKAGE_PROMPTS.resolve()


@lru_cache(maxsize=None)
def load_prompt_template(name: str) -> str:
    normalized = str(name or "").strip()
    if not normalized:
        raise ValueError("prompt template name is required")
    if "/" in normalized or "\\" in normalized or normalized in {".", ".."}:
        raise ValueError(f"invalid prompt template name: {normalized!r}")
    path = resolve_prompt_root() / normalized
    return path.read_text(encoding="utf-8")


@lru_cache(maxsize=1)
def load_intent_tag_descriptions() -> dict[str, str]:
    path = resolve_prompt_root() / "intent_tags.json"
    if not path.is_file():
        raise FileNotFoundError(f"intent tag file not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("intent_tags.json must be a JSON object")
    return {str(k): str(v) for k, v in data.items()}


def clear_prompt_cache() -> None:
    load_prompt_template.cache_clear()
    load_intent_tag_descriptions.cache_clear()
