"""
area_processor.py：从 Notion area_config 数据库读取论文列表，深度解析后同步到 Notion + 本地文件。

用法：
    python area_processor.py                    # 处理所有 area
    python area_processor.py --area 3d-gen-rec  # 只处理指定 area
    python area_processor.py --dry-run          # 只打印，不写入
"""

import os
import re
import sys
import json
import argparse
from datetime import datetime, timezone

import requests as req

from paper_analyzer import PaperAnalyzer
from renderers.docsify.paper import render_paper_md, paper_dict_from_analyzer_result
from run_pipeline import PipelineConfig, _set_pipeline_log_path
from renderers.notion.sync import NotionRenderer
from renderers.file.sync import FileRenderer


AREA_CONFIG_PAGE_ID = os.environ.get(
    "NOTION_AREA_CONFIG_PAGE_ID",
    "349e1dce836480ad9ac2ec0cffec8e59",
)
NOTION_API_VERSION = "2022-06-28"
CACHE_ROOT = "output/cache/area"


def _area_name_from_slug(slug: str) -> str:
    return "-".join(w.upper() if len(w) <= 3 else w.capitalize() for w in slug.split("-"))


def _extract_arxiv_id(url: str) -> str | None:
    m = re.search(r"(\d{4}\.\d{4,5})", url)
    return m.group(1) if m else None


def _cache_path(area_slug: str, entry_key: str) -> str:
    return os.path.join(CACHE_ROOT, area_slug, f"{entry_key}.json")


def _load_cache(path: str) -> dict | None:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def _save_cache(path: str, data: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _build_md(result: dict) -> str:
    paper = paper_dict_from_analyzer_result(result)
    return render_paper_md(paper, html_figure=False, include_title=False)


# ---- Notion 数据库读写 ----

class NotionConfigReader:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_API_VERSION,
        }
        self.base = "https://api.notion.com/v1"

    def list_area_databases(self) -> list[dict]:
        """列举 area_config 页面下所有 child_database，返回 [{id, slug}]。"""
        resp = req.get(
            f"{self.base}/blocks/{AREA_CONFIG_PAGE_ID}/children?page_size=100",
            headers=self.headers,
        )
        resp.raise_for_status()
        dbs = []
        for b in resp.json().get("results", []):
            if b["type"] == "child_database":
                dbs.append({
                    "id": b["id"].replace("-", ""),
                    "slug": b["child_database"]["title"],
                })
        return dbs

    def query_entries(self, db_id: str) -> list[dict]:
        """查询数据库所有行，返回 [{page_id, name, url, done}]。"""
        rows = []
        payload = {}
        while True:
            resp = req.post(
                f"{self.base}/databases/{db_id}/query",
                headers=self.headers,
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
            for page in data.get("results", []):
                props = page["properties"]
                row = {"page_id": page["id"]}
                for k, v in props.items():
                    t = v["type"]
                    if t == "title":
                        texts = v.get("title", [])
                        row[k] = texts[0]["plain_text"] if texts else ""
                    elif t == "url":
                        row[k] = v.get("url", "") or ""
                    elif t == "checkbox":
                        row[k] = v.get("checkbox", False)
                    elif t == "rich_text":
                        texts = v.get("rich_text", [])
                        row[k] = texts[0]["plain_text"] if texts else ""
                    else:
                        row[k] = f"<{t}>"
                rows.append(row)
            if not data.get("has_more"):
                break
            payload["start_cursor"] = data["next_cursor"]
        return rows

    def set_done(self, page_id: str, done: bool = True) -> None:
        """写回 done 复选框。"""
        resp = req.patch(
            f"{self.base}/pages/{page_id}",
            headers=self.headers,
            json={"properties": {"done": {"checkbox": done}}},
        )
        resp.raise_for_status()


# ---- 处理逻辑 ----

def process_area(
    area_slug: str,
    entries: list[dict],
    analyzer: PaperAnalyzer,
    notion_renderer: NotionRenderer | None,
    file_renderer: FileRenderer,
    config_reader: NotionConfigReader,
    dry_run: bool = False,
) -> None:
    area_name = _area_name_from_slug(area_slug)
    today = datetime.now(timezone.utc).strftime("%Y-%m")

    # 按 arXiv ID 从旧到新排序
    def _sort_key(e):
        aid = _extract_arxiv_id(e.get("url", ""))
        return aid if aid else "9999.99999"
    entries = sorted(entries, key=_sort_key)

    print(f"\n=== [{area_slug}] {area_name}，共 {len(entries)} 篇 ===")

    for entry in entries:
        url = entry.get("url", "").strip()
        name = entry.get("name", "").strip()
        page_id = entry.get("page_id", "")
        if not url:
            print(f"  跳过（无 url）: {entry}")
            continue
        if entry.get("done"):
            continue

        aid = _extract_arxiv_id(url)
        entry_key = aid if aid else re.sub(r"[^\w]", "_", url)[:60]

        if aid:
            yy, mm = aid[:2], aid[2:4]
            paper_date = f"20{yy}-{mm}"
        elif entry.get("date"):
            paper_date = entry["date"].strip()
        else:
            paper_date = today

        cache_file = _cache_path(area_slug, entry_key)
        cached = _load_cache(cache_file)

        if cached:
            print(f"  命中缓存: {name or entry_key}")
            result = cached
        else:
            print(f"  解析中: {name or url}")
            if dry_run:
                print(f"  [dry-run] 跳过 LLM 调用")
                continue
            try:
                result = analyzer.deep_analyze(url)
            except Exception as e:
                print(f"  解析失败: {e}", file=sys.stderr)
                continue
            _save_cache(cache_file, result)

        title = result.get("title") or name or entry_key
        md_content = _build_md(result)

        if dry_run:
            print(f"  [dry-run] 将同步: [{paper_date}] {title}")
            continue

        file_renderer.sync(area_slug, area_name, paper_date, title, md_content, arxiv_id=result.get("arxiv_id"))
        if notion_renderer:
            try:
                notion_renderer.sync(area_slug, area_name, paper_date, title, md_content, arxiv_id=result.get("arxiv_id"))
            except Exception as e:
                print(f"  Notion 同步失败: {e}", file=sys.stderr)
                continue

        # 写回 Notion done 复选框
        if page_id:
            try:
                config_reader.set_done(page_id, True)
                print(f"  [notion] 已标记 done: {name or entry_key}")
            except Exception as e:
                print(f"  [notion] 标记 done 失败: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Area 论文处理器")
    parser.add_argument("--area", help="只处理指定 area slug（如 3d-gen-rec）")
    parser.add_argument("--dry-run", action="store_true", help="只打印，不写入")
    parser.add_argument("--no-notion", action="store_true", help="跳过 Notion 同步")
    args = parser.parse_args()

    api_key = os.getenv("MY_API_KEY")
    if not api_key:
        print("错误：请设置环境变量 MY_API_KEY", file=sys.stderr)
        sys.exit(1)

    notion_token = os.getenv("NOTION_TOKEN")
    if not notion_token:
        print("错误：请设置环境变量 NOTION_TOKEN", file=sys.stderr)
        sys.exit(1)

    _set_pipeline_log_path(None)
    analyzer = PaperAnalyzer(api_key, cfg=PipelineConfig(), cache_dir="output/cache/analyzer")
    file_renderer = FileRenderer()
    notion_renderer = None if args.no_notion else NotionRenderer()
    config_reader = NotionConfigReader(notion_token)

    # 从 Notion 读取所有 area 数据库
    all_dbs = config_reader.list_area_databases()
    print(f"从 Notion area_config 读取到 {len(all_dbs)} 个 area 数据库")
    for db in all_dbs:
        print(f"  [{db['slug']}] id={db['id']}")

    if args.area:
        dbs = [db for db in all_dbs if db["slug"] == args.area]
        if not dbs:
            print(f"错误：未找到 area '{args.area}'，可用: {[db['slug'] for db in all_dbs]}", file=sys.stderr)
            sys.exit(1)
    else:
        dbs = all_dbs

    for db in dbs:
        entries = config_reader.query_entries(db["id"])
        process_area(
            db["slug"], entries, analyzer, notion_renderer, file_renderer, config_reader,
            dry_run=args.dry_run,
        )


if __name__ == "__main__":
    main()
