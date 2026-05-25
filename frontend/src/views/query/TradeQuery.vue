<template>
  <div class="trade-query-page">

    <!-- ① Filter Bar -->
    <div class="filter-bar">
      <div class="filter-fields">
        <div class="filter-item">
          <label class="filter-label">{{ t('tradeQuery.externalNo') }}</label>
          <el-input
            v-model="filters.externalNo"
            :placeholder="t('common.pleaseInput')"
            clearable
            size="default"
            style="width:220px"
          >
            <template #prefix><el-icon><Search /></el-icon></template>
          </el-input>
        </div>

        <div class="filter-item">
          <label class="filter-label">{{ t('tradeQuery.tradeStatus') }}</label>
          <el-select
            v-model="filters.tradeStatus"
            :placeholder="t('common.pleaseSelect')"
            clearable
            size="default"
            style="width:160px"
          >
            <el-option :label="t('tradeQuery.statusDone')" value="done" />
            <el-option :label="t('tradeQuery.statusPending')" value="pending" />
            <el-option :label="t('tradeQuery.statusCancelled')" value="cancelled" />
            <el-option :label="t('tradeQuery.statusExpired')" value="expired" />
          </el-select>
        </div>

        <div class="filter-item">
          <label class="filter-label">{{ t('tradeQuery.tradeDate') }}</label>
          <el-date-picker
            v-model="filters.tradeDateRange"
            type="daterange"
            range-separator="—"
            :start-placeholder="t('common.startDate')"
            :end-placeholder="t('common.endDate')"
            value-format="YYYY-MM-DD"
            size="default"
            style="width:260px"
          />
        </div>
      </div>

      <div class="filter-actions">
        <el-button size="default" @click="toggleExpand">
          {{ expanded ? t('common.collapse') : t('common.expand') }}
          <el-icon class="expand-icon" :class="{ rotated: expanded }"><ArrowDown /></el-icon>
        </el-button>
        <el-button type="primary" size="default" @click="handleQuery">{{ t('common.query') }}</el-button>
        <el-button size="default" @click="handleReset">{{ t('common.reset') }}</el-button>
      </div>
    </div>

    <!-- ② 数据表格区 -->
    <div class="table-card">
      <div class="table-header">
        <span class="table-title">{{ t('tradeQuery.title') }}</span>
        <el-icon class="table-setting"><Setting /></el-icon>
      </div>

      <el-table
        :data="tableData"
        border
        stripe
        size="small"
        style="width:100%"
        :header-cell-style="{ background: '#f5f7fa', color: '#606266', fontWeight: '600', fontSize: '13px' }"
      >
        <!-- 左侧冻结：外部流水号 -->
        <el-table-column prop="externalNo" :label="t('tradeQuery.externalNo')" width="160" fixed="left" />

        <!-- 核心业务信息 -->
        <el-table-column prop="tradeDate"    :label="t('tradeQuery.tradeDate')"   width="110" />
        <el-table-column prop="valueDate"    :label="t('tradeQuery.valueDate')"   width="110" />
        <el-table-column :label="t('tradeQuery.account')" width="160">
          <template #default="{ row }">
            <span class="link-text">{{ row.account }}</span>
          </template>
        </el-table-column>
        <el-table-column :label="t('tradeQuery.direction')" width="90" align="center">
          <template #default="{ row }">
            <span :class="row.direction === '卖出' ? 'dir-sell' : 'dir-buy'">{{ directionMap[row.direction] || row.direction }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="instrument"   :label="t('tradeQuery.instrument')"   width="120" />
        <el-table-column :label="t('tradeQuery.amount1')" width="130" align="right">
          <template #default="{ row }">{{ formatAmount(row.amount1) }}</template>
        </el-table-column>
        <el-table-column :label="t('tradeQuery.amount2')" width="130" align="right">
          <template #default="{ row }">{{ formatAmount(row.amount2) }}</template>
        </el-table-column>
        <el-table-column prop="maturityDate" :label="t('tradeQuery.maturityDate')"   width="110" />
        <el-table-column :label="t('tradeQuery.counterparty')" width="200">
          <template #default="{ row }">
            <span class="link-text-orange">{{ row.counterparty }}</span>
          </template>
        </el-table-column>

        <!-- 状态与清算/证实 -->
        <el-table-column :label="t('tradeQuery.tradeStatus')" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="statusType(row.tradeStatus)" size="small">{{ tradeStatusMap[row.tradeStatus] || row.tradeStatus }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column :label="t('tradeQuery.backlineStatus')" width="110" align="center">
          <template #default="{ row }">{{ backlineStatusMap[row.backlineStatus] || row.backlineStatus }}</template>
        </el-table-column>
        <el-table-column :label="t('tradeQuery.clearingMethod')" width="90">
          <template #default="{ row }">{{ clearingMethodMap[row.clearingMethod] || row.clearingMethod }}</template>
        </el-table-column>
        <el-table-column prop="confirmNo"         :label="t('tradeQuery.confirmNo')"       width="180" />
        <el-table-column prop="confirmMethod"     :label="t('tradeQuery.confirmMethod')"       width="120" />
        <el-table-column :label="t('tradeQuery.confirmStatus')" width="90" align="center">
          <template #default="{ row }">{{ confirmStatusMap[row.confirmStatus] || row.confirmStatus }}</template>
        </el-table-column>
        <el-table-column :label="t('tradeQuery.confirmMatchStatus')" width="110" align="center">
          <template #default="{ row }">{{ confirmMatchStatusMap[row.confirmMatchStatus] || row.confirmMatchStatus }}</template>
        </el-table-column>

        <!-- 交易属性与机构 -->
        <el-table-column :label="t('tradeQuery.tradeNature')" width="100">
          <template #default="{ row }">{{ tradeNatureMap[row.tradeNature] || row.tradeNature }}</template>
        </el-table-column>
        <el-table-column prop="tradeNo"         :label="t('tradeQuery.tradeNo')"   width="180" />
        <el-table-column prop="tradeBizNo"      :label="t('tradeQuery.tradeBizNo')" width="180" />
        <el-table-column prop="tradeEntryDate"  :label="t('tradeQuery.tradeEntryDate')"   width="110" />
        <el-table-column :label="t('tradeQuery.channel')" width="100">
          <template #default="{ row }">{{ channelMap[row.channel] || row.channel }}</template>
        </el-table-column>
        <el-table-column :label="t('tradeQuery.tradeSource')" width="90">
          <template #default="{ row }">{{ tradeSourceMap[row.tradeSource] || row.tradeSource }}</template>
        </el-table-column>
        <el-table-column :label="t('tradeQuery.eventType')" width="90">
          <template #default="{ row }">{{ eventTypeMap[row.eventType] || row.eventType }}</template>
        </el-table-column>
        <el-table-column :label="t('tradeQuery.operationOrg')" width="130">
          <template #default="{ row }">{{ operationOrgMap[row.operationOrg] || row.operationOrg }}</template>
        </el-table-column>
        <el-table-column :label="t('tradeQuery.bizOrg')" width="120">
          <template #default="{ row }">{{ bizOrgMap[row.bizOrg] || row.bizOrg }}</template>
        </el-table-column>

        <!-- 产品与人员 -->
        <el-table-column :label="t('tradeQuery.product')" width="100">
          <template #default="{ row }">{{ productMap[row.product] || row.product }}</template>
        </el-table-column>
        <el-table-column :label="t('tradeQuery.financialInstrument')" width="150">
          <template #default="{ row }">{{ financialInstrumentMap[row.financialInstrument] || row.financialInstrument }}</template>
        </el-table-column>
        <el-table-column prop="buyoutType"      :label="t('tradeQuery.buyoutType')"     width="90" />
        <el-table-column prop="trader"          :label="t('tradeQuery.trader')"       width="100" />

        <!-- 右侧冻结：操作 -->
        <el-table-column :label="t('common.actions')" width="80" fixed="right" align="center" class-name="col-ops">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="showDetail(row)">{{ t('common.detail') }}</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-bar">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[20, 50, 100]"
          layout="total, prev, pager, next, sizes, jumper"
          background
          small
        />
      </div>
    </div>

  </div>

  <!-- 详情对话框 -->
  <TradeDetail v-model="detailVisible" :row="currentRow" />

</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { Search, Setting } from '@element-plus/icons-vue'
import TradeDetail from './TradeDetail.vue'

const { t } = useI18n()

// ─── Computed translation maps (reactive to language switch) ─
const directionMap = computed(() => ({
  '买入': t('common.dirBuy'),
  '卖出': t('common.dirSell'),
  '借入': t('common.dirBorrow'),
  '贷出': t('common.dirLend'),
  '借出': t('common.dirLendOut'),
  '收':   t('common.dirReceive'),
  '付':   t('common.dirPay'),
}))

const tradeStatusMap = computed(() => ({
  '已成交': t('tradeQuery.statusDone'),
  '生效':   t('tradeQuery.statusActive'),
  '待确认': t('tradeQuery.statusPending'),
  '已撤销': t('tradeQuery.statusCancelled'),
  '已到期': t('tradeQuery.statusExpired'),
}))

const backlineStatusMap = computed(() => ({
  '已处理': t('tradeQuery.backlineDone'),
  '复核中': t('tradeQuery.backlineReview'),
  '待处理': t('tradeQuery.backlinePending'),
  '处理中': t('tradeQuery.backlineProcessing'),
}))

const confirmStatusMap = computed(() => ({
  '已确认': t('tradeQuery.confirmDone'),
}))

const confirmMatchStatusMap = computed(() => ({
  '已匹配': t('tradeQuery.matchDone'),
  '未匹配': t('tradeQuery.matchNone'),
}))

const tradeNatureMap = computed(() => ({
  '同业交易': t('tradeQuery.tradeNatureInterbank'),
}))

const channelMap = computed(() => ({
  '前台录入': t('tradeQuery.channelFront'),
  'RCS':     t('tradeQuery.channelRCS'),
}))

const tradeSourceMap = computed(() => ({
  '自营': t('tradeQuery.sourcePropriety'),
  '代客': t('tradeQuery.sourceAgency'),
  'RCS':  t('tradeQuery.channelRCS'),
}))

const eventTypeMap = computed(() => ({
  '新增': t('tradeQuery.eventTypeNew'),
  '修改': t('tradeQuery.eventTypeAmend'),
}))

const productMap = computed(() => ({
  '同业拆借': t('tradeQuery.productInterbank'),
  '现券买卖': t('tradeQuery.productSpotBond'),
}))

const financialInstrumentMap = computed(() => ({
  '美元同业拆借': t('tradeQuery.instrumentUsdInterbank'),
  '现券买卖':     t('tradeQuery.productSpotBond'),
}))

const clearingMethodMap = computed(() => ({
  '净额': t('tradeQuery.clearingNet'),
  'DVP':  t('tradeQuery.clearingDVP'),
}))

const operationOrgMap = computed(() => ({
  '总行营业部': t('tradeQuery.orgHeadOfficeBranch'),
}))

const bizOrgMap = computed(() => ({
  '金融市场部': t('tradeQuery.orgFinancialMarkets'),
  'CBHB总行':  t('tradeQuery.orgCBHBHQ'),
}))

// ─── Filter state ───────────────────────────────────────────
const expanded = ref(false)
const filters = reactive({
  externalNo: '26050800003781',
  tradeStatus: '',
  tradeDateRange: ['2025-07-08', '2026-05-08'],
})

function toggleExpand() { expanded.value = !expanded.value }
function handleQuery() { ElMessage.success(t('tradeQuery.querySuccess')) }
function handleReset() {
  filters.externalNo = ''
  filters.tradeStatus = ''
  filters.tradeDateRange = []
}

// ─── Pagination ─────────────────────────────────────────────
const page = ref(1)
const pageSize = ref(20)
const total = ref(2)

// ─── Mock Data — 真实同业拆借交易 ───────────────────────────
// 背景：境内某商业银行（账户 HFZBIFIMN001）向 ZG农业银行 拆出
//       USD 100万，期限 3 个月（2026-05-11 → 2026-08-11），
//       年利率 4.85%，ACT/360，Modified Following。
//       交易已通过 SWIFT MT320 证实并匹配，DVP 清算。
const tableData = ref([
  {
    externalNo:          '26050800003781',
    tradeDate:           '2026-05-08',
    valueDate:           '2026-05-11',
    account:             'HFZBIFIMN001',
    direction:           '卖出',           // 借出 → 外汇方向显示为"卖出"
    instrument:          'USD',
    amount1:             1_000_000.00,     // USD 名义本金
    amount2:             0.00,             // 应计利息（起息日当天为0）
    maturityDate:        '2026-08-11',
    counterparty:        'Agricultural Bank of China (ZG)',
    tradeStatus:         '已成交',
    backlineStatus:      '已处理',
    clearingMethod:      'DVP',
    confirmNo:           'CONF-IB-20260508-001',
    confirmMethod:       'SWIFT MT320',
    confirmStatus:       '已确认',
    confirmMatchStatus:  '已匹配',
    tradeNature:         '同业交易',
    tradeNo:             'TR-IB-20260508-7819',
    tradeBizNo:          'BIZ-IB-2026050801',
    tradeEntryDate:      '2026-05-08',
    channel:             '前台录入',
    tradeSource:         '自营',
    eventType:           '新增',
    operationOrg:        '总行营业部',
    bizOrg:              '金融市场部',
    product:             '同业拆借',
    financialInstrument: '美元同业拆借',
    buyoutType:          '—',
    trader:              'Wang Yifan',
  },
  {
    externalNo:          '26050800003498',
    tradeDate:           '2026-05-08',
    valueDate:           '2026-05-08',
    account:             'shymalCNY01',
    direction:           '买入',
    instrument:          'SHYMAL.IB',
    amount1:             1_000_000.00,
    amount2:             1_008_666.67,
    maturityDate:        '2026-05-08',
    counterparty:        'Agricultural Bank of China (ZG)',
    tradeStatus:         '生效',
    backlineStatus:      '复核中',
    clearingMethod:      '净额',
    confirmNo:           '',
    confirmMethod:       '',
    confirmStatus:       '',
    confirmMatchStatus:  '',
    tradeNature:         '同业交易',
    tradeNo:             '26050800003498',
    tradeBizNo:          '26050800003498',
    tradeEntryDate:      '2026-05-08',
    channel:             'RCS',
    tradeSource:         'RCS',
    eventType:           '新增',
    operationOrg:        'BANKZB',
    bizOrg:              'CBHB总行',
    product:             '现券买卖',
    financialInstrument: '现券买卖',
    buyoutType:          '—',
    trader:              'sh1ZB',
  }
])

// ─── Helpers ────────────────────────────────────────────────
function formatAmount(val) {
  if (val === null || val === undefined) return '—'
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function statusType(s) {
  const map = { '已成交': 'success', '生效': 'success', '待确认': 'warning', '已撤销': 'danger', '已到期': 'info' }
  return map[s] || ''
}

const detailVisible = ref(false)
const currentRow = ref(null)
function showDetail(row) {
  currentRow.value = row
  detailVisible.value = true
}
</script>

<style lang="scss" scoped>
.trade-query-page {
  display: flex;
  flex-direction: column;
  gap: 10px;
  height: 100%;
}

/* ─── Filter Bar ─── */
.filter-bar {
  background: #ffffff;
  border: 1px solid var(--git-border);
  border-radius: 4px;
  padding: 14px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-fields {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
  flex: 1;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 13px;
  color: var(--git-text-2);
  white-space: nowrap;
}

.filter-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;

  .expand-icon {
    margin-left: 2px;
    transition: transform 0.2s;
    &.rotated { transform: rotate(180deg); }
  }
}

/* ─── Table Card ─── */
.table-card {
  flex: 1;
  background: #ffffff;
  border: 1px solid var(--git-border);
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}

.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px 10px;
  border-bottom: 1px solid var(--git-border);

  .table-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--git-text-1);
  }

  .table-setting {
    font-size: 16px;
    color: var(--git-text-3);
    cursor: pointer;
    &:hover { color: var(--git-primary); }
  }
}

/* 表格区域可横向滚动 */
:deep(.el-table) {
  flex: 1;
  font-size: 13px;
}

:deep(.el-table .el-table__body td) {
  color: var(--git-text-1);
}

/* 全局禁止单元格折行 */
:deep(.el-table .cell) {
  white-space: nowrap;
}

.link-text {
  color: var(--git-primary);
  cursor: pointer;
  &:hover { text-decoration: underline; }
}

.link-text-orange {
  color: #e6a23c;
  cursor: pointer;
  &:hover { text-decoration: underline; }
}

.dir-sell { color: #f56c6c; font-weight: 600; }
.dir-buy  { color: #67c23a; font-weight: 600; }

:deep(.col-ops .cell) {
  white-space: nowrap;
  overflow: visible;
}

/* ─── Pagination ─── */
.pagination-bar {
  display: flex;
  justify-content: flex-end;
  padding: 10px 16px;
  border-top: 1px solid var(--git-border);
}
</style>
