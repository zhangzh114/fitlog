import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// vite 配置（仿 ai_emotion）
export default defineConfig({
  plugins: [vue()],
  resolve: {
    // '@' 指向 src，导入时可以写 '@/utils/request'
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 5174, // 用 5174，避开博客项目的 5173
    // 配置代理，解决跨域问题：
    // 前端请求 /api/xxx → 被 Vite 转发到 http://127.0.0.1:8001/api/xxx
    // 浏览器以为是同一个源，所以不会触发跨域拦截
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8001',
        changeOrigin: true,
      },
    },
  },
})
