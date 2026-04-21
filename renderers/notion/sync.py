import os
import sys
import time
import requests as req
from renderers.base import AreaRenderer


class NotionRenderer(AreaRenderer):
    def __init__(self):
        token = os.environ.get("NOTION_TOKEN")
        if not token:
            print("错误: 未检测到环境变量 NOTION_TOKEN", file=sys.stderr)
            sys.exit(1)
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2026-03-11",
        }
        self.root_id = os.environ.get("NOTION_ROOT_PAGE_ID", "347e1dce83648023abdde32fa8065aac").replace("-", "")
        self.base_url = "https://api.notion.com/v1"

    def _get_child_pages(self, parent_id: str) -> list[dict]:
        """列举 parent 下所有 child_page block，返回 [{id, title}]。"""
        pages = []
        url = f"{self.base_url}/blocks/{parent_id}/children?page_size=100"
        while url:
            resp = req.get(url, headers=self.headers)
            if resp.status_code >= 400:
                print(f"  [notion] 列举子页面失败 {resp.status_code}: {resp.text[:200]}", file=sys.stderr)
                break
            data = resp.json()
            for block in data.get("results", []):
                if block.get("type") == "child_page":
                    title = block.get("child_page", {}).get("title", "")
                    pages.append({"id": block["id"], "title": title})
            if data.get("has_more"):
                url = f"{self.base_url}/blocks/{parent_id}/children?page_size=100&start_cursor={data['next_cursor']}"
            else:
                url = None
        return pages

    def _find_or_create_area(self, area_name: str) -> str:
        children = self._get_child_pages(self.root_id)
        print(f"  [notion] root 下共 {len(children)} 个子页面")

        for child in children:
            print(f"  [notion]   子页面: '{child['title']}' id={child['id']}")
            if child["title"].lower() == area_name.lower():
                print(f"  [notion]   匹配 ✓ 使用已有 area")
                return child["id"]

        # 未找到，创建
        print(f"  [notion] 未找到 '{area_name}'，创建新 area 页面...")
        resp = req.post(f"{self.base_url}/pages", headers=self.headers, json={
            "parent": {"page_id": self.root_id},
            "properties": {"title": {"title": [{"text": {"content": area_name}}]}},
        })
        if resp.status_code >= 400:
            raise RuntimeError(f"Notion API 创建 area 失败 {resp.status_code}: {resp.text[:200]}")
        new_id = resp.json()["id"]
        print(f"  [notion] 已创建: {area_name} → {new_id}")
        return new_id

    def _is_duplicate(self, area_id: str, display_title: str) -> bool:
        children = self._get_child_pages(area_id)
        for child in children:
            if child["title"].lower() == display_title.lower():
                return True
        return False

    def sync(self, area_slug: str, area_name: str, paper_date: str, paper_title: str, md_content: str, arxiv_id: str | None = None) -> None:
        display_title = f"[{paper_date}] {paper_title}"
        area_id = self._find_or_create_area(area_name)

        if self._is_duplicate(area_id, display_title):
            print(f"  [notion] 跳过(已存在): {display_title}")
            return

        resp = req.post(f"{self.base_url}/pages", headers=self.headers, json={
            "parent": {"page_id": area_id},
            "properties": {"title": {"title": [{"text": {"content": display_title}}]}},
            "markdown": md_content,
        })

        if resp.status_code >= 400:
            raise RuntimeError(f"Notion API {resp.status_code}: {resp.text[:200]}")

        print(f"  [notion] 已同步: {display_title} → {area_name} (area_id={area_id})")
        time.sleep(0.3)
