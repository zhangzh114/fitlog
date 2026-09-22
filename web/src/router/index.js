// src/router/index.js
// 路由表 + 路由守卫（仿 ai_emotion 的布局组件写法）

import { createRouter, createWebHistory } from 'vue-router'
import AuthLayout from '@/components/AuthLayout.vue'
import FrontendLayout from '@/components/FrontendLayout.vue'

// 需要在"主布局"里显示的页面（必须先登录）
const frontendRoutes = [
  {
    path: '/',
    component: FrontendLayout,
    children: [
      {
        path: '',
        component: () => import('@/views/home.vue'),
        meta: { title: '我的动作' },
      },
      {
        path: 'record/:id',
        component: () => import('@/views/record.vue'),
        props: true, // 把路由参数 id 直接传给组件的 props
        meta: { title: '记录组数' },
      },
    ],
  },
]

// 登录/注册页（用另一个居中布局，不需要登录）
const authRoutes = [
  {
    path: '/auth',
    component: AuthLayout,
    children: [
      {
        path: 'login',
        component: () => import('@/views/login.vue'),
        meta: { title: '登录' },
      },
      {
        path: 'register',
        component: () => import('@/views/register.vue'),
        meta: { title: '注册' },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes: [...frontendRoutes, ...authRoutes],
})

// 路由前置守卫：没登录的人不许进主页面；已登录的人不用再去登录页
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const isAuthPage = to.path.startsWith('/auth')

  if (!token && !isAuthPage) {
    next('/auth/login') // 没令牌：赶去登录
  } else if (token && isAuthPage) {
    next('/') // 已登录：别停在登录页
  } else {
    next() // 其他情况放行
  }
})

export default router
