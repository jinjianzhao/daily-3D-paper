# Daily Paper 3D — 每日 3D 论文自动摘要系统

自动从 [Hugging Face Daily Papers](https://huggingface.co/papers) 抓取当日论文列表，利用 LLM 筛选 **3D 生成 / 3D 重建 / 计算机图形学 / Mesh 几何处理** 等方向的重点论文，生成短文摘要与深度解析，并输出一个可直接浏览的静态站点。

> **本项目代码由 AI 编写（Cursor）。**

---

## 功能一览

| 步骤 | 说明 |
|------|------|
| step01 | 拉取 HF 当日论文列表（标题 + arXiv 编号） |
| step02 | 多轮 LLM 筛选 3D 相关重点论文 |
| step03 | 抓取 arXiv 摘要页，提取 abstract 与 comments |
| step04 | 逐篇生成短文摘要（领域 + 两句话概括） |
| step05 | 下载重点论文 arXiv HTML 全文 |
| step06 | LLM 深度解析（任务 / 问题 / 思路 / 结果） |
| step07 | 从 HTML 中抽取论文图示 |
| step08 | 将图注批量翻译为中文 |
| step09 | 写入 `config.json`，复制前端模板，生成静态站点 |

## 项目结构

```
.
├── run_pipeline.py        # 主流水线：数据抓取、LLM 调用、缓存、站点生成
├── scheduler.py           # 定时调度器：每天 6 次（约每 4 小时）自动执行流水线
├── templates/
│   └── index.html         # 前端页面模板（Tailwind CSS + vanilla JS）
└── output/
    ├── papers/
    │   └── date/
    │       └── <YYYY-MM-DD>/   # 每日发布目录
    │           ├── config.json  # 前端读取的数据文件
    │           ├── index.html   # 可直接打开的静态站点
    │           └── images/      # 论文图示（若开启本地存储）
    └── cache/
        └── date/
            └── <YYYY-MM-DD>/   # 各步骤的 LLM 缓存
```

## 快速开始

### 1. 安装依赖

```bash
pip install requests beautifulsoup4 tqdm
```

### 2. 配置环境变量

```bash
export MY_API_KEY="your-siliconflow-api-key"
```

> 默认使用 SiliconFlow 的 DeepSeek-V3.2 模型。如需更换，在 `PipelineConfig` 中修改 `llm_model` 和 `llm_api_url`。

### 3. 运行流水线

```bash
# 处理今日论文
python run_pipeline.py

# 处理指定日期
python run_pipeline.py  # 修改 run_pipeline.py 末尾的 date_str
```

### 4. 定时调度（可选）

```bash
python scheduler.py
```

启动后立即执行一次，之后每天在 6 个固定整点时段自动运行（间隔约 4 小时）。

### 5. 查看结果

运行完成后，用浏览器打开 `output/papers/date/<YYYY-MM-DD>/index.html` 即可查看当日论文摘要站点。

### 6. 在线访问

部署到 GitHub Pages 后可通过以下地址浏览：

- **日期索引**：https://jinjianzhao.github.io/daily-3D-paper/date/
- **今日自动跳转**：https://jinjianzhao.github.io/daily-3D-paper/

> `output/papers/` 入口会自动跳转到当天（或昨天）的日期页面。

## 配置项

所有可调参数集中在 `PipelineConfig` 数据类中：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `llm_model` | `deepseek-ai/DeepSeek-V3.2` | LLM 模型名称 |
| `llm_api_url` | SiliconFlow endpoint | LLM API 地址 |
| `llm_temperature` | `0.7` | 生成温度 |
| `llm_max_tokens` | `2048` | 单次 LLM 最大输出 token |
| `focus_selection_llm_runs` | `2` | step02 多轮筛选合并次数 |
| `deep_body_max_chars` | `8000` | 深度解析截取正文长度 |
| `max_figures_per_paper` | `3` | 每篇论文最多抽取图示数 |
| `store_arxiv_figures_locally` | `False` | 是否下载图示到本地 |

## 前端

前端为纯静态页面（`templates/index.html`），使用 Tailwind CSS + vanilla JS 构建，主要特性：

- **深度解析区**：重点论文的完整分析，支持 Markdown 渲染、折叠/展开
- **全量简报区**：当日所有论文的两句话摘要
- **图示展示**：点击放大查看，中英文图注
- **目录导航**：左侧固定目录，滚动高亮当前位置
- **响应式设计**：适配桌面与移动端

## 关于 AI

本项目的代码（Python 流水线 + 前端页面）由 AI 辅助编写。具体来说，是在 **Cursor** 编辑器中使用 **Claude** 模型进行 pair programming 完成的。如果你也想在 README 中标注这一点，常见的写法有：

- `Built with AI assistance (Cursor + Claude)`
- `Vibe-coded with Claude`
- `Code generated with the help of AI`

选择你觉得合适的即可。
