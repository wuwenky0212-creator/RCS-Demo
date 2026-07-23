<template>
  <div class="tax-rule-config">
    <el-tabs v-model="activeProduct" class="product-tabs" @tab-change="handleTabChange">
      <el-tab-pane :label="t('taxRule.bondRulesTab')" name="bond" />
      <el-tab-pane :label="t('taxRule.interbankRulesTab')" name="interbank" />
    </el-tabs>

    <!-- 筛选区 -->
    <div class="filter-bar">
      <div class="filter-fields">
        <div class="filter-item">
          <label class="filter-label">{{ t('taxRule.country') }}</label>
          <el-select v-model="filter.country" :placeholder="t('common.pleaseSelect')" clearable size="default" style="width:150px">
            <el-option :label="t('taxRule.countryID')" value="ID" />
            <el-option :label="t('taxRule.countryCN')" value="CN" />
          </el-select>
        </div>

        <div v-if="activeProduct === 'bond'" class="filter-item">
          <label class="filter-label">{{ t('taxRule.relatedTransactionId') }}</label>
          <el-input
            v-model="filter.relatedTransactionId"
            :placeholder="t('taxRule.relatedTransactionIdPlaceholder')"
            clearable
            style="width:190px"
          />
        </div>

        <div v-if="activeProduct === 'bond'" class="filter-item">
          <label class="filter-label">{{ t('taxRule.bondCode') }}</label>
          <el-select
            v-model="filter.bondCode"
            :placeholder="t('common.pleaseSelect')"
            clearable
            filterable
            style="width:170px"
          >
            <el-option label="019009.SH - 10Y Treasury 09" value="019009.SH" />
            <el-option label="SHYMAL.IB" value="SHYMAL.IB" />
          </el-select>
        </div>

        <div v-if="activeProduct === 'interbank'" class="filter-item">
          <label class="filter-label">{{ t('taxRule.counterpartyTypes') }}</label>
          <el-select
            v-model="filter.counterpartyTypes"
            :placeholder="t('common.pleaseSelect')"
            multiple collapse-tags collapse-tags-tooltip
            clearable size="default" style="width:180px"
          >
            <el-option :label="t('taxRule.cpDomesticBank')" value="domestic_bank" />
            <el-option :label="t('taxRule.cpForeignFI')"    value="foreign_fi" />
            <el-option :label="t('taxRule.cpCentralBank')"  value="central_bank" />
            <el-option :label="t('taxRule.cpCorporate')"    value="corporate" />
          </el-select>
        </div>

        <div class="filter-item">
          <label class="filter-label">{{ t('taxRule.isActive') }}</label>
          <el-select v-model="filter.isActive" :placeholder="t('common.pleaseSelect')" clearable size="default" style="width:120px">
            <el-option :label="t('taxRule.active')" value="true" />
            <el-option :label="t('taxRule.inactive')" value="false" />
          </el-select>
        </div>
      </div>

      <div class="filter-actions">
        <el-button type="primary" :icon="Search" size="default" @click="loadData">{{ t('common.query') }}</el-button>
        <el-button :icon="Refresh" size="default" @click="resetFilter">{{ t('common.reset') }}</el-button>
        <el-button :icon="Upload" size="default" @click="triggerImport">{{ t('taxRule.importBtn') }}</el-button>
        <el-button :icon="Download" size="default" @click="handleExport">{{ t('taxRule.exportBtn') }}</el-button>
        <el-button type="primary" :icon="Plus" size="default" @click="openCreate" class="btn-add">{{ t('taxRule.addBtn') }}</el-button>
        <input
          ref="importFileInput"
          type="file"
          accept=".xlsx,.xls"
          hidden
          @change="handleImport"
        >
      </div>
    </div>

    <!-- 表格 -->
    <el-table
      :data="tableData"
      v-loading="loading"
      border
      stripe
      size="small"
      style="width:100%"
      class="rule-table"
    >
      <el-table-column
        prop="id"
        :label="t('taxRule.ruleId')"
        width="130"
        fixed
        class-name="rule-id-column"
        label-class-name="rule-id-column"
      />

      <el-table-column :label="t('taxRule.isActive')" width="90" align="center">
        <template #default="{ row }">
          <el-checkbox
            :model-value="row.isActive"
            @change="handleToggle(row)"
          />
        </template>
      </el-table-column>

      <el-table-column prop="effectiveDate" :label="t('taxRule.effectiveDate')" width="110" />
      <el-table-column prop="expiryDate" :label="t('taxRule.expiryDate')" width="110" />
      <el-table-column :label="t('taxRule.country')" width="100">
        <template #default="{ row }">{{ COUNTRY_MAP[row.country] || row.country }}</template>
      </el-table-column>

      <el-table-column v-if="activeProduct === 'bond'" :label="t('taxRule.bondCode')" width="140">
        <template #default="{ row }">{{ row.bondCode || '—' }}</template>
      </el-table-column>

      <el-table-column v-if="activeProduct === 'bond'" :label="t('taxRule.relatedTransactionId')" width="160">
        <template #default="{ row }">{{ row.relatedTransactionId || '—' }}</template>
      </el-table-column>

      <el-table-column v-if="activeProduct === 'bond'" :label="t('taxRule.acquisitionPrice')" width="120" align="right">
        <template #default="{ row }">
          {{ row.acquisitionPrice == null ? '—' : row.acquisitionPrice.toFixed(4) }}
        </template>
      </el-table-column>

      <el-table-column v-if="activeProduct === 'interbank'" :label="t('taxRule.counterpartyTypes')" width="120">
        <template #default="{ row }">{{ (row.counterpartyTypes || []).map(ct => CPTY_MAP[ct] || ct).join(', ') }}</template>
      </el-table-column>

      <el-table-column prop="taxRate" :label="t('taxRule.taxRate')" width="90" align="right">
        <template #default="{ row }">{{ row.taxRate.toFixed(4) }}</template>
      </el-table-column>

      <el-table-column :label="t('taxRule.settlementHandling')" width="150">
        <template #default="{ row }">{{ SETTLEMENT_HANDLING_MAP[row.settlementHandling] || row.settlementHandling }}</template>
      </el-table-column>

      <el-table-column :label="t('taxRule.accountingHandling')" width="120">
        <template #default="{ row }">{{ ACCOUNTING_HANDLING_MAP[row.accountingHandling] || row.accountingHandling }}</template>
      </el-table-column>

      <el-table-column
        :label="t('common.actions')"
        width="160"
        fixed="right"
        align="center"
        class-name="operation-column"
        label-class-name="operation-column"
      >
        <template #default="{ row }">
          <el-button link type="primary" size="small" @click="openEdit(row)">{{ t('common.edit') }}</el-button>
          <el-divider direction="vertical" />
          <el-button link type="primary" size="small" @click="openCopy(row)">{{ t('common.copy') }}</el-button>
          <el-divider direction="vertical" />
          <el-button link type="danger" size="small" @click="handleDelete(row)">{{ t('common.delete') }}</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增 / 编辑 / 复制 对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="480px"
      class="tax-rule-dialog"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="formRules"
        :label-width="locale === 'en-US' ? 'auto' : '130px'"
        :label-position="locale === 'en-US' ? 'top' : 'right'"
        size="default"
      >
        <el-row>
          <el-col :span="24">
            <el-form-item :label="t('taxRule.country')" prop="country">
              <el-select v-model="form.country" :placeholder="t('common.pleaseSelect')" style="width:100%">
                <el-option :label="t('taxRule.countryID')" value="ID" />
                <el-option :label="t('taxRule.countryCN')" value="CN" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item :label="t('taxRule.productCategory')" prop="productCategory">
              <el-select
                v-model="form.productCategory"
                :placeholder="t('common.pleaseSelect')"
                style="width:100%"
                disabled
              >
                <el-option :label="t('taxRule.productBond')" value="bond" />
                <el-option :label="t('taxRule.productInterbank')" value="interbank" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col v-if="form.productCategory === 'bond'" :span="24">
            <el-form-item :label="t('taxRule.bondCode')" prop="bondCode">
              <el-select v-model="form.bondCode" :placeholder="t('taxRule.optionalPlaceholder')" clearable filterable style="width:100%">
                <el-option label="019009.SH - 10Y Treasury 09" value="019009.SH" />
                <el-option label="SHYMAL.IB" value="SHYMAL.IB" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col v-if="form.productCategory === 'bond'" :span="24">
            <el-form-item :label="t('taxRule.relatedTransactionId')" prop="relatedTransactionId">
              <el-input
                v-model="form.relatedTransactionId"
                :placeholder="t('taxRule.relatedTransactionIdPlaceholder')"
                clearable
              />
            </el-form-item>
          </el-col>
          <el-col v-if="form.productCategory === 'bond'" :span="24">
            <el-form-item :label="t('taxRule.acquisitionPrice')" prop="acquisitionPrice">
              <el-input-number
                v-model="form.acquisitionPrice"
                :min="0.0001"
                :precision="4"
                :step="0.01"
                controls-position="right"
                style="width:100%"
              />
            </el-form-item>
          </el-col>
          <el-col v-if="form.productCategory === 'interbank'" :span="24">
            <el-form-item :label="t('taxRule.counterpartyTypes')" prop="counterpartyTypes">
              <el-select v-model="form.counterpartyTypes" :placeholder="t('common.pleaseSelect')" multiple collapse-tags collapse-tags-tooltip style="width:100%">
                <el-option :label="t('taxRule.cpDomesticBank')" value="domestic_bank" />
                <el-option :label="t('taxRule.cpForeignFI')"    value="foreign_fi" />
                <el-option :label="t('taxRule.cpCentralBank')"  value="central_bank" />
                <el-option :label="t('taxRule.cpCorporate')"    value="corporate" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item :label="t('taxRule.taxRate')" prop="taxRate">
              <el-input-number
                v-model="form.taxRate"
                :min="0"
                :max="100"
                :precision="4"
                style="width:100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item :label="t('taxRule.effectiveDate')" prop="effectiveDate">
              <el-date-picker
                v-model="form.effectiveDate"
                type="date"
                :placeholder="t('common.pleaseSelect')"
                value-format="YYYY-MM-DD"
                style="width:100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item :label="t('taxRule.expiryDate')" prop="expiryDate">
              <el-date-picker
                v-model="form.expiryDate"
                type="date"
                :placeholder="t('common.pleaseSelect')"
                value-format="YYYY-MM-DD"
                :disabled-date="disableExpiryDate"
                style="width:100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item :label="t('taxRule.settlementHandling')" prop="settlementHandling">
              <el-select v-model="form.settlementHandling" :placeholder="t('common.pleaseSelect')" disabled style="width:100%">
                <el-option :label="t('taxRule.settlementNoImpact')" value="no_impact" />
                <el-option :label="t('taxRule.settlementImpact')" value="impact" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item :label="t('taxRule.accountingHandling')" prop="accountingHandling">
              <el-select v-model="form.accountingHandling" :placeholder="t('common.pleaseSelect')" disabled style="width:100%">
                <el-option :label="t('taxRule.accountingNoPosting')" value="no_posting" />
                <el-option :label="t('taxRule.accountingPosting')" value="posting" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item :label="t('taxRule.isActive')">
              <el-checkbox v-model="form.isActive">{{ t('taxRule.effectiveLabel') }}</el-checkbox>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">{{ t('common.cancel') }}</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">{{ t('common.save') }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { Search, Refresh, Plus, Upload, Download } from '@element-plus/icons-vue'
import * as XLSX from 'xlsx'

const { t, locale } = useI18n()
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  listTaxRules,
  createTaxRule,
  updateTaxRule,
  toggleTaxRule,
  deleteTaxRule,
} from '@/api/basedata'

// ─── 响应式映射（跟随语言切换） ────────────────────────────────────────────────
const COUNTRY_MAP = computed(() => ({
  ID: t('taxRule.countryID'),
  CN: t('taxRule.countryCN'),
}))
const CPTY_MAP = computed(() => ({
  domestic_bank: t('taxRule.cpDomesticBank'),
  foreign_fi: t('taxRule.cpForeignFI'),
  central_bank: t('taxRule.cpCentralBank'),
  corporate: t('taxRule.cpCorporate'),
}))
const SETTLEMENT_HANDLING_MAP = computed(() => ({
  no_impact: t('taxRule.settlementNoImpact'),
  impact: t('taxRule.settlementImpact'),
}))
const ACCOUNTING_HANDLING_MAP = computed(() => ({
  no_posting: t('taxRule.accountingNoPosting'),
  posting: t('taxRule.accountingPosting'),
}))
// ─── 筛选 ────────────────────────────────────────────────────────────────────
const activeProduct = ref('bond')

const filter = reactive({
  country: '',
  relatedTransactionId: '',
  bondCode: '',
  counterpartyTypes: [],
  isActive: '',
})

function resetFilter() {
  Object.assign(filter, {
    country: '',
    relatedTransactionId: '',
    bondCode: '',
    counterpartyTypes: [],
    isActive: '',
  })
  loadData()
}

function handleTabChange() {
  dialogVisible.value = false
  filter.relatedTransactionId = ''
  filter.bondCode = ''
  filter.counterpartyTypes = []
  loadData()
}

// ─── 表格数据 ─────────────────────────────────────────────────────────────────
const tableData = ref([])
const loading = ref(false)

async function loadData() {
  loading.value = true
  try {
    const params = {}
    if (filter.country)                    params.country = filter.country
    params.productCategory = activeProduct.value
    if (activeProduct.value === 'bond' && filter.relatedTransactionId) {
      params.relatedTransactionId = filter.relatedTransactionId.trim()
    }
    if (activeProduct.value === 'bond' && filter.bondCode) {
      params.bondCode = filter.bondCode
    }
    if (activeProduct.value === 'interbank' && filter.counterpartyTypes.length) {
      params.counterpartyTypes = filter.counterpartyTypes.join(',')
    }
    if (filter.isActive)                   params.isActive = filter.isActive

    const res = await listTaxRules(params)
    tableData.value = res.items ?? []
  } catch (e) {
    ElMessage.error('加载数据失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

onMounted(loadData)

// ─── Excel 导入 / 导出 ───────────────────────────────────────────────────────
const importFileInput = ref(null)

function triggerImport() {
  importFileInput.value?.click()
}

function exportHeaders() {
  const commonHeaders = [
    t('taxRule.country'),
    t('taxRule.taxRate'),
    t('taxRule.effectiveDate'),
    t('taxRule.expiryDate'),
    t('taxRule.isActive'),
    t('taxRule.settlementHandling'),
    t('taxRule.accountingHandling'),
  ]
  return activeProduct.value === 'bond'
    ? [
        t('taxRule.ruleId'),
        ...commonHeaders.slice(0, 1),
        t('taxRule.bondCode'),
        t('taxRule.relatedTransactionId'),
        t('taxRule.acquisitionPrice'),
        ...commonHeaders.slice(1),
      ]
    : [
        t('taxRule.ruleId'),
        ...commonHeaders.slice(0, 1),
        t('taxRule.counterpartyTypes'),
        ...commonHeaders.slice(1),
      ]
}

function exportRow(row) {
  const commonValues = [
    row.country,
    row.taxRate,
    row.effectiveDate,
    row.expiryDate,
    row.isActive ? 'true' : 'false',
    row.settlementHandling,
    row.accountingHandling,
  ]
  return activeProduct.value === 'bond'
    ? [
        row.id,
        ...commonValues.slice(0, 1),
        row.bondCode || '',
        row.relatedTransactionId || '',
        row.acquisitionPrice ?? '',
        ...commonValues.slice(1),
      ]
    : [
        row.id,
        ...commonValues.slice(0, 1),
        (row.counterpartyTypes || []).join(','),
        ...commonValues.slice(1),
      ]
}

function handleExport() {
  const sheet = XLSX.utils.aoa_to_sheet([
    exportHeaders(),
    ...tableData.value.map(exportRow),
  ])
  sheet['!cols'] = exportHeaders().map(header => ({
    wch: Math.max(14, String(header).length * 2),
  }))
  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(
    workbook,
    sheet,
    activeProduct.value === 'bond' ? 'Bond Tax Rules' : 'Interbank Tax Rules',
  )
  const date = new Date().toISOString().slice(0, 10)
  XLSX.writeFile(
    workbook,
    `${activeProduct.value === 'bond' ? '债券' : '拆借'}税费规则_${date}.xlsx`,
  )
  ElMessage.success(t('taxRule.exportSuccess'))
}

function readImportValue(row, ...keys) {
  for (const key of keys) {
    if (row[key] !== undefined && row[key] !== null && row[key] !== '') return row[key]
  }
  return ''
}

function normalizeDate(value) {
  if (typeof value === 'number') return XLSX.SSF.format('yyyy-mm-dd', value)
  const text = String(value || '').trim().replace(/\//g, '-')
  const match = text.match(/^(\d{4})-(\d{1,2})-(\d{1,2})/)
  if (!match) return text
  return `${match[1]}-${match[2].padStart(2, '0')}-${match[3].padStart(2, '0')}`
}

function normalizeActive(value) {
  const text = String(value ?? '').trim().toLowerCase()
  return !['false', '0', '否', '未生效', 'inactive'].includes(text)
}

function parseImportRow(row, index) {
  const country = String(readImportValue(row, '国家/地区', 'Country / Region', 'country')).trim()
  const taxRateRaw = readImportValue(row, '税率(%)', 'Tax Rate (%)', 'taxRate')
  const effectiveDate = normalizeDate(
    readImportValue(row, '生效日期', 'Effective Date', 'effectiveDate') || getSystemDate(),
  )
  const expiryDate = normalizeDate(
    readImportValue(row, '失效日期', 'Expiry Date', 'expiryDate') || '2099-12-30',
  )

  const required = [
    [country, t('taxRule.country')],
    [taxRateRaw !== '', t('taxRule.taxRate')],
    [effectiveDate, t('taxRule.effectiveDate')],
    [expiryDate, t('taxRule.expiryDate')],
  ]

  const payload = {
    country,
    productCategory: activeProduct.value,
    bondCategory: null,
    bondCode: null,
    relatedTransactionId: null,
    acquisitionPrice: null,
    counterpartyTypes: [],
    direction: 'pay',
    taxRate: Number(taxRateRaw),
    settlementHandling: 'impact',
    accountingHandling: activeProduct.value === 'bond' ? 'posting' : 'no_posting',
    effectiveDate,
    expiryDate,
    isActive: normalizeActive(readImportValue(row, '是否生效', 'Active', 'isActive')),
  }

  if (activeProduct.value === 'bond') {
    payload.bondCode = String(readImportValue(row, '债券代码', 'Bond Code', 'bondCode')).trim() || null
    payload.relatedTransactionId = String(
      readImportValue(row, '关联交易流水号', 'Related Transaction ID', 'relatedTransactionId'),
    ).trim()
    const price = readImportValue(row, '购入价格', 'Acquisition Price', 'acquisitionPrice')
    payload.acquisitionPrice = Number(price)
    required.push(
      [payload.relatedTransactionId, t('taxRule.relatedTransactionId')],
      [price !== '' && Number(price) > 0, t('taxRule.acquisitionPrice')],
    )
  } else {
    const counterparties = String(
      readImportValue(row, '交易对手分类', 'Counterparty Type', 'counterpartyTypes'),
    ).trim()
    payload.counterpartyTypes = counterparties
      ? counterparties.split(/[,，;]/).map(item => item.trim()).filter(Boolean)
      : []
  }

  const invalid = required.find(([valid]) => !valid)
  if (invalid || Number.isNaN(payload.taxRate)) {
    const field = invalid?.[1] || t('taxRule.taxRate')
    throw new Error(t('taxRule.importInvalid', { row: index + 2, field }))
  }
  return payload
}

async function handleImport(event) {
  const file = event.target.files?.[0]
  event.target.value = ''
  if (!file) return

  try {
    const workbook = XLSX.read(await file.arrayBuffer(), { type: 'array' })
    const worksheet = workbook.Sheets[workbook.SheetNames[0]]
    const rows = XLSX.utils.sheet_to_json(worksheet, { defval: '', raw: true })
    if (!rows.length) throw new Error(t('taxRule.importEmpty'))

    const payloads = rows.map(parseImportRow)
    for (const payload of payloads) await createTaxRule(payload)

    ElMessage.success(t('taxRule.importSuccess', { count: payloads.length }))
    await loadData()
  } catch (error) {
    ElMessage.error(error?.message || t('taxRule.importEmpty'))
  }
}

// ─── 是否生效切换 ─────────────────────────────────────────────────────────────
async function handleToggle(row) {
  try {
    const updated = await toggleTaxRule(row.id)
    row.isActive = updated.isActive
    ElMessage.success(updated.isActive ? '已设为生效' : '已设为未生效')
  } catch {
    ElMessage.error('切换失败')
  }
}

// ─── 删除 ─────────────────────────────────────────────────────────────────────
async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(
      `确认删除规则「${row.id}」？此操作不可撤销。`,
      '删除确认',
      { type: 'warning', confirmButtonText: '删除', cancelButtonText: '取消', confirmButtonClass: 'el-button--danger' }
    )
    await deleteTaxRule(row.id)
    ElMessage.success('已删除')
    loadData()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

// ─── 对话框 ───────────────────────────────────────────────────────────────────
const dialogVisible = ref(false)
const dialogMode = ref('create')   // 'create' | 'edit' | 'copy'
const editId = ref(null)
const saving = ref(false)
const formRef = ref(null)

const dialogTitle = computed(() => ({
  create: t('taxRule.dialogCreate'),
  edit: t('taxRule.dialogEdit'),
  copy: t('taxRule.dialogCopy'),
}[dialogMode.value]))

function getSystemDate() {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const emptyForm = () => ({
  country: 'ID',
  productCategory: activeProduct.value,
  bondCode: '',
  relatedTransactionId: '',
  acquisitionPrice: null,
  counterpartyTypes: [],
  direction: 'pay',
  taxRate: 0,
  settlementHandling: 'impact',
  accountingHandling: activeProduct.value === 'interbank' ? 'no_posting' : 'posting',
  effectiveDate: getSystemDate(),
  expiryDate: '2099-12-30',
  isActive: true,
  sourceId: null,
})

const form = reactive(emptyForm())

watch(() => form.effectiveDate, (effectiveDate) => {
  if (effectiveDate && form.expiryDate && form.expiryDate < effectiveDate) {
    form.expiryDate = ''
  }
})

function disableExpiryDate(date) {
  if (!form.effectiveDate) return false
  const start = new Date(`${form.effectiveDate}T00:00:00`)
  return date.getTime() < start.getTime()
}

function validateExpiryDate(_rule, value, callback) {
  if (!value) return callback(new Error('请选择失效日期'))
  if (form.effectiveDate && value < form.effectiveDate) {
    return callback(new Error('失效日期不能早于生效日期'))
  }
  callback()
}

const formRules = {
  country:          [{ required: true, message: '请选择国家/地区' }],
  productCategory:  [{ required: true, message: '请选择产品类别' }],
  relatedTransactionId: [{ required: true, message: '请输入关联交易流水号' }],
  acquisitionPrice: [{ required: true, message: '请输入购入价格' }],
  taxRate:          [{ required: true, message: '请输入税率' }],
  settlementHandling: [{ required: true, message: '请选择结算处理方式' }],
  accountingHandling: [{ required: true, message: '请选择记账处理方式' }],
  effectiveDate:    [{ required: true, message: '请选择生效日期' }],
  expiryDate:       [{ required: true, validator: validateExpiryDate, trigger: 'change' }],
}

function fillForm(src) {
  Object.assign(form, {
    country:          src.country,
    productCategory:  src.productCategory,
    bondCode:         src.bondCode || '',
    relatedTransactionId: src.relatedTransactionId || '',
    acquisitionPrice: src.acquisitionPrice ?? null,
    counterpartyTypes: src.productCategory === 'bond' ? [] : (Array.isArray(src.counterpartyTypes) ? [...src.counterpartyTypes] : (src.counterpartyType ? [src.counterpartyType] : [])),
    taxRate:          src.taxRate,
    settlementHandling: 'impact',
    accountingHandling: src.productCategory === 'bond' ? 'posting' : 'no_posting',
    effectiveDate:    src.effectiveDate,
    expiryDate:       src.expiryDate,
    isActive:         src.isActive,
  })
}

function openCreate() {
  Object.assign(form, emptyForm())
  dialogMode.value = 'create'
  editId.value = null
  dialogVisible.value = true
}

function openEdit(row) {
  fillForm(row)
  dialogMode.value = 'edit'
  editId.value = row.id
  dialogVisible.value = true
}

function openCopy(row) {
  fillForm(row)
  form.effectiveDate = getSystemDate()
  form.expiryDate = '2099-12-30'
  form.sourceId = row.id
  dialogMode.value = 'copy'
  editId.value = null
  dialogVisible.value = true
}

async function handleSave() {
  await formRef.value.validate()
  saving.value = true
  try {
    const payload = {
      country:          form.country,
      productCategory:  form.productCategory,
      bondCategory:     null,
      bondCode:         form.bondCode || null,
      relatedTransactionId: form.relatedTransactionId || null,
      acquisitionPrice: form.acquisitionPrice,
      counterpartyTypes: form.productCategory === 'bond' ? [] : form.counterpartyTypes,
      direction:        'pay',
      taxRate:          form.taxRate,
      settlementHandling: 'impact',
      accountingHandling: form.productCategory === 'bond' ? 'posting' : 'no_posting',
      effectiveDate:    form.effectiveDate,
      expiryDate:       form.expiryDate,
      isActive:         form.isActive,
    }
    if (dialogMode.value === 'edit') {
      await updateTaxRule(editId.value, payload)
      ElMessage.success('保存成功')
    } else {
      if (form.sourceId) payload.sourceId = form.sourceId
      await createTaxRule(payload)
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
    loadData()
  } catch {
    ElMessage.error('保存失败，请稍后重试')
  } finally {
    saving.value = false
  }
}
</script>

<style lang="scss" scoped>
.tax-rule-config {
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: 100%;
}

.product-tabs {
  flex-shrink: 0;
  background: var(--git-surface);
  padding: 0 16px;
  border: 1px solid var(--git-border);
  border-radius: 4px;
}

:deep(.product-tabs .el-tabs__header) {
  margin: 0;
}

:deep(.product-tabs .el-tabs__nav-wrap::after) {
  height: 1px;
}

.filter-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  background: var(--git-surface);
  border: 1px solid var(--git-border);
  border-radius: 4px;
  padding: 14px 16px;
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
}

.btn-add {
  margin-left: 8px;
}

.rule-table {
  flex: 1;
  border-radius: 6px;
  overflow: hidden;
}

/* 英文 label-position=top 时适当减小行间距，保持弹窗紧凑 */
:deep(.el-form--label-top .el-form-item) {
  margin-bottom: 14px;
}
:deep(.el-form--label-top .el-form-item__label) {
  padding-bottom: 4px;
  line-height: 1.4;
  font-size: 13px;
  color: var(--git-text-2);
}

:deep(.el-table .cell) {
  white-space: nowrap;
}

:deep(.rule-id-column .cell) {
  padding-left: 18px;
}

/* 操作列始终紧贴表格右侧，不随横向滚动偏移 */
:deep(.el-table-fixed-column--right.operation-column) {
  right: 0 !important;
  z-index: 4;
}

:deep(.el-table__fixed-right) {
  right: 0 !important;
}

:global(.tax-rule-dialog) {
  max-width: calc(100vw - 32px);
}

:global(.tax-rule-dialog .el-dialog__header) {
  padding: 14px 18px 10px;
  margin-right: 0;
}

:global(.tax-rule-dialog .el-dialog__body) {
  padding: 8px 18px 4px;
}

:global(.tax-rule-dialog .el-dialog__footer) {
  padding: 8px 18px 14px;
}

:global(.tax-rule-dialog .el-form-item) {
  margin-bottom: 10px;
}

:global(.tax-rule-dialog .el-form-item__label) {
  padding-right: 12px;
}

</style>
