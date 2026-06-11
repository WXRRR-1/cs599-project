"""Lightweight benchmark metrics for ResearchFlow-Agent."""

from __future__ import annotations


def evaluate_research_result(topic: str, result: dict, runtime_seconds: float) -> dict:
    """Convert one workflow result into a compact evaluation record."""
    evaluation = result.get("evaluation", {}) or {}
    errors = result.get("errors", []) or []
    candidate_count = len(result.get("candidate_papers", []) or [])
    selected_count = len(result.get("selected_papers", []) or [])
    report = result.get("report", "") or ""
    llm_provider = evaluation.get("llm_provider", "unknown")

    report_generated = bool(report.strip())
    has_references = "## 7. 参考文献" in report and "暂无参考文献" not in report
    has_comparison_table = "| 论文 | 年份 | 核心方法 | 主要贡献 | 局限性 |" in report
    has_errors = bool(errors) or bool(evaluation.get("has_errors"))

    status = (
        "pass"
        if candidate_count > 0
        and selected_count > 0
        and report_generated
        and has_references
        and has_comparison_table
        and not has_errors
        else "warning"
    )

    return {
        "topic": topic,
        "search_success": candidate_count > 0,
        "candidate_count": candidate_count,
        "selected_count": selected_count,
        "report_generated": report_generated,
        "has_references": has_references,
        "has_comparison_table": has_comparison_table,
        "llm_provider": llm_provider,
        "fallback_used": llm_provider in {"mock", "deepseek_failed_fallback_mock"},
        "has_errors": has_errors,
        "runtime_seconds": round(runtime_seconds, 2),
        "status": status,
    }
