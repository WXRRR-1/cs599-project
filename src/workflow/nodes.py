"""LangGraph nodes for the ResearchFlow-Agent workflow."""

from __future__ import annotations

from agents.filter_agent import filter_papers
from agents.report_agent import generate_report, save_report
from agents.summary_agent import (
    get_active_llm_provider,
    get_summary_cache_stats,
    summarize_papers,
)
from config import LLM_DRY_RUN, LLM_PROVIDER, MAX_LLM_PAPERS, USE_DEMO_FALLBACK
from tools.arxiv_search_tool import get_last_arxiv_cache_hit, search_arxiv_papers
from tools.demo_paper_tool import get_demo_papers
from tools.openalex_search_tool import get_last_openalex_cache_hit, search_openalex_papers
from workflow.research_state import ResearchState


DEFAULT_REPORT_PATH = "src/outputs/sample_report.md"


def _with_logs(state: ResearchState, *messages: str) -> list[str]:
    return list(state.get("logs", [])) + [message for message in messages if message]


def _with_errors(state: ResearchState, *messages: str) -> list[str]:
    return list(state.get("errors", [])) + [message for message in messages if message]


def _with_cache_info(state: ResearchState, **items) -> dict:
    cache_info = dict(state.get("cache_info", {}) or {})
    cache_info.update(items)
    return cache_info


def planner_node(state: ResearchState) -> ResearchState:
    """Prepare the topic and simple keyword list for search."""
    topic = (state.get("topic") or "Agentic RAG").strip() or "Agentic RAG"
    normalized_topic = topic.lower()
    keywords = [topic]

    if "rag" in normalized_topic:
        keywords.extend(["Retrieval-Augmented Generation", "AI Agent", "Multi-Agent RAG"])
    elif "agent" in normalized_topic:
        keywords.extend(["AI Agent", "Agentic AI", "Multi-Agent Systems"])
    else:
        keywords.extend([f"{topic} survey", f"{topic} literature review"])

    return {
        "topic": topic,
        "keywords": keywords,
        "logs": _with_logs(state, f"Planner: topic='{topic}', keywords={len(keywords)}"),
    }


def search_node(state: ResearchState) -> ResearchState:
    """Search papers using OpenAlex, arXiv, and optional demo fallback."""
    topic = state.get("topic") or "Agentic RAG"
    limit = max(1, int(state.get("limit") or 10))

    try:
        papers = search_openalex_papers(topic, limit=limit)
        openalex_cache_hit = get_last_openalex_cache_hit()
        if papers:
            return {
                "candidate_papers": papers,
                "search_source": "OpenAlex",
                "cache_info": _with_cache_info(
                    state,
                    search_cache_hit=openalex_cache_hit,
                    search_cache_source="OpenAlex",
                ),
                "logs": _with_logs(
                    state,
                    f"Search: 使用 OpenAlex，候选论文数量 {len(papers)}",
                    f"Search cache: {'hit' if openalex_cache_hit else 'miss'}",
                ),
            }

        logs = _with_logs(state, "Search: OpenAlex 暂无可用结果，切换到 arXiv")
        papers = search_arxiv_papers(topic, limit=limit)
        arxiv_cache_hit = get_last_arxiv_cache_hit()
        if papers:
            return {
                "candidate_papers": papers,
                "search_source": "arXiv",
                "cache_info": _with_cache_info(
                    state,
                    search_cache_hit=arxiv_cache_hit,
                    search_cache_source="arXiv",
                ),
                "logs": logs
                + [
                    f"Search: 使用 arXiv，候选论文数量 {len(papers)}",
                    f"Search cache: {'hit' if arxiv_cache_hit else 'miss'}",
                ],
            }

        if USE_DEMO_FALLBACK:
            papers = get_demo_papers(topic, limit=limit)
            for paper in papers:
                paper.setdefault("source", "demo")
            return {
                "candidate_papers": papers,
                "search_source": "demo",
                "cache_info": _with_cache_info(
                    state,
                    search_cache_hit=False,
                    search_cache_source="demo",
                ),
                "logs": logs
                + [
                    "Search: arXiv 暂无可用结果，触发 demo fallback",
                    f"Search: 使用内置示例论文，候选论文数量 {len(papers)}",
                ],
            }

        return {
            "candidate_papers": [],
            "search_source": "none",
            "logs": logs + ["Search: 未启用 demo fallback，候选论文数量 0"],
            "errors": _with_errors(state, "Search: 未检索到可用论文"),
        }
    except Exception as exc:
        return {
            "candidate_papers": [],
            "search_source": "error",
            "logs": _with_logs(state, "Search: 检索节点异常，候选论文数量 0"),
            "errors": _with_errors(state, f"Search: {exc.__class__.__name__}"),
        }


def filter_node(state: ResearchState) -> ResearchState:
    """Filter candidate papers using the existing rule-based filter."""
    papers = state.get("candidate_papers", [])
    top_k = max(1, int(state.get("top_k") or 5))
    topic = state.get("topic") or "Agentic RAG"
    keywords = state.get("keywords", [])

    try:
        selected = filter_papers(papers, top_k=top_k, topic=topic, keywords=keywords)
        return {
            "selected_papers": selected,
            "logs": _with_logs(
                state,
                f"Filter: 输入 {len(papers)} 篇，筛选出 {len(selected)} 篇",
                "Filter: relevance_score = 关键词匹配分 + 年份分 + 引用量分",
            ),
        }
    except Exception as exc:
        return {
            "selected_papers": [],
            "logs": _with_logs(state, "Filter: 筛选节点异常"),
            "errors": _with_errors(state, f"Filter: {exc.__class__.__name__}"),
        }


def summary_node(state: ResearchState) -> ResearchState:
    """Summarize selected papers with DeepSeek or mock fallback."""
    selected = state.get("selected_papers", [])
    configured_provider = LLM_PROVIDER if LLM_PROVIDER in {"deepseek", "mock"} else "mock"

    try:
        summaries = summarize_papers(selected)
        active_provider = get_active_llm_provider()
        cache_stats = get_summary_cache_stats()
        fallback_note = (
            "；DeepSeek 调用失败时会自动回退到 mock"
            if configured_provider == "deepseek"
            else ""
        )
        return {
            "summaries": summaries,
            "cache_info": _with_cache_info(
                state,
                summary_cache_hit=cache_stats["summary_cache_hits"] > 0,
                **cache_stats,
            ),
            "logs": _with_logs(
                state,
                f"Summary: 配置 LLM_PROVIDER={configured_provider}{fallback_note}",
                f"Summary: 实际使用 provider={active_provider}",
                f"Summary: LLM_DRY_RUN={LLM_DRY_RUN}, MAX_LLM_PAPERS={MAX_LLM_PAPERS}",
                (
                    "Summary cache: "
                    f"hit={cache_stats['summary_cache_hits']}, "
                    f"miss={cache_stats['summary_cache_misses']}"
                ),
                f"Summary: 总结论文数量 {len(summaries)}",
            ),
        }
    except Exception as exc:
        return {
            "summaries": [],
            "logs": _with_logs(state, "Summary: 总结节点异常"),
            "errors": _with_errors(state, f"Summary: {exc.__class__.__name__}"),
        }


def report_node(state: ResearchState) -> ResearchState:
    """Generate and save the Markdown report."""
    topic = state.get("topic") or "Agentic RAG"
    summaries = state.get("summaries", [])

    try:
        report = generate_report(topic, summaries)
        save_report(report, DEFAULT_REPORT_PATH)
        return {
            "report": report,
            "report_path": DEFAULT_REPORT_PATH,
            "logs": _with_logs(state, f"Report: 报告已保存到 {DEFAULT_REPORT_PATH}"),
        }
    except Exception as exc:
        return {
            "report": "",
            "report_path": DEFAULT_REPORT_PATH,
            "logs": _with_logs(state, "Report: 报告节点异常"),
            "errors": _with_errors(state, f"Report: {exc.__class__.__name__}"),
        }


def evaluator_node(state: ResearchState) -> ResearchState:
    """Evaluate the generated report with lightweight rule checks."""
    report = state.get("report", "")
    selected = state.get("selected_papers", [])
    errors = state.get("errors", [])
    active_provider = get_active_llm_provider()

    evaluation = {
        "candidate_count": len(state.get("candidate_papers", [])),
        "paper_count": len(selected),
        "has_report": bool(report.strip()),
        "has_references": "## 7. 参考文献" in report and "暂无参考文献" not in report,
        "has_comparison_table": "| 论文 | 年份 | 核心方法 | 主要贡献 | 局限性 |" in report,
        "has_errors": bool(errors),
        "llm_provider": active_provider,
        "fallback_used": active_provider
        in {"mock", "deepseek_dry_run_mock", "deepseek_failed_fallback_mock"},
        "search_source": state.get("search_source", "unknown"),
        "cache_info": state.get("cache_info", {}),
        "llm_dry_run": LLM_DRY_RUN,
    }
    evaluation["status"] = (
        "pass"
        if evaluation["has_report"]
        and evaluation["paper_count"] > 0
        and evaluation["has_comparison_table"]
        and not evaluation["has_errors"]
        else "warning"
    )

    return {
        "evaluation": evaluation,
        "logs": _with_logs(state, f"Evaluator: status={evaluation['status']}"),
    }
