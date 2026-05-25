import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'
import i18n from './i18n'
import './styles/global.scss'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(i18n)

// Element Plus is configured without a fixed locale here.
// Dynamic locale is handled by <el-config-provider> in App.vue (Requirements 5.2, 12.2)
app.use(ElementPlus)

// 注册全部 Element Plus 图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.mount('#app')
