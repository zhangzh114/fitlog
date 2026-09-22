<!-- src/views/record.vue —— ⭐ 核心页面：记录组数 -->
<!-- 流程：设置重量/次数 → 点"完成一组" → 后端算出第几组 → 下方列表实时更新 -->

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import { addSet, deleteSet, getExercises, getSets } from '@/api/fitness'

const props = defineProps({
  id: { type: [String, Number], required: true }, // 路由参数 :id
})

const router = useRouter()

const exercise = ref(null)
const sets = ref([])
const loading = ref(true)
const saving = ref(false)

// 本次要记录的数据（默认值给个常见重量/次数，方便快速点）
const weight = ref(60)
const reps = ref(10)

// 下一组是第几组（当前最大组号 + 1，和后端算法一致）
const nextSetNumber = computed(() => {
  if (sets.value.length === 0) return 1
  return Math.max(...sets.value.map((s) => s.set_number)) + 1
})

// 上一组（用来给用户参考：上次做了多重）
const lastSet = computed(() => sets.value[sets.value.length - 1] || null)

async function load() {
  loading.value = true
  try {
    const list = await getExercises()
    exercise.value = list.find((e) => e.id === Number(props.id)) || null
    sets.value = await getSets(props.id)
    // 用最后一组的重量/次数作为下一次的默认值，减少输入
    if (lastSet.value) {
      weight.value = lastSet.value.weight
      reps.value = lastSet.value.reps
    }
  } catch {
    // 拦截器已提示
  } finally {
    loading.value = false
  }
}

onMounted(load)

// ⭐ 完成一组
async function handleAddSet() {
  saving.value = true
  try {
    const res = await addSet(props.id, { weight: weight.value, reps: reps.value })
    ElMessage.success(`第 ${res.set_number} 组已记录 💪`)
    sets.value = await getSets(props.id) // 重新拉列表，保证和后端一致
  } catch {
    // 拦截器已提示
  } finally {
    saving.value = false
  }
}

async function handleDeleteSet(set) {
  await deleteSet(set.id)
  ElMessage.success('已撤销')
  sets.value = await getSets(props.id)
}
</script>

<template>
  <div>
    <el-page-header content="记录组数" @back="router.push('/')" style="margin-bottom: 16px" />

    <p v-if="loading" class="tip">加载中…</p>

    <el-empty v-else-if="!exercise" description="找不到这个动作">
      <el-button type="primary" @click="router.push('/')">回首页</el-button>
    </el-empty>

    <template v-else>
      <!-- 动作信息 -->
      <el-card class="card">
        <div class="ex-head">
          <div>
            <div class="ex-name">{{ exercise.name }}</div>
            <div class="ex-meta">
              今日已做 <b>{{ exercise.today_sets }}</b> 组 · 目标 {{ exercise.target_sets }} 组
            </div>
          </div>
          <div class="next">下一组：<b>第 {{ nextSetNumber }} 组</b></div>
        </div>
      </el-card>

      <!-- 记录区 -->
      <el-card class="card">
        <div class="inputs">
          <div class="input-item">
            <label>重量 (kg)</label>
            <el-input-number v-model="weight" :min="0" :max="1000" size="large" />
          </div>
          <div class="input-item">
            <label>次数</label>
            <el-input-number v-model="reps" :min="0" :max="1000" size="large" />
          </div>
        </div>

        <div v-if="lastSet" class="last">
          上一组：{{ lastSet.weight }} kg × {{ lastSet.reps }} 次（第 {{ lastSet.set_number }} 组）
        </div>

        <el-button
          class="big-btn"
          type="primary"
          size="large"
          :loading="saving"
          @click="handleAddSet"
        >
          完成一组（第 {{ nextSetNumber }} 组）
        </el-button>
      </el-card>

      <!-- 已记录的组 -->
      <el-card class="card">
        <template #header>已记录 {{ sets.length }} 组</template>

        <el-empty v-if="sets.length === 0" description="还没有记录，点上面的按钮开始" :image-size="80" />

        <div v-else>
          <div v-for="s in sets" :key="s.id" class="set-row">
            <div class="set-no">第 {{ s.set_number }} 组</div>
            <div class="set-detail">{{ s.weight }} kg × {{ s.reps }} 次</div>
            <el-button link type="danger" @click="handleDeleteSet(s)">撤销</el-button>
          </div>
        </div>
      </el-card>
    </template>
  </div>
</template>

<style lang="scss" scoped>
.tip {
  color: #909399;
  font-size: 14px;
}

.card {
  margin-bottom: 16px;
}

.ex-head {
  display: flex;
  align-items: center;
  justify-content: space-between;

  .ex-name {
    font-size: 20px;
    font-weight: 700;
  }

  .ex-meta {
    margin-top: 6px;
    font-size: 13px;
    color: #909399;

    b {
      color: #409eff;
      font-size: 16px;
    }
  }

  .next {
    font-size: 14px;
    color: #606266;

    b {
      color: #e6a23c;
      font-size: 18px;
    }
  }
}

.inputs {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;

  .input-item {
    flex: 1;

    label {
      display: block;
      margin-bottom: 6px;
      font-size: 13px;
      color: #606266;
    }
  }
}

.last {
  font-size: 13px;
  color: #909399;
  margin-bottom: 16px;
}

.big-btn {
  width: 100%;
  height: 56px;
  font-size: 18px;
}

.set-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #f0f2f5;

  &:last-child {
    border-bottom: none;
  }

  .set-no {
    font-weight: 600;
    color: #303133;
    width: 80px;
  }

  .set-detail {
    flex: 1;
    color: #606266;
  }
}
</style>
