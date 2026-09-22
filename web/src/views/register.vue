<!-- src/views/register.vue —— 注册页（和登录页几乎一样，多了"确认密码"校验） -->
<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import { register } from '@/api/fitness'

const router = useRouter()
const ruleFormRef = ref(null)

const formData = reactive({
  username: '',
  password: '',
  confirmPassword: '',
})

// 自定义校验：确认密码要和密码一致
const validateConfirm = (rule, value, callback) => {
  if (value !== formData.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 50, message: '用户名 2~50 个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 64, message: '密码至少 6 位', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validateConfirm, trigger: 'blur' },
  ],
})

const submitForm = async (formRef) => {
  if (!formRef) return
  await formRef.validate((valid) => {
    if (!valid) return
    // 只把后端需要的字段发过去（不带 confirmPassword）
    register({ username: formData.username, password: formData.password })
      .then(() => {
        ElMessage.success('注册成功，请登录')
        router.push('/auth/login')
      })
      .catch(() => {})
  })
}
</script>

<template>
  <el-form ref="ruleFormRef" :model="formData" :rules="rules" label-position="top">
    <el-form-item label="用户名" prop="username">
      <el-input v-model="formData.username" placeholder="2~50 个字符" />
    </el-form-item>

    <el-form-item label="密码" prop="password">
      <el-input v-model="formData.password" type="password" placeholder="至少 6 位" show-password />
    </el-form-item>

    <el-form-item label="确认密码" prop="confirmPassword">
      <el-input v-model="formData.confirmPassword" type="password" placeholder="再输一次" show-password />
    </el-form-item>

    <el-button class="btn" type="primary" size="large" @click="submitForm(ruleFormRef)">
      注册
    </el-button>

    <div class="footer">
      已有账号？<router-link to="/auth/login">去登录</router-link>
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
