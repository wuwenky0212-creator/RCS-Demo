<template>
  <div class="tr-page">

    <!-- ── 筛选栏 ── -->
    <div class="tr-filter">
      <div class="tr-filter-row">

        <div class="tr-filter-item">
          <span class="tr-filter-label">{{ t('transferRecords.filterDate') }}</span>
          <el-date-picker
            v-model="filter.dateRange"
            type="daterange"
            value-format="YYYY-MM-DD"
            :range-separator="t('transferRecords.rangeSep')"
            :start-placeholder="t('transferRecords.dateFrom')"
            :end-placeholder="t('transferRecords.dateTo')"
            size="small"
            style="width: 240px"
          />
        </div>

        <div class="tr-filter-item">
          <span class="tr-filter-label">{{ t('transferRecords.filterSymbol') }}</span>
          <el-select v-model="filter.symbol" :placeholder="t('transferRecords.filterAll')" clearable size="small" style="width: 130px">
            <el-option v-for="s in symbolOptions" :key="s" :label="s" :value="s" />
          </el-select>
        </div>

        <div class="tr-filter-item">
          <span class="tr-filter-label">{{ t('transferRecords.filterFrom') }}</span>
          <el-select v-model="filter.fromAccount" :placeholder="t('transferRecords.filterAll')" clearable size="small" style="width: 160px">
            <el-option label="HO Beijing - FX Prop" value="A001" />
            <el-option label="HO Beijing - Market Making" value="A002" />
            <el-option label="HO Shanghai - FX Prop" value="A003" />
            <el-option label="BR Guangzhou - FX Prop" value="A004" />
          </el-select>
        </div>

        <div class="tr-filter-item">
          <span class="tr-filter-label">{{ t('transferRecords.filterTo') }}</span>
          <el-select v-model="filter.toAccount" :placeholder="t('transferRecords.filterAll')" clearable size="small" style="width: 160px">
            <el-option label="HO Beijing - FX Prop" value="A001" />
            <el-option label="HO Beijing - Market Making" value="A002" />
            <el-option label="HO Shanghai - FX Prop" value="A003" />
            <el-option label="BR Guangzhou - FX Prop" value="A004" />
          </el-select>
        </div>

        <div class="tr-filter-actions">
          <el-button type="primary" size="small" @click="handleQuery">
            <el-icon><Search /></el-icon>{{ t('transferRecords.btnQuery') }}
          </el-button>
          <el-button size="small" @click="handleReset">{{ t('transferRecords.btnReset') }}</el-button>
        </div>

      </div>
    </div>

    <!-- ── 表格区 ── -->
    <div class="tr-body">

      <div class="tr-table-hd">
        <span class="tr-table-title">{{ t('transferRecords.tableTitle') }}</span>
        <span class="tr-table-count">{{ t('transferRecords.totalCount', { n: filteredData.length }) }}</span>
      </div>

      <el-table
        :data="filteredData"
        size="small"
        border
        class="tr-table"
        :header-cell-style="{ background: '#f5f7fa', color: '#606266', fontWeight: '600', fontSize: '12px' }"
      >
        <el-table-column prop="transferNo" :label="t('transferRecords.colTransferNo')" width="160" fixed="left" />
        <el-table-column prop="symbol"     :label="t('transferRecords.colSymbol')"     width="90"  align="center" />
        <el-table-column prop="direction"  :label="t('transferRecords.colDirection')"  width="80"  align="center">
          <template #default="{ row }">
            <el-tag :type="row.direction === 'BUY' ? 'success' : 'danger'" size="small" effect="plain">
              {{ row.direction === 'BUY' ? t('transferRecords.dirReceiveShort') : t('transferRecords.dirPayShort') }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="ccy1"       :label="t('transferRecords.colCcy1')"       width="68"  align="center" />
        <el-table-column prop="amount1"    :label="t('transferRecords.colAmount1')"    width="130" align="right">
          <template #default="{ row }">{{ fmtNum(row.amount1) }}</template>
        </el-table-column>
        <el-table-column prop="spotRate"   :label="t('transferRecords.colSpotRate')"   width="110" align="right" />
        <el-table-column prop="ccy2"       :label="t('transferRecords.colCcy2')"       width="68"  align="center" />
        <el-table-column prop="amount2"    :label="t('transferRecords.colAmount2')"    width="140" align="right">
          <template #default="{ row }">
            <span :class="numClass(row.amount2)">{{ fmtNum(row.amount2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="fromAccount" :label="t('transferRecords.colFromAccount')" width="160" />
        <el-table-column prop="toAccount"   :label="t('transferRecords.colToAccount')"   width="160" />
        <el-table-column prop="tradeDate"   :label="t('transferRecords.colTradeDate')"   width="100" align="center" />
        <el-table-column prop="valueDate"   :label="t('transferRecords.colValueDate')"   width="100" align="center" />
        <el-table-column prop="tradeNature" :label="t('transferRecords.colTradeNature')" width="90"  align="center" />
        <el-table-column :label="t('transferRecords.colActions')" width="110" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="openDetail(row)">{{ t('transferRecords.btnDetail') }}</el-button>
            <el-divider direction="vertical" />
            <el-button
              type="danger" link size="small"
              :disabled="row.status !== 'pending'"
              @click="handleCancel(row)"
            >{{ t('transferRecords.btnCancel') }}</el-button>
          </template>
        </el-table-column>
      </el-table>

    </div>

    <!-- ── 详情抽屉 ── -->
    <el-drawer
      v-model="detailVisible"
      :title="t('transferRecords.drawerTitle')"
      direction="rtl"
      size="520px"
      class="detail-drawer"
    >
      <template #header>
        <div class="dd-header">
          <span class="dd-title">{{ t('transferRecords.detailTitle') }}</span>
        </div>
      </template>

      <div v-if="detailRow" class="dd-body">

        <div class="dd-section">
          <div class="dd-section-title"><span class="td-bar"></span>{{ t('transferRecords.sectionTradeInfo') }}</div>
          <div class="dd-fields">
            <div class="dd-row"><div class="dd-label">{{ t('transferRecords.labelTransferNo') }}</div><div class="dd-val">{{ detailRow.transferNo }}</div></div>
            <div class="dd-row"><div class="dd-label">{{ t('transferRecords.labelSymbol') }}</div><div class="dd-val">{{ detailRow.symbol }}</div></div>
            <div class="dd-row"><div class="dd-label">{{ t('transferRecords.labelDirection') }}</div>
              <div class="dd-val">
                <el-tag :type="detailRow.direction === 'BUY' ? 'success' : 'danger'" size="small" effect="plain">
                  {{ detailRow.direction === 'BUY' ? t('transferRecords.dirReceive') : t('transferRecords.dirPay') }}
                </el-tag>
              </div>
            </div>
            <div class="dd-row"><div class="dd-label">{{ t('transferRecords.labelAmount1', { ccy: detailRow.ccy1 }) }}</div><div class="dd-val">{{ fmtNum(detailRow.amount1) }}</div></div>
            <div class="dd-row"><div class="dd-label">{{ t('transferRecords.labelSpotRate') }}</div><div class="dd-val">{{ detailRow.spotRate }}</div></div>
            <div class="dd-row"><div class="dd-label">{{ t('transferRecords.labelAmount1', { ccy: detailRow.ccy2 }) }}</div><div class="dd-val">{{ fmtNum(detailRow.amount2) }}</div></div>
            <div class="dd-row"><div class="dd-label">{{ t('transferRecords.labelTradeDate') }}</div><div class="dd-val">{{ detailRow.tradeDate }}</div></div>
            <div class="dd-row"><div class="dd-label">{{ t('transferRecords.labelValueDate') }}</div><div class="dd-val">{{ detailRow.valueDate }}</div></div>
          </div>
        </div>

        <div class="dd-section">
          <div class="dd-section-title"><span class="td-bar"></span>{{ t('transferRecords.sectionAccountInfo') }}</div>
          <div class="dd-fields">
            <div class="dd-row"><div class="dd-label">{{ t('transferRecords.labelFromAccount') }}</div><div class="dd-val">{{ detailRow.fromAccount }}</div></div>
            <div class="dd-row"><div class="dd-label">{{ t('transferRecords.labelToAccount') }}</div><div class="dd-val">{{ detailRow.toAccount }}</div></div>
          </div>
        </div>

        <div class="dd-section">
          <div class="dd-section-title"><span class="td-bar"></span>{{ t('transferRecords.sectionOtherInfo') }}</div>
          <div class="dd-fields">
            <div class="dd-row"><div class="dd-label">{{ t('transferRecords.labelTradeNature') }}</div><div class="dd-val">{{ detailRow.tradeNature }}</div></div>
            <div class="dd-row"><div class="dd-label">{{ t('transferRecords.labelExternalNo') }}</div><div class="dd-val">{{ detailRow.externalNo || '—' }}</div></div>
            <div class="dd-row"><div class="dd-label">{{ t('transferRecords.labelRemark') }}</div><div class="dd-val">{{ detailRow.remark || '—' }}</div></div>
            <div class="dd-row"><div class="dd-label">{{ t('transferRecords.labelCreatedAt') }}</div><div class="dd-val">{{ detailRow.createdAt }}</div></div>
          </div>
        </div>

      </div>
    </el-drawer>

  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const { t } = useI18n()

// ── 筛选条件 ──────────────────────────────────────────────────────────────────
const filter = reactive({
  dateRange:   [],
  symbol:      '',
  fromAccount: '',
  toAccount:   '',
})

const symbolOptions = ['EURAUD', 'EURCNY', 'EURUSD', 'JPYCNY', 'USDCNY', 'USDJPY']

function handleQuery() { /* 实际场景：调接口 */ }
function handleReset() {
  Object.assign(filter, { dateRange: [], symbol: '', fromAccount: '', toAccount: '', status: '' })
}

// ── Mock 数据 ────────────────────────────────────────────────────────────────
const allData = ref([
  {
    transferNo: 'TRF-20260519-0001', symbol: 'USDCNY', direction: 'SELL',
    ccy1: 'USD', amount1: 5000000,   spotRate: '7.0411',
    ccy2: 'CNY', amount2: -35205500,
    fromAccount: 'HO Beijing - FX Prop', toAccount: 'HO Shanghai - FX Prop',
    tradeDate: '2026-05-19', valueDate: '2026-05-21',
    tradeNature: 'Internal', externalNo: '', remark: 'End-of-day position transfer',
    status: 'done', createdAt: '2026-05-19 09:32:15',
  },
  {
    transferNo: 'TRF-20260519-0002', symbol: 'EURUSD', direction: 'BUY',
    ccy1: 'EUR', amount1: 2000000,   spotRate: '1.1711',
    ccy2: 'USD', amount2: -2342200,
    fromAccount: 'HO Beijing - Market Making', toAccount: 'HO Beijing - FX Prop',
    tradeDate: '2026-05-19', valueDate: '2026-05-21',
    tradeNature: 'Internal', externalNo: 'EXT-88231', remark: '',
    status: 'pending', createdAt: '2026-05-19 10:15:44',
  },
  {
    transferNo: 'TRF-20260518-0003', symbol: 'USDJPY', direction: 'SELL',
    ccy1: 'USD', amount1: 1000000,   spotRate: '157.75',
    ccy2: 'JPY', amount2: -157750000,
    fromAccount: 'HO Shanghai - FX Prop', toAccount: 'BR Guangzhou - FX Prop',
    tradeDate: '2026-05-18', valueDate: '2026-05-20',
    tradeNature: 'Internal', externalNo: '', remark: 'Guangzhou branch top-up',
    status: 'done', createdAt: '2026-05-18 14:08:30',
  },
  {
    transferNo: 'TRF-20260518-0004', symbol: 'EURCNY', direction: 'BUY',
    ccy1: 'EUR', amount1: 500000,    spotRate: '8.2451',
    ccy2: 'CNY', amount2: -4122550,
    fromAccount: 'HO Beijing - FX Prop', toAccount: 'HO Beijing - Market Making',
    tradeDate: '2026-05-18', valueDate: '2026-05-20',
    tradeNature: 'Internal', externalNo: '', remark: '',
    status: 'cancelled', createdAt: '2026-05-18 16:22:09',
  },
  {
    transferNo: 'TRF-20260517-0005', symbol: 'USDCNY', direction: 'BUY',
    ccy1: 'USD', amount1: 3000000,   spotRate: '7.0411',
    ccy2: 'CNY', amount2: -21123300,
    fromAccount: 'BR Guangzhou - FX Prop', toAccount: 'HO Beijing - FX Prop',
    tradeDate: '2026-05-17', valueDate: '2026-05-19',
    tradeNature: 'Internal', externalNo: 'EXT-88100', remark: 'Month-end position consolidation',
    status: 'done', createdAt: '2026-05-17 11:45:52',
  },
])

// 前端筛选
const filteredData = computed(() => {
  return allData.value.filter(r => {
    if (filter.symbol      && r.symbol !== filter.symbol) return false
    if (filter.fromAccount && !r.fromAccount.includes(accountLabel(filter.fromAccount))) return false
    if (filter.toAccount   && !r.toAccount.includes(accountLabel(filter.toAccount)))   return false
    if (filter.status      && r.status !== filter.status) return false
    if (filter.dateRange?.length === 2) {
      if (r.tradeDate < filter.dateRange[0] || r.tradeDate > filter.dateRange[1]) return false
    }
    return true
  })
})

const accountMap = { A001: '外汇自营', A002: '做市账户', A003: '外汇自营', A004: '外汇自营' }
function accountLabel(v) { return accountMap[v] || '' }

// ── 工具函数 ──────────────────────────────────────────────────────────────────
function fmtNum(val) {
  if (val === null || val === undefined) return '—'
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
function numClass(val) {
  return Number(val) < 0 ? 'num-neg' : ''
}
function statusType(s) {
  return { pending: 'warning', done: 'success', cancelled: 'info' }[s] ?? ''
}
function statusLabel(s) {
  const map = {
    pending:   t('transferRecords.statusPending'),
    done:      t('transferRecords.statusDone'),
    cancelled: t('transferRecords.statusCancelled'),
  }
  return map[s] ?? s
}

// ── 详情抽屉 ──────────────────────────────────────────────────────────────────
const detailVisible = ref(false)
const detailRow     = ref(null)

function openDetail(row) {
  detailRow.value   = row
  detailVisible.value = true
}

// ── 撤销 ──────────────────────────────────────────────────────────────────────
function handleCancel(row) {
  ElMessageBox.confirm(
    t('transferRecords.cancelConfirmMsg', { no: row.transferNo }),
    t('transferRecords.cancelConfirmTitle'),
    { confirmButtonText: t('transferRecords.cancelConfirmBtn'), cancelButtonText: t('common.cancel'), type: 'warning' }
  ).then(() => {
    row.status = 'cancelled'
    ElMessage.success(t('transferRecords.cancelSuccess'))
  }).catch(() => {})
}
</script>

<style lang="scss" scoped>
.tr-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #fff;
}

/* ── 筛选栏 ── */
.tr-filter {
  padding: 14px 20px 12px;
  border-bottom: 1px solid var(--git-border);
  flex-shrink: 0;
}
.tr-filter-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}
.tr-filter-item {
  display: flex;
  align-items: center;
  gap: 6px;
}
.tr-filter-label {
  font-size: 13px;
  color: var(--git-text-2);
  white-space: nowrap;
}
.tr-filter-actions {
  display: flex;
  gap: 8px;
  margin-left: 4px;
}

/* ── 表格区 ── */
.tr-body {
  flex: 1;
  overflow: auto;
  padding: 16px 20px;
}
.tr-table-hd {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}
.tr-table-title {
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
.tr-table-count {
  font-size: 12px;
  color: var(--git-text-3);
}
.tr-table {
  :deep(.el-table__cell) { padding: 5px 0; }
  :deep(.el-table__body-wrapper) { font-size: 13px; }
}
.num-neg { color: #f56c6c; }

/* ── 详情抽屉 ── */
:deep(.detail-drawer) {
  .el-drawer__header {
    padding: 14px 20px;
    margin-bottom: 0;
    border-bottom: 1px solid var(--git-border);
  }
  .el-drawer__body { padding: 0; overflow-y: auto; }
}

.dd-header {
  display: flex;
  align-items: center;
  gap: 10px;
}
.dd-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--git-text-1);
}
.dd-body {
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.dd-section {}
.dd-section-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: var(--git-text-1);
  margin-bottom: 8px;
}
.td-bar {
  display: inline-block;
  width: 3px;
  height: 13px;
  background: var(--git-primary);
  border-radius: 2px;
  flex-shrink: 0;
}
.dd-fields {
  border: 1px solid #e4e8f0;
  border-radius: 4px;
  overflow: hidden;
}
.dd-row {
  display: flex;
  align-items: stretch;
  min-height: 34px;
  border-bottom: 1px solid #edf0f7;
  &:last-child { border-bottom: none; }
}
.dd-label {
  width: 96px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  padding: 6px 10px;
  font-size: 12px;
  color: var(--git-text-2);
  background: #f8f9fc;
  border-right: 1px solid #edf0f7;
  white-space: nowrap;
}
.dd-val {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 6px 12px;
  font-size: 13px;
  color: var(--git-text-1);
  background: #fff;
  word-break: break-all;
}
</style>
