# Daily 3D Paper — 项目说明（详细）

本文档描述仓库结构、流水线步骤、发布路径与配置，便于维护与二次开发。**安装依赖、环境变量与运行命令**见 [SETUP.md](SETUP.md)；仓库根目录 [README.md](../README.md) 主要面向网站访客。

## 目标

- 从 [Hugging Face Daily Papers](https://huggingface.co/papers) 获取当日论文元数据。
- 用 LLM 多轮筛选与 **3D / 视觉 / 几何** 相关的重点论文。
- 抓取 arXiv 摘要与（可选）HTML 正文，生成**短文摘要**与**深度解析**，抽取图示并翻译图注。
- 输出可部署的**静态站点**（Tailwind + 原生 JS），托管在 GitHub Pages。
- 支持 **area 流水线**：对感兴趣领域的论文单独深度解析，同步到 Notion。

---

## 仓库结构

```
run_pipeline.py          # PaperPipeline：LLM / 抓取工具层
daily_processor.py       # DailyPaperProcessor：日期流水线编排
paper_analyzer.py        # PaperAnalyzer：独立论文解析接口（可复制到其他项目）
area_processor.py        # area 流水线主入口
scheduler.py             # 定时调度器

areas/
  config/                # area 论文列表（YAML，用户维护）
    3d-gen-rec.yaml
  papers/                # area 论文本地输出（.md，git 追踪）
    3d-gen-rec/

renderers/
  base.py                # AreaRenderer 抽象基类
  notion/sync.py         # NotionRenderer：同步到 Notion
  file/sync.py           # FileRenderer：写入本地 .md

docs/                    # GitHub Pages 静态站点
  date/<YYYY-MM-DD>/     # 每日报告（index.html + config.json）
  date/config.json       # 日期索引

templates/index.html     # 单日报告前端模板
output/cache/            # 各步骤中间缓存（不提交）
delete/                  # 废弃代码存档
```

---

## date 流水线步骤

| 步骤 | 说明 |
|------|------|
| step01 | 拉取 HF 当日论文列表（标题 + arXiv 编号等） |
| step02 | 抓取 arXiv 摘要页，提取 abstract 与 comments |
| step03 | 多轮 LLM 板块归类（3D生成/重建、视频生成、图片生成等） |
| step04 | 逐篇生成短文摘要（领域 + 两句话概括） |
| step05 | 下载重点论文 arXiv HTML 全文 |
| step06 | LLM 深度解析（任务 / 问题 / 思路 / 结果） |
| step07 | 从 HTML 中抽取论文图示（最多 8 张候选） |
| step07b | 两轮 LLM 依据图注选出关键图（默认 3 张） |
| step08 | 对选中图注批量翻译为中文 |
| step09 | 写入 `config.json`，复制前端模板，更新日期索引 |

流水线入口：`PaperPipeline.run_pipeline(date_str)`，内部委托给 `DailyPaperProcessor`。

---

## area 流水线

area 流水线独立于 date 流水线，**不走 GitHub Action**，在本地 `git pull` 后手动运行。

### 配置格式（`areas/config/<slug>.yaml`）

```yaml
- name: "ReconViaGen"
  url: "https://arxiv.org/abs/2510.23306"
- name: "CUPID"
  url: "https://arxiv.org/abs/2603.10745"
```

支持 arXiv URL、arXiv ID、或任意网页 URL。

### 运行

```bash
python area_processor.py                    # 处理所有 area
python area_processor.py --area 3d-gen-rec  # 只处理指定 area
python area_processor.py --dry-run          # 只打印，不写入
python area_processor.py --no-notion        # 跳过 Notion，只写本地文件
```

### 输出

- **本地文件**：`areas/papers/<slug>/<date>_<title>.md`
- **Notion**：在 `NOTION_ROOT_PAGE_ID` 下自动创建/查找 area 子页面，写入论文页

### 环境变量

| 变量 | 说明 |
|------|------|
| `MY_API_KEY` | LLM API Key（SiliconFlow） |
| `NOTION_TOKEN` | Notion Integration Token |
| `NOTION_ROOT_PAGE_ID` | Notion areas 根页面 ID（默认 `347e1dce83648023abdde32fa8065aac`） |

---

## 独立论文解析接口

`paper_analyzer.py` 的 `PaperAnalyzer` 可独立使用或复制到其他项目：

```python
from paper_analyzer import PaperAnalyzer

analyzer = PaperAnalyzer(api_key="your-key")

# 简要解析
result = analyzer.summarize("https://arxiv.org/abs/2404.12345")

# 深度解析（含图示、图注翻译）
result = analyzer.deep_analyze("https://arxiv.org/abs/2404.12345")
# result: {arxiv_id, url, title, abstract, summary, deep_analysis, figures}
```

支持 arXiv URL 和通用网页 URL。缓存写入 `output/cache/analyzer/`。

---

## 配置

核心参数在 `run_pipeline.py` 的 `PipelineConfig` 数据类中：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `output_pub_dir_fmt` | `docs/date/{date_str}` | 发布目录 |
| `output_cache_dir_fmt` | `output/cache/date/{date_str}` | 缓存目录 |
| `llm_model` | `deepseek-ai/DeepSeek-V3.2` | LLM 模型 |
| `llm_api_url` | SiliconFlow | LLM API 地址 |
| `key_figure_count` | `3` | 每篇选取关键图数量 |
| `deep_body_max_chars` | `8000` | 深度解析正文截取长度 |
| `max_figures_per_paper` | `8` | 每篇最多抽取图示数 |
| `store_arxiv_figures_locally` | `False` | 是否下载图示到本地 |

---

## 关于本仓库内容来源

**Python 代码、前端模板、GitHub Pages 静态页、`docs/` 与根目录下的说明文档（含本文件）等**，均由 AI 主要在 Cursor 中编写。总述见根目录 [README.md](../README.md)。
