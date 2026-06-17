"""Run benchmark topics and write a Markdown evaluation report."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import time
from typing import Any


SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import PROJECT_ROOT  # noqa: E402
from evaluation.metrics import evaluate_research_result  # noqa: E402
from main import run_research  # noqa: E402


TOPICS_PATH = Path(__file__).resolve().with_name("benchmark_topics.json")
OUTPUT_PATH = PROJECT_ROOT / "src" / "outputs" / "eval_results.md"


def _load_topics() -> list[str]:
    return json.loads(TOPICS_PATH.read_text(encoding="utf-8"))


def _metric_to_row(metric: dict[str, Any]) -> str:
    return (
        f"| {metric['topic']} | {metric['status']} | "
        f"{metric['candidate_count']} | {metric['selected_count']} | "
        f"{metric['llm_provider']} | {metric['fallback_used']} | "
        f"{metric.get('keyword_hit_rate', 0)} | "
        f"{metric.get('avg_relevance_score', 0)} | "
        f"{metric['runtime_seconds']} | {metric['has_errors']} |"
    )


def _build_report(metrics: list[dict[str, Any]]) -> str:
    total = len(metrics)
    pass_count = sum(1 for item in metrics if item["status"] == "pass")
    error_count = sum(1 for item in metrics if item["has_errors"])
    avg_runtime = round(
        sum(item["runtime_seconds"] for item in metrics) / total,
        2,
    ) if total else 0
    avg_keyword_hit_rate = round(
        sum(item.get("keyword_hit_rate", 0) for item in metrics) / total,
        2,
    ) if total else 0
    avg_relevance_score = round(
        sum(item.get("avg_relevance_score", 0) for item in metrics) / total,
        2,
    ) if total else 0
    pass_rate = round(pass_count / total * 100, 1) if total else 0

    rows = "\n".join(_metric_to_row(metric) for metric in metrics)
    return f"""# ResearchFlow-Agent Benchmark Evaluation

## Summary

- Benchmark topics: {total}
- Pass count: {pass_count}
- Pass rate: {pass_rate}%
- Average runtime: {avg_runtime}s
- Average keyword hit rate: {avg_keyword_hit_rate}
- Average relevance score: {avg_relevance_score}
- Error count: {error_count}

## Results

| Topic | Status | Candidate Count | Selected Count | LLM Provider | Fallback Used | Keyword Hit Rate | Avg Relevance Score | Runtime Seconds | Has Errors |
|---|---|---:|---:|---|---|---:|---:|---:|---|
{rows}
"""


def run_benchmark() -> list[dict[str, Any]]:
    """Run all benchmark topics and return metric records."""
    metrics: list[dict[str, Any]] = []
    for topic in _load_topics():
        start = time.perf_counter()
        try:
            result = run_research(topic)
            runtime = time.perf_counter() - start
            metric = evaluate_research_result(topic, result, runtime)
        except Exception as exc:
            runtime = time.perf_counter() - start
            metric = {
                "topic": topic,
                "search_success": False,
                "candidate_count": 0,
                "selected_count": 0,
                "report_generated": False,
                "has_references": False,
                "has_comparison_table": False,
                "llm_provider": "unknown",
                "fallback_used": False,
                "keyword_hit_rate": 0,
                "avg_relevance_score": 0,
                "has_errors": True,
                "runtime_seconds": round(runtime, 2),
                "status": "error",
                "error_type": exc.__class__.__name__,
            }
        metrics.append(metric)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(_build_report(metrics), encoding="utf-8")
    return metrics


if __name__ == "__main__":
    results = run_benchmark()
    pass_count = sum(1 for item in results if item["status"] == "pass")
    print(f"Benchmark topics: {len(results)}")
    print(f"Pass count: {pass_count}")
    print(f"Evaluation report: {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
