"""Paper summary agent with configurable LLM provider and mock fallback."""

from __future__ import annotations

import json

from config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
    LLM_PROVIDER,
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENAI_MODEL,
)


def _short_text(text: str, max_len: int = 180) -> str:
    text = " ".join((text or "").split())
    return text[:max_len] + ("..." if len(text) > max_len else "")


def _mock_summary(paper: dict) -> dict:
    """Generate a deterministic Chinese summary when no LLM key is available."""
    abstract = _short_text(paper.get("abstract", ""))
    title = paper.get("title", "未知论文")
    return {
        "title": title,
        "year": paper.get("year", "N/A"),
        "authors": paper.get("authors", "N/A"),
        "background": f"该论文围绕“{title}”展开，摘要显示其研究背景与当前智能系统、信息检索或相关任务的发展需求有关。",
        "problem": "论文关注的问题可从摘要中概括为：如何在既有方法基础上提升任务效果、系统能力或应用可靠性。",
        "method": f"根据摘要，论文主要方法包括：{abstract}",
        "contribution": "该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。",
        "limitation": "当前 mock 模式仅基于标题和摘要生成概括，具体局限性需要进一步阅读全文确认。",
        "url": paper.get("url", ""),
    }


def _build_prompt(paper: dict) -> str:
    return f"""
请基于下面论文的标题和摘要，生成中文结构化总结。
要求：
1. 只基于给定标题和摘要，不要编造摘要中没有的信息；
2. 如果某项信息无法判断，请写“摘要中未明确说明”；
3. 只返回 JSON，不要输出 Markdown。

JSON 字段：
title, year, authors, background, problem, method, contribution, limitation, url

论文标题：{paper.get("title", "")}
作者：{paper.get("authors", "")}
年份：{paper.get("year", "")}
链接：{paper.get("url", "")}
摘要：{paper.get("abstract", "")}
""".strip()


def _call_openai_compatible(paper: dict, provider: str) -> dict:
    """Call OpenAI-compatible chat completion APIs and parse JSON result."""
    from openai import OpenAI

    if provider == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY 未配置")
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
        model = OPENAI_MODEL
    elif provider == "deepseek":
        if not DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY 未配置")
        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
        model = DEEPSEEK_MODEL
    else:
        raise ValueError(f"不支持的 LLM_PROVIDER：{provider}")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是严谨的中文学术文献总结助手。"},
            {"role": "user", "content": _build_prompt(paper)},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or "{}"
    summary = json.loads(content)

    # Keep important metadata available even if the model omits a field.
    fallback = _mock_summary(paper)
    fallback.update({key: summary.get(key) or fallback[key] for key in fallback})
    return fallback


def summarize_paper(paper: dict) -> dict:
    """Summarize one paper with configured LLM provider or mock fallback."""
    provider = LLM_PROVIDER or "mock"
    if provider == "mock":
        return _mock_summary(paper)

    try:
        return _call_openai_compatible(paper, provider)
    except Exception as exc:
        print(f"LLM 总结失败，已回退到 mock 模式：{exc}")
        return _mock_summary(paper)


def summarize_papers(papers: list[dict]) -> list[dict]:
    """Summarize a list of papers."""
    return [summarize_paper(paper) for paper in papers]
