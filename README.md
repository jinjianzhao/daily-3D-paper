# Daily 3D Paper

> **每天打开一页，把「今日 3D 论文」读薄**

[Hugging Face Daily Papers](https://huggingface.co/papers) 上的列表又长又杂——**本站帮你把和 3D 相关的那几篇拎出来**：用中文写好**短摘要**与**结构化深读**，配上**图示与图注**，按日期归档。你不需要装任何软件，点开链接就能看。

---

## 为什么值得收藏

|  |  |
|--:|--|
| **省时间** | 先从「深度解析」扫重点，再按需翻「全量简报」，不必自己一篇篇点开 arXiv。 |
| **方向对口** | 聚焦 **3D 生成、重建、图形学、Mesh / 几何** 等，少噪音、多相关。 |
| **能读下去** | 中文输出 + 左侧目录 + 可点开放大的图，适合通勤或午休快速跟进领域动态。 |

---

## 立即打开

|  |  |
|--|--|
| **站点首页**（项目说明与入口） | **[jinjianzhao.github.io/daily-3D-paper/](https://jinjianzhao.github.io/daily-3D-paper/)** |
| **按日期浏览**（推荐从这里进） | **[jinjianzhao.github.io/daily-3D-paper/date/](https://jinjianzhao.github.io/daily-3D-paper/date/)** |

在任意一天的页面里，通常包括：**深度解析**（重点论文）、**全量简报**（当日其余论文短讯）、**图示**（可放大，图注含中译，视数据而定）。

---

## 开发者 / 自建流水线

### date 流水线（每日自动）

每天自动从 Hugging Face 抓取论文，生成静态站点，发布到 GitHub Pages。详见 **[docs/SETUP.md](docs/SETUP.md)** 与 **[docs/PROJECT.md](docs/PROJECT.md)**。

```bash
# 本地跑一天
python run_pipeline.py 2026-04-19

# 指定重跑某步
python -c "from run_pipeline import PaperPipeline, PipelineConfig; import os; PaperPipeline(os.getenv('MY_API_KEY'), PipelineConfig()).run_pipeline('2026-04-19', force_rerun=['step01'])"
```

### area 流水线（本地 git pull 后手动跑）

在 `areas/config/` 下维护感兴趣领域的论文列表（YAML），本地 `git pull` 后跑 area 流水线，自动同步到 Notion 并写入本地文件。

```bash
# 解析并同步所有 area
python area_processor.py

# 只处理某个 area
python area_processor.py --area 3d-gen-rec

# 打印，不写入
python area_processor.py --dry-run

# 跳过 Notion，只写本地文件
python area_processor.py --no-notion
```

### 独立论文解析（可复制到其他项目）

`paper_analyzer.py` 提供 `summarize` / `deep_analyze` 接口，支持 arXiv 和通用网页。

```python
from paper_analyzer import PaperAnalyzer

analyzer = PaperAnalyzer(api_key="your-key")
result = analyzer.deep_analyze("https://arxiv.org/abs/2404.12345")
# result: {arxiv_id, url, title, abstract, summary, deep_analysis, figures}
```

---

*本仓库全部内容——含 Python 流水线、前端、静态站点、以及 README / `docs/` 下说明文档等——均由 AI 主要编写（Cursor）。*
