# RCS-Demo 系统演示

本仓库是「RCS 5.0」的重构演示版本。

> 当前版本（v0.1）已完成「后线工作台 - 交易复核」首屏 1:1 还原，覆盖原图全部字段、布局、Tab 与分页。
> 后续模块将按 PRD 增量交付：**税务规则配置**（新建）、**会计分录规则配置**（重构）等。

## 技术栈

| 层 | 选型 |
|---|---|
| 前端 | Vue 3 + Vite 5 + Element Plus 2.7 + Pinia + Vue Router 4（hash 模式）|
| 后端 | Python 3.10+ / FastAPI / Uvicorn / Pydantic v2 |
| Mock | 后端内置确定性随机数据（共 68 条），其中前 20 条与产品截图一一对应 |

## 目录结构

```
RCS-Demo/
├── frontend/
│   ├── package.json
│   ├── vite.config.js                # /api → http://127.0.0.1:8000
│   ├── index.html
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── router/index.js           # 顶部 + 工作台子菜单全部注册（部分占位）
│       ├── api/
│       │   ├── request.js
│       │   └── workbench.js
│       ├── layouts/
│       │   └── MainLayout.vue        # 顶部导航 + 左侧 rail + 工作台子菜单 + Tab + 页脚
│       ├── components/
│       │   ├── TopNav.vue            # RCS 5.0 顶部主导航（10 项 + admin）
│       │   └── WorkbenchSidebar.vue  # 工作台 7 大分组菜单
│       ├── views/
│       │   ├── Placeholder.vue
│       │   └── workbench/
│       │       └── TransactionReview.vue   # 交易复核（核心页）
│       └── styles/global.scss
└── backend/
    ├── requirements.txt
    └── app/
        ├── __init__.py
        ├── main.py                   # FastAPI 路由
        └── mock_data.py              # 截图 20 条 + 48 条合成 = 68 条
```

## 一键启动

### 1. 启动后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

健康检查：<http://127.0.0.1:8000/api/health> 应返回 `{"status":"ok","rows":68}`。

### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

打开 <http://localhost:5173>，默认进入「后线工作台 - 交易复核」。

## 已实现字段（与原图完全一致）

**顶部导航**：首页 / 交易录入 / 头寸管理 / 限额管理 / 业务管理 / 查询管理 / **后线工作台**（active） / 基础数据 / 查询统计 / 规则管理 / admin。

**工作台菜单（7 组 / 21 项）**：
- 流程审批 — 交易复核（active）/ 清算审批 / 调账审核
- 证实确认 — 证实匹配 / 证实明细 / 证实报文
- 清算结算 — 待轧差处理 / 待发报处理 / 来账分拣 / 支付假日调整 / 收付撤销 / 收付报文 / 结算路径
- 会计核算 — 计量跟踪处理 / 送账异常处理 / 余额初始 / 手工指定 / 阀值放行
- 每日核对 — 托管机构余额核对
- 交易录入 — 单边现金流
- 业务管理 — 定盘管理

**交易复核页**：
- Tabs：审批 / 补发 / 交易事件
- 搜索：外部流水号、交易流水号
- 操作：批量审批
- 表格列：☐ / 外部流水号 / 交易流水号 / 产品 / 动作 / 起息日 / 交易日 / 交易对手 / 标的 / 折美金额 / 买卖方向 / 审核 / 操作
- 买卖方向多色显示：买入/借入/收 → 绿；卖出/借出/付 → 红
- 分页：共 68 条 · 20 条/页 · 1 / 2 / 3 / 4 · 跳页

## API 一览

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/health` | 健康检查 |
| GET | `/api/workbench/menu` | 工作台菜单（含徽标） |
| GET | `/api/workbench/transaction-review?tab=&externalNo=&tradeNo=&page=&pageSize=` | 交易复核列表 |
| POST | `/api/workbench/transaction-review/{tradeNo}/approve` | 单笔审批 |
| POST | `/api/workbench/transaction-review/batch-approve` | 批量审批（body: `{ids: []}`）|

## 后续路线图

- [ ] 税务规则配置（**新建**）— 等待 PRD
- [ ] 会计分录规则配置（**重构**）— 等待 PRD
- [ ] 顶部其他主导航模块迁移
