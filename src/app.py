"""Streamlit UI for ResearchFlow-Agent."""

from __future__ import annotations

import streamlit as st

from config import LLM_PROVIDER
from main import run_research


st.set_page_config(page_title="ResearchFlow-Agent", layout="wide")

st.title("ResearchFlow-Agent")
st.write("面向研究生的自动化文献调研与报告生成智能体")

st.info(f"当前 LLM Provider: {LLM_PROVIDER}")
if LLM_PROVIDER == "deepseek":
    st.success("当前使用 DeepSeek API 生成论文总结。")
else:
    st.warning("当前未使用真实 LLM，总结内容由 mock 模式生成。")

topic = st.text_input("研究主题", value="Agentic RAG")

col1, col2 = st.columns(2)
with col1:
    limit = st.number_input("检索论文数量 limit", min_value=1, max_value=50, value=10, step=1)
with col2:
    top_k = st.number_input("筛选论文数量 top_k", min_value=1, max_value=10, value=5, step=1)

if st.button("开始调研", type="primary"):
    if not topic.strip():
        st.warning("请输入研究主题。")
    else:
        with st.status("LangGraph Agent 正在执行调研工作流...", expanded=True) as status:
            st.write("Planner → Search → Filter → Summary → Report → Evaluator")
            result = run_research(topic.strip(), limit=int(limit), top_k=int(top_k))
            status.update(label="调研报告已生成", state="complete")

        candidate_papers = result.get("candidate_papers", [])
        selected_papers = result.get("selected_papers", [])
        evaluation = result.get("evaluation", {})
        logs = result.get("logs", [])
        errors = result.get("errors", [])
        report = result.get("report", "")

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("候选论文数量", len(candidate_papers))
        metric_col2.metric("筛选后论文数量", len(selected_papers))
        metric_col3.metric("Evaluation", evaluation.get("status", "unknown"))

        if selected_papers:
            st.subheader("筛选后论文")
            table_rows = [
                {
                    "title": paper.get("title", ""),
                    "year": paper.get("year", ""),
                    "authors": paper.get("authors", ""),
                    "citationCount": paper.get("citationCount", 0),
                    "venue": paper.get("venue", ""),
                    "url": paper.get("url", ""),
                }
                for paper in selected_papers
            ]
            st.dataframe(table_rows, use_container_width=True)

        if logs:
            with st.expander("Agent 执行日志", expanded=True):
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
st.caption("当前为 v0.2 Demo；使用 LangGraph 编排 Planner、Search、Filter、Summary、Report、Evaluator 节点；LLM 使用 DeepSeek API 或 mock 模式。")
