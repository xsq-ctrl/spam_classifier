import fileinput
import sys
# 修改graceful_exit函数，添加文件创建代码
new_code = '''def graceful_exit(signum, frame):
    """信号处理函数，设置中断标志并优雅退出。"""
    global interrupted
    if not interrupted:
        interrupted = True
        print(f"\\n\\n捕获到信号 {signal.Signals(signum).name}! 正在尝试进行优雅退出。")
        
        # 创建检查点文件
        try:
            import os
            os.makedirs("models", exist_ok=True)
            with open("models/checkpoint.tmp", "w") as f:
                f.write(f"训练被信号 {signal.Signals(signum).name} 中断\\n")
                f.write(f"时间: {__import__('datetime').datetime.now()}\\n")
                f.write(f"信号值: {signum}\\n")
            print("✓ 检查点文件已创建: models/checkpoint.tmp")
        except Exception as e:
            print(f"✗ 创建检查点失败: {e}")
        
        # 实际场景中，这里可以添加保存模型 checkpoint 的代码
        # 为了演示，我们只打印信息后干净地退出
        print("训练已中断，不会保存最终模型。现在退出。")
        sys.exit(130) # 使用 130 退出码表示脚本被中断'''

# 读取原文件并修改
with open('scripts/train.py', 'r') as f:
    content = f.read()

# 替换graceful_exit函数
import re
pattern = r'def graceful_exit\(signum, frame\):.*?sys\.exit\(130\)'
updated_content = re.sub(pattern, new_code, content, flags=re.DOTALL)

# 写入修改后的文件
with open('scripts/train.py', 'w') as f:
    f.write(updated_content)

print("脚本已更新，添加了检查点文件创建功能")
