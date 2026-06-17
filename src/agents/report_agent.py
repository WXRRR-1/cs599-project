"""Markdown report generation agent."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re

from config import PROJECT_ROOT


def _md_escape_table(text: str) -> str:
    return str(text or "").replace("|", "\\|").replace("\n", " ")


def _format_score_breakdown(summary: dict) -> str:
    breakdown = summary.get("score_breakdown") or {}
    if not isinstance(breakdown, dict) or not breakdown:
        return "- 评分构成：暂无评分信息"

    return "\n".join(
        [
            "- 评分构成（score_breakdown）：",
            f"  - keyword_score: {breakdown.get('keyword_score', 'N/A')}",
            f"  - year_score: {breakdown.get('year_score', 'N/A')}",
            f"  - citation_score: {breakdown.get('citation_score', 'N/A')}",
        ]
    )


def generate_report(topic: str, summaries: list[dict]) -> str:
    """Generate a Chinese Markdown literature review report."""
    paper_lines = []
    detail_sections = []
    table_rows = []
    reference_lines = []

    for index, summary in enumerate(summaries, start=1):
        title = summary.get("title", "未知论文")
        year = summary.get("year", "N/A")
        authors = summary.get("authors", "N/A")
        url = summary.get("url", "")
        source = summary.get("source", "暂无来源信息")
        relevance_score = summary.get("relevance_score", "暂无评分信息")
        score_reason = summary.get("score_reason", "暂无评分解释")

        paper_lines.append(
            f"{index}. **{title}**（{year}）- {authors}；来源：{source}；相关性评分：{relevance_score}"
        )
        detail_sections.append(
            f"""### 论文 {index}：{title}

- 年份：{year}
- 作者：{authors}
- 来源：{source}
- 相关性评分（relevance_score）：{relevance_score}
{_format_score_breakdown(summary)}
- 筛选理由（score_reason）：{score_reason}
- 研究背景：{summary.get("background", "摘要中未明确说明")}
- 研究问题：{summary.get("problem", "摘要中未明确说明")}
- 核心方法：{summary.get("method", "摘要中未明确说明")}
- 主要贡献：{summary.get("contribution", "摘要中未明确说明")}
- 局限性：{summary.get("limitation", "摘要中未明确说明")}
- 链接：{url or "N/A"}
"""
        )
        table_rows.append(
            "| {title} | {year} | {source} | {score} | {method} | {contribution} | {limitation} |".format(
                title=_md_escape_table(title),
                year=_md_escape_table(year),
                source=_md_escape_table(source),
                score=_md_escape_table(relevance_score),
                method=_md_escape_table(summary.get("method", "")),
                contribution=_md_escape_table(summary.get("contribution", "")),
                limitation=_md_escape_table(summary.get("limitation", "")),
            )
        )
        reference_lines.append(f"{index}. {authors}. {title}. {year}. {url or 'N/A'}")

    if not summaries:
        paper_lines.append("暂无可用论文。请检查网络连接、检索主题或 OpenAlex API 状态。")

    report = f"""# 文献调研报告：{topic}

## 1. 研究主题

本报告围绕 **{topic}** 进行自动化文献调研，目标是快速了解相关研究方向中的代表性论文、核心方法与初步研究结论。

## 2. 检索与筛选说明

本项目首先根据用户输入的研究主题调用 OpenAlex / arXiv 等学术检索工具获取候选论文，失败时可使用内置示例论文保持 Demo 可运行。系统会过滤掉缺少标题或摘要的结果，然后使用轻量级规则评分方法筛选代表性论文。

论文筛选评分公式如下：

```text
relevance_score = keyword_score + year_score + citation_score
```

其中：

- `keyword_score`：根据研究主题关键词在论文标题和摘要中的命中情况计算；
- `year_score`：根据论文发表年份的新近程度计算；
- `citation_score`：根据论文引用量区间计算。

系统最终按照 `relevance_score` 从高到低排序，并选择排名靠前的论文作为代表性文献。随后基于论文标题和摘要生成中文结构化总结。

## 3. 代表性论文列表

{chr(10).join(paper_lines)}

## 4. 单篇论文结构化总结

{chr(10).join(detail_sections) if summaries else "暂无结构化总结。"}

## 5. 文献对比表

| 论文 | 年份 | 来源 | 相关性评分 | 核心方法 | 主要贡献 | 局限性 |
|---|---:|---|---:|---|---|---|
{chr(10).join(table_rows) if summaries else "| 暂无 | N/A | N/A | N/A | N/A | N/A | N/A |"}

## 6. 初步结论

从当前检索结果看，**{topic}** 相关研究通常围绕任务建模、系统架构、方法评估与实际应用展开。当前版本的结论仅基于标题和摘要，适合作为课程展示中的初步文献调研材料；后续版本可进一步加入多步骤 Agent 工作流、交叉验证与全文级分析。

## 7. 参考文献

{chr(10).join(reference_lines) if summaries else "暂无参考文献。"}
"""
    return report


def save_report(report: str, output_path: str = "src/outputs/latest_report.md") -> None:
    """Save the Markdown report to disk."""
    path = Path(output_path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")


def _safe_report_filename(topic: str) -> str:
    """Convert a research topic into a Windows-safe, compact filename stem."""
    normalized = re.sub(r"\s+", "_", (topic or "research_report").strip())
    normalized = re.sub(r'[<>:"/\\|?*]+', "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("._")
    return (normalized or "research_report")[:80]


def save_runtime_reports(
    report: str,
    topic: str,
    latest_path: str = "src/outputs/latest_report.md",
    archive_dir: str = "src/outputs/reports",
) -> dict[str, str]:
    """Save the latest report and an archived copy without touching sample_report.md."""
    save_report(report, latest_path)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"{_safe_report_filename(topic)}_{timestamp}.md"
    archive_path = str(Path(archive_dir) / archive_name).replace("\\", "/")
    save_report(report, archive_path)

    return {
        "report_path": latest_path,
        "archive_report_path": archive_path,
    }
