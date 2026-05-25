<template>
  <el-dialog
    v-model="dialogVisible"
    :title="t('settings.title')"
    width="400px"
    destroy-on-close
  >
    <el-form label-width="80px" class="settings-form">
      <el-form-item :label="t('settings.language')">
        <el-select v-model="currentLocale" style="width: 180px">
          <el-option :label="t('settings.chinese')" value="zh-CN" />
          <el-option :label="t('settings.english')" value="en-US" />
        </el-select>
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="dialogVisible = false">{{ t('common.cancel') }}</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useI18nStore } from '@/stores/i18n'

const props = defineProps({
  visible: { type: Boolean, default: false }
})
const emit = defineEmits(['update:visible'])

const { t } = useI18n()
const i18nStore = useI18nStore()

const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val)
})

const currentLocale = computed({
  get: () => i18nStore.locale,
  set: (val) => i18nStore.setLocale(val)
})
</script>

<style lang="scss" scoped>
.settings-form {
  padding: 8px 0;
}
</style>
