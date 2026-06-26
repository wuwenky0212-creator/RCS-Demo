<template>
  <div class="threshold-exception-page">

    <!-- ① Filter Bar -->
    <div class="filter-bar">
      <div class="filter-fields">
        <div class="filter-item">
          <label class="filter-label">{{ t('thresholdException.externalNo') }}</label>
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
          <label class="filter-label">{{ t('thresholdException.postingDate') }} <span class="req">*</span></label>
          <el-date-picker
            v-model="filters.dateRange"
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
        <el-button type="primary" size="default" @click="handleQuery">{{ t('common.query') }}</el-button>
        <el-button size="default" @click="handleReset">{{ t('common.reset') }}</el-button>
      </div>
    </div>

    <!-- ② 数据表格区 -->
    <div class="table-card">
      <div class="table-header">
        <span class="table-title">{{ t('thresholdException.title') }}</span>
        <el-button size="small" type="primary" plain :icon="Download" @click="handleExport">
          {{ t('thresholdException.export') }}
        </el-button>
      </div>

      <el-table
        :data="queriedData"
        border
        stripe
        size="small"
        style="width:100%"
        :header-cell-style="{ background:'#f5f7fa', color:'#606266', fontWeight:'600', fontSize:'13px' }"
        :empty-text="t('thresholdException.emptyText')"
        :default-sort="{ prop: 'postingDate', order: 'descending' }"
      >
        <el-table-column prop="excessAmount" :label="t('thresholdException.excessAmount')" width="150" align="right">
          <template #default="{ row }">
            <span class="excess-amt">{{ formatAmount(row.excessAmount) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="externalNo" :label="t('thresholdException.externalNo')" width="200" />
        <el-table-column prop="postingDate" :label="t('thresholdException.postingDate')" width="130" align="center" sortable />
        <el-table-column :label="t('thresholdException.currentAmount')" width="150" align="right">
          <template #default="{ row }">{{ formatAmount(row.currentAmount) }}</template>
        </el-table-column>
        <el-table-column :label="t('thresholdException.previousAmount')" width="150" align="right">
          <template #default="{ row }">{{ formatAmount(row.previousAmount) }}</template>
        </el-table-column>
        <el-table-column prop="currency" :label="t('thresholdException.currency')" width="90" align="center" />
        <el-table-column :label="t('thresholdException.thresholdAmount')" width="140" align="right">
          <template #default="{ row }">{{ formatAmount(row.thresholdAmount) }}</template>
        </el-table-column>
      </el-table>

      <!-- 分页（演示性，导出不受分页限制） -->
      <div class="pagination-bar">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :total="queriedData.length"
          :page-sizes="[10, 20, 50]"
          layout="total, prev, pager, next, sizes, jumper"
          background
          small
        />
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { Search, Download } from '@element-plus/icons-vue'
import * as XLSX from 'xlsx'

const { t } = useI18n()

// ─── 默认日期范围：当前日期前 90 天 ~ 当前日期 ───────────────
function toYMD(d) {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}
function defaultDateRange() {
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - 90)
  return [toYMD(start), toYMD(end)]
}

// ─── Filter state ───────────────────────────────────────────
const filters = reactive({
  externalNo: '',
  dateRange: defaultDateRange(),
})

// ─── Mock Data — 后线晚批超阈值异常表 ─────────────────────────
// 背景：后线系统晚批对 FXSPOT/FXFWD/FXSWAP 等产品执行估值(VOL)/计提(INT)/摊销(AMT)
//       入账处理，按产品维度配置的阈值参数比对，超出阈值的记录写入超阈值异常表。
const rawData = ref([
  {
    externalNo:      'TR-FXFWD-20260620-1187',
    postingDate:     '2026-06-20',
    currentAmount:   128650.32,
    previousAmount:  95200.10,
    currency:        'USD',
    thresholdAmount: 20000.00,
    excessAmount:    13450.22,
  },
  {
    externalNo:      'TR-FXSWAP-20260615-0942',
    postingDate:     '2026-06-15',
    currentAmount:   -86200.55,
    previousAmount:  -40300.18,
    currency:        'CNY',
    thresholdAmount: 30000.00,
    excessAmount:    15900.37,
  },
  {
    externalNo:      'TR-FXSPOT-20260610-3361',
    postingDate:     '2026-06-10',
    currentAmount:   542300.00,
    previousAmount:  498650.00,
    currency:        'EUR',
    thresholdAmount: 25000.00,
    excessAmount:    18650.00,
  },
  {
    externalNo:      'TR-FXFWD-20260528-7705',
    postingDate:     '2026-05-28',
    currentAmount:   33980.44,
    previousAmount:  12100.09,
    currency:        'USD',
    thresholdAmount: 15000.00,
    excessAmount:    6880.35,
  },
  {
    externalNo:      'TR-FXSWAP-20260502-2290',
    postingDate:     '2026-05-02',
    currentAmount:   -15820.00,
    previousAmount:  -2100.00,
    currency:        'CNY',
    thresholdAmount: 10000.00,
    excessAmount:    3720.00,
  },
])

function filterRaw() {
  return rawData.value.filter(row => {
    if (filters.externalNo && row.externalNo !== filters.externalNo) return false
    if (Array.isArray(filters.dateRange) && filters.dateRange.length === 2) {
      const [start, end] = filters.dateRange
      if (start && row.postingDate < start) return false
      if (end && row.postingDate > end) return false
    }
    return true
  })
}

// ─── 查询结果（页面进入时自动带入默认条件展示） ───────────────
const queriedData = ref(filterRaw())

function handleQuery() {
  if (!Array.isArray(filters.dateRange) || filters.dateRange.length !== 2 || !filters.dateRange[0] || !filters.dateRange[1]) {
    ElMessage.error(t('thresholdException.dateRequiredError'))
    return
  }
  if (filters.dateRange[0] > filters.dateRange[1]) {
    ElMessage.error(t('thresholdException.dateRangeInvalid'))
    return
  }
  queriedData.value = filterRaw()
  page.value = 1
  ElMessage.success(t('thresholdException.querySuccess'))
}

function handleReset() {
  filters.externalNo = ''
  filters.dateRange = defaultDateRange()
}

// ─── 分页（演示性展示，导出按当前查询结果全量导出） ────────────
const page = ref(1)
const pageSize = ref(20)

// ─── Helpers ────────────────────────────────────────────────
function formatAmount(val) {
  if (val === null || val === undefined) return '—'
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

// ─── 导出 Excel：当前查询条件下的全部结果，不受分页限制 ────────
function handleExport() {
  const headers = [
    t('thresholdException.excessAmount'),
    t('thresholdException.externalNo'),
    t('thresholdException.postingDate'),
    t('thresholdException.currentAmount'),
    t('thresholdException.previousAmount'),
    t('thresholdException.currency'),
    t('thresholdException.thresholdAmount'),
  ]
  const rows = queriedData.value.map(r => [
    r.excessAmount, r.externalNo, r.postingDate, r.currentAmount, r.previousAmount, r.currency, r.thresholdAmount,
  ])
  const aoa = [headers, ...rows]
  const ws = XLSX.utils.aoa_to_sheet(aoa)
  ws['!cols'] = [{ wch: 14 }, { wch: 24 }, { wch: 12 }, { wch: 16 }, { wch: 16 }, { wch: 8 }, { wch: 14 }]
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, t('thresholdException.title').slice(0, 31))

  const today = new Date()
  const ymd = `${today.getFullYear()}${String(today.getMonth() + 1).padStart(2, '0')}${String(today.getDate()).padStart(2, '0')}`
  XLSX.writeFile(wb, `阈值异常查询_${ymd}.xlsx`)

  ElMessage.success(t('thresholdException.exportSuccess'))
}
</script>

<style lang="scss" scoped>
.threshold-exception-page {
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

  .req { color: var(--git-danger); margin-left: 2px; }
}

.filter-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
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
}

:deep(.el-table) {
  flex: 1;
  font-size: 13px;
}

:deep(.el-table .cell) {
  white-space: nowrap;
}

.excess-amt {
  color: var(--git-danger);
  font-weight: 600;
}

/* ─── Pagination ─── */
.pagination-bar {
  display: flex;
  justify-content: flex-end;
  padding: 10px 16px;
  border-top: 1px solid var(--git-border);
}
</style>
