#!/bin/bash
echo "等待3秒后开始训练..."
sleep 10
./run_training.sh | while read line; do
    echo "$line"
    sleep 10  # 每行输出延迟1秒
done
