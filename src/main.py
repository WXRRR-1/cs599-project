"""Command-line entry point for ResearchFlow-Agent."""

from __future__ import annotations

import argparse

from config import LLM_PROVIDER
from workflow.research_graph import run_research_graph


def run_research(topic: str, limit: int = 10, top_k: int = 5) -> dict:
    """Run the LangGraph research workflow and return the final state."""
    return run_research_graph(topic, limit=limit, top_k=top_k)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ResearchFlow-Agent v0.2 LangGraph Demo")
    parser.add_argument("topic", nargs="?", default="Agentic RAG", help="研究主题")
    parser.add_argument("--limit", type=int, default=10, help="检索论文数量")
    parser.add_argument("--top-k", type=int, default=5, help="筛选论文数量")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    result = run_research(args.topic, limit=args.limit, top_k=args.top_k)
    evaluation = result.get("evaluation", {})

    print(f"候选论文数量：{len(result.get('candidate_papers', []))}")
    print(f"筛选论文数量：{len(result.get('selected_papers', []))}")
    print(f"报告保存路径：{result.get('report_path', 'N/A')}")
    print(f"LLM Provider：{LLM_PROVIDER}")
    print(f"evaluation status：{evaluation.get('status', 'unknown')}")

    errors = result.get("errors", [])
    if errors:
        print(f"工作流错误数量：{len(errors)}")
