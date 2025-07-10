#!/usr/bin/env bash
set -euo pipefail

# Conda 激活
eval "$(conda shell.bash hook)"
conda activate aivideo

# Redis (Homebrew) 自启
if ! pgrep -x "redis-server" >/dev/null; then
  brew services start redis
  echo "[+] Redis 已启动"
fi

# 导入环境变量
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs -0)
fi

# Backend
echo "[+] 启动 FastAPI..."
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
