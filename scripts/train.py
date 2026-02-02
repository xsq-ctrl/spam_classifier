#文件路径：scripts/train.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib
import os
import sys
import signal
import time

# --- 新增部分: 信号处理 (基于全局变量) ---
interrupted = False

def graceful_exit(signum, frame):
    """信号处理函数，设置中断标志并优雅退出。"""
    global interrupted
    if not interrupted:
        interrupted = True
        print(f"\n\n捕获到信号 {signal.Signals(signum).name}！正在尝试进行优雅退出...")
        
        # ======== 新增代码：创建检查点文件 ========
        try:
            # 确保models目录存在
            os.makedirs("models", exist_ok=True)
            
            # 创建检查点文件
            checkpoint_path = os.path.join("models", "checkpoint.tmp")
            with open(checkpoint_path, "w") as f:
                f.write(f"训练被信号 {signal.Signals(signum).name} 中断\n")
                f.write(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"信号值: {signum}\n")
                f.write(f"模型版本: {MODEL_VERSION if 'MODEL_VERSION' in globals() else 'N/A'}\n")
            
            print(f"✓ 检查点文件已创建: {checkpoint_path}")
        except Exception as e:
            print(f"✗ 创建检查点失败: {e}")
        # ======== 结束新增代码 ========
        
        # 实际场景中，这里可以添加保存模型 checkpoint 的代码
        # 为了演示，我们只打印信息然后干净地退出
        print("训练已中断，不会保存最终模型。现在退出。")
        sys.exit(130) # 使用 130 退出码表示脚本被中断

# 注册信号处理器，将 SIGINT 和 SIGTERM 信号都与我们的函数绑定
signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTERM, graceful_exit)
# --- 结束新增部分 ---

print("--- Python 训练脚本开始执行 ---")
print("(提示: 你可以在训练步骤中按 Ctrl+C 来测试中断功能)")

# 1. 从命令行接收版本号
if len(sys.argv) < 2:
    print("错误: 缺少版本号参数。")
    print("用法: python train.py <version>")
    sys.exit(1)

MODEL_VERSION = sys.argv[1]
print(f"接收到模型版本号: {MODEL_VERSION}")

# 2. 定义清晰的路径变量
DATA_PATH = 'data/spam.csv'
MODEL_DIR = 'models'
RESULTS_DIR = 'results'
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, f'spam_classifier_{MODEL_VERSION}.joblib')
VECTORIZER_PATH = os.path.join(MODEL_DIR, f'vectorizer_{MODEL_VERSION}.joblib')
RESULT_PATH = os.path.join(RESULTS_DIR, f'accuracy_{MODEL_VERSION}.txt')

# 3. 执行机器学习流程
try:
    print(f"\n步骤 1/5: 加载数据从 {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
    print("步骤 2/5: 划分训练集和测试集...")
    X_train, X_test, y_train, y_test = train_test_split(df['v2'], df['v1'], test_size=0.2, random_state=42)
    
    print("步骤 3/5: 文本特征化...")
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # --- 修改部分: 模拟可中断的训练过程 ---
    print("\n步骤 4/5: 训练朴素贝叶斯模型... (将模拟一个15秒的训练过程)")
    # 注意: 实际的 model.fit() 本身不易中断。
    # 这种循环检查的方式更适用于可以分批次(batch)训练的深度学习模型。
    # 这里我们用它来模拟这个概念。
    for i in range(15):
        # 这个检查点至关重要。它确保在下一次循环之前检查是否收到了退出信号。
        # 由于 graceful_exit 已经处理了 sys.exit，这里的 break 实际上不会被执行，
        # 但在不直接退出的实现中，这个 break 是必要的。
        if interrupted:
            break
        print(f"  训练中... {i+1}/15 秒")
        time.sleep(1) 
    # --- 结束修改部分 ---
    
    # 训练模型 (只有在未中断的情况下执行)
    print("  模拟训练结束，现在执行实际的 fit 操作...")
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)
    
    print("\n步骤 5/5: 评估模型并保存结果...")
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"模型在测试集上的准确率: {accuracy:.4f}")
    
    # 保存所有产出物
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    with open(RESULT_PATH, 'w') as f:
        f.write(f'Accuracy: {accuracy:.4f}\n')
    
    print(f"\n训练成功！产出物如下:")
    print(f"  - 模型: {MODEL_PATH}")
    print(f"  - 特征转换器: {VECTORIZER_PATH}")
    print(f"  - 评估报告: {RESULT_PATH}")
    
except Exception as e:
    print(f"\n!!!!!! 训练过程中发生错误: {e} !!!!!!")
    sys.exit(1)

print("\n--- Python 训练脚本执行完毕 ---")
sys.exit(0)
