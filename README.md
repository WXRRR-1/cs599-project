# ResearchFlow-Agent

## 项目简介

ResearchFlow-Agent 是一个面向研究生的自动化文献调研与报告生成智能体。用户输入研究主题后，系统会检索相关论文、筛选代表性论文、生成中文结构化总结，并输出 Markdown 文献调研报告。

## 课程方向

方向一：Agentic AI 原生开发

## 当前版本

v0.1 Demo

## 核心功能

- 调用 OpenAlex API 检索相关论文
- OpenAlex 不可用时自动切换到 arXiv API
- 获取论文标题、作者、年份、摘要、引用量、链接和 venue
- 按引用量和年份筛选代表性论文
- 支持 OpenAI、DeepSeek 和 Mock Mode 生成中文总结
- 生成 Markdown 格式文献调研报告
- 使用 Streamlit 展示结果并支持下载
- 将报告保存到 `src/outputs/sample_report.md`

## 技术栈

- AI Development Tool: OpenAI Codex
- Language: Python
- UI: Streamlit
- Paper Search: OpenAlex API
- Fallback Search: arXiv API
- LLM: OpenAI / DeepSeek / Mock Mode
- Report Format: Markdown

## 项目结构

```text
cs599-project/
├── docs/
│   └── proposal.md
├── src/
│   ├── app.py
│   ├── main.py
│   ├── config.py
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

## 环境变量配置

复制 `.env.example` 为 `.env`，再按需填写 API Key。

```bash
copy .env.example .env
```

默认配置为：

```env
LLM_PROVIDER=mock
```

mock 模式不需要配置任何 LLM API Key，也可以跑通完整 Demo。

如果所有外部学术 API 都被限流或暂时没有结果，项目默认会启用内置示例论文，保证页面中可以看到完整报告效果：

```env
USE_DEMO_FALLBACK=true
```

可选配置：

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

或：

```env
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

学术检索 API 配置：

```env
OPENALEX_API_KEY=
OPENALEX_BASE_URL=https://api.openalex.org/works
ARXIV_BASE_URL=http://export.arxiv.org/api/query
```

如果 Python 不能直接访问外部 API，但浏览器可以访问，通常是代理或防火墙问题。可以在 `.env` 中配置代理：

```env
NETWORK_PROXY=http://127.0.0.1:7890
```

检查学术 API 的连通性：

```bash
python src/check_apis.py
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

## 项目状态

- [x] Proposal
- [ ] MVP
- [ ] Final

## 注意事项

- 不得硬编码 API Key
- `.env` 文件不要上传到 GitHub
- 当前版本只基于论文标题和摘要生成总结，不代表完整论文精读结论
- 如果外部学术 API 请求失败，系统会回退到内置示例论文，保证 Demo 页面可展示
