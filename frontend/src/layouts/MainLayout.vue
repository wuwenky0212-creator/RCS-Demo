<template>
  <div class="git-app-shell">
    <TopNav />

    <div class="git-body">
      <!-- 左侧两条工具栏（占位，对齐原图收藏/新增图标列） -->
      <div class="git-rail">
        <div class="rail-icon"><el-icon><Star /></el-icon></div>
        <div class="rail-icon"><el-icon><Plus /></el-icon></div>
      </div>

      <!-- 后线工作台子菜单 -->
      <WorkbenchSidebar v-if="showWorkbenchSidebar" />

      <!-- 基础数据子菜单 -->
      <BaseDataSidebar v-if="showBaseDataSidebar" />

      <!-- 查询统计子菜单 -->
      <QuerySidebar v-if="showQuerySidebar" />

      <!-- 头寸管理子菜单 -->
      <PositionSidebar v-if="showPositionSidebar" />


      <!-- 主内容区 -->
      <main class="git-main">
        <!-- Tab 标题条 -->
        <div class="git-tabbar">
          <div class="tab-item active">
            <el-icon><UserFilled /></el-icon>
            <span>{{ currentTabTitle }}</span>
          </div>

          <div class="tabbar-tools">
            <el-icon class="tool"><RefreshRight /></el-icon>
            <el-icon class="tool"><CopyDocument /></el-icon>
            <el-icon class="tool"><Delete /></el-icon>
            <el-icon class="tool"><FullScreen /></el-icon>
          </div>
        </div>

        <div class="git-page" :class="{ 'git-page--no-pad': isTradeEntry }">
          <router-view />
        </div>
      </main>
    </div>

    <footer class="git-footer">
      {{ t('layout.footerCopyright') }}　{{ buildTime }}　V20260508112645
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  Star, Plus, UserFilled, RefreshRight, CopyDocument, Delete, FullScreen
} from '@element-plus/icons-vue'
import TopNav from '@/components/TopNav.vue'
import WorkbenchSidebar from '@/components/WorkbenchSidebar.vue'
import BaseDataSidebar from '@/components/BaseDataSidebar.vue'
import QuerySidebar from '@/components/QuerySidebar.vue'
import PositionSidebar from '@/components/PositionSidebar.vue'

const route = useRoute()
const { t } = useI18n()

const showWorkbenchSidebar = computed(() => route.path.startsWith('/workbench'))
const showBaseDataSidebar  = computed(() => route.path.startsWith('/base-data'))
const showQuerySidebar     = computed(() => route.path.startsWith('/statistics'))
const showPositionSidebar  = computed(() => route.path.startsWith('/position'))
const isTradeEntry         = computed(() => route.path.startsWith('/trade-entry'))

const currentTabTitle = computed(() => {
  const name = route.name
  if (name && t(`layout.routeTitle.${name}`) !== `layout.routeTitle.${name}`) {
    return t(`layout.routeTitle.${name}`)
  }
  return route.meta?.title || t('layout.routeTitle.home')
})

// 简单格式化构建时间，避免 SSR 不一致
const buildTime = (() => {
  const d = new Date()
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
})()
</script>

<style lang="scss" scoped>
.git-app-shell {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--git-bg);
}

.git-body {
  flex: 1;
  display: flex;
  min-height: 0;
}

.git-rail {
  width: 36px;
  background: #ffffff;
  border-right: 1px solid var(--git-border);
  padding: 8px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;

  .rail-icon {
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    color: var(--git-text-2);
    cursor: pointer;
    font-size: 14px;

    &:hover { background: #f2f4f7; color: var(--git-primary); }
  }
}

.git-main {
  flex: 1;
  min-height: 0;        /* 允许高度被 flex 算法压缩，激活下层滚动 */
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.git-tabbar {
  height: 36px;
  background: #ffffff;
  border-bottom: 1px solid var(--git-border);
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  padding: 0 12px 0 0;

  .tab-item {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 0 18px;
    height: 100%;
    color: var(--git-text-2);
    font-size: 13px;
    border-right: 1px solid var(--git-border);
    cursor: pointer;

    &.active {
      color: var(--git-primary);
      background: #f5f9ff;
      position: relative;

      &::after {
        content: '';
        position: absolute;
        left: 0; right: 0; bottom: -1px;
        height: 2px;
        background: var(--git-primary);
      }
    }
  }

  .tabbar-tools {
    display: flex;
    align-items: center;
    gap: 14px;

    .tool {
      font-size: 16px;
      color: var(--git-text-3);
      cursor: pointer;

      &:hover { color: var(--git-primary); }
    }
  }
}

.git-page {
  flex: 1;
  overflow: auto;
  padding: 12px;

  &--no-pad {
    padding: 0;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }
}

.git-footer {
  height: 30px;
  line-height: 30px;
  background: #ffffff;
  border-top: 1px solid var(--git-border);
  text-align: left;
  padding-left: 24px;
  color: var(--git-text-3);
  font-size: 12px;
}
</style>
