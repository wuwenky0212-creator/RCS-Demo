<template>
  <!-- ElConfigProvider provides dynamic Element Plus locale (Requirements 5.2, 12.2) -->
  <el-config-provider :locale="elementPlusLocale">
    <router-view />
  </el-config-provider>
</template>

<script setup>
import { computed } from 'vue'
import { ElConfigProvider } from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import en from 'element-plus/es/locale/lang/en'
import { useI18nStore } from './stores/i18n'

const i18nStore = useI18nStore()

// Initialize locale synchronously
i18nStore.initLocale()

// Computed Element Plus locale based on i18n store (Requirements 5.2, 12.2, 12.5)
const elementPlusLocale = computed(() => {
  return i18nStore.locale === 'en-US' ? en : zhCn
})
</script>

<style lang="scss">
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei',
    'Helvetica Neue', Helvetica, Arial, sans-serif;
  background: var(--git-bg);
  color: var(--git-text-1);
}
</style>
