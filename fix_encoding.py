#!/usr/bin/env python3
import pandas as pd
import sys

filepath = sys.argv[1] if len(sys.argv) > 1 else "data/spam.csv"

encodings = ['latin1', 'ISO-8859-1', 'cp1252', 'utf-8', 'windows-1252']

for enc in encodings:
    try:
        print(f"尝试 {enc}...")
        df = pd.read_csv(filepath, encoding=enc, on_bad_lines='skip')
        print(f"  成功! 共 {len(df)} 行，{len(df.columns)} 列")
        print(f"  列名: {list(df.columns)}")
        
        # 保存为 UTF-8
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"  已转换为 UTF-8")
        
        # 验证
        test = pd.read_csv(filepath, encoding='utf-8')
        print(f"  验证通过: {len(test)} 行")
        break
    except Exception as e:
        print(f"  失败: {str(e)[:60]}")
        continue
