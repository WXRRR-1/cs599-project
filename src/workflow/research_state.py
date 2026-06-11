"""Shared state schema for the ResearchFlow-Agent LangGraph workflow."""

from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class ResearchState(TypedDict, total=False):
    """State passed between LangGraph nodes."""

    topic: str
    limit: int
    top_k: int
    keywords: List[str]
    candidate_papers: List[Dict[str, Any]]
    selected_papers: List[Dict[str, Any]]
    summaries: List[Dict[str, Any]]
    report: str
    report_path: str
    evaluation: Dict[str, Any]
    logs: List[str]
    errors: List[str]
    search_source: str
