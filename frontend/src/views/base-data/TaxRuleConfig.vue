<template>
  <div class="tax-rule-config">
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

        <div class="filter-item">
          <label class="filter-label">{{ t('taxRule.productCategory') }}</label>
          <el-select v-model="filter.productCategory" :placeholder="t('common.pleaseSelect')" clearable size="default" style="width:130px">
            <el-option :label="t('taxRule.productBond')" value="bond" />
            <el-option :label="t('taxRule.productInterbank')" value="interbank" />
          </el-select>
        </div>

        <div class="filter-item">
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
        <el-button type="primary" :icon="Plus" size="default" @click="openCreate" class="btn-add">{{ t('taxRule.addBtn') }}</el-button>
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
      <el-table-column prop="id" :label="t('taxRule.ruleId')" width="130" fixed />

      <el-table-column :label="t('taxRule.isActive')" width="90" align="center">
        <template #default="{ row }">
          <el-checkbox
            :model-value="row.isActive"
            @change="handleToggle(row)"
          />
        </template>
      </el-table-column>

      <el-table-column prop="effectiveDate" :label="t('taxRule.effectiveDate')" width="110" />
      <el-table-column :label="t('taxRule.country')" width="100">
        <template #default="{ row }">{{ COUNTRY_MAP[row.country] || row.country }}</template>
      </el-table-column>

      <el-table-column :label="t('taxRule.productCategory')" width="110">
        <template #default="{ row }">{{ PRODUCT_MAP[row.productCategory] || row.productCategory }}</template>
      </el-table-column>

      <el-table-column :label="t('taxRule.bondCategory')" width="110">
        <template #default="{ row }">{{ row.bondCategory || '—' }}</template>
      </el-table-column>

      <el-table-column :label="t('taxRule.counterpartyTypes')" width="120">
        <template #default="{ row }">{{ (row.counterpartyTypes || []).map(ct => CPTY_MAP[ct] || ct).join(', ') }}</template>
      </el-table-column>

      <el-table-column prop="taxRate" :label="t('taxRule.taxRate')" width="90" align="right">
        <template #default="{ row }">{{ row.taxRate.toFixed(4) }}</template>
      </el-table-column>

      <el-table-column :label="t('taxRule.taxBase')" width="120">
        <template #default="{ row }">{{ TAX_BASE_MAP[row.taxBase] || row.taxBase }}</template>
      </el-table-column>

      <el-table-column :label="t('taxRule.settlementImpact')" width="100">
        <template #default="{ row }">{{ SETTLE_MAP[row.settlementImpact] || row.settlementImpact }}</template>
      </el-table-column>

      <el-table-column :label="t('taxRule.taxTiming')" min-width="130">
        <template #default="{ row }">
          {{ TAX_TIMING_BASE_MAP[row.taxTimingBase] || row.taxTimingBase }} T+{{ row.taxTimingOffset }}
        </template>
      </el-table-column>

      <el-table-column :label="t('common.actions')" width="160" fixed="right" align="center">
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
      width="620px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="formRules"
        :label-width="locale === 'en-US' ? 'auto' : '110px'"
        :label-position="locale === 'en-US' ? 'top' : 'right'"
        size="default"
      >
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item :label="t('taxRule.country')" prop="country">
              <el-select v-model="form.country" :placeholder="t('common.pleaseSelect')" style="width:100%">
                <el-option :label="t('taxRule.countryID')" value="ID" />
                <el-option :label="t('taxRule.countryCN')" value="CN" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="t('taxRule.productCategory')" prop="productCategory">
              <el-select v-model="form.productCategory" :placeholder="t('common.pleaseSelect')" style="width:100%">
                <el-option :label="t('taxRule.productBond')" value="bond" />
                <el-option :label="t('taxRule.productInterbank')" value="interbank" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="t('taxRule.bondCategory')">
              <el-select v-model="form.bondCategory" :placeholder="t('taxRule.bondCategoryPlaceholder')" clearable style="width:100%">
                <el-option :label="t('taxRule.bondGovt')"        value="国债" />
                <el-option :label="t('taxRule.bondLocalGovt')"   value="地方政府债" />
                <el-option :label="t('taxRule.bondPolicyBank')"  value="政策性金融债" />
                <el-option :label="t('taxRule.bondCommercial')"  value="商业银行债" />
                <el-option :label="t('taxRule.bondCorp')"        value="企业债" />
                <el-option :label="t('taxRule.bondConvertible')" value="可转债" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item :label="t('taxRule.counterpartyTypes')" prop="counterpartyTypes">
              <el-select v-model="form.counterpartyTypes" :placeholder="t('common.pleaseSelect')" multiple collapse-tags collapse-tags-tooltip style="width:100%">
                <el-option :label="t('taxRule.cpDomesticBank')" value="domestic_bank" />
                <el-option :label="t('taxRule.cpForeignFI')"    value="foreign_fi" />
                <el-option :label="t('taxRule.cpCentralBank')"  value="central_bank" />
                <el-option :label="t('taxRule.cpCorporate')"    value="corporate" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
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
          <el-col :span="12">
            <el-form-item :label="t('taxRule.taxBase')" prop="taxBase">
              <el-select v-model="form.taxBase" :placeholder="t('common.pleaseSelect')" style="width:100%">
                <el-option :label="t('taxRule.taxBaseAccrued')"  value="accrued_interest" />
                <el-option :label="t('taxRule.taxBaseCapitalGains')" value="capital_gains" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
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
          <el-col :span="12">
            <el-form-item :label="t('taxRule.settlementImpact')" prop="settlementImpact">
              <el-select v-model="form.settlementImpact" :placeholder="t('common.pleaseSelect')" style="width:100%">
                <el-option :label="t('taxRule.settlementNet')"        value="net_deduct" />
                <el-option :label="t('taxRule.settlementStandalone')" value="standalone" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item :label="t('taxRule.taxTiming')" prop="taxTimingBase" required>
              <el-select v-model="form.taxTimingBase" :placeholder="t('taxRule.baseDay')" style="width:140px">
                <el-option :label="t('taxRule.timingTradeDate')"    value="trade_date" />
                <el-option :label="t('taxRule.timingValueDate')"    value="value_date" />
                <el-option :label="t('taxRule.timingCouponDate')"   value="coupon_date" />
                <el-option :label="t('taxRule.timingMaturityDate')" value="maturity_date" />
              </el-select>
              <span style="margin:0 8px;color:var(--git-text-2)">T +</span>
              <el-input-number
                v-model="form.taxTimingOffset"
                :min="0"
                :max="365"
                :precision="0"
                style="width:100px"
              />
              <span style="margin-left:6px;color:var(--git-text-3);font-size:12px">{{ t('common.days') }}</span>
            </el-form-item>
          </el-col>
          <el-col :span="12">
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { Search, Refresh, Plus } from '@element-plus/icons-vue'

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
const PRODUCT_MAP = computed(() => ({
  bond: t('taxRule.productBond'),
  interbank: t('taxRule.productInterbank'),
}))
const CPTY_MAP = computed(() => ({
  domestic_bank: t('taxRule.cpDomesticBank'),
  foreign_fi: t('taxRule.cpForeignFI'),
  central_bank: t('taxRule.cpCentralBank'),
  corporate: t('taxRule.cpCorporate'),
}))
const TAX_BASE_MAP = computed(() => ({
  accrued_interest: t('taxRule.taxBaseAccrued'),
  capital_gains: t('taxRule.taxBaseCapitalGains'),
}))
const SETTLE_MAP = computed(() => ({
  net_deduct: t('taxRule.settlementNet'),
  standalone: t('taxRule.settlementStandalone'),
}))
const TAX_TIMING_BASE_MAP = computed(() => ({
  trade_date: t('taxRule.timingTradeDate'),
  value_date: t('taxRule.timingValueDate'),
  coupon_date: t('taxRule.timingCouponDate'),
  maturity_date: t('taxRule.timingMaturityDate'),
}))

// ─── 筛选 ────────────────────────────────────────────────────────────────────
const filter = reactive({
  country: '',
  productCategory: '',
  counterpartyTypes: [],
  isActive: '',
})

function resetFilter() {
  Object.assign(filter, {
    country: '',
    productCategory: '',
    counterpartyTypes: [],
    isActive: '',
  })
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
    if (filter.productCategory)            params.productCategory = filter.productCategory
    if (filter.counterpartyTypes.length)   params.counterpartyTypes = filter.counterpartyTypes.join(',')
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

const emptyForm = () => ({
  country: 'ID',
  productCategory: '',
  bondCategory: '',
  counterpartyTypes: [],
  direction: 'pay',
  taxRate: 0,
  taxBase: '',
  settlementImpact: 'net_deduct',
  taxTimingBase: 'value_date',
  taxTimingOffset: 0,
  effectiveDate: '',
  isActive: true,
  sourceId: null,
})

const form = reactive(emptyForm())

const formRules = {
  country:          [{ required: true, message: '请选择国家/地区' }],
  productCategory:  [{ required: true, message: '请选择产品类别' }],
  counterpartyTypes: [{ required: true, type: 'array', min: 1, message: '请选择至少一个对手方类型' }],
  taxRate:          [{ required: true, message: '请输入税率' }],
  taxBase:          [{ required: true, message: '请选择税基' }],
  settlementImpact: [{ required: true, message: '请选择结算影响' }],
  taxTimingBase:    [{ required: true, message: '请选择税费交收基准日' }],
  effectiveDate:    [{ required: true, message: '请选择生效日期' }],
}

function fillForm(src) {
  Object.assign(form, {
    country:          src.country,
    productCategory:  src.productCategory,
    bondCategory:     src.bondCategory || '',
    counterpartyTypes: Array.isArray(src.counterpartyTypes) ? [...src.counterpartyTypes] : (src.counterpartyType ? [src.counterpartyType] : []),
    taxRate:          src.taxRate,
    taxBase:          src.taxBase,
    settlementImpact: src.settlementImpact || 'net_deduct',
    taxTimingBase:    src.taxTimingBase || 'value_date',
    taxTimingOffset:  src.taxTimingOffset ?? 0,
    effectiveDate:    src.effectiveDate,
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
  form.effectiveDate = ''    // 复制时清空生效日期，要求重新填写
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
      bondCategory:     form.bondCategory || null,
      counterpartyTypes: form.counterpartyTypes,
      direction:        'pay',
      taxRate:          form.taxRate,
      taxBase:          form.taxBase,
      settlementImpact: form.settlementImpact,
      taxTimingBase:    form.taxTimingBase,
      taxTimingOffset:  form.taxTimingOffset,
      effectiveDate:    form.effectiveDate,
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

</style>
