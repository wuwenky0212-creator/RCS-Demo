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

        <el-table-column :label="t('suspenseAcct.status')" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)" size="small" effect="light">{{ statusMap[row.status] || row.status }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="suspenseDate" :label="t('suspenseAcct.suspenseDate')" width="110" />
        <el-table-column prop="suspenseTime" :label="t('suspenseAcct.suspenseTime')" width="90"  align="center" />

        <el-table-column prop="currency" :label="t('suspenseAcct.currency')" width="90" align="center" />

        <el-table-column :label="t('suspenseAcct.amount')" width="150" align="right">
          <template #default="{ row }">
            <span class="amount-text">{{ fmtAmt(row.amount) }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="externalNo"   :label="t('suspenseAcct.externalNo')" min-width="190" />

        <el-table-column v-if="activeTab === 'written'" prop="writeOffDate" :label="t('suspenseAcct.writeOffDate')" width="110" />
        <el-table-column v-if="activeTab === 'written'" prop="writeOffBy"   :label="t('suspenseAcct.writeOffBy')" width="110" />

        <el-table-column v-if="activeTab === 'pending'" :label="t('common.actions')" width="100" fixed="right" align="center">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openWriteOffSingle(row)">{{ t('suspenseAcct.writeOff') }}</el-button>
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
    width="760px"
    top="4vh"
    :close-on-click-modal="false"
  >
    <div v-if="writeOffTarget" class="wo-body">

      <!-- 收付信息区块 -->
      <div class="wo-section">
        <div class="wo-section-title"><span class="wo-bar"></span>{{ t('internalTransfer.suspenseSectionPayment') }}</div>
        <div class="wo-grid">
          <div class="wo-row"><div class="wo-label">{{ t('internalTransfer.suspensePaymentId') }}</div><div class="wo-val">{{ writeOffTarget.paymentId }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('internalTransfer.suspensePayDate') }}</div><div class="wo-val">{{ writeOffTarget.paymentDate }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('internalTransfer.suspenseSendDate') }}</div><div class="wo-val">{{ writeOffTarget.sendDate }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('internalTransfer.suspenseOperationOrg') }}</div><div class="wo-val">{{ writeOffTarget.operationOrg }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('internalTransfer.suspenseEntity') }}</div><div class="wo-val">{{ writeOffTarget.entity }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('internalTransfer.suspenseDirection') }}</div><div class="wo-val">{{ writeOffTarget.suspenseType === '应收' ? t('common.dirReceive') : t('common.dirPay') }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('internalTransfer.suspenseCpty') }}</div><div class="wo-val link-orange">{{ writeOffTarget.counterparty }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('internalTransfer.suspenseClearMethod') }}</div><div class="wo-val">{{ clearMethodMap[writeOffTarget.clearingMethod] || writeOffTarget.clearingMethod }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('internalTransfer.suspenseSettleMethod') }}</div><div class="wo-val">{{ settleMethodMap[writeOffTarget.settlementMethod] || writeOffTarget.settlementMethod }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('internalTransfer.suspenseCurrency') }}</div><div class="wo-val">{{ writeOffTarget.currency }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('internalTransfer.suspenseAmount') }}</div><div class="wo-val amount-text">{{ fmtAmt(writeOffTarget.amount) }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('internalTransfer.suspenseNetting') }}</div><div class="wo-val">{{ normalMap[writeOffTarget.nettingStatus] || writeOffTarget.nettingStatus }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('internalTransfer.suspensePayStatus') }}</div><div class="wo-val">{{ normalMap[writeOffTarget.paymentStatus] || writeOffTarget.paymentStatus }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('internalTransfer.suspenseCancelStatus') }}</div><div class="wo-val text-muted">{{ normalMap[writeOffTarget.cancelStatus] || writeOffTarget.cancelStatus }}</div></div>
          <div class="wo-row wo-row--full"><div class="wo-label">{{ t('internalTransfer.suspensePayerPath') }}</div><div class="wo-val">{{ writeOffTarget.payerPath }}</div></div>
          <div class="wo-row wo-row--full"><div class="wo-label">{{ t('internalTransfer.suspenseReceiverPath') }}</div><div class="wo-val">{{ writeOffTarget.receiverPath }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('internalTransfer.suspenseGenerateDate') }}</div><div class="wo-val">{{ writeOffTarget.generateDate }}</div></div>
        </div>
      </div>

      <!-- 销账信息区块 -->
      <div class="wo-section">
        <div class="wo-section-title"><span class="wo-bar"></span>{{ t('suspenseAcct.sectionWriteOff') }}</div>
        <div class="wo-grid">
          <div class="wo-row"><div class="wo-label">{{ t('internalTransfer.suspenseCurrencyCode') }}</div><div class="wo-val">{{ writeOffTarget.currency }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('suspenseAcct.bglAccount') }}</div><div class="wo-val link-text">{{ writeOffTarget.bglAccount }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('suspenseAcct.origAccount') }}</div><div class="wo-val">{{ writeOffTarget.origAccount }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('suspenseAcct.suspenseType') }}</div><div class="wo-val">{{ suspenseTypeMap[writeOffTarget.suspenseType] || writeOffTarget.suspenseType }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('suspenseAcct.amount') }}</div><div class="wo-val amount-text">{{ fmtAmt(writeOffTarget.amount) }}</div></div>
          <div class="wo-row"><div class="wo-label">{{ t('suspenseAcct.suspenseDate') }}</div><div class="wo-val">{{ writeOffTarget.suspenseDate }}</div></div>
          <div class="wo-row wo-row--full"><div class="wo-label">{{ t('suspenseAcct.externalNo') }}</div><div class="wo-val">{{ writeOffTarget.externalNo }}</div></div>

          <!-- 销账账户类型：可编辑 -->
          <div class="wo-row wo-row--full wo-row--input">
            <div class="wo-label wo-label--required">{{ t('suspenseAcct.writeOffAcctType') }}</div>
            <div class="wo-val wo-input-wrap">
              <el-select v-model="writeOffAccountType" :placeholder="t('suspenseAcct.writeOffAcctTypePlaceholder')" style="width:260px">
                <el-option :label="t('suspenseAcct.writeOffAcctTypeCustomer')" value="CUSTOMER" />
                <el-option :label="t('suspenseAcct.writeOffAcctTypeBgl')" value="BGL" />
                <el-option :label="t('suspenseAcct.writeOffAcctTypeInterbank')" value="INTERBANK" />
              </el-select>
            </div>
          </div>
          <!-- 销账账号：可编辑 -->
          <div class="wo-row wo-row--full wo-row--input">
            <div class="wo-label wo-label--required">{{ t('suspenseAcct.writeOffAcct') }}</div>
            <div class="wo-val wo-input-wrap">
              <el-input v-model="writeOffAccount" :placeholder="t('suspenseAcct.writeOffAcctPlaceholder')" style="width:260px" />
            </div>
          </div>
          <!-- 核销编号：可编辑 -->
          <div class="wo-row wo-row--full wo-row--input">
            <div class="wo-label">{{ t('suspenseAcct.chargeOffsCode') }}</div>
            <div class="wo-val wo-input-wrap">
              <el-input v-model="chargeOffsCode" :placeholder="t('suspenseAcct.chargeOffsCodePlaceholder')" style="width:260px" />
            </div>
          </div>
          <!-- 销账原因：可编辑 -->
          <div class="wo-row wo-row--full wo-row--input">
            <div class="wo-label">{{ t('suspenseAcct.writeOffReason') }}</div>
            <div class="wo-val wo-input-wrap">
              <el-input
                v-model="writeOffReason"
                type="textarea"
                :rows="3"
                :placeholder="t('suspenseAcct.writeOffReasonPlaceholder')"
                style="width:100%"
              />
            </div>
          </div>
        </div>
      </div>

    </div>
    <template #footer>
      <el-button @click="writeOffVisible = false">{{ t('common.cancel') }}</el-button>
      <el-button
        type="primary"
        :disabled="!writeOffAccount.trim() || !writeOffAccountType"
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

const { t } = useI18n()

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

const clearMethodMap = computed(() => ({
  'GROSS_SETTLE': t('internalTransfer.clearGross'),
  'NET_SETTLE':   t('internalTransfer.clearNet'),
}))

const settleMethodMap = computed(() => ({
  'SWIFT_INTERNAL': t('internalTransfer.settleSwiftInternal'),
}))

const normalMap = computed(() => ({
  'NORMAL':        t('internalTransfer.statusNormal'),
  'NOT_CANCELLED': t('internalTransfer.cancelNotCancelled'),
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
    origAccount:  '1010****0021',
    origAcctFlag: 'CGL_INTERNAL',
    status:       '挂账中',
    suspenseDate: '2026-05-08',
    suspenseTime: '14:32',
    currency:     'USD',
    amount:       1_000_000.00,
    externalNo:   'BANCS-20260508-7819',
    // 销账弹窗扩展字段（收付信息区）
    paymentId:        'PMT-IB-20260508-001',
    operationOrg:     'Head Office Branch',
    paymentDate:      '2026-05-08',
    sendDate:         '2026-05-08',
    entity:           'Head Office',
    counterparty:     'Agricultural Bank of China (ZG)',
    clearingMethod:   'GROSS_SETTLE',
    settlementMethod: 'SWIFT_INTERNAL',
    nettingStatus:    'NORMAL',
    paymentStatus:    'NORMAL',
    cancelStatus:     'NOT_CANCELLED',
    payerPath:        'SWIFT/BIC: HFZBCN2X',
    receiverPath:     'SWIFT/BIC: BKCHCNBJ',
    generateDate:     '2026-05-08',
  },
  {
    seq:          2,
    suspenseType: '应收',
    bglAccount:   '2199000000',
    origAccount:  '5500****0108',
    origAcctFlag: 'CGL_INTERNAL',
    status:       '挂账中',
    suspenseDate: '2026-05-09',
    suspenseTime: '10:15',
    currency:     'EUR',
    amount:       875_000.00,
    externalNo:   'BANCS-20260509-3361',
    paymentId:        'PMT-FX-20260509-005',
    operationOrg:     'Financial Markets Dept',
    paymentDate:      '2026-05-09',
    sendDate:         '2026-05-09',
    entity:           'Financial Markets Dept',
    counterparty:     'Deutsche Bank AG',
    clearingMethod:   'NET_SETTLE',
    settlementMethod: 'SWIFT_INTERNAL',
    nettingStatus:    'NORMAL',
    paymentStatus:    'NORMAL',
    cancelStatus:     'NOT_CANCELLED',
    payerPath:        'SWIFT/BIC: HFZBCN2X',
    receiverPath:     'SWIFT/BIC: DEUTDEFF',
    generateDate:     '2026-05-09',
  },
  {
    seq:          3,
    suspenseType: '应付',
    bglAccount:   '2199000000',
    origAccount:  '3100****3820',
    origAcctFlag: 'CGL_INTERNAL',
    status:       '挂账中',
    suspenseDate: '2026-05-09',
    suspenseTime: '13:47',
    currency:     'CNY',
    amount:       -88_560_000.00,
    externalNo:   'BANCS-20260509-7793',
    paymentId:        'PMT-MM-20260509-006',
    operationOrg:     'CBHB HQ',
    paymentDate:      '2026-05-09',
    sendDate:         '2026-05-09',
    entity:           'CBHB HQ',
    counterparty:     'Agricultural Bank of China (ZG)',
    clearingMethod:   'GROSS_SETTLE',
    settlementMethod: 'SWIFT_INTERNAL',
    nettingStatus:    'NORMAL',
    paymentStatus:    'NORMAL',
    cancelStatus:     'NOT_CANCELLED',
    payerPath:        'CNAPS/行号: 313100000013',
    receiverPath:     'CNAPS/行号: 103100000026',
    generateDate:     '2026-05-09',
  },
])

const writtenData = ref([
  {
    seq:          1,
    suspenseType: '应付',
    bglAccount:   '2199000000',
    origAccount:  '1010****0045',
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
const writeOffVisible     = ref(false)
const writeOffTarget      = ref(null)
const writeOffAccountType = ref('')
const writeOffAccount     = ref('')
const chargeOffsCode      = ref('')
const writeOffReason      = ref('')
const writeOffLoading     = ref(false)

function openWriteOff() {
  if (selectedRows.value.length === 0) return
  writeOffTarget.value      = selectedRows.value[0]
  writeOffAccountType.value = ''
  writeOffAccount.value     = ''
  chargeOffsCode.value      = ''
  writeOffReason.value      = ''
  writeOffVisible.value     = true
}
function openWriteOffSingle(row) {
  writeOffTarget.value      = row
  writeOffAccountType.value = ''
  writeOffAccount.value     = ''
  chargeOffsCode.value      = ''
  writeOffReason.value      = ''
  writeOffVisible.value     = true
}
async function confirmWriteOff() {
  if (!writeOffAccount.value.trim() || !writeOffAccountType.value) return
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
.wo-body {
  padding: 0;
  max-height: 72vh;
  overflow-y: auto;
}

.wo-section {
  background: #fff;
  border: 1px solid #e4e8f0;
  border-radius: 4px;
  margin: 0 0 12px;
  overflow: hidden;
}

.wo-section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 9px 14px;
  font-size: 13px;
  font-weight: 600;
  color: #303133;
  border-bottom: 1px solid #edf0f7;
  background: #fff;
}

.wo-bar {
  display: inline-block;
  width: 3px;
  height: 13px;
  background: var(--git-primary);
  border-radius: 2px;
}

.wo-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.wo-row {
  display: grid;
  grid-template-columns: 140px 1fr;
  border-bottom: 1px solid #edf0f7;
  min-height: 36px;

  &:last-child { border-bottom: none; }

  &--full {
    grid-column: 1 / -1;
  }

  &--input {
    min-height: 52px;
  }
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

  &--required::before {
    content: '*';
    color: #f56c6c;
    margin-right: 4px;
  }
}

.wo-val {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  font-size: 13px;
  color: #303133;
  background: #fff;
}

.wo-input-wrap {
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  padding: 8px 12px;
}

.link-orange {
  color: #e6a23c;
  cursor: pointer;
  &:hover { text-decoration: underline; }
}

.text-muted { color: #909399; }
</style>
