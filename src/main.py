"""Command-line entry point for ResearchFlow-Agent."""

from __future__ import annotations

import argparse

from config import LLM_PROVIDER
from memory.history_store import append_history
from workflow.research_graph import run_research_graph


def _append_run_history(result: dict, topic: str) -> None:
    """Write a compact run record without interrupting the main workflow."""
    evaluation = result.get("evaluation", {}) or {}
    append_history(
        {
            "topic": result.get("topic") or topic or "Agentic RAG",
            "candidate_count": len(result.get("candidate_papers", []) or []),
            "selected_count": len(result.get("selected_papers", []) or []),
            "llm_provider": evaluation.get("llm_provider", LLM_PROVIDER),
            "evaluation_status": evaluation.get("status", "unknown"),
            "report_path": result.get("report_path", ""),
            "errors": result.get("errors", []) or [],
        }
    )


def run_research(topic: str, limit: int = 10, top_k: int = 5) -> dict:
    """Run the LangGraph research workflow and return the final state."""
    normalized_topic = (topic or "Agentic RAG").strip() or "Agentic RAG"
    result = run_research_graph(normalized_topic, limit=limit, top_k=top_k)
    _append_run_history(result, normalized_topic)
    return result


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ResearchFlow-Agent v0.3.6 Demo")
    parser.add_argument("topic", nargs="?", default="Agentic RAG", help="研究主题")
    parser.add_argument("--limit", type=int, default=10, help="检索论文数量")
    parser.add_argument("--top-k", type=int, default=5, help="筛选论文数量")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    result = run_research(args.topic, limit=args.limit, top_k=args.top_k)
    evaluation = result.get("evaluation", {}) or {}

    print(f"候选论文数量：{len(result.get('candidate_papers', []) or [])}")
    print(f"筛选论文数量：{len(result.get('selected_papers', []) or [])}")
    print(f"报告保存路径：{result.get('report_path', 'N/A')}")
    print(f"配置 LLM Provider：{LLM_PROVIDER}")
    print(f"实际 LLM Provider：{evaluation.get('llm_provider', 'unknown')}")
    print(f"evaluation status：{evaluation.get('status', 'unknown')}")

    errors = result.get("errors", []) or []
    if errors:
        print(f"工作流错误数量：{len(errors)}")
