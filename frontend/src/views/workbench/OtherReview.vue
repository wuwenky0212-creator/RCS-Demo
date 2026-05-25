<template>
  <div class="other-review">
    <div class="page-card">

      <div class="page-header">
        <div class="title">{{ t('otherReview.title') }}</div>
        <div class="title-tools">
          <el-icon class="tool" @click="handleQuery"><RefreshRight /></el-icon>
          <el-icon class="tool"><Setting /></el-icon>
        </div>
      </div>

      <!-- Tabs + 过滤 + 批量操作 -->
      <div class="toolbar">
        <div class="tabs">
          <div
            v-for="tab in tabs"
            :key="tab.value"
            class="tab"
            :class="{ active: activeTab === tab.value }"
            @click="switchTab(tab.value)"
          >
            {{ tab.label }}
            <span v-if="tab.count" class="tab-badge" :class="tab.badgeType">{{ tab.count }}</span>
          </div>
        </div>

        <div class="filters">
          <div class="filter">
            <span class="filter-label">{{ t('otherReview.externalNo') }}</span>
            <el-input
              v-model="filters.externalNo"
              :placeholder="t('common.search')"
              :prefix-icon="Search"
              clearable
              size="default"
              style="width:190px"
              @keyup.enter="handleQuery"
              @clear="handleQuery"
            />
          </div>
          <div class="filter">
            <span class="filter-label">{{ t('otherReview.approvalType') }}</span>
            <el-select
              v-model="filters.approvalType"
              :placeholder="t('common.all')"
              clearable
              size="default"
              style="width:140px"
            >
              <el-option v-for="at in approvalTypes" :key="at" :label="approvalTypeMap[at] || at" :value="at" />
            </el-select>
          </div>
          <div class="filter">
            <span class="filter-label">{{ t('otherReview.status') }}</span>
            <el-select
              v-model="filters.status"
              :placeholder="t('common.all')"
              clearable
              size="default"
              style="width:120px"
            >
              <el-option :label="t('otherReview.tabPending')" value="待审核" />
              <el-option :label="t('otherReview.tabApproved')" value="已审核" />
              <el-option :label="t('otherReview.tabRejected')" value="已驳回" />
            </el-select>
          </div>
          <el-button type="primary" size="default" @click="handleQuery">{{ t('common.query') }}</el-button>
          <el-button
            type="primary"
            size="default"
            :disabled="selectedRows.length === 0"
            @click="openBatchApprove"
          >{{ t('otherReview.batchApprove') }}</el-button>
        </div>
      </div>

      <!-- 表格 -->
      <el-table
        :data="currentData"
        border
        stripe
        size="default"
        style="width:100%"
        header-row-class-name="git-table-head"
        :header-cell-style="{ background:'#f5f7fa', color:'#606266', fontWeight:'600', fontSize:'13px' }"
        @selection-change="val => selectedRows = val"
      >
        <el-table-column type="selection" width="44" align="center" />

        <el-table-column prop="externalNo"   :label="t('otherReview.externalNo')" min-width="200" />
        <el-table-column :label="t('otherReview.approvalType')" min-width="140">
          <template #default="{ row }">{{ approvalTypeMap[row.approvalType] || row.approvalType }}</template>
        </el-table-column>

        <el-table-column :label="t('otherReview.status')" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)" size="small" effect="light">{{ statusMap[row.status] || row.status }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="initiator"  :label="t('otherReview.initiator')" min-width="100" />
        <el-table-column prop="handler"    :label="t('otherReview.handler')" min-width="100" />

        <el-table-column prop="eventContent" :label="t('otherReview.eventContent')" min-width="220">
          <template #default="{ row }">
            <span class="event-content" :title="row.eventContent">{{ row.eventContent }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="createTime" :label="t('otherReview.createTime')" width="160" />

        <el-table-column :label="t('common.actions')" width="120" fixed="right" align="center">
          <template #default="{ row }">
            <template v-if="row.status === '待审核'">
              <el-button link type="primary" size="small" @click="openApprove(row)">{{ t('otherReview.approve') }}</el-button>
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
          :page-sizes="[10, 20, 50, 100]"
          layout="total, prev, pager, next, sizes, jumper"
          background
        />
      </div>

    </div>
  </div>

  <!-- ── 审批弹窗 ── -->
  <el-dialog v-model="approveVisible" :title="t('otherReview.approveDialog')" width="520px" :close-on-click-modal="false">
    <div v-if="approveRow" class="approve-body">
      <div class="approve-info">
        <div class="info-row"><span class="info-label">{{ t('otherReview.externalNo') }}</span><span class="info-val link-text">{{ approveRow.externalNo }}</span></div>
        <div class="info-row"><span class="info-label">{{ t('otherReview.approvalType') }}</span><span class="info-val">{{ approvalTypeMap[approveRow.approvalType] || approveRow.approvalType }}</span></div>
        <div class="info-row"><span class="info-label">{{ t('otherReview.initiator') }}</span><span class="info-val">{{ approveRow.initiator }}</span></div>
        <div class="info-row"><span class="info-label">{{ t('otherReview.eventContent') }}</span><span class="info-val">{{ approveRow.eventContent }}</span></div>
      </div>
      <el-form label-width="80px" style="margin-top:16px">
        <el-form-item :label="t('otherReview.approveComment')">
          <el-input
            v-model="approveComment"
            type="textarea"
            :rows="3"
            :placeholder="t('otherReview.approveCommentPlaceholder')"
          />
        </el-form-item>
      </el-form>
    </div>
    <template #footer>
      <el-button @click="approveVisible = false">{{ t('common.cancel') }}</el-button>
      <el-button type="danger"   plain @click="confirmReject">{{ t('otherReview.reject') }}</el-button>
      <el-button type="primary"        @click="confirmApprove">{{ t('otherReview.approvePass') }}</el-button>
    </template>
  </el-dialog>

  <!-- ── 批量审批弹窗 ── -->
  <el-dialog v-model="batchVisible" :title="t('otherReview.batchDialog')" width="440px" :close-on-click-modal="false">
    <div class="confirm-body">
      <el-icon class="confirm-icon"><WarningFilled /></el-icon>
      <div class="confirm-text">
        <div class="confirm-title">{{ t('otherReview.batchConfirmTitle') }}</div>
        <div class="confirm-desc" v-html="t('otherReview.batchConfirmDesc', { n: selectedRows.length })"></div>
      </div>
    </div>
    <template #footer>
      <el-button @click="batchVisible = false">{{ t('common.cancel') }}</el-button>
      <el-button type="primary" @click="confirmBatchApprove">{{ t('otherReview.confirmApprove') }}</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage, ElNotification } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { Search, RefreshRight, Setting, WarningFilled } from '@element-plus/icons-vue'

const { t } = useI18n()

// ─── Computed translation maps ───────────────────────────────
const statusMap = computed(() => ({
  '待审核': t('otherReview.statusPending'),
  '已审核': t('otherReview.statusApproved'),
  '已驳回': t('otherReview.statusRejected'),
}))

const approvalTypeMap = computed(() => ({
  '挂账审批':   t('otherReview.approvalTypeSuspense'),
  '不入账审批': t('otherReview.approvalTypeNoEntry'),
  '销账审批':   t('otherReview.approvalTypeWriteOff'),
}))

// ─── 过滤 ───────────────────────────────────────────────────
const filters = ref({ externalNo: '', approvalType: '', status: '' })
const approvalTypes = ['挂账审批', '不入账审批', '销账审批']

function handleQuery() { ElMessage.success(t('common.querySuccess')) }

// ─── Tabs ───────────────────────────────────────────────────
const tabs = computed(() => [
  { label: t('otherReview.tabPending'), value: 'pending', count: 3, badgeType: 'badge-danger' },
  { label: t('otherReview.tabApproved'), value: 'approved', count: null, badgeType: '' },
  { label: t('otherReview.tabRejected'), value: 'rejected', count: null, badgeType: '' },
])
const activeTab = ref('pending')
function switchTab(v) {
  activeTab.value = v
  selectedRows.value = []
}

// ─── 分页 ───────────────────────────────────────────────────
const page     = ref(1)
const pageSize = ref(20)

// ─── Mock 数据 ──────────────────────────────────────────────
const pendingData = ref([
  {
    externalNo:   'BANCS-20260508-7819',
    approvalType: '挂账审批',
    status:       '待审核',
    initiator:    'Kevin Wang',
    handler:      'Lisa Chen',
    eventContent: 'Internal transfer failed (PMT-IB-20260508-001), Direction: Receive, Amount: USD 1,000,000.00. Suspense entry submitted to BGL account 2199000000, pending reviewer approval before funds are credited.',
    createTime:   '2026-05-08 14:32:17',
  },
  {
    externalNo:   'BANCS-20260508-3498',
    approvalType: '不入账审批',
    status:       '待审核',
    initiator:    'Sarah Zhang',
    handler:      'David Chen',
    eventContent: 'Internal transfer failed (PMT-BD-20260508-001), Direction: Receive, Amount: CNY 1,008,666.67. Operator confirmed funds arrived via alternative channel; no-entry marking applied, pending reviewer confirmation.',
    createTime:   '2026-05-08 15:10:44',
  },
  {
    externalNo:   'BANCS-20260509-3361',
    approvalType: '销账审批',
    status:       '待审核',
    initiator:    'Michael Liu',
    handler:      'Lisa Chen',
    eventContent: 'Suspense record (BGL account: 2199000000, EUR 875,000.00) write-off requested. Target account: 9001****3820, Orig. ref: BANCS-20260509-3361. Pending reviewer approval before funds transfer.',
    createTime:   '2026-05-10 09:48:22',
  },
])

const approvedData = ref([
  {
    externalNo:   'BANCS-20260507-6120',
    approvalType: '挂账审批',
    status:       '已审核',
    initiator:    'Michael Liu',
    handler:      'James Zhao',
    eventContent: 'Internal transfer failed (PMT-FX-20260507-001), Direction: Pay, Amount: USD 320,000.00. Suspended to BGL account 2199000000. Review approved; write-off to be completed within T+3.',
    createTime:   '2026-05-07 16:44:09',
  },
])

const rejectedData = ref([
  {
    externalNo:   'BANCS-20260507-5881',
    approvalType: '不入账审批',
    status:       '已驳回',
    initiator:    'Amy Sun',
    handler:      'Kevin Wang',
    eventContent: 'Internal transfer failed (PMT-MM-20260507-002), Amount: CNY 88,000,000.00. No-entry application rejected — funds not confirmed via alternative channel; continued tracking required.',
    createTime:   '2026-05-07 17:22:35',
  },
])

const currentData = computed(() => {
  if (activeTab.value === 'pending')  return pendingData.value
  if (activeTab.value === 'approved') return approvedData.value
  if (activeTab.value === 'rejected') return rejectedData.value
  return []
})

// ─── 多选 ───────────────────────────────────────────────────
const selectedRows = ref([])

// ─── 状态标签 ───────────────────────────────────────────────
function statusTagType(s) {
  const map = { '待审核': 'warning', '已审核': 'success', '已驳回': 'danger' }
  return map[s] || 'info'
}

// ─── 单条审批 ────────────────────────────────────────────────
const approveVisible  = ref(false)
const approveRow      = ref(null)
const approveComment  = ref('')

function openApprove(row) {
  approveRow.value    = row
  approveComment.value = ''
  approveVisible.value = true
}
function confirmApprove() {
  approveVisible.value = false
  ElNotification({ title: t('otherReview.approveSuccessTitle'), message: t('otherReview.approveSuccessMsg', { no: approveRow.value?.externalNo }), type: 'success', duration: 4000 })
  selectedRows.value = []
}
function confirmReject() {
  approveVisible.value = false
  ElNotification({ title: t('otherReview.rejectTitle'), message: t('otherReview.rejectMsg', { no: approveRow.value?.externalNo }), type: 'warning', duration: 4000 })
  selectedRows.value = []
}

// ─── 批量审批 ────────────────────────────────────────────────
const batchVisible = ref(false)

function openBatchApprove() {
  batchVisible.value = true
}
function confirmBatchApprove() {
  batchVisible.value = false
  ElNotification({ title: t('otherReview.batchApproveSuccessTitle'), message: t('otherReview.batchApproveSuccessMsg', { n: selectedRows.value.length }), type: 'success', duration: 4000 })
  selectedRows.value = []
}
</script>

<style lang="scss" scoped>
.other-review { height: 100%; }

.page-card {
  background: #fff;
  border-radius: 4px;
  padding: 16px 20px 12px;
  box-shadow: 0 1px 2px rgba(0,0,0,.02);
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;

  .title { font-size: 16px; font-weight: 600; color: var(--git-text-1); }
  .title-tools {
    display: flex; gap: 12px;
    .tool { font-size: 16px; color: var(--git-text-3); cursor: pointer; &:hover { color: var(--git-primary); } }
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
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 4px 14px;
    font-size: 13px;
    color: #99a3b1;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.15s, color 0.15s;

    &:hover { color: var(--git-primary); }
    &.active { color: #fff; background: var(--git-primary); font-weight: 600; }
  }
}

.tab-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: 9px;
  font-size: 11px;
  font-weight: 600;

  &.badge-danger { background: #fef0f0; color: #f56c6c; }

  .tab.active & {
    background: rgba(255,255,255,0.25);
    color: #fff;
  }
}

.filters {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.filter {
  display: flex;
  align-items: center;
  gap: 6px;
}

.filter-label {
  font-size: 13px;
  color: var(--git-text-2);
  white-space: nowrap;
}

:deep(.el-table .cell) { white-space: nowrap; }

.event-content {
  display: block;
  max-width: 340px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.link-text {
  color: var(--git-primary);
  cursor: pointer;
  &:hover { text-decoration: underline; }
}

.pagination-bar {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
}

/* ── 审批弹窗 ── */
.approve-body {
  padding: 0 4px;
}

.approve-info {
  background: #f8f9fc;
  border: 1px solid var(--git-border);
  border-radius: 4px;
  padding: 4px 0;

  .info-row {
    display: flex;
    align-items: flex-start;
    padding: 8px 16px;
    font-size: 13px;
    border-bottom: 1px solid #edf0f7;
    &:last-child { border-bottom: none; }
  }

  .info-label {
    width: 80px;
    flex-shrink: 0;
    color: #606266;
  }

  .info-val {
    color: #303133;
    line-height: 1.6;
  }
}

/* ── 批量审批弹窗 ── */
.confirm-body {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 4px 8px 12px;

  .confirm-icon { font-size: 28px; color: #e6a23c; flex-shrink: 0; margin-top: 2px; }
  .confirm-title { font-size: 15px; font-weight: 600; color: #303133; margin-bottom: 8px; }
  .confirm-desc { font-size: 13px; color: #606266; line-height: 1.7; b { color: #303133; } }
}
</style>
