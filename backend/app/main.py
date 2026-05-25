"""RCS-Demo 后端入口

FastAPI 应用，为前端提供：
- 工作台菜单
- 交易复核 列表 / 单笔审批 / 批量审批

启动：
    uvicorn app.main:app --reload --port 8000
"""

from __future__ import annotations
from typing import List, Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .mock_data import (
    TRANSACTION_REVIEWS,
    WORKBENCH_MENU,
    TAX_RULES,
    SCENARIOS,
    PORTFOLIOS,
    RULE_CONDITION_POOL,
    get_dataset,
    _next_tax_rule_id,
    _next_scenario_id,
)


app = FastAPI(title="RCS-Demo API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------------------------------- #
# 响应模型
# --------------------------------------------------------------------------- #
class TransactionReviewItem(BaseModel):
    externalNo: str = Field(..., description="外部流水号")
    tradeNo: str = Field(..., description="交易流水号")
    product: str
    action: str
    valueDate: str = Field(..., description="起息日")
    tradeDate: str = Field(..., description="交易日")
    counterparty: str
    instrument: str = Field(..., description="标的")
    usdAmount: float = Field(..., description="折美金额")
    direction: str = Field(..., description="买卖方向")
    reviewer: str = Field(..., description="审核")


class TransactionReviewList(BaseModel):
    items: List[TransactionReviewItem]
    total: int
    page: int
    pageSize: int


class BatchApprovePayload(BaseModel):
    ids: List[str]


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _row_to_camel(row: dict) -> dict:
    return {
        "externalNo":   row["external_no"],
        "tradeNo":      row["trade_no"],
        "product":      row["product"],
        "action":       row["action"],
        "valueDate":    row["value_date"],
        "tradeDate":    row["trade_date"],
        "counterparty": row["counterparty"],
        "instrument":   row["instrument"],
        "usdAmount":    row["usd_amount"],
        "direction":    row["direction"],
        "reviewer":     row["reviewer"],
    }


# --------------------------------------------------------------------------- #
# Routes
# --------------------------------------------------------------------------- #
@app.get("/api/health")
def health():
    return {"status": "ok", "service": "RCS-Demo", "rows": len(TRANSACTION_REVIEWS)}


@app.get("/api/workbench/menu")
def workbench_menu():
    return {"groups": WORKBENCH_MENU}


@app.get("/api/workbench/transaction-review", response_model=TransactionReviewList)
def list_transaction_review(
    tab: str = Query("approve", description="审批/补发/交易事件"),
    externalNo: Optional[str] = None,
    tradeNo: Optional[str] = None,
    page: int = 1,
    pageSize: int = 20,
):
    dataset = get_dataset(tab)

    # 过滤
    rows = dataset
    if externalNo:
        rows = [r for r in rows if externalNo in r["external_no"]]
    if tradeNo:
        rows = [r for r in rows if tradeNo in r["trade_no"]]

    total = len(rows)
    start = (page - 1) * pageSize
    end = start + pageSize
    page_rows = rows[start:end]

    return {
        "items": [_row_to_camel(r) for r in page_rows],
        "total": total,
        "page": page,
        "pageSize": pageSize,
    }


@app.post("/api/workbench/transaction-review/{trade_no}/approve")
def approve_one(trade_no: str):
    return {"ok": True, "approved": [trade_no]}


@app.post("/api/workbench/transaction-review/batch-approve")
def batch_approve(payload: BatchApprovePayload):
    return {"ok": True, "approved": payload.ids, "count": len(payload.ids)}


# --------------------------------------------------------------------------- #
# 税务规则配置接口
# --------------------------------------------------------------------------- #
class TaxRuleItem(BaseModel):
    id: str
    isActive: bool
    effectiveDate: str
    country: str
    productCategory: str
    counterpartyTypes: List[str]
    direction: str
    taxRate: float
    taxBase: str
    settlementImpact: str
    taxTimingBase: str
    taxTimingOffset: int
    createdBy: str
    createdAt: str


class TaxRuleList(BaseModel):
    items: List[TaxRuleItem]
    total: int


class SaveTaxRulePayload(BaseModel):
    country: str
    productCategory: str
    counterpartyTypes: List[str]
    direction: str = "pay"
    taxRate: float
    taxBase: str
    settlementImpact: str
    taxTimingBase: str
    taxTimingOffset: int = 0
    effectiveDate: str
    isActive: bool = True
    sourceId: Optional[str] = None   # 复制来源规则ID


def _rule_to_camel(r: dict) -> dict:
    return {
        "id": r["id"],
        "isActive": r["is_active"],
        "effectiveDate": r["effective_date"],
        "country": r["country"],
        "productCategory": r["product_category"],
        "counterpartyTypes": r["counterparty_types"],
        "direction": r["direction"],
        "taxRate": r["tax_rate"],
        "taxBase": r["tax_base"],
        "settlementImpact": r["settlement_impact"],
        "taxTimingBase": r["tax_timing_base"],
        "taxTimingOffset": r["tax_timing_offset"],
        "createdBy": r["created_by"],
        "createdAt": r["created_at"],
    }


@app.get("/api/base-data/tax-rules", response_model=TaxRuleList)
def list_tax_rules(
    country: Optional[str] = None,
    productCategory: Optional[str] = None,
    counterpartyTypes: Optional[str] = None,
    isActive: Optional[str] = None,
):
    rows = list(TAX_RULES)
    if country:
        rows = [r for r in rows if r["country"] == country]
    if productCategory:
        rows = [r for r in rows if r["product_category"] == productCategory]
    if counterpartyTypes:
        allowed = [v.strip() for v in counterpartyTypes.split(",") if v.strip()]
        rows = [r for r in rows if any(t in allowed for t in r["counterparty_types"])]
    if isActive is not None:
        flag = isActive.lower() == "true"
        rows = [r for r in rows if r["is_active"] == flag]
    return {"items": [_rule_to_camel(r) for r in rows], "total": len(rows)}


@app.post("/api/base-data/tax-rules", response_model=TaxRuleItem)
def create_tax_rule(payload: SaveTaxRulePayload):
    from datetime import date as _date
    new_rule = {
        "id": _next_tax_rule_id(),
        "is_active": payload.isActive,
        "effective_date": payload.effectiveDate,
        "country": payload.country,
        "product_category": payload.productCategory,
        "counterparty_types": payload.counterpartyTypes,
        "direction": payload.direction,
        "tax_rate": payload.taxRate,
        "tax_base": payload.taxBase,
        "settlement_impact": payload.settlementImpact,
        "tax_timing_base": payload.taxTimingBase,
        "tax_timing_offset": payload.taxTimingOffset,
        "created_by": "current_user",
        "created_at": _date.today().isoformat(),
    }
    TAX_RULES.append(new_rule)
    return _rule_to_camel(new_rule)


@app.put("/api/base-data/tax-rules/{rule_id}", response_model=TaxRuleItem)
def update_tax_rule(rule_id: str, payload: SaveTaxRulePayload):
    for r in TAX_RULES:
        if r["id"] == rule_id:
            r["is_active"] = payload.isActive
            r["effective_date"] = payload.effectiveDate
            r["country"] = payload.country
            r["product_category"] = payload.productCategory
            r["counterparty_types"] = payload.counterpartyTypes
            r["direction"] = payload.direction
            r["tax_rate"] = payload.taxRate
            r["tax_base"] = payload.taxBase
            r["settlement_impact"] = payload.settlementImpact
            r["tax_timing_base"] = payload.taxTimingBase
            r["tax_timing_offset"] = payload.taxTimingOffset
            return _rule_to_camel(r)
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="规则不存在")


@app.patch("/api/base-data/tax-rules/{rule_id}/toggle", response_model=TaxRuleItem)
def toggle_tax_rule(rule_id: str):
    for r in TAX_RULES:
        if r["id"] == rule_id:
            r["is_active"] = not r["is_active"]
            return _rule_to_camel(r)
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="规则不存在")


@app.delete("/api/base-data/tax-rules/{rule_id}")
def delete_tax_rule(rule_id: str):
    for i, r in enumerate(TAX_RULES):
        if r["id"] == rule_id:
            TAX_RULES.pop(i)
            return {"ok": True, "id": rule_id}
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="规则不存在")


# --------------------------------------------------------------------------- #
# 损益归因 - 情景查询接口
# --------------------------------------------------------------------------- #
class ScenarioItem(BaseModel):
    id: str
    name: str
    portfolio: str
    attributionMethod: str
    calculationScheme: str
    currency: str
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    ruleConditions: List[str]


class ScenarioList(BaseModel):
    items: List[ScenarioItem]
    total: int


class SaveScenarioPayload(BaseModel):
    name: str
    portfolio: str
    attributionMethod: str
    calculationScheme: str
    currency: str
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    ruleConditions: List[str]


def _scenario_to_camel(s: dict) -> dict:
    return {
        "id": s["id"],
        "name": s["name"],
        "portfolio": s["portfolio"],
        "attributionMethod": s["attribution_method"],
        "calculationScheme": s["calculation_scheme"],
        "currency": s["currency"],
        "startDate": s.get("start_date"),
        "endDate": s.get("end_date"),
        "ruleConditions": s["rule_conditions"],
    }


@app.get("/api/pnl/scenarios", response_model=ScenarioList)
def list_scenarios(
    name: Optional[str] = None,
    portfolio: Optional[str] = None,
    page: int = 1,
    pageSize: int = 20,
):
    rows = list(SCENARIOS)
    if name:
        rows = [r for r in rows if name.lower() in r["name"].lower()]
    if portfolio:
        rows = [r for r in rows if r["portfolio"] == portfolio]
    total = len(rows)
    start = (page - 1) * pageSize
    return {"items": [_scenario_to_camel(r) for r in rows[start:start + pageSize]], "total": total}


@app.get("/api/pnl/scenarios/{scenario_id}", response_model=ScenarioItem)
def get_scenario(scenario_id: str):
    for s in SCENARIOS:
        if s["id"] == scenario_id:
            return _scenario_to_camel(s)
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Scenario not found")


@app.get("/api/pnl/portfolios")
def list_portfolios():
    return {"items": PORTFOLIOS}


@app.get("/api/pnl/rule-conditions")
def list_rule_conditions():
    return {"items": RULE_CONDITION_POOL}


@app.post("/api/pnl/scenarios", response_model=ScenarioItem)
def create_scenario(payload: SaveScenarioPayload):
    new_s = {
        "id": _next_scenario_id(),
        "name": payload.name,
        "portfolio": payload.portfolio,
        "attribution_method": payload.attributionMethod,
        "calculation_scheme": payload.calculationScheme,
        "currency": payload.currency,
        "start_date": payload.startDate,
        "end_date": payload.endDate,
        "rule_conditions": payload.ruleConditions,
    }
    SCENARIOS.append(new_s)
    return _scenario_to_camel(new_s)


@app.put("/api/pnl/scenarios/{scenario_id}", response_model=ScenarioItem)
def update_scenario(scenario_id: str, payload: SaveScenarioPayload):
    for s in SCENARIOS:
        if s["id"] == scenario_id:
            s["name"] = payload.name
            s["portfolio"] = payload.portfolio
            s["attribution_method"] = payload.attributionMethod
            s["calculation_scheme"] = payload.calculationScheme
            s["currency"] = payload.currency
            s["start_date"] = payload.startDate
            s["end_date"] = payload.endDate
            s["rule_conditions"] = payload.ruleConditions
            return _scenario_to_camel(s)
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Scenario not found")


@app.delete("/api/pnl/scenarios/{scenario_id}")
def delete_scenario(scenario_id: str):
    for i, s in enumerate(SCENARIOS):
        if s["id"] == scenario_id:
            SCENARIOS.pop(i)
            return {"ok": True, "id": scenario_id}
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Scenario not found")
