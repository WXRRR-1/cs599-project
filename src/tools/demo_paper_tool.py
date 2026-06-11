"""Built-in demo papers used when the public search API is unavailable.

This keeps the v0.1 classroom demo visible even before an academic search API
key is configured. The real workflow still tries OpenAlex and arXiv first.
"""

from __future__ import annotations


def get_demo_papers(topic: str, limit: int = 10) -> list[dict]:
    """Return representative demo papers for a local fallback run."""
    papers = [
        {
            "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
            "authors": "Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Kuttler, Mike Lewis, Wen-tau Yih, Tim Rocktaschel, Sebastian Riedel, Douwe Kiela",
            "year": 2020,
            "abstract": "Retrieval-Augmented Generation combines a pretrained sequence-to-sequence model with a dense vector index of Wikipedia, allowing the model to retrieve external knowledge and condition generation on retrieved passages for knowledge-intensive NLP tasks.",
            "citationCount": 4500,
            "url": "https://arxiv.org/abs/2005.11401",
            "venue": "NeurIPS",
        },
        {
            "title": "ReAct: Synergizing Reasoning and Acting in Language Models",
            "authors": "Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao",
            "year": 2023,
            "abstract": "ReAct prompts language models to generate both reasoning traces and task-specific actions, enabling models to interact with external environments such as Wikipedia search while maintaining interpretable reasoning trajectories.",
            "citationCount": 2500,
            "url": "https://arxiv.org/abs/2210.03629",
            "venue": "ICLR",
        },
        {
            "title": "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection",
            "authors": "Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, Hannaneh Hajishirzi",
            "year": 2023,
            "abstract": "Self-RAG trains a language model to adaptively retrieve passages, generate responses, and critique its own outputs using reflection tokens, improving factuality and controllability for retrieval-augmented generation.",
            "citationCount": 900,
            "url": "https://arxiv.org/abs/2310.11511",
            "venue": "arXiv",
        },
        {
            "title": "Corrective Retrieval Augmented Generation",
            "authors": "Shi-Qi Yan, Jia-Chen Gu, Yun Zhu, Zhen-Hua Ling",
            "year": 2024,
            "abstract": "Corrective Retrieval Augmented Generation introduces a lightweight evaluator to assess retrieved documents and trigger corrective actions, aiming to reduce the impact of irrelevant or low-quality retrieved evidence.",
            "citationCount": 250,
            "url": "https://arxiv.org/abs/2401.15884",
            "venue": "arXiv",
        },
        {
            "title": "Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity",
            "authors": "Akhil Mallen, Akari Asai, Victor Zhong, Rajarshi Das, Daniel Khashabi, Hannaneh Hajishirzi",
            "year": 2024,
            "abstract": "Adaptive-RAG studies how retrieval-augmented systems can select different strategies according to question complexity, balancing efficiency and answer quality across simple and complex information needs.",
            "citationCount": 180,
            "url": "https://arxiv.org/abs/2403.14403",
            "venue": "arXiv",
        },
    ]

    normalized_topic = topic.strip()
    if normalized_topic:
        for paper in papers:
            paper["abstract"] = (
                paper["abstract"]
                + f" This fallback record is used to demonstrate a literature review workflow for the topic: {normalized_topic}."
            )

    return papers[: max(1, min(limit, len(papers)))]
