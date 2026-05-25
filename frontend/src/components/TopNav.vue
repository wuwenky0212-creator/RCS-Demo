<template>
  <header class="git-top-nav">
    <div class="logo">
      <img src="/rcslogo.png" alt="RCS Logo" class="logo-img" />
    </div>

    <nav class="nav-menu">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        custom
        v-slot="{ navigate }"
      >
        <div
          class="nav-item"
          :class="{ active: isActive(item) }"
          @click="navigate"
        >
          <el-icon class="nav-icon"><component :is="item.icon" /></el-icon>
          <span>{{ t(item.labelKey) }}</span>
        </div>
      </router-link>
    </nav>

    <div class="right-tools">
      <el-icon class="tool-icon"><Files /></el-icon>
      <el-badge :value="3" class="tool-badge">
        <el-icon class="tool-icon"><Bell /></el-icon>
      </el-badge>
      <!-- Settings Button (Requirements 7.1, 7.2, 9) -->
      <el-tooltip :content="t('nav.settings')" placement="bottom">
        <el-icon class="tool-icon" @click="showSettings = true"><Setting /></el-icon>
      </el-tooltip>
      <div class="user-info">
        <el-icon><User /></el-icon>
        <span>admin</span>
        <el-icon class="caret"><ArrowDown /></el-icon>
      </div>
    </div>
  </header>

  <!-- Settings Dialog (Task 8, 9) -->
  <Settings v-model:visible="showSettings" />
</template>

<script setup>
import { ref, computed, markRaw } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  HomeFilled, EditPen, Histogram, Coin, Briefcase,
  Search, UserFilled, DataLine, DataAnalysis, Setting,
  Files, Bell, User, ArrowDown, TrendCharts
} from '@element-plus/icons-vue'
import Settings from './Settings.vue'

const route = useRoute()
const { t } = useI18n()

const showSettings = ref(false)

// Menu items using i18n translation keys (Task 10.1)
const menuItems = [
  { path: '/home',         labelKey: 'nav.home',       icon: markRaw(HomeFilled) },
  { path: '/trade-entry',  labelKey: 'nav.tradeEntry',  icon: markRaw(EditPen) },
  { path: '/position',     labelKey: 'nav.position',    icon: markRaw(Histogram) },
  { path: '/limit',        labelKey: 'nav.limit',       icon: markRaw(Coin) },
  { path: '/business',     labelKey: 'nav.business',    icon: markRaw(Briefcase) },
  { path: '/query',        labelKey: 'nav.query',       icon: markRaw(Search) },
  { path: '/workbench',    labelKey: 'nav.workbench',   icon: markRaw(UserFilled) },
  { path: '/base-data',    labelKey: 'nav.baseData',    icon: markRaw(DataLine) },
  { path: '/statistics',   labelKey: 'nav.statistics',  icon: markRaw(DataAnalysis) },
  { path: '/rules',        labelKey: 'nav.rules',       icon: markRaw(Setting) },
  { path: '/pnl-attribution', labelKey: 'nav.pnlAttribution', icon: markRaw(TrendCharts) }
]

function isActive(item) {
  // 子路径匹配（如 /workbench/* 命中 /workbench）
  return route.path === item.path || route.path.startsWith(item.path + '/')
}
</script>

<style lang="scss" scoped>
.git-top-nav {
  height: 56px;
  background: var(--git-surface);
  border-bottom: 1px solid var(--git-border);
  display: flex;
  align-items: center;
  padding: 0 20px;
  position: relative;
  z-index: 100;
}

.logo {
  display: flex;
  align-items: center;
  margin-right: 28px;
  flex-shrink: 0;
  user-select: none;

  .logo-img {
    height: 24px;
    width: auto;
    object-fit: contain;
    display: block;
  }
}

.nav-menu {
  display: flex;
  flex: 1;
  height: 100%;
  align-items: center;
  gap: 4px;
  overflow-x: auto;
}

.nav-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 0 14px;
  height: 100%;
  font-size: 14px;
  color: var(--git-text-2);
  cursor: pointer;
  white-space: nowrap;
  position: relative;
  transition: color 0.15s;

  .nav-icon {
    font-size: 16px;
  }

  &:hover {
    color: var(--git-primary);
  }

  &.active {
    color: var(--git-text-1);
    font-weight: 600;

    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 14px;
      right: 14px;
      height: 2px;
      background: var(--git-primary);
      border-radius: 2px;
    }
  }
}

.right-tools {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-left: 12px;
}

.tool-icon {
  font-size: 18px;
  color: var(--git-text-2);
  cursor: pointer;

  &:hover { color: var(--git-primary); }
}

.user-info {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: var(--git-text-1);
  cursor: pointer;

  .caret { font-size: 12px; color: var(--git-text-3); }
}
</style>
