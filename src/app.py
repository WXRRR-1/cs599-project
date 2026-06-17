"""Streamlit UI for ResearchFlow-Agent."""

from __future__ import annotations

import streamlit as st

from config import LLM_DRY_RUN, LLM_PROVIDER, USE_DEMO_FALLBACK
from main import run_research
from memory.history_store import load_recent_history


st.set_page_config(page_title="ResearchFlow-Agent", layout="wide")

st.title("ResearchFlow-Agent")
st.write("面向研究生的自动化文献调研与报告生成智能体")

status_col1, status_col2, status_col3, status_col4 = st.columns(4)
status_col1.info(f"配置 LLM Provider: {LLM_PROVIDER}")
status_col2.info(f"LLM_DRY_RUN: {'true' if LLM_DRY_RUN else 'false'}")
status_col3.info("Mock summary fallback: 已启用")
status_col4.info(f"Demo paper fallback: {'已启用' if USE_DEMO_FALLBACK else '未启用'}")

if LLM_PROVIDER == "deepseek":
    st.success("当前配置为 DeepSeek API。若调用失败，系统会自动回退到 mock 总结。")
else:
    st.warning("当前配置为 mock 模式，不需要 LLM API Key，也可以跑通完整 Demo。")
if LLM_DRY_RUN:
    st.warning("LLM_DRY_RUN=true：当前不会真实调用 DeepSeek，可避免开发阶段产生 LLM 调用费用。")

topic = st.text_input("研究主题", value="Agentic RAG")

col1, col2 = st.columns(2)
with col1:
    limit = st.number_input("检索论文数量 limit", min_value=1, max_value=50, value=10, step=1)
with col2:
    top_k = st.number_input("筛选论文数量 top_k", min_value=1, max_value=20, value=5, step=1)

if st.button("开始调研", type="primary"):
    normalized_topic = topic.strip() or "Agentic RAG"
    if not topic.strip():
        st.info("研究主题为空，已使用默认主题 Agentic RAG。")

    with st.status("LangGraph Agent 正在执行调研工作流...", expanded=True) as status:
        st.write("Planner -> Search -> Filter -> Summary -> Report -> Evaluator")
        result = run_research(normalized_topic, limit=int(limit), top_k=int(top_k))
        status.update(label="调研报告已生成", state="complete")

    candidate_papers = result.get("candidate_papers", []) or []
    selected_papers = result.get("selected_papers", []) or []
    evaluation = result.get("evaluation", {}) or {}
    cache_info = result.get("cache_info", {}) or {}
    logs = result.get("logs", []) or []
    errors = result.get("errors", []) or []
    report = result.get("report", "") or ""

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    metric_col1.metric("候选论文数量", len(candidate_papers))
    metric_col2.metric("筛选后论文数量", len(selected_papers))
    metric_col3.metric("Evaluation", evaluation.get("status", "unknown"))
    metric_col4.metric("实际 LLM", evaluation.get("llm_provider", "unknown"))

    cache_col1, cache_col2, cache_col3 = st.columns(3)
    cache_col1.metric("Search Cache", "hit" if cache_info.get("search_cache_hit") else "miss")
    cache_col2.metric("Summary Cache Hit", cache_info.get("summary_cache_hits", 0))
    cache_col3.metric("Summary Cache Miss", cache_info.get("summary_cache_misses", 0))

    if selected_papers:
        st.subheader("筛选后论文")
        table_rows = [
            {
                "title": paper.get("title", ""),
                "year": paper.get("year", ""),
                "authors": paper.get("authors", ""),
                "citationCount": paper.get("citationCount", 0),
                "relevance_score": paper.get("relevance_score", 0),
                "score_breakdown": paper.get("score_breakdown", {}),
                "score_reason": paper.get("score_reason", ""),
                "venue": paper.get("venue", ""),
                "source": paper.get("source", ""),
                "url": paper.get("url", ""),
            }
            for paper in selected_papers
        ]
        st.dataframe(table_rows, use_container_width=True)

    if logs:
        with st.expander("LangGraph 执行日志", expanded=True):
            for log in logs:
                st.write(f"- {log}")

    if evaluation:
        with st.expander("Evaluation 结果", expanded=True):
            st.json(evaluation)

    if errors:
        st.warning("工作流执行过程中出现可恢复问题：")
        for error in errors:
            st.write(f"- {error}")

    st.subheader("生成的 Markdown 报告")
    st.markdown(report)
    st.download_button(
        label="下载报告",
        data=report,
        file_name="sample_report.md",
        mime="text/markdown",
    )

st.divider()
st.subheader("最近任务历史")
recent_history = load_recent_history(limit=10)
if recent_history:
    st.dataframe(recent_history, use_container_width=True)
else:
    st.caption("暂无历史记录。运行一次调研后会自动生成。")

st.caption(
    "当前为 v0.3.2 Demo；使用 OpenAlex / arXiv 检索论文，"
    "使用 LangGraph 编排多步骤 Agent 工作流，使用 DeepSeek API 或 mock 模式生成总结。"
)
