# 文件路径: scripts/memory_eater.py
import time
import os
import psutil # 一个强大的跨平台系统信息库

# 获取当前进程对象
process = psutil.Process(os.getpid())

print("--- 内存怪兽即将出笼 ---")
print(f"我的进程ID是: {os.getpid()}")
print("我将创建一个列表，并以每秒约100MB的速度填充它。")
print("请在另一个终端使用 'free -h', 'vmstat 1' 或 'htop' 观察内存变化。")
time.sleep(5)

huge_list = []
# 每次分配一个 1MB 的字符串
chunk_size = 1024 * 1024 

try:
    i = 0
    while True:
        # 每次循环消耗约 100MB
        for _ in range(100):
            huge_list.append(' ' * chunk_size)
        
        i += 1
        # 使用 psutil 获取进程实际占用的物理内存 (RSS: Resident Set Size)
        rss_memory_mb = process.memory_info().rss / (1024 * 1024)
        print(f"第 {i} 轮，已消耗内存约: {i * 100} MB | "
              f"进程实际占用 (RSS): {rss_memory_mb:.2f} MB")
        
        time.sleep(1)
except MemoryError:
    # 这个异常可能在 OOM Killer 动手之前被 Python 解释器自己捕获
    print("\nPython 捕获到 MemoryError！内存已无法分配。")
    print("这通常发生在 OOM Killer 采取行动之前，因为Python的内存管理器预见到了问题。")
except Exception as e:
    print(f"\n发生未知错误: {e}")
finally:
    print("内存怪兽执行结束。")
