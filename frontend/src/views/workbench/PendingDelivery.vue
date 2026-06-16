<template>
  <div class="pd-page">

    <!-- ── 查询区 ── -->
    <div class="filter-bar">
      <div class="filter-grid">
        <!-- 第一行：始终显示 -->
        <div class="fg-item">
          <label class="fg-label">{{ t('pendingDelivery.cashflowId') }}</label>
          <el-input v-model="filters.cashflowId" :placeholder="t('common.pleaseInput')" clearable size="default" class="fg-input" />
        </div>
        <div class="fg-item">
          <label class="fg-label">{{ t('pendingDelivery.paymentInfoId') }}</label>
          <el-input v-model="filters.paymentInfoId" :placeholder="t('common.pleaseInput')" clearable size="default" class="fg-input" />
        </div>
        <div class="fg-item">
          <label class="fg-label">{{ t('pendingDelivery.externalNo') }}</label>
          <el-input v-model="filters.externalNo" :placeholder="t('common.pleaseInput')" clearable size="default" class="fg-input" />
        </div>
        <div class="fg-item">
          <label class="fg-label">{{ t('pendingDelivery.operatingInst') }}</label>
          <el-input v-model="filters.operatingInst" :placeholder="t('common.pleaseInput')" clearable size="default" class="fg-input" />
        </div>
        <!-- 第一行最后一格：收起时显示查询/重置+展开按钮 -->
        <div v-if="!filterExpanded" class="fg-item fg-item--actions">
          <el-button type="primary" size="default" @click="handleQuery">{{ t('common.query') }}</el-button>
          <el-button size="default" @click="handleReset">{{ t('common.reset') }}</el-button>
          <el-button link size="default" @click="filterExpanded = true" class="expand-btn">
            {{ t('common.expand') }}<el-icon class="expand-icon"><ArrowDown /></el-icon>
          </el-button>
        </div>
        <div v-if="filterExpanded" class="fg-item">
          <label class="fg-label">{{ t('pendingDelivery.counterparty') }}</label>
          <el-input v-model="filters.counterparty" :placeholder="t('common.pleaseInput')" clearable size="default" class="fg-input" />
        </div>

        <!-- 展开后的行 -->
        <template v-if="filterExpanded">
          <div class="fg-item">
            <label class="fg-label">{{ t('pendingDelivery.currency') }}</label>
            <el-select v-model="filters.currency" :placeholder="t('common.all')" clearable size="default" class="fg-input">
              <el-option label="USD" value="USD" />
              <el-option label="EUR" value="EUR" />
              <el-option label="CNY" value="CNY" />
              <el-option label="IDR" value="IDR" />
            </el-select>
          </div>
          <div class="fg-item">
            <label class="fg-label">{{ t('pendingDelivery.clearingMethod') }}</label>
            <el-select v-model="filters.clearingMethod" :placeholder="t('common.all')" clearable size="default" class="fg-input">
              <el-option :label="t('pendingDelivery.cmGross')" value="全额" />
              <el-option :label="t('pendingDelivery.cmNet')"   value="净额" />
            </el-select>
          </div>
          <div class="fg-item">
            <label class="fg-label">{{ t('pendingDelivery.settlementMethod') }}</label>
            <el-select v-model="filters.settlementMethod" :placeholder="t('common.all')" clearable size="default" class="fg-input">
              <el-option :label="t('pendingDelivery.smInternal')"   value="内部账" />
              <el-option :label="t('pendingDelivery.smSwiftInter')" value="SWIFT+内部账" />
            </el-select>
          </div>
          <div class="fg-item">
            <label class="fg-label">{{ t('pendingDelivery.direction') }}</label>
            <el-select v-model="filters.direction" :placeholder="t('common.all')" clearable size="default" class="fg-input">
              <el-option :label="t('pendingDelivery.dirPay')"  value="付" />
              <el-option :label="t('pendingDelivery.dirRecv')" value="收" />
            </el-select>
          </div>
          <div class="fg-item fg-item--span2">
            <label class="fg-label">{{ t('pendingDelivery.paymentDate') }}</label>
            <el-date-picker v-model="filters.paymentDate" type="daterange" range-separator="—"
              :start-placeholder="t('common.startDate')" :end-placeholder="t('common.endDate')"
              value-format="YYYY-MM-DD" size="default" class="fg-input" />
          </div>
          <div class="fg-item fg-item--span2">
            <label class="fg-label">{{ t('pendingDelivery.generateDate') }}</label>
            <el-date-picker v-model="filters.generateDate" type="daterange" range-separator="—"
              :start-placeholder="t('common.startDate')" :end-placeholder="t('common.endDate')"
              value-format="YYYY-MM-DD" size="default" class="fg-input" />
          </div>
          <div class="fg-item fg-item--actions">
            <el-button type="primary" size="default" @click="handleQuery">{{ t('common.query') }}</el-button>
            <el-button size="default" @click="handleReset">{{ t('common.reset') }}</el-button>
            <el-button link size="default" @click="filterExpanded = false" class="expand-btn">
              {{ t('common.collapse') }}<el-icon class="expand-icon expand-icon--up"><ArrowDown /></el-icon>
            </el-button>
          </div>
        </template>
      </div>
    </div>

    <!-- ── 主卡片 ── -->
    <div class="table-card">

      <!-- 操作栏 -->
      <div class="action-bar">
        <el-button type="primary" size="small" :disabled="selectedRows.length !== 1" @click="openDelivery">
          {{ t('pendingDelivery.actionDeliver') }}
        </el-button>
        <el-button size="small" :disabled="selectedRows.length !== 1" @click="openSuspense">
          {{ t('pendingDelivery.actionSuspense') }}
        </el-button>
        <el-button size="small" :disabled="selectedRows.length !== 1" @click="handleNoPost">
          {{ t('pendingDelivery.actionNoPost') }}
        </el-button>
        <span v-if="selectedRows.length > 0" class="selected-hint">
          {{ t('pendingDelivery.selectedHint', { n: selectedRows.length }) }}
        </span>
        <div class="action-bar-right">
          <span class="page-size-label">{{ t('pendingDelivery.perPage') }}</span>
          <el-select v-model="pageSize" size="small" style="width:76px" @change="page = 1">
            <el-option :label="15" :value="15" />
            <el-option :label="20" :value="20" />
            <el-option :label="30" :value="30" />
            <el-option :label="40" :value="40" />
            <el-option :label="50" :value="50" />
          </el-select>
        </div>
      </div>


      <!-- 表格 -->
      <el-table :data="pagedData" border stripe size="small" style="width:100%"
        :header-cell-style="{ background:'#f5f7fa', color:'#606266', fontWeight:'600', fontSize:'13px' }"
        @selection-change="val => selectedRows = val">
        <el-table-column type="selection" width="44" fixed="left" align="center" header-align="center" />
        <el-table-column prop="seq" :label="t('pendingDelivery.colSeq')" width="55" align="center" fixed="left" />
        <el-table-column prop="cashflowId" :label="t('pendingDelivery.cashflowId')" width="150" />
        <el-table-column prop="paymentInfoId" :label="t('pendingDelivery.paymentInfoId')" width="150" />
        <el-table-column prop="externalNo" :label="t('pendingDelivery.externalNo')" width="190" />
        <el-table-column prop="counterparty" :label="t('pendingDelivery.counterparty')" width="130" />
        <el-table-column :label="t('pendingDelivery.direction')" width="70" align="center">
          <template #default="{ row }">
            <span :class="row.direction === '付' ? 'git-tag-pay' : 'git-tag-recv'">
              {{ row.direction === '付' ? t('pendingDelivery.dirPay') : t('pendingDelivery.dirRecv') }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="currency" :label="t('pendingDelivery.currency')" width="70" align="center" />
        <el-table-column :label="t('pendingDelivery.amount')" width="160" align="right">
          <template #default="{ row }">
            <span class="amount-text">{{ fmtAmt(row.amount) }}</span>
          </template>
        </el-table-column>
        <el-table-column :label="t('pendingDelivery.settlementMethod')" width="130" align="center">
          <template #default="{ row }">{{ settlementLabel(row.settlementMethod) }}</template>
        </el-table-column>
        <el-table-column :label="t('pendingDelivery.clearingMethod')" width="80" align="center">
          <template #default="{ row }">{{ clearingLabel(row.clearingMethod) }}</template>
        </el-table-column>
        <el-table-column prop="paymentDate" :label="t('pendingDelivery.paymentDate')" width="110" align="center" />
        <el-table-column prop="generateDate" :label="t('pendingDelivery.generateDate')" width="110" align="center" />
        <el-table-column :label="t('common.actions')" width="80" fixed="right" align="center">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openDetail(row)">{{ t('common.detail') }}</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-bar">
        <el-pagination v-model:current-page="page" v-model:page-size="pageSize"
          :total="allData.length" :page-sizes="[15,20,30,40,50]"
          layout="total, prev, pager, next, jumper"
          background small />
      </div>
    </div>
  </div>

  <!-- ══ 交割弹窗 ══ -->
  <el-dialog v-model="deliveryVisible" :title="t('pendingDelivery.deliveryTitle')"
    width="720px" :close-on-click-modal="false">
    <el-tabs v-model="deliveryTab" class="dlg-tabs">
      <!-- Tab 1: 收付信息 -->
      <el-tab-pane :label="t('pendingDelivery.tabPaymentInfo')" name="info">
        <div class="dlg-two-col">
          <!-- 左：基本信息 -->
          <div class="dlg-col">
            <div class="dlg-col-title">{{ t('pendingDelivery.basicInfo') }}</div>
            <div class="dlg-field"><span class="dlf-label">{{ t('pendingDelivery.operatingInst') }}：</span><span class="dlf-val">Jakarta Branch</span></div>
            <div class="dlg-field"><span class="dlf-label">{{ t('pendingDelivery.counterparty') }}：</span><span class="dlf-val">{{ deliveryTarget?.counterparty }}</span></div>
            <div class="dlg-field"><span class="dlf-label">{{ t('pendingDelivery.settlementMethod') }}：</span><span class="dlf-val">{{ settlementLabel(deliveryTarget?.settlementMethod) }}</span></div>
            <div class="dlg-field"><span class="dlf-label">{{ t('pendingDelivery.clearingMethod') }}：</span><span class="dlf-val">{{ clearingLabel(deliveryTarget?.clearingMethod) }}</span></div>
            <div class="dlg-field"><span class="dlf-label">{{ t('pendingDelivery.externalNo') }}：</span><span class="dlf-val">{{ deliveryTarget?.externalNo }}</span></div>
          </div>
          <!-- 右：其他信息 + 内部账号 -->
          <div class="dlg-col">
            <div class="dlg-col-title">{{ t('pendingDelivery.otherInfo') }}</div>
            <div class="dlg-field"><span class="dlf-label">{{ t('pendingDelivery.currency') }}：</span><span class="dlf-val">{{ deliveryTarget?.currency }}</span></div>
            <div class="dlg-field"><span class="dlf-label">{{ t('pendingDelivery.amount') }}：</span><span class="dlf-val amount-text">{{ fmtAmt(deliveryTarget?.amount) }}</span></div>
            <div class="dlg-field"><span class="dlf-label">{{ t('pendingDelivery.direction') }}：</span>
              <span :class="deliveryTarget?.direction === '付' ? 'git-tag-pay' : 'git-tag-recv'">
                {{ deliveryTarget?.direction === '付' ? t('pendingDelivery.dirPay') : t('pendingDelivery.dirRecv') }}
              </span>
            </div>
            <div class="dlg-field"><span class="dlf-label">{{ t('pendingDelivery.paymentDate') }}：</span><span class="dlf-val">{{ deliveryTarget?.paymentDate }}</span></div>
            <div class="dlg-field dlg-field--acct">
              <span class="dlf-label dlf-label--required">{{ t('pendingDelivery.internalAcct') }}：</span>
              <el-input v-model="deliveryAcct" :placeholder="t('pendingDelivery.internalAcctPlaceholder')" size="small" style="flex:1" />
              <el-button size="small" :loading="acctQuerying" @click="queryInternalAcct" style="margin-left:4px">
                {{ t('pendingDelivery.queryAcct') }}
              </el-button>
            </div>
            <div v-if="acctInfo" class="acct-info-box" style="margin-top:4px">
              <span class="acct-info-item"><span class="acct-info-label">{{ t('pendingDelivery.acctName') }}</span>{{ acctInfo.name }}</span>
            </div>
            <div class="dlg-field" style="margin-top:8px"><span class="dlf-label">{{ t('pendingDelivery.remark') }}：</span>
              <el-input v-model="deliveryRemark" type="textarea" :rows="2" size="small" :placeholder="t('common.optional')" style="flex:1" />
            </div>
          </div>
        </div>
      </el-tab-pane>
      <!-- Tab 2: 现金流（占位） -->
      <el-tab-pane :label="t('pendingDelivery.tabCashflow')" name="cashflow">
        <div class="dlg-placeholder">{{ t('pendingDelivery.tabCashflowPlaceholder') }}</div>
      </el-tab-pane>
    </el-tabs>
    <template #footer>
      <el-button @click="deliveryVisible = false">{{ t('common.cancel') }}</el-button>
      <el-button type="primary" :disabled="!deliveryAcct.trim()" :loading="deliveryLoading" @click="confirmDelivery">
        {{ deliveryLoading ? t('pendingDelivery.processing') : t('common.confirm') }}
      </el-button>
    </template>
  </el-dialog>

  <!-- ══ 挂账弹窗 ══ -->
  <el-dialog v-model="suspenseVisible" :title="t('pendingDelivery.suspenseTitle')"
    width="680px" :close-on-click-modal="false">
    <div class="dlg-body">

      <!-- 上：收付信息 -->
      <div class="onacct-section-title">{{ t('pendingDelivery.sectionPaymentInfo') }}</div>
      <div class="onacct-grid">
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.paymentInfoId') }}：</span><span class="oa-val">{{ suspenseTarget?.paymentInfoId }}</span></div>
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.paymentDate') }}：</span><span class="oa-val">{{ suspenseTarget?.paymentDate }}</span></div>
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.sendDate') }}：</span><span class="oa-val">{{ suspenseTarget?.generateDate }}</span></div>
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.operatingInst') }}：</span><span class="oa-val">Jakarta Branch</span></div>
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.entity') }}：</span><span class="oa-val">Jakarta</span></div>
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.nettingStatus') }}：</span><span class="oa-val">—</span></div>
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.counterparty') }}：</span><span class="oa-val">{{ suspenseTarget?.counterparty }}</span></div>
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.clearingMethod') }}：</span><span class="oa-val">{{ clearingLabel(suspenseTarget?.clearingMethod) }}</span></div>
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.settlementMethod') }}：</span><span class="oa-val">{{ settlementLabel(suspenseTarget?.settlementMethod) }}</span></div>
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.currency') }}：</span><span class="oa-val">{{ suspenseTarget?.currency }}</span></div>
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.amount') }}：</span><span class="oa-val amount-text">{{ fmtAmt(suspenseTarget?.amount) }}</span></div>
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.direction') }}：</span>
          <span :class="suspenseTarget?.direction === '付' ? 'git-tag-pay' : 'git-tag-recv'">
            {{ suspenseTarget?.direction === '付' ? t('pendingDelivery.dirPay') : t('pendingDelivery.dirRecv') }}
          </span>
        </div>
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.paymentStatus') }}：</span><span class="oa-val">normal</span></div>
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.normalProcStatus') }}：</span><span class="oa-val">over</span></div>
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.cancelProcStatus') }}：</span><span class="oa-val">initial</span></div>
        <div class="oa-item oa-item--span2"><span class="oa-label">{{ t('pendingDelivery.payerSettlePath') }}：</span><span class="oa-val">{{ suspenseTarget?.externalNo }}</span></div>
        <div class="oa-item oa-item--span2"><span class="oa-label">{{ t('pendingDelivery.receiverSettlePath') }}：</span><span class="oa-val">{{ suspenseTarget?.externalNo }}</span></div>
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.generateDate') }}：</span><span class="oa-val">{{ suspenseTarget?.generateDate }}</span></div>
      </div>

      <!-- 下：挂账信息 -->
      <div class="onacct-section-title" style="margin-top:16px">{{ t('pendingDelivery.sectionOnAcct') }}</div>
      <div class="onacct-grid onacct-grid--bottom">
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.currency') }}：</span><span class="oa-val">{{ suspenseTarget?.currency }}</span></div>
        <div class="oa-item"><span class="oa-label">{{ t('pendingDelivery.amount') }}：</span><span class="oa-val amount-text">{{ fmtAmt(suspenseTarget?.amount) }}</span></div>
        <div class="oa-item oa-item--full oa-item--acct">
          <span class="oa-label oa-label--required">{{ t('pendingDelivery.bglAcct') }}：</span>
          <el-input v-model="suspenseAcct" :placeholder="t('pendingDelivery.bglAcctPlaceholder')" size="small" style="flex:1;max-width:240px" />
        </div>
      </div>

    </div>
    <template #footer>
      <el-button @click="suspenseVisible = false">{{ t('common.cancel') }}</el-button>
      <el-button type="primary" :disabled="!suspenseAcct.trim()" :loading="suspenseLoading" @click="confirmSuspense">
        {{ suspenseLoading ? t('pendingDelivery.processing') : t('common.confirm') }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'
import { ArrowDown } from '@element-plus/icons-vue'
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()
const isEn = computed(() => locale.value === 'en-US')
const filterExpanded = ref(false)

// ─── 查询条件 ────────────────────────────────────────────────
const filters = ref({
  cashflowId:      '',
  paymentInfoId:   '',
  externalNo:      '',
  operatingInst:   '',
  counterparty:    '',
  currency:        '',
  clearingMethod:  '',
  settlementMethod:'',
  direction:       '',
  processStatus:   '',
  paymentDate:     [],
  generateDate:    [],
})
function handleQuery() { ElMessage.success(t('common.querySuccess')) }
function handleReset() {
  Object.assign(filters.value, {
    cashflowId:'', paymentInfoId:'', externalNo:'', operatingInst:'',
    counterparty:'', currency:'', clearingMethod:'', settlementMethod:'',
    direction:'', paymentDate:[], generateDate:[],
  })
}

// ─── 分页 ────────────────────────────────────────────────────
const page     = ref(1)
const pageSize = ref(15)

// ─── Mock 数据 ───────────────────────────────────────────────
const allData = ref([
  { seq:1, cashflowId:'CF-2026-00418', paymentInfoId:'PI-2026-00831', externalNo:'20260611041', counterparty:'Bank Mandiri',   direction:'付', currency:'USD', amount:2_500_000,      settlementMethod:'内部账',      clearingMethod:'全额', paymentDate:'2026-06-11', generateDate:'2026-06-10', processStatus:'待交割' },
  { seq:2, cashflowId:'CF-2026-00419', paymentInfoId:'PI-2026-00832', externalNo:'20260611042', counterparty:'BNI Indonesia',  direction:'收', currency:'IDR', amount:38_750_000_000, settlementMethod:'内部账',      clearingMethod:'净额', paymentDate:'2026-06-11', generateDate:'2026-06-10', processStatus:'待交割' },
  { seq:3, cashflowId:'CF-2026-00420', paymentInfoId:'PI-2026-00833', externalNo:'20260612093', counterparty:'DBS Singapore',  direction:'付', currency:'USD', amount:1_000_000,      settlementMethod:'SWIFT+内部账', clearingMethod:'全额', paymentDate:'2026-06-12', generateDate:'2026-06-11', processStatus:'待交割' },
  { seq:4, cashflowId:'CF-2026-00421', paymentInfoId:'PI-2026-00834', externalNo:'20260612055', counterparty:'Bank BCA',       direction:'收', currency:'IDR', amount:15_200_000_000, settlementMethod:'内部账',      clearingMethod:'净额', paymentDate:'2026-06-12', generateDate:'2026-06-11', processStatus:'待交割' },
  { seq:5, cashflowId:'CF-2026-00410', paymentInfoId:'PI-2026-00820', externalNo:'20260609031', counterparty:'Bank Mandiri',   direction:'收', currency:'USD', amount:800_000,        settlementMethod:'内部账',      clearingMethod:'全额', paymentDate:'2026-06-09', generateDate:'2026-06-08', processStatus:'已交割' },
  { seq:6, cashflowId:'CF-2026-00411', paymentInfoId:'PI-2026-00821', externalNo:'20260610038', counterparty:'BRI Indonesia',  direction:'付', currency:'IDR', amount:22_000_000_000, settlementMethod:'内部账',      clearingMethod:'净额', paymentDate:'2026-06-10', generateDate:'2026-06-09', processStatus:'已交割' },
  { seq:7, cashflowId:'CF-2026-00412', paymentInfoId:'PI-2026-00822', externalNo:'20260609033', counterparty:'CIMB Niaga',     direction:'付', currency:'USD', amount:500_000,        settlementMethod:'内部账',      clearingMethod:'全额', paymentDate:'2026-06-09', generateDate:'2026-06-08', processStatus:'已挂账' },
  { seq:8, cashflowId:'CF-2026-00413', paymentInfoId:'PI-2026-00823', externalNo:'20260608021', counterparty:'Bank BTN',       direction:'收', currency:'IDR', amount:8_000_000_000,  settlementMethod:'内部账',      clearingMethod:'净额', paymentDate:'2026-06-08', generateDate:'2026-06-07', processStatus:'交割未明' },
])

const pagedData = computed(() => {
  const start = (page.value - 1) * pageSize.value
  return allData.value.slice(start, start + pageSize.value).map((r, i) => ({ ...r, seq: start + i + 1 }))
})

// ─── 多选 ────────────────────────────────────────────────────
const selectedRows = ref([])

// ─── 工具函数 ────────────────────────────────────────────────
function fmtAmt(val) {
  if (val === undefined || val === null) return ''
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
function statusLabel(s) {
  const map = {
    '待交割': t('pendingDelivery.statusPending'),
    '已交割': t('pendingDelivery.statusDelivered'),
    '已挂账': t('pendingDelivery.statusSuspense'),
    '不入账': t('pendingDelivery.statusNoPost'),
    '交割未明': t('pendingDelivery.statusUnknown'),
  }
  return map[s] || s
}
function statusTagType(s) {
  return { '待交割':'warning', '已交割':'success', '已挂账':'info', '不入账':'info', '交割未明':'danger' }[s] || 'info'
}
function clearingLabel(s) {
  return { '全额': t('pendingDelivery.cmGross'), '净额': t('pendingDelivery.cmNet') }[s] || s
}
function settlementLabel(s) {
  return { '内部账': t('pendingDelivery.smInternal'), 'SWIFT+内部账': t('pendingDelivery.smSwiftInter') }[s] || s
}
function openDetail(row) { ElMessage.info(`Detail: ${row.paymentInfoId}`) }

// ─── 交割 ────────────────────────────────────────────────────
const deliveryVisible = ref(false)
const deliveryTab     = ref('info')
const deliveryTarget  = ref(null)
const deliveryAcct    = ref('')
const deliveryRemark  = ref('')
const deliveryLoading = ref(false)
const acctQuerying    = ref(false)
const acctInfo        = ref(null)

function openDelivery() {
  if (selectedRows.value.length !== 1) return
  deliveryTarget.value  = selectedRows.value[0]
  deliveryAcct.value    = ''
  deliveryRemark.value  = ''
  acctInfo.value        = null
  deliveryTab.value     = 'info'
  deliveryVisible.value = true
}
async function queryInternalAcct() {
  if (!deliveryAcct.value.trim()) { ElMessage.warning(t('pendingDelivery.acctRequired')); return }
  acctQuerying.value = true
  await new Promise(r => setTimeout(r, 900))
  acctQuerying.value = false
  // 模拟核心返回账户信息
  acctInfo.value = { name: 'Jakarta Branch Internal A/C', currency: deliveryTarget.value?.currency, balance: 12_000_000 }
}
async function confirmDelivery() {
  if (!deliveryAcct.value.trim()) return
  deliveryLoading.value = true
  await new Promise(r => setTimeout(r, 1400))
  deliveryLoading.value = false
  deliveryVisible.value = false

  // 模拟核心返回（随机演示三种结果）
  const outcomes = ['success', 'fail', 'unknown']
  const result   = outcomes[Math.floor(Math.random() * 3)]
  const row = deliveryTarget.value

  if (result === 'success') {
    row.processStatus = '已交割'
    ElNotification({ title: t('pendingDelivery.deliverSuccess'), type: 'success', duration: 4000 })
  } else if (result === 'fail') {
    ElNotification({ title: t('pendingDelivery.deliverFail'), message: t('pendingDelivery.deliverFailMsg'), type: 'error', duration: 6000 })
  } else {
    row.processStatus = '交割未明'
    ElNotification({ title: t('pendingDelivery.deliverUnknown'), message: t('pendingDelivery.deliverUnknownMsg'), type: 'warning', duration: 6000 })
  }
  selectedRows.value = []
}

// ─── 挂账 ────────────────────────────────────────────────────
const suspenseVisible = ref(false)
const suspenseTarget  = ref(null)
const suspenseAcct    = ref('')
const suspenseReason  = ref('')
const suspenseLoading = ref(false)

function openSuspense() {
  if (selectedRows.value.length !== 1) return
  suspenseTarget.value  = selectedRows.value[0]
  suspenseAcct.value    = ''
  suspenseReason.value  = ''
  suspenseVisible.value = true
}
async function confirmSuspense() {
  if (!suspenseAcct.value.trim()) return
  suspenseLoading.value = true
  await new Promise(r => setTimeout(r, 1000))
  suspenseLoading.value = false
  suspenseVisible.value = false
  suspenseTarget.value.processStatus = '已挂账'
  ElNotification({ title: t('pendingDelivery.suspenseSubmitted'), message: t('pendingDelivery.suspenseWorkflowMsg'), type: 'success', duration: 5000 })
  selectedRows.value = []
}

// ─── 不入账 ──────────────────────────────────────────────────
async function handleNoPost() {
  if (selectedRows.value.length !== 1) return
  const row = selectedRows.value[0]
  try {
    await ElMessageBox.confirm(
      t('pendingDelivery.noPostConfirmMsg', { id: row.paymentInfoId }),
      t('pendingDelivery.noPostConfirmTitle'),
      { confirmButtonText: t('common.confirm'), cancelButtonText: t('common.cancel'), type: 'warning' }
    )
    row.processStatus = '不入账'
    ElMessage.success(t('pendingDelivery.noPostSuccess'))
    selectedRows.value = []
  } catch { /* cancelled */ }
}
</script>

<style lang="scss" scoped>
.pd-page {
  display: flex; flex-direction: column; gap: 10px; height: 100%;
}

/* ── 查询区 ── */
.filter-bar {
  background: #fff; border: 1px solid var(--git-border); border-radius: 4px;
  padding: 14px 16px; flex-shrink: 0;
}
/* 5列等宽网格 */
.filter-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px 16px;
}
.fg-item {
  display: flex; align-items: center; gap: 8px; min-width: 0;
}
.fg-item--span2 { grid-column: span 2; }
.fg-item--span3 { grid-column: span 3; }
.fg-item--actions { display: flex; align-items: center; gap: 8px; justify-content: flex-end; }
.expand-btn { color: var(--git-primary, #1677ff); padding: 0 4px; }
.expand-icon { margin-left: 2px; transition: transform 0.25s; }
.expand-icon--up { transform: rotate(180deg); }
.fg-label {
  font-size: 13px; color: var(--git-text-2); white-space: nowrap; flex-shrink: 0;
}
.fg-input { flex: 1; min-width: 0; }

/* ── 主卡片 ── */
.table-card {
  flex: 1; background: #fff; border: 1px solid var(--git-border); border-radius: 4px;
  display: flex; flex-direction: column; overflow: hidden; min-height: 0;
}

/* Tabs */
.status-tabs { display: flex; border-bottom: 1px solid var(--git-border); padding: 0 16px; flex-shrink: 0; }
.status-tab {
  display: flex; align-items: center; gap: 6px; padding: 0 14px; height: 44px;
  font-size: 13px; color: var(--git-text-2); cursor: pointer;
  border-bottom: 2px solid transparent; margin-bottom: -1px; white-space: nowrap;
  &:hover { color: var(--git-primary); }
  &.active { color: var(--git-primary); font-weight: 600; border-bottom-color: var(--git-primary); }
}
.tab-count {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 18px; height: 18px; padding: 0 5px; border-radius: 9px;
  font-size: 11px; font-weight: 600;
  &.count-warning { background: #fdf6ec; color: #e6a23c; }
  &.count-success { background: #f0f9eb; color: #67c23a; }
  &.count-info    { background: #ecf5ff; color: #409eff; }
  &.count-danger  { background: #fef0f0; color: #f56c6c; }
}

/* 操作栏 */
.action-bar {
  display: flex; align-items: center; gap: 8px; padding: 10px 16px;
  border-bottom: 1px solid var(--git-border); background: #fafbfc; flex-shrink: 0;
}
.action-bar-right { margin-left: auto; display: flex; align-items: center; gap: 8px; }
.page-size-label  { font-size: 13px; color: var(--git-text-2); }
.selected-hint    { font-size: 13px; color: var(--git-primary); }

/* 表格 */
:deep(.el-table) { flex: 1; font-size: 13px; }
:deep(.el-table .cell) { white-space: nowrap; }
:deep(.el-table .el-table-column--selection .cell) { display: flex; justify-content: center; align-items: center; padding: 0; }
.amount-text { font-family: 'Helvetica Neue', monospace; font-weight: 500; }

/* 分页 */
.pagination-bar {
  display: flex; justify-content: flex-end; padding: 10px 16px;
  border-top: 1px solid var(--git-border); flex-shrink: 0;
}

/* ── 弹窗 ── */
.dlg-body { padding: 0 4px; }
/* 交割弹窗 tabs */
.dlg-tabs { margin-top: -10px; }
.dlg-two-col { display: flex; gap: 16px; min-height: 240px; }
.dlg-col { flex: 1; background: #f9fafb; border: 1px solid #e4e7ed; border-radius: 4px; padding: 12px 14px; }
.dlg-col-title { font-weight: 600; font-size: 13px; color: var(--git-primary, #1677ff); border-bottom: 1px solid #e4e7ed; padding-bottom: 8px; margin-bottom: 10px; }
.dlg-field { display: flex; align-items: flex-start; margin-bottom: 8px; font-size: 13px; line-height: 1.6; }
.dlg-field--acct { align-items: center; }
.dlf-label { color: #606266; white-space: nowrap; min-width: 88px; }
.dlf-label--required::before { content: '* '; color: #f56c6c; }
.dlf-val { color: #303133; word-break: break-all; }
.dlg-placeholder { color: #909399; font-size: 13px; text-align: center; padding: 40px 0; }
/* 挂账弹窗 */
.onacct-section-title { font-weight: 600; font-size: 13px; color: var(--git-primary, #1677ff); background: #f0f5ff; padding: 6px 10px; border-radius: 3px; margin-bottom: 10px; }
.onacct-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px 16px; }
.onacct-grid--bottom { grid-template-columns: repeat(3, 1fr); align-items: center; }
.oa-item { display: flex; align-items: center; font-size: 13px; min-width: 0; }
.oa-item--acct { display: flex; align-items: center; gap: 4px; }
.oa-item--span2 { grid-column: span 2; }
.oa-item--full { grid-column: 1 / -1; }
.oa-label { color: #606266; white-space: nowrap; margin-right: 2px; }
.oa-label--required::before { content: '* '; color: #f56c6c; }
.oa-val { color: #303133; }

.summary-grid {
  background: #f8f9fc; border: 1px solid var(--git-border); border-radius: 4px;
  display: grid; grid-template-columns: 1fr 1fr; overflow: hidden;
  &--en { grid-template-columns: 1fr;
    .sg-row { grid-template-columns: 140px 1fr;
      &:nth-last-child(-n+2) { border-bottom: 1px solid #edf0f7; }
      &:last-child { border-bottom: none; }
    }
  }
}
.sg-row {
  display: grid; grid-template-columns: 100px 1fr;
  border-bottom: 1px solid #edf0f7; min-height: 36px;
  &:nth-last-child(-n+2) { border-bottom: none; }
}
.sg-label {
  display: flex; align-items: center; padding: 6px 12px;
  font-size: 12px; color: #606266; background: #f8f9fc;
  border-right: 1px solid #edf0f7; white-space: nowrap;
}
.sg-val { display: flex; align-items: center; padding: 6px 12px; font-size: 13px; color: #303133; }

.acct-row { display: flex; gap: 8px; }
.acct-info-box {
  margin-top: 8px; padding: 8px 12px; background: #f0f6ff;
  border: 1px solid #c6d9f7; border-radius: 4px;
  display: flex; gap: 24px; font-size: 13px;
}
.acct-info-item { display: flex; align-items: center; gap: 6px; }
.acct-info-label { color: var(--git-text-2); font-size: 12px; }
</style>
