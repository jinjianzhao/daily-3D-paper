# 本地环境与运行（开发者）

面向在本机执行流水线、部署或修改代码的贡献者；**仅浏览网站的用户无需阅读本文**。

---

## 依赖安装

```bash
pip install requests beautifulsoup4 tqdm pyyaml notion-client PyMuPDF
```

| 包 | 用途 |
|---|---|
| `requests` / `beautifulsoup4` / `tqdm` | 网络抓取与进度条 |
| `pyyaml` | area 配置读写 |
| `notion-client` | area 论文同步到 Notion（可选） |
| `PyMuPDF` | 本地 PDF 文本提取（area 流水线） |

---

## 环境变量

```bash
export MY_API_KEY="your-siliconflow-api-key"
export NOTION_TOKEN="your-notion-integration-token"       # area 流水线需要
export NOTION_ROOT_PAGE_ID="your-notion-root-page-id"     # 可选，有默认值
```

默认使用 SiliconFlow 的 DeepSeek 兼容接口。更换模型或 API 地址可在 `run_pipeline.py` 的 `PipelineConfig` 中修改 `llm_model` 与 `llm_api_url`。

---

## 运行流水线

```bash
python run_pipeline.py
```

处理哪些日期由 `run_pipeline.py` 末尾 `if __name__ == "__main__":` 中对 `run_pipeline(...)` 的调用决定，可按需改为单日或连续多日。

运行结束后，在浏览器打开：

```text
docs/date/<YYYY-MM-DD>/index.html
```

---

## 定时调度（可选）

```bash
python scheduler.py
```

行为以 `scheduler.py` 内注释与逻辑为准（例如固定间隔重复执行）。

---

## 更多说明

流水线各步骤、发布目录与 `PipelineConfig` 参数说明见 **[PROJECT.md](PROJECT.md)**。

---

关于文档与仓库内容的编写说明，见根目录 **[README.md](../README.md)**（与 PROJECT 中「关于本仓库内容来源」一节一致）。
