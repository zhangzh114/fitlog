// src/api/fitness.js
// 所有后端接口集中在这里（仿 ai_emotion 的 api 分层）
// 页面里只调用这些函数，不关心 URL 细节

import service from '@/utils/request'

// ---------------- 认证 ----------------

// 注册
export const register = (data) => {
  return service.post('/auth/register', data)
}

// 登录：返回 { token, userInfo }
export const login = (data) => {
  return service.post('/auth/login', data)
}

// 当前登录用户
export const getMe = () => {
  return service.get('/auth/me')
}

// ---------------- 动作 ----------------

// 我的动作列表（每个动作带 today_sets：今日已完成组数）
export const getExercises = () => {
  return service.get('/exercises')
}

// 添加动作
export const addExercise = (data) => {
  return service.post('/exercises', data)
}

// 删除动作
export const deleteExercise = (id) => {
  return service.delete(`/exercises/${id}`)
}

// ---------------- 组记录 ----------------

// 某个动作的所有组记录
export const getSets = (exerciseId) => {
  return service.get(`/exercises/${exerciseId}/sets`)
}

// ⭐ 记录一组（第几组由后端自动算）
export const addSet = (exerciseId, data) => {
  return service.post(`/exercises/${exerciseId}/sets`, data)
}

// 撤销一组
export const deleteSet = (setId) => {
  return service.delete(`/sets/${setId}`)
}
