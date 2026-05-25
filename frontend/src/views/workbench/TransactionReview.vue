<template>
  <div class="transaction-review">
    <div class="page-card">
      <div class="page-header">
        <div class="title">{{ t('transactionReview.title') }}</div>
        <div class="title-tools">
          <el-icon class="tool" @click="loadData"><RefreshRight /></el-icon>
          <el-icon class="tool"><Setting /></el-icon>
        </div>
      </div>

      <!-- Tabs + 搜索 + 批量操作 -->
      <div class="toolbar">
        <div class="tabs">
          <div
            v-for="tab in tabs"
            :key="tab.value"
            class="tab"
            :class="{ active: activeTab === tab.value }"
            @click="onTabChange(tab.value)"
          >
            {{ tab.label }}
          </div>
        </div>

        <div class="filters">
          <div class="filter">
            <span class="filter-label">{{ t('transactionReview.externalNo') }}</span>
            <el-input
              v-model="filters.externalNo"
              :placeholder="t('transactionReview.searchPlaceholder')"
              :prefix-icon="Search"
              clearable
              size="default"
              style="width: 200px;"
              @keyup.enter="loadData"
              @clear="loadData"
            />
          </div>
          <div class="filter">
            <span class="filter-label">{{ t('transactionReview.tradeNo') }}</span>
            <el-input
              v-model="filters.tradeNo"
              :placeholder="t('transactionReview.searchPlaceholder')"
              :prefix-icon="Search"
              clearable
              size="default"
              style="width: 200px;"
              @keyup.enter="loadData"
              @clear="loadData"
            />
          </div>
          <el-button type="primary" @click="batchApprove" :disabled="!selectedIds.length">
            {{ t('transactionReview.batchApprove') }}
          </el-button>
        </div>
      </div>

      <!-- 表格 -->
      <el-table
        :data="rows"
        v-loading="loading"
        @selection-change="onSelectionChange"
        stripe
        border
        size="default"
        header-row-class-name="git-table-head"
        style="width: 100%;"
      >
        <el-table-column type="selection" width="44" align="center" />

        <el-table-column prop="externalNo" :label="t('transactionReview.externalNo')" min-width="160" />
        <el-table-column prop="tradeNo"    :label="t('transactionReview.tradeNo')"    min-width="160" />

        <el-table-column :label="t('transactionReview.product')" min-width="130">
          <template #header>
            <span class="th-with-filter">
              {{ t('transactionReview.product') }}
              <el-icon><Filter /></el-icon>
            </span>
          </template>
          <template #default="{ row }">{{ row.product }}</template>
        </el-table-column>

        <el-table-column :label="t('transactionReview.action')" min-width="84" align="left">
          <template #header>
            <span class="th-with-filter">{{ t('transactionReview.action') }} <el-icon><Filter /></el-icon></span>
          </template>
          <template #default="{ row }">{{ row.action }}</template>
        </el-table-column>

        <el-table-column :label="t('transactionReview.valueDate')" min-width="120">
          <template #header>
            <span class="th-with-filter">{{ t('transactionReview.valueDate') }} <el-icon><Filter /></el-icon></span>
          </template>
          <template #default="{ row }">{{ row.valueDate }}</template>
        </el-table-column>

        <el-table-column prop="tradeDate"   :label="t('transactionReview.tradeDate')"   min-width="110" />

        <el-table-column :label="t('transactionReview.counterparty')" min-width="100">
          <template #default="{ row }">
            <span class="link">{{ row.counterparty }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="instrument"  :label="t('transactionReview.instrument')"  min-width="130" />

        <el-table-column :label="t('transactionReview.usdAmount')" min-width="140" align="right">
          <template #default="{ row }">{{ formatAmount(row.usdAmount) }}</template>
        </el-table-column>

        <el-table-column :label="t('transactionReview.direction')" min-width="100">
          <template #default="{ row }">
            <span :class="directionClass(row.direction)">{{ row.direction }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="reviewer"    :label="t('transactionReview.reviewer')"    min-width="100" />

        <el-table-column :label="t('transactionReview.operate')" width="80" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="approveOne(row)">{{ t('transactionReview.approve') }}</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-bar">
        <el-pagination
          v-model:current-page="page.current"
          v-model:page-size="page.size"
          :page-sizes="[10, 20, 50, 100]"
          :total="page.total"
          background
          layout="total, prev, pager, next, sizes, jumper"
          @current-change="loadData"
          @size-change="loadData"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Filter, RefreshRight, Setting } from '@element-plus/icons-vue'
import {
  listTransactionReviews,
  approveTransactionReview,
  batchApproveTransactionReviews
} from '@/api/workbench'

const { t } = useI18n()

const tabs = computed(() => [
  { label: t('transactionReview.tabApprove'), value: 'approve' },
  { label: t('transactionReview.tabReissue'), value: 'reissue' },
  { label: t('transactionReview.tabEvent'),   value: 'event' }
])
const activeTab = ref('approve')

const filters = reactive({
  externalNo: '',
  tradeNo: ''
})

const page = reactive({
  current: 1,
  size: 20,
  total: 0
})

const rows = ref([])
const loading = ref(false)
const selectedIds = ref([])

function onTabChange(v) {
  activeTab.value = v
  page.current = 1
  loadData()
}

async function loadData() {
  loading.value = true
  try {
    const data = await listTransactionReviews({
      tab: activeTab.value,
      externalNo: filters.externalNo || undefined,
      tradeNo: filters.tradeNo || undefined,
      page: page.current,
      pageSize: page.size
    })
    rows.value = data.items
    page.total = data.total
  } catch (e) {
    ElMessage.error(t('transactionReview.loadError'))
  } finally {
    loading.value = false
  }
}

function onSelectionChange(sel) {
  selectedIds.value = sel.map((x) => x.tradeNo)
}

async function approveOne(row) {
  try {
    await ElMessageBox.confirm(
      t('transactionReview.approveConfirmMsg', { no: row.tradeNo }),
      t('transactionReview.approveConfirmTitle'),
      { type: 'info' }
    )
    await approveTransactionReview(row.tradeNo)
    ElMessage.success(t('transactionReview.approveSuccess'))
    loadData()
  } catch (_) { /* cancel */ }
}

async function batchApprove() {
  if (!selectedIds.value.length) return
  try {
    await ElMessageBox.confirm(
      t('transactionReview.batchApproveMsg', { n: selectedIds.value.length }),
      t('transactionReview.batchApproveTitle'),
      { type: 'warning' }
    )
    await batchApproveTransactionReviews(selectedIds.value)
    ElMessage.success(t('transactionReview.batchApproveSuccess', { n: selectedIds.value.length }))
    selectedIds.value = []
    loadData()
  } catch (_) { /* cancel */ }
}

function formatAmount(v) {
  if (v === null || v === undefined) return ''
  return Number(v).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function directionClass(d) {
  switch (d) {
    case 'Buy':     return 'git-tag-buy'
    case 'Sell':    return 'git-tag-sell'
    case 'Pay':     return 'git-tag-pay'
    case 'Receive': return 'git-tag-recv'
    case 'Lend':    return 'git-tag-borrow'
    case 'Borrow':  return 'git-tag-lend'
    default: return ''
  }
}

onMounted(loadData)
</script>

<style lang="scss" scoped>
.transaction-review {
  height: 100%;
}

.page-card {
  background: #fff;
  border-radius: 4px;
  padding: 16px 20px 12px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;

  .title {
    font-size: 16px;
    font-weight: 600;
    color: var(--git-text-1);
  }

  .title-tools {
    display: flex;
    gap: 12px;
    .tool {
      font-size: 16px;
      color: var(--git-text-3);
      cursor: pointer;
      &:hover { color: var(--git-primary); }
    }
  }
}

.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
  gap: 12px;
  flex-wrap: wrap;
}

.tabs {
  display: flex;
  gap: 6px;

  .tab {
    padding: 4px 14px;
    font-size: 13px;
    color: var(--git-text-2);
    border-radius: 4px;
    cursor: pointer;
    background: transparent;
    transition: background 0.15s, color 0.15s;

    &:hover { color: var(--git-primary); }

    &.active {
      color: #fff;
      background: var(--git-primary);
      font-weight: 600;
    }

    &:not(.active) {
      color: #99a3b1;
    }
  }
}

.filters {
  display: flex;
  gap: 12px;
  align-items: center;

  .filter {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .filter-label {
    font-size: 13px;
    color: var(--git-text-2);
  }
}

/* 全局禁止单元格折行 */
:deep(.el-table .cell) {
  white-space: nowrap;
}

.th-with-filter {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  .el-icon { font-size: 12px; color: var(--git-text-3); }
}

.link {
  color: #ff7d00;
  cursor: pointer;
  &:hover { text-decoration: underline; }
}

.pagination-bar {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
}
</style>
