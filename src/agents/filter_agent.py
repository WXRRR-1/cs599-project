"""Simple rule-based paper filtering agent."""

from __future__ import annotations


def _score_paper(paper: dict) -> tuple[int, int]:
    """Score papers by citation count first and publication year second."""
    citation_count = int(paper.get("citationCount") or 0)
    year = paper.get("year") or 0
    try:
        year_value = int(year)
    except (TypeError, ValueError):
        year_value = 0
    return citation_count, year_value


def filter_papers(papers: list[dict], top_k: int = 5) -> list[dict]:
    """Select representative papers using a stable citation/year heuristic."""
    valid_papers = [paper for paper in papers if paper.get("abstract")]
    sorted_papers = sorted(valid_papers, key=_score_paper, reverse=True)
    return sorted_papers[: max(1, top_k)]
