<!-- src/views/login.vue —— 登录页（仿 ai_emotion 的 login.vue：el-form + rules + 拦截器） -->
<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import { login } from '@/api/fitness'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const ruleFormRef = ref(null) // 表单引用：用来调用 validate()

const formData = reactive({
  username: '',
  password: '',
})

// 表单校验规则（prop 名要和 formData 的字段名对上）
const rules = reactive({
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
})

const submitForm = async (formRef) => {
  if (!formRef) return
  await formRef.validate((valid) => {
    if (!valid) return
    // login 返回的是拆完信封的 data：{ token, userInfo }
    login(formData)
      .then((data) => {
        userStore.setAuth(data.token, data.userInfo)
        ElMessage.success('登录成功')
        router.push('/')
      })
      .catch(() => {
        // 错误提示已经在 request.js 拦截器里统一弹过了，这里不用重复
      })
  })
}
</script>

<template>
  <el-form ref="ruleFormRef" :model="formData" :rules="rules" label-position="top">
    <el-form-item label="用户名" prop="username">
      <el-input v-model="formData.username" placeholder="请输入用户名" />
    </el-form-item>

    <el-form-item label="密码" prop="password">
      <el-input v-model="formData.password" type="password" placeholder="请输入密码" show-password />
    </el-form-item>

    <el-button class="btn" type="primary" size="large" @click="submitForm(ruleFormRef)">
      登录
    </el-button>

    <div class="footer">
      还没有账号？<router-link to="/auth/register">去注册</router-link>
    </div>
  </el-form>
</template>

<style lang="scss" scoped>
.btn {
  width: 100%;
  margin-top: 8px;
}

.footer {
  margin-top: 20px;
  font-size: 14px;
  color: #606266;
}
</style>
