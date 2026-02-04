# 文件路径: scripts/process_data.py
import pandas as pd
import time
import sys
import os
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

# 确保路径的健壮性
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'spam.csv')

# 这是一个模拟耗时计算的函数 (CPU-bound)
def slow_process_text(text):
    """模拟一个比较耗费CPU的文本处理任务"""
    # 故意增加计算量，模拟复杂的正则或分析
    vowel_count = sum(1 for char in text.lower() if char in 'aeiou')
    # 再增加一点无意义的计算来消耗CPU时间
    _ = [i*i for i in range(500)]
    return vowel_count

def run_single_process(texts):
    """单进程处理所有文本"""
    print("模式: 单进程。开始处理...")
    start_time = time.time()
    results = [slow_process_text(text) for text in texts]
    end_time = time.time()
    print(f"单进程处理完成。耗时: {end_time - start_time:.2f} 秒。")
    return results

def run_multi_thread(texts, num_workers):
    """多线程处理 - 用于对比，预期效果不佳"""
    print(f"模式: 多线程 (使用 {num_workers} 个工作线程)。开始处理...")
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(slow_process_text, texts))
    end_time = time.time()
    print(f"多线程处理完成。耗时: {end_time - start_time:.2f} 秒。")
    return results

def run_multi_process(texts, num_workers):
    """多进程并行处理所有文本"""
    print(f"模式: 多进程 (使用 {num_workers} 个工作进程)。开始处理...")
    start_time = time.time()
    with multiprocessing.Pool(processes=num_workers) as pool:
        results = pool.map(slow_process_text, texts)
    end_time = time.time()
    print(f"多进程处理完成。耗时: {end_time - start_time:.2f} 秒。")
    return results

if __name__ == '__main__':
    print("开始加载数据...")
    try:
        df = pd.read_csv(DATA_PATH)
        texts_to_process = list(df['v2']) * 10 # 增加数据量以放大效果
        print(f"数据加载完毕，共 {len(texts_to_process)} 条文本需要处理。")
    except FileNotFoundError:
        print(f"错误: 数据文件 {DATA_PATH} 未找到。请先运行第二周的实验下载数据。")
        sys.exit(1)

    if len(sys.argv) < 2 or sys.argv[1] not in ['single', 'thread', 'multi']:
        print("用法: python process_data.py [single | thread | multi]")
        sys.exit(1)
    
    mode = sys.argv[1]
    cpu_cores = multiprocessing.cpu_count()
    print(f"检测到系统有 {cpu_cores} 个CPU核心。")

    if mode == 'single':
        run_single_process(texts_to_process)
    elif mode == 'thread':
        run_multi_thread(texts_to_process, num_workers=cpu_cores)
    elif mode == 'multi':
        run_multi_process(texts_to_process, num_workers=cpu_cores)
    print(f"\n主要任务完成，开始30秒CPU活动以便监控 (PID: {os.getpid()})")
    start = time.time()
    while time.time() - start < 30:
        #简单的CPU计算
        sum(i*i for i in range(10000))
    print("程序结束")
