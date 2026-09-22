<!-- src/views/home.vue —— 首页：我的动作列表（今日进度 + 去记录/删除） -->
<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

import { addExercise, deleteExercise, getExercises } from '@/api/fitness'

const router = useRouter()

const exercises = ref([])
const loading = ref(false)

// 新增动作的弹窗
const dialogVisible = ref(false)
const form = reactive({ name: '', target_sets: 4 })
const submitting = ref(false)

async function load() {
  loading.value = true
  try {
    exercises.value = await getExercises()
  } catch {
    // 拦截器已提示
  } finally {
    loading.value = false
  }
}

onMounted(load)

async function handleAdd() {
  if (!form.name.trim()) {
    ElMessage.warning('请输入动作名称')
    return
  }
  submitting.value = true
  try {
    await addExercise({ name: form.name.trim(), target_sets: form.target_sets })
    ElMessage.success('添加成功')
    dialogVisible.value = false
    form.name = ''
    form.target_sets = 4
    load()
  } catch {
    // 拦截器已提示（例如"这个动作已经有了"）
  } finally {
    submitting.value = false
  }
}

async function handleDelete(ex) {
  try {
    await ElMessageBox.confirm(
      `确定删除「${ex.name}」吗？它的组记录也会一起删除`,
      '提示',
      { type: 'warning' }
    )
  } catch {
    return // 用户点了取消
  }
  await deleteExercise(ex.id)
  ElMessage.success('已删除')
  load()
}

// 进度百分比（今日组数 / 目标组数）
function percent(ex) {
  if (!ex.target_sets) return 0
  return Math.min(100, Math.round((ex.today_sets / ex.target_sets) * 100))
}
</script>

<template>
  <div>
    <div class="head">
      <h2>我的动作</h2>
      <el-button type="primary" @click="dialogVisible = true">
        <el-icon><Plus /></el-icon>&nbsp;添加动作
      </el-button>
    </div>

    <p v-if="loading" class="tip">加载中…</p>

    <el-empty v-else-if="exercises.length === 0" description="还没有动作，先添加一个吧（比如：深蹲）" />

    <el-card v-for="ex in exercises" :key="ex.id" class="ex-card" shadow="hover">
      <div class="ex-row">
        <div class="left">
          <div class="name">{{ ex.name }}</div>
          <div class="meta">
            今日进度
            <b>{{ ex.today_sets }}</b> / {{ ex.target_sets }} 组
          </div>
        </div>
        <div class="right">
          <el-button type="primary" @click="router.push(`/record/${ex.id}`)">去记录</el-button>
          <el-button type="danger" plain @click="handleDelete(ex)">删除</el-button>
        </div>
      </div>
      <el-progress :percentage="percent(ex)" :stroke-width="10" style="margin-top: 12px" />
    </el-card>

    <!-- 添加动作弹窗 -->
    <el-dialog v-model="dialogVisible" title="添加动作" width="360px">
      <el-form label-position="top">
        <el-form-item label="动作名称">
          <el-input v-model="form.name" placeholder="例如：深蹲、卧推、硬拉" />
        </el-form-item>
        <el-form-item label="计划做几组">
          <el-input-number v-model="form.target_sets" :min="1" :max="20" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleAdd">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style lang="scss" scoped>
.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.tip {
  color: #909399;
  font-size: 14px;
}

.ex-card {
  margin-bottom: 14px;

  .ex-row {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .name {
      font-size: 17px;
      font-weight: 600;
    }

    .meta {
      margin-top: 6px;
      font-size: 13px;
      color: #909399;

      b {
        color: #409eff;
        font-size: 16px;
      }
    }
  }
}
</style>
