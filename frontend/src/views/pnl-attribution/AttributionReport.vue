<template>
  <div class="attribution-report">
    <PnlSubNav />

    <!-- ── 情景信息栏 ── -->
    <div class="ar-infobar">
      <div class="info-left">
        <div class="scenario-avatar">S</div>
        <div>
          <div class="scenario-name">{{ scenarioName }}</div>
          <div class="scenario-meta">{{ t('pnlAttribution.accountLabel') }}：{{ portfolio }} &nbsp;|&nbsp; {{ t('pnlAttribution.currencyLabel') }}：{{ currency }}</div>
        </div>
      </div>
      <div class="info-right">
        <div class="filter-item">
          <span class="filter-lbl">* {{ t('pnlAttribution.scenarioLabel') }}</span>
          <el-select :placeholder="t('common.pleaseSelect')" size="small" style="width:150px;" />
        </div>
        <div class="filter-item">
          <span class="filter-lbl">* {{ t('pnlAttribution.dateLabel') }}</span>
          <el-date-picker type="daterange" size="small" range-separator="—"
            :start-placeholder="t('common.startDate')" :end-placeholder="t('common.endDate')" style="width:230px;" />
        </div>
        <!-- 视图切换 -->
        <div class="view-toggle">
          <button
            class="vt-btn"
            :class="{ active: viewMode === 'table' }"
            @click="viewMode = 'table'"
          >
            <el-icon><Grid /></el-icon>
            {{ t('pnlAttribution.viewTable') }}
          </button>
          <button
            class="vt-btn"
            :class="{ active: viewMode === 'dashboard' }"
            @click="viewMode = 'dashboard'"
          >
            <el-icon><PieChart /></el-icon>
            {{ t('pnlAttribution.viewDashboard') }}
          </button>
        </div>
      </div>
    </div>

    <!-- ════════════════════════════════════════════════ -->
    <!-- 表格视图                                          -->
    <!-- ════════════════════════════════════════════════ -->
    <div v-if="viewMode === 'table'" class="ar-table-view">
      <div class="table-toolbar">
        <span class="table-title">{{ t('pnlAttribution.reportTitle') }}</span>
        <div class="toolbar-right">
          <span class="total-hint">
            {{ t('pnlAttribution.grandTotalLabel') }}
            <strong>{{ fmtVal(grandTotal) }}&nbsp;{{ currency }}</strong>
          </span>
          <el-button
            size="small"
            :type="showPct ? 'primary' : ''"
            :plain="!showPct"
            @click="showPct = !showPct"
          >
            {{ t('pnlAttribution.showPctBtn') }}
          </el-button>
          <el-button size="small" plain @click="exportTable">
            <el-icon><Download /></el-icon> {{ t('pnlAttribution.exportBtn') }}
          </el-button>
        </div>
      </div>

      <!-- ── 归因大表：列 = 计算顺序分类/子类；行 = 金融工具 > 资产标的 > 明细 ── -->
      <el-table
        :data="tableRows"
        row-key="_rowKey"
        :tree-props="{ children: 'children' }"
        border
        stripe
        size="small"
        :header-cell-style="{ background: '#f5f7fa', color: '#606266', fontWeight: '600', fontSize: '12px' }"
        :summary-method="getSummary"
        show-summary
        style="width: 100%;"
      >
        <!-- ── 固定左列：金融工具 / 资产标的 / 曲线 / 交易明细 ── -->
        <el-table-column prop="_label" min-width="240" fixed="left" class-name="col-label">
          <template #header><span>{{ t('pnlAttribution.dimHeader') }}</span></template>
          <template #default="{ row }">
            <!-- 一级：运营机构 -->
            <span v-if="row._rowType === 'entity'" class="lbl-entity">{{ row._label }}</span>
            <!-- 二级：账户性质 -->
            <span v-else-if="row._rowType === 'acctype'" class="lbl-acctype">{{ row._label }}</span>
            <!-- 三级：账户 -->
            <span v-else-if="row._rowType === 'account'" class="lbl-account">
              {{ row._label }}<span class="lbl-account-sub">{{ row._sublabel }}</span>
            </span>
            <!-- 四级：金融工具 -->
            <span v-else-if="row._rowType === 'instrument'" class="lbl-instrument">{{ row._label }}</span>
            <!-- 五级：资产标的 -->
            <span v-else-if="row._rowType === 'asset'" class="lbl-asset">
              {{ row._label }}<span class="lbl-asset-sub">{{ row._sublabel }}</span>
            </span>
            <!-- 六级：曲线/交易明细 -->
            <span v-else-if="row._rowType === 'curve'" class="lbl-detail">{{ row._label }}</span>
            <span v-else-if="row._rowType === 'deal'" class="lbl-detail">
              {{ t(`pnlAttribution.${row.dealTypeKey}`) }}&nbsp;·&nbsp;{{ row._label }}
            </span>
          </template>
        </el-table-column>

        <!-- ══ 初始化 ══ -->
        <el-table-column :label="t('pnlAttribution.groupInit')" align="center" class-name="col-group-init">
          <el-table-column prop="modelPl" label="Model Assign." min-width="130" align="right">
            <template #default="{ row }">
              <div class="factor-cell">
                <span :class="cellClass(row,'modelPl')">{{ cellVal(row,'modelPl') }}</span>
                <span v-if="showPct && pctText(row,'modelPl')" :class="pctBadgeClass(row,'modelPl')">{{ pctText(row,'modelPl') }}</span>
              </div>
            </template>
          </el-table-column>
        </el-table-column>

        <!-- ══ 时间衰减 ══ -->
        <el-table-column :label="t('pnlAttribution.groupTime')" align="center" class-name="col-group-time">
          <el-table-column prop="timePl" label="Time Decay" min-width="110" align="right">
            <template #default="{ row }">
              <div class="factor-cell">
                <span :class="cellClass(row,'timePl')">{{ cellVal(row,'timePl') }}</span>
                <span v-if="showPct && pctText(row,'timePl')" :class="pctBadgeClass(row,'timePl')">{{ pctText(row,'timePl') }}</span>
              </div>
            </template>
          </el-table-column>
        </el-table-column>

        <!-- ══ 市场数据 ══ -->
        <el-table-column :label="t('pnlAttribution.groupMarket')" align="center" class-name="col-group-mkt">
          <el-table-column prop="spotPl" label="FX Spot" min-width="110" align="right">
            <template #default="{ row }">
              <div class="factor-cell">
                <span :class="cellClass(row,'spotPl')">{{ cellVal(row,'spotPl') }}</span>
                <span v-if="showPct && pctText(row,'spotPl')" :class="pctBadgeClass(row,'spotPl')">{{ pctText(row,'spotPl') }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="yieldCurvePl" label="Yield Curves" min-width="120" align="right">
            <template #default="{ row }">
              <div class="factor-cell">
                <span :class="cellClass(row,'yieldCurvePl')">{{ cellVal(row,'yieldCurvePl') }}</span>
                <span v-if="showPct && pctText(row,'yieldCurvePl')" :class="pctBadgeClass(row,'yieldCurvePl')">{{ pctText(row,'yieldCurvePl') }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="basisCurvePl" label="Basis Curves" min-width="120" align="right">
            <template #default="{ row }">
              <div class="factor-cell">
                <span :class="cellClass(row,'basisCurvePl')">{{ cellVal(row,'basisCurvePl') }}</span>
                <span v-if="showPct && pctText(row,'basisCurvePl')" :class="pctBadgeClass(row,'basisCurvePl')">{{ pctText(row,'basisCurvePl') }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="volPl" label="FX Vol/Smiles" min-width="120" align="right">
            <template #default="{ row }">
              <div class="factor-cell">
                <span :class="cellClass(row,'volPl')">{{ cellVal(row,'volPl') }}</span>
                <span v-if="showPct && pctText(row,'volPl')" :class="pctBadgeClass(row,'volPl')">{{ pctText(row,'volPl') }}</span>
              </div>
            </template>
          </el-table-column>
        </el-table-column>

        <!-- ══ 定盘价 ══ -->
        <el-table-column :label="t('pnlAttribution.groupFixing')" align="center" class-name="col-group-fixing">
          <el-table-column prop="fixingPl" label="Fixings" min-width="110" align="right">
            <template #default="{ row }">
              <div class="factor-cell">
                <span :class="cellClass(row,'fixingPl')">{{ cellVal(row,'fixingPl') }}</span>
                <span v-if="showPct && pctText(row,'fixingPl')" :class="pctBadgeClass(row,'fixingPl')">{{ pctText(row,'fixingPl') }}</span>
              </div>
            </template>
          </el-table-column>
        </el-table-column>

        <!-- ══ 折算 ══ -->
        <el-table-column :label="t('pnlAttribution.groupConv')" align="center" class-name="col-group-conv">
          <el-table-column prop="conversionPl" label="Spot PL Conv." min-width="120" align="right">
            <template #default="{ row }">
              <div class="factor-cell">
                <span :class="cellClass(row,'conversionPl')">{{ cellVal(row,'conversionPl') }}</span>
                <span v-if="showPct && pctText(row,'conversionPl')" :class="pctBadgeClass(row,'conversionPl')">{{ pctText(row,'conversionPl') }}</span>
              </div>
            </template>
          </el-table-column>
        </el-table-column>

        <!-- ══ 交易活动 ══ -->
        <el-table-column :label="t('pnlAttribution.groupTrade')" align="center" class-name="col-group-trade">
          <el-table-column prop="newDealPl" :label="t('pnlAttribution.newDeal')" min-width="100" align="right">
            <template #default="{ row }">
              <div class="factor-cell">
                <span :class="cellClass(row,'newDealPl')">{{ cellVal(row,'newDealPl') }}</span>
                <span v-if="showPct && pctText(row,'newDealPl')" :class="pctBadgeClass(row,'newDealPl')">{{ pctText(row,'newDealPl') }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="modifyPl" :label="t('pnlAttribution.modifyDeal')" min-width="100" align="right">
            <template #default="{ row }">
              <div class="factor-cell">
                <span :class="cellClass(row,'modifyPl')">{{ cellVal(row,'modifyPl') }}</span>
                <span v-if="showPct && pctText(row,'modifyPl')" :class="pctBadgeClass(row,'modifyPl')">{{ pctText(row,'modifyPl') }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="cancelPl" :label="t('pnlAttribution.cancelDeal')" min-width="100" align="right">
            <template #default="{ row }">
              <div class="factor-cell">
                <span :class="cellClass(row,'cancelPl')">{{ cellVal(row,'cancelPl') }}</span>
                <span v-if="showPct && pctText(row,'cancelPl')" :class="pctBadgeClass(row,'cancelPl')">{{ pctText(row,'cancelPl') }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="othersPl" label="Others" min-width="100" align="right">
            <template #default="{ row }">
              <div class="factor-cell">
                <span :class="cellClass(row,'othersPl')">{{ cellVal(row,'othersPl') }}</span>
                <span v-if="showPct && pctText(row,'othersPl')" :class="pctBadgeClass(row,'othersPl')">{{ pctText(row,'othersPl') }}</span>
              </div>
            </template>
          </el-table-column>
        </el-table-column>

        <!-- ══ PL 结果（固定右）══ -->
        <el-table-column :label="t('pnlAttribution.groupResult')" align="center" class-name="col-group-result" fixed="right">
          <!-- P&L Currency: shown at account/portfolio level, — for other levels -->
          <el-table-column :label="t('pnlAttribution.plCurrencyCol')" min-width="76" align="center" fixed="right">
            <template #default="{ row }">
              <span class="ccy-tag">{{ row._plCurrency || '—' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="mvPl" :label="t('pnlAttribution.mvPlCol')" min-width="108" align="right" fixed="right">
            <template #default="{ row }">
              <span :class="cellClass(row,'mvPl')">{{ cellVal(row,'mvPl') }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="mvConvPl" :label="`${t('pnlAttribution.mvConvPlCol')} (${currency})`" min-width="120" align="right" fixed="right">
            <template #default="{ row }">
              <span :class="[cellClass(row,'mvConvPl'), { 'cell-val-result': row._rowType === 'entity' || row._rowType === 'acctype' }]">
                {{ cellVal(row,'mvConvPl') }}
              </span>
            </template>
          </el-table-column>
        </el-table-column>
      </el-table>
    </div>

    <!-- ════════════════════════════════════════════════ -->
    <!-- 仪表盘视图                                        -->
    <!-- ════════════════════════════════════════════════ -->
    <template v-if="viewMode === 'dashboard'">
      <!-- ── 面包屑 ── -->
      <div class="ar-breadcrumb">
        <span class="crumb crumb-home" @click="collapseToDepth(0)">
          <el-icon><HomeFilled /></el-icon> {{ t('pnlAttribution.breadcrumbSummary') }}
        </span>
        <template v-for="(label, i) in breadcrumbTail" :key="i">
          <span class="crumb-sep">›</span>
          <span
            class="crumb"
            :class="{ 'crumb-active': i === breadcrumbTail.length - 1 }"
            @click="collapseToDepth(i + 1)"
          >{{ label }}</span>
        </template>
      </div>

      <!-- ── 横向面板区 ── -->
      <div class="ar-panels-scroll">
        <div class="ar-panels-row">

          <!-- 数据面板 (0 ~ expandedDepth) -->
          <div
            v-for="(panel, pi) in visiblePanels"
            :key="panel.key"
            class="ar-panel"
          >
            <div class="panel-hd">
              <el-icon class="panel-icon"><DataLine /></el-icon>
              <span class="panel-title">{{ panel.label }}</span>
              <span class="panel-count">{{ panel.items.length }}{{ t('pnlAttribution.dashTimePct') }}</span>
            </div>

            <div class="panel-body">
              <div
                v-for="item in panel.items"
                :key="item.id"
                class="panel-item"
                :class="{ active: selections[pi] === item.id }"
                @click="selectItem(pi, item)"
              >
                <div class="pi-row">
                  <span class="pi-name">{{ item.name }}</span>
                  <span class="pi-val">{{ fmtVal(item.value) }}</span>
                  <el-icon v-if="selections[pi] === item.id" class="pi-arrow"><ArrowRight /></el-icon>
                </div>
                <div class="pi-pct">{{ t('pnlAttribution.pctLabel') }} {{ item.pct.toFixed(2) }}%</div>
                <div class="pi-bar-track">
                  <div class="pi-bar-fill" :style="{ width: item.pct + '%', background: item.color }" />
                </div>
              </div>
            </div>

            <div class="panel-ft">{{ t('pnlAttribution.totalLabel') }} &nbsp;<strong>1,250.50 CNY</strong></div>
          </div>

          <!-- 图表面板（始终显示，数据跟随当前最深层） -->
          <div class="ar-chart-panel">
            <div class="cp-title">{{ chartTitle }}</div>
            <div class="cp-total-lbl">{{ t('pnlAttribution.totalLabel') }}</div>
            <div class="cp-total-val">{{ fmtVal(chartTotal) }} {{ currency }}</div>

            <div class="cp-donut-wrap">
              <svg viewBox="0 0 200 200" class="cp-donut">
                <circle cx="100" cy="100" r="70" fill="none" stroke="#f0f2f5" stroke-width="28" />
                <circle
                  v-for="seg in chartSegments"
                  :key="seg.id"
                  cx="100" cy="100" r="70"
                  fill="none"
                  :stroke="seg.color"
                  stroke-width="28"
                  :stroke-dasharray="seg.dasharray"
                  :stroke-dashoffset="seg.dashoffset"
                />
              </svg>
            </div>

            <div class="cp-legend">
              <div v-for="item in activeChartItems" :key="item.id" class="leg-row">
                <span class="leg-dot" :style="{ background: item.color }" />
                <span class="leg-name">{{ item.name }}</span>
                <div class="leg-nums">
                  <span class="leg-val">{{ fmtVal(item.value) }}</span>
                  <span class="leg-pct">{{ ((item.value / chartTotal) * 100).toFixed(2) }}%</span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </template>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { ArrowRight, HomeFilled, DataLine, Grid, PieChart, Download } from '@element-plus/icons-vue'
import PnlSubNav from '@/components/PnlSubNav.vue'
import { getScenario } from '@/api/pnl'
import * as XLSX from 'xlsx'

const route = useRoute()
const { t, locale } = useI18n()
const isEn = computed(() => locale.value === 'en-US')

// ── 视图模式 ─────────────────────────────────────────────────────────────────
const viewMode = ref('table')

// ── 占比模式（因子列显示贡献百分比） ──────────────────────────────────────────
const showPct = ref(false)

// ── 情景基础信息（从 API 加载） ──────────────────────────────────────────────
const scenarioName = ref(route.query.name || 'Scenario 1')
const portfolio    = ref('—')
const currency     = ref('USD')   // 报告货币，跟随情景设置

// ── 日终即期汇率（各币种兑 CNY，T 日收盘价）────────────────────────────────────
const SPOT_RATES_CNY = {
  CNY: 1.0000,
  USD: 7.2456,
  EUR: 7.8821,
  GBP: 9.1234,
  AUD: 4.7823,
  JPY: 0.0464,
}

// 将金额从 fromCcy 折算为报告货币 toCcy（均以 CNY 为中间货币）
function convertToReport(amount, fromCcy, toCcy) {
  if (amount == null) return null
  const from = SPOT_RATES_CNY[fromCcy] ?? 1
  const to   = SPOT_RATES_CNY[toCcy]   ?? 1
  return parseFloat((amount * from / to).toFixed(2))
}

// ── 产品名称映射 ──────────────────────────────────────────────────────────────
const PRODUCT_META_RAW = {
  'FX Spot':    { nameKey: 'productFxSpot',    color: '#4a7ede' },
  'FX Forward': { nameKey: 'productFxForward', color: '#36c9a0' },
  'FX Swap':    { nameKey: 'productFxSwap',    color: '#f56c6c' },
  'FX Option':  { nameKey: 'productFxOption',  color: '#f0a500' },
  'CCS':        { nameKey: 'productCcs',        color: '#9b59b6' },
  'IRS':        { nameKey: 'productIrs',        color: '#27ae60' },
}
const PRODUCT_META = computed(() =>
  Object.fromEntries(
    Object.entries(PRODUCT_META_RAW).map(([k, v]) => [k, {
      zhName: t(`pnlAttribution.${v.nameKey}`),
      color:  v.color,
    }])
  )
)

// ── 账户元数据（由 bookStructure 动态生成）────────────────────────────────────
import { PORTFOLIOS as _PORTFOLIOS } from '@/data/bookStructure.js'
// 响应语言切换的账户元数据
const FOLDER_META = computed(() =>
  Object.fromEntries(
    _PORTFOLIOS.map(p => [p.code, {
      entity:      'OBID (Jakarta Branch)',
      accountType: isEn.value ? (p.accountTypeEn || p.accountType) : p.accountType,
      accountName: isEn.value ? (p.descriptionEn  || p.description) : p.description,
      plCurrency:  'USD',
    }])
  )
)

// ── 仪表盘：产品面板条目 ──────────────────────────────────────────────────────
const BASE_VALS = [562.73, 437.68, 250.09, 180.00, 120.00, 100.00]
function buildProductItems(ruleConditions) {
  const total = ruleConditions.reduce((s, _, i) => s + (BASE_VALS[i] ?? 100), 0)
  return ruleConditions.map((rc, i) => {
    const meta  = PRODUCT_META.value[rc] || { zhName: rc, color: '#4a7ede' }
    const value = BASE_VALS[i] ?? 100
    return { id: `prod_${i}`, name: meta.zhName, value, color: meta.color, pct: (value / total) * 100 }
  })
}

// ── 曲线 / 交易明细（三级 detail 行）────────────────────────────────────────
// 注：FX Spot 无曲线明细，只有交易动作明细
// FX Forward 曲线明细：各期限节点 yieldCurvePl / basisCurvePl 之和 = 头寸 yieldCurvePl / basisCurvePl
const DETAIL_ROWS = {
  // FX Spot：仅交易动作明细（无曲线）
  'FXS-2024-0081': [
    { _rowType: 'deal', _rowKey: 'deal_FXS-2024-0081_D081',  _label: 'FXS-D-081',
      dealTypeKey: 'dealTypeNew', newDealPl: 29.13 },
  ],
  'FXS-2024-0092': [
    { _rowType: 'deal', _rowKey: 'deal_FXS-2024-0092_D092a', _label: 'FXS-D-092a',
      dealTypeKey: 'dealTypeNew', newDealPl: 18.00 },
    { _rowType: 'deal', _rowKey: 'deal_FXS-2024-0092_D092b', _label: 'FXS-D-092b',
      dealTypeKey: 'dealTypeCancel', cancelPl: -4.60 },
  ],
  // FX Forward：曲线期限节点 + 交易动作明细
  // FXF-2024-0033：yieldCurvePl(-28.30) = (-45.80)+(17.50)；basisCurvePl(135.20) = 81.12+54.08
  // SOFR 短端上行 → 负；长端回落 → 正；XCCY 基差收窄 → 两段均正
  'FXF-2024-0033': [
    { _rowType: 'curve', _rowKey: 'curve_FXF-2024-0033_SOFR-3M', _label: 'SOFR-USD (3M)',      yieldCurvePl: -45.80 },
    { _rowType: 'curve', _rowKey: 'curve_FXF-2024-0033_SOFR-6M', _label: 'SOFR-USD (6M)',      yieldCurvePl:  17.50 },
    { _rowType: 'curve', _rowKey: 'curve_FXF-2024-0033_XCCY-3M', _label: 'XCCY-USD/CNY (3M)', basisCurvePl:  81.12 },
    { _rowType: 'curve', _rowKey: 'curve_FXF-2024-0033_XCCY-6M', _label: 'XCCY-USD/CNY (6M)', basisCurvePl:  54.08 },
    { _rowType: 'deal',  _rowKey: 'deal_FXF-2024-0033_D051',      _label: 'FXF-D-051',
      dealTypeKey: 'dealTypeCancel', cancelPl: -20.75 },
  ],
  // FXF-2024-0047：yieldCurvePl(-22.80) = (8.20)+(-31.00)；basisCurvePl(77.14) = 44.72+32.42
  // SOFR 短端小幅改善 → 正；长端大幅上行 → 负；XCCY 基差收窄 → 两段均正
  'FXF-2024-0047': [
    { _rowType: 'curve', _rowKey: 'curve_FXF-2024-0047_SOFR-3M', _label: 'SOFR-USD (3M)',      yieldCurvePl:   8.20 },
    { _rowType: 'curve', _rowKey: 'curve_FXF-2024-0047_SOFR-6M', _label: 'SOFR-USD (6M)',      yieldCurvePl: -31.00 },
    { _rowType: 'curve', _rowKey: 'curve_FXF-2024-0047_XCCY-3M', _label: 'XCCY-USD/CNY (3M)', basisCurvePl:  44.72 },
    { _rowType: 'curve', _rowKey: 'curve_FXF-2024-0047_XCCY-6M', _label: 'XCCY-USD/CNY (6M)', basisCurvePl:  32.42 },
    { _rowType: 'deal',  _rowKey: 'deal_FXF-2024-0047_D047a',     _label: 'FXF-D-047a',
      dealTypeKey: 'dealTypeAmend', modifyPl: 20.00 },
    { _rowType: 'deal',  _rowKey: 'deal_FXF-2024-0047_D047b',     _label: 'FXF-D-047b',
      dealTypeKey: 'dealTypeCancel', cancelPl: -31.57 },
  ],
}

// ── 工具：字段求和 / null 压缩 ────────────────────────────────────────────────
function sumField(arr, field) {
  return arr.reduce((s, p) => s + (p[field] || 0), 0)
}
function orNull(v) {
  const n = parseFloat(v.toFixed(2))
  return n !== 0 ? n : null
}

// ── 构造 asset 级树行（二级，children = 曲线/交易明细）────────────────────────
function buildAssetRow(pos) {
  const details = DETAIL_ROWS[pos.assetId] || []
  return {
    _rowKey:      `asset_${pos.assetId}`,
    _rowType:     'asset',
    _label:       pos.assetId,
    _sublabel:    pos.underlying,
    initialPl:    pos.initialPl,
    modelPl:      pos.modelPl,
    timePl:       pos.timePl,
    spotPl:       pos.spotPl,
    yieldCurvePl: pos.yieldCurvePl,
    basisCurvePl: pos.basisCurvePl,
    volPl:        pos.volPl,
    fixingPl:     pos.fixingPl,
    conversionPl: pos.conversionPl,
    newDealPl:    pos.newDealPl,
    modifyPl:     pos.modifyPl,
    cancelPl:     pos.cancelPl,
    mvPl:         pos.mvPl,
    mvConvPl:     pos.mvConvPl,
    children:     details.length ? details : undefined,
  }
}

// ── 头寸 mock 数据 ────────────────────────────────────────────────────────────
// 范围：OBIDTFXD 代客外汇组（交易账户），仅含 FX Spot + FX Forward
//
// 因子列单位 = 头寸货币（posCurrency）
// 各因子之和 = mvPl（头寸货币）
// mvConvPl / cashConvPl 由 convertToReport() 动态折算为报告货币（USD）
//
// 汇率参考（SPOT_RATES_CNY）：USD=7.2456，EUR=7.8821 → EUR/USD=1.0879
//
// 因子设计原则：
//   FX Spot  → 无时间衰减(timePl=null)，无利率曲线；spotPl 为主因，加新增交易动作
//   FX Fwd   → timePl（利差carry）+ spotPl + yieldCurvePl + basisCurvePl + conversionPl（EUR头寸折算效应）+ 交易动作
//   conversionPl：仅 EUR 头寸非空，表示 EUR/USD 汇率变动对存量头寸价值的折算影响
//
// 各头寸因子加总验证（括号内为校验式）：
//   FXS-0081：91.17 + 29.13 = 120.30 ✓
//   FXS-0092：(-21.80) + 18.00 + (-4.60) = -8.40 ✓
//   FXF-0033：67.30 + 82.40 + (-28.30) + 135.20 + (-20.75) = 235.85 ✓
//   FXF-0047：45.20 + 38.43 + (-22.80) + 77.14 + (-5.60) + 20.00 + (-31.57) = 120.80 ✓
//
// 当日市场情景：
//   USD/CNY 小幅走强；EUR/CNY 小幅走弱；EUR/USD 轻微走弱
//   SOFR 短端上行(-45.80/-31.00)，长端回落(+17.50/+8.20) → yieldCurvePl 有正有负
//   XCCY USD/CNY 基差大幅收窄 → basisCurvePl 大正贡献
//   D303（多 EUR 即期）当日亏损；D601（空 EUR 远期）因 EUR 走弱反而盈利

const POSITION_MOCK_ALL = [
  // ── FX Spot ────────────────────────────────────────────────────────────────
  {
    // D302：代客即期 USD/CNY，净多 USD — USD 走强，当日正收益
    assetId: 'FXS-2024-0081', instrument: 'FX Spot', underlying: 'USD/CNY',
    posCurrency: 'USD', foldersCode: 'OBIDTFXD_D302', siteCode: 'OBID',
    mvPl: 120.30, cashPl: null, cashConvPl: null,
    modelPl: null,  timePl: null,       // Spot 无时间衰减
    spotPl:    91.17,                   // USD/CNY 上行 → 多 USD 盈利
    yieldCurvePl: null, basisCurvePl: null, volPl: null, fixingPl: null,
    conversionPl: null,                 // USD 头寸无折算效应
    newDealPl: 29.13, modifyPl: null, cancelPl: null, othersPl: null,
  },
  {
    // D303：代客即期 EUR/CNY，净多 EUR — EUR/CNY 走弱，当日净亏损
    assetId: 'FXS-2024-0092', instrument: 'FX Spot', underlying: 'EUR/CNY',
    posCurrency: 'EUR', foldersCode: 'OBIDTFXD_D303', siteCode: 'OBID',
    mvPl: -8.40, cashPl: null, cashConvPl: null,
    modelPl: null, timePl: null,        // Spot 无时间衰减
    spotPl:   -21.80,                   // EUR/CNY 下行 → 多 EUR 亏损
    yieldCurvePl: null, basisCurvePl: null, volPl: null, fixingPl: null,
    conversionPl: null,
    newDealPl: 18.00, modifyPl: null, cancelPl: -4.60, othersPl: null,
  },
  // ── FX Forward ─────────────────────────────────────────────────────────────
  {
    // D501：USD/CNY 3M 远期，净多 USD
    // spot 正贡献；SOFR 短端上行拖累但被基差大幅收窄抵消有余
    assetId: 'FXF-2024-0033', instrument: 'FX Forward', underlying: 'USD/CNY 3M',
    posCurrency: 'USD', foldersCode: 'OBIDTFXD_D501', siteCode: 'OBID',
    mvPl: 235.85, cashPl: 12.30, cashConvPl: null,
    modelPl: null,
    timePl:        67.30,   // Carry：USD 远期升水，时间衰减正贡献
    spotPl:        82.40,   // USD/CNY 即期上行贡献
    yieldCurvePl: -28.30,   // SOFR 短端上行(-45.80) 被长端回落(+17.50) 部分抵消，净负
    basisCurvePl: 135.20,   // XCCY USD/CNY 基差大幅收窄 → 大正贡献
    volPl: null, fixingPl: null,
    conversionPl: null,     // USD 头寸无折算效应
    newDealPl: null, modifyPl: null, cancelPl: -20.75, othersPl: null,
  },
  {
    // D601：EUR/CNY 6M 远期，净空 EUR（对冲客户即期多头）
    // EUR 走弱 → 空头远期盈利；EUR/USD 走弱产生负的折算效应
    assetId: 'FXF-2024-0047', instrument: 'FX Forward', underlying: 'EUR/CNY 6M',
    posCurrency: 'EUR', foldersCode: 'OBIDTFXD_D601', siteCode: 'OBID',
    mvPl: 120.80, cashPl: 8.50, cashConvPl: null,
    modelPl: null,
    timePl:        45.20,   // Carry 正贡献
    spotPl:        38.43,   // EUR/CNY 下行 → 空 EUR 远期盈利
    yieldCurvePl: -22.80,   // SOFR 短端小幅改善(+8.20) 被长端大幅回落(-31.00) 抵消，净负
    basisCurvePl:  77.14,   // XCCY EUR/CNY 基差改善 → 正贡献
    volPl: null, fixingPl: null,
    conversionPl:  -5.60,   // EUR/USD 走弱 → EUR 多头名义折算损失（负贡献）
    newDealPl: null, modifyPl: 20.00, cancelPl: -31.57, othersPl: null,
  },
]

// ── 情景所含产品（OBIDTFXD 交易账户：FX Spot + FX Forward）──────────────────
const scenarioProducts = ref(['FX Spot', 'FX Forward'])

// ── 分组工具 ─────────────────────────────────────────────────────────────────
function groupBy(arr, key) {
  return arr.reduce((acc, item) => {
    const k = typeof key === 'function' ? key(item) : item[key]
    ;(acc[k] = acc[k] || []).push(item)
    return acc
  }, {})
}

// 对一批头寸汇总所有 PL 字段
function sumAllPl(arr) {
  return {
    initialPl:    parseFloat(sumField(arr, 'initialPl').toFixed(2)),
    modelPl:      orNull(sumField(arr, 'modelPl')),
    timePl:       parseFloat(sumField(arr, 'timePl').toFixed(2)),
    spotPl:       orNull(sumField(arr, 'spotPl')),
    yieldCurvePl: orNull(sumField(arr, 'yieldCurvePl')),
    basisCurvePl: orNull(sumField(arr, 'basisCurvePl')),
    volPl:        orNull(sumField(arr, 'volPl')),
    fixingPl:     orNull(sumField(arr, 'fixingPl')),
    conversionPl: parseFloat(sumField(arr, 'conversionPl').toFixed(2)),
    newDealPl:    orNull(sumField(arr, 'newDealPl')),
    modifyPl:     orNull(sumField(arr, 'modifyPl')),
    cancelPl:     orNull(sumField(arr, 'cancelPl')),
    othersPl:     orNull(sumField(arr, 'othersPl')),
    cashPl:       orNull(sumField(arr, 'cashPl')),
    cashConvPl:   orNull(sumField(arr, 'cashConvPl')),
    mvPl:         parseFloat(sumField(arr, 'mvPl').toFixed(2)),
    mvConvPl:     parseFloat(sumField(arr, 'mvConvPl').toFixed(2)),
    // 总损益 = MV损益 + Cash损益（头寸货币）；总损益折算 = MV折算 + Cash折算（报告货币）
    totalPl:      parseFloat((sumField(arr, 'mvPl') + sumField(arr, 'cashPl')).toFixed(2)),
    totalConvPl:  parseFloat((sumField(arr, 'mvConvPl') + sumField(arr, 'cashConvPl')).toFixed(2)),
  }
}

// ── 表格行：运营机构 > 账户性质 > 账户 > 金融工具 > 资产标的 > 曲线/交易明细 ──
const tableRows = computed(() => {
  const prods  = scenarioProducts.value
  const rptCcy = currency.value && currency.value !== '—' ? currency.value : 'USD'

  const positions = POSITION_MOCK_ALL
    .filter(p => prods.includes(p.instrument))
    .map(p => ({
      ...p,
      ...(FOLDER_META.value[p.foldersCode] || { entity: p.siteCode, accountType: isEn.value ? 'Other' : '其他', accountName: p.foldersCode }),
      // 按报告货币重新折算
      mvConvPl:   convertToReport(p.mvPl,   p.posCurrency, rptCcy),
      cashConvPl: p.cashPl != null ? convertToReport(p.cashPl, p.posCurrency, rptCcy) : null,
    }))

  // 一级：按运营机构分组
  return Object.entries(groupBy(positions, 'entity')).map(([entity, entPos]) => ({
    _rowKey:  `ent_${entity}`,
    _rowType: 'entity',
    _label:   entity,
    ...sumAllPl(entPos),

    // 二级：按账户性质分组
    children: Object.entries(groupBy(entPos, 'accountType')).map(([accType, atPos]) => ({
      _rowKey:  `atype_${entity}_${accType}`,
      _rowType: 'acctype',
      _label:   accType,
      ...sumAllPl(atPos),

      // 三级：按账户分组；账户展开后子行全部铺平（无需再次点击）
      children: Object.entries(groupBy(atPos, 'foldersCode')).map(([acct, acctPos]) => {
        const acctMeta = FOLDER_META.value[acct] || {}

        // 账户下的扁平子行：金融工具小计 → 资产标的 → 曲线/交易明细
        const flat = []
        Object.entries(groupBy(acctPos, 'instrument')).forEach(([instr, instrPos]) => {
          // 金融工具汇总行（无 children，不可展开）
          flat.push({
            _rowKey:  `instr_${acct}_${instr}`,
            _rowType: 'instrument',
            _label:   (PRODUCT_META.value[instr] || { zhName: instr }).zhName,
            ...sumAllPl(instrPos),
          })
          // 资产标的行 + 曲线/期限明细行（账户展开后全部铺平，不含交易动作行）
          instrPos.forEach(p => {
            flat.push({
              _rowKey: `asset_${p.assetId}`, _rowType: 'asset',
              _label: p.assetId, _sublabel: p.underlying,
              initialPl: p.initialPl, modelPl: p.modelPl, timePl: p.timePl,
              spotPl: p.spotPl, yieldCurvePl: p.yieldCurvePl, basisCurvePl: p.basisCurvePl,
              volPl: p.volPl, fixingPl: p.fixingPl, conversionPl: p.conversionPl,
              newDealPl: p.newDealPl, modifyPl: p.modifyPl, cancelPl: p.cancelPl,
              othersPl: p.othersPl,
              cashPl: p.cashPl, cashConvPl: p.cashConvPl,
              mvPl: p.mvPl, mvConvPl: p.mvConvPl,
              totalPl:     parseFloat(((p.mvPl || 0) + (p.cashPl || 0)).toFixed(2)),
              totalConvPl: parseFloat(((p.mvConvPl || 0) + (p.cashConvPl || 0)).toFixed(2)),
            })
            // 曲线/期限明细行（只保留 curve 类型，deal 类型不展示）
            // 每个期限节点的 MV 贡献 = 该节点的因子 PL，按报告货币折算后填入 MV/总损益列
            ;(DETAIL_ROWS[p.assetId] || [])
              .filter(d => d._rowType === 'curve')
              .forEach(d => {
                const curvePl = d.yieldCurvePl ?? d.basisCurvePl ?? null
                const curveConv = curvePl != null
                  ? convertToReport(curvePl, p.posCurrency, rptCcy)
                  : null
                flat.push({
                  ...d,
                  mvPl:     curvePl,
                  mvConvPl: curveConv,
                })
              })
          })
        })

        return {
          _rowKey:      `acct_${acct}`,
          _rowType:     'account',
          _label:       acct,
          _sublabel:    acctMeta.accountName || acct,
          // 损益货币取头寸实际货币（同一账户下头寸货币一致）
          _plCurrency:  acctPos[0]?.posCurrency || acctMeta.plCurrency || '—',
          ...sumAllPl(acctPos),
          children:     flat,
        }
      }),
    })),
  }))
})

// ── 表格合计行 ────────────────────────────────────────────────────────────────
const grandTotal = computed(() =>
  tableRows.value.reduce((s, r) => s + (r.mvConvPl || 0), 0)
)

const PL_FIELDS = [
  'modelPl','timePl','spotPl','yieldCurvePl','basisCurvePl',
  'volPl','fixingPl','conversionPl','newDealPl','modifyPl','cancelPl','othersPl',
  'mvPl','mvConvPl',
]

function getSummary({ columns }) {
  return columns.map(col => {
    if (!col.property) return ''
    if (col.property === '_label') return t('pnlAttribution.grandTotalRow')
    if (PL_FIELDS.includes(col.property)) {
      const sum = parseFloat(tableRows.value.reduce((s, r) => s + (r[col.property] || 0), 0).toFixed(2))
      if (sum === 0) return ''
      return sum < 0 ? `(${fmtVal(Math.abs(sum))})` : fmtVal(sum)
    }
    return ''
  })
}

// ── 导出：将树形行展平为二维数组（含层级缩进前缀）────────────────────────────
function flattenRows(rows, depth = 0) {
  const result = []
  for (const row of rows) {
    // 层级缩进用全角空格表达（Excel 中可见）
    const indent = '　'.repeat(depth)
    let label = indent + (row._label || '')
    if (row._sublabel) label += '  ' + row._sublabel
    if (row._rowType === 'deal') {
      label = indent + t(`pnlAttribution.${row.dealTypeKey}`) + ' · ' + (row._label || '')
    }

    const numOrDash = v => (v == null ? '' : v)

    result.push({
      _label:       label,
      _plCurrency:  row._plCurrency || '',
      modelPl:      numOrDash(row.modelPl),
      timePl:       numOrDash(row.timePl),
      spotPl:       numOrDash(row.spotPl),
      yieldCurvePl: numOrDash(row.yieldCurvePl),
      basisCurvePl: numOrDash(row.basisCurvePl),
      volPl:        numOrDash(row.volPl),
      fixingPl:     numOrDash(row.fixingPl),
      conversionPl: numOrDash(row.conversionPl),
      newDealPl:    numOrDash(row.newDealPl),
      modifyPl:     numOrDash(row.modifyPl),
      cancelPl:     numOrDash(row.cancelPl),
      othersPl:     numOrDash(row.othersPl),
      mvPl:         numOrDash(row.mvPl),
      mvConvPl:     numOrDash(row.mvConvPl),
    })

    if (row.children && row.children.length) {
      result.push(...flattenRows(row.children, depth + 1))
    }
  }
  return result
}

function exportTable() {
  const rptCcy = currency.value || 'USD'

  // ── 表头第一行：列分组（合并单元格） ──────────────────────────────────────
  // 列索引（0-based）：
  //  0  归因维度
  //  1  初始化 / Model Assign.
  //  2  时间衰减 / Time Decay
  //  3-6  市场数据 / FX Spot, Yield Curves, Basis Curves, FX Vol/Smiles
  //  7  定盘价 / Fixings
  //  8  折算 / Spot PL Conv.
  //  9-12 交易活动 / New Deal, Modify Deal, Cancel Deal, Others
  //  13-15 PL 结果（P&L Currency, MV PL, MV Conv PL）
  const groupRow = [
    t('pnlAttribution.dimHeader'),   // 0
    t('pnlAttribution.groupInit'),   // 1  → span 1
    t('pnlAttribution.groupTime'),   // 2  → span 1
    t('pnlAttribution.groupMarket'), // 3  → span 4
    '', '', '',                      // 4-6
    t('pnlAttribution.groupFixing'), // 7  → span 1
    t('pnlAttribution.groupConv'),   // 8  → span 1
    t('pnlAttribution.groupTrade'),  // 9  → span 4
    '', '', '',                      // 10-12
    t('pnlAttribution.groupResult'), // 13 → span 3
    '', '',                          // 14-15
  ]

  // ── 表头第二行：字段名 ────────────────────────────────────────────────────
  const fieldRow = [
    t('pnlAttribution.dimHeader'),
    'Model Assign.',
    'Time Decay',
    'FX Spot',
    'Yield Curves',
    'Basis Curves',
    'FX Vol/Smiles',
    'Fixings',
    'Spot PL Conv.',
    t('pnlAttribution.newDeal'),
    t('pnlAttribution.modifyDeal'),
    t('pnlAttribution.cancelDeal'),
    'Others',
    t('pnlAttribution.plCurrencyCol'),
    t('pnlAttribution.mvPlCol'),
    `${t('pnlAttribution.mvConvPlCol')} (${rptCcy})`,
  ]

  // ── 展平数据行 ────────────────────────────────────────────────────────────
  const flat = flattenRows(tableRows.value)

  // ── 合计行 ────────────────────────────────────────────────────────────────
  const sumRow = flat.reduce((acc, r) => {
    ;[
      'modelPl','timePl','spotPl','yieldCurvePl','basisCurvePl','volPl',
      'fixingPl','conversionPl','newDealPl','modifyPl','cancelPl','othersPl',
      'mvPl','mvConvPl',
    ].forEach(f => { if (typeof r[f] === 'number') acc[f] = (acc[f] || 0) + r[f] })
    return acc
  }, { _label: t('pnlAttribution.grandTotalRow'), _plCurrency: '' })

  // ── 组装 worksheet 数据（aoa = array of arrays）───────────────────────────
  const FIELDS = [
    '_label','modelPl','timePl','spotPl','yieldCurvePl','basisCurvePl','volPl',
    'fixingPl','conversionPl','newDealPl','modifyPl','cancelPl','othersPl',
    '_plCurrency','mvPl','mvConvPl',
  ]

  const aoa = [
    groupRow,
    fieldRow,
    ...flat.map(r => FIELDS.map(f => r[f] ?? '')),
    FIELDS.map(f => sumRow[f] ?? ''),
  ]

  // ── 创建 workbook / worksheet ────────────────────────────────────────────
  const ws = XLSX.utils.aoa_to_sheet(aoa)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, t('pnlAttribution.reportTitle').slice(0, 31))

  // ── 合并单元格（列分组表头）────────────────────────────────────────────────
  ws['!merges'] = [
    // 归因维度：两行合并
    { s: { r: 0, c: 0  }, e: { r: 1, c: 0  } },
    // 初始化（1列）
    { s: { r: 0, c: 1  }, e: { r: 0, c: 1  } },
    // 时间衰减（1列）
    { s: { r: 0, c: 2  }, e: { r: 0, c: 2  } },
    // 市场数据（4列）
    { s: { r: 0, c: 3  }, e: { r: 0, c: 6  } },
    // 定盘价（1列）
    { s: { r: 0, c: 7  }, e: { r: 0, c: 7  } },
    // 折算（1列）
    { s: { r: 0, c: 8  }, e: { r: 0, c: 8  } },
    // 交易活动（4列）
    { s: { r: 0, c: 9  }, e: { r: 0, c: 12 } },
    // PL 结果（3列）
    { s: { r: 0, c: 13 }, e: { r: 0, c: 15 } },
  ]

  // ── 列宽 ──────────────────────────────────────────────────────────────────
  ws['!cols'] = [
    { wch: 36 }, // 归因维度
    { wch: 14 }, // Model Assign.
    { wch: 12 }, // Time Decay
    { wch: 12 }, // FX Spot
    { wch: 14 }, // Yield Curves
    { wch: 14 }, // Basis Curves
    { wch: 14 }, // FX Vol/Smiles
    { wch: 12 }, // Fixings
    { wch: 14 }, // Spot PL Conv.
    { wch: 12 }, // New Deal
    { wch: 12 }, // Modify Deal
    { wch: 12 }, // Cancel Deal
    { wch: 10 }, // Others
    { wch: 10 }, // P&L Currency
    { wch: 12 }, // MV PL
    { wch: 16 }, // MV Conv PL
  ]

  // ── 触发下载 ──────────────────────────────────────────────────────────────
  const filename = `归因分析报告_${scenarioName.value}_${new Date().toISOString().slice(0,10)}.xlsx`
  XLSX.writeFile(wb, filename)

  ElMessage.success(t('pnlAttribution.exportSuccess'))
}

// ── 表格单元格工具 ────────────────────────────────────────────────────────────
function cellVal(row, field) {
  const v = row[field]
  if (v == null) return '—'
  if (v < 0) return `(${fmtVal(Math.abs(v))})`
  return fmtVal(v)
}

function cellClass(row, field) {
  const v = row[field]
  return {
    'cell-val': true,
    'cell-val-bold': row._rowType === 'entity' || row._rowType === 'acctype',
    'cell-val-dim':  row._rowType === 'curve'  || row._rowType === 'deal',
    'val-neg': v != null && v < 0,
  }
}

// ── 因子占比工具函数 ──────────────────────────────────────────────────────────
// 基准：该行 mvPl（头寸货币）；因子与 mvPl 同货币，占比在货币内自洽
// 上层汇总行（entity/acctype）的 mvPl 为各头寸数值加总，可能混货币，仅作方向参考
function cellPct(row, field) {
  const v = row[field]
  const base = Math.abs(row.mvPl ?? 0)
  if (v == null || base === 0) return null
  return parseFloat(((v / base) * 100).toFixed(1))
}

function pctText(row, field) {
  const p = cellPct(row, field)
  if (p == null) return null
  return (p > 0 ? '+' : '') + p + '%'
}

function pctBadgeClass(row, field) {
  const v = row[field]
  if (v == null) return ''
  return v >= 0 ? 'pct-badge pct-pos' : 'pct-badge pct-neg'
}

// ── badge 颜色映射 ────────────────────────────────────────────────────────────
const BADGE_COLORS = {
  'Initial State': '#6b7c9e',
  'Initialization': '#7c5cba',
  'Time Decay':    '#4a7ede',
  'Market Data':   '#36c9a0',
  'Historical':    '#f0a500',
  'Conversion':    '#909399',
  'Trade Activity':'#f56c6c',
}

function badgeColor(badge) {
  return BADGE_COLORS[badge] || '#909399'
}

// ── 仪表盘：汇总数据 ─────────────────────────────────────────────────────────
const SUMMARY_ITEMS = computed(() => [
  { id: 'time',   name: t('pnlAttribution.groupTime'),   value: 350.20, color: '#4a7ede', pct: 28.00 },
  { id: 'market', name: t('pnlAttribution.groupMarket'), value: 680.30, color: '#36c9a0', pct: 54.40 },
  { id: 'trade',  name: t('pnlAttribution.groupTrade'),  value: 220.00, color: '#f56c6c', pct: 17.60 },
])

// ── 仪表盘：产品面板条目 ──────────────────────────────────────────────────────
const productItems = computed(() => buildProductItems(['FX Spot', 'FX Forward']))

// ── 仪表盘：面板配置 ─────────────────────────────────────────────────────────
const PANELS_CFG = computed(() => [
  { key: 'summary',   staticLabel: t('pnlAttribution.dashSummary'), items: SUMMARY_ITEMS.value },
  {
    key: 'factor', dynamicLabel: true,
    itemsMap: {
      time:   [
        { id: 'time_val', name: 'Time',              value: 350.20, color: '#4a7ede', pct: 33.60 },
        { id: 'accrual',  name: 'Accrual',           value: 692.21, color: '#36c9a0', pct: 66.40 },
      ],
      market: [
        { id: 'yield',   name: 'Yield curves',       value: 450.00, color: '#36c9a0', pct: 66.15 },
        { id: 'basis',   name: 'Basis curves',       value: 230.30, color: '#4a7ede', pct: 33.85 },
      ],
      trade:  [
        { id: 'mktops', name: 'Market Operations',   value: 220.00, color: '#f56c6c', pct: 100.00 },
      ],
    },
  },
  { key: 'product',   staticLabel: t('pnlAttribution.dashProduct'),   items: productItems.value },
  {
    key: 'portfolio', staticLabel: t('pnlAttribution.dashPortfolio'),
    items: [
      { id: 'finmkt', name: 'Financial Mkt Dept', value: 562.73, color: '#4a7ede', pct: 45.00 },
      { id: 'pa',     name: 'Portfolio A',         value: 437.68, color: '#36c9a0', pct: 35.00 },
      { id: 'pb',     name: 'Portfolio B',         value: 250.09, color: '#f56c6c', pct: 20.00 },
    ],
  },
  {
    key: 'asset',     staticLabel: t('pnlAttribution.dashAsset'),
    items: [
      { id: 'ccs001', name: 'CCS-001', value: 650.00, color: '#4a7ede', pct: 52.00 },
      { id: 'ccs002', name: 'CCS-002', value: 600.50, color: '#36c9a0', pct: 48.00 },
    ],
  },
])

// ── 仪表盘：状态 ─────────────────────────────────────────────────────────────
const expandedDepth = ref(0)
const selections    = ref([null, null, null, null, null])

// ── 工具 ─────────────────────────────────────────────────────────────────────
function getPanelItems(pi) {
  const cfg = PANELS_CFG.value[pi]
  if (cfg.dynamicLabel) {
    const sel = selections.value[pi - 1] || 'time'
    return cfg.itemsMap[sel] || cfg.itemsMap['time']
  }
  return cfg.items
}

function getPanelLabel(pi) {
  const cfg = PANELS_CFG.value[pi]
  if (cfg.dynamicLabel) {
    const sel  = selections.value[pi - 1]
    const prev = getPanelItems(pi - 1)
    return prev.find(i => i.id === sel)?.name || t('pnlAttribution.dashDetail')
  }
  return cfg.staticLabel
}

function fmtVal(v) {
  if (v == null) return '—'
  return v.toLocaleString('en', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

// ── 仪表盘：计算属性 ─────────────────────────────────────────────────────────
const visiblePanels = computed(() => {
  const depth = Math.min(expandedDepth.value, 4)
  return Array.from({ length: depth + 1 }, (_, i) => ({
    key: PANELS_CFG.value[i].key,
    label: getPanelLabel(i),
    items: getPanelItems(i),
  }))
})

const breadcrumbTail = computed(() => {
  const tail = []
  for (let i = 1; i <= Math.min(expandedDepth.value, 4); i++) {
    tail.push(getPanelLabel(i))
  }
  if (expandedDepth.value >= 5) tail.push(t('pnlAttribution.dashAsset'))
  return tail
})

// ── 仪表盘：交互 ─────────────────────────────────────────────────────────────
function selectItem(pi, item) {
  const sels = [...selections.value]
  sels[pi] = item.id
  for (let i = pi + 1; i < 5; i++) sels[i] = null
  selections.value = sels
  expandedDepth.value = pi + 1
}

function collapseToDepth(depth) {
  expandedDepth.value = depth
}

// ── 仪表盘：图表数据 ─────────────────────────────────────────────────────────
const activeChartItems = computed(() => {
  const depth = Math.min(expandedDepth.value, 4)
  const cfg   = PANELS_CFG.value[depth]
  if (cfg.dynamicLabel) {
    const sel = selections.value[depth - 1] || 'time'
    return cfg.itemsMap[sel] || cfg.itemsMap['time']
  }
  return cfg.items
})

const chartTotal = computed(() =>
  activeChartItems.value.reduce((s, item) => s + item.value, 0)
)

const chartTitle = computed(() => {
  const depth = Math.min(expandedDepth.value, 4)
  return getPanelLabel(depth) + ' ' + t('pnlAttribution.distributionLabel')
})

const R = 70
const C = 2 * Math.PI * R

const chartSegments = computed(() => {
  const items = activeChartItems.value
  const total = chartTotal.value
  let acc = 0
  return items.map(item => {
    const len = (item.value / total) * C
    const seg = {
      ...item,
      dasharray: `${len.toFixed(3)} ${(C - len).toFixed(3)}`,
      dashoffset: (C / 4 - acc).toFixed(3),
    }
    acc += len
    return seg
  })
})

// ── 加载情景数据 ─────────────────────────────────────────────────────────────
onMounted(async () => {
  const id = route.query.id
  if (!id) return
  try {
    const scenario = await getScenario(id)
    scenarioName.value     = scenario.name
    portfolio.value        = scenario.portfolio
    currency.value         = scenario.currency
    const rcs              = scenario.ruleConditions || []
    productItems.value     = buildProductItems(rcs)
    scenarioProducts.value = rcs
  } catch {
    ElMessage.error(t('pnlAttribution.loadError'))
  }
})
</script>

<style lang="scss" scoped>
.attribution-report {
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* ── 情景信息栏 ── */
.ar-infobar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border: 1px solid var(--git-border);
  border-radius: 4px;
  padding: 10px 20px;
  margin-top: 12px;
  flex-shrink: 0;
}

.info-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.scenario-avatar {
  width: 34px; height: 34px;
  border-radius: 50%;
  background: var(--git-primary);
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.scenario-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--git-text-1);
}

.scenario-meta {
  font-size: 12px;
  color: var(--git-text-3);
  margin-top: 2px;
}

.info-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.filter-lbl {
  font-size: 12px;
  color: var(--git-text-2);
  white-space: nowrap;
}

/* ── 视图切换 ── */
.view-toggle {
  display: flex;
  border: 1px solid var(--git-border);
  border-radius: 4px;
  overflow: hidden;
}

.vt-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 12px;
  font-size: 12px;
  color: var(--git-text-2);
  background: #fff;
  border: none;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  line-height: 1.6;

  .el-icon { font-size: 13px; }

  &:first-child { border-right: 1px solid var(--git-border); }

  &:hover { background: #f4f6f8; }

  &.active {
    background: var(--git-primary);
    color: #fff;
  }
}

/* ════════════════════════════════════════════════ */
/* 表格视图                                          */
/* ════════════════════════════════════════════════ */
.ar-table-view {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  background: #fff;
  border: 1px solid var(--git-border);
  border-radius: 4px;
  margin-top: 12px;
  padding: 10px 16px 0;
  overflow: auto;
}

.table-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
  flex-shrink: 0;
}

.table-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--git-text-1);
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.total-hint {
  font-size: 13px;
  color: var(--git-text-2);

  strong {
    color: var(--git-text-1);
    font-size: 15px;
  }
}

/* ── 全局：单元格禁止折行（对齐 TradeQuery 风格）── */
:deep(.el-table .cell) {
  white-space: nowrap;
}

/* ── 固定左列：展开箭头与标签强制同行 ── */
:deep(.col-label .cell) {
  display: flex !important;
  align-items: center !important;
  flex-wrap: nowrap !important;
  gap: 2px;
  overflow: hidden;
  white-space: nowrap;
}

/* ── 列分组表头颜色（:deep 穿透 scoped）── */
:deep(.col-group-init .cell)   { color: #7c5cba; font-weight: 600; }
:deep(.col-group-time .cell)   { color: #4a7ede; font-weight: 600; }
:deep(.col-group-mkt .cell)    { color: #36c9a0; font-weight: 600; }
:deep(.col-group-fixing .cell) { color: #f0a500; font-weight: 600; }
:deep(.col-group-conv .cell)   { color: #909399; font-weight: 600; }
:deep(.col-group-trade .cell)  { color: #f56c6c; font-weight: 600; }
:deep(.col-group-result .cell) { color: var(--git-text-1); font-weight: 600; }
:deep(.col-group-total .cell)  { color: var(--git-text-1); font-weight: 700; background: #f0f4ff; }

/* ── 左列行标签（六层层级）── */
.lbl-entity {
  font-size: 13px;
  font-weight: 700;
  color: var(--git-text-1);
}

.lbl-acctype {
  font-size: 13px;
  font-weight: 600;
  color: var(--git-text-1);
}

.lbl-account {
  font-size: 12px;
  font-weight: 500;
  color: var(--git-text-1);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.lbl-account-sub {
  font-size: 11px;
  color: var(--git-text-3);
  font-weight: 400;
  margin-left: 6px;
}

.lbl-instrument {
  font-size: 12px;
  color: var(--git-text-1);
  font-weight: 500;
  /* 金融工具作为账户内的分组小标题，不额外缩进 */
}

.lbl-asset {
  font-size: 12px;
  color: var(--git-text-2);
  padding-left: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.lbl-asset-sub {
  font-size: 11px;
  color: var(--git-text-3);
  margin-left: 5px;
}

.lbl-detail {
  font-size: 11px;
  color: var(--git-text-3);
  padding-left: 28px;   /* 曲线/交易明细：二级缩进 */
}

/* ── 损益货币标签 ── */
.ccy-tag {
  font-size: 11px;
  font-weight: 600;
  color: var(--git-text-3);
  letter-spacing: 0.03em;
}

/* ── 因子单元格（占比模式）── */
.factor-cell {
  display: inline-flex;
  align-items: center;
  justify-content: flex-end;
  gap: 5px;
  width: 100%;
}

/* 贡献占比徽标 */
.pct-badge {
  display: inline-block;
  font-size: 10px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  padding: 1px 4px;
  border-radius: 3px;
  white-space: nowrap;
  flex-shrink: 0;

  &.pct-pos {
    color: #1a7f5a;
    background: #e6f9f2;
  }

  &.pct-neg {
    color: #c0392b;
    background: #fdedec;
  }
}

/* ── 数值单元格 ── */
.cell-val {
  font-size: 12px;
  font-variant-numeric: tabular-nums;
  color: var(--git-text-1);

  &.val-neg {
    display: inline-block;
    color: #c0392b;
    background: #fff0ef;
    border-radius: 3px;
    padding: 0 3px;
  }

  &.cell-val-bold   { font-weight: 600; }
  &.cell-val-dim    { opacity: 0.7; }
  &.cell-val-result { font-weight: 700; }
}

/* ════════════════════════════════════════════════ */
/* 仪表盘视图                                        */
/* ════════════════════════════════════════════════ */

/* ── 面包屑 ── */
.ar-breadcrumb {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 2px;
  font-size: 12px;
  flex-shrink: 0;
}

.crumb {
  display: flex;
  align-items: center;
  gap: 3px;
  color: var(--git-text-3);
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 3px;
  transition: color 0.15s;

  &:hover { color: var(--git-primary); }

  &-home {
    color: var(--git-text-2);
    font-weight: 500;
  }

  &-active {
    color: #fff;
    background: var(--git-primary);
    font-weight: 600;
    cursor: default;
    &:hover { color: #fff; }
  }
}

.crumb-sep {
  color: var(--git-text-3);
  font-size: 14px;
  line-height: 1;
}

/* ── 横向面板滚动区 ── */
.ar-panels-scroll {
  flex: 1;
  min-height: 0;
  overflow-x: auto;
  overflow-y: hidden;
}

.ar-panels-row {
  display: flex;
  height: 100%;
  gap: 0;
}

/* ── 单个数据面板 ── */
.ar-panel {
  width: 260px;
  flex-shrink: 0;
  border: 1px solid var(--git-border);
  border-right: none;
  background: #fff;
  display: flex;
  flex-direction: column;

  &:first-child { border-radius: 4px 0 0 4px; }
}

.panel-hd {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 14px;
  border-bottom: 1px solid var(--git-border);
  flex-shrink: 0;
}

.panel-icon {
  font-size: 14px;
  color: var(--git-primary);
}

.panel-title {
  flex: 1;
  font-size: 13px;
  font-weight: 600;
  color: var(--git-text-1);
}

.panel-count {
  font-size: 11px;
  color: var(--git-text-3);
  background: #f4f6f8;
  padding: 1px 6px;
  border-radius: 10px;
}

.panel-body {
  flex: 1;
  overflow-y: auto;
}

.panel-item {
  padding: 10px 14px;
  cursor: pointer;
  border-bottom: 1px solid #f4f6f8;
  transition: background 0.12s;

  &:hover { background: #f8f9fb; }

  &.active {
    background: #eaf1ff;
    border-left: 3px solid var(--git-primary);
    padding-left: 11px;
  }
}

.pi-row {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 3px;
}

.pi-name {
  flex: 1;
  font-size: 12px;
  font-weight: 500;
  color: var(--git-text-1);
}

.pi-val {
  font-size: 13px;
  font-weight: 600;
  color: var(--git-text-1);
}

.pi-arrow {
  font-size: 12px;
  color: var(--git-primary);
  flex-shrink: 0;
}

.pi-pct {
  font-size: 11px;
  color: var(--git-text-3);
  margin-bottom: 5px;
}

.pi-bar-track {
  height: 3px;
  background: #e8edf2;
  border-radius: 2px;
  overflow: hidden;
}

.pi-bar-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s;
}

.panel-ft {
  padding: 8px 14px;
  border-top: 1px solid var(--git-border);
  font-size: 12px;
  color: var(--git-text-2);
  flex-shrink: 0;
  background: #fafbfc;

  strong { color: var(--git-text-1); }
}

/* ── 图表面板 ── */
.ar-chart-panel {
  width: 300px;
  flex-shrink: 0;
  border: 1px solid var(--git-border);
  border-radius: 4px;
  margin-left: 8px;
  background: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px 20px;
  overflow-y: auto;
}

.cp-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--git-text-1);
  align-self: flex-start;
  margin-bottom: 12px;
}

.cp-total-lbl {
  font-size: 11px;
  color: var(--git-text-3);
  margin-bottom: 2px;
}

.cp-total-val {
  font-size: 20px;
  font-weight: 700;
  color: var(--git-text-1);
  margin-bottom: 16px;
}

.cp-donut-wrap {
  width: 160px;
  height: 160px;
  margin-bottom: 20px;
}

.cp-donut { width: 100%; height: 100%; }

.cp-legend {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.leg-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.leg-dot {
  width: 9px; height: 9px;
  border-radius: 50%;
  flex-shrink: 0;
}

.leg-name {
  flex: 1;
  font-size: 12px;
  color: var(--git-text-2);
}

.leg-nums {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 1px;
}

.leg-val {
  font-size: 12px;
  font-weight: 600;
  color: var(--git-text-1);
}

.leg-pct {
  font-size: 11px;
  color: var(--git-text-3);
}
</style>
