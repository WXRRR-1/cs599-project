# ResearchFlow-Agent

## 项目简介

ResearchFlow-Agent 是一个面向研究生的自动化文献调研与报告生成智能体。用户输入研究主题后，系统会检索相关论文、筛选代表性论文、生成中文结构化总结，并输出 Markdown 文献调研报告。

## 课程方向

方向一：Agentic AI 原生开发

## 当前版本

v0.2 LangGraph Agent Workflow Demo

## 已实现功能

- 输入研究主题并启动自动化调研流程
- 优先调用 OpenAlex API 检索相关论文
- OpenAlex 不可用时自动切换到 arXiv API
- 获取论文标题、作者、年份、摘要、引用量、链接和 venue
- 按引用量和年份筛选代表性论文
- 使用 DeepSeek API 或 Mock Mode 生成中文结构化总结
- 生成 Markdown 格式文献调研报告
- 使用 Streamlit 展示结果并支持下载
- 将报告保存到 `src/outputs/sample_report.md`
- 使用 `src/check_apis.py` 检查学术 API 连通性
- 使用 LangGraph 编排 Planner、Search、Filter、Summary、Report、Evaluator 节点
- 在 Streamlit 页面展示 Agent 执行日志和评估结果

## v0.2 更新

- 引入 LangGraph 工作流
- 增加 `ResearchState` 状态对象
- 将调研任务拆分为 Planner、Search、Filter、Summary、Report、Evaluator 节点
- 使用 DeepSeek API 作为主 LLM
- 保留 mock fallback，保证无 API Key 时可演示
- 在 Streamlit 页面展示 Agent 执行日志和评估结果

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
│       └── sample_report.md
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
DEEPSEEK_API_KEY=你的 DeepSeek API Key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

本项目使用 `openai` Python SDK 的 OpenAI-compatible 写法调用 DeepSeek API。`openai` 只是兼容 SDK，不表示本项目把 OpenAI API 作为主 LLM 方案。

如果没有配置 DeepSeek API Key，保持默认配置即可：

```env
LLM_PROVIDER=mock
```

mock 模式不需要任何 LLM API Key，也可以跑通完整 Demo。

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
src/outputs/sample_report.md
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

## 项目状态

- [x] Proposal
- [x] v0.1 Demo
- [x] v0.2 LangGraph Workflow
- [ ] MVP
- [ ] Final

## 安全说明

- 不得硬编码 API Key
- `.env` 文件不得上传 GitHub
- `.env.example` 只保留环境变量名称和示例配置
- 程序日志不得输出真实 API Key
- 本项目默认使用 mock 模式，避免没有 LLM API Key 时无法运行

## References

- OpenAlex API: https://docs.openalex.org/
- arXiv API: https://info.arxiv.org/help/api/
- DeepSeek API: https://api-docs.deepseek.com/
- Streamlit: https://streamlit.io/
- OpenAI-compatible Python SDK: https://github.com/openai/openai-python
