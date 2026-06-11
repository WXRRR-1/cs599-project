"""Streamlit UI for ResearchFlow-Agent."""

from __future__ import annotations

import streamlit as st

from main import run_research


st.set_page_config(page_title="ResearchFlow-Agent", layout="wide")

st.title("ResearchFlow-Agent")
st.write("面向研究生的自动化文献调研与报告生成智能体")

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
        with st.status("正在检索论文、筛选结果并生成报告...", expanded=True) as status:
            st.write("正在调用 OpenAlex API 检索论文")
            report = run_research(topic.strip(), limit=int(limit), top_k=int(top_k))
            status.update(label="调研报告已生成", state="complete")

        st.subheader("生成的 Markdown 报告")
        st.markdown(report)
        st.download_button(
            label="下载报告",
            data=report,
            file_name="sample_report.md",
            mime="text/markdown",
        )

st.divider()
st.caption("当前为 v0.1 Demo；优先使用 OpenAlex API 检索论文，失败后切换到 arXiv API；如果仍无结果，会使用内置示例论文展示完整流程；使用 LLM 或 mock 模式生成总结。")
