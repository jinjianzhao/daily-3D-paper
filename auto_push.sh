#!/bin/bash
set -e  # 遇到错误立即退出

# ============================
# 自动尝试 push 脚本（当前路径，main 分支）
# ============================
BRANCH="main"

# 检查是否是 Git 仓库
if [ ! -d ".git" ]; then
    echo "当前目录不是 Git 仓库！"
    exit 1
fi

# 检查是否有修改
if ! git diff-index --quiet HEAD --; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') 检测到修改，正在提交并 push..."
    git add .
    git commit -m "Auto commit $(date '+%Y-%m-%d %H:%M:%S')"
    git push origin "$BRANCH"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') 没有修改，跳过 push"
fi