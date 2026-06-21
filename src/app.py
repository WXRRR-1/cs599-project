"""Streamlit UI for ResearchFlow-Agent."""

from __future__ import annotations

from typing import Any

import streamlit as st

from config import LLM_DRY_RUN, LLM_PROVIDER, USE_DEMO_FALLBACK
from main import run_research
from memory.history_store import load_recent_history


APP_VERSION = "v0.3.9"


st.set_page_config(
    page_title="ResearchFlow-Agent",
    page_icon="RF",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 3rem;
        max-width: 1320px;
    }
    .rf-hero {
        padding: 1.35rem 1.45rem;
        border: 1px solid rgba(120, 130, 150, 0.24);
        border-radius: 8px;
        background: linear-gradient(135deg, rgba(38, 70, 105, 0.18), rgba(42, 48, 58, 0.08));
        margin-bottom: 1rem;
    }
    .rf-title {
        font-size: 2.1rem;
        font-weight: 760;
        line-height: 1.15;
        margin: 0 0 0.35rem 0;
    }
    .rf-subtitle {
        font-size: 1.02rem;
        color: rgba(240, 242, 246, 0.82);
        margin: 0 0 0.9rem 0;
    }
    .rf-chip {
        display: inline-block;
        padding: 0.22rem 0.55rem;
        margin: 0 0.24rem 0.24rem 0;
        border: 1px solid rgba(120, 130, 150, 0.3);
        border-radius: 999px;
        font-size: 0.82rem;
        color: rgba(240, 242, 246, 0.9);
        background: rgba(90, 110, 140, 0.14);
    }
    .rf-note {
        color: rgba(240, 242, 246, 0.72);
        font-size: 0.93rem;
        margin-bottom: 0.6rem;
    }
    .rf-paper-meta {
        color: rgba(240, 242, 246, 0.74);
        font-size: 0.9rem;
        line-height: 1.55;
        margin-bottom: 0.45rem;
    }
    .rf-inline-label {
        color: rgba(240, 242, 246, 0.7);
        font-size: 0.86rem;
        margin-bottom: 0.15rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def _enabled_text(value: bool) -> str:
    return "已启用" if value else "未启用"


def _format_score(value: Any) -> str:
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return "0.00"


def _format_breakdown(breakdown: dict | None) -> str:
    if not isinstance(breakdown, dict) or not breakdown:
        return "暂无评分构成"

    return "\n".join(f"- `{key}`: {value}" for key, value in breakdown.items())


def _display_header() -> None:
    st.markdown(
        """
        <div class="rf-hero">
            <div class="rf-title">ResearchFlow-Agent</div>
            <p class="rf-subtitle">面向研究生的自动化文献调研与报告生成智能体</p>
            <span class="rf-chip">Streamlit</span>
            <span class="rf-chip">LangGraph</span>
            <span class="rf-chip">DeepSeek API</span>
            <span class="rf-chip">OpenAlex</span>
            <span class="rf-chip">arXiv</span>
            <span class="rf-chip">Benchmark</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="rf-note">输入一个研究主题，系统会检索候选论文、筛选代表性文献、生成中文结构化总结，并输出 Markdown 文献调研报告。</p>',
        unsafe_allow_html=True,
    )


def _display_sidebar() -> None:
    with st.sidebar:
        st.header("运行配置")
        st.caption(f"当前版本：{APP_VERSION} Demo")
        st.metric("Agent Workflow", "LangGraph")
        st.write(f"LLM Provider：`{LLM_PROVIDER}`")
        st.write(f"LLM_DRY_RUN：`{str(LLM_DRY_RUN).lower()}`")
        st.write(f"Demo fallback：`{_enabled_text(USE_DEMO_FALLBACK)}`")

        st.divider()
        st.subheader("项目状态")
        st.write("论文检索：OpenAlex / arXiv")
        st.write("论文筛选：可解释规则评分")
        st.write("报告输出：latest_report.md / reports/")

        st.divider()
        st.subheader("使用说明")
        st.markdown(
            """
            1. 输入研究主题。
            2. 设置检索数量和筛选数量。
            3. 点击开始调研。
            4. 在结果区查看论文、日志、评估和报告。
            """
        )

        st.info("不要在页面、代码或截图中输入 API Key。真实密钥只应放在本地 `.env` 文件。")
        if LLM_DRY_RUN:
            st.warning("当前为 dry-run，不会真实调用 DeepSeek。")
        else:
            st.success("当前允许真实 DeepSeek 调用；失败时会自动回退到 mock。")


def _display_run_metrics(result: dict) -> None:
    candidate_papers = result.get("candidate_papers", []) or []
    selected_papers = result.get("selected_papers", []) or []
    evaluation = result.get("evaluation", {}) or {}
    cache_info = result.get("cache_info", {}) or {}

    metric_cols = st.columns(6)
    metric_cols[0].metric("候选论文", len(candidate_papers))
    metric_cols[1].metric("代表性论文", len(selected_papers))
    metric_cols[2].metric("评估状态", evaluation.get("status", "unknown"))
    metric_cols[3].metric("实际 LLM", evaluation.get("llm_provider", "unknown"))
    metric_cols[4].metric("Keyword Hit Rate", evaluation.get("keyword_hit_rate", 0))
    metric_cols[5].metric("Avg Score", evaluation.get("avg_relevance_score", 0))

    cache_cols = st.columns(3)
    cache_cols[0].metric("Search Cache", "hit" if cache_info.get("search_cache_hit") else "miss")
    cache_cols[1].metric("Summary Cache Hit", cache_info.get("summary_cache_hits", 0))
    cache_cols[2].metric("Summary Cache Miss", cache_info.get("summary_cache_misses", 0))


def _display_paper_card(paper: dict, index: int) -> None:
    title = paper.get("title") or f"论文 {index}"
    year = paper.get("year") or "N/A"
    source = paper.get("source") or "N/A"
    venue = paper.get("venue") or "N/A"
    authors = paper.get("authors") or "N/A"
    url = paper.get("url") or ""
    score = paper.get("relevance_score", 0)
    score_reason = paper.get("score_reason") or "暂无评分解释"
    breakdown = paper.get("score_breakdown", {})

    with st.expander(f"{index}. {title}", expanded=index <= 2):
        score_cols = st.columns([1, 1, 1, 1])
        score_cols[0].metric("相关性评分", _format_score(score))
        score_cols[1].metric("年份", year)
        score_cols[2].metric("来源", source)
        score_cols[3].metric("引用量", paper.get("citationCount", 0))

        st.markdown(
            f"""
            <div class="rf-paper-meta">
            作者：{authors}<br>
            发表 venue：{venue}
            </div>
            """,
            unsafe_allow_html=True,
        )

        left, right = st.columns([1, 1])
        with left:
            st.markdown("**评分构成**")
            st.markdown(_format_breakdown(breakdown))
        with right:
            st.markdown("**筛选理由**")
            st.write(score_reason)

        if url:
            st.link_button("打开论文链接", url)


def _display_report_paths(result: dict) -> None:
    report_path = result.get("report_path", "") or ""
    archive_report_path = result.get("archive_report_path", "") or ""
    if not report_path and not archive_report_path:
        return

    st.markdown("**报告输出路径**")
    path_cols = st.columns([1, 1])
    if report_path:
        with path_cols[0]:
            st.markdown('<div class="rf-inline-label">最近报告</div>', unsafe_allow_html=True)
            st.code(report_path, language="text")
    if archive_report_path:
        with path_cols[1]:
            st.markdown('<div class="rf-inline-label">归档报告</div>', unsafe_allow_html=True)
            st.code(archive_report_path, language="text")


def _display_history() -> None:
    recent_history = load_recent_history(limit=10)
    if recent_history:
        st.dataframe(recent_history, use_container_width=True, hide_index=True)
    else:
        st.caption("暂无历史记录。运行一次调研后会自动生成。")


def _display_empty_state() -> None:
    overview_cols = st.columns(3)
    overview_cols[0].info("支持 OpenAlex / arXiv 学术检索，并保留 demo fallback。")
    overview_cols[1].info("支持 DeepSeek API、dry-run 和 mock fallback，便于课堂演示。")
    overview_cols[2].info("支持 benchmark evaluation、缓存和历史记录。")

    st.subheader("最近任务历史")
    _display_history()


if "last_result" not in st.session_state:
    st.session_state.last_result = None


_display_sidebar()
_display_header()

with st.form("research_form"):
    st.subheader("输入研究主题")
    topic = st.text_input("研究主题", value="Agentic RAG", placeholder="例如：Agentic RAG")
    col1, col2 = st.columns(2)
    with col1:
        limit = st.number_input("检索论文数量 limit", min_value=1, max_value=50, value=10, step=1)
    with col2:
        top_k = st.number_input("筛选论文数量 top_k", min_value=1, max_value=20, value=5, step=1)

    submitted = st.form_submit_button("开始调研", type="primary", use_container_width=True)

if submitted:
    normalized_topic = topic.strip() or "Agentic RAG"
    if not topic.strip():
        st.info("研究主题为空，已使用默认主题 Agentic RAG。")

    with st.status("LangGraph Agent 正在执行调研工作流...", expanded=True) as status:
        st.write("Planner -> Search -> Filter -> Summary -> Report -> Evaluator")
        result = run_research(normalized_topic, limit=int(limit), top_k=int(top_k))
        st.session_state.last_result = result
        status.update(label="调研报告已生成", state="complete")


result = st.session_state.last_result

if result:
    evaluation = result.get("evaluation", {}) or {}
    selected_papers = result.get("selected_papers", []) or []
    logs = result.get("logs", []) or []
    errors = result.get("errors", []) or []
    report = result.get("report", "") or ""

    st.success("调研完成。下面展示本次 Agent 工作流结果。")
    _display_run_metrics(result)

    tab_papers, tab_report, tab_logs, tab_history = st.tabs(
        ["论文结果", "Markdown 报告", "执行日志与评估", "历史记录"]
    )

    with tab_papers:
        st.subheader("筛选后的代表性论文")
        if selected_papers:
            for idx, paper in enumerate(selected_papers, start=1):
                _display_paper_card(paper, idx)
        else:
            st.warning("本次没有筛选出论文。可以尝试扩大 limit 或换一个研究主题。")

    with tab_report:
        _display_report_paths(result)
        st.subheader("生成的 Markdown 报告")
        st.markdown(report or "暂无报告内容。")
        st.download_button(
            label="下载报告",
            data=report,
            file_name="latest_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with tab_logs:
        log_col, eval_col = st.columns([1, 1])
        with log_col:
            st.subheader("执行日志")
            if logs:
                for log in logs:
                    st.write(f"- {log}")
            else:
                st.caption("暂无执行日志。")

            if errors:
                st.warning("工作流执行过程中出现可恢复问题：")
                for error in errors:
                    st.write(f"- {error}")

        with eval_col:
            st.subheader("Evaluation JSON")
            if evaluation:
                st.json(evaluation)
            else:
                st.caption("暂无评估结果。")

    with tab_history:
        st.subheader("最近任务历史")
        _display_history()
else:
    _display_empty_state()

st.divider()
st.caption(
    f"当前为 {APP_VERSION} Demo；使用 OpenAlex / arXiv 检索论文，使用 LangGraph 编排多步骤 Agent 工作流，使用 DeepSeek API 或 mock 模式生成总结。"
)
