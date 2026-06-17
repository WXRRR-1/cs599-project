"""Explainable rule-based paper filtering agent."""

from __future__ import annotations

from datetime import datetime


def _safe_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _normalize_keywords(topic: str, keywords: list[str] | None) -> list[str]:
    raw_keywords = [topic or "Agentic RAG"] + list(keywords or [])
    normalized = []
    for keyword in raw_keywords:
        text = " ".join(str(keyword or "").lower().split())
        if text and text not in normalized:
            normalized.append(text)
    return normalized


def _keyword_score(paper: dict, keywords: list[str]) -> tuple[int, list[str]]:
    title = str(paper.get("title", "") or "").lower()
    abstract = str(paper.get("abstract", "") or "").lower()
    score = 0
    matched = []

    for keyword in keywords:
        keyword_hit = False
        if keyword in title:
            score += 14
            keyword_hit = True
        if keyword in abstract:
            score += 7
            keyword_hit = True
        if keyword_hit:
            matched.append(keyword)

    return min(score, 40), matched[:5]


def _year_score(year) -> int:
    year_value = _safe_int(year)
    if not year_value:
        return 0

    current_year = datetime.utcnow().year
    age = current_year - year_value
    if age <= 3:
        return 30
    if age <= 5:
        return 22
    if age <= 10:
        return 14
    return 6


def _citation_score(citation_count) -> int:
    count = _safe_int(citation_count)
    if count >= 1000:
        return 30
    if count >= 500:
        return 25
    if count >= 100:
        return 18
    if count >= 50:
        return 12
    if count > 0:
        return 6
    return 0


def _score_reason(matched_keywords: list[str], year_score: int, citation_score: int) -> str:
    parts = []
    if matched_keywords:
        parts.append(f"标题或摘要命中关键词：{', '.join(matched_keywords)}")
    else:
        parts.append("标题和摘要未明显命中规划关键词")

    if year_score >= 30:
        parts.append("年份较新")
    elif year_score >= 14:
        parts.append("年份具有一定时效性")
    else:
        parts.append("年份较早或缺失")

    if citation_score >= 25:
        parts.append("引用量较高")
    elif citation_score >= 12:
        parts.append("引用量中等")
    else:
        parts.append("引用量较低或暂缺")

    return "，".join(parts) + "。"


def score_paper(paper: dict, topic: str = "Agentic RAG", keywords: list[str] | None = None) -> dict:
    """Return a copy of paper with explainable relevance scoring fields."""
    normalized_keywords = _normalize_keywords(topic, keywords)
    keyword_score, matched_keywords = _keyword_score(paper, normalized_keywords)
    year_score = _year_score(paper.get("year"))
    citation_score = _citation_score(paper.get("citationCount"))
    relevance_score = min(100, keyword_score + year_score + citation_score)

    scored = dict(paper)
    scored.setdefault("source", paper.get("venue", "unknown") or "unknown")
    scored["relevance_score"] = relevance_score
    scored["score_breakdown"] = {
        "keyword_score": keyword_score,
        "year_score": year_score,
        "citation_score": citation_score,
    }
    scored["score_reason"] = _score_reason(matched_keywords, year_score, citation_score)
    return scored


def filter_papers(
    papers: list[dict],
    top_k: int = 5,
    topic: str = "Agentic RAG",
    keywords: list[str] | None = None,
) -> list[dict]:
    """Select representative papers using an explainable relevance score."""
    valid_papers = [paper for paper in papers if paper.get("title") and paper.get("abstract")]
    scored_papers = [score_paper(paper, topic=topic, keywords=keywords) for paper in valid_papers]

    def sort_key(paper: dict) -> tuple[int, int, int]:
        return (
            paper.get("relevance_score", 0),
            _safe_int(paper.get("year")),
            _safe_int(paper.get("citationCount")),
        )

    preferred_papers = [
        paper
        for paper in scored_papers
        if paper.get("score_breakdown", {}).get("keyword_score", 0) > 0
    ]
    fallback_papers = [
        paper
        for paper in scored_papers
        if paper.get("score_breakdown", {}).get("keyword_score", 0) <= 0
    ]

    sorted_preferred = sorted(preferred_papers, key=sort_key, reverse=True)
    sorted_fallback = sorted(fallback_papers, key=sort_key, reverse=True)

    if sorted_preferred:
        sorted_papers = sorted_preferred + sorted_fallback
    else:
        sorted_papers = sorted(
            scored_papers,
            key=sort_key,
            reverse=True,
        )

    return sorted_papers[: max(1, top_k)]
