# 2026-04-28 全量简报

# Stochastic KV Routing: Enabling Adaptive Depth-Wise Cache Sharing

**【自适应共享KV缓存优化大模型推理】**

**arXiv**: https://arxiv.org/abs/2604.22782  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.22782  
**HF Paper**: https://hf-mirror.com/papers/2604.22782  

## 简要摘要

*自然语言处理;大模型推理优化;KV缓存深度共享*

背景/任务是降低大语言模型推理时KV缓存的内存开销。
提出了一种名为随机跨层注意力的训练方法，使模型能适应深度维度的KV缓存共享，从而在不损失性能的前提下显著减少内存占用。

---

# SketchVLM: Vision language models can annotate images to explain thoughts and guide users

**【让视觉语言模型在图上标注解释】**

**arXiv**: https://arxiv.org/abs/2604.22875  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.22875  
**HF Paper**: https://hf-mirror.com/papers/2604.22875  
**HF Votes**: 8

## 简要摘要

*计算机视觉;视觉问答;视觉推理与标注*

现有视觉语言模型仅用文本回答图像问题，用户难以验证其推理过程。
提出SketchVLM框架，让模型能在输入图像上生成可编辑的SVG标注，以视觉方式解释答案，提升了多个视觉推理任务的准确性和标注质量。

---

# ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation

**【高效评估生成式AI模型性能】**

**arXiv**: https://arxiv.org/abs/2604.23099  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23099  
**HF Paper**: https://hf-mirror.com/papers/2604.23099  

## 简要摘要

*机器学习;生成模型评估;主动式性能估计与故障发现*

生成式AI模型评估因推理慢、标注贵、模型与基准快速增加而日益耗费资源。
提出主动评估框架ProEval，通过迁移学习和贝叶斯求积高效估计性能并主动发现故障，理论证明其无偏有界，实验显示其样本效率显著优于基线。

---

# Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms

**【视觉语言动作模型安全综述】**

**arXiv**: https://arxiv.org/abs/2604.23775  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.23775  
**HF Paper**: https://hf-mirror.com/papers/2604.23775  
**HF Votes**: 1

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
**HF Votes**: 14

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
**HF Votes**: 1

## 简要摘要

*自然语言处理;大语言模型推理;高效推理方法  *

大型语言模型推理需大量计算且生成过长推理链，现有高效推理方法常受限短上下文微调，导致训练不稳定与精度下降。  
提出步级优势选择方法，通过筛选高置信度推理步实现更优精度与长度平衡，在数学与通用推理基准上提升准确率并缩短推理长度。

---

# Rewarding the Scientific Process: Process-Level Reward Modeling for Agentic Data Analysis

**【为数据分析智能体设计过程奖励模型】**

**arXiv**: https://arxiv.org/abs/2604.24198  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24198  
**HF Paper**: https://hf-mirror.com/papers/2604.24198  
**HF Votes**: 10

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
**HF Votes**: 14

## 简要摘要

*计算机视觉;视觉语言模型;三维空间推理评估*

现有视觉语言模型的空间智能评估方法存在两个主要问题：一是基于点云标注生成问答对时存在错误和歧义，二是评估常假设模型能获取完整场景，而实际模型输入仅为稀疏采样的帧。
我们提出了ReVSI基准和协议，通过重新标注381个场景的对象与几何信息，并基于模型实际可获取的帧生成可靠的问答对，以提供更准确、可控的视觉空间推理评估。

---

# OmniShotCut: Holistic Relational Shot Boundary Detection with Shot-Query Transformer

**【用Transformer检测视频镜头边界】**

**arXiv**: https://arxiv.org/abs/2604.24762  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24762  
**HF Paper**: https://hf-mirror.com/papers/2604.24762  
**HF Votes**: 2

## 简要摘要

*计算机视觉;视频理解;镜头边界检测*

现有镜头边界检测方法存在边界不明确、漏检等问题，且依赖有噪声的标注和过时的基准。
提出OmniShotCut方法，通过基于镜头查询的Transformer联合预测镜头内与镜头间关系，并构建了合成数据管道和新基准进行评测。

---
