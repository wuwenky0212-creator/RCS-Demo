<template>
  <div class="itp-page">

    <!-- ① 搜索过滤区 -->
    <div class="filter-bar">
      <div class="filter-fields">
        <div class="filter-item">
          <label class="filter-label">{{ t('internalTransfer.paymentId') }}</label>
          <el-input
            v-model="filters.paymentId"
            :placeholder="t('common.pleaseInput')"
            clearable
            size="default"
            style="width:190px"
          >
            <template #prefix><el-icon><Search /></el-icon></template>
          </el-input>
        </div>
        <div class="filter-item">
          <label class="filter-label">{{ t('internalTransfer.externalNo') }}</label>
          <el-input
            v-model="filters.externalNo"
            :placeholder="t('common.pleaseInput')"
            clearable
            size="default"
            style="width:190px"
          />
        </div>
        <div class="filter-item">
          <label class="filter-label">{{ t('internalTransfer.operationOrg') }}</label>
          <el-input
            v-model="filters.operationOrg"
            :placeholder="t('common.pleaseInput')"
            clearable
            size="default"
            style="width:150px"
          />
        </div>
        <div class="filter-item">
          <label class="filter-label">{{ t('internalTransfer.plannedDate') }}</label>
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

    <!-- ② 主内容卡片 -->
    <div class="table-card">

      <!-- 状态切换 Tabs -->
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

      <!-- 操作工具栏（入账失败） -->
      <div v-if="activeTab === 'failed'" class="action-bar">
        <el-button
          type="primary"
          size="small"
          :disabled="selectedRows.length === 0"
          @click="openResend"
        >{{ t('internalTransfer.resend') }}</el-button>
        <el-button
          size="small"
          :disabled="selectedRows.length === 0"
          @click="openNoEntry"
        >{{ t('internalTransfer.noEntry') }}</el-button>
        <el-button
          size="small"
          :disabled="selectedRows.length === 0"
          @click="openSuspense()"
        >{{ t('internalTransfer.suspense') }}</el-button>
        <span v-if="selectedRows.length > 0" class="selected-hint">
          {{ t('internalTransfer.selectedHint', { n: selectedRows.length }) }}
        </span>
      </div>

      <!-- 操作工具栏（入账不明） -->
      <div v-if="activeTab === 'unknown'" class="action-bar">
        <el-button
          type="success"
          size="small"
          :disabled="selectedRows.length === 0"
          @click="openSetSuccess"
        >{{ t('internalTransfer.setSuccess') }}</el-button>
        <el-button
          type="danger"
          size="small"
          :disabled="selectedRows.length === 0"
          @click="openSetFailed"
        >{{ t('internalTransfer.setFailed') }}</el-button>
        <el-button
          size="small"
          :disabled="selectedRows.length === 0"
          @click="openAutoProcess"
        >{{ t('internalTransfer.autoProcess') }}</el-button>
        <span v-if="selectedRows.length > 0" class="selected-hint">
          {{ t('internalTransfer.selectedHint', { n: selectedRows.length }) }}
        </span>
      </div>

      <!-- 数据表格 -->
      <el-table
        :data="currentData"
        border
        stripe
        size="small"
        style="width:100%"
        :header-cell-style="{ background:'#f5f7fa', color:'#606266', fontWeight:'600', fontSize:'13px' }"
        @selection-change="val => selectedRows = val"
      >
        <el-table-column v-if="activeTab === 'failed' || activeTab === 'unknown'" type="selection" width="44" fixed="left" align="center" header-align="center" />

        <el-table-column prop="seq" :label="t('internalTransfer.seq')" width="60" align="center" fixed="left" />

        <el-table-column :label="t('internalTransfer.paymentId')" width="200" fixed="left">
          <template #default="{ row }">
            <span class="link-text">{{ row.paymentId }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="externalNo"       :label="t('internalTransfer.externalNo')"   width="200" />
        <el-table-column prop="debitAccount"     :label="t('internalTransfer.debitAccount')"  width="150" />
        <el-table-column prop="creditAccount"    :label="t('internalTransfer.creditAccount')" width="150" />
        <el-table-column :label="t('internalTransfer.creditFlag')" width="160" align="center">
          <template #default="{ row }">{{ acctFlagMap[row.creditFlag] || row.creditFlag }}</template>
        </el-table-column>
        <el-table-column prop="currency"         :label="t('internalTransfer.currency')"     width="90"  align="center" />

        <el-table-column :label="t('internalTransfer.amount')" width="140" align="right">
          <template #default="{ row }">
            <span class="amount-text">{{ fmtAmt(row.amount) }}</span>
          </template>
        </el-table-column>

        <el-table-column :label="t('internalTransfer.status')" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)" size="small" effect="light">{{ statusMap[row.status] || row.status }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="generateDate" :label="t('internalTransfer.generateDate')"     width="110" />
        <el-table-column prop="plannedDate"  :label="t('internalTransfer.plannedDate')" width="120" />
        <el-table-column prop="actualEntryDate" :label="t('internalTransfer.actualEntryDate')" width="120">
          <template #default="{ row }">{{ row.actualEntryDate || '-' }}</template>
        </el-table-column>
        <el-table-column prop="actualEntryTime" :label="t('internalTransfer.actualEntryTime')" width="110">
          <template #default="{ row }">{{ row.actualEntryTime || '-' }}</template>
        </el-table-column>
        <el-table-column prop="operationOrg" :label="t('internalTransfer.operationOrg')"   width="130" />
        <el-table-column v-if="activeTab === 'success'" prop="remark" :label="t('internalTransfer.remark')" min-width="200" />

        <el-table-column v-if="activeTab === 'failed'" :label="t('common.actions')" width="100" fixed="right" align="center" class-name="col-ops">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openResendSingle(row)">{{ t('internalTransfer.resend') }}</el-button>
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

  <!-- ── 置为成功 ── -->
  <el-dialog v-model="setSuccessVisible" :title="t('internalTransfer.setSuccessTitle')" width="440px" :close-on-click-modal="false">
    <div class="confirm-body">
      <el-icon class="confirm-icon" style="color:#67c23a"><WarningFilled /></el-icon>
      <div class="confirm-text">
        <div class="confirm-title">{{ t('internalTransfer.setSuccessConfirmTitle') }}</div>
        <div class="confirm-desc" v-html="t('internalTransfer.setSuccessDesc', { n: pendingUnknownRows.length })"></div>
      </div>
    </div>
    <template #footer>
      <el-button @click="setSuccessVisible = false">{{ t('common.cancel') }}</el-button>
      <el-button type="success" @click="confirmSetSuccess">{{ t('internalTransfer.confirmSetSuccess') }}</el-button>
    </template>
  </el-dialog>

  <!-- ── 置为失败 ── -->
  <el-dialog v-model="setFailedVisible" :title="t('internalTransfer.setFailedTitle')" width="500px" :close-on-click-modal="false">
    <div class="confirm-body">
      <el-icon class="confirm-icon" style="color:#f56c6c"><WarningFilled /></el-icon>
      <div class="confirm-text">
        <div class="confirm-title">{{ t('internalTransfer.setFailedConfirmTitle') }}</div>
        <div class="confirm-desc" v-html="t('internalTransfer.setFailedDesc', { n: pendingUnknownRows.length })"></div>
      </div>
    </div>
    <el-form label-width="100px" style="padding: 12px 8px 0">
      <el-form-item :label="t('internalTransfer.failedReason')">
        <el-input
          v-model="setFailedReason"
          type="textarea"
          :rows="3"
          :placeholder="t('internalTransfer.failedReasonPlaceholder')"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="setFailedVisible = false">{{ t('common.cancel') }}</el-button>
      <el-button type="danger" @click="confirmSetFailed">{{ t('internalTransfer.confirmSetFailed') }}</el-button>
    </template>
  </el-dialog>

  <!-- ── 自动处理 ── -->
  <el-dialog v-model="autoProcessVisible" :title="t('internalTransfer.autoProcessTitle')" width="440px" :close-on-click-modal="false">
    <div class="confirm-body">
      <el-icon class="confirm-icon"><WarningFilled /></el-icon>
      <div class="confirm-text">
        <div class="confirm-title">{{ t('internalTransfer.autoProcessConfirmTitle') }}</div>
        <div class="confirm-desc" v-html="t('internalTransfer.autoProcessDesc', { n: pendingUnknownRows.length })"></div>
      </div>
    </div>
    <template #footer>
      <el-button @click="autoProcessVisible = false">{{ t('common.cancel') }}</el-button>
      <el-button type="primary" @click="confirmAutoProcess">{{ t('common.confirm') }}</el-button>
    </template>
  </el-dialog>

  <!-- ── 补送确认弹窗 ── -->
  <el-dialog v-model="resendVisible" :title="t('internalTransfer.resendTitle')" width="440px" :close-on-click-modal="false">
    <div class="confirm-body">
      <el-icon class="confirm-icon"><WarningFilled /></el-icon>
      <div class="confirm-text">
        <div class="confirm-title">{{ t('internalTransfer.resendConfirmTitle') }}</div>
        <div class="confirm-desc" v-html="t('internalTransfer.resendDesc', { n: pendingRows.length })"></div>
      </div>
    </div>
    <template #footer>
      <el-button @click="resendVisible = false">{{ t('common.cancel') }}</el-button>
      <el-button type="primary" @click="confirmResend">{{ t('internalTransfer.confirmResend') }}</el-button>
    </template>
  </el-dialog>

  <!-- ── 不入账弹窗 ── -->
  <el-dialog v-model="noEntryVisible" :title="t('internalTransfer.noEntryTitle')" width="500px" :close-on-click-modal="false">
    <el-form label-width="100px" style="padding: 0 8px">
      <el-form-item :label="t('internalTransfer.noEntryReason')">
        <el-input
          v-model="noEntryReason"
          type="textarea"
          :rows="4"
          :placeholder="t('internalTransfer.noEntryReasonPlaceholder')"
        />
      </el-form-item>
      <el-form-item :label="t('internalTransfer.operator')">
        <el-input :model-value="t('internalTransfer.operatorCurrentUser')" disabled />
      </el-form-item>
    </el-form>
    <div class="dialog-warn">
      <el-icon><WarningFilled /></el-icon>
      {{ t('internalTransfer.noEntryWarn') }}
    </div>
    <template #footer>
      <el-button @click="noEntryVisible = false">{{ t('common.cancel') }}</el-button>
      <el-button type="danger" @click="confirmNoEntry">{{ t('internalTransfer.submitReview') }}</el-button>
    </template>
  </el-dialog>

  <!-- ── 挂账弹窗 ── -->
  <el-dialog
    v-model="suspenseVisible"
    :title="t('internalTransfer.suspenseTitle')"
    width="760px"
    top="4vh"
    :close-on-click-modal="false"
    :before-close="closeSuspense"
    class="suspense-dialog"
  >
    <div v-if="suspenseRow" class="susp-body">

      <!-- 收付信息区块 -->
      <div class="susp-section">
        <div class="susp-section-title"><span class="susp-bar"></span>{{ t('internalTransfer.suspenseSectionPayment') }}</div>
        <div class="susp-grid">
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspensePaymentId') }}</div><div class="susp-val link-text">{{ suspenseRow.paymentId }}</div></div>
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspensePayDate') }}</div><div class="susp-val">{{ suspenseRow.paymentDate }}</div></div>
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspenseSendDate') }}</div><div class="susp-val">{{ suspenseRow.sendDate }}</div></div>
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspenseOperationOrg') }}</div><div class="susp-val">{{ suspenseRow.operationOrg }}</div></div>
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspenseEntity') }}</div><div class="susp-val">{{ suspenseRow.entity }}</div></div>
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspenseDirection') }}</div><div class="susp-val">{{ suspenseRow.amount >= 0 ? t('common.dirReceive') : t('common.dirPay') }}</div></div>
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspenseCpty') }}</div><div class="susp-val link-orange">{{ suspenseRow.counterparty }}</div></div>
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspenseClearMethod') }}</div><div class="susp-val">{{ clearMethodMap[suspenseRow.clearingMethod] || suspenseRow.clearingMethod }}</div></div>
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspenseSettleMethod') }}</div><div class="susp-val">{{ settleMethodMap[suspenseRow.settlementMethod] || suspenseRow.settlementMethod }}</div></div>
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspenseCurrency') }}</div><div class="susp-val">{{ suspenseRow.currency }}</div></div>
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspenseAmount') }}</div><div class="susp-val amount-text">{{ fmtAmt(suspenseRow.amount) }}</div></div>
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspenseNetting') }}</div><div class="susp-val">{{ normalMap[suspenseRow.nettingStatus] || suspenseRow.nettingStatus }}</div></div>
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspensePayStatus') }}</div><div class="susp-val">{{ normalMap[suspenseRow.paymentStatus] || suspenseRow.paymentStatus }}</div></div>
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspenseCancelStatus') }}</div><div class="susp-val text-muted">{{ normalMap[suspenseRow.cancelStatus] || suspenseRow.cancelStatus }}</div></div>
          <div class="susp-row susp-row--full"><div class="susp-label">{{ t('internalTransfer.suspensePayerPath') }}</div><div class="susp-val">{{ suspenseRow.payerPath }}</div></div>
          <div class="susp-row susp-row--full"><div class="susp-label">{{ t('internalTransfer.suspenseReceiverPath') }}</div><div class="susp-val">{{ suspenseRow.receiverPath }}</div></div>
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspenseGenerateDate') }}</div><div class="susp-val">{{ suspenseRow.generateDate }}</div></div>
        </div>
      </div>

      <!-- 挂账信息区块 -->
      <div class="susp-section">
        <div class="susp-section-title"><span class="susp-bar"></span>{{ t('internalTransfer.suspenseSectionAcct') }}</div>
        <div class="susp-grid">
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspenseCurrencyCode') }}</div><div class="susp-val">{{ suspenseRow.currency }}</div></div>
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspenseDebitAcct') }}</div><div class="susp-val">{{ suspenseRow.debitAccount }}</div></div>
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspenseCreditAcct') }}</div><div class="susp-val">{{ suspenseRow.creditAccount }}</div></div>
          <div class="susp-row"><div class="susp-label">{{ t('internalTransfer.suspenseAmount') }}</div><div class="susp-val amount-text">{{ fmtAmt(suspenseRow.amount) }}</div></div>
          <!-- BGL账号：可编辑 -->
          <div class="susp-row susp-row--full susp-row--input">
            <div class="susp-label susp-label--required">{{ t('internalTransfer.suspenseBglAcct') }}</div>
            <div class="susp-val susp-input-wrap">
              <el-input
                v-model="bglAccount"
                :placeholder="t('internalTransfer.suspenseBglPlaceholder')"
                :class="{ 'is-error': bglAccountError }"
                size="default"
                style="width: 300px"
                @input="bglAccountError = ''"
              />
              <span v-if="bglAccountError" class="input-error-tip">{{ bglAccountError }}</span>
              <span class="input-hint">{{ t('internalTransfer.suspenseBglHint') }}</span>
            </div>
          </div>
        </div>
      </div>

    </div>

    <template #footer>
      <el-button @click="closeSuspense">{{ t('common.cancel') }}</el-button>
      <el-button
        type="warning"
        :loading="suspenseLoading"
        @click="confirmSuspense"
      >{{ suspenseLoading ? t('internalTransfer.submitting') : t('internalTransfer.confirmSuspense') }}</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage, ElNotification } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { Search, WarningFilled } from '@element-plus/icons-vue'

const { t } = useI18n()

// ─── Computed translation maps ───────────────────────────────
const statusMap = computed(() => ({
  '入账失败': t('internalTransfer.statusFailed'),
  '入账不明': t('internalTransfer.statusUnknown'),
  '入账成功': t('internalTransfer.statusSuccess'),
  '不入账':   t('internalTransfer.statusVoid'),
}))

const acctFlagMap = computed(() => ({
  'CGL_INTERNAL':  t('internalTransfer.acctFlagCgl'),
  'BGL_ACCOUNT':   t('internalTransfer.acctFlagBgl'),
  'BGL_PENDING':   t('internalTransfer.acctFlagBglPending'),
  'BGL_DEPOSIT':   t('internalTransfer.acctFlagBglDeposit'),
  'BGL_SETTLE':    t('internalTransfer.acctFlagBglSettle'),
  'BGL_INCOME':    t('internalTransfer.acctFlagBglIncome'),
  'NET_NETTING':   t('internalTransfer.acctFlagNet'),
}))

const clearMethodMap = computed(() => ({
  'GROSS_SETTLE':  t('internalTransfer.clearGross'),
  'NET_SETTLE':    t('internalTransfer.clearNet'),
}))

const settleMethodMap = computed(() => ({
  'SWIFT_INTERNAL': t('internalTransfer.settleSwiftInternal'),
}))

const normalMap = computed(() => ({
  'NORMAL':        t('internalTransfer.statusNormal'),
  'NOT_CANCELLED': t('internalTransfer.cancelNotCancelled'),
}))

// ─── 过滤条件 ────────────────────────────────────────────────
const filters = ref({
  paymentId:    '',
  externalNo:   '',
  operationOrg: '',
  dateRange:    ['2025-05-08', '2026-05-08'],
})
function handleQuery() { ElMessage.success(t('common.querySuccess')) }
function handleReset() {
  filters.value = { paymentId: '', externalNo: '', operationOrg: '', dateRange: [] }
}

// ─── 状态 Tabs ───────────────────────────────────────────────
const tabs = computed(() => [
  { key: 'failed',   label: t('internalTransfer.tabFailed'), count: 4,    countType: 'count-danger' },
  { key: 'unknown',  label: t('internalTransfer.tabUnknown'), count: 4,  countType: 'count-warning' },
  { key: 'success',  label: t('internalTransfer.tabSuccess'), count: 2,    countType: 'count-success' },
  { key: 'void',     label: t('internalTransfer.tabVoid'),   count: null,  countType: '' },
])
const activeTab = ref('failed')
function switchTab(key) {
  activeTab.value = key
  selectedRows.value = []
}

// ─── 分页 ────────────────────────────────────────────────────
const page     = ref(1)
const pageSize = ref(20)

// ─── Mock 数据 ───────────────────────────────────────────────
const failedData = ref([
  {
    seq:          1,
    paymentId:    'PMT-IB-20260508-001',
    externalNo:   'BANCS-20260508-7819',
    debitAccount: '1010****0021',
    debitFlag:    'CGL_INTERNAL',
    creditAccount:'2524****4301',
    creditFlag:   'BGL_ACCOUNT',
    currency:     'USD',
    amount:       1_000_000.00,
    status:       '入账失败',
    generateDate: '2026-05-08',
    plannedDate:  '2026-05-11',
    actualEntryDate: '',
    actualEntryTime: '',
    operationOrg: 'Head Office Branch',
    // 挂账弹窗扩展字段
    paymentDate:    '2026-05-08',
    sendDate:       '2026-05-08',
    entity:         'Head Office',
    counterparty:   'Agricultural Bank of China (ZG)',
    clearingMethod: 'GROSS_SETTLE',
    settlementMethod:'SWIFT_INTERNAL',
    nettingStatus:  'NORMAL',
    paymentStatus:  'NORMAL',
    cancelStatus:   'NOT_CANCELLED',
    payerPath:      'SWIFT/BIC: HFZBCN2X',
    receiverPath:   'SWIFT/BIC: BKCHCNBJ',
  },
  {
    seq:          2,
    paymentId:    'PMT-BD-20260508-001',
    externalNo:   'BANCS-20260508-3498',
    debitAccount: '4032****0117',
    debitFlag:    'CGL_INTERNAL',
    creditAccount:'1303****8309',
    creditFlag:   'BGL_ACCOUNT',
    currency:     'CNY',
    amount:       1_008_666.67,
    status:       '入账失败',
    generateDate: '2026-05-08',
    plannedDate:  '2026-05-08',
    actualEntryDate: '',
    actualEntryTime: '',
    operationOrg: 'BANKZB',
    paymentDate:    '2026-05-08',
    sendDate:       '2026-05-08',
    entity:         'CBHB HQ',
    counterparty:   '10275 ZG农业银行股份有限公司',
    clearingMethod: '净额清算',
    settlementMethod:'SWIFT_INTERNAL',
    nettingStatus:  'NORMAL',
    paymentStatus:  'NORMAL',
    cancelStatus:   'NOT_CANCELLED',
    payerPath:      'CNAPS/行号: 313100000013',
    receiverPath:   'CNAPS/行号: 103100000026',
  },
  {
    seq:          3,
    paymentId:    'PMT-FX-20260508-002',
    externalNo:   'BANCS-20260508-2252',
    debitAccount: '5500****0091',
    debitFlag:    'CGL_INTERNAL',
    creditAccount:'9999****0012',
    creditFlag:   'BGL_ACCOUNT',
    currency:     'USD',
    amount:       10_000.00,
    status:       '入账失败',
    generateDate: '2026-05-08',
    plannedDate:  '2026-05-08',
    actualEntryDate: '',
    actualEntryTime: '',
    operationOrg: 'Financial Markets Dept',
    paymentDate:    '2026-05-08',
    sendDate:       '2026-05-08',
    entity:         'Head Office',
    counterparty:   'Agricultural Bank of China (ZG)',
    clearingMethod: 'NET_SETTLE',
    settlementMethod:'SWIFT_INTERNAL',
    nettingStatus:  'NORMAL',
    paymentStatus:  'NORMAL',
    cancelStatus:   'NOT_CANCELLED',
    payerPath:      'SWIFT/BIC: HFZBCN2X',
    receiverPath:   'SWIFT/BIC: BKCHCNBJ',
  },
  {
    seq:          4,
    paymentId:    'PMT-MM-20260508-003',
    externalNo:   'BANCS-20260508-0341',
    debitAccount: '3100****2610',
    debitFlag:    'CGL_INTERNAL',
    creditAccount:'1303****0281',
    creditFlag:   'BGL_ACCOUNT',
    currency:     'CNY',
    amount:       426_039_536.47,
    status:       '入账失败',
    generateDate: '2026-05-08',
    plannedDate:  '2026-05-08',
    actualEntryDate: '',
    actualEntryTime: '',
    operationOrg: 'CBHB HQ',
    paymentDate:    '2026-05-08',
    sendDate:       '2026-05-08',
    entity:         'CBHB HQ',
    counterparty:   'Agricultural Bank of China (ZG)',
    clearingMethod: 'GROSS_SETTLE',
    settlementMethod:'SWIFT_INTERNAL',
    nettingStatus:  'NORMAL',
    paymentStatus:  'NORMAL',
    cancelStatus:   'NOT_CANCELLED',
    payerPath:      'CNAPS/行号: 313100000013',
    receiverPath:   'CNAPS/行号: 103100000026',
  },
])

// ─── 入账不明 Mock 数据 ──────────────────────────────────────
const unknownData = ref([
  {
    seq:          1,
    paymentId:    'PMT-IB-20260509-004',
    externalNo:   'BANCS-20260509-1127',
    debitAccount: '1010****0034',
    debitFlag:    'CGL_INTERNAL',
    creditAccount:'2524****8802',
    creditFlag:   'BGL_ACCOUNT',
    currency:     'USD',
    amount:       2_500_000.00,
    status:       '入账不明',
    generateDate: '2026-05-09',
    plannedDate:  '2026-05-12',
    actualEntryDate: '',
    actualEntryTime: '',
    operationOrg: 'Head Office Branch',
  },
  {
    seq:          2,
    paymentId:    'PMT-FX-20260509-005',
    externalNo:   'BANCS-20260509-3361',
    debitAccount: '5500****0108',
    debitFlag:    'CGL_INTERNAL',
    creditAccount:'9999****0033',
    creditFlag:   'BGL_ACCOUNT',
    currency:     'EUR',
    amount:       875_000.00,
    status:       '入账不明',
    generateDate: '2026-05-09',
    plannedDate:  '2026-05-09',
    actualEntryDate: '',
    actualEntryTime: '',
    operationOrg: 'Financial Markets Dept',
  },
  {
    seq:          3,
    paymentId:    'PMT-BD-20260509-003',
    externalNo:   'BANCS-20260509-5540',
    debitAccount: '4032****0228',
    debitFlag:    'CGL_INTERNAL',
    creditAccount:'1303****9917',
    creditFlag:   'BGL_ACCOUNT',
    currency:     'CNY',
    amount:       -3_120_000.00,
    status:       '入账不明',
    generateDate: '2026-05-09',
    plannedDate:  '2026-05-09',
    actualEntryDate: '',
    actualEntryTime: '',
    operationOrg: 'BANKZB',
  },
  {
    seq:          4,
    paymentId:    'PMT-MM-20260509-006',
    externalNo:   'BANCS-20260509-7793',
    debitAccount: '3100****3820',
    debitFlag:    'CGL_INTERNAL',
    creditAccount:'1303****0555',
    creditFlag:   'BGL_ACCOUNT',
    currency:     'CNY',
    amount:       88_560_000.00,
    status:       '入账不明',
    generateDate: '2026-05-09',
    plannedDate:  '2026-05-12',
    actualEntryDate: '',
    actualEntryTime: '',
    operationOrg: 'CBHB HQ',
  },
])

// ─── 入账成功 Mock 数据 ──────────────────────────────────────
// 记录1：USD 同业拆借本金补送后成功入账
// 记录2：CNY 现券买卖全价款 DVP 交割成功
const successData = ref([
  {
    seq:          1,
    paymentId:    'PMT-IB-20260507-003',
    externalNo:   'BANCS-20260507-6210',
    debitAccount: '1010****0021',           // 101000000021 脱敏
    debitFlag:    'CGL_INTERNAL',
    creditAccount:'2524****4301',            // 2524410301 脱敏
    creditFlag:   'BGL_ACCOUNT',
    currency:     'USD',
    amount:       500_000.00,
    status:       '入账成功',
    generateDate: '2026-05-07',
    plannedDate:  '2026-05-08',
    actualEntryDate: '2026-05-08',
    actualEntryTime: '09:15:32',
    operationOrg: 'Head Office Branch',
    remark:       'Entry successful, BANCS response code: 00',
  },
  {
    seq:          2,
    paymentId:    'PMT-BD-20260507-002',
    externalNo:   'BANCS-20260507-4812',
    debitAccount: '4032****0117',            // 403200000117 脱敏
    debitFlag:    'CGL_INTERNAL',
    creditAccount:'6011****0000',            // 6011000000 脱敏
    creditFlag:   'BGL_ACCOUNT',
    currency:     'CNY',
    amount:       980_000.00,
    status:       '入账成功',
    generateDate: '2026-05-07',
    plannedDate:  '2026-05-07',
    actualEntryDate: '2026-05-07',
    actualEntryTime: '14:32:08',
    operationOrg: 'BANKZB',
    remark:       'DVP delivery entry completed, BANCS response code: 00',
  },
])

const currentData = computed(() => {
  if (activeTab.value === 'failed')  return failedData.value
  if (activeTab.value === 'unknown') return unknownData.value
  if (activeTab.value === 'success') return successData.value
  return []
})

// ─── 表格多选 ────────────────────────────────────────────────
const selectedRows = ref([])

// ─── 格式化 ─────────────────────────────────────────────────
function fmtAmt(val) {
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
function statusTagType(s) {
  const map = { '入账失败': 'danger', '入账不明': 'warning', '入账成功': 'success', '不入账': 'info' }
  return map[s] || ''
}

// ─── 入账不明操作 ────────────────────────────────────────────
const pendingUnknownRows  = ref([])
const setSuccessVisible   = ref(false)
const setFailedVisible    = ref(false)
const setFailedReason     = ref('')
const autoProcessVisible  = ref(false)

function openSetSuccess() {
  pendingUnknownRows.value = [...selectedRows.value]
  setSuccessVisible.value = true
}
function confirmSetSuccess() {
  setSuccessVisible.value = false
  ElNotification({ title: t('internalTransfer.setSuccessNotifTitle'), message: t('internalTransfer.setSuccessNotifMsg', { n: pendingUnknownRows.value.length }), type: 'success', duration: 4000 })
  selectedRows.value = []
}

function openSetFailed() {
  pendingUnknownRows.value = [...selectedRows.value]
  setFailedReason.value = ''
  setFailedVisible.value = true
}
function confirmSetFailed() {
  setFailedVisible.value = false
  ElNotification({ title: t('internalTransfer.setFailedNotifTitle'), message: t('internalTransfer.setFailedNotifMsg', { n: pendingUnknownRows.value.length }), type: 'warning', duration: 4000 })
  selectedRows.value = []
}

function openAutoProcess() {
  pendingUnknownRows.value = [...selectedRows.value]
  autoProcessVisible.value = true
}
function confirmAutoProcess() {
  autoProcessVisible.value = false
  ElNotification({ title: t('internalTransfer.autoProcessNotifTitle'), message: t('internalTransfer.autoProcessNotifMsg', { n: pendingUnknownRows.value.length }), type: 'info', duration: 5000 })
  selectedRows.value = []
}

// ─── 补送 ────────────────────────────────────────────────────
const resendVisible = ref(false)
const pendingRows   = ref([])

function openResend() {
  pendingRows.value = [...selectedRows.value]
  resendVisible.value = true
}
function openResendSingle(row) {
  pendingRows.value = [row]
  resendVisible.value = true
}
function confirmResend() {
  resendVisible.value = false
  ElNotification({ title: t('internalTransfer.resendNotifTitle'), message: t('internalTransfer.resendNotifMsg', { n: pendingRows.value.length }), type: 'success', duration: 4000 })
  pendingRows.value = []
  selectedRows.value = []
}

// ─── 不入账 ──────────────────────────────────────────────────
const noEntryVisible = ref(false)
const noEntryReason  = ref('')

function openNoEntry() {
  noEntryReason.value = ''
  noEntryVisible.value = true
}
function confirmNoEntry() {
  noEntryVisible.value = false
  ElNotification({ title: t('internalTransfer.noEntryNotifTitle'), message: t('internalTransfer.noEntryNotifMsg'), type: 'warning', duration: 4000 })
  selectedRows.value = []
}

// ─── 挂账 ────────────────────────────────────────────────────
const suspenseVisible  = ref(false)
const suspenseRow      = ref(null)
const bglAccount       = ref('')
const bglAccountError  = ref('')
const suspenseLoading  = ref(false)

function openSuspense() {
  if (selectedRows.value.length === 0) return
  suspenseRow.value     = selectedRows.value[0]
  bglAccount.value      = '2199000000'   // 挂账参数维护默认带出
  bglAccountError.value = ''
  suspenseLoading.value = false
  suspenseVisible.value = true
}
function openSuspenseSingle(row) {
  suspenseRow.value     = row
  bglAccount.value      = '2199000000'
  bglAccountError.value = ''
  suspenseLoading.value = false
  suspenseVisible.value = true
}
function closeSuspense() {
  suspenseVisible.value = false
  bglAccount.value      = ''
  suspenseRow.value     = null
}
async function confirmSuspense() {
  if (!bglAccount.value.trim()) {
    bglAccountError.value = t('internalTransfer.bglRequired')
    return
  }
  bglAccountError.value = ''
  suspenseLoading.value = true
  // 模拟 POST 请求延迟
  await new Promise(r => setTimeout(r, 1500))
  suspenseLoading.value = false
  suspenseVisible.value = false
  ElNotification({
    title: t('internalTransfer.suspenseNotifTitle'),
    message: t('internalTransfer.suspenseNotifMsg', { paymentId: suspenseRow.value?.paymentId, bglAcct: bglAccount.value }),
    type: 'success',
    duration: 5000,
  })
  selectedRows.value = []
  suspenseRow.value  = null
}
</script>

<style lang="scss" scoped>
.itp-page {
  display: flex;
  flex-direction: column;
  gap: 10px;
  height: 100%;
}

/* ─── 过滤栏 ─── */
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

/* ─── 主卡片 ─── */
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

/* ─── 状态 Tabs ─── */
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

  &.count-danger  { background: #fef0f0; color: #f56c6c; }
  &.count-warning { background: #fdf6ec; color: #e6a23c; }
  &.count-success { background: #f0f9eb; color: #67c23a; }
}

/* ─── 操作工具栏 ─── */
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

/* ─── 表格 ─── */
:deep(.el-table) {
  flex: 1;
  font-size: 13px;
}

:deep(.el-table .cell) {
  white-space: nowrap;
}
:deep(.el-table .el-table-column--selection .cell) {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;
}

:deep(.col-ops .cell) {
  white-space: nowrap;
  overflow: visible;
}

.link-text {
  color: var(--git-primary);
  cursor: pointer;
  &:hover { text-decoration: underline; }
}

.amount-text {
  font-family: 'Helvetica Neue', monospace;
  font-weight: 500;
}

/* ─── 分页 ─── */
.pagination-bar {
  display: flex;
  justify-content: flex-end;
  padding: 10px 16px;
  border-top: 1px solid var(--git-border);
  flex-shrink: 0;
}

/* ─── 弹窗 ─── */
.confirm-body {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 4px 8px 12px;

  .confirm-icon {
    font-size: 28px;
    color: #e6a23c;
    flex-shrink: 0;
    margin-top: 2px;
  }

  .confirm-title {
    font-size: 15px;
    font-weight: 600;
    color: #303133;
    margin-bottom: 8px;
  }

  .confirm-desc {
    font-size: 13px;
    color: #606266;
    line-height: 1.7;
    b { color: #303133; }
  }
}

/* ── 挂账弹窗内容 ── */
.susp-body {
  padding: 0;
  max-height: 72vh;
  overflow-y: auto;
}

.susp-section {
  background: #fff;
  border: 1px solid #e4e8f0;
  border-radius: 4px;
  margin: 0 0 12px;
  overflow: hidden;
}

.susp-section-title {
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

.susp-bar {
  display: inline-block;
  width: 3px;
  height: 13px;
  background: var(--git-primary);
  border-radius: 2px;
}

.susp-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.susp-row {
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

.susp-label {
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

.susp-val {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  font-size: 13px;
  color: #303133;
  background: #fff;
}

.susp-input-wrap {
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  padding: 8px 12px;
}

.input-error-tip {
  font-size: 12px;
  color: #f56c6c;
}

.input-hint {
  font-size: 12px;
  color: #909399;
}

.is-error :deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px #f56c6c inset;
}

.link-orange {
  color: #e6a23c;
  cursor: pointer;
  &:hover { text-decoration: underline; }
}

.text-muted { color: #909399; }

.dialog-warn {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 8px 8px 0;
  padding: 10px 14px;
  background: #fff8e6;
  border: 1px solid #ffe4a0;
  border-radius: 4px;
  font-size: 12px;
  color: #92710e;

  .el-icon { color: #e6a23c; font-size: 14px; flex-shrink: 0; }
}
</style>
