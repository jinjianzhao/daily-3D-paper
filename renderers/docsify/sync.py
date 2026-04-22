"""
DocsifyRenderer：从 date 流水线的 config.json 数据生成 docsify 兼容的 .md 文件。

输出结构（在 pub_dir 下）：
  README.md       — 当天概览
  _sidebar.md     — 当天侧边栏
  briefs.md       — 全量简报
  papers/{aid}.md  — 每篇重点论文
"""

import os
import re

from renderers.docsify.paper import render_paper_md


def _split_step04_summary(text: str) -> tuple[str, str, str]:
    """解析 step04 摘要格式：第1行=15字一句话，第2行=标签，第3行起=4行摘要。"""
    lines = text.strip().split("\n")
    short = lines[0] if lines else ""
    tags = lines[1] if len(lines) > 1 else ""
    body = "\n".join(lines[2:]) if len(lines) > 2 else ""
    return short, tags, body


def _extract_method_name(title: str) -> str:
    """从论文标题提取方法缩写。
    优先取冒号前的部分（如 'HY-World 2.0'），
    否则取前两个单词加省略号。
    """
    if ":" in title:
        before_colon = title.split(":")[0].strip()
        if len(before_colon) <= 40:
            return before_colon
    words = title.split()
    if len(words) <= 2:
        return title
    return " ".join(words[:2]) + "..."


class DocsifyRenderer:
    def render_date(self, pub_dir: str, config_data: dict, hf_votes: dict) -> None:
        date_str = config_data["date"]
        base_info = config_data.get("base_info", {})
        summaries = config_data.get("summaries", {})
        deep_analysis = config_data.get("deep_analysis", {})
        images_meta = config_data.get("images_meta", {})
        focus_sections = config_data.get("focus_sections", {})
        focus_ids = config_data.get("focus_ids", [])
        date_dir_name = os.path.basename(pub_dir)

        papers_dir = os.path.join(pub_dir, "papers")
        os.makedirs(papers_dir, exist_ok=True)

        for aid in focus_ids:
            self._render_paper(
                papers_dir, aid, base_info, summaries, deep_analysis, images_meta, hf_votes
            )

        self._render_readme(pub_dir, date_str, date_dir_name, base_info, summaries, focus_sections, focus_ids, hf_votes)
        sidebar_content = self._render_sidebar(pub_dir, date_str, date_dir_name, base_info, summaries, focus_sections, focus_ids)

        # papers/ 下也放一份相同的 sidebar，否则 docsify 在论文页面找不到
        papers_sidebar = os.path.join(papers_dir, "_sidebar.md")
        with open(papers_sidebar, "w", encoding="utf-8") as f:
            f.write(sidebar_content)

    def _render_paper(
        self, papers_dir, aid, base_info, summaries, deep_analysis, images_meta, hf_votes
    ):
        info = base_info.get(aid, {})
        title = info.get("title", aid)
        hf_link = info.get("hf_link", "")
        summary_text = summaries.get(aid, "")
        short_zh, tags, body_summary = _split_step04_summary(summary_text)
        deep = deep_analysis.get(aid, "")
        imgs = images_meta.get(aid, [])
        votes = hf_votes.get(aid, 0)

        paper = {
            "title": title,
            "arxiv_id": aid,
            "hf_link": hf_link,
            "hf_votes": votes,
            "short_zh": short_zh,
            "tags": tags,
            "body_summary": body_summary,
            "deep_analysis": deep,
            "figures": imgs,
        }

        md = render_paper_md(paper)
        fp = os.path.join(papers_dir, f"{aid}.md")
        with open(fp, "w", encoding="utf-8") as f:
            f.write(md)

    def _render_readme(
        self, pub_dir, date_str, date_dir_name, base_info, summaries, focus_sections, focus_ids, hf_votes
    ):
        total = len(base_info)
        focus_count = len(set(focus_ids))
        focus_id_set = set(focus_ids)

        lines = []
        lines.append(f"# {date_str} 3D 论文日报")
        lines.append("")
        lines.append(f"共 **{total}** 篇，重点 **{focus_count}** 篇")
        lines.append("")

        if focus_sections:
            lines.append("## 重点论文")
            lines.append("")
            for sec_name, aids in focus_sections.items():
                if not aids:
                    continue
                lines.append(f"### {sec_name}")
                lines.append("")
                for aid in aids:
                    title = base_info.get(aid, {}).get("title", aid)
                    method = _extract_method_name(title)
                    short_zh, _, _ = _split_step04_summary(summaries.get(aid, ""))
                    label = f"**{method}**"
                    if short_zh:
                        label += f" | {short_zh}"
                    label += f" | {title}"
                    lines.append(f"- [{label}](/{date_dir_name}/papers/{aid}.md)")
                lines.append("")

        non_focus = [aid for aid in base_info if aid not in focus_id_set]
        if non_focus:
            lines.append(f"## [全量简报](/{date_dir_name}/briefs.md)")
            lines.append("")
            lines.append("| 简称 | 简介 | 领域 | 论文全名 | Votes |")
            lines.append("|------|------|------|----------|------:|")
            for aid in non_focus:
                title = base_info.get(aid, {}).get("title", aid)
                method = _extract_method_name(title)
                short_zh, tags, _ = _split_step04_summary(summaries.get(aid, ""))
                votes = hf_votes.get(aid, 0)
                votes_str = str(votes) if votes else ""
                anchor = method.lower().replace(" ", "-").replace(".", "").replace(":", "")
                lines.append(f"| [**{method}**](/{date_dir_name}/briefs.md?id={anchor}) | {short_zh} | {tags} | {title} | {votes_str} |")
            lines.append("")

            self._render_briefs(pub_dir, date_str, date_dir_name, non_focus, base_info, summaries, hf_votes)

        fp = os.path.join(pub_dir, "README.md")
        with open(fp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def _render_sidebar(self, pub_dir, date_str, date_dir_name, base_info, summaries, focus_sections, focus_ids):
        focus_id_set = set(focus_ids)

        lines = []
        lines.append(f"- [**{date_str} 日报**](/{date_dir_name}/)")
        lines.append("")

        for sec_name, aids in focus_sections.items():
            if not aids:
                continue
            lines.append(f"  - **{sec_name}**")
            for aid in aids:
                title = base_info.get(aid, {}).get("title", aid)
                method = _extract_method_name(title)
                short_zh, _, _ = _split_step04_summary(summaries.get(aid, ""))
                label = f"{method} | {short_zh}" if short_zh else method
                lines.append(f"    - [{label}](/{date_dir_name}/papers/{aid}.md)")

        non_focus = [aid for aid in base_info if aid not in focus_id_set]
        if non_focus:
            lines.append(f"  - [**全量简报 ({len(non_focus)} 篇)**](/{date_dir_name}/briefs.md)")
            for aid in non_focus:
                title = base_info.get(aid, {}).get("title", aid)
                method = _extract_method_name(title)
                short_zh, _, _ = _split_step04_summary(summaries.get(aid, ""))
                label = f"{method} | {short_zh}" if short_zh else method
                anchor = method.lower().replace(" ", "-").replace(".", "").replace(":", "")
                lines.append(f"    - [{label}](/{date_dir_name}/briefs.md?id={anchor})")

        fp = os.path.join(pub_dir, "_sidebar.md")
        content = "\n".join(lines)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        return content

    def _render_briefs(self, pub_dir, date_str, date_dir_name, non_focus_ids, base_info, summaries, hf_votes):
        from renderers.docsify.paper import render_paper_md

        all_lines = []
        all_lines.append(f"# {date_str} 全量简报")
        all_lines.append("")

        for aid in non_focus_ids:
            info = base_info.get(aid, {})
            title = info.get("title", aid)
            hf_link = info.get("hf_link", "")
            summary_text = summaries.get(aid, "")
            short_zh, tags, body_summary = _split_step04_summary(summary_text)
            votes = hf_votes.get(aid, 0)

            paper = {
                "title": title,
                "arxiv_id": aid,
                "hf_link": hf_link,
                "hf_votes": votes,
                "short_zh": short_zh,
                "tags": tags,
                "body_summary": body_summary,
                "deep_analysis": "",  # briefs 不放深度解析
                "figures": [],
            }
            all_lines.append(render_paper_md(paper))
            all_lines.append("---\n")

        fp = os.path.join(pub_dir, "briefs.md")
        with open(fp, "w", encoding="utf-8") as f:
            f.write("\n".join(all_lines))
