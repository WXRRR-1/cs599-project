"""Connectivity check for academic APIs used by ResearchFlow-Agent."""

from __future__ import annotations

from tools.arxiv_search_tool import search_arxiv_papers
from tools.openalex_search_tool import search_openalex_papers


def _check_api(name: str, search_fn) -> None:
    print(f"\n=== {name} ===")
    papers = search_fn("reinforcement learning", limit=3)
    if not papers:
        print("状态：不可用或未返回带摘要的论文")
        return

    print(f"状态：可用，返回 {len(papers)} 篇论文")
    for index, paper in enumerate(papers[:2], start=1):
        print(f"{index}. {paper.get('title')} ({paper.get('year')})")


if __name__ == "__main__":
    _check_api("OpenAlex", search_openalex_papers)
    _check_api("arXiv", search_arxiv_papers)
