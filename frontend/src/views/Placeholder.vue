<template>
  <div class="placeholder">
    <el-empty
      :description="`「${title}」 — ${t('placeholder.comingSoon')}`"
    >
      <template #image>
        <el-icon style="font-size: 80px; color: #c0c4cc;">
          <Tools />
        </el-icon>
      </template>
      <p style="color: #909399; font-size: 13px;">
        {{ t('placeholder.demoNote') }}
      </p>
    </el-empty>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { Tools } from '@element-plus/icons-vue'

const route = useRoute()
const { t } = useI18n()
const title = computed(() => route.meta?.title || '—')
</script>

<style lang="scss" scoped>
.placeholder {
  background: var(--git-surface);
  border-radius: 6px;
  padding: 60px 24px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
