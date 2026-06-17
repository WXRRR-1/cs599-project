# 文献调研报告：Memory-Augmented Agents

## 1. 研究主题

本报告围绕 **Memory-Augmented Agents** 进行自动化文献调研，目标是快速了解相关研究方向中的代表性论文、核心方法与初步研究结论。

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

1. **Generative Agents: Interactive Simulacra of Human Behavior**（2023）- Joon Sung Park, Joseph O’Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein；来源：OpenAlex；相关性评分：60
2. **A Survey of Augmented Reality Technologies, Applications and Limitations**（2010）- D. W. F. van Krevelen, Ronald Poelman；来源：OpenAlex；相关性评分：36
3. **Early Exposure to Common Anesthetic Agents Causes Widespread Neurodegeneration in the Developing Rat Brain and Persistent Learning Deficits**（2003）- Vesna Jevtović‐Todorović, Richard E. Hartman, Yukitoshi Izumi, N. Benshoff, Krikor Dikranian, Charles F. Zorumski, John W. Olney, David F. Wozniak；来源：OpenAlex；相关性评分：36
4. **Social Cognitive Theory: An Agentic Perspective**（1999）- Albert Bandura；来源：OpenAlex；相关性评分：36
5. **Multiple Trajectory Prediction of Moving Agents With Memory Augmented Networks**（2020）- Francesco Marchetti, Federico Becattini, Lorenzo Seidenari, Alberto Del Bimbo；来源：OpenAlex；相关性评分：26

## 4. 单篇论文结构化总结

### 论文 1：Generative Agents: Interactive Simulacra of Human Behavior

- 年份：2023
- 作者：Joon Sung Park, Joseph O’Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein
- 来源：OpenAlex
- 相关性评分（relevance_score）：60
- 评分构成（score_breakdown）：
  - keyword_score: 0
  - year_score: 30
  - citation_score: 30
- 筛选理由（score_reason）：标题和摘要未明显命中规划关键词，年份较新，引用量较高。
- 研究背景：该论文围绕“Generative Agents: Interactive Simulacra of Human Behavior”展开，摘要显示其研究背景与当前智能系统、信息检索或相关任务的发展需求有关。
- 研究问题：论文关注的核心问题可从摘要中概括为：如何在已有方法基础上提升任务效果、系统能力或应用可靠性。
- 核心方法：根据摘要，论文主要方法包括：Believable proxies of human behavior can empower interactive applications ranging from immersive environments to rehearsal spaces for interpersonal communication to prototyping too...
- 主要贡献：该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。
- 局限性：当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。
- 链接：https://doi.org/10.1145/3586183.3606763

### 论文 2：A Survey of Augmented Reality Technologies, Applications and Limitations

- 年份：2010
- 作者：D. W. F. van Krevelen, Ronald Poelman
- 来源：OpenAlex
- 相关性评分（relevance_score）：36
- 评分构成（score_breakdown）：
  - keyword_score: 0
  - year_score: 6
  - citation_score: 30
- 筛选理由（score_reason）：标题和摘要未明显命中规划关键词，年份较早或缺失，引用量较高。
- 研究背景：该论文围绕“A Survey of Augmented Reality Technologies, Applications and Limitations”展开，摘要显示其研究背景与当前智能系统、信息检索或相关任务的发展需求有关。
- 研究问题：论文关注的核心问题可从摘要中概括为：如何在已有方法基础上提升任务效果、系统能力或应用可靠性。
- 核心方法：根据摘要，论文主要方法包括：A Survey of Augmented Reality Technologies, Applications and Limitations
- 主要贡献：该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。
- 局限性：当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。
- 链接：https://doi.org/10.20870/ijvr.2010.9.2.2767

### 论文 3：Early Exposure to Common Anesthetic Agents Causes Widespread Neurodegeneration in the Developing Rat Brain and Persistent Learning Deficits

- 年份：2003
- 作者：Vesna Jevtović‐Todorović, Richard E. Hartman, Yukitoshi Izumi, N. Benshoff, Krikor Dikranian, Charles F. Zorumski, John W. Olney, David F. Wozniak
- 来源：OpenAlex
- 相关性评分（relevance_score）：36
- 评分构成（score_breakdown）：
  - keyword_score: 0
  - year_score: 6
  - citation_score: 30
- 筛选理由（score_reason）：标题和摘要未明显命中规划关键词，年份较早或缺失，引用量较高。
- 研究背景：该论文围绕“Early Exposure to Common Anesthetic Agents Causes Widespread Neurodegeneration in the Developing Rat Brain and Persistent Learning Deficits”展开，摘要显示其研究背景与当前智能系统、信息检索或相关任务的发展需求有关。
- 研究问题：论文关注的核心问题可从摘要中概括为：如何在已有方法基础上提升任务效果、系统能力或应用可靠性。
- 核心方法：根据摘要，论文主要方法包括：Recently it was demonstrated that exposure of the developing brain during the period of synaptogenesis to drugs that block NMDA glutamate receptors or drugs that potentiate GABA(A)...
- 主要贡献：该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。
- 局限性：当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。
- 链接：https://doi.org/10.1523/jneurosci.23-03-00876.2003

### 论文 4：Social Cognitive Theory: An Agentic Perspective

- 年份：1999
- 作者：Albert Bandura
- 来源：OpenAlex
- 相关性评分（relevance_score）：36
- 评分构成（score_breakdown）：
  - keyword_score: 0
  - year_score: 6
  - citation_score: 30
- 筛选理由（score_reason）：标题和摘要未明显命中规划关键词，年份较早或缺失，引用量较高。
- 研究背景：该论文围绕“Social Cognitive Theory: An Agentic Perspective”展开，摘要显示其研究背景与当前智能系统、信息检索或相关任务的发展需求有关。
- 研究问题：论文关注的核心问题可从摘要中概括为：如何在已有方法基础上提升任务效果、系统能力或应用可靠性。
- 核心方法：根据摘要，论文主要方法包括：This article presents the basic tenets of social cognitive theory. It is founded on a causal model of triadic reciprocal causation in which personal factors in the form of cognitiv...
- 主要贡献：该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。
- 局限性：当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。
- 链接：https://doi.org/10.1111/1467-839x.00024

### 论文 5：Multiple Trajectory Prediction of Moving Agents With Memory Augmented Networks

- 年份：2020
- 作者：Francesco Marchetti, Federico Becattini, Lorenzo Seidenari, Alberto Del Bimbo
- 来源：OpenAlex
- 相关性评分（relevance_score）：26
- 评分构成（score_breakdown）：
  - keyword_score: 0
  - year_score: 14
  - citation_score: 12
- 筛选理由（score_reason）：标题和摘要未明显命中规划关键词，年份具有一定时效性，引用量中等。
- 研究背景：该论文围绕“Multiple Trajectory Prediction of Moving Agents With Memory Augmented Networks”展开，摘要显示其研究背景与当前智能系统、信息检索或相关任务的发展需求有关。
- 研究问题：论文关注的核心问题可从摘要中概括为：如何在已有方法基础上提升任务效果、系统能力或应用可靠性。
- 核心方法：根据摘要，论文主要方法包括：Pedestrians and drivers are expected to safely navigate complex urban environments along with several non cooperating agents. Autonomous vehicles will soon replicate this capabilit...
- 主要贡献：该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。
- 局限性：当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。
- 链接：https://doi.org/10.1109/tpami.2020.3008558


## 5. 文献对比表

| 论文 | 年份 | 来源 | 相关性评分 | 核心方法 | 主要贡献 | 局限性 |
|---|---:|---|---:|---|---|---|
| Generative Agents: Interactive Simulacra of Human Behavior | 2023 | OpenAlex | 60 | 根据摘要，论文主要方法包括：Believable proxies of human behavior can empower interactive applications ranging from immersive environments to rehearsal spaces for interpersonal communication to prototyping too... | 该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。 | 当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。 |
| A Survey of Augmented Reality Technologies, Applications and Limitations | 2010 | OpenAlex | 36 | 根据摘要，论文主要方法包括：A Survey of Augmented Reality Technologies, Applications and Limitations | 该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。 | 当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。 |
| Early Exposure to Common Anesthetic Agents Causes Widespread Neurodegeneration in the Developing Rat Brain and Persistent Learning Deficits | 2003 | OpenAlex | 36 | 根据摘要，论文主要方法包括：Recently it was demonstrated that exposure of the developing brain during the period of synaptogenesis to drugs that block NMDA glutamate receptors or drugs that potentiate GABA(A)... | 该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。 | 当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。 |
| Social Cognitive Theory: An Agentic Perspective | 1999 | OpenAlex | 36 | 根据摘要，论文主要方法包括：This article presents the basic tenets of social cognitive theory. It is founded on a causal model of triadic reciprocal causation in which personal factors in the form of cognitiv... | 该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。 | 当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。 |
| Multiple Trajectory Prediction of Moving Agents With Memory Augmented Networks | 2020 | OpenAlex | 26 | 根据摘要，论文主要方法包括：Pedestrians and drivers are expected to safely navigate complex urban environments along with several non cooperating agents. Autonomous vehicles will soon replicate this capabilit... | 该论文的主要贡献在于提出或验证了一种面向具体研究问题的技术方案，并提供了实验或分析依据。 | 当前 mock 模式仅基于标题和摘要生成概括；如果摘要信息有限，无法判断更具体的局限性。 |

## 6. 初步结论

从当前检索结果看，**Memory-Augmented Agents** 相关研究通常围绕任务建模、系统架构、方法评估与实际应用展开。当前版本的结论仅基于标题和摘要，适合作为课程展示中的初步文献调研材料；后续版本可进一步加入多步骤 Agent 工作流、交叉验证与全文级分析。

## 7. 参考文献

1. Joon Sung Park, Joseph O’Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein. Generative Agents: Interactive Simulacra of Human Behavior. 2023. https://doi.org/10.1145/3586183.3606763
2. D. W. F. van Krevelen, Ronald Poelman. A Survey of Augmented Reality Technologies, Applications and Limitations. 2010. https://doi.org/10.20870/ijvr.2010.9.2.2767
3. Vesna Jevtović‐Todorović, Richard E. Hartman, Yukitoshi Izumi, N. Benshoff, Krikor Dikranian, Charles F. Zorumski, John W. Olney, David F. Wozniak. Early Exposure to Common Anesthetic Agents Causes Widespread Neurodegeneration in the Developing Rat Brain and Persistent Learning Deficits. 2003. https://doi.org/10.1523/jneurosci.23-03-00876.2003
4. Albert Bandura. Social Cognitive Theory: An Agentic Perspective. 1999. https://doi.org/10.1111/1467-839x.00024
5. Francesco Marchetti, Federico Becattini, Lorenzo Seidenari, Alberto Del Bimbo. Multiple Trajectory Prediction of Moving Agents With Memory Augmented Networks. 2020. https://doi.org/10.1109/tpami.2020.3008558
