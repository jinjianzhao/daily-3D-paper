"""
renderers/docsify/paper.py

单篇论文 md 渲染的公共逻辑，供 date 流水线（DocsifyRenderer）和
area 流水线（area_processor._build_md）共用。

标准 paper dict 格式：
{
    "title": str,
    "arxiv_id": str | None,
    "hf_link": str,
    "hf_votes": int,
    "short_zh": str,       # 15字一句话
    "tags": str,           # 领域标签
    "body_summary": str,   # 4行简要摘要
    "deep_analysis": str,
    "figures": [{"path": str, "caption_zh": str, ...}],
}
"""

import re


def _extract_method_name(title: str) -> str:
    if ":" in title:
        before_colon = title.split(":")[0].strip()
        if len(before_colon) <= 40:
            return before_colon
    words = title.split()
    if len(words) <= 2:
        return title
    return " ".join(words[:2]) + "..."


def render_paper_md(paper: dict, html_figure: bool = True, include_title: bool = True) -> str:
    """渲染单篇论文为 markdown 字符串。

    html_figure=True  → docsify 用，<figure> 居中 + 限高
    html_figure=False → Notion 等纯 markdown 环境，用 ![caption](url)
    include_title=True → 输出 # 标题行（docsify 独立页面用）
    include_title=False → 跳过标题行（Notion 页面已有标题时用）
    """
    title = paper.get("title", "")
    arxiv_id = paper.get("arxiv_id")
    hf_link = paper.get("hf_link", "")
    hf_votes = paper.get("hf_votes", 0)
    short_zh = paper.get("short_zh", "")
    tags = paper.get("tags", "")
    body_summary = paper.get("body_summary", "")
    deep = paper.get("deep_analysis", "")
    imgs = paper.get("figures", [])

    lines = []

    if include_title:
        lines.append(f"# {title}")
        lines.append("")

    if short_zh:
        lines.append(f"**【{short_zh}】**")
        lines.append("")

    if arxiv_id:
        lines.append(f"**arXiv**: https://arxiv.org/abs/{arxiv_id}  ")
        lines.append(f"**AlphaXiv**: https://www.alphaxiv.org/zh/overview/{arxiv_id}  ")
    if hf_link:
        lines.append(f"**HF Paper**: {hf_link}  ")
    if hf_votes:
        lines.append(f"**HF Votes**: {hf_votes}")
    lines.append("")

    if body_summary:
        lines.append("## 简要摘要")
        lines.append("")
        if tags:
            lines.append(f"*{tags}*")
            lines.append("")
        lines.append(body_summary)
        lines.append("")

    if imgs:
        lines.append("## 图示")
        lines.append("")
        for img in imgs:
            path = img.get("path", "")
            caption_zh = img.get("caption_zh", "") or img.get("caption", "")
            if path:
                if html_figure:
                    lines.append('<figure style="margin:0 auto 1.5em auto; text-align:center">')
                    lines.append(f'  <img src="{path}" style="max-height:60vw; max-width:100%; height:auto; display:inline-block">')
                    if caption_zh:
                        lines.append(f'  <figcaption style="color:#666; font-size:0.85em; margin-top:0.4em">{caption_zh}</figcaption>')
                    lines.append('</figure>')
                else:
                    lines.append(f"![{caption_zh}]({path})")
                    if caption_zh:
                        lines.append(f"*{caption_zh}*")
                lines.append("")

    if deep:
        lines.append("## 深度解析")
        lines.append("")
        lines.append(deep)
        lines.append("")

    return "\n".join(lines)


def paper_dict_from_analyzer_result(result: dict, hf_link: str = "", hf_votes: int = 0) -> dict:
    """把 paper_analyzer.deep_analyze() 的返回值转成标准 paper dict。"""
    summary_text = result.get("summary", "")
    lines = summary_text.strip().split("\n") if summary_text else []
    short_zh = lines[0] if lines else ""
    tags = lines[1] if len(lines) > 1 else ""
    body_summary = "\n".join(lines[2:]) if len(lines) > 2 else ""

    arxiv_id = result.get("arxiv_id")
    if not hf_link and arxiv_id:
        hf_link = f"https://huggingface.co/papers/{arxiv_id}"

    return {
        "title": result.get("title", ""),
        "arxiv_id": arxiv_id,
        "hf_link": hf_link,
        "hf_votes": hf_votes,
        "short_zh": short_zh,
        "tags": tags,
        "body_summary": body_summary,
        "deep_analysis": result.get("deep_analysis", ""),
        "figures": result.get("figures", []),
    }
