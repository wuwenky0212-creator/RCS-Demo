<template>
  <div class="sa-page">

    <!-- 过滤区 -->
    <div class="filter-bar">
      <div class="filter-fields">
        <div class="filter-item">
          <label class="filter-label">{{ t('suspenseAcct.bglAccount') }}</label>
          <el-input
            v-model="filters.bglAccount"
            :placeholder="t('common.pleaseInput')"
            clearable
            size="default"
            style="width:180px"
          >
            <template #prefix><el-icon><Search /></el-icon></template>
          </el-input>
        </div>
        <div class="filter-item">
          <label class="filter-label">{{ t('suspenseAcct.origAccount') }}</label>
          <el-input
            v-model="filters.origAccount"
            :placeholder="t('common.pleaseInput')"
            clearable
            size="default"
            style="width:180px"
          />
        </div>
        <div class="filter-item">
          <label class="filter-label">{{ t('suspenseAcct.suspenseType') }}</label>
          <el-select
            v-model="filters.suspenseType"
            :placeholder="t('common.all')"
            clearable
            size="default"
            style="width:140px"
          >
            <el-option :label="t('suspenseAcct.typeReceivable')" value="应收" />
            <el-option :label="t('suspenseAcct.typePayable')" value="应付" />
          </el-select>
        </div>
        <div class="filter-item">
          <label class="filter-label">{{ t('suspenseAcct.suspenseDate') }}</label>
          <el-date-picker
            v-model="filters.dateRange"
            type="daterange"
            range-separator="—"
            :start-placeholder="t('common.startDate')"
            :end-placeholder="t('common.endDate')"
            value-format="YYYY-MM-DD"
            size="default"
            style="width:250px"
          />
        </div>
      </div>
      <div class="filter-actions">
        <el-button type="primary" size="default" @click="handleQuery">{{ t('common.query') }}</el-button>
        <el-button size="default" @click="handleReset">{{ t('common.reset') }}</el-button>
      </div>
    </div>

    <!-- 主卡片 -->
    <div class="table-card">

      <!-- 状态 Tabs -->
      <div class="status-tabs">
        <div
          v-for="tab in tabs"
          :key="tab.key"
          class="status-tab"
          :class="{ active: activeTab === tab.key }"
          @click="switchTab(tab.key)"
        >
          {{ tab.label }}
          <span v-if="tab.count" class="tab-count" :class="tab.countType">{{ tab.count }}</span>
        </div>
      </div>

      <!-- 操作栏（挂账中可销账） -->
      <div v-if="activeTab === 'pending'" class="action-bar">
        <el-button
          type="primary"
          size="small"
          :disabled="selectedRows.length === 0"
          @click="openWriteOff"
        >{{ t('suspenseAcct.writeOff') }}</el-button>
        <span v-if="selectedRows.length > 0" class="selected-hint">{{ t('suspenseAcct.selectedHint', { n: selectedRows.length }) }}</span>
      </div>

      <!-- 表格 -->
      <el-table
        :data="currentData"
        border
        stripe
        size="small"
        style="width:100%"
        :header-cell-style="{ background:'#f5f7fa', color:'#606266', fontWeight:'600', fontSize:'13px' }"
        @selection-change="val => selectedRows = val"
      >
        <el-table-column v-if="activeTab === 'pending'" type="selection" width="44" fixed="left" />
        <el-table-column prop="seq"          :label="t('suspenseAcct.seq')"     width="60"  align="center" fixed="left" />

        <el-table-column :label="t('suspenseAcct.suspenseType')" width="110" align="center">
          <template #default="{ row }">
            <el-tag type="info" size="small" effect="light">{{ suspenseTypeMap[row.suspenseType] || row.suspenseType }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="bglAccount"   :label="t('suspenseAcct.bglAccount')"    width="140" />
        <el-table-column prop="origAccount"  :label="t('suspenseAcct.origAccount')" width="150" />
        <el-table-column :label="t('suspenseAcct.origAcctFlag')" width="170">
          <template #default="{ row }">{{ acctFlagMap[row.origAcctFlag] || row.origAcctFlag }}</template>
        </el-table-column>

        <el-table-column :label="t('suspenseAcct.status')" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)" size="small" effect="light">{{ statusMap[row.status] || row.status }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="suspenseDate" :label="t('suspenseAcct.suspenseDate')" width="110" />
        <el-table-column prop="suspenseTime" :label="t('suspenseAcct.suspenseTime')" width="90"  align="center" />

        <el-table-column :label="t('suspenseAcct.amount')" width="150" align="right">
          <template #default="{ row }">
            <span class="amount-text">{{ row.currency }} {{ fmtAmt(row.amount) }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="externalNo"   :label="t('suspenseAcct.externalNo')" min-width="190" />

        <el-table-column v-if="activeTab === 'written'" prop="writeOffDate" :label="t('suspenseAcct.writeOffDate')" width="110" />
        <el-table-column v-if="activeTab === 'written'" prop="writeOffBy"   :label="t('suspenseAcct.writeOffBy')" width="110" />

        <el-table-column :label="t('common.actions')" width="100" fixed="right" align="center">
          <template #default="{ row }">
            <template v-if="activeTab === 'pending'">
              <el-button link type="primary" size="small" @click="openWriteOffSingle(row)">{{ t('suspenseAcct.writeOff') }}</el-button>
              <el-divider direction="vertical" />
            </template>
            <el-button link type="primary" size="small">{{ t('common.detail') }}</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-bar">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :total="currentData.length"
          :page-sizes="[20, 50, 100]"
          layout="total, prev, pager, next, sizes, jumper"
          background
          small
        />
      </div>

    </div>
  </div>

  <!-- ── 销账弹窗 ── -->
  <el-dialog
    v-model="writeOffVisible"
    :title="t('suspenseAcct.writeOffDialog')"
    :width="isEn ? '580px' : '520px'"
    :close-on-click-modal="false"
  >
    <div class="wo-body">
      <div :class="['wo-info', { 'wo-info--en': isEn }]">
        <div class="wo-row"><div class="wo-label">{{ t('suspenseAcct.bglAccount') }}</div><div class="wo-val link-text">{{ writeOffTarget?.bglAccount }}</div></div>
        <div class="wo-row"><div class="wo-label">{{ t('suspenseAcct.origAccount') }}</div><div class="wo-val">{{ writeOffTarget?.origAccount }}</div></div>
        <div class="wo-row"><div class="wo-label">{{ t('suspenseAcct.suspenseType') }}</div><div class="wo-val">{{ suspenseTypeMap[writeOffTarget?.suspenseType] || writeOffTarget?.suspenseType }}</div></div>
        <div class="wo-row"><div class="wo-label">{{ t('suspenseAcct.amount') }}</div><div class="wo-val amount-text">{{ writeOffTarget?.currency }} {{ fmtAmt(writeOffTarget?.amount) }}</div></div>
        <div class="wo-row"><div class="wo-label">{{ t('suspenseAcct.suspenseDate') }}</div><div class="wo-val">{{ writeOffTarget?.suspenseDate }}</div></div>
        <div class="wo-row"><div class="wo-label">{{ t('suspenseAcct.externalNo') }}</div><div class="wo-val">{{ writeOffTarget?.externalNo }}</div></div>
      </div>
      <el-form :label-width="isEn ? 'auto' : '90px'" :label-position="isEn ? 'top' : 'right'" style="margin-top:16px">
        <el-form-item :label="t('suspenseAcct.writeOffAcct')" required>
          <el-input v-model="writeOffAccount" :placeholder="t('suspenseAcct.writeOffAcctPlaceholder')" style="width:100%" />
        </el-form-item>
        <el-form-item :label="t('suspenseAcct.writeOffReason')">
          <el-input
            v-model="writeOffReason"
            type="textarea"
            :rows="3"
            :placeholder="t('suspenseAcct.writeOffReasonPlaceholder')"
          />
        </el-form-item>
      </el-form>
    </div>
    <template #footer>
      <el-button @click="writeOffVisible = false">{{ t('common.cancel') }}</el-button>
      <el-button
        type="primary"
        :disabled="!writeOffAccount.trim()"
        :loading="writeOffLoading"
        @click="confirmWriteOff"
      >{{ writeOffLoading ? t('suspenseAcct.processing') : t('suspenseAcct.submitWriteOff') }}</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage, ElNotification } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { Search } from '@element-plus/icons-vue'

const { t, locale } = useI18n()
const isEn = computed(() => locale.value === 'en-US')

// ─── Computed translation maps ───────────────────────────────
const suspenseTypeMap = computed(() => ({
  '应收': t('suspenseAcct.typeReceivable'),
  '应付': t('suspenseAcct.typePayable'),
}))

const statusMap = computed(() => ({
  '挂账中': t('suspenseAcct.statusSuspended'),
  '已销账': t('suspenseAcct.statusWrittenOff'),
}))

const acctFlagMap = computed(() => ({
  'CGL_INTERNAL': t('internalTransfer.acctFlagCgl'),
  'BGL_PENDING':  t('internalTransfer.acctFlagBglPending'),
  'BGL_DEPOSIT':  t('internalTransfer.acctFlagBglDeposit'),
  'BGL_SETTLE':   t('internalTransfer.acctFlagBglSettle'),
  'BGL_INCOME':   t('internalTransfer.acctFlagBglIncome'),
  'NET_NETTING':  t('internalTransfer.acctFlagNet'),
}))

// ─── 过滤 ────────────────────────────────────────────────────
const filters = ref({
  bglAccount:   '',
  origAccount:  '',
  suspenseType: '',
  dateRange:    ['2025-05-08', '2026-05-11'],
})
function handleQuery() { ElMessage.success(t('common.querySuccess')) }
function handleReset() {
  filters.value = { bglAccount: '', origAccount: '', suspenseType: '', dateRange: [] }
}

// ─── Tabs ────────────────────────────────────────────────────
const tabs = computed(() => [
  { key: 'pending', label: t('suspenseAcct.tabPending'), count: 3, countType: 'count-warning' },
  { key: 'written', label: t('suspenseAcct.tabWritten'), count: 1, countType: 'count-success' },
])
const activeTab = ref('pending')
function switchTab(key) {
  activeTab.value = key
  selectedRows.value = []
}

// ─── 分页 ────────────────────────────────────────────────────
const page     = ref(1)
const pageSize = ref(20)

// ─── Mock 数据 ───────────────────────────────────────────────
const pendingData = ref([
  {
    seq:          1,
    suspenseType: '应收',
    bglAccount:   '2199000000',
    origAccount:  'HFZB****N001',
    origAcctFlag: 'CGL_INTERNAL',
    status:       '挂账中',
    suspenseDate: '2026-05-08',
    suspenseTime: '14:32',
    currency:     'USD',
    amount:       1_000_000.00,
    externalNo:   'BANCS-20260508-7819',
  },
  {
    seq:          2,
    suspenseType: '应收',
    bglAccount:   '2199000000',
    origAccount:  'USDCNH****002',
    origAcctFlag: 'CGL_INTERNAL',
    status:       '挂账中',
    suspenseDate: '2026-05-09',
    suspenseTime: '10:15',
    currency:     'EUR',
    amount:       875_000.00,
    externalNo:   'BANCS-20260509-3361',
  },
  {
    seq:          3,
    suspenseType: '应付',
    bglAccount:   '2199000000',
    origAccount:  'CBHB****3820',
    origAcctFlag: 'CGL_INTERNAL',
    status:       '挂账中',
    suspenseDate: '2026-05-09',
    suspenseTime: '13:47',
    currency:     'CNY',
    amount:       -88_560_000.00,
    externalNo:   'BANCS-20260509-7793',
  },
])

const writtenData = ref([
  {
    seq:          1,
    suspenseType: '应付',
    bglAccount:   '2199000000',
    origAccount:  'HFZB****N002',
    origAcctFlag: 'CGL_INTERNAL',
    status:       '已销账',
    suspenseDate: '2026-05-07',
    suspenseTime: '16:44',
    currency:     'USD',
    amount:       320_000.00,
    externalNo:   'BANCS-20260507-6120',
    writeOffDate: '2026-05-09',
    writeOffBy:   'James Zhao',
  },
])

const currentData = computed(() => {
  if (activeTab.value === 'pending') return pendingData.value
  if (activeTab.value === 'written') return writtenData.value
  return []
})

// ─── 多选 ────────────────────────────────────────────────────
const selectedRows = ref([])

// ─── 格式化 ──────────────────────────────────────────────────
function fmtAmt(val) {
  if (val === undefined || val === null) return ''
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
function statusTagType(s) {
  const map = { '挂账中': 'warning', '已销账': 'success' }
  return map[s] || 'info'
}

// ─── 销账 ────────────────────────────────────────────────────
const writeOffVisible = ref(false)
const writeOffTarget  = ref(null)
const writeOffAccount = ref('')
const writeOffReason  = ref('')
const writeOffLoading = ref(false)

function openWriteOff() {
  if (selectedRows.value.length === 0) return
  writeOffTarget.value  = selectedRows.value[0]
  writeOffAccount.value = ''
  writeOffReason.value  = ''
  writeOffVisible.value = true
}
function openWriteOffSingle(row) {
  writeOffTarget.value  = row
  writeOffAccount.value = ''
  writeOffReason.value  = ''
  writeOffVisible.value = true
}
async function confirmWriteOff() {
  if (!writeOffAccount.value.trim()) return
  writeOffLoading.value = true
  await new Promise(r => setTimeout(r, 1200))
  writeOffLoading.value = false
  writeOffVisible.value = false
  ElNotification({
    title: t('suspenseAcct.writeOffSuccessTitle'),
    message: t('suspenseAcct.writeOffSuccessMsg', { externalNo: writeOffTarget.value?.externalNo, account: writeOffAccount.value }),
    type: 'success',
    duration: 5000,
  })
  selectedRows.value = []
}
</script>

<style lang="scss" scoped>
.sa-page {
  display: flex;
  flex-direction: column;
  gap: 10px;
  height: 100%;
}

/* 过滤栏 */
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
  flex-shrink: 0;
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
}

/* 主卡片 */
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

/* Tabs */
.status-tabs {
  display: flex;
  border-bottom: 1px solid var(--git-border);
  padding: 0 16px;
  flex-shrink: 0;
}
.status-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 16px;
  height: 44px;
  font-size: 13px;
  color: var(--git-text-2);
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition: color 0.15s, border-color 0.15s;
  white-space: nowrap;
  &:hover { color: var(--git-primary); }
  &.active {
    color: var(--git-primary);
    font-weight: 600;
    border-bottom-color: var(--git-primary);
  }
}
.tab-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: 9px;
  font-size: 11px;
  font-weight: 600;
  &.count-warning { background: #fdf6ec; color: #e6a23c; }
  &.count-success { background: #f0f9eb; color: #67c23a; }
  &.count-danger  { background: #fef0f0; color: #f56c6c; }
}

/* 操作栏 */
.action-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-bottom: 1px solid var(--git-border);
  background: #fafbfc;
  flex-shrink: 0;
}
.selected-hint {
  font-size: 13px;
  color: var(--git-primary);
  margin-left: 4px;
}

/* 表格 */
:deep(.el-table) { flex: 1; font-size: 13px; }
:deep(.el-table .cell) { white-space: nowrap; }

.amount-text {
  font-family: 'Helvetica Neue', monospace;
  font-weight: 500;
}
.link-text {
  color: var(--git-primary);
  cursor: pointer;
  &:hover { text-decoration: underline; }
}

/* 分页 */
.pagination-bar {
  display: flex;
  justify-content: flex-end;
  padding: 10px 16px;
  border-top: 1px solid var(--git-border);
  flex-shrink: 0;
}

/* 销账弹窗 */
.wo-body { padding: 0 4px; }

.wo-info {
  background: #f8f9fc;
  border: 1px solid var(--git-border);
  border-radius: 4px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  overflow: hidden;

  /* English: single-column so long labels and values have room */
  &--en {
    grid-template-columns: 1fr;

    .wo-row {
      grid-template-columns: 135px 1fr;
      /* In 1-col layout only the very last row has no border */
      &:nth-last-child(-n+2) { border-bottom: 1px solid #edf0f7; }
      &:last-child { border-bottom: none; }
    }
  }
}
.wo-row {
  display: grid;
  grid-template-columns: 100px 1fr;
  border-bottom: 1px solid #edf0f7;
  min-height: 36px;
  &:nth-last-child(-n+2) { border-bottom: none; }
}
.wo-label {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  font-size: 12px;
  color: #606266;
  background: #f8f9fc;
  border-right: 1px solid #edf0f7;
  white-space: nowrap;
}
.wo-val {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  font-size: 13px;
  color: #303133;
}

/* el-form label-top spacing in EN */
:deep(.el-form--label-top .el-form-item__label) {
  margin-bottom: 4px;
  line-height: 1.4;
}
:deep(.el-form--label-top .el-form-item) {
  margin-bottom: 14px;
}
</style>
