# ResearchFlow-Agent 期末大作业评分验证报告

生成日期：2026-06-21  
审查范围：当前本地仓库 `WXRRR-1/cs599-project`，不读取 `.env`，不修改业务代码。

## 1. 项目基本信息

* 项目名称：ResearchFlow-Agent
* 课程方向：方向一：Agentic AI 原生开发
* 当前版本：v0.3.7 Academic Filtering Polish
* GitHub 仓库：`WXRRR-1/cs599-project`
* 仓库可见性：Public
* 默认分支：`main`
* 技术栈：Python、Streamlit、LangGraph、DeepSeek API / Mock fallback、OpenAlex、arXiv

仓库结构检查结果：

* 已包含 `README.md`、`requirements.txt`、`.env.example`、`.gitignore`、`docs/`、`src/`。
* `src/` 中包含 Streamlit 页面、命令行入口、工具层、Agent 层、LangGraph workflow、evaluation、memory、cache 等模块。
* `docs/` 当前仅包含 `proposal.md` 和本报告 `final_score_audit.md`。
* 缺少最终报告 PDF，例如 `docs/CS599_大作业报告.pdf`。
* 缺少独立架构文档，例如 `docs/architecture.md`。
* 缺少 `LICENSE` 文件。

运行环境检查结果：

* Python 版本：Python 3.12.7
* `pip install -r requirements.txt`：通过，依赖均已满足。
* 命令行 Demo：通过。
* Benchmark：通过。
* Streamlit：可正常启动。

## 2. 最终估分总览

| 评分项 | 满分 | 自评分 | 证据 | 扣分原因 | 补救建议 |
|---|---:|---:|---|---|---|
| 选题与设计思想 | 20 | 18 | README 和 proposal 明确面向研究生文献调研，符合 Agentic AI 方向 | 选题论证主要在 README/proposal，缺少最终报告中的系统性展开 | 在最终 PDF 中补充痛点、目标用户、价值、与 Agentic AI 的关系 |
| Specs 规格设计 | 20 | 10 | 有 `.env.example`、README 运行说明、proposal、模块接口较清晰 | 缺少正式 `product_spec.md`、`api_spec.md`、`evaluation.md` 或等价规格文档 | 快速补 `docs/product_spec.md`、`docs/api_spec.md`、`docs/evaluation.md` |
| 系统架构与设计 | 15 | 13 | 已使用 LangGraph，包含 Planner/Search/Filter/Summary/Report/Evaluator 节点和 ResearchState | 缺少独立架构图、架构说明文档 | 补 `docs/architecture.md`，包含流程图、状态字段、模块关系 |
| 关键实现与代码 | 15 | 14 | OpenAlex/arXiv 工具调用、DeepSeek/mock fallback、可解释筛选评分、报告生成、Streamlit 展示均已实现 | 仍是课程 Demo 级实现，非企业级部署；没有完整异常分层和测试框架 | 在报告中强调 v0.3.7 Demo 范围，说明后续工程化计划 |
| 测试与评估 | 10 | 8 | 有 benchmark topics、`run_evaluation.py`、`eval_results.md`、keyword_hit_rate、avg_relevance_score | 缺少单元测试、自动化 CI、截图证据 | 增加 Demo 截图和一页 benchmark 结果说明 |
| 升级扩展设想 | 10 | 8 | README 已列出 MCP、Function Calling、向量数据库、PDF RAG 等未实现方向 | 缺少最终报告中的路线图、优先级、风险说明 | 在最终 PDF 中补系统升级路线图 |
| 课程总结 | 10 | 3 | README 有项目状态和安全说明 | 缺少个人课程总结、开发反思、AI 工具使用反思 | 最终 PDF 必须补“课程总结”章节 |
| 加分项 | +10 | +6 | 使用 LangGraph、DeepSeek-compatible SDK、benchmark、history、cache、可解释评分、Git tags | 未实现 MCP、Function Calling、向量数据库、云部署、CI | 不建议临时大改；用文档说明加分点和未实现边界 |

当前保守估分：80 / 100 左右。  
当前乐观估分：86 / 100 左右。  
若补齐最终 PDF、architecture.md、Specs 文档和 LICENSE，预计可提升到 88-93 分区间。

## 3. 课程核心技术要素覆盖情况

| 技术要素 | 是否覆盖 | 项目证据 | 风险 |
|---|---|---|---|
| SDD 规格驱动开发 | 部分覆盖 | `docs/proposal.md`、README、`.env.example`、模块化接口 | 缺少完整 specs 文档，最终报告中需要补足 |
| Tool Use / API 调用 | 已覆盖 | OpenAlex、arXiv、DeepSeek-compatible API、Streamlit UI | 外部 API 网络不稳定时依赖 demo fallback |
| LangGraph 状态管理与多步骤推理 | 已覆盖 | `src/workflow/research_graph.py`、`nodes.py`、`research_state.py` | 需要在最终报告中画图说明 |
| 多 Agent / 多节点协作 | 部分覆盖 | Planner、Search、Filter、Summary、Report、Evaluator 节点分工明确 | 更准确表述应为“多节点 Agent 工作流”，不是完整多智能体系统 |
| 记忆机制 | 部分覆盖 | `src/memory/history_store.py` 记录轻量任务历史 | 不是向量记忆、不是长期语义记忆，报告中不要夸大 |
| 可观测性与评估 | 已覆盖 | logs、benchmark、`eval_results.md`、keyword_hit_rate、avg_relevance_score | 缺少 CI 和单元测试 |
| DeepSeek API / Mock fallback | 已覆盖 | `summary_agent.py` 支持 DeepSeek、dry-run、失败回退 mock | 提交时必须确认 `.env` 不被上传 |
| Streamlit 交互页面 | 已覆盖 | `src/app.py` 支持主题输入、结果展示、下载报告、日志和评估展示 | 需要最终报告或 README 中加入页面截图更稳 |

## 4. GitHub 最终提交检查

| 检查项 | 状态 | 说明 |
|---|---|---|
| 仓库名 | 通过 | GitHub 远程为 `WXRRR-1/cs599-project` |
| Public 仓库 | 通过 | GitHub 元信息显示 visibility 为 public |
| README.md | 基本通过 | 内容完整，包含简介、技术栈、运行方式、版本记录、安全说明 |
| docs/ | 部分通过 | 有 `proposal.md`，本次新增 `final_score_audit.md` |
| 最终报告 PDF | 未通过 | 未发现 `docs/CS599_大作业报告.pdf` |
| architecture.md 或等价架构说明 | 未通过 | README 有 LangGraph 流程说明，但缺少独立架构文档 |
| .gitignore | 通过 | 已忽略 `.env`、`.venv/`、缓存、运行历史、latest_report、reports |
| LICENSE | 未通过 | 未发现 LICENSE 文件；Public 仓库建议添加 |
| requirements.txt | 通过 | 包含 streamlit、requests、python-dotenv、openai、langgraph |
| .env 是否被排除 | 通过 | `git ls-files .env` 无输出，`.env` 未被跟踪 |
| .env.example 是否安全 | 通过 | 仅包含空 key 和示例配置，未发现真实 DeepSeek Key |
| tag / version | 基本通过 | 当前版本为 v0.3.7，本地已有 `v0.3.7` tag |

## 5. 运行验证结果

| 命令 | 结果 | 关键输出 | 备注 |
|---|---|---|---|
| `git status` | 通过 | 生成报告前工作区干净；生成后仅新增 `docs/final_score_audit.md` | 无 `.env` 修改 |
| `python --version` | 通过 | Python 3.12.7 | 使用 `.venv` 中 Python |
| `pip install -r requirements.txt` | 通过 | 所有依赖均 Requirement already satisfied | 未升级依赖 |
| `python src/main.py "Agentic RAG"` | 通过 | `evaluation status：pass` | 输出报告到 `src/outputs/latest_report.md` |
| `python src/evaluation/run_evaluation.py` | 通过 | `Benchmark topics: 5`，`Pass count: 5` | 评估报告可生成 |
| `streamlit run src/app.py` | 通过 | `streamlit_started=true` | 短暂启动验证后关闭 |

运行验证时，为避免误消耗 DeepSeek token，应优先保持 `LLM_DRY_RUN=true` 或确认当前测试只需 mock fallback。

## 6. 安全与学术纪律检查

* 未读取或打印 `.env` 中的真实密钥。
* `git ls-files .env` 无输出，说明 `.env` 未被 Git 跟踪。
* `.gitignore` 已包含 `.env`、`.venv/`、缓存、运行历史等。
* `.env.example` 中 `DEEPSEEK_API_KEY=` 为空，未发现真实 key。
* 代码中未发现硬编码 DeepSeek API Key。
* README 引用了 OpenAlex、arXiv、DeepSeek、Streamlit、OpenAI-compatible SDK，来源说明较完整。
* 学术报告仍需要在最终 PDF 中补充参考资料、课程要求对应关系和个人总结，避免“只有项目说明、没有课程总结”的扣分。

## 7. 最关键的扣分风险

1. 最终 PDF 报告缺失：`docs/CS599_大作业报告.pdf` 未发现，这是最高优先级风险。
2. Specs 文档不完整：目前只有 proposal，缺少产品规格、API 规格、评估规格等正式 SDD 材料。
3. 架构图和架构说明不足：README 有流程文字，但缺少 `architecture.md` 或最终报告中的清晰架构图。
4. LICENSE 缺失：Public GitHub 仓库通常建议包含 LICENSE。
5. Demo 截图和评估材料不足：有 `eval_results.md`，但缺少 Streamlit 页面截图、运行截图、DeepSeek/mock fallback 截图。

## 8. 最后 1 小时补救建议

优先级 1：生成最终 PDF 报告  
最少包含封面、目录、选题背景、Specs、架构、关键代码、测试评估、升级扩展、课程总结。

优先级 2：补 `docs/architecture.md`  
写清楚 LangGraph 节点、ResearchState、工具调用、数据流、输出文件策略。可以使用 Mermaid 图。

优先级 3：补 Specs 文档  
至少补：

* `docs/product_spec.md`
* `docs/api_spec.md`
* `docs/evaluation.md`

优先级 4：补 LICENSE  
建议选择 MIT License 或按课程要求选择；如果不确定，至少在 README 中说明课程项目用途。

优先级 5：补截图和提交说明  
保存 Streamlit 页面截图、命令行运行截图、benchmark 结果截图，并在最终报告中引用。

## 9. 最终结论

当前项目代码与 Demo 能力已经较完整，能体现方向一 Agentic AI 原生开发的核心能力：工具调用、LangGraph 状态管理、多步骤 Agent 工作流、轻量记忆、可观测性、benchmark 评估、DeepSeek / Mock fallback、安全配置。

当前主要短板不是代码，而是最终交付材料：PDF 报告、架构文档、Specs 文档、LICENSE 和截图证据。

* 当前保守估分：80 / 100 左右
* 当前乐观估分：86 / 100 左右
* 补齐最终报告和关键 docs 后预计：88-93 / 100
* 是否建议提交：可以提交当前代码和本审查报告，但建议提交前先补最终 PDF 和 architecture.md
* 是否建议打最终 tag：如果只作为 v0.3.7 阶段版本，可以保留 `v0.3.7`；如果最终报告补齐后，建议再打 `v1.0-final`

建议提交本报告：

```bash
git add docs/final_score_audit.md
git commit -m "Add final scoring audit report"
```

如果最终报告、README、代码和评估都确认完成，再执行：

```bash
git tag v1.0-final
git push origin main --tags
```
