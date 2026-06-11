# ResearchFlow-Agent 项目 Proposal

## 1. 项目背景

研究生在进行文献调研时，需要面对大量英文论文，存在检索成本高、筛选困难、总结效率低、报告结构不清晰等问题。

## 2. 项目目标

构建一个自动化文献调研与报告生成智能体，实现从研究主题输入到文献调研报告输出的最小闭环。

## 3. 核心功能

- 根据研究主题检索 OpenAlex 和 arXiv 论文数据
- 获取论文标题、作者、年份、摘要、引用量、链接和会议或期刊信息
- 使用简单规则筛选 3-5 篇代表性论文
- 基于标题和摘要生成中文结构化总结
- 输出 Markdown 格式文献调研报告
- 在 Streamlit 页面中展示结果并支持下载

## 4. 技术路线

项目采用 Python 3.10+ 开发，使用 requests 调用 OpenAlex API，并使用 Python 标准库 urllib 调用 arXiv API；使用 python-dotenv 管理环境变量，使用 OpenAI-compatible SDK 调用 DeepSeek API，并使用 Streamlit 构建轻量交互页面。默认使用 mock 模式，保证未配置 DeepSeek API Key 时仍可完成完整 Demo 流程。

## 5. v0.1 Demo 范围

v0.1 版本只实现最小可运行闭环：主题输入、论文检索、规则筛选、摘要总结、报告生成和页面展示。不包含 Docker、数据库、PDF 全文解析、向量数据库、RAG 管线或 LangGraph 工作流。

## 6. 后续计划

- 将检索、筛选、总结、报告生成拆分为 LangGraph 节点
- 增加多轮反思和结果校验步骤
- 支持更多论文数据源和全文 PDF 解析
- 引入引用关系分析和主题聚类
- 改进报告质量评估与人工编辑流程
