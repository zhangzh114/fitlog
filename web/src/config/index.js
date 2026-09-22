// src/config/index.js
// 公共配置（仿 ai_emotion 的 config 目录）

// 应用名（显示在标题/导航栏）
export const APP_NAME = 'Fitlog健身日志'

// 后端地址：因为 vite.config.js 配了代理，这里写 '/api' 就够
// （真实请求会被 Vite 转发到 http://127.0.0.1:8001）
export const API_PREFIX = '/api'
