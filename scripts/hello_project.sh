#!/bin/bash
#这是一个简单的项目入口脚本，用于展示项目信息。

#___ 关键步骤：确保脚本从项目根目录执行 ___
#获取脚本所在的目录
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
#切换到项目根目录（即脚本所在目录的上一级）
cd "$SCRIPT_DIR/.."

PROJECT_NAME="垃圾邮件分类器项目"

clear #清空屏幕，让输出更干净
echo "========================================"
echo "=== 欢迎来到 ${PROJECT_NAME} ==="
echo "========================================"
echo ""
echo "当前工作目录：$(pwd)"
echo "项目结构如下："
# 使用find命令以树状递归显示当前目录结构，并忽略.git目录
find . -maxdepth 2 -not -path "./.git*" | sed 's|^\./||'

echo ""
echo "项目说明文档内容："
cat docs/README.md

echo ""
echo "脚本执行完毕。"
