<template>
  <div class="homework-container">
    <h2>{{ classCode ? `${classCode}作业` : '作业' }}</h2>
    
    <div v-if="loading" class="loading-container">
      <el-loading />
    </div>
    
    <template v-else>
      <div v-if="currentTabDuration > 0" class="total-duration">
        <el-alert
          :title="activeTab === '日常' ? '日常作业时间预估' : '周末作业时间预估'"
          type="warning"
          :description="`完成${activeTab === '日常' ? '日常' : '周末'}作业预计需要 ${currentTabDuration} 分钟（${Math.round(currentTabDuration/60 * 10) / 10} 小时）`"
          show-icon
        />
      </div>

      <el-tabs v-model="activeTab" class="homework-tabs">
        <el-tab-pane label="日常作业" name="日常">
          <el-empty v-if="!homework.日常 || homework.日常.length === 0" description="暂无日常作业" />
          <el-table
            v-else
            :data="homework.日常"
            style="width: 100%"
            :default-sort="{ prop: 'deadline', order: 'ascending' }"
            border
            stripe
          >
            <el-table-column prop="subject" label="科目" width="100">
              <template #default="scope">
                <span class="subject-label" :class="getSubjectClass(scope.row.subject)">
                  {{ scope.row.subject }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="content" label="作业内容" min-width="300">
              <template #default="scope">
                <div class="content-cell">{{ scope.row.content }}</div>
              </template>
            </el-table-column>
            <el-table-column prop="teacher" label="任课教师" width="100" />
            <el-table-column prop="duration" label="预计用时" width="120" sortable>
              <template #default="scope">
                {{ scope.row.duration }} 分钟
              </template>
            </el-table-column>
            <el-table-column prop="deadline" label="上交日期" width="120" sortable>
              <template #default="scope">
                <span :class="{ 'urgent': isUrgent(scope.row.deadline) }">
                  {{ scope.row.deadline }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="assigned_date" label="布置日期" width="120" />
          </el-table>
        </el-tab-pane>
        
        <el-tab-pane label="周末作业" name="周末">
          <el-empty v-if="!homework.周末 || homework.周末.length === 0" description="暂无周末作业" />
          <el-table
            v-else
            :data="homework.周末"
            style="width: 100%"
            :default-sort="{ prop: 'deadline', order: 'ascending' }"
            border
            stripe
          >
            <el-table-column prop="subject" label="科目" width="100">
              <template #default="scope">
                <span class="subject-label" :class="getSubjectClass(scope.row.subject)">
                  {{ scope.row.subject }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="content" label="作业内容" min-width="300">
              <template #default="scope">
                <div class="content-cell">{{ scope.row.content }}</div>
              </template>
            </el-table-column>
            <el-table-column prop="teacher" label="任课教师" width="100" />
            <el-table-column prop="duration" label="预计用时" width="120" sortable>
              <template #default="scope">
                {{ scope.row.duration }} 分钟
              </template>
            </el-table-column>
            <el-table-column prop="deadline" label="上交日期" width="120" sortable>
              <template #default="scope">
                <span :class="{ 'urgent': isUrgent(scope.row.deadline) }">
                  {{ scope.row.deadline }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="assigned_date" label="布置日期" width="120" />
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElLoading, ElMessage, ElEmpty, ElTabs, ElTabPane, ElTable, ElTableColumn, ElAlert } from 'element-plus'
import api from '../utils/api'

const loading = ref(false)
const activeTab = ref('日常')
const homework = ref({
  日常: [],
  周末: []
})
const classCode = ref('') // 班级代码

// 计算日常作业总时长
const dailyDuration = computed(() => {
  return homework.value.日常?.reduce((total, item) => total + item.duration, 0) || 0
})

// 计算周末作业总时长
const weeklyDuration = computed(() => {
  return homework.value.周末?.reduce((total, item) => total + item.duration, 0) || 0
})

// 根据当前选中的标签页显示对应类型的作业总时长
const currentTabDuration = computed(() => {
  return activeTab.value === '日常' ? dailyDuration.value : weeklyDuration.value
})

// 计算所有作业总时长（保留原有的totalDuration以备他用）
const totalDuration = computed(() => {
  return dailyDuration.value + weeklyDuration.value
})

const getClassCode = () => {
  const code = document.cookie.split('; ').find(row => row.startsWith('classCode='))
  return code ? code.split('=')[1] : null
}

const getSubjectClass = (subject) => {
  const classes = {
    '语文': 'subject-chinese',
    '数学': 'subject-math',
    '英语': 'subject-english',
    '物理': 'subject-physics',
    '化学': 'subject-chemistry',
    '生物': 'subject-biology',
    '政治': 'subject-politics',
    '历史': 'subject-history',
    '地理': 'subject-geography'
  }
  return classes[subject] || 'subject-default'
}

const isUrgent = (deadline) => {
  const now = new Date()
  const dueDate = new Date(deadline)
  const diffDays = Math.ceil((dueDate - now) / (1000 * 60 * 60 * 24))
  return diffDays <= 2 && diffDays >= 0
}

const fetchHomework = async () => {
  const classCode = getClassCode()
  if (!classCode) {
    ElMessage.warning('请先选择班级')
    return
  }

  loading.value = true
  try {
    const response = await api.get(`/api/homework/${classCode}`)
    homework.value = response.data
  } catch (error) {
    console.error('Error fetching homework:', error)
    ElMessage.error('获取作业列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchHomework()
  classCode.value = getClassCode() // 获取班级代码
})

</script>

<style scoped>
.homework-container {
  padding: 1rem;
}

.homework-tabs {
  margin-top: 1rem;
}

.total-duration {
  margin-bottom: 1rem;
}

.content-cell {
  white-space: pre-wrap;
  word-break: break-all;
  line-height: 1.5;
  padding: 8px 0;
}

.urgent {
  color: #F56C6C;
  font-weight: bold;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

:deep(.el-table) {
  margin-top: 1rem;
}

:deep(.el-table__header) {
  background-color: #f5f7fa;
}

:deep(.el-table__row) {
  cursor: pointer;
}

:deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

/* 科目标签样式 */
.subject-label {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  color: #fff;
  font-size: 13px;
  line-height: 1.2;
  text-align: center;
  white-space: nowrap;
}

.subject-chinese {
  background-color: #67C23A;
}

.subject-math {
  background-color: #E6A23C;
}

.subject-english {
  background-color: #F56C6C;
}

.subject-physics {
  background-color: #409EFF;
}

.subject-chemistry {
  background-color: #9B59B6;
}

.subject-biology {
  background-color: #2ECC71;
}

.subject-politics {
  background-color: #FF9800;
}

.subject-history {
  background-color: #795548;
}

.subject-geography {
  background-color: #607D8B;
}

.subject-default {
  background-color: #909399;
}

/* 移动设备适配 */
@media screen and (max-width: 768px) {
  .homework-container {
    padding: 0.5rem;
  }

  :deep(.el-table) {
    font-size: 14px;
  }

  :deep(.el-table .cell) {
    padding: 8px 4px;
  }

  .content-cell {
    font-size: 14px;
    padding: 4px 0;
  }

  :deep(.el-alert) {
    padding: 8px 12px;
  }

  :deep(.el-alert__title) {
    font-size: 13px;
  }

  :deep(.el-alert__description) {
    font-size: 12px;
    margin: 5px 0 0;
  }

  :deep(.el-tabs__item) {
    font-size: 14px;
    padding: 0 10px;
  }

  .subject-label {
    padding: 2px 6px;
    font-size: 12px;
  }
}
</style>
