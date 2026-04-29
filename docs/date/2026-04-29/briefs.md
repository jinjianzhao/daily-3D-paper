# 2026-04-29 全量简报

# For-Value: Efficient Forward-Only Data Valuation for finetuning LLMs and VLMs

**【高效前向数据估值框架】**

**arXiv**: https://arxiv.org/abs/2508.10180  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2508.10180  
**HF Paper**: https://hf-mirror.com/papers/2508.10180  
**HF Votes**: 12

## 简要摘要

*机器学习;数据估值;大模型数据价值评估*

现有数据估值方法依赖梯度计算，在大模型上计算成本高且难以批量并行
本文提出仅需单次前向传播的闭式估值方法，在保持效果的同时显著提升效率

---

# Disentangled Robot Learning via Separate Forward and Inverse Dynamics Pretraining

**【分离训练机器人视觉与动作模型】**

**arXiv**: https://arxiv.org/abs/2604.16391  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.16391  
**HF Paper**: https://hf-mirror.com/papers/2604.16391  
**HF Votes**: 1

## 简要摘要

*机器人;机器人学习;视觉语言动作模型*

视觉语言动作模型面临二维图像预测与三维动作预测的对齐难题，且训练方式限制了模型从无动作网络视频中学习。
提出DeFI框架，分别预训练前向和逆向动力学模型以利用不同数据源，再整合微调，在多个基准上取得了领先性能。

---

# Taming Actor-Observer Asymmetry in Agents via Dialectical Alignment

**【解决多智能体视角偏差】**

**arXiv**: https://arxiv.org/abs/2604.19548  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.19548  
**HF Paper**: https://hf-mirror.com/papers/2604.19548  
**HF Votes**: 13

## 简要摘要

*自然语言处理;大语言模型智能体;角色扮演认知偏差*

大语言模型智能体在执行复杂任务时，因扮演不同角色会产生类似人类的认知偏差，即行动者-旁观者不对称。
我们提出了ReTAS方法，通过辩证法对齐训练，引导智能体综合矛盾观点，有效缓解偏差并提升故障解决率。

---

# How Much Is One Recurrence Worth? Iso-Depth Scaling Laws for Looped Language Models

**【循环模型深度与参数效率关系】**

**arXiv**: https://arxiv.org/abs/2604.21106  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.21106  
**HF Paper**: https://hf-mirror.com/papers/2604.21106  
**HF Votes**: 5

## 简要摘要

*自然语言处理;语言模型;循环模型缩放定律*

研究循环语言模型中额外循环层对模型性能的提升效果，量化其相当于增加多少唯一参数。
通过大量实验拟合出包含循环等价指数的缩放定律，并用该指数评估不同训练策略对循环机制真实容量的影响。

---

# Efficient Agent Evaluation via Diversity-Guided User Simulation

**【高效评估AI客服的可靠性】**

**arXiv**: https://arxiv.org/abs/2604.21480  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.21480  
**HF Paper**: https://hf-mirror.com/papers/2604.21480  
**HF Votes**: 12

## 简要摘要

*自然语言处理;智能体评估;用户模拟*

当前评估大型语言模型客服效率低且难以发现深层故障
提出DIVERT框架，利用快照复用和多样性引导模拟提升评估效率与覆盖

---

# From Skills to Talent: Organising Heterogeneous Agents as a Real-World Company

**【构建动态自组织多智能体系统】**

**arXiv**: https://arxiv.org/abs/2604.22446  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.22446  
**HF Paper**: https://hf-mirror.com/papers/2604.22446  
**HF Votes**: 95

## 简要摘要

*多智能体系统;组织与协作;动态任务分解与执行*

当前多智能体系统受限于固定的团队结构、紧密耦合的协调逻辑和会话绑定学习，缺乏一个原则性的组织层。
本文提出OneManCompany框架，通过封装技能为可移植的Talent身份，利用Talent市场按需招募，并采用E²R树搜索进行组织决策，将多智能体系统提升为能够适应开放领域任务的自组织和自改进AI组织。

---

# Stochastic KV Routing: Enabling Adaptive Depth-Wise Cache Sharing

**【随机KV路由实现跨层缓存共享】**

**arXiv**: https://arxiv.org/abs/2604.22782  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.22782  
**HF Paper**: https://hf-mirror.com/papers/2604.22782  
**HF Votes**: 1

## 简要摘要

*自然语言处理;大语言模型推理;KV缓存优化*

自回归生成时KV缓存内存开销大，现有方法多在时间维度优化，深度维度潜力未充分挖掘。
提出随机跨层注意力训练法，使模型适应不同深度缓存共享策略，显著减少内存且常提升性能。

---

# ATTN-FIQA: Interpretable Attention-based Face Image Quality Assessment with Vision Transformers

**【用注意力评估人脸图像质量  】**

**arXiv**: https://arxiv.org/abs/2604.22841  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.22841  
**HF Paper**: https://hf-mirror.com/papers/2604.22841  
**HF Votes**: 2

## 简要摘要

*计算机视觉;生物特征识别;人脸图像质量评估  *

人脸识别系统的可靠性依赖于对人脸图像识别效用的评估，即人脸图像质量评估。  
本研究提出一种无需训练的方法，利用预训练视觉Transformer模型中的注意力分数来评估人脸图像质量，仅需一次前向传播即可获得质量分数和空间可解释性。

---

# EX-FIQA: Leveraging Intermediate Early eXit Representations from Vision Transformers for Face Image Quality Assessment

**【利用ViT中间层进行人脸质量评估  】**

**arXiv**: https://arxiv.org/abs/2604.22842  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.22842  
**HF Paper**: https://hf-mirror.com/papers/2604.22842  
**HF Votes**: 1

## 简要摘要

*计算机视觉;生物识别;人脸图像质量评估  *

现有基于ViT的人脸图像质量评估方法仅依赖最终层特征，忽略了中间层的质量相关信息。  
本文首次系统研究了ViT各中间层表示通过早期退出机制对质量评估的贡献，并提出一种无需修改结构或额外训练的分数融合框架，在多个基准上验证了其性能提升与计算效率优势。

---

# SketchVLM: Vision language models can annotate images to explain thoughts and guide users

**【视觉语言模型用草图注释图像解释答案】**

**arXiv**: https://arxiv.org/abs/2604.22875  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.22875  
**HF Paper**: https://hf-mirror.com/papers/2604.22875  
**HF Votes**: 17

## 简要摘要

*计算机视觉;多模态学习;视觉问答*

现有视觉语言模型仅用文本回答图像问题，用户难以验证
提出无需训练的通用框架，让模型在图像上叠加可编辑草图进行可视化解释

---

# TexOCR: Advancing Document OCR Models for Compilable Page-to-LaTeX Reconstruction

**【将科学文档重建为可编译的LaTeX】**

**arXiv**: https://arxiv.org/abs/2604.22880  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.22880  
**HF Paper**: https://hf-mirror.com/papers/2604.22880  
**HF Votes**: 6

## 简要摘要

*自然语言处理;文档理解;科学文档OCR*

现有文档OCR主要针对纯文本或Markdown，忽略了LaTeX在科学出版中至关重要的结构和可执行属性。
我们提出了TexOCR-Bench基准、TexOCR-Train训练集和TexOCR模型，通过监督微调和带可验证奖励的强化学习，在转录保真度、结构忠实度和端到端可编译性上提升科学PDF到LaTeX的重建。

---

# ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation

**【高效评估生成式人工智能】**

**arXiv**: https://arxiv.org/abs/2604.23099  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23099  
**HF Paper**: https://hf-mirror.com/papers/2604.23099  
**HF Votes**: 1

## 简要摘要

*机器学习;模型评估;主动性能估计与故障发现*

当前生成式AI模型评估面临推理慢、人工标注成本高、模型与基准测试数量激增的挑战。
提出主动评估框架ProEval，利用预训练高斯过程作为代理，通过贝叶斯求积主动选择测试输入，高效估计性能并发现故障案例。

---

# Discovering Agentic Safety Specifications from 1-Bit Danger Signals

**【大模型从1比特危险信号学安全规则】**

**arXiv**: https://arxiv.org/abs/2604.23210  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23210  
**HF Paper**: https://hf-mirror.com/papers/2604.23210  
**HF Votes**: 1

## 简要摘要

*强化学习；AI安全；安全规范发现*

要让大语言模型代理从极简的二元危险信号中，自主发现隐藏的安全约束，而非依赖人类详尽规定。
提出了EPO-Safe框架，仅凭稀疏危险警告迭代优化行为规范，发现安全行为并生成可读的安全假设。

---

# Learning to Identify Out-of-Distribution Objects for 3D LiDAR Anomaly Segmentation

**【三维激光雷达异常分割新方法  】**

**arXiv**: https://arxiv.org/abs/2604.23604  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23604  
**HF Paper**: https://hf-mirror.com/papers/2604.23604  
**HF Votes**: 2

## 简要摘要

*计算机视觉;三维场景理解;激光雷达异常分割  *

在自动驾驶等应用中，识别三维激光雷达点云中的未知物体至关重要，但现有研究不足。  
提出了一种直接在特征空间建模已知类分布以约束异常的方法，并构建了包含复杂场景的新混合数据集进行验证。

---

# RaV-IDP: A Reconstruction-as-Validation Framework for Faithful Intelligent Document Processing

**【通过重建验证文档处理准确性】**

**arXiv**: https://arxiv.org/abs/2604.23644  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23644  
**HF Paper**: https://hf-mirror.com/papers/2604.23644  
**HF Votes**: 1

## 简要摘要

*文档处理;信息抽取;文档处理质量验证*

现有文档处理流程提取结构化信息时缺乏对提取结果是否忠实于原文的验证机制。
提出RaV-IDP框架，让每个提取的实体通过重建并与原文比对来获得保真度分数，分数过低则触发GPT-4.1备用方案，从而验证提取的忠实性。

---

# PageGuide: Browser extension to assist users in navigating a webpage and locating information

**【网页导航助手提升浏览效率】**

**arXiv**: https://arxiv.org/abs/2604.23772  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23772  
**HF Paper**: https://hf-mirror.com/papers/2604.23772  
**HF Votes**: 3

## 简要摘要

*人机交互;智能辅助界面;网页信息定位*

用户浏览网页时难以快速定位信息、完成多步骤任务并避开干扰内容。
开发了PageGuide浏览器扩展，通过视觉叠加将LLM答案与网页DOM关联，实现信息定位、分步引导和干扰内容隐藏功能。

---

# Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms

**【VLA系统的安全威胁与防御综述】**

**arXiv**: https://arxiv.org/abs/2604.23775  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23775  
**HF Paper**: https://hf-mirror.com/papers/2604.23775  
**HF Votes**: 41

## 简要摘要

*机器人学习;具身智能安全;多模态攻击与防御*

随着视觉-语言-动作模型成为具身智能的统一平台，其安全问题因物理不可逆性、多模态攻击面等新挑战而日益突出。
本文系统梳理了VLA模型在攻击、防御、评估与部署四个方面的安全研究，并指出了未来关键开放问题。

---

# ClawMark: A Living-World Benchmark for Multi-Turn, Multi-Day, Multimodal Coworker Agents

**【构建长期多模态工作助手评测基准】**

**arXiv**: https://arxiv.org/abs/2604.23781  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23781  
**HF Paper**: https://hf-mirror.com/papers/2604.23781  
**HF Votes**: 24

## 简要摘要

*智能代理;多模态语言模型;长期协作任务评估*

现有基准难以评估在多日多模态动态环境中持续工作的语言模型助手
提出了一个多日多任务基准并评估了前沿系统发现完全执行仍很困难

---

# Stabilizing Efficient Reasoning with Step-Level Advantage Selection

**【稳定高效推理的步骤优势选择  】**

**arXiv**: https://arxiv.org/abs/2604.24003  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24003  
**HF Paper**: https://hf-mirror.com/papers/2604.24003  
**HF Votes**: 4

## 简要摘要

*自然语言处理;大语言模型推理;推理过程压缩  *

大型语言模型推理需要大量计算生成冗长推理链，现有高效推理方法在缩短上下文窗口后训练会损害稳定性与准确性。  
提出步骤级优势选择法，通过动态评估推理步骤置信度实现更优的准确率与效率平衡。

---

# Credal Concept Bottleneck Models for Epistemic-Aleatoric Uncertainty Decomposition

**【概念瓶颈模型的不确定性分解】**

**arXiv**: https://arxiv.org/abs/2604.24170  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24170  
**HF Paper**: https://hf-mirror.com/papers/2604.24170  

## 简要摘要

*机器学习;可解释人工智能;概念不确定性分解*

概念瓶颈模型通过可解释概念进行预测，但通常输出的点概率混淆了认识不确定性和偶然不确定性。
提出CREDENCE框架，用概率区间表示概念，分解不确定性以支持决策，并能指导自动化、数据收集和人工审查。

---

# Rewarding the Scientific Process: Process-Level Reward Modeling for Agentic Data Analysis

**【设计数据分析智能体的过程奖励模型】**

**arXiv**: https://arxiv.org/abs/2604.24198  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24198  
**HF Paper**: https://hf-mirror.com/papers/2604.24198  
**HF Votes**: 15

## 简要摘要

*自然语言处理;智能体与交互系统;过程奖励建模*

现有过程奖励模型在静态领域成功，但难以监督动态数据分析任务，常误判探索行为或漏检静默错误。
本文提出DataPRM，一种能主动与环境交互检验中间状态、区分可纠正错误与不可恢复错误的环境感知过程奖励模型，并通过大规模数据构建和实验验证其有效性。

---

# ReVSI: Rebuilding Visual Spatial Intelligence Evaluation for Accurate Assessment of VLM 3D Reasoning

**【改进视觉空间智能评测基准  】**

**arXiv**: https://arxiv.org/abs/2604.24300  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24300  
**HF Paper**: https://hf-mirror.com/papers/2604.24300  
**HF Votes**: 53

## 简要摘要

*计算机视觉;视觉语言模型;3D空间推理评测  *

现有3D空间推理评测方法因数据缺陷和模型输入不匹配导致评估失真。  
作者构建了高质量数据集ReVSI，通过重新标注和生成可回答问题，支持可控诊断评估。

---

# Improving Vision-language Models with Perception-centric Process Reward Models

**【用感知奖励模型提升视觉语言模型】**

**arXiv**: https://arxiv.org/abs/2604.24583  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24583  
**HF Paper**: https://hf-mirror.com/papers/2604.24583  
**HF Votes**: 1

## 简要摘要

*多模态人工智能;视觉语言模型;感知错误检测与纠正*

当前强化学习对视觉语言模型（VLM）的监督过于粗放，难以诊断和纠正推理链中的具体错误。
本文提出感知奖励模型Perceval，能在训练和推理阶段实现细粒度错误定位与修正，显著提升多种VLM在多项任务上的性能。

---

# Quantum Kernel Advantage over Classical Collapse in Medical Foundation Model Embeddings

**【量子核在医学嵌入分类中胜出】**

**arXiv**: https://arxiv.org/abs/2604.24597  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24597  
**HF Paper**: https://hf-mirror.com/papers/2604.24597  

## 简要摘要

*机器学习;量子机器学习;医学影像分类*

在胸部X光医保分类任务中，比较量子支持向量机与经典支持向量机的性能。
量子支持向量机在多种配置下性能显著优于经典方法，并分析了量子核有效秩高的优势。

---

# OmniShotCut: Holistic Relational Shot Boundary Detection with Shot-Query Transformer

**【镜头边界检测新方法  】**

**arXiv**: https://arxiv.org/abs/2604.24762  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24762  
**HF Paper**: https://hf-mirror.com/papers/2604.24762  
**HF Votes**: 7

## 简要摘要

*计算机视觉;视频分析;镜头边界检测  *

现有镜头边界检测方法存在边界不清晰、漏检严重、依赖有噪声标注等问题。  
提出基于合成数据和关系预测的镜头边界检测框架，并构建现代多领域评测基准。

---
