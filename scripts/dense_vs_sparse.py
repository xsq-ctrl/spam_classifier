import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer

# 1. 从 spam.csv 加载 v2 列作为文本数据
print("加载 spam.csv 数据...")
df = pd.read_csv('data/spam.csv', encoding='latin-1')  # 使用正确的编码
texts = df['v2'].tolist()
print(f"共加载 {len(texts)} 条短信数据")
print(f"示例: {texts[0][:50]}...")

# 2. 创建 CountVectorizer（这就是你之前缺少的部分！）
vectorizer = CountVectorizer()

print("\n" + "="*50)
print("开始进行文本向量化...")
print("="*50)

# 默认情况下，fit_transform 返回一个稀疏矩阵 (CSR格式)
sparse_matrix = vectorizer.fit_transform(texts)

print("\n--- 稀疏矩阵 (Scipy CSR Matrix) ---")
print(f"类型: {type(sparse_matrix)}")
print(f"形状 (shape): {sparse_matrix.shape}")

# 精确计算稀疏矩阵内存：数据 + 索引 + 指针
sparse_mem_bytes = (sparse_matrix.data.nbytes + 
                    sparse_matrix.indices.nbytes + 
                    sparse_matrix.indptr.nbytes)
print(f"内存占用: 约 {sparse_mem_bytes / 1024 / 1024:.2f} MB")
print("(由 data, indices, indptr 三部分组成)")

print("\n--- 转换为密集矩阵 (Numpy Array) ---")
try:
    dense_matrix = sparse_matrix.toarray()
    dense_mem_bytes = dense_matrix.nbytes
    
    print(f"类型: {type(dense_matrix)}")
    print(f"形状 (shape): {dense_matrix.shape}")
    print(f"内存占用: 约 {dense_mem_bytes / 1024 / 1024:.2f} MB")
    
    # 计算内存占用差异
    if sparse_mem_bytes > 0:
        ratio = dense_mem_bytes / sparse_mem_bytes
        print(f"\n结论：密集矩阵的内存占用是稀疏矩阵的 {ratio:.1f} 倍！")
        
except MemoryError:
    print("\n错误：尝试转换为密集矩阵时发生 MemoryError！")
    print("这证明了在处理高维稀疏数据时，使用密集矩阵是多么危险。")
