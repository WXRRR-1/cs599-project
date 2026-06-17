# 文献调研报告：Agentic RAG

## 1. 研究主题

本报告围绕 **Agentic RAG** 进行自动化文献调研，目标是快速了解相关研究方向中的代表性论文、核心方法与初步研究结论。

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

1. **Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG**（2025）- Aditi Singh, Abul Ehtesham, Saket Kumar, Tala Talaei Khoei, Vasilakos, Athanasios V.；来源：OpenAlex；相关性评分：76
2. **Agentic RAG with Human-in-the-Retrieval**（2025）- Xiwei Xu, Dawen Zhang, Qing Liu, Qinghua Lu, Liming Zhu；来源：OpenAlex；相关性评分：71
3. **CyberRAG: An agentic RAG cyber attack classification and reporting tool**（2025）- Francesco Blefari, Cristian Cosentino, Francesco Aurelio Pironti, Angelo Furfaro, Fabrizio Marozzo；来源：OpenAlex；相关性评分：57
4. **Monitoring indoor environmental conditions in office buildings using a sustainable Agentic RAG-LLM system**（2025）- Muhammad Arslan, Saba Munawar, Lamine Mahdjoubi, Patrick Manu；来源：OpenAlex；相关性评分：57
5. **MARSHA: multi-agent RAG system for hazard adaptation**（2025）- Yangxinyu Xie, Bowen Jiang, Tanwi Mallick, Joshua Bergerson, John K. Hutchison, Duane R. Verner, Jordan Branham, M. Ross Alexander, Robert B. Ross, Yan Feng, Leslie-Anne Levy, Weijie Su, Camillo J. Taylor；来源：OpenAlex；相关性评分：57

## 4. 单篇论文结构化总结

### 论文 1：Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG

- 年份：2025
- 作者：Aditi Singh, Abul Ehtesham, Saket Kumar, Tala Talaei Khoei, Vasilakos, Athanasios V.
- 来源：OpenAlex
- 相关性评分（relevance_score）：76
- 评分构成（score_breakdown）：
  - keyword_score: 40
  - year_score: 30
  - citation_score: 6
- 筛选理由（score_reason）：标题或摘要命中关键词：agentic rag, retrieval-augmented generation, ai agent，年份较新，引用量较低或暂缺。
- 研究背景：该论文围绕“Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG”展开，摘要显示其研究背景与当前智能系统、信息检索或相关任务的发展需求有关。
- 研究问题：论文关注的核心问题可从摘要中概括为：如何在已有方法基础上提升任务效果、系统能力或应用可靠性。
- 核心方法：根据摘要，论文主要方法包括：Large Language Models (LLMs) have advanced artificial intelligence by enabling human-like text generation and natural language understanding. However, their reliance on static trai...
- 主要贡献：该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。
- 局限性：当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。
- 链接：http://arxiv.org/abs/2501.09136

### 论文 2：Agentic RAG with Human-in-the-Retrieval

- 年份：2025
- 作者：Xiwei Xu, Dawen Zhang, Qing Liu, Qinghua Lu, Liming Zhu
- 来源：OpenAlex
- 相关性评分（relevance_score）：71
- 评分构成（score_breakdown）：
  - keyword_score: 35
  - year_score: 30
  - citation_score: 6
- 筛选理由（score_reason）：标题或摘要命中关键词：agentic rag, retrieval-augmented generation, ai agent，年份较新，引用量较低或暂缺。
- 研究背景：该论文围绕“Agentic RAG with Human-in-the-Retrieval”展开，摘要显示其研究背景与当前智能系统、信息检索或相关任务的发展需求有关。
- 研究问题：论文关注的核心问题可从摘要中概括为：如何在已有方法基础上提升任务效果、系统能力或应用可靠性。
- 核心方法：根据摘要，论文主要方法包括：Retrieval-Augmented Generation (RAG) has emerged as a promising solution to address key challenges faced by GenAI, such as hallucination, outdated or non-removable parametric knowl...
- 主要贡献：该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。
- 局限性：当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。
- 链接：https://doi.org/10.1109/icsa-c65153.2025.00074

### 论文 3：CyberRAG: An agentic RAG cyber attack classification and reporting tool

- 年份：2025
- 作者：Francesco Blefari, Cristian Cosentino, Francesco Aurelio Pironti, Angelo Furfaro, Fabrizio Marozzo
- 来源：OpenAlex
- 相关性评分（relevance_score）：57
- 评分构成（score_breakdown）：
  - keyword_score: 21
  - year_score: 30
  - citation_score: 6
- 筛选理由（score_reason）：标题或摘要命中关键词：agentic rag, retrieval-augmented generation，年份较新，引用量较低或暂缺。
- 研究背景：该论文围绕“CyberRAG: An agentic RAG cyber attack classification and reporting tool”展开，摘要显示其研究背景与当前智能系统、信息检索或相关任务的发展需求有关。
- 研究问题：论文关注的核心问题可从摘要中概括为：如何在已有方法基础上提升任务效果、系统能力或应用可靠性。
- 核心方法：根据摘要，论文主要方法包括：Intrusion Detection and Prevention Systems (IDS/IPS) in large enterprises can generate hundreds of thousands of alerts per hour, overwhelming analysts with logs requiring rapidly e...
- 主要贡献：该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。
- 局限性：当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。
- 链接：https://doi.org/10.1016/j.future.2025.108186

### 论文 4：Monitoring indoor environmental conditions in office buildings using a sustainable Agentic RAG-LLM system

- 年份：2025
- 作者：Muhammad Arslan, Saba Munawar, Lamine Mahdjoubi, Patrick Manu
- 来源：OpenAlex
- 相关性评分（relevance_score）：57
- 评分构成（score_breakdown）：
  - keyword_score: 21
  - year_score: 30
  - citation_score: 6
- 筛选理由（score_reason）：标题或摘要命中关键词：agentic rag, retrieval-augmented generation，年份较新，引用量较低或暂缺。
- 研究背景：该论文围绕“Monitoring indoor environmental conditions in office buildings using a sustainable Agentic RAG-LLM system”展开，摘要显示其研究背景与当前智能系统、信息检索或相关任务的发展需求有关。
- 研究问题：论文关注的核心问题可从摘要中概括为：如何在已有方法基础上提升任务效果、系统能力或应用可靠性。
- 核心方法：根据摘要，论文主要方法包括：• Indoor Environmental Conditions impact health, productivity, and energy use. • Thermal comfort monitoring requires diverse data and intelligent analysis. • BIM integration with r...
- 主要贡献：该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。
- 局限性：当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。
- 链接：https://doi.org/10.1016/j.enbuild.2025.116276

### 论文 5：MARSHA: multi-agent RAG system for hazard adaptation

- 年份：2025
- 作者：Yangxinyu Xie, Bowen Jiang, Tanwi Mallick, Joshua Bergerson, John K. Hutchison, Duane R. Verner, Jordan Branham, M. Ross Alexander, Robert B. Ross, Yan Feng, Leslie-Anne Levy, Weijie Su, Camillo J. Taylor
- 来源：OpenAlex
- 相关性评分（relevance_score）：57
- 评分构成（score_breakdown）：
  - keyword_score: 21
  - year_score: 30
  - citation_score: 6
- 筛选理由（score_reason）：标题或摘要命中关键词：retrieval-augmented generation, multi-agent rag，年份较新，引用量较低或暂缺。
- 研究背景：该论文围绕“MARSHA: multi-agent RAG system for hazard adaptation”展开，摘要显示其研究背景与当前智能系统、信息检索或相关任务的发展需求有关。
- 研究问题：论文关注的核心问题可从摘要中概括为：如何在已有方法基础上提升任务效果、系统能力或应用可靠性。
- 核心方法：根据摘要，论文主要方法包括：Large language models (LLMs) are a transformational capability at the frontier of artificial intelligence and machine learning that can support decision-makers in addressing pressi...
- 主要贡献：该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。
- 局限性：当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。
- 链接：https://doi.org/10.1038/s44168-025-00254-1


## 5. 文献对比表

| 论文 | 年份 | 来源 | 相关性评分 | 核心方法 | 主要贡献 | 局限性 |
|---|---:|---|---:|---|---|---|
| Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG | 2025 | OpenAlex | 76 | 根据摘要，论文主要方法包括：Large Language Models (LLMs) have advanced artificial intelligence by enabling human-like text generation and natural language understanding. However, their reliance on static trai... | 该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。 | 当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。 |
| Agentic RAG with Human-in-the-Retrieval | 2025 | OpenAlex | 71 | 根据摘要，论文主要方法包括：Retrieval-Augmented Generation (RAG) has emerged as a promising solution to address key challenges faced by GenAI, such as hallucination, outdated or non-removable parametric knowl... | 该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。 | 当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。 |
| CyberRAG: An agentic RAG cyber attack classification and reporting tool | 2025 | OpenAlex | 57 | 根据摘要，论文主要方法包括：Intrusion Detection and Prevention Systems (IDS/IPS) in large enterprises can generate hundreds of thousands of alerts per hour, overwhelming analysts with logs requiring rapidly e... | 该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。 | 当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。 |
| Monitoring indoor environmental conditions in office buildings using a sustainable Agentic RAG-LLM system | 2025 | OpenAlex | 57 | 根据摘要，论文主要方法包括：• Indoor Environmental Conditions impact health, productivity, and energy use. • Thermal comfort monitoring requires diverse data and intelligent analysis. • BIM integration with r... | 该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。 | 当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。 |
| MARSHA: multi-agent RAG system for hazard adaptation | 2025 | OpenAlex | 57 | 根据摘要，论文主要方法包括：Large language models (LLMs) are a transformational capability at the frontier of artificial intelligence and machine learning that can support decision-makers in addressing pressi... | 该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。 | 当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。 |

## 6. 初步结论

从当前检索结果看，**Agentic RAG** 相关研究通常围绕任务建模、系统架构、方法评估与实际应用展开。当前版本的结论仅基于标题和摘要，适合作为课程展示中的初步文献调研材料；后续版本可进一步加入多步骤 Agent 工作流、交叉验证与全文级分析。

## 7. 参考文献

1. Aditi Singh, Abul Ehtesham, Saket Kumar, Tala Talaei Khoei, Vasilakos, Athanasios V.. Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG. 2025. http://arxiv.org/abs/2501.09136
2. Xiwei Xu, Dawen Zhang, Qing Liu, Qinghua Lu, Liming Zhu. Agentic RAG with Human-in-the-Retrieval. 2025. https://doi.org/10.1109/icsa-c65153.2025.00074
3. Francesco Blefari, Cristian Cosentino, Francesco Aurelio Pironti, Angelo Furfaro, Fabrizio Marozzo. CyberRAG: An agentic RAG cyber attack classification and reporting tool. 2025. https://doi.org/10.1016/j.future.2025.108186
4. Muhammad Arslan, Saba Munawar, Lamine Mahdjoubi, Patrick Manu. Monitoring indoor environmental conditions in office buildings using a sustainable Agentic RAG-LLM system. 2025. https://doi.org/10.1016/j.enbuild.2025.116276
5. Yangxinyu Xie, Bowen Jiang, Tanwi Mallick, Joshua Bergerson, John K. Hutchison, Duane R. Verner, Jordan Branham, M. Ross Alexander, Robert B. Ross, Yan Feng, Leslie-Anne Levy, Weijie Su, Camillo J. Taylor. MARSHA: multi-agent RAG system for hazard adaptation. 2025. https://doi.org/10.1038/s44168-025-00254-1
