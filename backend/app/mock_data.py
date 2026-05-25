"""RCS-Demo 后端 Mock 数据集

为「后线工作台 - 交易复核」演示提供高仿真数据。
- 前 20 条与产品截图一一对应（包含外部流水号、产品、金额、买卖方向等）
- 余下补充至 68 条，覆盖外汇即期/远期/掉期/期权、利率衍生品、债券、同业拆借、货币市场、单边现金流等业务类型
"""

from __future__ import annotations
import random
from datetime import date, timedelta
from typing import List, Dict, Any


# ---------------------------------------------------------------------------
# 数据字典 — 与原系统一致
# ---------------------------------------------------------------------------
PRODUCTS = [
    "Interbank Lending",
    "Asset Mgmt Cashflow",
    "Single Cashflow",
    "FX Swap",
    "FX European Option",
    "FX Spot",
    "FX Forward",
    "Money Market Deposit",
    "Interest Rate Cap/Floor",
    "Bond Trading",
    "Interest Rate Swaption",
    "Bond Lending",
    "Repo",
    "Interest Rate Swap",
]

ACTIONS = ["New", "Modify", "Delete", "Cancel"]

INSTRUMENTS_FX = ["USDCNY", "USDCNH", "EURUSD", "USDJPY", "GBPUSD", "USDHKD", "AUDUSD"]
INSTRUMENTS_RATE = ["CNY", "USD", "EUR", "BND"]
INSTRUMENTS_BOND = ["cbo_test_bond1", "10230402Z.IB", "190210.IB", "220215.IB", "230020.IB"]

DIRECTIONS_FX = ["Buy", "Sell"]
DIRECTIONS_CF = ["Receive", "Pay"]
DIRECTIONS_LEND = ["Borrow", "Lend"]

COUNTERPARTIES = ["10275", "10312", "10408", "10519", "11203", "11567", "12099", "12846", "13501"]
REVIEWERS = ["Supervisor", "Reviewer A", "Reviewer B", "Risk Ctrl A"]


# ---------------------------------------------------------------------------
# 截图前 20 条精确还原
# ---------------------------------------------------------------------------
_SCREENSHOT_ROWS: List[Dict[str, Any]] = [
    # external_no, product, action, value_date, trade_date, counterparty, instrument, usd_amount, direction
    ("25112700002758", "Interbank Lending",       "New",    "2025-11-06", "2025-11-04", "10275", "CNY",            142023.26,    "Lend"),
    ("25112900002764", "Asset Mgmt Cashflow",     "New",    "2025-11-29", "2025-11-29", "10275", "BND",            15.76,        "Buy"),
    ("25112300002539", "Single Cashflow",         "New",    "2025-11-23", "2025-11-23", "10275", "CNY",            1420.23,      "Pay"),
    ("25112300002252", "FX Swap",                 "New",    "2025-11-05", "2025-11-03", "10275", "USDCNH",         10000.00,     "Sell"),
    ("25112300002049", "FX European Option",      "New",    "2025-11-25", "2025-11-23", "10275", "USDCNY",         100000.00,    "Buy"),
    ("25112300001926", "FX Spot",                 "New",    "2025-11-26", "2025-11-24", "10275", "USDCNY",         12.00,        "Buy"),
    ("25112300001459", "FX Forward",              "New",    "2025-11-25", "2025-11-23", "10275", "USDCNY",         50000.00,     "Buy"),
    ("25112300001341", "Money Market Deposit",    "Modify", "2025-11-28", "2025-11-26", "10275", "CNY",            284046.53,    "Lend"),
    ("25112300001327", "Single Cashflow",         "New",    "2025-11-23", "2025-11-23", "10275", "CNY",            601585.26,    "Pay"),
    ("25112300001016", "Interest Rate Cap/Floor", "New",    "2025-11-24", "2025-11-20", "10275", "CNY",            14202.33,     "Sell"),
    ("25112300001049", "FX Spot",                 "New",    "2025-11-26", "2025-11-24", "10275", "USDCNY",         10000.00,     "Buy"),
    ("25112300000473", "Bond Trading",            "Modify", "2025-11-22", "2025-11-22", "10275", "cbo_test_bond1", 28404.65,     "Buy"),
    ("25112300000281", "FX Spot",                 "New",    "2025-11-26", "2025-11-24", "10275", "EURUSD",         13.97,        "Buy"),
    ("25112100331402", "FX Spot",                 "New",    "2025-11-26", "2025-11-24", "10275", "EURUSD",         13.97,        "Buy"),
    ("25112000341261", "Interbank Lending",       "New",    "2025-11-24", "2025-11-20", "10275", "CNY",            426039536.47, "Lend"),
    ("25112000341168", "FX Spot",                 "New",    "2025-11-20", "2025-11-20", "10275", "USDCNY",         100000.00,    "Buy"),
    ("25112000341164", "Interest Rate Swaption",  "New",    "2025-12-30", "2025-11-20", "10275", "USD",            50000000.00,  "Buy"),
    ("25112000341048", "FX Spot",                 "New",    "2025-11-26", "2025-11-24", "10275", "USDCNY",         12.00,        "Buy"),
    ("25112000341075", "FX Spot",                 "New",    "2025-11-26", "2025-11-24", "10275", "USDCNY",         12.00,        "Buy"),
    ("25112000340691", "Bond Trading",            "New",    "2025-11-20", "2025-11-20", "",      "10230402Z.IB",   142013.18,    "Sell"),
]


# ---------------------------------------------------------------------------
# 余下 48 条 由可控随机数据生成（每次启动结果一致）
# ---------------------------------------------------------------------------
def _gen_extra_rows(start_no: int, count: int) -> List[Dict[str, Any]]:
    rng = random.Random(20260508)  # 固定种子，保证 demo 的稳定性
    rows: List[Dict[str, Any]] = []
    base_date = date(2025, 11, 20)

    for i in range(count):
        product = rng.choice(PRODUCTS)
        action = rng.choices(ACTIONS, weights=[7, 2, 0.5, 0.5])[0]

        if product.startswith("FX"):
            instrument = rng.choice(INSTRUMENTS_FX)
            direction = rng.choice(DIRECTIONS_FX)
            usd = rng.choice([12.0, 13.97, 100.0, 1000.0, 10000.0, 50000.0, 100000.0, 500000.0])
        elif product in ("Interbank Lending", "Money Market Deposit"):
            instrument = "CNY"
            direction = rng.choice(DIRECTIONS_LEND)
            usd = round(rng.uniform(50_000, 800_000_000), 2)
        elif "Cashflow" in product:
            instrument = rng.choice(INSTRUMENTS_RATE)
            direction = rng.choice(DIRECTIONS_CF)
            usd = round(rng.uniform(20.0, 1_500_000.0), 2)
        elif "Interest Rate" in product:
            instrument = rng.choice(["CNY", "USD"])
            direction = rng.choice(DIRECTIONS_FX)
            usd = round(rng.uniform(10_000.0, 60_000_000.0), 2)
        elif "Bond" in product or product == "Repo":
            instrument = rng.choice(INSTRUMENTS_BOND)
            direction = rng.choice(DIRECTIONS_FX)
            usd = round(rng.uniform(20_000.0, 5_000_000.0), 2)
        else:
            instrument = rng.choice(INSTRUMENTS_RATE + INSTRUMENTS_FX)
            direction = rng.choice(DIRECTIONS_FX)
            usd = round(rng.uniform(100.0, 1_000_000.0), 2)

        trade_d = base_date - timedelta(days=rng.randint(0, 18))
        value_d = trade_d + timedelta(days=rng.choice([0, 1, 2, 3, 7, 30, 90]))

        # 与原系统格式一致：14 位 = YYMMDD(6) + 8 位流水
        no = f"2511{rng.randint(10, 30):02d}{(start_no - i):08d}"

        rows.append(dict(
            external_no=no,
            trade_no=no,
            product=product,
            action=action,
            value_date=value_d.isoformat(),
            trade_date=trade_d.isoformat(),
            counterparty=rng.choice(COUNTERPARTIES),
            instrument=instrument,
            usd_amount=usd,
            direction=direction,
            reviewer=rng.choice(REVIEWERS),
        ))

    return rows


def _build_full_dataset() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for r in _SCREENSHOT_ROWS:
        rows.append(dict(
            external_no=r[0],
            trade_no=r[0],
            product=r[1],
            action=r[2],
            value_date=r[3],
            trade_date=r[4],
            counterparty=r[5],
            instrument=r[6],
            usd_amount=r[7],
            direction=r[8],
            reviewer="Supervisor",
        ))

    rows.extend(_gen_extra_rows(start_no=340500, count=48))
    return rows


# 模块级单例数据集（68 条）
TRANSACTION_REVIEWS: List[Dict[str, Any]] = _build_full_dataset()


# 不同 Tab 的数据子集（演示用）
def get_dataset(tab: str) -> List[Dict[str, Any]]:
    if tab == "approve":
        return TRANSACTION_REVIEWS
    if tab == "reissue":
        # 补发：取动作为修改的 + 部分新增
        return [r for r in TRANSACTION_REVIEWS if r["action"] in ("Modify", "Cancel")][:18]
    if tab == "event":
        # 交易事件：取最近的 12 条
        return TRANSACTION_REVIEWS[:12]
    return TRANSACTION_REVIEWS


# ---------------------------------------------------------------------------
# 税务规则配置 Mock 数据（印尼雅加达市场同业拆借与债券交易）
# ---------------------------------------------------------------------------
TAX_RULES: List[Dict[str, Any]] = [
    {
        "id": "TAX-IDR-009",
        "is_active": True,
        "effective_date": "2026-05-09",
        "country": "ID",
        "product_category": "interbank",
        "counterparty_types": ["foreign_fi"],
        "direction": "pay",
        "tax_type": "WHT",
        "tax_rate": 20.0000,
        "tax_base": "accrued_interest",
        "override_control": "doc_required",
        "created_by": "admin",
        "created_at": "2026-05-09",
        "settlement_impact": "standalone",
        "tax_timing_base": "coupon_date",
        "tax_timing_offset": 0,
    },
    {
        "id": "TAX-IDR-010",
        "is_active": True,
        "effective_date": "2026-05-09",
        "country": "ID",
        "product_category": "bond",
        "counterparty_types": ["foreign_fi"],
        "direction": "pay",
        "tax_type": "WHT",
        "tax_rate": 10.0000,
        "tax_base": "accrued_interest",
        "override_control": "doc_required",
        "created_by": "admin",
        "created_at": "2026-05-09",
        "settlement_impact": "net_deduct",
        "tax_timing_base": "value_date",
        "tax_timing_offset": 0,
    },
]


def _next_tax_rule_id() -> str:
    nums = []
    for r in TAX_RULES:
        try:
            nums.append(int(r["id"].split("-")[-1]))
        except ValueError:
            pass
    return f"TAX-IDR-{(max(nums) + 1):03d}" if nums else "TAX-IDR-001"


# ---------------------------------------------------------------------------
# 损益归因 - 情景查询 Mock 数据
# ---------------------------------------------------------------------------
PORTFOLIOS = ["Portfolio A", "Portfolio B", "Portfolio C", "Portfolio D"]

ATTRIBUTION_METHODS = ["PLVar", "Sensitivity"]

CALC_SCHEMES = ["Accumulate", "Recover"]

RULE_CONDITION_POOL = [
    "FX Forward", "FX Spot", "FX Swap", "FX European Option", "FX American Option",
    "Interest Rate Swap", "Interest Rate Cap/Floor", "Interest Rate Swaption",
    "Bond Trading", "Bond Lending", "Interbank Lending", "Money Market Deposit", "Repo",
]

SCENARIOS: List[Dict[str, Any]] = [
    {
        "id": "SCN-001", "name": "Scenario 1", "portfolio": "Portfolio A",
        "attribution_method": "PLVar", "calculation_scheme": "Accumulate", "currency": "USD",
        "rule_conditions": ["FX Spot", "FX Forward", "FX Swap"],
    },
]


def _next_scenario_id() -> str:
    nums = []
    for s in SCENARIOS:
        try:
            nums.append(int(s["id"].split("-")[-1]))
        except ValueError:
            pass
    return f"SCN-{(max(nums) + 1):03d}" if nums else "SCN-001"


# 工作台菜单（用于扩展）
WORKBENCH_MENU = [
    {"name": "流程审批", "items": [
        {"label": "交易复核", "key": "transaction-review", "badge": 68},
        {"label": "清算审批", "key": "clearing-review", "badge": 12},
        {"label": "调账审核", "key": "adjust-review",   "badge": 3},
    ]},
    {"name": "证实确认", "items": [
        {"label": "证实匹配", "key": "confirm-match"},
        {"label": "证实明细", "key": "confirm-detail"},
        {"label": "证实报文", "key": "confirm-msg"},
    ]},
    {"name": "清算结算", "items": [
        {"label": "待轧差处理", "key": "netting"},
        {"label": "待发报处理", "key": "dispatch"},
        {"label": "来账分拣", "key": "incoming-sort"},
        {"label": "支付假日调整", "key": "holiday-adjust"},
        {"label": "收付撤销", "key": "payment-cancel"},
        {"label": "收付报文", "key": "payment-msg"},
        {"label": "结算路径", "key": "settle-route"},
    ]},
    {"name": "会计核算", "items": [
        {"label": "计量跟踪处理", "key": "measure-track"},
        {"label": "送账异常处理", "key": "post-error"},
        {"label": "余额初始", "key": "balance-init"},
        {"label": "手工指定", "key": "manual-assign"},
        {"label": "阀值放行", "key": "threshold-pass"},
    ]},
    {"name": "每日核对", "items": [
        {"label": "托管机构余额核对", "key": "custodian-recon"},
    ]},
    {"name": "交易录入", "items": [
        {"label": "单边现金流", "key": "cashflow-entry"},
    ]},
    {"name": "业务管理", "items": [
        {"label": "定盘管理", "key": "fix-mgmt"},
    ]},
]
