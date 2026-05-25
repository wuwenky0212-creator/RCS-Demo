#!/usr/bin/env bash
# RCS-Demo 一键启动脚本（macOS / Linux）
# 首次运行自动安装依赖，后续直接启动
# 用法：bash start-dev.sh
# 退出：Ctrl-C

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║        RCS-Demo  Launcher            ║"
echo "╚══════════════════════════════════════╝"
echo ""

# ── 检查基础依赖 ─────────────────────────
if ! command -v python3 &>/dev/null; then
  echo "❌ 未找到 python3，请先安装 Python 3.9+"
  exit 1
fi
if ! command -v node &>/dev/null; then
  echo "❌ 未找到 node，请先安装 Node.js 18+"
  exit 1
fi
if ! command -v npm &>/dev/null; then
  echo "❌ 未找到 npm，请先安装 npm"
  exit 1
fi

# ── 后端初始化 ───────────────────────────
echo "▶ 初始化后端..."
cd "$ROOT/backend"

if [ ! -d ".venv" ]; then
  echo "  → 创建 Python 虚拟环境..."
  python3 -m venv .venv
fi

if [ ! -f ".venv/lib/python*/site-packages/fastapi" ] && \
   [ ! -d ".venv/lib/python3."*"/site-packages/fastapi" ] 2>/dev/null; then
  echo "  → 安装 Python 依赖（首次约需 30 秒）..."
  ./.venv/bin/pip install -r requirements.txt -q
fi

echo "  → 启动后端服务 http://localhost:8000"
./.venv/bin/uvicorn app.main:app --reload --port 8000 &
BACK_PID=$!

# ── 前端初始化 ───────────────────────────
echo ""
echo "▶ 初始化前端..."
cd "$ROOT/frontend"

if [ ! -d "node_modules" ]; then
  echo "  → 安装 npm 依赖（首次约需 1 分钟）..."
  npm install --silent
fi

echo "  → 启动前端服务 http://localhost:5173"
npm run dev &
FRONT_PID=$!

# ── 完成提示 ────────────────────────────
echo ""
echo "✅ 启动完成！"
echo "   前端：http://localhost:5173"
echo "   后端：http://localhost:8000"
echo "   按 Ctrl-C 停止所有服务"
echo ""

trap "echo ''; echo '正在停止服务...'; kill $BACK_PID $FRONT_PID 2>/dev/null || true; echo '已停止。'" INT TERM

wait
