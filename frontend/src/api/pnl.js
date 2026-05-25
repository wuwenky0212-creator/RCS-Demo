/**
 * 损益归因 API — 本地 Mock（无后端时直接返回数据）
 */
import { PORTFOLIOS } from '@/data/bookStructure.js'

// ── 金融产品（只涉及以下 6 种）────────────────────────────────────────────────
const RULE_CONDITION_ITEMS = [
  'FX Spot',
  'FX Forward',
  'FX Swap',
  'FX Option',
  'CCS',
  'IRS',
]

// ── 情景 Mock 数据（portfolio 取自簿记架构，按 Book 层级选取）────────────────
let _scenarios = [
  {
    id: 'S001',
    name: 'Scenario 1',
    portfolio:          'OBIDTFXD',      // Book 层级：代客外汇组
    attributionMethod:  '重估值',
    calculationScheme:  '累计模式',
    currency:           'USD',
    startDate:          '2026-05-01',
    endDate:            '2026-05-21',
    ruleConditions:     ['FX Spot', 'FX Forward'],
  },
]

let _nextId = 2

function delay(ms = 120) {
  return new Promise(r => setTimeout(r, ms))
}

// ── 情景查询 ──────────────────────────────────────────────────────────────────
export async function listScenarios({ name, portfolio, page = 1, pageSize = 20 } = {}) {
  await delay()
  let items = [..._scenarios]
  if (name)      items = items.filter(s => s.name.includes(name))
  if (portfolio) items = items.filter(s => s.portfolio === portfolio)
  const start = (page - 1) * pageSize
  return { items: items.slice(start, start + pageSize), total: items.length }
}

export async function getScenario(id) {
  await delay()
  const s = _scenarios.find(s => s.id === id)
  if (!s) throw new Error('Not found')
  return s
}

export async function createScenario(data) {
  await delay()
  const newItem = { ...data, id: `S${String(_nextId++).padStart(3, '0')}` }
  _scenarios.push(newItem)
  return newItem
}

export async function updateScenario(id, data) {
  await delay()
  const idx = _scenarios.findIndex(s => s.id === id)
  if (idx === -1) throw new Error('Not found')
  _scenarios[idx] = { ..._scenarios[idx], ...data }
  return _scenarios[idx]
}

export async function deleteScenario(id) {
  await delay()
  _scenarios = _scenarios.filter(s => s.id !== id)
  return { ok: true }
}

// ── 基础数据 ──────────────────────────────────────────────────────────────────

/** Portfolio 列表 — 取自簿记架构，格式：code（说明） */
export async function listPortfolios() {
  await delay()
  const items = PORTFOLIOS.map(p => p.code)
  return { items }
}

/** 金融产品（规则条件）— 仅 6 种 */
export async function listRuleConditions() {
  await delay()
  return { items: RULE_CONDITION_ITEMS }
}
