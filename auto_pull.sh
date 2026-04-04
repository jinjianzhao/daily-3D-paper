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

git pull
