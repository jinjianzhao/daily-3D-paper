# Daily 3D Paper — 项目说明（详细）

本文档描述仓库结构、流水线步骤、发布路径与配置，便于维护与二次开发。**安装依赖、环境变量与运行命令**见 [SETUP.md](SETUP.md)；仓库根目录 [README.md](../README.md) 主要面向网站访客。

## 目标

- 从 [Hugging Face Daily Papers](https://huggingface.co/papers) 获取当日论文元数据。
- 用 LLM 多轮筛选与 **3D / 视觉 / 几何** 相关的重点论文。
- 抓取 arXiv 摘要与（可选）HTML 正文，生成**短文摘要**与**深度解析**，抽取图示并翻译图注。
- 输出可部署的**静态站点**（Tailwind + 原生 JS），托管在 GitHub Pages。

## 流水线与步骤

| 步骤 | 说明 |
|------|------|
| step01 | 拉取 HF 当日论文列表（标题 + arXiv 编号等） |
| step02 | 多轮 LLM 筛选 3D 相关重点论文 |
| step03 | 抓取 arXiv 摘要页，提取 abstract 与 comments |
| step04 | 逐篇生成短文摘要（领域 + 两句话概括） |
| step05 | 下载重点论文 arXiv HTML 全文（供深度解析） |
| step06 | LLM 深度解析（任务 / 问题 / 思路 / 结果） |
| step07 | 从 HTML 中抽取论文图示 |
| step08 | 图注批量翻译为中文 |
| step09 | 写入 `config.json`，复制前端模板，生成静态站点 |

调度器 `scheduler.py` 可按固定间隔重复执行流水线（详见该文件）。

## 目录与产物

### 发布目录（站点）

默认配置下，**对外展示**的静态文件位于：

- `docs/date/<YYYY-MM-DD>/`：某一日的 `index.html`、`config.json`、图示等。
- `docs/date/index.html`：**日期索引**（列出所有已发布日期）。
- `docs/date/config.json`：日期列表与各日论文数量（由流水线扫描生成）。
- `docs/index.html`：**项目首页**（说明与入口，不自动跳转）。

GitHub Pages 通常将仓库的 `docs/` 作为站点根目录，因此：

- 站点根：`https://<user>.github.io/<repo>/`
- 日期列表：`https://<user>.github.io/<repo>/date/`

### 缓存目录

各步骤的中间结果（LLM 缓存、抓取结果等）默认在：

- `output/cache/date/<YYYY-MM-DD>/`

便于断点续跑与调试；**不必**提交到 Git 的体积过大内容可按 `.gitignore` 自行处理。

### 前端模板

- `templates/index.html`：单日报告页模板；流水线复制到 `docs/date/<date>/` 并填入数据。

## 配置

核心参数在 `run_pipeline.py` 的 `PipelineConfig` 数据类中，例如：

- `output_pub_dir_fmt`：发布目录模式，默认 `docs/date/{date_str}`。
- `output_cache_dir_fmt`：缓存目录，默认 `output/cache/date/{date_str}`。
- `llm_model`、`llm_api_url`、`llm_temperature`、`llm_max_tokens`：LLM 调用相关。
- `focus_selection_llm_runs`：step02 多轮筛选次数。
- `deep_body_max_chars`：深度解析所用正文最大字符数。
- `max_figures_per_paper`：每篇最多抽取的图示数量。
- `store_arxiv_figures_locally`：是否将 arXiv 图示下载到本地。

运行前需设置 API Key（如 `MY_API_KEY`，见 [SETUP.md](SETUP.md)）。

## 前端能力（单日页）

- 深度解析区：Markdown 渲染、折叠。
- 全量简报区：当日其余论文的两句话摘要。
- 图示：点击放大，中英文图注。
- 左侧目录与滚动高亮（宽屏）。

## 关于本仓库内容来源

**Python 代码、前端模板、GitHub Pages 静态页、`docs/` 与根目录下的说明文档（含本文件）等**，均由 AI 主要在 Cursor 中编写。总述见根目录 [README.md](../README.md)。
