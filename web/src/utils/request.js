// src/utils/request.js
// axios 封装（仿 ai_emotion 的 utils/request.js）
//
// 三个统一：
//   1. 统一 baseURL（'/api'，由 Vite 代理转发到后端）
//   2. 统一带 token（请求拦截器）
//   3. 统一拆信封 + 统一错误提示（响应拦截器）

import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 实例
const service = axios.create({
  baseURL: '/api', // 所有请求自动加 /api 前缀
  timeout: 5000, // 5 秒超时
})

// ---------- 请求拦截器：发请求之前 ----------
service.interceptors.request.use(
  (config) => {
    // 从 localStorage 取令牌，放进请求头 token（和后端约定一致）
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['token'] = token
    }
    return config
  },
  (error) => Promise.reject(error)
)

// ---------- 响应拦截器：收到响应之后 ----------
service.interceptors.response.use(
  (response) => {
    const { data, config } = response

    // 成功的信封：{ code: '200', data: 真数据, msg: 'success' }
    if (data.code === '200') {
      return data.data // ⭐ 页面拿到的直接是业务数据，看不到信封
    }

    // 登录过期（后端约定用 '-1' 表示）
    if (data.code === '-1') {
      // 如果本来就是在登录接口报的错，就别跳转，只提示
      if (!config.url?.includes('/login')) {
        ElMessage.error(data.msg || '登录过期，请重新登录')
        localStorage.removeItem('token')
        localStorage.removeItem('userInfo')
        window.location.href = '/auth/login'
      } else {
        ElMessage.error(data.msg || '登录失败')
      }
      return Promise.reject(new Error(data.msg || '登录过期'))
    }

    // 其他业务错误：400 / 403 / 404 / 422 …（比参考项目更完整一点）
    ElMessage.error(data.msg || '请求失败')
    return Promise.reject(new Error(data.msg || '请求失败'))
  },
  (error) => {
    // 网络层面的错误（后端没启动、超时等）
    ElMessage.error('网络异常，请检查后端是否启动')
    return Promise.reject(error)
  }
)

export default service
