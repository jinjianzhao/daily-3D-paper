import os
import re
from renderers.base import AreaRenderer


def _slugify(text: str) -> str:
    """将标题转为文件名安全的 slug。"""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text[:50]


class FileRenderer(AreaRenderer):
    def __init__(self, base_dir: str = "areas/papers"):
        self.base_dir = base_dir

    def sync(self, area_slug: str, area_name: str, paper_date: str, paper_title: str, md_content: str, arxiv_id: str | None = None) -> None:
        area_dir = os.path.join(self.base_dir, area_slug)
        os.makedirs(area_dir, exist_ok=True)

        title_slug = _slugify(paper_title)
        filename = f"{paper_date}_{title_slug}.md"
        filepath = os.path.join(area_dir, filename)

        if os.path.exists(filepath):
            print(f"跳过(已存在): {filepath}")
            return

        header = f"# [{paper_date}] {paper_title}\n\n"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(header + md_content)

        print(f"已写入: {filepath}")
