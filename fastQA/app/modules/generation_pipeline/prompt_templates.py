#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prompt templates for generation-driven RAG stages (loaded from external files)."""

from typing import Tuple

from app.core.prompt_loader import load_prompt_template


def load_generation_prompts() -> Tuple[str, str]:
    """Return stage1/stage2 prompt templates from ``fastQA/prompts/``."""
    return (
        load_prompt_template("stage1_planning.txt"),
        load_prompt_template("stage2_synthesis.txt"),
    )
