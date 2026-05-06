# 2026-05-05 全量简报

# HiL-Bench (Human-in-Loop Benchmark): Do Agents Know When to Ask for Help?

**【AI助手如何判断何时求助】**

**arXiv**: https://arxiv.org/abs/2604.09408  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.09408  
**HF Paper**: https://hf-mirror.com/papers/2604.09408  
**HF Votes**: 1

## 简要摘要

*自然语言处理;智能体与交互;人机协作决策*

当前智能体在处理信息不全的任务时难以判断何时应自主行动、何时需向人类求助，现有基准无法评估这一关键能力。
提出新基准HiL-Bench和Ask-F1指标来评估智能体选择性求助的能力，发现前沿模型普遍存在判断缺陷，但通过强化学习可训练该能力。

---

# Prior-Aligned Data Cleaning for Tabular Foundation Models

**【表格基础模型数据清洗对齐】**

**arXiv**: https://arxiv.org/abs/2604.25154  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.25154  
**HF Paper**: https://hf-mirror.com/papers/2604.25154  
**HF Votes**: 1

## 简要摘要

*机器学习;数据预处理;表格数据清洗对齐*

表格基础模型在干净数据上零样本性能优异，但实际数据存在缺失值等问题导致性能下降。
提出强化学习框架L2C2，通过智能排序清洗操作对齐数据分布，提升模型准确率与泛化能力。

---

# Assessing Pancreatic Ductal Adenocarcinoma Vascular Invasion: the PDACVI Benchmark

**【胰腺癌血管侵犯AI评估基准  】**

**arXiv**: https://arxiv.org/abs/2604.27582  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.27582  
**HF Paper**: https://hf-mirror.com/papers/2604.27582  
**HF Votes**: 1

## 简要摘要

*计算机视觉;医学图像分析;胰腺癌血管侵犯评估  *

胰腺癌手术需准确评估肿瘤对血管的侵犯，但现有方法面临公开数据缺乏和诊断模糊的挑战。  
研究者发布了包含多专家标注的数据集和评测基准，发现传统分割模型在关键区域表现不稳定，而考虑标注不确定性的概率模型更具鲁棒性。

---

# From Context to Skills: Can Language Models Learn from Context Skillfully?

**【语言模型从上下文学习技能】**

**arXiv**: https://arxiv.org/abs/2604.27660  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.27660  
**HF Paper**: https://hf-mirror.com/papers/2604.27660  
**HF Votes**: 120

## 简要摘要

*自然语言处理;大语言模型;上下文技能学习*

许多现实任务需要语言模型从超出其参数知识的长篇复杂上下文中学习并推理。
提出一个无需人工监督的自进化框架，通过多智能体博弈自动发现和精炼上下文特定技能，提升模型的上下文学习能力。

---

# Repetition over Diversity: High-Signal Data Filtering for Sample-Efficient German Language Modeling

**【重复高质量数据提升德语模型训练效率】**

**arXiv**: https://arxiv.org/abs/2604.28075  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.28075  
**HF Paper**: https://hf-mirror.com/papers/2604.28075  
**HF Votes**: 13

## 简要摘要

*自然语言处理;语言模型预训练;德语语料过滤策略*

研究探讨在德语大语言模型预训练中，是使用大量轻度过滤的多样数据单次训练，还是重复训练少量严格过滤的高质量数据更有效。
通过分级过滤构建不同质量的德语语料子集并进行多尺度实验，发现重复训练高质量数据能持续优于单次训练更多数据，并发布了相关模型与评测基准。

---

# Hierarchical Abstract Tree for Cross-Document Retrieval-Augmented Generation

**【跨文档检索增强生成索引优化】**

**arXiv**: https://arxiv.org/abs/2605.00529  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2605.00529  
**HF Paper**: https://hf-mirror.com/papers/2605.00529  
**HF Votes**: 3

## 简要摘要

*自然语言处理;检索增强生成;知识库索引构建*

现有树状检索增强生成方法在处理跨文档多跳问题时面临适应性差、结构孤立和抽象粗糙等挑战。
提出了Ψ-RAG框架，通过无分布假设的层次抽象树索引和智能多粒度检索代理，显著提升了跨文档问答性能。

---

# Persistent Visual Memory: Sustaining Perception for Deep Generation in LVLMs

**【保持长序列生成中视觉感知持续准确】**

**arXiv**: https://arxiv.org/abs/2605.00814  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2605.00814  
**HF Paper**: https://hf-mirror.com/papers/2605.00814  
**HF Votes**: 12

## 简要摘要

*多模态大模型;视觉语言理解;长序列视觉感知*

自回归视觉语言模型在生成长文本时会出现视觉信号稀释问题
提出轻量持续视觉记忆模块，通过并行检索路径缓解信号衰减

---

# OceanPile: A Large-Scale Multimodal Ocean Corpus for Foundation Models

**【构建海洋多模态基础模型数据集】**

**arXiv**: https://arxiv.org/abs/2605.00877  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2605.00877  
**HF Paper**: https://hf-mirror.com/papers/2605.00877  
**HF Votes**: 10

## 简要摘要

*多模态学习;多模态大语言模型;海洋科学知识建模*

海洋数据高度碎片化且缺乏高质量对齐的多模态数据集，限制了AI在海洋领域的应用。
我们构建了一个高质量、大规模的多模态海洋语料库OceanPile，包含整合数据、指令集和评测基准，以支持海洋领域AI模型发展。

---

# Linking spatial biology and clinical histology via Haiku

**【多模态医学图像分析】**

**arXiv**: https://arxiv.org/abs/2605.00925  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2605.00925  
**HF Paper**: https://hf-mirror.com/papers/2605.00925  

## 简要摘要

*医学影像分析；多模态学习；空间生物学与临床病理对齐*

整合分子、形态和临床数据对生物医学研究至关重要，但联合建模框架有限。
提出Haiku三模态对比学习模型，实现跨模态检索、提升预测任务，并通过反事实分析探索生物学关联。

---

# Code World Model Preparedness Report

**【评估代码生成模型风险】**

**arXiv**: https://arxiv.org/abs/2605.00932  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2605.00932  
**HF Paper**: https://hf-mirror.com/papers/2605.00932  
**HF Votes**: 2

## 简要摘要

*代码生成与推理;大语言模型安全评估;代码世界模型风险分级*

评估Meta公司代码世界模型在潜在风险领域的安全性
测试表明模型未新增前沿风险故开放权重发布

---

# Agentic AI Systems Should Be Designed as Marginal Token Allocators

**【智能体按边际成本分配算力】**

**arXiv**: https://arxiv.org/abs/2605.01214  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2605.01214  
**HF Paper**: https://hf-mirror.com/papers/2605.01214  
**HF Votes**: 1

## 简要摘要

*人工智能系统;智能体系统;计算资源分配*

当前AI系统各层级在资源分配上各自为政，导致整体效率低下。
提出将智能体AI系统视为边际令牌分配经济来统一设计与评估，并分析了四层经济结构及其共享的一阶条件，指出了常见失败模式和未来研究方向。

---

# Hallucinations Undermine Trust; Metacognition is a Way Forward

**【大模型幻觉与信任问题研究】**

**arXiv**: https://arxiv.org/abs/2605.01428  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2605.01428  
**HF Paper**: https://hf-mirror.com/papers/2605.01428  
**HF Votes**: 9

## 简要摘要

*自然语言处理;语言模型可靠性;幻觉检测与校准*

尽管生成式AI在事实可靠性上取得进展，但幻觉问题仍是其应用于复杂场景时的重大隐患，根源在于模型难以区分已知与未知。
论文提出通过实现“忠实的不确定性”这一元认知能力，使模型能诚实表达内在不确定性，从而在保持实用性的同时建立信任。

---

# Linear-Time Global Visual Modeling without Explicit Attention

**【用动态参数实现线性全局建模】**

**arXiv**: https://arxiv.org/abs/2605.01711  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2605.01711  
**HF Paper**: https://hf-mirror.com/papers/2605.01711  
**HF Votes**: 1

## 简要摘要

*计算机视觉;视觉模型架构;全局序列建模*

现有研究多将Transformer的全局序列建模能力归因于显式注意力计算，但该过程存在二次复杂度瓶颈。
本文提出将注意力数学重构为带动态参数的MLP，通过设计多种动态参数预测策略并集成到标准网络层，实现了线性复杂度下的高效全局建模。

---

# Counting as a minimal probe of language model reliability

**【大型语言模型可靠性的计数测试】**

**arXiv**: https://arxiv.org/abs/2605.02028  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2605.02028  
**HF Paper**: https://hf-mirror.com/papers/2605.02028  
**HF Votes**: 2

## 简要摘要

*自然语言处理;语言模型评估;模型逻辑推理可靠性*

当前大型语言模型在多项任务上表现优异，但其遵循规则的能力是否可靠尚不明确。
研究者通过计数符号的简单测试，发现模型的规则遵循能力有限，依赖于类似“数手指”的有限内部状态。

---

# T^2PO: Uncertainty-Guided Exploration Control for Stable Multi-Turn Agentic Reinforcement Learning

**【不确定性引导多轮智能体强化学习探索】**

**arXiv**: https://arxiv.org/abs/2605.02178  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2605.02178  
**HF Paper**: https://hf-mirror.com/papers/2605.02178  
**HF Votes**: 4

## 简要摘要

*强化学习;智能体强化学习;多轮交互探索稳定性*

多轮强化学习提升大模型复杂交互任务性能，但探索效率低下导致训练不稳定
提出T^2PO框架，通过令牌和回合级不确定性监控干预，动态控制探索提升稳定性与性能

---

# PhysicianBench: Evaluating LLM Agents in Real-World EHR Environments

**【评估大模型在真实电子病历中的诊疗能力】**

**arXiv**: https://arxiv.org/abs/2605.02240  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2605.02240  
**HF Paper**: https://hf-mirror.com/papers/2605.02240  
**HF Votes**: 6

## 简要摘要

*自然语言处理;智能体与多智能体系统;医疗智能体评估*

现有医疗智能体基准难以评估其在实际临床环境中的长流程、复合任务执行能力。
构建了基于真实电子病历环境和病例的基准PhysicianBench，用于评估大模型代理在跨科室、多步骤临床任务中的表现。

---

# AcademiClaw: When Students Set Challenges for AI Agents

**【学生为AI智能体设难题  】**

**arXiv**: https://arxiv.org/abs/2605.02661  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2605.02661  
**HF Paper**: https://hf-mirror.com/papers/2605.02661  
**HF Votes**: 8

## 简要摘要

*机器学习;智能体评测;学术任务评测  *

现有评测仅关注助手级任务，缺乏对AI智能体处理真实学术任务能力的评估。  
构建了学生提交的复杂学术任务评测集，通过多维度评估方法测试前沿模型，发现其能力存在明显局限。

---

# Perceptual Flow Network for Visually Grounded Reasoning

**【视觉推理的感知流网络  】**

**arXiv**: https://arxiv.org/abs/2605.02730  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2605.02730  
**HF Paper**: https://hf-mirror.com/papers/2605.02730  
**HF Votes**: 2

## 简要摘要

*多模态学习;视觉语言模型;视觉可靠性提升  *

现有视觉语言模型因缺乏视觉约束而存在语言偏见和幻觉问题。  
本文提出感知流网络，通过解耦感知与推理、引入多维奖励和变分强化学习，提升模型的视觉可靠性和推理性能。

---

# MolmoAct2: Action Reasoning Models for Real-world Deployment

**【开放机器人通用控制模型】**

**arXiv**: https://arxiv.org/abs/2605.02881  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2605.02881  
**HF Paper**: https://hf-mirror.com/papers/2605.02881  
**HF Votes**: 160

## 简要摘要

*机器人;具身智能;视觉语言动作模型*

当前机器人通用控制模型在可部署性上存在诸多不足。
本文提出了一个开放、高效的机器人动作推理模型，通过专用骨干、新数据集、新分词器、新架构和动态推理优化了性能。

---
