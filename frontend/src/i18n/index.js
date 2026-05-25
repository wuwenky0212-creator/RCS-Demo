import { createI18n } from 'vue-i18n'
import zhCN from '../locales/zh-CN.json'
import enUS from '../locales/en-US.json'

/**
 * Vue I18n 实例配置
 * 
 * 功能：
 * - 支持中文（zh-CN）和英文（en-US）两种语言
 * - 默认语言为中文（zh-CN）
 * - 启用后备机制：缺失的翻译键返回键名本身
 * - 在开发模式下对缺失的翻译键输出警告
 * 
 * 需求：8.1, 8.3, 8.4, 8.5
 */

const i18n = createI18n({
  // 使用 Composition API 模式
  legacy: false,
  
  // 全局注入 $t 函数
  globalInjection: true,
  
  // 默认语言为中文
  locale: 'zh-CN',
  
  // 后备语言为中文
  fallbackLocale: 'zh-CN',
  
  // 翻译消息
  messages: {
    'zh-CN': zhCN,
    'en-US': enUS
  },
  
  // 缺失翻译键时的处理
  // 返回键名本身作为后备（需求 8.3）
  missingWarn: true, // 开发模式下警告（需求 8.4）
  fallbackWarn: true, // 后备警告
  
  // 在生产环境中禁用警告
  silentTranslationWarn: process.env.NODE_ENV === 'production',
  silentFallbackWarn: process.env.NODE_ENV === 'production'
})

export default i18n
