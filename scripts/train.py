#文件路径：scripts/train.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib   #用于保存和加载模型
import os
import sys

print("--- Python 训练脚本开始执行 ---")

#1.从命令行接受版本号
if len(sys.argv) < 2:
    print("错误：缺少版本号参数。")
    print("用法：python train.py <version>")
    sys.exit(1)  #以非0状态退出，表示错误

MODEL_VERSION = sys.argv[1]
print(f"接收到模型版本号：{MODEL_VERSION}")

#2.定义清晰的路径变量
DATA_PATH = 'data/spam.csv'
MODEL_DIR = 'models'
RESULTS_DIR = 'results'

#确保输出目录存在
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

#根据版本号生成动态的文件名
MODEL_PATH = os.path.join(MODEL_DIR,f'spam_classifier_{MODEL_VERSION}.joblib')
VECTORIZER_PATH = os.path.join(MODEL_DIR,f'vectorizer_{MODEL_VERSION}.joblib')
RESULT_PATH = os.path.join(RESULTS_DIR,f'accuracy_{MODEL_VERSION}.txt')

#执行机器学习流程
try:
    print(f"步骤 1/5：加载数据从 {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)

    print("步骤 2/5：划分训练集和测试集...")
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

    print("步骤 3/5: 文本特征化...")
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("步骤 4/5: 训练朴素贝叶斯模型...")
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)

    print("步骤 5/5: 评估模型并保存结果...")
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
    sys.exit(1) # 发生任何异常都以错误状态退出

print("--- Python 训练脚本执行完毕 ---")
sys.exit(0)  #明确以成功状态退出
