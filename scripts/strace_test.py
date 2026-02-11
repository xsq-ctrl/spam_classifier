# 文件路径: scripts/strace_test.py
print("脚本开始执行...")
try:
    with open("test_output.txt", "w") as f:
        f.write("Hello, strace!")
    print("文件写入成功。")
except Exception as e:
    print(f"发生错误: {e}")
print("脚本执行结束。")
