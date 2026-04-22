# 2026-04-22 全量简报

# Accurate and scalable exchange-correlation with deep learning

**【深度学习提升密度泛函精度】**

**arXiv**: https://arxiv.org/abs/2506.14665  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2506.14665  
**HF Paper**: https://huggingface.co/papers/2506.14665  
**HF Votes**: 2

## 简要摘要

*计算化学;密度泛函理论;交换相关泛函*

密度泛函理论(DFT)的预测可靠性受限于其对未知交换相关泛函的近似，传统方法难以兼顾精度与效率。
本研究开发了深度学习交换相关泛函Skala，在保持半局部计算成本的同时，精度超越主流杂化泛函，为第一性原理模拟提供了更优方案。

---

# Predicting integers from continuous parameters

**【预测整数型标签的离散分布建模】**

**arXiv**: https://arxiv.org/abs/2602.10751  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2602.10751  
**HF Paper**: https://huggingface.co/papers/2602.10751  
**HF Votes**: 1

## 简要摘要

*机器学习;深度学习;整数回归*

研究如何直接为整数值标签建模离散分布，而非将其视为连续值进行传统回归。
提出了多种可微离散分布，其中比特位伯努利分布和离散拉普拉斯分布在多个任务上表现最佳。

---

# AgentSPEX: An Agent SPecification and EXecution Language

**【提出语言模型智能体工作流规范与执行语言  】**

**arXiv**: https://arxiv.org/abs/2604.13346  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.13346  
**HF Paper**: https://huggingface.co/papers/2604.13346  
**HF Votes**: 45

## 简要摘要

*大语言模型应用;智能体系统;工作流规范与执行  *

现有语言模型智能体系统依赖隐式的反应式提示，或与Python代码紧耦合，使其行为难以控制和维护。  
我们提出了AgentSPEX语言，用于显式、模块化地定义智能体工作流，并提供配套的可执行环境、可视化编辑器及现成智能体，经评测证明其有效性与可用性。

---

# Target-Oriented Pretraining Data Selection via Neuron-Activated Graph

**【目标导向预训练数据选择】**

**arXiv**: https://arxiv.org/abs/2604.15706  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.15706  
**HF Paper**: https://huggingface.co/papers/2604.15706  
**HF Votes**: 6

## 简要摘要

*自然语言处理;语言模型预训练;预训练数据选择*

日常任务皆有目标，围绕目标预训练模型能使其成为专家
我们提出基于神经元激活图的无训练数据选择方法提升目标导向预训练效果

---

# Mind's Eye: A Benchmark of Visual Abstraction, Transformation and Composition for Multimodal LLMs

**【构建多模态大模型视觉推理评测基准】**

**arXiv**: https://arxiv.org/abs/2604.16054  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.16054  
**HF Paper**: https://huggingface.co/papers/2604.16054  

## 简要摘要

*多模态学习;视觉语言理解;视觉推理能力评测*

多模态大语言模型在视觉语言任务上进步显著，但其视觉认知与空间推理能力尚不明确。
为评估该能力，本文提出了Mind's Eye基准，包含八项任务，测试发现当前模型表现远逊于人类。

---

# Chain-of-Thought Degrades Visual Spatial Reasoning Capabilities of Multimodal LLMs

**【链式思维损害多模态大模型视觉空间推理】**

**arXiv**: https://arxiv.org/abs/2604.16060  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.16060  
**HF Paper**: https://huggingface.co/papers/2604.16060  

## 简要摘要

*多模态人工智能;视觉语言推理;视觉空间推理评估*

多模态推理模型广泛使用链式思维方法提升数理逻辑解题能力，但其在视觉空间推理任务上的有效性受到质疑。
该研究评估了十七个模型在十三个空间基准上的表现，发现链式思维提示会降低视觉空间推理性能，并揭示了模型存在严重的捷径学习和幻觉问题。

---

# The Cognitive Penalty: Ablating System 1 and System 2 Reasoning in Edge-Native SLMs for Decentralized Consensus

**【SLMs推理机制对DAO共识影响评估】**

**arXiv**: https://arxiv.org/abs/2604.16913  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.16913  
**HF Paper**: https://huggingface.co/papers/2604.16913  

## 简要摘要

*自然语言处理;语言模型与推理;去中心化共识系统*

在去中心化自治组织中，需要评估小型语言模型在对抗性治理环境中作为防火墙时的推理机制选择。
通过实验发现，直觉式推理比深度思考在速度、稳定性和安全性上更具优势。

---

# Understanding and Enforcing Weight Disentanglement in Task Arithmetic

**【正交正则化增强任务算术性能】**

**arXiv**: https://arxiv.org/abs/2604.17078  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.17078  
**HF Paper**: https://huggingface.co/papers/2604.17078  
**HF Votes**: 4

## 简要摘要

*机器学习;模型编辑;任务算术*

任务算术是一种高效的免训练模型编辑方法，但其成功缺乏理论解释，且理想的“权重解缠”特性难以直接控制。
本文提出任务特征专业化是权重解缠的根源，并由此推导出权重正交性这一可优化代理目标，进而设计了正交正则化方法来主动塑造权重更新，以促进解缠并提升任务算术效果。

---

# Code-Switching Information Retrieval: Benchmarks, Analysis, and the Limits of Current Retrievers

**【代码切换信息检索性能研究】**

**arXiv**: https://arxiv.org/abs/2604.17632  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.17632  
**HF Paper**: https://huggingface.co/papers/2604.17632  
**HF Votes**: 7

## 简要摘要

*自然语言处理;信息检索;多语言混合检索*

现代信息检索系统主要针对单语设计，但语言混合现象在沟通中普遍存在
构建混合语言检索数据集，分析现有模型性能瓶颈并揭示其嵌入空间差异

---

# Contrastive Attribution in the Wild: An Interpretability Analysis of LLM Failures on Realistic Benchmarks

**【分析大模型失败归因】**

**arXiv**: https://arxiv.org/abs/2604.17761  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.17761  
**HF Paper**: https://huggingface.co/papers/2604.17761  
**HF Votes**: 2

## 简要摘要

*自然语言处理;大语言模型;失败归因分析*

现有可解释性工具多关注简单场景，对大模型在真实基准测试中失败的分析不足。
本研究提出对比归因方法，系统分析了多种真实测试中模型失败时的内部模式与局限性。

---

# Mitigating Multimodal Hallucination via Phase-wise Self-reward

**【为视觉大模型自动奖励降幻觉】**

**arXiv**: https://arxiv.org/abs/2604.17982  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.17982  
**HF Paper**: https://huggingface.co/papers/2604.17982  
**HF Votes**: 1

## 简要摘要

*多模态学习;视觉语言模型;幻觉缓解*

大型视觉语言模型仍存在生成内容与视觉输入不一致的幻觉问题。
我们提出一个分阶段自奖励解码框架，用轻量奖励模型在线指导解码，动态抑制幻觉。

---

# MM-JudgeBias: A Benchmark for Evaluating Compositional Biases in MLLM-as-a-Judge

**【多模态大模型自动评测偏差基准】**

**arXiv**: https://arxiv.org/abs/2604.18164  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.18164  
**HF Paper**: https://huggingface.co/papers/2604.18164  
**HF Votes**: 3

## 简要摘要

*多模态内容理解与生成;大模型评测;多模态评测中的组合偏差*

多模态大模型被用作自动评测工具，但其可靠性和偏见风险研究不足。
定义了多模态评测中的组合偏差，构建了包含1800+样本的基准MM-JudgeBias，并评估了26个模型。

---

# AJ-Bench: Benchmarking Agent-as-a-Judge for Environment-Aware Evaluation

**【评估智能体作为裁判能力】**

**arXiv**: https://arxiv.org/abs/2604.18240  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.18240  
**HF Paper**: https://huggingface.co/papers/2604.18240  
**HF Votes**: 8

## 简要摘要

*强化学习;智能体评估;环境感知评测*

随着智能体训练规模扩大，复杂环境中可靠验证行为变得困难，现有方法泛化性不足。
提出了AJ-Bench基准，在三个领域评估智能体裁判的信息获取与验证能力，实验显示其优于基线并揭示了挑战。

---

# SPRITE: From Static Mockups to Engine-Ready Game UI

**【游戏界面截图转可编辑资源】**

**arXiv**: https://arxiv.org/abs/2604.18591  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.18591  
**HF Paper**: https://huggingface.co/papers/2604.18591  

## 简要摘要

*计算机图形学;用户界面生成;游戏界面重建*

当前截图转代码工具难以处理游戏UI不规则布局和深层嵌套。
SPRITE结合视觉语言模型与YAML中间表示，自动重建复杂游戏UI并提升开发效率。

---

# Dual-View Training for Instruction-Following Information Retrieval

**【指令遵循检索的双视图训练】**

**arXiv**: https://arxiv.org/abs/2604.18845  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.18845  
**HF Paper**: https://huggingface.co/papers/2604.18845  
**HF Votes**: 7

## 简要摘要

*自然语言处理;信息检索;指令遵循信息检索*

现有检索器主要关注语义相关性，难以区分符合查询主题和满足用户指令的文档，导致在指令遵循信息检索任务上表现不佳。
提出一种基于极性反转的双视图数据合成方法，通过大语言模型生成互补指令来交换文档间的相关性标签，迫使检索模型关注指令本身，从而显著提升了指令遵循的检索性能。

---

# ClawNet: Human-Symbiotic Agent Network for Cross-User Autonomous Cooperation

**【构建跨用户协作的智能体网络】**

**arXiv**: https://arxiv.org/abs/2604.19211  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.19211  
**HF Paper**: https://huggingface.co/papers/2604.19211  
**HF Votes**: 1

## 简要摘要

*智能体系统；人机协作；身份治理代理*

现有AI代理框架服务于单用户，缺乏跨用户代理协作的基础设施与治理机制。
提出人机共生代理范式与ClawNet框架，通过分层身份、范围授权和行动问责实现安全的跨用户代理协作。

---

# ShadowPEFT: Shadow Network for Parameter-Efficient Fine-Tuning

**【阴影网络实现高效微调】**

**arXiv**: https://arxiv.org/abs/2604.19254  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.19254  
**HF Paper**: https://huggingface.co/papers/2604.19254  
**HF Votes**: 12

## 简要摘要

*自然语言处理;大型语言模型微调;参数高效微调*

背景/任务：为降低大语言模型的全参数微调成本，参数高效微调方法仅训练少量参数，但现有方法（如LoRA）的局部参数化适配方式存在局限。
做了什么：提出了一个名为ShadowPEFT的集中式框架，通过一个跨层共享的阴影模块进行层级的隐状态精炼，实现了从分布式权重扰动到集中式层空间精炼的转变，在多种任务上达到或超越了现有方法的性能。

---

# TEMPO: Scaling Test-time Training for Large Reasoning Models

**【推理模型测试时训练优化】**

**arXiv**: https://arxiv.org/abs/2604.19295  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.19295  
**HF Paper**: https://huggingface.co/papers/2604.19295  
**HF Votes**: 19

## 简要摘要

*自然语言处理;大型语言模型;测试时训练优化*

现有推理模型测试时训练方法易陷入性能瓶颈与多样性丧失
提出TEMPO框架，通过策略精炼与奖励信号周期性校准实现持续改进

---

# Evaluation-driven Scaling for Scientific Discovery

**【简单评估扩展框架推进科学发现】**

**arXiv**: https://arxiv.org/abs/2604.19341  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.19341  
**HF Paper**: https://huggingface.co/papers/2604.19341  
**HF Votes**: 1

## 简要摘要

*自然语言处理;大语言模型应用;评估驱动科学发现循环*

语言模型在科学发现中用于生成假设和方案，但如何高效扩展基于评估的迭代发现循环是未明确解决的难题。
本文提出SimpleTES框架，通过并行探索与反馈优化，在多个科学问题上发现超越前沿模型的解决方案，并能利用成功轨迹训练模型提升泛化能力。

---

# LoopCTR: Unlocking the Loop Scaling Power for Click-Through Rate Prediction

**【循环缩放提升点击率预测性能】**

**arXiv**: https://arxiv.org/abs/2604.19550  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.19550  
**HF Paper**: https://huggingface.co/papers/2604.19550  
**HF Votes**: 3

## 简要摘要

*机器学习;推荐系统;点击率预测*

基于Transformer的点击率预测模型扩大规模时，参数量增长会带来巨大的计算和存储开销，与工业部署的严苛约束产生矛盾。
提出LoopCTR，通过递归共享模型层的循环缩放范式，将计算与参数增长解耦，并采用增强结构和过程监督，实现了训练多循环、推理零循环的高效模型。

---

# Chat2Workflow: A Benchmark for Generating Executable Visual Workflows with Natural Language

**【用自然语言生成可执行视觉工作流】**

**arXiv**: https://arxiv.org/abs/2604.19667  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.19667  
**HF Paper**: https://huggingface.co/papers/2604.19667  
**HF Votes**: 12

## 简要摘要

*自然语言处理;任务导向对话;工作流自动生成*

当前可执行视觉工作流的构建依赖高成本、易出错的手工开发，研究能否用大语言模型自动化此过程。
本文提出了Chat2Workflow基准和代理框架来直接从自然语言生成可部署的工作流，实验表明现有模型在复杂需求下仍面临挑战。

---

# PlayCoder: Making LLM-Generated GUI Code Playable

**【大语言模型生成可玩GUI代码】**

**arXiv**: https://arxiv.org/abs/2604.19742  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.19742  
**HF Paper**: https://huggingface.co/papers/2604.19742  
**HF Votes**: 18

## 简要摘要

*程序生成;图形用户界面;交互式应用评测*

现有大模型生成图形界面应用的能力研究不足，评测方法不完善。
提出了新评测基准、指标和测试工具，并设计了一个能修复错误的生成框架。

---
