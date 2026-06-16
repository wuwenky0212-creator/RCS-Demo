<template>
  <aside class="git-workbench-sidebar">
    <div class="panel-header">
      <span class="panel-icon">🧩</span>
      <span class="panel-title">{{ t('workbench.title') }}</span>
    </div>

    <div class="search-box">
      <el-input
        v-model="keyword"
        :placeholder="t('common.search')"
        :prefix-icon="Search"
        clearable
        size="default"
      />
    </div>

    <div class="menu-scroll">
      <div
        v-for="group in filteredGroups"
        :key="group.nameKey"
        class="menu-group"
      >
        <div class="group-title">
          <el-icon class="group-icon"><component :is="group.icon" /></el-icon>
          <span>{{ t(group.nameKey) }}</span>
        </div>
        <div class="group-items">
          <router-link
            v-for="m in group.children"
            :key="m.path"
            :to="m.path"
            custom
            v-slot="{ navigate }"
          >
            <div
              class="menu-item"
              :class="{ active: isActive(m.path) }"
              @click="navigate"
            >
              <span class="dot">●</span>
              <span class="label">{{ t(m.labelKey) }}</span>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, markRaw } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  Search, Operation, CircleCheck, Money, Notebook,
  Calendar, EditPen, Briefcase, Switch
} from '@element-plus/icons-vue'

const route = useRoute()
const { t } = useI18n()
const keyword = ref('')

// 工作台菜单分组 - 使用 i18n 翻译键 (Task 10.2)
const menuGroups = [
  {
    nameKey: 'workbench.flowApproval',
    icon: markRaw(Operation),
    children: [
      { labelKey: 'workbench.transactionReview', path: '/workbench/transaction-review' },
      { labelKey: 'workbench.clearingApproval',  path: '/workbench/clearing-review' },
      { labelKey: 'workbench.adjustReview',       path: '/workbench/adjust-review' },
      { labelKey: 'workbench.otherReview',        path: '/workbench/other-review' }
    ]
  },
  {
    nameKey: 'workbench.confirmVerification',
    icon: markRaw(CircleCheck),
    children: [
      { labelKey: 'workbench.confirmMatch',  path: '/workbench/confirm-match' },
      { labelKey: 'workbench.confirmDetail', path: '/workbench/confirm-detail' },
      { labelKey: 'workbench.confirmMsg',    path: '/workbench/confirm-msg' }
    ]
  },
  {
    nameKey: 'workbench.clearingSettlement',
    icon: markRaw(Money),
    children: [
      { labelKey: 'workbench.netting',        path: '/workbench/netting' },
      { labelKey: 'workbench.dispatch',        path: '/workbench/dispatch' },
      { labelKey: 'workbench.incomingSort',    path: '/workbench/incoming-sort' },
      { labelKey: 'workbench.holidayAdjust',   path: '/workbench/holiday-adjust' },
      { labelKey: 'workbench.paymentCancel',   path: '/workbench/payment-cancel' },
      { labelKey: 'workbench.paymentMsg',      path: '/workbench/payment-msg' },
      { labelKey: 'workbench.settleRoute',     path: '/workbench/settle-route' }
    ]
  },
  {
    nameKey: 'workbench.internalAcct',
    icon: markRaw(Switch),
    children: [
      { labelKey: 'workbench.pendingDelivery',       path: '/workbench/pending-delivery' },
      { labelKey: 'workbench.internalTransferError', path: '/workbench/internal-transfer-error' },
      { labelKey: 'workbench.suspenseAcct',          path: '/workbench/suspense-acct' }
    ]
  },
  {
    nameKey: 'workbench.accounting',
    icon: markRaw(Notebook),
    children: [
      { labelKey: 'workbench.measureTrack', path: '/workbench/measure-track' },
      { labelKey: 'workbench.postError',    path: '/workbench/post-error' },
      { labelKey: 'workbench.balanceInit',  path: '/workbench/balance-init' },
      { labelKey: 'workbench.manualAssign', path: '/workbench/manual-assign' },
      { labelKey: 'workbench.thresholdPass',path: '/workbench/threshold-pass' }
    ]
  },
  {
    nameKey: 'workbench.dailyRecon',
    icon: markRaw(Calendar),
    children: [
      { labelKey: 'workbench.custodianRecon', path: '/workbench/custodian-recon' }
    ]
  },
  {
    nameKey: 'workbench.tradeEntryGroup',
    icon: markRaw(EditPen),
    children: [
      { labelKey: 'workbench.cashflowEntry', path: '/workbench/cashflow-entry' }
    ]
  },
  {
    nameKey: 'workbench.businessMgmt',
    icon: markRaw(Briefcase),
    children: [
      { labelKey: 'workbench.fixMgmt', path: '/workbench/fix-mgmt' }
    ]
  }
]

const filteredGroups = computed(() => {
  const kw = keyword.value.trim().toLowerCase()
  if (!kw) return menuGroups
  return menuGroups
    .map((g) => ({
      ...g,
      children: g.children.filter((c) => t(c.labelKey).toLowerCase().includes(kw))
    }))
    .filter((g) => g.children.length > 0)
})

function isActive(path) {
  return route.path === path
}
</script>

<style lang="scss" scoped>
.git-workbench-sidebar {
  width: 220px;
  flex-shrink: 0;
  background: var(--git-surface);
  border-right: 1px solid var(--git-border);
  display: flex;
  flex-direction: column;
  height: 100%;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 16px 8px;
  font-size: 15px;
  font-weight: 600;
  color: var(--git-text-1);

  .panel-icon { font-size: 16px; }
}

.search-box {
  padding: 4px 12px 12px;
}

.menu-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 0 4px 16px;
}

.menu-group + .menu-group {
  margin-top: 4px;
}

.group-title {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px 4px;
  color: var(--git-text-2);
  font-size: 13px;
  font-weight: 600;

  .group-icon {
    font-size: 14px;
    color: var(--git-text-2);
  }
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px 6px 24px;
  font-size: 13px;
  color: var(--git-text-2);
  cursor: pointer;
  border-radius: 4px;
  margin: 2px 4px;
  position: relative;
  transition: background 0.15s, color 0.15s;

  .dot {
    color: #cbd2d9;
    font-size: 8px;
    line-height: 1;
  }

  &:hover {
    background: var(--git-bg);
    color: var(--git-text-1);
  }

  &.active {
    background: #eaf1ff;
    color: var(--git-primary);
    font-weight: 600;

    .dot { color: var(--git-primary); }

    &::before {
      content: '';
      position: absolute;
      left: 0;
      top: 6px;
      bottom: 6px;
      width: 3px;
      background: var(--git-primary);
      border-radius: 0 2px 2px 0;
    }
  }
}
</style>
