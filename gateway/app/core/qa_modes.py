"""Parse which QA modes (fast/thinking/patent) are enabled on the gateway."""

from __future__ import annotations

import os

ALL_QA_MODES = frozenset({"fast", "thinking", "patent"})


def parse_enabled_qa_modes() -> frozenset[str]:
    """Resolve enabled QA modes from env.

    Priority:
    1. ``QA_ENABLED_MODES=fast,thinking`` (comma/semicolon/space separated)
    2. Per-mode ``QA_FAST_ENABLED`` / ``QA_THINKING_ENABLED`` / ``QA_PATENT_ENABLED``
       (also accepts ``GATEWAY_*_ENABLED`` aliases)
    3. Default: all three enabled
    """
    explicit = str(os.getenv("QA_ENABLED_MODES", "") or "").strip()
    if explicit:
        parts = {
            token.strip().lower()
            for token in explicit.replace(";", ",").replace(" ", ",").split(",")
            if token.strip()
        }
        enabled = parts & ALL_QA_MODES
        if enabled:
            return frozenset(enabled)

    modes: set[str] = set()
    for mode in sorted(ALL_QA_MODES):
        flag_names = (f"QA_{mode.upper()}_ENABLED", f"GATEWAY_{mode.upper()}_ENABLED")
        raw: str | None = None
        for name in flag_names:
            val = os.getenv(name)
            if val is not None:
                raw = val
                break
        if raw is None:
            modes.add(mode)
        elif str(raw).strip().lower() in {"1", "true", "yes", "on"}:
            modes.add(mode)
    return frozenset(modes) if modes else ALL_QA_MODES
