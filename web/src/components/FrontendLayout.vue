<!-- src/components/FrontendLayout.vue —— 主布局：顶部导航 + 页面内容（仿 ai_emotion 的 FrontendLayout） -->
<script setup>
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import { useUserStore } from '@/stores/user'
import { APP_NAME } from '@/config'

const router = useRouter()
const userStore = useUserStore()

function handleLogout() {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/auth/login')
}
</script>

<template>
  <div class="layout">
    <header class="navbar">
      <div class="brand" @click="router.push('/')">🏋️ {{ APP_NAME }}</div>
      <div class="right">
        <span class="username">{{ userStore.userInfo?.username }}</span>
        <el-button link type="primary" @click="handleLogout">退出登录</el-button>
      </div>
    </header>

    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style lang="scss" scoped>
.layout {
  min-height: 100vh;

  .navbar {
    height: 60px;
    padding: 0 24px;
    background: #fff;
    border-bottom: 1px solid #e4e7ed;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 10;

    .brand {
      font-size: 18px;
      font-weight: 700;
      color: #409eff;
      cursor: pointer;
    }

    .right {
      display: flex;
      align-items: center;
      gap: 12px;

      .username {
        color: #606266;
        font-size: 14px;
      }
    }
  }

  .content {
    max-width: 720px;
    margin: 0 auto;
    padding: 24px 16px 48px;
  }
}
</style>
