from abc import ABC, abstractmethod


class AreaRenderer(ABC):
    @abstractmethod
    def sync(self, area_slug: str, area_name: str, paper_date: str, paper_title: str, md_content: str, arxiv_id: str | None = None) -> None:
        """同步一篇论文到目标（Notion / 文件系统 / …）。"""
        ...
