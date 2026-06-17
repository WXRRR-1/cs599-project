# ResearchFlow-Agent

## 项目简介

ResearchFlow-Agent 是一个面向研究生的自动化文献调研与报告生成智能体。用户输入研究主题后，系统会检索相关论文、筛选代表性论文、生成中文结构化总结，并输出 Markdown 文献调研报告。

## 课程方向

方向一：Agentic AI 原生开发

## 当前版本

v0.3.4 Output Report Separation

## 已实现功能

- 输入研究主题并启动自动化调研流程
- 优先调用 OpenAlex API 检索相关论文
- OpenAlex 不可用时自动切换到 arXiv API
- 获取论文标题、作者、年份、摘要、引用量、链接和 venue
- 使用关键词、年份、引用量的可解释评分筛选代表性论文
- 使用 DeepSeek API 或 Mock Mode 生成中文结构化总结
- 生成 Markdown 格式文献调研报告
- 使用 Streamlit 展示结果并支持下载
- 将最近一次运行报告保存到 `src/outputs/latest_report.md`
- 使用 `src/check_apis.py` 检查学术 API 连通性
- 使用 LangGraph 编排 Planner、Search、Filter、Summary、Report、Evaluator 节点
- 在 Streamlit 页面展示 Agent 执行日志和评估结果
- 区分配置的 LLM Provider 与实际使用的 LLM Provider
- DeepSeek 调用失败时自动回退到 mock 总结
- 默认启用 `LLM_DRY_RUN=true`，避免开发阶段误调用 DeepSeek 产生费用
- 使用本地 JSON 缓存减少重复 OpenAlex / arXiv 检索和重复论文总结
- 运行时可记录最近调研任务历史到 `src/outputs/history.jsonl`
- 运行 benchmark 主题并生成 `src/outputs/eval_results.md`

## v0.2 更新

- 引入 LangGraph 工作流
- 增加 `ResearchState` 状态对象
- 将调研任务拆分为 Planner、Search、Filter、Summary、Report、Evaluator 节点
- 使用 DeepSeek API 作为主 LLM
- 保留 mock fallback，保证无 API Key 时可演示
- 在 Streamlit 页面展示 Agent 执行日志和评估结果

## v0.3 更新

- 增加 `get_active_llm_provider()`，展示 DeepSeek / mock / DeepSeek 失败后 mock 兜底的真实状态
- 增加轻量 benchmark 评估脚本 `src/evaluation/run_evaluation.py`
- 增加轻量任务历史模块 `src/memory/history_store.py`
- Streamlit 页面展示实际 LLM、demo fallback 状态、评估结果、执行日志和最近任务历史
- 改进空主题、top_k 大于候选数量、API 失败和报告保存失败等边界情况的可恢复性

## v0.3.1 更新

- 增加 DeepSeek 成本保护：dry-run、最大总结论文数、摘要截断、超时和重试限制
- 增加 search cache 与 summary cache，减少重复 API 调用
- 增强论文筛选可信度，输出 `relevance_score`、`score_breakdown`、`score_reason`

## v0.3.2 更新

- 同步文献调研报告中的筛选评分说明
- 在 `sample_report.md` 中展示 `relevance_score`、`score_breakdown`、`score_reason`
- 更新文献对比表，增加来源和相关性评分字段

## v0.3.3 更新

- 同步 README 和 Streamlit 页面版本标签
- 将 `history.jsonl` 作为本地运行历史文件处理，默认不提交到 GitHub
- 保持 `sample_report.md` 作为课程展示样例

## v0.3.4 更新

- `src/outputs/sample_report.md` 作为人工确认过的稳定展示样例
- `src/outputs/latest_report.md` 作为最近一次运行自动生成的报告
- `src/outputs/reports/` 作为可选历史归档目录
- 普通运行和 benchmark 不再覆盖 `sample_report.md`

## 技术栈

- AI Development Tool: OpenAI Codex
- Language: Python
- UI: Streamlit
- Agent Workflow: LangGraph
- Paper Search: OpenAlex API, arXiv API
- LLM: DeepSeek API / Mock Mode
- LLM SDK: OpenAI-compatible SDK
- Report Format: Markdown
- Version Control: GitHub

## 项目结构

```text
cs599-project/
├── docs/
│   └── proposal.md
├── src/
│   ├── app.py
│   ├── main.py
│   ├── config.py
│   ├── check_apis.py
│   ├── cache/
│   │   └── cache_store.py
│   ├── evaluation/
│   │   ├── benchmark_topics.json
│   │   ├── metrics.py
│   │   └── run_evaluation.py
│   ├── memory/
│   │   └── history_store.py
│   ├── workflow/
│   │   ├── research_state.py
│   │   ├── nodes.py
│   │   └── research_graph.py
│   ├── tools/
│   │   ├── openalex_search_tool.py
│   │   ├── arxiv_search_tool.py
│   │   ├── demo_paper_tool.py
│   │   └── http_client.py
│   ├── agents/
│   │   ├── filter_agent.py
│   │   ├── summary_agent.py
│   │   └── report_agent.py
│   └── outputs/
│       ├── sample_report.md
│       ├── latest_report.md        # 运行时生成，默认不提交
│       ├── reports/                # 运行时归档，默认不提交
│       └── eval_results.md
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

## 环境搭建

建议使用 Python 3.10+。

```bash
cd cs599-project
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## DeepSeek API 配置

复制 `.env.example` 为 `.env`：

```bash
copy .env.example .env
```

如果需要使用真实 LLM 总结，在 `.env` 中填写：

```env
LLM_PROVIDER=deepseek
LLM_DRY_RUN=true
MAX_LLM_PAPERS=5
MAX_ABSTRACT_CHARS=2000
LLM_TIMEOUT_SECONDS=30
LLM_MAX_RETRIES=1
DEEPSEEK_API_KEY=你的 DeepSeek API Key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

本项目使用 `openai` Python SDK 的 OpenAI-compatible 写法调用 DeepSeek API。`openai` 只是兼容 SDK，不表示本项目把 OpenAI API 作为主 LLM 方案。

如果没有配置 DeepSeek API Key，保持默认 DeepSeek 主方案配置即可。系统会在缺少 Key 或 DeepSeek 调用失败时自动回退到 mock 总结：

```env
LLM_PROVIDER=deepseek
```

mock fallback 不需要任何 LLM API Key，也可以跑通完整 Demo。也可以显式设置 `LLM_PROVIDER=mock` 进行离线演示。

## DeepSeek 成本保护

默认配置中 `LLM_DRY_RUN=true`，即使 `LLM_PROVIDER=deepseek`，系统也不会真实调用 DeepSeek，而是使用 mock summary 跑通流程。只有在 `LLM_DRY_RUN=false` 且 `DEEPSEEK_API_KEY` 存在时，才会尝试真实调用 DeepSeek。

- `MAX_LLM_PAPERS`：每次最多允许多少篇论文进入真实 LLM 总结
- `MAX_ABSTRACT_CHARS`：发送给 LLM 的摘要最大字符数
- `LLM_TIMEOUT_SECONDS`：DeepSeek 请求超时时间
- `LLM_MAX_RETRIES`：DeepSeek 调用失败后的最大重试次数

程序日志只显示 dry-run、fallback 和错误类型，不输出 API Key 或请求头。

## 学术 API 与网络配置

OpenAlex 和 arXiv 用于论文检索：

```env
OPENALEX_EMAIL=
OPENALEX_BASE_URL=https://api.openalex.org/works
ARXIV_BASE_URL=http://export.arxiv.org/api/query
```

如果 Python 不能直接访问外部 API，但浏览器可以访问，通常是代理或防火墙问题。可以在 `.env` 中配置代理：

```env
NETWORK_PROXY=http://127.0.0.1:7890
```

如果所有外部学术 API 都被限流或暂时没有结果，项目默认会启用内置示例论文，保证页面中可以看到完整报告效果：

```env
USE_DEMO_FALLBACK=true
```

## 运行方式

### 命令行运行

```bash
python src/main.py "Agentic RAG"
```

运行结束后，报告会保存到：

```text
src/outputs/latest_report.md
```

### Streamlit 页面运行

```bash
streamlit run src/app.py
```

在页面中输入研究主题，点击“开始调研”，即可查看并下载 Markdown 报告。

### API 连通性检查

```bash
python src/check_apis.py
```

### Benchmark 评估

```bash
python src/evaluation/run_evaluation.py
```

评估脚本会依次运行 `src/evaluation/benchmark_topics.json` 中的主题，并生成：

```text
src/outputs/eval_results.md
```

## LangGraph 工作流

v0.2 使用 LangGraph 显式管理调研状态，核心流程为：

```text
Planner Node
→ Search Node
→ Filter Node
→ Summary Node
→ Report Node
→ Evaluator Node
→ END
```

状态对象定义在 `src/workflow/research_state.py`，节点实现位于 `src/workflow/nodes.py`，图构建与统一入口位于 `src/workflow/research_graph.py`。

## 评估与历史记录

v0.3 增加了轻量级运行观测能力：

- `src/outputs/sample_report.md`：人工确认过的稳定展示样例，普通运行不会自动覆盖
- `src/outputs/latest_report.md`：最近一次生成的 Markdown 文献调研报告，默认不提交到 GitHub
- `src/outputs/reports/`：每次运行的历史归档报告目录，默认不提交到 GitHub
- `src/outputs/eval_results.md`：benchmark 批量评估结果
- `src/outputs/history.jsonl`：最近调研任务历史，每行记录一个任务

`history.jsonl` 只记录主题、候选论文数、筛选论文数、实际 LLM Provider、评估状态、报告路径和错误类型，不记录 API Key。该文件属于本地运行历史，默认不提交到 GitHub。

## 缓存与筛选评分

v0.3.1 起使用本地 JSON 文件减少重复调用。缓存文件在运行时自动生成，默认不提交到 GitHub：

- `src/outputs/cache/search_cache.json`：缓存 OpenAlex / arXiv 检索结果
- `src/outputs/cache/summary_cache.json`：缓存论文结构化总结

缓存 key 基于 topic、limit、source、论文标题、链接和年份等非敏感信息生成，不保存 API Key。

论文筛选使用可解释评分公式：

```text
relevance_score = 关键词匹配分 + 年份分 + 引用量分
```

筛选后的论文会包含：

- `relevance_score`：综合相关性分数
- `score_breakdown`：关键词、年份、引用量三部分分数
- `score_reason`：自然语言评分原因

这些字段会在 Streamlit 的筛选后论文表格中展示。

## 项目状态

- [x] Proposal
- [x] v0.1 Demo
- [x] v0.2 LangGraph Workflow
- [x] v0.3 Project Hardening
- [ ] MVP
- [ ] Final

## 当前尚未实现

- MCP 协议接入
- OpenAI / DeepSeek Function Calling
- 向量数据库或长期语义记忆
- 论文 PDF 全文 RAG
- Docker 或云部署

## 安全说明

- 不得硬编码 API Key
- `.env` 文件不得上传 GitHub
- `.env.example` 只保留环境变量名称和示例配置
- 程序日志不得输出真实 API Key
- 本项目默认以 DeepSeek API 为主方案，缺少 API Key 或调用失败时自动回退到 mock

## References

- OpenAlex API: https://docs.openalex.org/
- arXiv API: https://info.arxiv.org/help/api/
- DeepSeek API: https://api-docs.deepseek.com/
- Streamlit: https://streamlit.io/
- OpenAI-compatible Python SDK: https://github.com/openai/openai-python
