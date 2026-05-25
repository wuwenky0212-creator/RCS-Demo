import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import VueI18nPlugin from '@intlify/unplugin-vue-i18n/vite'
import path from 'node:path'

// RCS-Demo 前端构建配置
// - 端口 5173
// - /api 代理到本地 FastAPI 后端 8000 端口
// - Vue I18n 插件支持多语言
export default defineConfig({
  plugins: [
    vue(),
    VueI18nPlugin({
      // 指定 i18n 资源文件路径
      include: [path.resolve(__dirname, 'src/locales/**')],
      // 启用 Composition API 模式
      compositionOnly: true,
      // 在生产环境中移除警告
      dropMessageCompiler: true
    })
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  },
  test: {
    environment: 'happy-dom',
    globals: true
  }
})
