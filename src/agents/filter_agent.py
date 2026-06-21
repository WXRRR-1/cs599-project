"""Explainable rule-based paper filtering agent."""

from __future__ import annotations

from datetime import datetime


def _safe_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
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


def _keyword_score(paper: dict, keywords: list[str]) -> tuple[int, list[str], float]:
    title = str(paper.get("title", "") or "").lower()
    abstract = str(paper.get("abstract", "") or "").lower()
    matched = []
    title_hits = 0
    abstract_hits = 0

    for keyword in keywords:
        keyword_hit = False
        if keyword in title:
            title_hits += 1
            keyword_hit = True
        if keyword in abstract:
            abstract_hits += 1
            keyword_hit = True
        if keyword_hit:
            matched.append(keyword)

    keyword_count = max(1, len(keywords))
    unique_matched = list(dict.fromkeys(matched))
    keyword_coverage = len(unique_matched) / keyword_count
    title_hit_ratio = title_hits / keyword_count
    abstract_hit_ratio = abstract_hits / keyword_count
    score = round(
        25 * keyword_coverage
        + 12 * title_hit_ratio
        + 8 * abstract_hit_ratio
    )

    return min(score, 45), unique_matched[:5], round(keyword_coverage, 2)


def _year_score(year) -> int:
    year_value = _safe_int(year)
    if not year_value:
        return 0

    current_year = datetime.utcnow().year
    age = current_year - year_value
    if age <= 2:
        return 25
    if age <= 4:
        return 20
    if age <= 7:
        return 14
    if age <= 10:
        return 8
    return 3


def _citation_per_year(citation_count, year) -> float:
    count = _safe_int(citation_count)
    year_value = _safe_int(year)
    current_year = datetime.utcnow().year
    if year_value:
        paper_age = max(1, current_year - year_value + 1)
    else:
        paper_age = 1
    return round(count / paper_age, 2)


def _citation_score(citation_count, year) -> tuple[int, float]:
    citation_per_year = _citation_per_year(citation_count, year)
    if citation_per_year >= 100:
        return 30, citation_per_year
    if citation_per_year >= 50:
        return 24, citation_per_year
    if citation_per_year >= 20:
        return 18, citation_per_year
    if citation_per_year >= 10:
        return 12, citation_per_year
    if citation_per_year > 0:
        return 6, citation_per_year
    return 0, citation_per_year


def _score_reason(
    matched_keywords: list[str],
    year_score: int,
    citation_score: int,
    keyword_coverage: float,
    citation_per_year: float,
) -> str:
    parts = []
    if matched_keywords:
        parts.append(
            f"标题或摘要命中关键词：{', '.join(matched_keywords)}，关键词覆盖率 {keyword_coverage:.2f}"
        )
    else:
        parts.append("标题和摘要未明显命中规划关键词")

    if year_score >= 25:
        parts.append("年份较新")
    elif year_score >= 14:
        parts.append("年份具有一定时效性")
    else:
        parts.append("年份较早或缺失")

    if citation_score >= 24:
        parts.append(f"年均引用影响力较高（{citation_per_year:.2f}/年）")
    elif citation_score >= 12:
        parts.append(f"年均引用影响力中等（{citation_per_year:.2f}/年）")
    else:
        parts.append(f"年均引用影响力较低或暂缺（{citation_per_year:.2f}/年）")

    return "，".join(parts) + "。"


def score_paper(paper: dict, topic: str = "Agentic RAG", keywords: list[str] | None = None) -> dict:
    """Return a copy of paper with explainable relevance scoring fields."""
    normalized_keywords = _normalize_keywords(topic, keywords)
    keyword_score, matched_keywords, keyword_coverage = _keyword_score(paper, normalized_keywords)
    year_score = _year_score(paper.get("year"))
    citation_score, citation_per_year = _citation_score(
        paper.get("citationCount"),
        paper.get("year"),
    )
    relevance_score = min(100, keyword_score + year_score + citation_score)

    scored = dict(paper)
    scored.setdefault("source", paper.get("venue", "unknown") or "unknown")
    scored["relevance_score"] = relevance_score
    scored["score_breakdown"] = {
        "keyword_score": keyword_score,
        "year_score": year_score,
        "citation_score": citation_score,
        "keyword_coverage": keyword_coverage,
        "citation_per_year": citation_per_year,
    }
    scored["score_reason"] = _score_reason(
        matched_keywords,
        year_score,
        citation_score,
        keyword_coverage,
        citation_per_year,
    )
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

    def sort_key(paper: dict) -> tuple[int, int, float, int]:
        breakdown = paper.get("score_breakdown", {})
        return (
            paper.get("relevance_score", 0),
            _safe_int(paper.get("year")),
            _safe_float(breakdown.get("citation_per_year")),
            _safe_int(paper.get("citationCount")),
        )

    preferred_papers = [
        paper
        for paper in scored_papers
        if paper.get("score_breakdown", {}).get("keyword_score", 0) >= 10
        or paper.get("score_breakdown", {}).get("keyword_coverage", 0) >= 0.25
    ]
    fallback_papers = [
        paper
        for paper in scored_papers
        if paper not in preferred_papers
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
