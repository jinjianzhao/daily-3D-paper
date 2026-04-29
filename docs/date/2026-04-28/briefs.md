# 2026-04-28 全量简报

# For-Value: Efficient Forward-Only Data Valuation for finetuning LLMs and VLMs

**【高效估值大模型微调数据】**

**arXiv**: https://arxiv.org/abs/2508.10180  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2508.10180  
**HF Paper**: https://hf-mirror.com/papers/2508.10180  
**HF Votes**: 16

## 简要摘要

*机器学习;数据估值;大模型数据价值评估*

数据估值对提升大模型透明度与问责制至关重要，但现有依赖梯度的方法计算成本极高。
本文提出仅需前向传播即可高效批量估算数据价值的框架，在多项任务中表现优异且效率显著提升。

---

# Why Fine-Tuning Encourages Hallucinations and How to Fix It

**【微调如何导致幻觉及解决】**

**arXiv**: https://arxiv.org/abs/2604.15574  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.15574  
**HF Paper**: https://hf-mirror.com/papers/2604.15574  
**HF Votes**: 17

## 简要摘要

*自然语言处理;语言模型微调;幻觉缓解*

大语言模型在微调时容易产生事实性幻觉，这是知识遗忘或干扰所致。
提出自蒸馏微调法和冻结参数法来减轻幻觉，并验证了语义表征干扰是主因。

---

# Disentangled Robot Learning via Separate Forward and Inverse Dynamics Pretraining

**【分离机器人视觉前向逆动力学预训练】**

**arXiv**: https://arxiv.org/abs/2604.16391  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.16391  
**HF Paper**: https://hf-mirror.com/papers/2604.16391  
**HF Votes**: 1

## 简要摘要

*机器人;机器人学习;视觉语言动作模型*

视觉语言动作模型在构建通用机器人时面临二维图像预测与三维动作预测不匹配的困境。
提出DeFI框架，分别预训练前向与逆动力学模型以利用不同数据源，再整合微调，在多个基准测试中实现领先性能。

---

# Towards Understanding the Robustness of Sparse Autoencoders

**【稀疏自编码器增强大模型抗攻击性】**

**arXiv**: https://arxiv.org/abs/2604.18756  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.18756  
**HF Paper**: https://hf-mirror.com/papers/2604.18756  
**HF Votes**: 2

## 简要摘要

*大语言模型安全;对抗攻击与防御;稀疏自编码器鲁棒性研究*

大语言模型易受基于梯度的越狱攻击，而用于可解释性的稀疏自编码器（SAE）的鲁棒性尚未被充分研究。
本研究通过在推理时将预训练SAE集成到大模型的残差流中，显著降低了多种攻击的成功率，并探究了稀疏度与层位置对防御效果和模型性能的影响。

---

# Taming Actor-Observer Asymmetry in Agents via Dialectical Alignment

**【减少多智能体角色偏见】**

**arXiv**: https://arxiv.org/abs/2604.19548  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.19548  
**HF Paper**: https://hf-mirror.com/papers/2604.19548  
**HF Votes**: 14

## 简要摘要

*自然语言处理;多智能体系统;行为者-观察者不对称*

大型语言模型智能体在角色扮演中会出现行为者-观察者不对称的认知偏差，影响其可靠性。
提出通过辩证对齐训练的ReTAS方法，能合成矛盾观点以减轻偏见，提升模糊场景的故障解决率。

---

# How Much Is One Recurrence Worth? Iso-Depth Scaling Laws for Looped Language Models

**【循环语言模型深度循环等效参数标度律】**

**arXiv**: https://arxiv.org/abs/2604.21106  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.21106  
**HF Paper**: https://hf-mirror.com/papers/2604.21106  
**HF Votes**: 5

## 简要摘要

*自然语言处理;语言模型;循环模型标度律*

研究循环语言模型增加循环次数带来的性能提升，需要量化其相当于增加多少唯一参数。
通过大量训练实验拟合出包含循环等价指数φ的联合标度律，发现φ约为0.46，并验证其作为评估工具可区分训练技巧带来的真实能力提升与计算增益。

---

# Efficient Agent Evaluation via Diversity-Guided User Simulation

**【高效评估对话智能体】**

**arXiv**: https://arxiv.org/abs/2604.21480  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.21480  
**HF Paper**: https://hf-mirror.com/papers/2604.21480  
**HF Votes**: 13

## 简要摘要

*自然语言处理;语言模型评估;用户模拟*

当前对大型语言模型作为客服智能体的评估方法效率低且难以发现深层故障。
提出DIVERT框架，通过状态快照复用与多样化用户响应分支，系统探索交互路径以提升评估效率与覆盖率。

---

# Sapiens2

**【高分辨率人体视觉通用模型  】**

**arXiv**: https://arxiv.org/abs/2604.21681  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.21681  
**HF Paper**: https://hf-mirror.com/papers/2604.21681  
**HF Votes**: 12

## 简要摘要

*计算机视觉;人体视觉;高分辨率人体图像理解  *

本文聚焦于构建具备强泛化、多用途和高保真输出能力的人体中心视觉模型。  
我们提出了Sapiens2模型系列，通过结合掩码图像重建与自蒸馏对比目标进行预训练，并在十亿级高质量人体图像数据及改进的标注上进行训练，在姿态估计、部件分割等多个任务上取得了显著性能提升。

---

# From Skills to Talent: Organising Heterogeneous Agents as a Real-World Company

**【构建自组织多智能体公司系统】**

**arXiv**: https://arxiv.org/abs/2604.22446  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.22446  
**HF Paper**: https://hf-mirror.com/papers/2604.22446  
**HF Votes**: 110

## 简要摘要

*智能体系统;多智能体协作;智能体组织架构*

当前多智能体系统受限于固定团队结构和紧耦合协调逻辑，缺乏能动态组建、治理和改进智能体工作队伍的组织层。
提出OneManCompany框架，通过可移植的Talent封装技能、Talent市场动态招募、以及探索-执行-审查树搜索统一规划执行与评估，将多智能体系统提升为能自适应开放任务的自组织AI组织。

---

# Stochastic KV Routing: Enabling Adaptive Depth-Wise Cache Sharing

**【自适应共享KV缓存优化大模型推理】**

**arXiv**: https://arxiv.org/abs/2604.22782  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.22782  
**HF Paper**: https://hf-mirror.com/papers/2604.22782  
**HF Votes**: 4

## 简要摘要

*自然语言处理;大模型推理优化;KV缓存深度共享*

背景/任务是降低大语言模型推理时KV缓存的内存开销。
提出了一种名为随机跨层注意力的训练方法，使模型能适应深度维度的KV缓存共享，从而在不损失性能的前提下显著减少内存占用。

---

# ATTN-FIQA: Interpretable Attention-based Face Image Quality Assessment with Vision Transformers

**【用注意力评估人脸图像质量  】**

**arXiv**: https://arxiv.org/abs/2604.22841  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.22841  
**HF Paper**: https://hf-mirror.com/papers/2604.22841  
**HF Votes**: 3

## 简要摘要

*计算机视觉;生物特征识别;人脸图像质量评估  *

人脸图像质量评估任务旨在判断人脸图像对识别系统的可用性。  
本研究提出一种免训练方法，利用预训练视觉变换器的注意力分数作为人脸图像质量指标。

---

# EX-FIQA: Leveraging Intermediate Early eXit Representations from Vision Transformers for Face Image Quality Assessment

**【利用中间层提升人脸质量评估  】**

**arXiv**: https://arxiv.org/abs/2604.22842  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.22842  
**HF Paper**: https://hf-mirror.com/papers/2604.22842  
**HF Votes**: 2

## 简要摘要

*计算机视觉;人脸识别;人脸图像质量评估  *

现有基于视觉变换器的人脸质量评估方法仅依赖最终层特征，忽略了中间层的质量信息。  
系统分析了视觉变换器中所有中间层的作用，提出无需修改架构的分数融合框架，在保持性能的同时显著降低计算成本。

---

# SketchVLM: Vision language models can annotate images to explain thoughts and guide users

**【让视觉语言模型在图上标注解释】**

**arXiv**: https://arxiv.org/abs/2604.22875  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.22875  
**HF Paper**: https://hf-mirror.com/papers/2604.22875  
**HF Votes**: 27

## 简要摘要

*计算机视觉;视觉问答;视觉推理与标注*

现有视觉语言模型仅用文本回答图像问题，用户难以验证其推理过程。
提出SketchVLM框架，让模型能在输入图像上生成可编辑的SVG标注，以视觉方式解释答案，提升了多个视觉推理任务的准确性和标注质量。

---

# TexOCR: Advancing Document OCR Models for Compilable Page-to-LaTeX Reconstruction

**【优化文档OCR生成可编译LaTeX  】**

**arXiv**: https://arxiv.org/abs/2604.22880  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.22880  
**HF Paper**: https://hf-mirror.com/papers/2604.22880  
**HF Votes**: 7

## 简要摘要

*文档智能;光学字符识别与理解;科学文档LaTeX重建  *

现有文档OCR主要关注提取纯文本或Markdown格式，忽略了LaTeX在科学出版中至关重要的结构与可编译特性。  
我们构建了包含评测基准与训练数据集的TexOCR系统，通过监督微调和基于可验证奖励的强化学习训练模型，显著提升了科学PDF到可编译LaTeX的重建质量。

---

# ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation

**【高效评估生成式AI模型性能】**

**arXiv**: https://arxiv.org/abs/2604.23099  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23099  
**HF Paper**: https://hf-mirror.com/papers/2604.23099  
**HF Votes**: 2

## 简要摘要

*机器学习;生成模型评估;主动式性能估计与故障发现*

生成式AI模型评估因推理慢、标注贵、模型与基准快速增加而日益耗费资源。
提出主动评估框架ProEval，通过迁移学习和贝叶斯求积高效估计性能并主动发现故障，理论证明其无偏有界，实验显示其样本效率显著优于基线。

---

# Discovering Agentic Safety Specifications from 1-Bit Danger Signals

**【大模型从稀疏危险信号学安全规则】**

**arXiv**: https://arxiv.org/abs/2604.23210  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23210  
**HF Paper**: https://hf-mirror.com/papers/2604.23210  
**HF Votes**: 2

## 简要摘要

*强化学习;智能体安全;稀疏反馈安全性*

背景/任务：研究大语言模型智能体能否仅通过稀疏的二进制危险信号（而非丰富反馈）来发现隐藏的安全约束。
做了什么：提出了EPO-Safe框架，让智能体通过反思从危险信号中演化出可读的安全规范，并在网格世界和文本场景中验证了其有效性，发现仅基于奖励的反思会损害安全。

---

# IndustryAssetEQA: A Neurosymbolic Operational Intelligence System for Embodied Question Answering in Industrial Asset Maintenance

**【工业资产问答神经符号系统】**

**arXiv**: https://arxiv.org/abs/2604.23446  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23446  
**HF Paper**: https://hf-mirror.com/papers/2604.23446  
**HF Votes**: 1

## 简要摘要

*操作智能；具身问答；工业资产维护*

工业维护需要AI助手，但现有大模型解释模糊、缺乏可验证依据。
我们结合时序数据与知识图谱，构建了可验证、支持反事实推理的维护问答系统。

---

# Personality Shapes Gender Bias in Persona-Conditioned LLM Narratives Across English and Hindi: An Empirical Investigation

**【人格特质影响大语言模型性别偏见  】**

**arXiv**: https://arxiv.org/abs/2604.23600  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23600  
**HF Paper**: https://hf-mirror.com/papers/2604.23600  

## 简要摘要

*自然语言处理;社会偏见分析;人格条件化文本生成  *

背景/任务是研究在人格设定下大语言模型生成文本中的性别偏见问题。  
我们让多个大模型生成了大量故事，发现人格特质会显著改变性别偏见的程度和方向，且黑暗人格特质会强化刻板印象。

---

# Learning to Identify Out-of-Distribution Objects for 3D LiDAR Anomaly Segmentation

**【3D激光雷达异常物体分割】**

**arXiv**: https://arxiv.org/abs/2604.23604  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23604  
**HF Paper**: https://hf-mirror.com/papers/2604.23604  
**HF Votes**: 4

## 简要摘要

*自动驾驶感知;三维点云理解;异常物体分割*

在自动驾驶中，识别三维点云中未知的异常物体是关键任务。
我们提出一种直接在特征空间建模的方法，并构建了混合数据集来提升性能。

---

# RaV-IDP: A Reconstruction-as-Validation Framework for Faithful Intelligent Document Processing

**【文档处理重建验证框架】**

**arXiv**: https://arxiv.org/abs/2604.23644  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23644  
**HF Paper**: https://hf-mirror.com/papers/2604.23644  
**HF Votes**: 2

## 简要摘要

*文档智能;信息抽取;抽取结果验证*

现有智能文档处理流程提取文档实体但缺乏验证其是否忠实于原文档的内在机制
提出重建验证框架，通过将抽取结果重建并与原文档区域比较来提供保真度分数，分数过低时触发结构化大模型回退并重复验证循环

---

# PageGuide: Browser extension to assist users in navigating a webpage and locating information

**【浏览器插件助用户浏览网页定位信息】**

**arXiv**: https://arxiv.org/abs/2604.23772  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23772  
**HF Paper**: https://hf-mirror.com/papers/2604.23772  
**HF Votes**: 5

## 简要摘要

*人机交互;智能用户界面;网页信息导航*

用户常难以在杂乱网页中快速定位信息、完成多步任务并保持专注，现有AI助手和浏览器代理无法直观展示信息来源。
我们开发了PageGuide浏览器扩展，通过视觉叠加将LLM回答直接锚定在网页DOM中，提供查找、引导和隐藏功能，有效提升信息查找准确性、任务完成率和专注度。

---

# Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms

**【视觉语言动作模型安全综述】**

**arXiv**: https://arxiv.org/abs/2604.23775  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23775  
**HF Paper**: https://hf-mirror.com/papers/2604.23775  
**HF Votes**: 42

## 简要摘要

*机器人;机器人安全;视觉语言动作模型安全*

背景/任务：视觉语言动作模型作为具身智能的统一基础，带来了新的安全挑战，但相关研究分散。
做了什么：本文从攻击、防御、评估与部署四个维度，按攻击与防御的时间轴系统梳理了该领域的安全威胁、对策、评估方法与部署挑战，并指出了关键开放问题。

---

# ClawMark: A Living-World Benchmark for Multi-Turn, Multi-Day, Multimodal Coworker Agents

**【构建多模态长期协作智能体评测基准】**

**arXiv**: https://arxiv.org/abs/2604.23781  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23781  
**HF Paper**: https://hf-mirror.com/papers/2604.23781  
**HF Votes**: 30

## 简要摘要

*自然语言处理;智能体评测;长期多模态任务评测*

现有基准难以评估在多日多模态动态环境中工作的智能体
我们提出了一个包含多日任务和动态沙盒环境的基准，并评估了多个前沿系统

---

# Stabilizing Efficient Reasoning with Step-Level Advantage Selection

**【提升大模型推理效率  】**

**arXiv**: https://arxiv.org/abs/2604.24003  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24003  
**HF Paper**: https://hf-mirror.com/papers/2604.24003  
**HF Votes**: 5

## 简要摘要

*自然语言处理;大语言模型推理;高效推理方法  *

大型语言模型推理需大量计算且生成过长推理链，现有高效推理方法常受限短上下文微调，导致训练不稳定与精度下降。  
提出步级优势选择方法，通过筛选高置信度推理步实现更优精度与长度平衡，在数学与通用推理基准上提升准确率并缩短推理长度。

---

# Improving Robustness of Tabular Retrieval via Representational Stability

**【提升表格检索抗干扰能力】**

**arXiv**: https://arxiv.org/abs/2604.24040  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24040  
**HF Paper**: https://hf-mirror.com/papers/2604.24040  
**HF Votes**: 1

## 简要摘要

*自然语言处理;信息检索;表格检索稳定性*

表格语义不变时，不同序列化格式仍会导致检索结果不稳定。
通过中心表征和轻量适配器抑制格式扰动，提升多格式下表格检索的鲁棒性。

---

# Credal Concept Bottleneck Models for Epistemic-Aleatoric Uncertainty Decomposition

**【概念瓶颈模型不确定性分解】**

**arXiv**: https://arxiv.org/abs/2604.24170  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24170  
**HF Paper**: https://hf-mirror.com/papers/2604.24170  

## 简要摘要

*可信推理;可解释人工智能;概念不确定性分解*

概念瓶颈模型通过可解释概念预测，但其点估计概念概率混合了认知不确定性和偶然不确定性，导致概念级不确定性难以解释和决策。
我们提出CREDENCE框架，将概念表示为概率区间，通过不同概念头间的差异分离认知不确定性，并训练专门输出估计偶然不确定性，从而支持自动化、数据收集和人工审查等决策。

---

# Rewarding the Scientific Process: Process-Level Reward Modeling for Agentic Data Analysis

**【为数据分析智能体设计过程奖励模型】**

**arXiv**: https://arxiv.org/abs/2604.24198  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24198  
**HF Paper**: https://hf-mirror.com/papers/2604.24198  
**HF Votes**: 17

## 简要摘要

*自然语言处理;智能体与交互系统;数据分析过程奖励建模*

现有过程奖励模型在动态数据分析任务中表现不佳，难以发现隐蔽错误并误判探索行为。
本文提出了环境感知的过程奖励模型DataPRM，能主动验证、区分错误类型，并通过新数据集和训练方法显著提升了智能体的数据分析性能。

---

# ReVSI: Rebuilding Visual Spatial Intelligence Evaluation for Accurate Assessment of VLM 3D Reasoning

**【重建视觉空间智能评估基准】**

**arXiv**: https://arxiv.org/abs/2604.24300  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24300  
**HF Paper**: https://hf-mirror.com/papers/2604.24300  
**HF Votes**: 59

## 简要摘要

*计算机视觉;视觉语言模型;三维空间推理评估*

现有视觉语言模型的空间智能评估方法存在两个主要问题：一是基于点云标注生成问答对时存在错误和歧义，二是评估常假设模型能获取完整场景，而实际模型输入仅为稀疏采样的帧。
我们提出了ReVSI基准和协议，通过重新标注381个场景的对象与几何信息，并基于模型实际可获取的帧生成可靠的问答对，以提供更准确、可控的视觉空间推理评估。

---

# Improving Vision-language Models with Perception-centric Process Reward Models

**【提升视觉语言模型感知精度】**

**arXiv**: https://arxiv.org/abs/2604.24583  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24583  
**HF Paper**: https://hf-mirror.com/papers/2604.24583  
**HF Votes**: 1

## 简要摘要

*计算机视觉;视觉语言模型;过程奖励模型*

现有视觉语言模型依赖结果级奖励信号，难以诊断和纠正推理链中的感知错误。
提出感知中心过程奖励模型，在训练中提供细粒度监督信号并在推理中实现测试时扩展。

---

# Quantum Kernel Advantage over Classical Collapse in Medical Foundation Model Embeddings

**【量子核在医学图像分类中的优势】**

**arXiv**: https://arxiv.org/abs/2604.24597  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24597  
**HF Paper**: https://hf-mirror.com/papers/2604.24597  

## 简要摘要

*机器学习;核方法;量子支持向量机*

研究量子支持向量机在医学影像嵌入分类任务中的潜力。
在公平对比下，量子核在多项指标上显著优于经典线性核，并分析了其高有效秩的特性。

---

# OmniShotCut: Holistic Relational Shot Boundary Detection with Shot-Query Transformer

**【用Transformer检测视频镜头边界】**

**arXiv**: https://arxiv.org/abs/2604.24762  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24762  
**HF Paper**: https://hf-mirror.com/papers/2604.24762  
**HF Votes**: 9

## 简要摘要

*计算机视觉;视频理解;镜头边界检测*

现有镜头边界检测方法存在边界不明确、漏检等问题，且依赖有噪声的标注和过时的基准。
提出OmniShotCut方法，通过基于镜头查询的Transformer联合预测镜头内与镜头间关系，并构建了合成数据管道和新基准进行评测。

---
