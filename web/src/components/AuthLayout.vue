<!-- src/components/AuthLayout.vue —— 登录/注册用的居中布局（仿 ai_emotion 的 AuthLayout） -->
<script setup></script>

<template>
  <div class="auth-layout">
    <div class="auth-box">
      <h1 class="logo">🏋️ Fitlog健身日志</h1>
      <p class="slogan">记录每一个动作做到了第几组</p>
      <!-- 子路由（登录/注册页）显示在这里 -->
      <router-view />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #eef2ff 0%, #f5f7fa 100%);

  .auth-box {
    width: 420px;
    padding: 40px;
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
    text-align: center;

    .logo {
      font-size: 28px;
      margin-bottom: 8px;
    }

    .slogan {
      color: #909399;
      font-size: 14px;
      margin-bottom: 28px;
    }
  }
}
</style>
