<template>
  <div class="spot-fx-page">

    <!-- ── 顶部 Tab ── -->
    <div class="sfx-tabs">
      <div v-for="tab in tabs" :key="tab.key" class="sfx-tab"
        :class="{ active: activeTab === tab.key }" @click="activeTab = tab.key">
        {{ tab.label }}
      </div>
    </div>

    <!-- ── 筛选栏 ── -->
    <div class="sfx-filter">
      <span class="sfx-filter-label">{{ t('spotPosition.account') }}</span>
      <el-select v-model="filterAccount" size="small" style="width: 220px">
        <el-option
          v-for="book in BOOKS"
          :key="book.code"
          :label="isEn ? `${book.code} (${book.nameEn || book.name})` : `${book.code}（${book.name}）`"
          :value="book.code"
        />
      </el-select>
      <el-button type="primary" size="small" @click="handleQuery">{{ t('spotPosition.query') }}</el-button>
      <el-button size="small" @click="handleReset">{{ t('spotPosition.reset') }}</el-button>
    </div>

    <!-- ── 内容区 ── -->
    <div class="sfx-body">
      <div class="sfx-section">
        <div class="sfx-section-hd">
          <span class="sfx-section-title">{{ t('spotPosition.sectionTitle') }}</span>
          <div class="sfx-auto-refresh">
            <el-switch v-model="autoRefresh" size="small" @change="onAutoRefreshChange" />
            <span class="sfx-ar-label">{{ t('spotPosition.autoRefresh') }}</span>
            <el-icon class="sfx-ar-setting"><Setting /></el-icon>
          </div>
        </div>

        <el-table :data="spotFxData" size="small" border class="sfx-table"
          :header-cell-style="{ background: '#f5f7fa', color: '#606266', fontWeight: '600', fontSize: '12px' }">
          <el-table-column prop="symbol"      :label="t('spotPosition.colSymbol')"          width="88"  fixed="left" />
          <el-table-column prop="ccy1"        :label="t('spotPosition.colCcy1')"            width="68"  align="center" />
          <el-table-column prop="exposure1"   :label="t('spotPosition.colExposure1')"       width="130" align="right">
            <template #default="{ row }"><span :class="numClass(row.exposure1)">{{ fmtNum(row.exposure1) }}</span></template>
          </el-table-column>
          <el-table-column prop="ccy2"        :label="t('spotPosition.colCcy2')"            width="68"  align="center" />
          <el-table-column prop="exposure2"   :label="t('spotPosition.colExposure2')"       width="150" align="right">
            <template #default="{ row }"><span :class="numClass(row.exposure2)">{{ fmtNum(row.exposure2) }}</span></template>
          </el-table-column>
          <el-table-column prop="costExposure" :label="t('spotPosition.colCostExposure')"  width="150" align="right">
            <template #default="{ row }"><span :class="numClass(row.costExposure)">{{ fmtNum(row.costExposure) }}</span></template>
          </el-table-column>
          <el-table-column prop="marketRate"  :label="t('spotPosition.colMarketRate')"      width="110" align="right" />
          <el-table-column prop="breakeven"   :label="t('spotPosition.colBreakeven')"       width="110" align="right" />
          <el-table-column prop="costPrice"   :label="t('spotPosition.colCostPrice')"       width="110" align="right" />
          <el-table-column prop="floatPnl"    :label="t('spotPosition.colFloatPnl')"        width="110" align="right">
            <template #default="{ row }"><span :class="numClass(row.floatPnl)">{{ fmtNum(row.floatPnl) }}</span></template>
          </el-table-column>
          <el-table-column prop="pnlCcy"      :label="t('spotPosition.colPnlCcy')"          width="76"  align="center" />
          <el-table-column prop="totalPnl"    :label="t('spotPosition.colTotalPnl')"        width="160" align="right">
            <template #default="{ row }"><span :class="numClass(row.totalPnl)">{{ fmtNum(row.totalPnl) }}</span></template>
          </el-table-column>
          <el-table-column prop="dailyRealizedPnl" :label="t('spotPosition.colDailyRealizedPnl')" width="200" align="right">
            <template #default="{ row }"><span :class="numClass(row.dailyRealizedPnl)">{{ fmtNum(row.dailyRealizedPnl) }}</span></template>
          </el-table-column>
          <el-table-column prop="realizedPnl" :label="t('spotPosition.colRealizedPnl')"    width="190" align="right">
            <template #default="{ row }"><span :class="numClass(row.realizedPnl)">{{ fmtNum(row.realizedPnl) }}</span></template>
          </el-table-column>
          <el-table-column prop="dailyPnl"    :label="t('spotPosition.colDailyPnl')"        width="165" align="right">
            <template #default="{ row }"><span :class="numClass(row.dailyPnl)">{{ fmtNum(row.dailyPnl) }}</span></template>
          </el-table-column>
          <el-table-column prop="monthlyPnl"  :label="t('spotPosition.colMonthlyPnl')"      width="165" align="right">
            <template #default="{ row }"><span :class="numClass(row.monthlyPnl)">{{ fmtNum(row.monthlyPnl) }}</span></template>
          </el-table-column>
          <el-table-column prop="yearlyPnl"   :label="t('spotPosition.colYearlyPnl')"       width="165" align="right">
            <template #default="{ row }"><span :class="numClass(row.yearlyPnl)">{{ fmtNum(row.yearlyPnl) }}</span></template>
          </el-table-column>
          <el-table-column :label="t('spotPosition.colActions')" width="140" align="center" fixed="right">
            <template #default="{ row }">
              <span style="white-space: nowrap; display: inline-flex; align-items: center; gap: 0;">
                <el-button type="primary" link size="small" style="white-space: nowrap">{{ t('spotPosition.btnDetail') }}</el-button>
                <el-divider direction="vertical" />
                <el-button type="primary" link size="small" style="white-space: nowrap" @click="openTransfer(row)">{{ t('spotPosition.btnTransfer') }}</el-button>
              </span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════════════════
         转移抽屉
    ══════════════════════════════════════════════════════════════════════ -->
    <el-drawer
      v-model="drawerVisible"
      :title="t('spotPosition.drawerTitle')"
      direction="rtl"
      size="560px"
      :close-on-click-modal="false"
      class="transfer-drawer"
      @close="resetTransferForm"
    >
      <!-- 抽屉头部 slot：标题 + 操作图标 -->
      <template #header>
        <div class="td-header">
          <span class="td-title">{{ t('spotPosition.drawerTitle') }}</span>
          <div class="td-header-tags">
            <el-tag size="small" type="info" effect="plain">{{ t('spotPosition.tagInternal') }}</el-tag>
            <el-tag v-if="transferRow" size="small" effect="plain">{{ transferRow.symbol }}</el-tag>
          </div>
        </div>
      </template>

      <!-- 抽屉主体：左表单 + 右分析面板 -->
      <div class="td-body">

        <!-- ── 左侧：表单 ── -->
        <div class="td-form-panel">
          <div class="td-form-scroll">

            <!-- ① 交易信息 -->
            <div class="td-section">
              <div class="td-section-title">
                <span class="td-bar"></span>{{ t('spotPosition.sectionTradeInfo') }}
              </div>
              <div class="td-fields">

                <!-- Currency Pair -->
                <div class="td-row">
                  <div class="td-label">{{ t('spotPosition.fieldCurrencyPair') }} <span class="req">*</span></div>
                  <div class="td-value">
                    <el-input :value="tf.currencyPair" disabled size="small" style="width:100%" />
                  </div>
                </div>

                <!-- Amount: BUY / SELL dual input -->
                <div class="td-row td-row--tall">
                  <div class="td-label">{{ t('spotPosition.fieldAmount', { ccy1: tf.ccy1, ccy2: tf.ccy2 }) }} <span class="req">*</span></div>
                  <div class="td-value td-value--buysell">
                    <div class="bs-half">
                      <span class="bs-tag bs-tag--buy">BUY</span>
                      <span class="bs-arrow">⇌</span>
                      <el-input
                        v-model="tf.amount1"
                        size="small"
                        :placeholder="t('spotPosition.placeholderInput')"
                        class="bs-input"
                        @blur="calcFromBuy"
                      />
                    </div>
                    <div class="bs-sep"></div>
                    <div class="bs-half">
                      <span class="bs-tag bs-tag--sell">SELL</span>
                      <span class="bs-arrow">⇌</span>
                      <el-input
                        v-model="tf.amount2"
                        size="small"
                        :placeholder="t('spotPosition.placeholderInput')"
                        class="bs-input"
                        @blur="calcFromSell"
                      />
                    </div>
                  </div>
                </div>

                <!-- Spot Rate -->
                <div class="td-row">
                  <div class="td-label">{{ t('spotPosition.fieldSpotRate') }} <span class="req">*</span></div>
                  <div class="td-value">
                    <el-input v-model="tf.spotRate" size="small" :placeholder="t('spotPosition.placeholderInput')" style="width:100%"
                      @blur="calcFromBuy" />
                  </div>
                </div>

                <!-- Trade Date -->
                <div class="td-row">
                  <div class="td-label">{{ t('spotPosition.fieldTradeDate') }} <span class="req">*</span></div>
                  <div class="td-value td-value--split">
                    <el-date-picker v-model="tf.tradeDate" type="date" value-format="YYYY-MM-DD"
                      size="small" style="flex:1" :placeholder="t('spotPosition.placeholderDate')" />
                    <el-time-picker v-model="tf.tradeTime" format="HH:mm:ss" value-format="HH:mm:ss"
                      size="small" style="width:110px" :placeholder="t('spotPosition.placeholderTime')" />
                  </div>
                </div>

                <!-- Value Date -->
                <div class="td-row">
                  <div class="td-label">{{ t('spotPosition.fieldValueDate') }} <span class="req">*</span></div>
                  <div class="td-value">
                    <el-date-picker v-model="tf.valueDate" type="date" value-format="YYYY-MM-DD"
                      size="small" style="width:100%" :placeholder="t('spotPosition.placeholderDate')" />
                  </div>
                </div>

              </div>
            </div>

            <!-- ② 账户信息 -->
            <div class="td-section">
              <div class="td-section-title">
                <span class="td-bar"></span>{{ t('spotPosition.sectionAccountInfo') }}
              </div>
              <div class="td-fields">

                <!-- Account -->
                <div class="td-row">
                  <div class="td-label">{{ t('spotPosition.fieldAccount') }} <span class="req">*</span></div>
                  <div class="td-value td-value--split">
                    <el-select v-model="tf.fromAccount" :placeholder="t('spotPosition.placeholderSelect')" size="small" style="flex:1">
                      <el-option-group
                        v-for="book in BOOKS"
                        :key="book.code"
                        :label="isEn ? `${book.code} (${book.nameEn || book.name})` : `${book.code}（${book.name}）`"
                      >
                        <el-option
                          v-for="p in getPortfoliosByBook(book.code)"
                          :key="p.code"
                          :label="p.code"
                          :value="p.code"
                        />
                      </el-option-group>
                    </el-select>
                    <el-input :value="tf.fromAccountName" :placeholder="t('spotPosition.placeholderAutoFill')"
                      size="small" style="width:120px" disabled />
                  </div>
                </div>

                <!-- Counterparty -->
                <div class="td-row">
                  <div class="td-label">{{ t('spotPosition.fieldCounterparty') }} <span class="req">*</span></div>
                  <div class="td-value td-value--split">
                    <el-select v-model="tf.toAccount" :placeholder="t('spotPosition.placeholderSelect')" size="small" style="flex:1">
                      <el-option-group
                        v-for="book in BOOKS"
                        :key="book.code"
                        :label="isEn ? `${book.code} (${book.nameEn || book.name})` : `${book.code}（${book.name}）`"
                      >
                        <el-option
                          v-for="p in getPortfoliosByBook(book.code)"
                          :key="p.code"
                          :label="p.code"
                          :value="p.code"
                        />
                      </el-option-group>
                    </el-select>
                    <el-input :value="tf.toAccountName" :placeholder="t('spotPosition.placeholderAutoFill')"
                      size="small" style="width:120px" disabled />
                  </div>
                </div>

              </div>
            </div>

            <!-- ③ 备注 -->
            <div class="td-section">
              <div class="td-section-title">
                <span class="td-bar"></span>{{ t('spotPosition.sectionRemarks') }}
              </div>
              <div class="td-fields">

                <div class="td-row">
                  <div class="td-label">{{ t('spotPosition.fieldTradeNature') }}</div>
                  <div class="td-value">
                    <el-select v-model="tf.tradeNature" :placeholder="t('spotPosition.placeholderSelect')" size="small" style="width:100%">
                      <el-option :label="t('spotPosition.optionInternal')" value="internal" />
                      <el-option :label="t('spotPosition.optionInterbank')" value="interbank" />
                    </el-select>
                  </div>
                </div>

                <div class="td-row">
                  <div class="td-label">{{ t('spotPosition.fieldExternalNo') }}</div>
                  <div class="td-value td-value--split">
                    <el-input v-model="tf.externalNo" :placeholder="t('spotPosition.placeholderInput')" size="small" style="flex:1" />
                    <el-select v-model="tf.externalSystem" size="small" style="width:90px">
                      <el-option label="RCS" value="RCS" />
                      <el-option label="SWIFT" value="SWIFT" />
                    </el-select>
                  </div>
                </div>

                <div class="td-row">
                  <div class="td-label">{{ t('spotPosition.fieldPurpose') }}</div>
                  <div class="td-value">
                    <el-input v-model="tf.purpose" :placeholder="t('spotPosition.placeholderInput')" size="small" style="width:100%" />
                  </div>
                </div>

                <div class="td-row">
                  <div class="td-label">{{ t('spotPosition.fieldRemark') }}</div>
                  <div class="td-value">
                    <el-input v-model="tf.remark" type="textarea" :rows="2"
                      :placeholder="t('spotPosition.placeholderInput')" size="small" style="width:100%" />
                  </div>
                </div>

              </div>
            </div>

          </div><!-- /td-form-scroll -->

          <!-- 底部按钮 -->
          <div class="td-footer">
            <el-button size="small" @click="resetTransferForm">
              <el-icon><Delete /></el-icon>{{ t('spotPosition.btnClearAll') }}
            </el-button>
            <el-button type="primary" size="small" @click="handleTransferSubmit">{{ t('spotPosition.btnSubmit') }}</el-button>
          </div>
        </div>

      </div><!-- /td-body -->
    </el-drawer>

  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import {
  Setting, Delete, RefreshRight, ArrowRight,
  DataAnalysis, Money, Warning, CircleCheck, TrendCharts
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { BOOKS, PORTFOLIOS, getPortfoliosByBook } from '@/data/bookStructure.js'

const { t, locale } = useI18n()
const isEn = computed(() => locale.value === 'en-US')

// ── Tabs / 筛选 ──────────────────────────────────────────────────────────────
const tabs = computed(() => [
  { key: 'realtime', label: t('spotPosition.realtimeTab') },
])
const activeTab     = ref('realtime')
const filterAccount = ref('OBIDTFXD')
const autoRefresh   = ref(false)

// ── Mock 数据 ────────────────────────────────────────────────────────────────
const spotFxData = ref([
  { symbol: 'EURAUD', ccy1: 'EUR', exposure1: -1_256_000,      ccy2: 'AUD', exposure2: 2_222_412.00,
    costExposure: 2_218_500.00,  marketRate: '1.770973', breakeven: '1.771165', costPrice: '1.770973',
    floatPnl: -2_340.50, pnlCcy: 'USD', totalPnl: -2_340.50, dailyRealizedPnl: 0.00, realizedPnl: 0.00,
    dailyPnl: -2_340.50, monthlyPnl: -8_920.30, yearlyPnl: -12_450.80 },
  { symbol: 'EURCNY', ccy1: 'EUR', exposure1: 3_450_000,       ccy2: 'CNY', exposure2: -28_445_595.00,
    costExposure: -28_432_440.00, marketRate: '8.245100', breakeven: '8.245838', costPrice: '8.245100',
    floatPnl: -3_200.00, pnlCcy: 'USD', totalPnl: -3_200.00, dailyRealizedPnl: 0.00, realizedPnl: 0.00,
    dailyPnl: -3_200.00, monthlyPnl: -9_500.00, yearlyPnl: -28_500.00 },
  { symbol: 'EURUSD', ccy1: 'EUR', exposure1: 5_248_600,       ccy2: 'USD', exposure2: -6_146_634.60,
    costExposure: -6_133_100.00, marketRate: '1.171100', breakeven: '1.171000', costPrice: '1.171100',
    floatPnl: 52_400.00, pnlCcy: 'USD', totalPnl: 52_400.00, dailyRealizedPnl: 0.00, realizedPnl: 125_643.00,
    dailyPnl: 52_400.00, monthlyPnl: 189_022.00, yearlyPnl: 534_267.00 },
  { symbol: 'JPYCNY', ccy1: 'JPY', exposure1: 200_000_000,     ccy2: 'CNY', exposure2: -8_927_000.00,
    costExposure: -8_927_000.00, marketRate: '4.463500', breakeven: '4.463500', costPrice: '0.044635',
    floatPnl: 0.00, pnlCcy: 'USD', totalPnl: 0.00, dailyRealizedPnl: 0.00, realizedPnl: 0.00,
    dailyPnl: 0.00, monthlyPnl: 0.00, yearlyPnl: 0.00 },
  { symbol: 'USDCNY', ccy1: 'USD', exposure1: 32_497_143,      ccy2: 'CNY', exposure2: -228_862_292.67,
    costExposure: -227_207_413.00, marketRate: '7.041100', breakeven: '7.041100', costPrice: '7.041100',
    floatPnl: -67_167.00, pnlCcy: 'USD', totalPnl: -67_167.00, dailyRealizedPnl: 0.00, realizedPnl: -23_450.00,
    dailyPnl: -67_167.00, monthlyPnl: -182_344.00, yearlyPnl: -451_288.00 },
  { symbol: 'USDJPY', ccy1: 'USD', exposure1: 13_466_000,      ccy2: 'JPY', exposure2: -2_124_697_500.00,
    costExposure: -2_118_450_000.00, marketRate: '157.7500', breakeven: '166.0000', costPrice: '157.7500',
    floatPnl: -78_550.00, pnlCcy: 'USD', totalPnl: -78_550.00, dailyRealizedPnl: 0.00, realizedPnl: -1_230.00,
    dailyPnl: -78_550.00, monthlyPnl: -312_400.00, yearlyPnl: -987_630.00 },
])

// ── 工具函数 ──────────────────────────────────────────────────────────────────
function fmtNum(val) {
  if (val === null || val === undefined || val === '') return '—'
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
function numClass(val) {
  return (val !== null && val !== undefined && Number(val) < 0) ? 'num-neg' : ''
}

let refreshTimer = null
function onAutoRefreshChange(val) {
  clearInterval(refreshTimer)
  if (val) refreshTimer = setInterval(() => {}, 5000)
}
function handleQuery() {}
function handleReset() { filterAccount.value = 'OBIDTFXD' }

// ── 转移抽屉 ──────────────────────────────────────────────────────────────────
const drawerVisible = ref(false)
const transferRow   = ref(null)

// 今日 & 默认起息日（T+2 工作日，简化取 +2 天）
const today    = new Date().toISOString().slice(0, 10)
const valueDt  = (() => { const d = new Date(); d.setDate(d.getDate() + 2); return d.toISOString().slice(0, 10) })()
const nowTime  = new Date().toTimeString().slice(0, 8)

const tf = reactive({
  currencyPair:   '',
  ccy1: '', ccy2: '',
  direction:      'BUY',
  amount1:        '',
  spotRate:       '',
  amount2:        '',
  tradeDate:      today,
  tradeTime:      nowTime,
  valueDate:      valueDt,
  fromAccount:    '',
  fromAccountName:'',
  toAccount:      '',
  toAccountName:  '',
  tradeNature:    'internal',
  externalNo:     '',
  externalSystem: 'RCS',
  purpose:        '',
  remark:         '',
})

// 账户说明自动填入（取自 bookStructure PORTFOLIOS，locale-reactive）
const accountMap = computed(() =>
  Object.fromEntries(PORTFOLIOS.map(p => [p.code, isEn.value ? (p.descriptionEn || p.description) : p.description]))
)
watch(() => tf.fromAccount, v => { tf.fromAccountName = accountMap.value[v] || '' })
watch(() => tf.toAccount,   v => { tf.toAccountName   = accountMap.value[v] || '' })
// Re-fill names when locale changes
watch(isEn, () => {
  tf.fromAccountName = accountMap.value[tf.fromAccount] || ''
  tf.toAccountName   = accountMap.value[tf.toAccount]   || ''
})

// BUY 输入 → 计算 SELL（amount2 = amount1 × spotRate）
function calcFromBuy() {
  const a = parseFloat(tf.amount1)
  const r = parseFloat(tf.spotRate)
  if (!isNaN(a) && !isNaN(r) && r !== 0) {
    tf.amount2 = (a * r).toFixed(2)
  }
}
// SELL 输入 → 反向计算 BUY（amount1 = amount2 / spotRate）
function calcFromSell() {
  const a = parseFloat(tf.amount2)
  const r = parseFloat(tf.spotRate)
  if (!isNaN(a) && !isNaN(r) && r !== 0) {
    tf.amount1 = (a / r).toFixed(2)
  }
}
// 保留旧名以兼容其他调用
function calcAmount2() { calcFromBuy() }

function openTransfer(row) {
  transferRow.value = row
  tf.currencyPair = row.symbol
  tf.ccy1         = row.ccy1
  tf.ccy2         = row.ccy2
  tf.spotRate     = row.marketRate
  // 自动带入当前货币对的敞口金额（取绝对值）
  tf.amount1      = Math.abs(row.exposure1).toFixed(2)
  tf.amount2      = Math.abs(row.exposure2).toFixed(2)
  tf.fromAccount  = ''
  tf.toAccount    = ''
  drawerVisible.value = true
}

function resetTransferForm() {
  Object.assign(tf, {
    amount1: '', spotRate: '', amount2: '',
    tradeDate: today, tradeTime: nowTime, valueDate: valueDt,
    fromAccount: '', fromAccountName: '', toAccount: '', toAccountName: '',
    broker: '', tradeNature: 'internal',
    externalNo: '', externalSystem: 'RCS', purpose: '', remark: '',
  })
}

function handleTransferSubmit() {
  if (!tf.fromAccount || !tf.toAccount) {
    ElMessage.warning(t('spotPosition.errFillAccounts'))
    return
  }
  if (!tf.amount1 || !tf.spotRate) {
    ElMessage.warning(t('spotPosition.errFillAmount'))
    return
  }
  ElMessage.success(t('spotPosition.successSubmit'))
  drawerVisible.value = false
}

// ── 右侧分析面板 ─────────────────────────────────────────────────────────────
const analysisItems = computed(() => [
  { key: 'valuation',    label: t('spotPosition.analysisValuation'),   icon: 'DataAnalysis', open: false },
  { key: 'cashflow',     label: t('spotPosition.analysisCashflow'),    icon: 'Money',        open: false },
  { key: 'op-risk',      label: t('spotPosition.analysisOpRisk'),      icon: 'Warning',      open: false },
  { key: 'credit-risk',  label: t('spotPosition.analysisCreditRisk'),  icon: 'CircleCheck',  open: false },
  { key: 'market-risk',  label: t('spotPosition.analysisMarketRisk'),  icon: 'TrendCharts',  open: false },
])
const analysisOpen = reactive({})
function toggleAnalysis(key) { analysisOpen[key] = !analysisOpen[key] }
</script>

<style lang="scss" scoped>
/* ════════════════════════════════════════════════════════════
   头寸监控页
════════════════════════════════════════════════════════════ */
.spot-fx-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #fff;
}

.sfx-tabs {
  display: flex;
  align-items: flex-end;
  padding: 0 20px;
  border-bottom: 2px solid var(--git-border);
  flex-shrink: 0;
}
.sfx-tab {
  padding: 10px 20px;
  font-size: 14px;
  color: var(--git-text-2);
  cursor: pointer;
  position: relative;
  transition: color 0.15s;
  margin-bottom: -2px;
  &:hover { color: var(--git-primary); }
  &.active {
    color: var(--git-primary);
    font-weight: 600;
    &::after {
      content: '';
      position: absolute;
      left: 0; right: 0; bottom: 0;
      height: 2px;
      background: var(--git-primary);
      border-radius: 1px;
    }
  }
}

.sfx-filter {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  border-bottom: 1px solid var(--git-border);
  flex-shrink: 0;
}
.sfx-filter-label { font-size: 13px; color: var(--git-text-2); white-space: nowrap; }

.sfx-body { flex: 1; overflow: auto; padding: 16px 20px; }
.sfx-section { margin-bottom: 24px; }
.sfx-section-hd {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}
.sfx-section-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--git-text-1);
  position: relative;
  padding-left: 10px;
  &::before {
    content: '';
    position: absolute;
    left: 0; top: 2px; bottom: 2px;
    width: 3px;
    background: var(--git-primary);
    border-radius: 2px;
  }
}
.sfx-auto-refresh { display: flex; align-items: center; gap: 6px; }
.sfx-ar-label { font-size: 12px; color: var(--git-text-2); }
.sfx-ar-setting { font-size: 14px; color: var(--git-text-3); cursor: pointer; &:hover { color: var(--git-primary); } }

.sfx-table {
  :deep(.el-table__cell) { padding: 5px 0; }
  :deep(.el-table__body-wrapper) { font-size: 13px; }
}
.num-neg { color: #f56c6c; }

/* ════════════════════════════════════════════════════════════
   转移抽屉
════════════════════════════════════════════════════════════ */
:deep(.transfer-drawer) {
  .el-drawer__header {
    padding: 14px 20px 14px;
    margin-bottom: 0;
    border-bottom: 1px solid var(--git-border);
  }
  .el-drawer__body {
    padding: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
}

/* 抽屉标题行 */
.td-header {
  display: flex;
  align-items: center;
  gap: 10px;
}
.td-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--git-text-1);
}
.td-header-tags { display: flex; gap: 6px; }

/* 抽屉主体：左右分栏 */
.td-body {
  flex: 1;
  display: flex;
  min-height: 0;
  overflow: hidden;
}

/* ── 左侧表单面板 ── */
.td-form-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  border-right: 1px solid var(--git-border);
}
.td-form-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
}

/* section 块 */
.td-section { margin-bottom: 20px; }
.td-section-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: var(--git-text-1);
  margin-bottom: 8px;
  padding-left: 2px;
}
.td-bar {
  display: inline-block;
  width: 3px;
  height: 13px;
  background: var(--git-primary);
  border-radius: 2px;
  flex-shrink: 0;
}

/* 字段行 */
.td-fields {
  border: 1px solid #e4e8f0;
  border-radius: 4px;
  overflow: hidden;
}
.td-row {
  display: flex;
  align-items: stretch;
  min-height: 36px;
  border-bottom: 1px solid #edf0f7;
  &:last-child { border-bottom: none; }
}
.td-label {
  width: 100px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  padding: 0 10px;
  font-size: 12px;
  color: var(--git-text-2);
  background: #f8f9fc;
  border-right: 1px solid #edf0f7;
  white-space: nowrap;
  .req { color: #f56c6c; margin-left: 2px; }
}
.td-value {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 3px 8px;
  background: #fff;

  &--auto {
    background: #f5f8ff;
    :deep(.el-input.is-disabled .el-input__wrapper) { background: transparent !important; box-shadow: none !important; }
    :deep(.el-input.is-disabled .el-input__inner) {
      color: var(--git-primary) !important;
      -webkit-text-fill-color: var(--git-primary) !important;
      font-weight: 600;
    }
  }
  &--split { gap: 6px; }

  :deep(.el-input__wrapper),
  :deep(.el-select .el-input__wrapper) {
    box-shadow: none !important;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    background: #fff;
    padding: 0 8px;
    transition: border-color 0.2s;
    &:hover { border-color: var(--git-primary); }
  }
  :deep(.el-textarea__inner) {
    box-shadow: none !important;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    resize: none;
  }
  :deep(.el-date-editor .el-input__wrapper) { padding: 0 8px; }
}

/* BUY / SELL 双向金额输入行 */
.td-row--tall { min-height: 44px; }

.td-value--buysell {
  padding: 0;
  gap: 0;
  align-items: stretch;
}

.bs-half {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 4px 8px;
  gap: 6px;
  min-width: 0;
}

.bs-sep {
  width: 1px;
  background: #edf0f7;
  align-self: stretch;
}

.bs-tag {
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
  letter-spacing: 0.5px;
  &--buy  { color: var(--git-primary); }
  &--sell { color: #f56c6c; }
}

.bs-arrow {
  color: var(--git-text-3);
  font-size: 13px;
  flex-shrink: 0;
}

.bs-input {
  flex: 1;
  min-width: 0;
}

/* 底部按钮 */
.td-footer {
  flex-shrink: 0;
  padding: 12px 20px;
  border-top: 1px solid var(--git-border);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  background: #fff;
}

/* ── 右侧分析面板 ── */
.td-analysis-panel {
  width: 260px;
  flex-shrink: 0;
  overflow-y: auto;
  background: #fafbfc;
}

.td-analysis-item {
  border-bottom: 1px solid var(--git-border);
  cursor: pointer;
  &:hover .td-ai-hd { background: #f0f4ff; }
}

.td-ai-hd {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 13px 16px;
  transition: background 0.15s;
}
.td-ai-left {
  display: flex;
  align-items: center;
  gap: 8px;
}
.td-ai-icon {
  font-size: 15px;
  color: var(--git-primary);
}
.td-ai-title {
  font-size: 13px;
  font-weight: 500;
  color: var(--git-text-1);
}
.td-ai-right {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--git-text-3);
  font-size: 14px;
}
.td-ai-refresh:hover { color: var(--git-primary); }
.td-ai-arrow {
  transition: transform 0.2s;
  &.is-open { transform: rotate(90deg); }
}
.td-ai-body {
  padding: 12px 16px;
  border-top: 1px solid #edf0f7;
  background: #fff;
}
.td-ai-empty {
  font-size: 12px;
  color: var(--git-text-3);
}
</style>
