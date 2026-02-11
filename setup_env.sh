#!/bin/bash
set -e # 任何命令失败则立即退出

ENV_NAME="spam_env"
ENV_FILE="environment.yml"

echo "--- 正在设置项目环境: ${ENV_NAME} ---"

if ! command -v conda &> /dev/null
then
    echo "错误: 未找到 conda 命令。请先安装 Anaconda 或 Miniconda。"
    exit 1
fi

echo "正在根据 ${ENV_FILE} 创建或更新 conda 环境..."
# 使用 a -f (file) b --prune (删除环境中多余的包) 的方式确保环境一致
conda env create -f ${ENV_FILE} || conda env update -f ${ENV_FILE} --prune

echo ""
echo "--- 环境设置完毕 ---"
echo "请运行 'conda activate ${ENV_NAME}' 来激活环境。"
