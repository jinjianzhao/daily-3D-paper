# 2026-05-01 全量简报

# The Last Human-Written Paper: Agent-Native Research Artifacts

**【用可执行研究包替代传统论文】**

**arXiv**: https://arxiv.org/abs/2604.24658  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.24658  
**HF Paper**: https://hf-mirror.com/papers/2604.24658  
**HF Votes**: 4

## 简要摘要

*科学知识表示与传播;研究流程与成果标准化;面向智能体的研究制品*

传统科学论文为了线性叙事而丢弃了大量研究过程细节，这阻碍了AI智能体对研究的理解、复现和扩展。
提出了一种面向智能体的研究制品协议，它包含科学逻辑、可执行代码、探索图谱和证据四层结构，并设计了配套工具链，提高了AI对论文的理解和复现成功率。

---

# Length Value Model: Scalable Value Pretraining for Token-Level Length Modeling

**【剩余生成长度建模】**

**arXiv**: https://arxiv.org/abs/2604.27039  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.27039  
**HF Paper**: https://hf-mirror.com/papers/2604.27039  
**HF Votes**: 15

## 简要摘要

*自然语言处理;语言模型;生成长度控制*

现有自回归模型缺乏对生成长度的细粒度建模，影响推理成本与性能。
提出长度价值模型，将长度建模转化为价值估计问题，实现无需标注的细粒度长度预测与控制，提升模型效率与性能。

---

# Co-Evolving Policy Distillation

**【共进化策略蒸馏统一专家能力】**

**arXiv**: https://arxiv.org/abs/2604.27083  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.27083  
**HF Paper**: https://hf-mirror.com/papers/2604.27083  
**HF Votes**: 23

## 简要摘要

*机器学习;强化学习;多模态智能体策略蒸馏*

现有两种后训练范式在整合多个专家能力时存在不足，各有缺陷。
我们提出共进化策略蒸馏，让专家并行互教、协同进化，实现了文本、图像和视频推理能力的高效统一。

---

# Efficient Training on Multiple Consumer GPUs with RoundPipe

**【用消费级GPU高效微调大模型】**

**arXiv**: https://arxiv.org/abs/2604.27085  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.27085  
**HF Paper**: https://hf-mirror.com/papers/2604.27085  
**HF Votes**: 16

## 简要摘要

*自然语言处理;模型高效训练;流水线并行调度*

在消费级GPU上微调大语言模型面临显存和通信瓶颈，现有流水线并行方案存在负载不均问题。
提出了RoundPipe调度方法，通过轮询调度和一系列优化，在消费级GPU上实现了高效、近零气泡的流水线并行训练。

---

# Compliance versus Sensibility: On the Reasoning Controllability in Large Language Models

**【大模型推理的可控性研究】**

**arXiv**: https://arxiv.org/abs/2604.27251  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.27251  
**HF Paper**: https://hf-mirror.com/papers/2604.27251  
**HF Votes**: 4

## 简要摘要

*自然语言处理;语言模型推理;逻辑模式解耦*

研究大语言模型能否将基本逻辑推理模式从具体问题中分离出来以实现可控推理。
通过制造推理冲突发现模型更注重任务合理性而非指令遵循，并探索了通过干预提高可控性的方法。

---

# Heterogeneous Scientific Foundation Model Collaboration

**【异构科学基础模型协作框架】**

**arXiv**: https://arxiv.org/abs/2604.27351  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.27351  
**HF Paper**: https://hf-mirror.com/papers/2604.27351  
**HF Votes**: 141

## 简要摘要

*人工智能系统;多智能体;科学基础模型协作*

现有智能体系统依赖语言接口，难以处理科学领域非语言数据和任务
开发了Eywa框架，用语言模型协调专业基础模型，提升多模态科学任务性能

---

# InteractWeb-Bench: Can Multimodal Agent Escape Blind Execution in Interactive Website Generation?

**【多模态网站生成代理的盲执行问题】**

**arXiv**: https://arxiv.org/abs/2604.27419  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.27419  
**HF Paper**: https://hf-mirror.com/papers/2604.27419  
**HF Votes**: 6

## 简要摘要

*多模态交互;代码生成;网站生成基准*

现有网站生成基准依赖理想化假设，无法应对非专业用户模糊指令导致的语义错位问题，即"盲执行"。
本文提出了首个模拟非专业低代码用户的交互式网站生成基准InteractWeb-Bench，包含多样化用户代理和指令扰动，并构建了支持澄清、执行、验证等动作的交互环境，实验发现前沿模型仍受困于盲执行。

---

# Claw-Eval-Live: A Live Agent Benchmark for Evolving Real-World Workflows

**【评估智能体实时工作流程的基准  】**

**arXiv**: https://arxiv.org/abs/2604.28139  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.28139  
**HF Paper**: https://hf-mirror.com/papers/2604.28139  
**HF Votes**: 14

## 简要摘要

*自然语言处理;智能体评估;工作流自动化基准  *

现有智能体基准的静态任务设置难以评估其适应不断变化的真实工作需求并验证任务执行过程。  
本文提出了一个可更新的实时工作流智能体基准，通过分离需求信号层与可复现的快照来构建任务，记录执行痕迹进行多维度评估，发现当前前沿模型在复杂工作流任务上表现仍不理想。

---

# Intern-Atlas: A Methodological Evolution Graph as Research Infrastructure for AI Scientists

**【构建AI研究方法演化图谱  】**

**arXiv**: https://arxiv.org/abs/2604.28158  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.28158  
**HF Paper**: https://hf-mirror.com/papers/2604.28158  
**HF Votes**: 11

## 简要摘要

*科学知识图谱;方法关系挖掘;演化链自动构建  *

现有研究基础设施以文档为中心，无法显式刻画方法的演变关系，阻碍了AI研究代理等新型知识消费者的理解与应用。  
我们提出了Intern-Atlas，一个自动构建的方法演化图谱，它从海量论文中识别方法实体、推断谱系关系，并支持下游应用如演化链搜索与创意生成。

---

# Synthetic Computers at Scale for Long-Horizon Productivity Simulation

**【规模化合成计算机模拟长程办公任务】**

**arXiv**: https://arxiv.org/abs/2604.28181  
**AlphaXiv**: https://www.alphaxiv.org/zh/overview/2604.28181  
**HF Paper**: https://hf-mirror.com/papers/2604.28181  
**HF Votes**: 6

## 简要摘要

*Agentic AI;智能体模拟环境构建;办公环境合成与长程模拟*

背景：真实的长程办公任务高度依赖用户特定的计算机环境，但为这类场景大规模创建合成数据存在挑战。
本文提出一种可扩展方法，能批量创建包含文件夹和文档的合成计算机环境，并在其上运行代理完成长程任务模拟，实验表明该方法能有效提升代理在办公任务上的性能。

---
