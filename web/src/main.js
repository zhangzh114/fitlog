// src/main.js —— 应用入口（仿 ai_emotion：注册 Element Plus + 图标 + pinia + router）

import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)

// 把所有 Element Plus 图标注册成全局组件，模板里可直接 <el-icon><Plus /></el-icon>
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(ElementPlus).use(createPinia()).use(router).mount('#app')
