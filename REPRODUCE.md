# 项目复现指南

本文档提供了从零开始完整复现 `spam-classifier` 项目所有实验结果的详细步骤。

## 1. 先决条件

- 一个类 Linux 操作系统 (如 Ubuntu, CentOS)。
- 已安装 `git`。
- 已安装 [Anaconda](https://www.anaconda.com/products/distribution) 或 [Miniconda](https://docs.conda.io/en/latest/miniconda.html)。

## 2. 复现步骤

### 步骤 1: 克隆项目仓库

首先，克隆本项目的代码仓库到你的本地机器，并进入项目目录。
git clone <你的项目仓库URL>  
cd spam-classifier

### 步骤 2: 创建并激活虚拟环境
本项目使用 Conda 管理依赖环境。我们提供了一个自动化脚本来创建和配置所需的环境。

运行以下脚本：
./setup_env.sh
脚本执行成功后，激活新创建的环境：
conda activate spam_env
(你的命令行提示符前应该会出现 (spam_env) 字样)

### 步骤 3: 下载并准备数据
在激活虚拟环境后，运行数据下载脚本来获取原始数据集。
python scripts/download_data.py

### 步骤 4: 运行核心训练流程
现在，你可以运行核心的训练脚本来生成模型和评估结果。由于我们固定了随机种子，每次运行的结果都应该是相同的。

我们使用一个固定的版本号 reproducible_test 来方便对比。
./run_training.sh reproducible_test

### 步骤 5: 验证结果
最后，检查 results/ 目录下的评估报告。其内容（如 accuracy, precision, recall）应与基准结果保持一致。
cat results/evaluation_reproducible_test.json
至此，整个项目的核心流程已成功复现。
