# 文献调研报告：Agentic RAG

## 1. 研究主题

本报告围绕 **Agentic RAG** 进行自动化文献调研，目标是快速了解相关研究方向中的代表性论文、核心方法与初步研究结论。

## 2. 检索与筛选说明

系统优先使用 OpenAlex API 检索相关论文，失败后切换到 arXiv API，并过滤掉缺少标题或摘要的结果。当前 v0.1 Demo 使用简单规则进行筛选：优先选择引用量较高、年份较新的论文。随后基于论文标题和摘要生成中文结构化总结。

## 3. 代表性论文列表

1. **Emulsifier of Arthrobacter RAG-1: isolation and emulsifying properties**（1979）- Eugene Rosenberg, A. Zuckerberg, C. Rubinovitz, David L. Gutnick
2. **Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG**（2025）- Aditi Singh, Abul Ehtesham, Saket Kumar, Tala Talaei Khoei, Vasilakos, Athanasios V.
3. **Multi-Agent RAG Chatbot Architecture for Decision Support in Net-Zero Emission Energy Systems**（2024）- Gihan Gamage, Nishan Mills, Daswin De Silva, Milos Manic, Harsha Moraliyage, Andrew Jennings, Damminda Alahakoon
4. **CyberRAG: An agentic RAG cyber attack classification and reporting tool**（2025）- Francesco Blefari, Cristian Cosentino, Francesco Aurelio Pironti, Angelo Furfaro, Fabrizio Marozzo
5. **Sustainable Digitalization of Business with Multi-Agent RAG and LLM**（2024）- Muhammad Arslan, Saba Munawar, Christophe Cruz

## 4. 单篇论文结构化总结

### 论文 1：Emulsifier of Arthrobacter RAG-1: isolation and emulsifying properties

- 年份：1979
- 作者：Eugene Rosenberg, A. Zuckerberg, C. Rubinovitz, David L. Gutnick
- 研究背景：该论文围绕“Emulsifier of Arthrobacter RAG-1: isolation and emulsifying properties”展开，摘要显示其研究背景与当前智能系统、信息检索或相关任务的发展需求有关。
- 研究问题：论文关注的问题可从摘要中概括为：如何在既有方法基础上提升任务效果、系统能力或应用可靠性。
- 核心方法：根据摘要，论文主要方法包括：The oil-degrading Arthrobacter sp. RAG-1 produced an extracellular nondialyzable emulsifying agent when grown on hexadecane, ethanol, or acetate medium. The emulsifier was prepared...
- 主要贡献：该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。
- 局限性：当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。
- 链接：https://doi.org/10.1128/aem.37.3.402-408.1979

### 论文 2：Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG

- 年份：2025
- 作者：Aditi Singh, Abul Ehtesham, Saket Kumar, Tala Talaei Khoei, Vasilakos, Athanasios V.
- 研究背景：该论文围绕“Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG”展开，摘要显示其研究背景与当前智能系统、信息检索或相关任务的发展需求有关。
- 研究问题：论文关注的问题可从摘要中概括为：如何在既有方法基础上提升任务效果、系统能力或应用可靠性。
- 核心方法：根据摘要，论文主要方法包括：Large Language Models (LLMs) have advanced artificial intelligence by enabling human-like text generation and natural language understanding. However, their reliance on static trai...
- 主要贡献：该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。
- 局限性：当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。
- 链接：http://arxiv.org/abs/2501.09136

### 论文 3：Multi-Agent RAG Chatbot Architecture for Decision Support in Net-Zero Emission Energy Systems

- 年份：2024
- 作者：Gihan Gamage, Nishan Mills, Daswin De Silva, Milos Manic, Harsha Moraliyage, Andrew Jennings, Damminda Alahakoon
- 研究背景：该论文围绕“Multi-Agent RAG Chatbot Architecture for Decision Support in Net-Zero Emission Energy Systems”展开，摘要显示其研究背景与当前智能系统、信息检索或相关任务的发展需求有关。
- 研究问题：论文关注的问题可从摘要中概括为：如何在既有方法基础上提升任务效果、系统能力或应用可靠性。
- 核心方法：根据摘要，论文主要方法包括：Modern energy platforms are increasingly leveraging Artificial Intelligence (AI) for effective decision-making and efficient operations. This has led to the development of expansiv...
- 主要贡献：该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。
- 局限性：当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。
- 链接：https://doi.org/10.1109/icit58233.2024.10540920

### 论文 4：CyberRAG: An agentic RAG cyber attack classification and reporting tool

- 年份：2025
- 作者：Francesco Blefari, Cristian Cosentino, Francesco Aurelio Pironti, Angelo Furfaro, Fabrizio Marozzo
- 研究背景：该论文围绕“CyberRAG: An agentic RAG cyber attack classification and reporting tool”展开，摘要显示其研究背景与当前智能系统、信息检索或相关任务的发展需求有关。
- 研究问题：论文关注的问题可从摘要中概括为：如何在既有方法基础上提升任务效果、系统能力或应用可靠性。
- 核心方法：根据摘要，论文主要方法包括：Intrusion Detection and Prevention Systems (IDS/IPS) in large enterprises can generate hundreds of thousands of alerts per hour, overwhelming analysts with logs requiring rapidly e...
- 主要贡献：该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。
- 局限性：当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。
- 链接：https://doi.org/10.1016/j.future.2025.108186

### 论文 5：Sustainable Digitalization of Business with Multi-Agent RAG and LLM

- 年份：2024
- 作者：Muhammad Arslan, Saba Munawar, Christophe Cruz
- 研究背景：该论文围绕“Sustainable Digitalization of Business with Multi-Agent RAG and LLM”展开，摘要显示其研究背景与当前智能系统、信息检索或相关任务的发展需求有关。
- 研究问题：论文关注的问题可从摘要中概括为：如何在既有方法基础上提升任务效果、系统能力或应用可靠性。
- 核心方法：根据摘要，论文主要方法包括：Businesses heavily rely on data sourced from various channels like news articles, financial reports, and consumer reviews to drive their operations, enabling informed decision-maki...
- 主要贡献：该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。
- 局限性：当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。
- 链接：https://doi.org/10.1016/j.procs.2024.09.337


## 5. 文献对比表

| 论文 | 年份 | 核心方法 | 主要贡献 | 局限性 |
|---|---:|---|---|---|
| Emulsifier of Arthrobacter RAG-1: isolation and emulsifying properties | 1979 | 根据摘要，论文主要方法包括：The oil-degrading Arthrobacter sp. RAG-1 produced an extracellular nondialyzable emulsifying agent when grown on hexadecane, ethanol, or acetate medium. The emulsifier was prepared... | 该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。 | 当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。 |
| Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG | 2025 | 根据摘要，论文主要方法包括：Large Language Models (LLMs) have advanced artificial intelligence by enabling human-like text generation and natural language understanding. However, their reliance on static trai... | 该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。 | 当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。 |
| Multi-Agent RAG Chatbot Architecture for Decision Support in Net-Zero Emission Energy Systems | 2024 | 根据摘要，论文主要方法包括：Modern energy platforms are increasingly leveraging Artificial Intelligence (AI) for effective decision-making and efficient operations. This has led to the development of expansiv... | 该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。 | 当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。 |
| CyberRAG: An agentic RAG cyber attack classification and reporting tool | 2025 | 根据摘要，论文主要方法包括：Intrusion Detection and Prevention Systems (IDS/IPS) in large enterprises can generate hundreds of thousands of alerts per hour, overwhelming analysts with logs requiring rapidly e... | 该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。 | 当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。 |
| Sustainable Digitalization of Business with Multi-Agent RAG and LLM | 2024 | 根据摘要，论文主要方法包括：Businesses heavily rely on data sourced from various channels like news articles, financial reports, and consumer reviews to drive their operations, enabling informed decision-maki... | 该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。 | 当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。 |

## 6. 初步结论

从当前检索结果看，**Agentic RAG** 相关研究通常围绕任务建模、系统架构、方法评估与实际应用展开。v0.1 Demo 的结论仅基于标题和摘要，适合作为课程展示中的初步文献调研材料；后续版本可进一步加入多步骤 Agent 工作流、交叉验证与全文级分析。

## 7. 参考文献

1. Eugene Rosenberg, A. Zuckerberg, C. Rubinovitz, David L. Gutnick. Emulsifier of Arthrobacter RAG-1: isolation and emulsifying properties. 1979. https://doi.org/10.1128/aem.37.3.402-408.1979
2. Aditi Singh, Abul Ehtesham, Saket Kumar, Tala Talaei Khoei, Vasilakos, Athanasios V.. Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG. 2025. http://arxiv.org/abs/2501.09136
3. Gihan Gamage, Nishan Mills, Daswin De Silva, Milos Manic, Harsha Moraliyage, Andrew Jennings, Damminda Alahakoon. Multi-Agent RAG Chatbot Architecture for Decision Support in Net-Zero Emission Energy Systems. 2024. https://doi.org/10.1109/icit58233.2024.10540920
4. Francesco Blefari, Cristian Cosentino, Francesco Aurelio Pironti, Angelo Furfaro, Fabrizio Marozzo. CyberRAG: An agentic RAG cyber attack classification and reporting tool. 2025. https://doi.org/10.1016/j.future.2025.108186
5. Muhammad Arslan, Saba Munawar, Christophe Cruz. Sustainable Digitalization of Business with Multi-Agent RAG and LLM. 2024. https://doi.org/10.1016/j.procs.2024.09.337
