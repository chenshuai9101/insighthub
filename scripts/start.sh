#!/bin/bash
# InsightHub 启动脚本
cd "$(dirname "$0")/.."
python3 -m pip install -r requirements.txt -q 2>/dev/null
python3 main.py
