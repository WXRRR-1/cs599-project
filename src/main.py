"""Command-line entry point for ResearchFlow-Agent."""

from __future__ import annotations

import argparse

from agents.filter_agent import filter_papers
from agents.report_agent import generate_report, save_report
from agents.summary_agent import summarize_papers
from config import USE_DEMO_FALLBACK
from tools.arxiv_search_tool import search_arxiv_papers
from tools.demo_paper_tool import get_demo_papers
from tools.openalex_search_tool import search_openalex_papers


DEFAULT_OUTPUT_PATH = "src/outputs/sample_report.md"


def run_research(topic: str, limit: int = 10, top_k: int = 5) -> str:
    """Run the full research workflow and return the Markdown report."""
    papers = search_openalex_papers(topic, limit=limit)
    if not papers:
        print("OpenAlex 暂无可用结果，正在切换到 arXiv API 检索。")
        papers = search_arxiv_papers(topic, limit=limit)

    if not papers and USE_DEMO_FALLBACK:
        print("arXiv 暂无可用结果，已切换到内置示例论文以展示 Demo 效果。")
        papers = get_demo_papers(topic, limit=limit)

    selected_papers = filter_papers(papers, top_k=top_k)
    summaries = summarize_papers(selected_papers)
    report = generate_report(topic, summaries)
    save_report(report, DEFAULT_OUTPUT_PATH)

    print(f"检索到 {len(papers)} 篇包含标题和摘要的论文")
    print(f"筛选出 {len(selected_papers)} 篇代表性论文")
    print(f"报告保存路径：{DEFAULT_OUTPUT_PATH}")

    return report


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ResearchFlow-Agent v0.1 Demo")
    parser.add_argument("topic", nargs="?", default="Agentic RAG", help="研究主题")
    parser.add_argument("--limit", type=int, default=10, help="检索论文数量")
    parser.add_argument("--top-k", type=int, default=5, help="筛选论文数量")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    run_research(args.topic, limit=args.limit, top_k=args.top_k)
