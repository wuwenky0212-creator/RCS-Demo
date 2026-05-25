<template>
  <div class="scenario-query">

    <!-- 模块内横向导航 -->
    <PnlSubNav />

    <!-- 筛选条 -->
    <div class="filter-card">
      <div class="filter-row">
        <div class="filter-item">
          <span class="filter-label">{{ t('pnlAttribution.scenarioName') }}</span>
          <el-input
            v-model="filters.name"
            :placeholder="t('pnlAttribution.searchPlaceholder')"
            :prefix-icon="Search"
            clearable
            style="width: 200px;"
            @keyup.enter="doQuery"
            @clear="doQuery"
          />
        </div>
        <div class="filter-item">
          <span class="filter-label">{{ t('pnlAttribution.portfolio') }}</span>
          <el-tree-select
            v-model="filters.portfolio"
            :data="portfolioTreeData"
            node-key="value"
            :props="treeProps"
            clearable
            filterable
            check-strictly
            style="width: 280px;"
            :placeholder="t('pnlAttribution.portfolioPlaceholder')"
            @change="doQuery"
          />
        </div>
        <el-button type="primary" @click="doQuery">{{ t('pnlAttribution.query') }}</el-button>
        <el-button @click="doReset">{{ t('pnlAttribution.reset') }}</el-button>
      </div>
    </div>

    <!-- 表格卡片 -->
    <div class="table-card">
      <div class="card-header">
        <span class="card-title">{{ t('pnlAttribution.scenarioQuery') }}</span>
        <el-button type="primary" size="small" @click="openAdd">
          {{ t('pnlAttribution.add') }}
        </el-button>
      </div>

      <el-table
        :data="rows"
        v-loading="loading"
        stripe
        border
        size="default"
        header-row-class-name="git-table-head"
        style="width: 100%;"
      >
        <el-table-column :label="t('pnlAttribution.scenarioName')" min-width="140">
          <template #default="{ row }">
            <span class="scenario-link" @click="goToReport(row)">{{ row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="portfolio" :label="t('pnlAttribution.portfolio')" min-width="110" />
        <el-table-column :label="t('pnlAttribution.attributionMethod')" min-width="110">
          <template #default="{ row }">{{ translateMethod(row.attributionMethod) }}</template>
        </el-table-column>
        <el-table-column :label="t('pnlAttribution.calcScheme')" min-width="110">
          <template #default="{ row }">{{ translateScheme(row.calculationScheme) }}</template>
        </el-table-column>
        <el-table-column prop="currency" :label="t('pnlAttribution.currency')" min-width="80" />

        <el-table-column :label="t('common.actions')" width="110" fixed="right" align="center">
          <template #default="{ row }">
            <el-button link type="danger" @click="doDelete(row)">{{ t('pnlAttribution.delete') }}</el-button>
            <el-button link type="primary" @click="openEdit(row)">{{ t('pnlAttribution.edit') }}</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-bar">
        <el-pagination
          v-model:current-page="page.current"
          v-model:page-size="page.size"
          :page-sizes="[10, 20, 50]"
          :total="page.total"
          background
          layout="total, prev, pager, next, sizes"
          @current-change="loadData"
          @size-change="loadData"
        />
      </div>
    </div>

    <!-- 新增 / 编辑对话框 -->
    <el-dialog
      v-model="dialog.visible"
      :title="dialog.isEdit ? t('pnlAttribution.editScenario') : t('pnlAttribution.addScenario')"
      width="560px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="formRules"
        label-width="120px"
        label-position="right"
      >
        <el-form-item :label="t('pnlAttribution.scenarioName')" prop="name">
          <el-input v-model="form.name" :placeholder="t('pnlAttribution.namePlaceholder')" />
        </el-form-item>
        <el-form-item :label="t('pnlAttribution.portfolio')" prop="portfolio">
          <el-tree-select
            v-model="form.portfolio"
            :data="portfolioTreeData"
            node-key="value"
            :props="treeProps"
            clearable
            filterable
            check-strictly
            style="width: 100%;"
            :placeholder="t('pnlAttribution.portfolioPlaceholder')"
          />
        </el-form-item>
        <el-form-item :label="t('pnlAttribution.attributionMethod')">
          <span class="scheme-fixed">{{ t('pnlAttribution.attributionMethodRevalue') }}</span>
        </el-form-item>
        <el-form-item :label="t('pnlAttribution.calcScheme')" prop="calculationScheme">
          <el-select v-model="form.calculationScheme" style="width: 100%;">
            <el-option :label="t('pnlAttribution.schemeAccumulate')" value="累计模式" />
            <el-option :label="t('pnlAttribution.schemeRestore')" value="恢复模式" />
          </el-select>
        </el-form-item>
        <el-form-item :label="t('pnlAttribution.currency')" prop="currency">
          <el-select v-model="form.currency" :placeholder="t('pnlAttribution.currencyPlaceholder')" style="width: 100%;">
            <el-option v-for="c in CURRENCIES" :key="c" :label="c" :value="c" />
          </el-select>
        </el-form-item>
        <el-form-item :label="t('pnlAttribution.dateRange')">
          <div class="date-range-row">
            <div class="date-range-item">
              <span class="date-label">{{ t('pnlAttribution.startDate') }}</span>
              <el-date-picker
                v-model="form.startDate"
                type="date"
                value-format="YYYY-MM-DD"
                :placeholder="t('common.startDate')"
                style="width: 100%;"
                disabled
              />
            </div>
            <div class="date-range-item">
              <span class="date-label">{{ t('pnlAttribution.endDate') }}</span>
              <el-date-picker
                v-model="form.endDate"
                type="date"
                value-format="YYYY-MM-DD"
                :placeholder="t('common.endDate')"
                style="width: 100%;"
                disabled
              />
            </div>
          </div>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialog.visible = false">{{ t('common.cancel') }}</el-button>
        <el-button type="primary" :loading="saving" @click="doSave">{{ t('common.confirm') }}</el-button>
      </template>
    </el-dialog>

  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import PnlSubNav from '@/components/PnlSubNav.vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import {
  listScenarios,
  createScenario,
  updateScenario,
  deleteScenario,
} from '@/api/pnl'
import {
  ENTITY,
  BUSINESS_UNITS,
  BOOKS,
  PORTFOLIOS as _PORTFOLIOS,
} from '@/data/bookStructure.js'

// ── 树形 props ──────────────────────────────────────────────────────────────
const treeProps = { label: 'label', children: 'children' }

// ── 账户树（Entity → BusinessUnit → Book → Portfolio）────────────────────────
// 用户通常在 Book 层级选取，各层均可选
const portfolioTreeData = [
  {
    value: ENTITY.code,
    label: ENTITY.name,
    children: BUSINESS_UNITS.map(bu => ({
      value: bu.code,
      label: bu.name,
      children: BOOKS.filter(b => b.businessUnit === bu.code).map(book => ({
        value: book.code,
        label: `${book.code} · ${book.name}`,
        children: _PORTFOLIOS.filter(p => p.book === book.code).map(p => ({
          value: p.code,
          label: `${p.code}（${p.description}）`,
        })),
      })),
    })),
  },
]

const { t } = useI18n()
const router = useRouter()

const MAX_TAGS = 7

const CURRENCIES = ['USD', 'CNY', 'EUR', 'GBP', 'JPY']

// ── 筛选 ──────────────────────────────────────────────────────────────────
const filters = reactive({ name: '', portfolio: '' })

// ── 分页 ──────────────────────────────────────────────────────────────────
const page = reactive({ current: 1, size: 20, total: 0 })
const rows = ref([])
const loading = ref(false)

// ── 对话框 ────────────────────────────────────────────────────────────────
const dialog = reactive({ visible: false, isEdit: false })
const formRef = ref(null)
const saving = ref(false)

function todayStr() {
  return new Date().toISOString().slice(0, 10)
}
function yesterdayStr() {
  const d = new Date()
  d.setDate(d.getDate() - 1)
  return d.toISOString().slice(0, 10)
}

const emptyForm = () => ({
  id: '',
  name: '',
  portfolio: '',
  attributionMethod: '重估值',
  calculationScheme: '累计模式',
  currency: 'USD',
  startDate: yesterdayStr(),
  endDate: todayStr(),
  ruleConditions: [],
})
const form = reactive(emptyForm())

const formRules = computed(() => ({
  name:              [{ required: true, message: t('pnlAttribution.namePlaceholder'),    trigger: 'blur' }],
  portfolio:         [{ required: true, message: t('pnlAttribution.portfolioPlaceholder'), trigger: 'change' }],
  currency:          [{ required: true, message: t('pnlAttribution.currencyPlaceholder'), trigger: 'change' }],
}))

// ── 显示值翻译 ──────────────────────────────────────────────────────────────
function translateMethod(v) {
  if (v === '重估值') return t('pnlAttribution.attributionMethodRevalue')
  return v
}
function translateScheme(v) {
  if (v === '累计模式') return t('pnlAttribution.schemeAccumulate')
  if (v === '恢复模式') return t('pnlAttribution.schemeRestore')
  return v
}

// ── 方法 ──────────────────────────────────────────────────────────────────
function goToReport(row) {
  router.push({ name: 'attribution-report', query: { id: row.id, name: row.name } })
}

function visibleTags(conditions) {
  return conditions.slice(0, MAX_TAGS)
}

async function loadData() {
  loading.value = true
  try {
    const data = await listScenarios({
      name: filters.name || undefined,
      portfolio: filters.portfolio || undefined,
      page: page.current,
      pageSize: page.size,
    })
    rows.value = data.items
    page.total = data.total
  } catch {
    ElMessage.error(t('pnlAttribution.loadError'))
  } finally {
    loading.value = false
  }
}

function doQuery() {
  page.current = 1
  loadData()
}

function doReset() {
  filters.name = ''
  filters.portfolio = ''
  doQuery()
}

function openAdd() {
  Object.assign(form, emptyForm())
  dialog.isEdit = false
  dialog.visible = true
}

function openEdit(row) {
  Object.assign(form, {
    id: row.id,
    name: row.name,
    portfolio: row.portfolio,
    attributionMethod: row.attributionMethod,
    calculationScheme: row.calculationScheme,
    currency: row.currency,
    startDate: row.startDate || '',
    endDate: row.endDate || '',
    ruleConditions: [...row.ruleConditions],
  })
  dialog.isEdit = true
  dialog.visible = true
}

async function doSave() {
  await formRef.value.validate()
  saving.value = true
  try {
    const payload = {
      name: form.name,
      portfolio: form.portfolio,
      attributionMethod: form.attributionMethod,
      calculationScheme: form.calculationScheme,
      currency: form.currency,
      startDate: form.startDate,
      endDate: form.endDate,
      ruleConditions: form.ruleConditions,
    }
    if (dialog.isEdit) {
      await updateScenario(form.id, payload)
    } else {
      await createScenario(payload)
    }
    ElMessage.success(t('pnlAttribution.saveSuccess'))
    dialog.visible = false
    loadData()
  } catch {
    ElMessage.error(t('pnlAttribution.loadError'))
  } finally {
    saving.value = false
  }
}

async function doDelete(row) {
  try {
    await ElMessageBox.confirm(
      t('pnlAttribution.deleteConfirmMsg', { name: row.name }),
      t('pnlAttribution.deleteConfirmTitle'),
      { type: 'warning' }
    )
    await deleteScenario(row.id)
    ElMessage.success(t('pnlAttribution.deleteSuccess'))
    loadData()
  } catch { /* cancel */ }
}

onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
.scenario-query {
  display: flex;
  flex-direction: column;
  gap: 0;
  height: 100%;
}

.filter-card,
.table-card {
  margin-top: 12px;
}

/* ── 筛选条 ── */
.filter-card {
  background: #fff;
  border-radius: 4px;
  padding: 14px 20px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
  flex-shrink: 0;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
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

/* ── 表格卡片 ── */
.table-card {
  background: #fff;
  border-radius: 4px;
  padding: 16px 20px 12px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--git-text-1);
}

/* ── 日期范围行 ── */
.date-range-row {
  display: flex;
  gap: 16px;
  width: 100%;
}

.date-range-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.date-label {
  font-size: 12px;
  color: var(--git-text-2);
  white-space: nowrap;
}

/* ── 计算方案固定值 ── */
.scheme-fixed {
  font-size: 13px;
  color: var(--git-text-1);
  line-height: 32px;
}

/* ── 情景名称 link ── */
.scenario-link {
  color: var(--git-primary);
  cursor: pointer;
  font-weight: 500;
  &:hover { text-decoration: underline; }
}

/* ── Tags ── */
.tags-cell {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  align-items: center;
}

.rule-tag {
  font-size: 12px;
  border-radius: 3px;

  &--more {
    background: #f0f2f5;
    color: var(--git-text-2);
    border-color: #d9dde4;
    font-weight: 600;
  }
}

/* ── 分页 ── */
.pagination-bar {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
}
</style>
