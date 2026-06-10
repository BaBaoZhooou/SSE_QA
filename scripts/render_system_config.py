#!/usr/bin/env python3
"""Render config/system.yaml into shell export statements or a flat .env file."""

from __future__ import annotations

import argparse
import shlex
import sys
from pathlib import Path
from typing import Any

# Per-service env vars must not be exported globally from unified YAML.
_GLOBAL_EXPORT_BLOCKLIST = frozenset(
    {
        "REDIS_KEY_PREFIX",
        "PROMPTS_DIR",
        "name",
        "domain",
    }
)


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "PyYAML is required: pip install pyyaml\n"
            "Or keep using layered .env files under config/ and resource/config/."
        ) from exc
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: root must be a mapping")
    return data


def _flatten(obj: Any, prefix: str = "") -> dict[str, str]:
    out: dict[str, str] = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_str = str(key).strip()
            if (
                not key_str
                or key_str.startswith("#")
                or key_str.startswith("_")
                or key_str in _GLOBAL_EXPORT_BLOCKLIST
            ):
                continue
            if isinstance(value, dict):
                out.update(_flatten(value, prefix))
            elif value is None:
                continue
            else:
                out[key_str] = str(value)
    return out


def render_exports(path: Path) -> list[str]:
    flat = _flatten(_load_yaml(path))
    lines: list[str] = []
    for key in sorted(flat):
        value = flat[key]
        if value == "":
            continue
        lines.append(f"export {key}={shlex.quote(value)}")
    return lines


def render_dotenv(path: Path) -> str:
    flat = _flatten(_load_yaml(path))
    rows = [f"{key}={value}" for key, value in sorted(flat.items()) if value != ""]
    return "\n".join(rows) + ("\n" if rows else "")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("yaml_path", type=Path, help="Path to system.yaml")
    parser.add_argument(
        "--export-shell",
        action="store_true",
        help="Print bash export lines to stdout",
    )
    parser.add_argument(
        "--write-env",
        type=Path,
        help="Write flattened KEY=value file (e.g. config/system.generated.env)",
    )
    args = parser.parse_args(argv)
    path = args.yaml_path.resolve()
    if not path.is_file():
        raise SystemExit(f"config file not found: {path}")

    if args.export_shell:
        print("\n".join(render_exports(path)))
        return 0
    if args.write_env:
        args.write_env.write_text(render_dotenv(path), encoding="utf-8")
        print(f"wrote {args.write_env}")
        return 0
    print(render_dotenv(path), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
