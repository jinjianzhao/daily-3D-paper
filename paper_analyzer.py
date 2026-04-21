"""
独立论文解析脚本：支持 arXiv 和通用网页。

用法：
    python paper_analyzer.py summarize "https://arxiv.org/abs/2404.12345"
    python paper_analyzer.py deep_analyze "https://arxiv.org/abs/2404.12345"
    python paper_analyzer.py deep_analyze "https://some-project-page.com"

输出 JSON 到 stdout，缓存写入 output/cache/analyzer/
"""

import os
import re
import sys
import json
import argparse
from run_pipeline import (
    PaperPipeline,
    PipelineConfig,
    pipeline_debug,
    _set_pipeline_log_path,
    PROMPT_STEP04_SUMMARY,
    PROMPT_STEP06_DEEP,
)
import requests
from bs4 import BeautifulSoup


def _extract_arxiv_id(url: str) -> str | None:
    """从 URL 中提取 arXiv ID，如 2404.12345。"""
    m = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", url)
    return m.group(1) if m else None


def _is_arxiv_url(url: str) -> bool:
    return "arxiv.org" in url and _extract_arxiv_id(url) is not None


def _is_local_pdf(path: str) -> bool:
    return path.endswith(".pdf") and not path.startswith("http")


def _is_notion_url(url: str) -> bool:
    return "notion.so/" in url or "notion.site/" in url


def _extract_notion_page_id(url: str) -> str | None:
    """从 Notion URL 提取 32 位 page ID。"""
    m = re.search(r"([0-9a-f]{32})\s*$", url.rstrip("/"))
    return m.group(1) if m else None


def _read_pdf_text(path: str) -> str:
    """用 PyMuPDF 提取 PDF 全文文本，噪声由 LLM 消化。"""
    import fitz
    doc = fitz.open(path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return "\n".join(pages)


def _fetch_webpage(url: str, timeout: int = 30) -> dict:
    """通用网页抓取：返回 {title, text, html}。"""
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # 提取标题
    title = ""
    title_tag = soup.find("title")
    if title_tag:
        title = title_tag.get_text(strip=True)
    # 尝试 og:title
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        title = og["content"]
    # 尝试 h1
    if not title:
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(strip=True)

    # 提取正文
    text = soup.get_text(separator=" ", strip=True)

    # 提取图片
    images = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if not src or src.startswith("data:"):
            continue
        if not src.startswith("http"):
            # 相对路径转绝对
            from urllib.parse import urljoin
            src = urljoin(url, src)
        alt = img.get("alt", "")
        images.append({"path": src, "caption": alt})

    return {"title": title, "text": text, "html": resp.text, "images": images}


class PaperAnalyzer:
    """独立论文解析器，复用 PaperPipeline 的 LLM 和 arXiv 基础设施。"""

    def __init__(self, api_key: str, cfg: PipelineConfig | None = None, cache_dir: str = "output/cache/analyzer"):
        self.cfg = cfg or PipelineConfig()
        self.pipeline = PaperPipeline(api_key, self.cfg)
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def summarize(self, url: str) -> dict:
        """简要解析：标题 + 摘要 + 4行摘要。"""
        if _is_local_pdf(url):
            return self._summarize_pdf(url)
        if _is_arxiv_url(url):
            return self._summarize_arxiv(url)
        return self._summarize_generic(url)

    def deep_analyze(self, url: str) -> dict:
        """深度解析：摘要 + 深度分析 + 关键图 + 图注翻译。"""
        if _is_local_pdf(url):
            return self._deep_analyze_pdf(url)
        if _is_notion_url(url):
            return self._deep_analyze_notion(url)
        if _is_arxiv_url(url):
            return self._deep_analyze_arxiv(url)
        return self._deep_analyze_generic(url)

    # ---- arXiv 路径 ----

    def _summarize_arxiv(self, url: str) -> dict:
        aid = _extract_arxiv_id(url)
        cache_abs = os.path.join(self.cache_dir, "arxiv_abs")
        details = self.pipeline.get_arxiv_details(aid, cache_abs)
        title = details.get("title", "")
        abstract = details["abstract"]

        # 如果 get_arxiv_details 没返回 title，从 abs 页面抓
        if not title:
            title = self._fetch_arxiv_title(aid)

        summary = self.pipeline._post_chat_completion(
            PROMPT_STEP04_SUMMARY.format(title=title, abstract=abstract)
        )

        return {
            "arxiv_id": aid,
            "url": url,
            "title": title,
            "abstract": abstract,
            "summary": summary,
        }

    def _deep_analyze_arxiv(self, url: str) -> dict:
        aid = _extract_arxiv_id(url)

        # step 1: 摘要
        result = self._summarize_arxiv(url)

        # step 2: 下载 HTML + 深度解析
        html_cache = os.path.join(self.cache_dir, "arxiv_html")
        h_p, t_p = self.pipeline.download_arxiv_html(aid, html_cache)

        deep_analysis = ""
        figures = []

        if os.path.exists(h_p):
            with open(t_p, "r", encoding="utf-8") as f:
                clean_txt = f.read()
            with open(h_p, "r", encoding="utf-8") as f:
                full_html = f.read()

            # 深度解析
            deep_analysis = self.pipeline._post_chat_completion(
                PROMPT_STEP06_DEEP.format(
                    paper_body_excerpt=clean_txt[: self.cfg.deep_body_max_chars]
                )
            )

            # 抽图
            img_cache = os.path.join(self.cache_dir, "images")
            raw_meta = self.pipeline.extract_images_from_html(
                full_html, aid, img_cache,
                debug_step="analyzer", debug_title="抽取图示",
            )

            if raw_meta:
                # 选关键图
                if len(raw_meta) == 1:
                    k_sel = self.cfg.key_figure_count
                    selected = [
                        {"path": raw_meta[0]["path"], "caption": raw_meta[0]["caption"],
                         "role": self.pipeline._pipeline_role_for_slot(i)}
                        for i in range(1, k_sel + 1)
                    ]
                else:
                    select_cache = os.path.join(self.cache_dir, "key_figure_select")
                    selected = self.pipeline.select_key_figures_by_caption_two_round(
                        raw_meta, aid, select_cache, force_rerun=False,
                        debug_step="analyzer", debug_title="关键图选择",
                    )

                # 图注翻译
                caption_cache = os.path.join(self.cache_dir, "caption_zh")
                figures = self.pipeline.translate_figure_captions(
                    selected, aid, caption_cache,
                    debug_step="analyzer", debug_title="图注翻译",
                )
        else:
            pipeline_debug("analyzer", "深度解析", f"arXiv HTML 不可用 aid={aid}，仅输出摘要")

        result["deep_analysis"] = deep_analysis
        result["figures"] = figures
        return result

    def _fetch_arxiv_title(self, aid: str) -> str:
        """从 arXiv abs 页面抓取标题。"""
        try:
            resp = requests.get(
                f"{self.cfg.arxiv_abs_base_url}{aid}",
                headers={"User-Agent": self.cfg.http_user_agent},
                timeout=self.cfg.timeout_arxiv_abs_sec,
            )
            soup = BeautifulSoup(resp.text, "html.parser")
            title_tag = soup.find("h1", class_="title")
            if title_tag:
                return title_tag.get_text(strip=True).replace("Title:", "").strip()
        except Exception:
            pass
        return ""

    # ---- Notion 页面路径 ----

    def _fetch_notion_page(self, url: str) -> dict:
        """从 Notion 页面提取标题、正文、图片+图注。"""
        import requests as notion_req
        page_id = _extract_notion_page_id(url)
        if not page_id:
            raise ValueError(f"无法从 URL 提取 Notion page ID: {url}")

        notion_token = os.environ.get("NOTION_TOKEN", "")
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

        # 读取页面标题
        resp = notion_req.get(
            f"https://api.notion.com/v1/pages/{page_id}",
            headers=headers,
        )
        resp.raise_for_status()
        page_data = resp.json()
        title = ""
        for k, v in page_data.get("properties", {}).items():
            if v.get("type") == "title":
                texts = v.get("title", [])
                title = "".join(t["plain_text"] for t in texts)
                break

        # 读取子 blocks
        all_blocks = []
        next_url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
        while next_url:
            resp = notion_req.get(next_url, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            all_blocks.extend(data.get("results", []))
            if data.get("has_more"):
                next_url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100&start_cursor={data['next_cursor']}"
            else:
                next_url = None

        text_parts = []
        figures = []
        pending_image = None

        for b in all_blocks:
            t = b["type"]

            if t == "image":
                img_data = b["image"]
                if img_data["type"] == "file":
                    img_url = img_data["file"]["url"]
                elif img_data["type"] == "external":
                    img_url = img_data["external"]["url"]
                else:
                    continue
                caption_parts = img_data.get("caption", [])
                caption = "".join(c["plain_text"] for c in caption_parts)
                pending_image = {"path": img_url, "caption": caption, "caption_zh": ""}
                continue

            # 提取文本
            block_text = ""
            if t in ("paragraph", "heading_1", "heading_2", "heading_3",
                      "bulleted_list_item", "numbered_list_item", "quote"):
                rich_texts = b[t].get("rich_text", [])
                block_text = "".join(rt["plain_text"] for rt in rich_texts)

            # 图片后面紧跟的段落当作图注
            if pending_image is not None:
                if block_text.lower().startswith("figure") or block_text.lower().startswith("fig"):
                    pending_image["caption"] = block_text
                figures.append(pending_image)
                pending_image = None

            if block_text:
                text_parts.append(block_text)

        if pending_image is not None:
            figures.append(pending_image)

        return {
            "title": title,
            "text": "\n".join(text_parts),
            "figures": figures[:self.cfg.max_figures_per_paper],
        }

    def _deep_analyze_notion(self, url: str) -> dict:
        page = self._fetch_notion_page(url)
        title = page["title"]
        text = page["text"]

        # LLM 提取摘要
        text_excerpt = text[:4000]
        prompt_extract = f"""以下是一篇论文的标题和正文片段，请提取核心摘要（abstract）。
只输出摘要文本，不要其他说明。

【标题】
{title}

【正文片段】
{text_excerpt}
"""
        abstract = self.pipeline._post_chat_completion(prompt_extract)
        summary = self.pipeline._post_chat_completion(
            PROMPT_STEP04_SUMMARY.format(title=title, abstract=abstract)
        )

        # LLM 深度解析
        deep_text = text[:self.cfg.deep_body_max_chars]
        deep_analysis = self.pipeline._post_chat_completion(
            PROMPT_STEP06_DEEP.format(paper_body_excerpt=deep_text)
        )

        # 图注翻译
        figures = page["figures"]
        if figures:
            caption_cache = os.path.join(self.cache_dir, "caption_zh")
            page_id = _extract_notion_page_id(url)
            figures = self.pipeline.translate_figure_captions(
                figures, page_id or "notion", caption_cache,
                debug_step="analyzer", debug_title="图注翻译",
            )

        return {
            "arxiv_id": None,
            "url": url,
            "title": title,
            "abstract": abstract,
            "summary": summary,
            "deep_analysis": deep_analysis,
            "figures": figures,
        }

    # ---- 通用网页路径 ----

    def _summarize_generic(self, url: str) -> dict:
        page = _fetch_webpage(url)
        title = page["title"]
        # 截取正文前 4000 字符让 LLM 提取摘要
        text_excerpt = page["text"][:4000]

        prompt_extract = f"""以下是一个网页的标题和正文片段，请提取这篇论文/文章的核心摘要（abstract）。
如果不是论文，请根据内容写一段 200 字以内的摘要。只输出摘要文本，不要其他说明。

【标题】
{title}

【正文片段】
{text_excerpt}
"""
        abstract = self.pipeline._post_chat_completion(prompt_extract)

        summary = self.pipeline._post_chat_completion(
            PROMPT_STEP04_SUMMARY.format(title=title, abstract=abstract)
        )

        return {
            "arxiv_id": None,
            "url": url,
            "title": title,
            "abstract": abstract,
            "summary": summary,
        }

    def _deep_analyze_generic(self, url: str) -> dict:
        result = self._summarize_generic(url)
        page = _fetch_webpage(url)

        text_excerpt = page["text"][:self.cfg.deep_body_max_chars]

        deep_analysis = self.pipeline._post_chat_completion(
            PROMPT_STEP06_DEEP.format(paper_body_excerpt=text_excerpt)
        )

        # 尝试从网页抓图（取前 8 张有意义的图片）
        figures = []
        for img in page["images"][:self.cfg.max_figures_per_paper]:
            if img["path"] and not img["path"].endswith((".svg", ".gif", ".ico")):
                figures.append({
                    "path": img["path"],
                    "caption": img["caption"] or "Figure from page",
                    "caption_zh": "",
                    "role": "",
                })

        result["deep_analysis"] = deep_analysis
        result["figures"] = figures
        return result

    # ---- 本地 PDF 路径 ----

    def _summarize_pdf(self, path: str) -> dict:
        text = _read_pdf_text(path)
        title = os.path.splitext(os.path.basename(path))[0]
        text_excerpt = text[:4000]

        prompt_extract = f"""以下是一篇 PDF 论文的文本内容（可能含排版噪声），请提取核心摘要（abstract）。
只输出摘要文本，不要其他说明。

【正文片段】
{text_excerpt}
"""
        abstract = self.pipeline._post_chat_completion(prompt_extract)
        summary = self.pipeline._post_chat_completion(
            PROMPT_STEP04_SUMMARY.format(title=title, abstract=abstract)
        )
        return {
            "arxiv_id": None,
            "url": path,
            "title": title,
            "abstract": abstract,
            "summary": summary,
        }

    def _deep_analyze_pdf(self, path: str) -> dict:
        result = self._summarize_pdf(path)
        text = _read_pdf_text(path)
        text_excerpt = text[:self.cfg.deep_body_max_chars]
        deep_analysis = self.pipeline._post_chat_completion(
            PROMPT_STEP06_DEEP.format(paper_body_excerpt=text_excerpt)
        )
        result["deep_analysis"] = deep_analysis
        result["figures"] = []
        return result


def main():
    parser = argparse.ArgumentParser(description="独立论文解析脚本")
    parser.add_argument("action", choices=["summarize", "deep_analyze"], help="解析模式")
    parser.add_argument("url", help="论文 URL（arXiv 或通用网页）")
    parser.add_argument("--cache-dir", default="output/cache/analyzer", help="缓存目录")
    parser.add_argument("--pretty", action="store_true", help="格式化 JSON 输出")
    args = parser.parse_args()

    api_key = os.getenv("MY_API_KEY")
    if not api_key:
        print("错误：请设置环境变量 MY_API_KEY", file=sys.stderr)
        sys.exit(1)

    _set_pipeline_log_path(None)
    analyzer = PaperAnalyzer(api_key, cache_dir=args.cache_dir)

    if args.action == "summarize":
        result = analyzer.summarize(args.url)
    else:
        result = analyzer.deep_analyze(args.url)

    indent = 2 if args.pretty else None
    print(json.dumps(result, ensure_ascii=False, indent=indent))


if __name__ == "__main__":
    main()
