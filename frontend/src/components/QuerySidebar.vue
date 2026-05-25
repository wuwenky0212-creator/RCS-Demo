<template>
  <aside class="git-query-sidebar">
    <div class="panel-header">
      <el-icon class="panel-icon"><DataAnalysis /></el-icon>
      <span class="panel-title">{{ t('querySidebar.title') }}</span>
    </div>

    <div class="menu-scroll">

      <!-- 交易查询 -->
      <div class="menu-group">
        <div class="group-title">
          <el-icon class="group-icon"><List /></el-icon>
          <span>{{ t('querySidebar.groupQuery') }}</span>
        </div>
        <div class="group-items">
          <router-link to="/statistics" custom v-slot="{ navigate }">
            <div
              class="menu-item"
              :class="{ active: isActive('/statistics') }"
              @click="navigate"
            >
              <span class="dot">●</span>
              <span class="label">{{ t('querySidebar.tradeQuery') }}</span>
            </div>
          </router-link>
          <div class="menu-item disabled">
            <span class="dot">●</span>
            <span class="label">{{ t('querySidebar.positionQuery') }}</span>
          </div>
          <div class="menu-item disabled">
            <span class="dot">●</span>
            <span class="label">{{ t('querySidebar.acctBalanceQuery') }}</span>
          </div>
        </div>
      </div>

      <!-- 报表统计 -->
      <div class="menu-group">
        <div class="group-title">
          <el-icon class="group-icon"><TrendCharts /></el-icon>
          <span>{{ t('querySidebar.groupStats') }}</span>
        </div>
        <div class="group-items">
          <div class="menu-item disabled">
            <span class="dot">●</span>
            <span class="label">{{ t('querySidebar.maturityStats') }}</span>
          </div>
          <div class="menu-item disabled">
            <span class="dot">●</span>
            <span class="label">{{ t('querySidebar.taxReport') }}</span>
          </div>
          <div class="menu-item disabled">
            <span class="dot">●</span>
            <span class="label">{{ t('querySidebar.cashflowReport') }}</span>
          </div>
        </div>
      </div>

    </div>
  </aside>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { DataAnalysis, List, TrendCharts } from '@element-plus/icons-vue'

const route = useRoute()
const { t } = useI18n()

function isActive(path) {
  return route.path === path || route.path.startsWith(path + '/')
}
</script>

<style lang="scss" scoped>
.git-query-sidebar {
  width: 200px;
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

  .panel-icon {
    font-size: 16px;
    color: var(--git-primary);
  }
}

.menu-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 0 4px 16px;
}

.group-title {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px 4px;
  color: var(--git-text-2);
  font-size: 13px;
  font-weight: 600;

  .group-icon { font-size: 14px; }
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

  &.disabled {
    opacity: 0.45;
    cursor: not-allowed;
    &:hover { background: transparent; color: var(--git-text-2); }
  }
}
</style>
