# 文件路径: scripts/io_format_test.py
import pandas as pd
import numpy as np
import time
import os

# 1. 创建一个有代表性的大型 DataFrame
print("正在创建一个大型 DataFrame (100万行 x 10列)...")
num_rows = 1000000
data = {
    'float_col': np.random.rand(num_rows),
    'int_col': np.random.randint(0, 1000, size=num_rows),
    'string_col': [f'id_{i}' for i in range(num_rows)],
    'bool_col': np.random.choice([True, False], size=num_rows)
}
df = pd.DataFrame(data)
print("创建完毕。")

# 2. 定义测试函数
def test_format(format_name, write_func, read_func, file_path):
    print(f"\n--- 测试格式: {format_name} ---")
    
    # 测试写性能
    start_time = time.time()
    write_func(df, file_path)
    write_time = time.time() - start_time
    file_size = os.path.getsize(file_path) / 1024 / 1024 # MB
    
    print(f"写入耗时: {write_time:.4f} 秒")
    print(f"文件大小: {file_size:.2f} MB")
    
    # 测试读性能
    start_time = time.time()
    _ = read_func(file_path)
    read_time = time.time() - start_time
    
    print(f"读取耗时: {read_time:.4f} 秒")
    os.remove(file_path) # 清理文件
    return write_time, read_time, file_size

# 3. 执行测试
results = {}

# 测试 CSV
results['CSV'] = test_format(
    'CSV', 
    lambda d, p: d.to_csv(p, index=False), 
    lambda p: pd.read_csv(p),
    'test_data.csv'
)

# 测试 Parquet (使用 pyarrow 引擎)
results['Parquet'] = test_format(
    'Parquet', 
    lambda d, p: d.to_parquet(p, engine='pyarrow', index=False), 
    lambda p: pd.read_parquet(p, engine='pyarrow'),
    'test_data.parquet'
)

# 测试 Feather
results['Feather'] = test_format(
    'Feather', 
    lambda d, p: d.to_feather(p), 
    lambda p: pd.read_feather(p),
    'test_data.feather'
)

# 4. 打印总结报告
print("\n--- 性能总结报告 ---")
# 设定 CSV 为基准
base_write_time = results['CSV'][0]
base_read_time = results['CSV'][1]

print(f"{'格式':<10} | {'写入耗时(s)':<15} | {'读取耗时(s)':<15} | {'文件大小(MB)':<15} | {'读性能提升':<15}")
print("-" * 75)
for name, (w, r, s) in results.items():
    read_speedup = f"{(base_read_time / r):.1f}x" if name != 'CSV' else "1.0x (基准)"
    print(f"{name:<10} | {w:<15.4f} | {r:<15.4f} | {s:<15.2f} | {read_speedup:<15}")
