<template>
  <div class="pnl-subnav">
    <div
      v-for="item in navItems"
      :key="item.name"
      class="nav-item"
      :class="{ active: isActive(item.path) }"
      @click="router.push(item.path)"
    >
      {{ item.label }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()

const navItems = computed(() => [
  { label: t('pnlSidebar.productMaintenance'),  path: '/pnl-attribution/product-maintenance' },
  { label: t('pnlSidebar.scenarioQuery'),       path: '/pnl-attribution/scenario-query' },
  { label: t('pnlSidebar.attributionReport'),   path: '/pnl-attribution/attribution-report' },
])

function isActive(path) {
  return route.path === path || route.path.startsWith(path + '/')
}
</script>

<style lang="scss" scoped>
.pnl-subnav {
  display: flex;
  gap: 0;
  border-bottom: 1px solid var(--git-border);
  margin-bottom: 16px;
  background: #fff;
  padding: 0 4px;
}

.nav-item {
  padding: 10px 20px;
  font-size: 13px;
  color: var(--git-text-2);
  cursor: pointer;
  position: relative;
  white-space: nowrap;
  transition: color 0.15s;

  &:hover {
    color: var(--git-primary);
  }

  &.active {
    color: var(--git-primary);
    font-weight: 600;

    &::after {
      content: '';
      position: absolute;
      left: 0;
      right: 0;
      bottom: -1px;
      height: 2px;
      background: var(--git-primary);
      border-radius: 1px 1px 0 0;
    }
  }
}
</style>
