"""
Docsify 全局索引生成：全局 _sidebar.md、入口 index.html、.nojekyll。
"""

import os


DOCSIFY_HTML = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Daily 3D Paper</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify@4/lib/themes/vue.css">
</head>
<body>
  <div id="app"></div>
  <script>
    window.$docsify = {
      name: 'Daily 3D Paper',
      loadSidebar: true,
      subMaxLevel: 3,
      auto2top: true,
      homepage: '{{HOMEPAGE}}',
    };
  </script>
  <script src="//cdn.jsdelivr.net/npm/docsify@4/lib/docsify.min.js"></script>
  <script src="//cdn.jsdelivr.net/npm/docsify/lib/plugins/zoom-image.min.js"></script>
</body>
</html>
"""


def ensure_docsify_entry(docs_date_dir: str) -> None:
    """确保 docsify 入口 docsify.html、README.md 和 .nojekyll 存在。"""
    date_dirs = []
    for name in sorted(os.listdir(docs_date_dir)):
        sub = os.path.join(docs_date_dir, name)
        if os.path.isdir(sub) and len(name) == 10 and name[4] == "-" and name[7] == "-":
            date_dirs.append(name)

    # 生成根 README.md 作为日期索引
    readme_lines = []
    readme_lines.append("# Daily 3D Paper")
    readme_lines.append("")
    readme_lines.append("选择日期查看当日论文报告：")
    readme_lines.append("")
    for d in reversed(date_dirs):  # 最新的在前
        readme_lines.append(f"- [{d}](/{d}/)")
    readme_lines.append("")

    readme_path = os.path.join(docs_date_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(readme_lines))

    # docsify.html 指向根 README.md
    html = DOCSIFY_HTML.replace("{{HOMEPAGE}}", "README.md")
    entry_path = os.path.join(docs_date_dir, "docsify.html")
    with open(entry_path, "w", encoding="utf-8") as f:
        f.write(html)

    nojekyll = os.path.join(docs_date_dir, ".nojekyll")
    with open(nojekyll, "w") as f:
        f.write("")


def update_global_sidebar(docs_date_dir: str) -> None:
    """扫描 docs_date_dir 下所有日期子目录，生成顶层 _sidebar.md。"""
    if not os.path.isdir(docs_date_dir):
        return

    # 找出所有日期目录（格式 YYYY-MM-DD）
    date_dirs = []
    for name in sorted(os.listdir(docs_date_dir)):
        sub = os.path.join(docs_date_dir, name)
        if os.path.isdir(sub) and len(name) == 10 and name[4] == "-" and name[7] == "-":
            date_dirs.append(name)

    lines = []
    for d in reversed(date_dirs):  # 最新的在前面
        lines.append(f"- [{d}]({d}/)")
    lines.append("")
    lines.append("- [**Docsify 使用说明**]")
    lines.append("  - 按日期浏览：左侧边栏选择日期")
    lines.append("  - 论文页面内可点击图片放大")
    lines.append("  - HF Votes 数字越大表示当日热度越高")

    sidebar_path = os.path.join(docs_date_dir, "_sidebar.md")
    with open(sidebar_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
