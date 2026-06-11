"""Markdown report generation agent."""

from __future__ import annotations

from pathlib import Path

from config import PROJECT_ROOT


def _md_escape_table(text: str) -> str:
    return str(text or "").replace("|", "\\|").replace("\n", " ")


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

        paper_lines.append(f"{index}. **{title}**（{year}）- {authors}")
        detail_sections.append(
            f"""### 论文 {index}：{title}

- 年份：{year}
- 作者：{authors}
- 研究背景：{summary.get("background", "摘要中未明确说明")}
- 研究问题：{summary.get("problem", "摘要中未明确说明")}
- 核心方法：{summary.get("method", "摘要中未明确说明")}
- 主要贡献：{summary.get("contribution", "摘要中未明确说明")}
- 局限性：{summary.get("limitation", "摘要中未明确说明")}
- 链接：{url or "N/A"}
"""
        )
        table_rows.append(
            "| {title} | {year} | {method} | {contribution} | {limitation} |".format(
                title=_md_escape_table(title),
                year=_md_escape_table(year),
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

系统优先使用 OpenAlex API 检索相关论文，失败后切换到 arXiv API，并过滤掉缺少标题或摘要的结果。当前 v0.1 Demo 使用简单规则进行筛选：优先选择引用量较高、年份较新的论文。随后基于论文标题和摘要生成中文结构化总结。

## 3. 代表性论文列表

{chr(10).join(paper_lines)}

## 4. 单篇论文结构化总结

{chr(10).join(detail_sections) if summaries else "暂无结构化总结。"}

## 5. 文献对比表

| 论文 | 年份 | 核心方法 | 主要贡献 | 局限性 |
|---|---:|---|---|---|
{chr(10).join(table_rows) if summaries else "| 暂无 | N/A | N/A | N/A | N/A |"}

## 6. 初步结论

从当前检索结果看，**{topic}** 相关研究通常围绕任务建模、系统架构、方法评估与实际应用展开。v0.1 Demo 的结论仅基于标题和摘要，适合作为课程展示中的初步文献调研材料；后续版本可进一步加入多步骤 Agent 工作流、交叉验证与全文级分析。

## 7. 参考文献

{chr(10).join(reference_lines) if summaries else "暂无参考文献。"}
"""
    return report


def save_report(report: str, output_path: str = "src/outputs/sample_report.md") -> None:
    """Save the Markdown report to disk."""
    path = Path(output_path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")
