"""LangGraph workflow assembly for ResearchFlow-Agent."""

from __future__ import annotations

from langgraph.graph import END, StateGraph

from workflow.nodes import (
    evaluator_node,
    filter_node,
    planner_node,
    report_node,
    search_node,
    summary_node,
)
from workflow.research_state import ResearchState


def build_research_graph():
    """Build the ResearchFlow-Agent LangGraph workflow."""
    graph = StateGraph(ResearchState)
    graph.add_node("planner", planner_node)
    graph.add_node("search", search_node)
    graph.add_node("filter", filter_node)
    graph.add_node("summary", summary_node)
    graph.add_node("report", report_node)
    graph.add_node("evaluator", evaluator_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "search")
    graph.add_edge("search", "filter")
    graph.add_edge("filter", "summary")
    graph.add_edge("summary", "report")
    graph.add_edge("report", "evaluator")
    graph.add_edge("evaluator", END)
    return graph.compile()


def run_research_graph(topic: str, limit: int = 10, top_k: int = 5) -> dict:
    """Run the LangGraph research workflow and return the final state."""
    app = build_research_graph()
    initial_state: ResearchState = {
        "topic": topic,
        "limit": limit,
        "top_k": top_k,
        "logs": [],
        "errors": [],
    }
    result = app.invoke(initial_state)
    return dict(result)
