"""Paper summary agent with DeepSeek-compatible LLM support and mock fallback."""

from __future__ import annotations

import json

from cache.cache_store import get_cached_value, make_cache_key, set_cached_value
from config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
    LLM_DRY_RUN,
    LLM_MAX_RETRIES,
    LLM_PROVIDER,
    LLM_TIMEOUT_SECONDS,
    MAX_ABSTRACT_CHARS,
    MAX_LLM_PAPERS,
)


_ACTIVE_LLM_PROVIDER = "mock"
_SUMMARY_CACHE_HITS = 0
_SUMMARY_CACHE_MISSES = 0


def get_active_llm_provider() -> str:
    """Return the provider that was actually used by the latest summary run."""
    return _ACTIVE_LLM_PROVIDER


def get_summary_cache_stats() -> dict:
    """Return cache hit/miss counts for the latest batch summary run."""
    return {
        "summary_cache_hits": _SUMMARY_CACHE_HITS,
        "summary_cache_misses": _SUMMARY_CACHE_MISSES,
    }


def _reset_summary_cache_stats() -> None:
    global _SUMMARY_CACHE_HITS, _SUMMARY_CACHE_MISSES
    _SUMMARY_CACHE_HITS = 0
    _SUMMARY_CACHE_MISSES = 0


def _set_active_llm_provider(provider: str) -> None:
    global _ACTIVE_LLM_PROVIDER
    _ACTIVE_LLM_PROVIDER = provider


def _short_text(text: str, max_len: int = 180) -> str:
    text = " ".join((text or "").split())
    return text[:max_len] + ("..." if len(text) > max_len else "")


def _limited_abstract(paper: dict) -> str:
    abstract = " ".join((paper.get("abstract", "") or "").split())
    return abstract[:MAX_ABSTRACT_CHARS]


def _mock_summary(paper: dict) -> dict:
    """Generate a deterministic Chinese summary when no LLM key is available."""
    abstract = _short_text(paper.get("abstract", ""))
    title = paper.get("title") or "未知论文"
    return _attach_paper_metadata(
        {
        "title": title,
        "year": paper.get("year", "N/A"),
        "authors": paper.get("authors", "N/A"),
        "background": f"该论文围绕“{title}”展开，摘要显示其研究背景与当前智能系统、信息检索或相关任务的发展需求有关。",
        "problem": "论文关注的核心问题可从摘要中概括为：如何在已有方法基础上提升任务效果、系统能力或应用可靠性。",
        "method": f"根据摘要，论文主要方法包括：{abstract or '摘要信息有限，无法判断'}",
        "contribution": "该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。",
        "limitation": "当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。",
        "url": paper.get("url", ""),
        },
        paper,
    )


def _attach_paper_metadata(summary: dict, paper: dict) -> dict:
    """Preserve filter metadata so report generation can explain selection."""
    enriched = dict(summary)
    for key in ("source", "relevance_score", "score_breakdown", "score_reason"):
        if key in paper and key not in enriched:
            enriched[key] = paper.get(key)
    return enriched


def _build_prompt(paper: dict) -> str:
    return f"""
请基于下面论文的标题和摘要，生成中文结构化总结。
要求：
1. 只基于给定标题、作者、年份、链接和摘要，不要编造摘要中没有的信息；
2. 如果某项信息无法判断，请写“摘要信息有限，无法判断”；
3. 只返回 JSON，不要输出 Markdown。

JSON 字段：title, year, authors, background, problem, method, contribution, limitation, url

论文标题：{paper.get("title", "")}
作者：{paper.get("authors", "")}
年份：{paper.get("year", "")}
链接：{paper.get("url", "")}
摘要：{_limited_abstract(paper)}
""".strip()


def _parse_llm_json(content: str) -> dict:
    """Parse JSON content returned by the LLM, tolerating simple code fences."""
    text = (content or "{}").strip()
    if text.startswith("```"):
        text = text.strip("`").strip()
        if text.lower().startswith("json"):
            text = text[4:].strip()
    return json.loads(text)


def _summary_cache_key(paper: dict, provider_mode: str) -> str:
    return make_cache_key(
        "summary",
        provider_mode,
        paper.get("title", ""),
        paper.get("url", ""),
        paper.get("year", ""),
    )


def _get_cached_summary(paper: dict, provider_mode: str) -> dict | None:
    global _SUMMARY_CACHE_HITS, _SUMMARY_CACHE_MISSES

    cached = get_cached_value("summary", _summary_cache_key(paper, provider_mode))
    if isinstance(cached, dict):
        _SUMMARY_CACHE_HITS += 1
        summary = cached.get("summary") if isinstance(cached.get("summary"), dict) else cached
        _set_active_llm_provider(cached.get("provider", provider_mode))
        return _attach_paper_metadata(summary, paper)

    _SUMMARY_CACHE_MISSES += 1
    return None


def _set_cached_summary(paper: dict, provider_mode: str, summary: dict) -> None:
    set_cached_value(
        "summary",
        _summary_cache_key(paper, provider_mode),
        {"provider": provider_mode, "summary": summary},
    )


def _call_deepseek(paper: dict) -> dict:
    """Call DeepSeek through the OpenAI-compatible SDK and parse JSON result."""
    from openai import OpenAI

    if not DEEPSEEK_API_KEY:
        raise ValueError("DEEPSEEK_API_KEY 未配置")

    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL,
        timeout=LLM_TIMEOUT_SECONDS,
    )

    last_error: Exception | None = None
    for _ in range(LLM_MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=DEEPSEEK_MODEL,
                messages=[
                    {"role": "system", "content": "你是严谨的中文学术文献总结助手。"},
                    {"role": "user", "content": _build_prompt(paper)},
                ],
                temperature=0.2,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content or "{}"
            summary = _parse_llm_json(content)

            fallback = _mock_summary(paper)
            fallback.update({key: summary.get(key) or fallback[key] for key in fallback})
            return _attach_paper_metadata(fallback, paper)
        except Exception as exc:
            last_error = exc

    raise last_error or RuntimeError("DeepSeek 调用失败")


def _provider_mode(allow_llm_call: bool = True) -> str:
    provider = (LLM_PROVIDER or "mock").strip().lower()
    if provider == "mock":
        return "mock"
    if provider != "deepseek":
        return "mock"
    if LLM_DRY_RUN:
        return "deepseek_dry_run_mock"
    if not DEEPSEEK_API_KEY:
        return "deepseek_failed_fallback_mock"
    if not allow_llm_call:
        return "mock"
    return "deepseek"


def summarize_paper(paper: dict, allow_llm_call: bool = True) -> dict:
    """Summarize one paper with configured LLM provider or mock fallback."""
    mode = _provider_mode(allow_llm_call=allow_llm_call)
    cached = _get_cached_summary(paper, mode)
    if cached:
        return cached

    if mode != "deepseek":
        _set_active_llm_provider(mode)
        summary = _mock_summary(paper)
        _set_cached_summary(paper, mode, summary)
        return summary

    try:
        summary = _call_deepseek(paper)
        _set_active_llm_provider("deepseek")
        _set_cached_summary(paper, "deepseek", summary)
        return summary
    except Exception as exc:
        mode = "deepseek_failed_fallback_mock"
        _set_active_llm_provider(mode)
        print(f"DeepSeek 总结失败，已回退到 mock 模式：{exc.__class__.__name__}")
        summary = _mock_summary(paper)
        _set_cached_summary(paper, mode, summary)
        return summary


def summarize_papers(papers: list[dict]) -> list[dict]:
    """Summarize a list of papers with cache and cost protection."""
    _reset_summary_cache_stats()
    if not papers:
        _set_active_llm_provider("mock" if LLM_PROVIDER == "mock" else _provider_mode())
        return []

    if LLM_PROVIDER == "deepseek" and LLM_DRY_RUN:
        _set_active_llm_provider("deepseek_dry_run_mock")
        print("LLM_DRY_RUN=true，本次不会真实调用 DeepSeek，已使用 mock 模式总结。")
    elif LLM_PROVIDER == "deepseek" and not DEEPSEEK_API_KEY:
        _set_active_llm_provider("deepseek_failed_fallback_mock")
        print("DeepSeek API Key 未配置，已使用 mock 模式完成本次批量总结。")

    summaries = []
    for index, paper in enumerate(papers):
        allow_llm_call = index < MAX_LLM_PAPERS
        summaries.append(summarize_paper(paper, allow_llm_call=allow_llm_call))
    return summaries
