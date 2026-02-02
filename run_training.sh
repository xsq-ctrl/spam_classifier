#!/bin/bash

# --- Shell 脚本的最佳实践 (Boilerplate) ---
# 1. 在任何命令失败时立即退出
set -e
# 2. 在引用未定义变量时报错
set -u
# 3. 管道中任何一个命令失败，都视为失败 (对 | tee 很重要)
set -o pipefail

# --- 1. 配置与准备阶段 ---
# 将 MODEL_VERSION 导出为环境变量，这样子进程(如 python 脚本)就可以读取到它
export MODEL_VERSION=$(date +%Y%m%d_%H%M%S)
DATA_FILE="data/spam.csv"
DATA_URL="https://storage.googleapis.com/just-learning-assets/spam.csv"
LOG_DIR="logs"

# 检查并创建日志目录
mkdir -p ${LOG_DIR}
LOG_FILE="${LOG_DIR}/training_${MODEL_VERSION}.log"

# --- 2. 执行阶段 (封装在函数中，更清晰) ---
main() {
    echo "================================================="
    echo "=== 开始垃圾邮件分类器训练流水线 ==="
    echo "=== 模型版本: ${MODEL_VERSION}                 ==="
    echo "================================================="
    echo "所有日志将记录在: ${LOG_FILE}"
    echo ""

    echo "--> 步骤 1/3: 检查并下载数据集..."
    if [ ! -f "${DATA_FILE}" ]; then
        echo "数据集不存在于 ${DATA_FILE}"
        echo "下载链接: https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset"
        echo "下载文件: 在该页面点击 "Download" 按钮，会得到一个名为 archive.zip 的文件，里面包含了 spam.csv。"
    else
        echo "数据集已存在，跳过下载。"
    fi
    echo ""

    # (可选) 如果你使用了Python虚拟环境 (如 venv 或 conda)，在这里激活
    # echo "激活 Python 虚拟环境..."
    # source /path/to/your/venv/bin/activate

    echo "--> 步骤 2/3: 运行 Python 训练脚本..."
    # 核心命令！python 脚本将从环境变量 $MODEL_VERSION 中读取版本号
    python3 scripts/train.py "$MODEL_VERSION"
    
    echo ""
    echo "--> 步骤 3/3: 检查最终产出物..."
    echo "检查模型文件..."
    ls -l "models/spam_classifier_${MODEL_VERSION}.joblib"
    echo "检查评估报告..."
    ls -l "results/accuracy_${MODEL_VERSION}.txt"
    echo ""
}

# --- 3. 启动与日志记录 ---
# 将 main 函数的所有输出 (stdout 标准输出 和 stderr 标准错误) 都通过管道传给 tee
main 2>&1 | tee "${LOG_FILE}"


# --- 4. 最终总结 ---
# 由于 `set -e -u -o pipefail` 的存在，脚本能运行到这里就意味着所有步骤都成功了
echo "*************************************************"
echo "**  流水线执行成功！"
echo "**  模型版本: ${MODEL_VERSION}"
echo "**  请查看以下产出物:"
echo "**    - 日志: ${LOG_FILE}"
echo "**    - 模型: models/spam_classifier_${MODEL_VERSION}.joblib"
echo "**    - 结果: results/accuracy_${MODEL_VERSION}.txt"
echo "*************************************************"
echo ""
