<template>
  <div class="current-classes">
    <!-- 当前课程部分 -->
    <el-card class="box-card mb-4" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <span class="title">当前课程</span>
            <span class="user-info" v-if="isLoggedIn">
              用户: <el-tag size="small" type="success">{{ username }}</el-tag>
            </span>
          </div>
          <div class="header-right">
            <el-button type="primary" size="small" @click="fetchCurrentClasses" :loading="loading">
              刷新
            </el-button>
            <el-button 
              v-if="isLoggedIn" 
              type="danger" 
              size="small" 
              @click="handleLogout"
            >
              退出登录
            </el-button>
          </div>
        </div>
      </template>
      <el-table 
        v-loading="loading" 
        :data="currentClassesArray" 
        style="width: 100%"
        :header-cell-style="{ background: '#f5f7fa', color: '#606266' }"
      >
        <el-table-column prop="className" label="班级" width="120">
          <template #default="{ row }">
            <span class="class-name">{{ row.className }}</span>
          </template>
        </el-table-column>
        <!-- <el-table-column prop="currentCourse" label="当前课程" width="120">
          <template #default="{ row }">
            <span class="course-name">{{ row.currentCourse }}</span>
          </template> -->
        <!-- </el-table-column> -->
        <el-table-column prop="teacher" label="任课教师" width="120">
          <template #default="{ row }">
            <span class="teacher-name">{{ row.teacher }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="subject" label="学科" width="120">
          <template #default="{ row }">
            <span class="subject-name">{{ row.subject }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="period" label="课节" width="120">
          <template #default="{ row }">
            <span class="period-name">{{ row.period }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="time" label="时间" min-width="180">
          <template #default="{ row }">
            <span class="time-range">{{ periods[row.period] || '' }}</span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 教师课表部分 -->
    <el-card class="box-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span class="title">教师课表</span>
          <div class="header-right">
            <el-input 
              v-model="teacherSearch" 
              placeholder="搜索教师" 
              style="width: 200px; margin-left: 10px"
            />
            <el-select
              v-model="selectedTeacher"
              placeholder="选择教师"
              style="width: 200px"
              @change="handleTeacherChange"
              :filter-method="filterTeachers"
            >
              <el-option
                v-for="teacher in filteredTeachers"
                :key="teacher"
                :label="teacher"
                :value="teacher"
              />
            </el-select>
            <el-button-group>
              <el-button 
                :type="isNextWeek ? 'default' : 'primary'" 
                size="small" 
                @click="toggleWeek(false)"
                :disabled="!selectedTeacher"
              >
                本周
              </el-button>
              <el-button 
                :type="isNextWeek ? 'primary' : 'default'" 
                size="small" 
                @click="toggleWeek(true)"
                :disabled="!selectedTeacher"
              >
                下周
              </el-button>
            </el-button-group>
            <el-button 
              type="primary" 
              size="small" 
              @click="refreshSchedule" 
              :loading="teacherScheduleLoading"
            >
              刷新
            </el-button>
          </div>
        </div>
      </template>
      <div v-loading="teacherScheduleLoading">
        <template v-if="teacherSchedule">
          <el-table 
            :data="formatTeacherSchedule" 
            style="width: 100%; text-align: center;"
            :header-cell-style="{ background: '#f5f7fa', color: '#606266' }"
            border
          >
            <el-table-column prop="period" label="节次" width="120" fixed="left">
              <template #default="{ row }">
                <div class="period-cell">
                  <span class="period-name">{{ row.period }}</span>
                  <span class="time-range">{{ periods[row.period] || '' }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="monday" label="星期一" min-width="120">
              <template #default="{ row }">
                <template v-if="row.monday">
                  <div v-for="(item, index) in parseScheduleCell(row.monday)" :key="index" class="schedule-cell" style="display: flex; flex-direction: column;">
                    <el-tag size="small" effect="plain" class="class-tag">{{ item.class_code }}</el-tag>
                    <el-tag size="small" effect="plain" type="success" class="subject-tag">{{ item.subject }}</el-tag>
                  </div>
                </template>
              </template>
            </el-table-column>
            <el-table-column prop="tuesday" label="星期二" min-width="120">
              <template #default="{ row }">
                <template v-if="row.tuesday">
                  <div v-for="(item, index) in parseScheduleCell(row.tuesday)" :key="index" class="schedule-cell" style="display: flex; flex-direction: column;">
                    <el-tag size="small" effect="plain" class="class-tag">{{ item.class_code }}</el-tag>
                    <el-tag size="small" effect="plain" type="success" class="subject-tag">{{ item.subject }}</el-tag>
                  </div>
                </template>
              </template>
            </el-table-column>
            <el-table-column prop="wednesday" label="星期三" min-width="120">
              <template #default="{ row }">
                <template v-if="row.wednesday">
                  <div v-for="(item, index) in parseScheduleCell(row.wednesday)" :key="index" class="schedule-cell" style="display: flex; flex-direction: column;">
                    <el-tag size="small" effect="plain" class="class-tag">{{ item.class_code }}</el-tag>
                    <el-tag size="small" effect="plain" type="success" class="subject-tag">{{ item.subject }}</el-tag>
                  </div>
                </template>
              </template>
            </el-table-column>
            <el-table-column prop="thursday" label="星期四" min-width="120">
              <template #default="{ row }">
                <template v-if="row.thursday">
                  <div v-for="(item, index) in parseScheduleCell(row.thursday)" :key="index" class="schedule-cell" style="display: flex; flex-direction: column;">
                    <el-tag size="small" effect="plain" class="class-tag">{{ item.class_code }}</el-tag>
                    <el-tag size="small" effect="plain" type="success" class="subject-tag">{{ item.subject }}</el-tag>
                  </div>
                </template>
              </template>
            </el-table-column>
            <el-table-column prop="friday" label="星期五" min-width="120">
              <template #default="{ row }">
                <template v-if="row.friday">
                  <div v-for="(item, index) in parseScheduleCell(row.friday)" :key="index" class="schedule-cell" style="display: flex; flex-direction: column;">
                    <el-tag size="small" effect="plain" class="class-tag">{{ item.class_code }}</el-tag>
                    <el-tag size="small" effect="plain" type="success" class="subject-tag">{{ item.subject }}</el-tag>
                  </div>
                </template>
              </template>
            </el-table-column>
          </el-table>
        </template>
        <el-empty v-else description="请选择教师查看课表" />
      </div>
    </el-card>

    <!-- 登录对话框 -->
    <el-dialog 
      v-model="showLoginDialog" 
      title="登录" 
      :width="isMobile ? '90%' : '400px'"
      class="login-dialog"
    >
      <el-form :model="loginForm" :rules="loginRules" ref="loginFormRef">
        <el-form-item prop="username" label="用户">
          <el-input v-model="loginForm.username" />
        </el-form-item>
        <el-form-item prop="password" label="密码">
          <el-input v-model="loginForm.password" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showLoginDialog = false">取消</el-button>
        <el-button type="primary" @click="handleLogin" :loading="loginLoading">登录</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../utils/api'

// 数据定义
const currentClasses = ref({})
const loading = ref(false)
const teachers = ref([])
const selectedTeacher = ref('')
const teacherSchedule = ref(null)
const teacherScheduleLoading = ref(false)
const showLoginDialog = ref(false)
const loginLoading = ref(false)
const periods = ref({})
const loginForm = ref({
  username: '',
  password: ''
})
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}
const username = ref('') // 用户名
const teacherSearch = ref('')
const isNextWeek = ref(false)

// 将对象格式的当前课程数据转换为数组格式
const currentClassesArray = computed(() => {
  return Object.entries(currentClasses.value).map(([className, data]) => ({
    className,
    ...data
  }))
})

// 解析课表单元格数据
const parseScheduleCell = (cellData) => {
  if (!cellData) return []
  return cellData.split(', ').map(item => {
    const [class_code, subject] = item.split(' ')
    return { class_code, subject }
  })
}

// 格式化教师课表数据
const formatTeacherSchedule = computed(() => {
  if (!teacherSchedule.value) return []
  
  const periodList = Object.keys(periods.value)
  return periodList.map(period => {
    const row = { period }
    const weekdays = {
      '1': 'monday',
      '2': 'tuesday',
      '3': 'wednesday',
      '4': 'thursday',
      '5': 'friday'
    }
    
    Object.entries(weekdays).forEach(([dayNumber, dayName]) => {
      const classes = teacherSchedule.value[dayNumber]?.[period]
      if (classes && classes.length > 0) {
        row[dayName] = classes.map(c => `${c.class_code} ${c.subject}`).join(', ')
      } else {
        row[dayName] = ''
      }
    })
    
    return row
  })
})

// 教师搜索
const filteredTeachers = computed(() => {
  if (!teacherSearch.value) {
    return teachers.value
  }
  const search = teacherSearch.value.toLowerCase()
  return teachers.value.filter(teacher => 
    teacher.toLowerCase().includes(search)
  )
})

// 教师选择框的过滤方法
const filterTeachers = (query) => {
  const search = query.toLowerCase()
  return teachers.value.filter(teacher => 
    teacher.toLowerCase().includes(search)
  )
}

// 判断是否为移动设备
const isMobile = computed(() => {
  return window.innerWidth <= 768
})

// 监听窗口大小变化
const handleResize = () => {
  // 触发isMobile的重新计算
  window.dispatchEvent(new Event('resize'))
}

// 获取课程时间表
const fetchPeriods = async () => {
  try {
    const response = await api.get('/api/periods')
    periods.value = response.data.periods
  } catch (error) {
    handleApiError(error)
    ElMessage.error('获取课程时间表失败')
  }
}

// 检查登录状态
const checkLoginStatus = () => {
  const token = localStorage.getItem('token')
  if (token) {
    try {
      // 设置 API 请求头
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      
      // 解析用户名
      const base64Url = token.split('.')[1]
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
      const payload = JSON.parse(window.atob(base64))
      username.value = payload.sub
      
      isLoggedIn.value = true
      
      // 设置默认选中的教师为当前登录用户
      selectedTeacher.value = username.value
      
      return true
    } catch (error) {
      console.error('Failed to parse token:', error)
      handleLogout()
      return false
    }
  }else {
    isLoggedIn.value = false
    showLoginDialog.value = true
  }
  return false
}

// 登录处理
const handleLogin = async () => {
  loginLoading.value = true
  try {
    const formData = new URLSearchParams()
    formData.append('username', loginForm.value.username)
    formData.append('password', loginForm.value.password)
    
    const response = await api.post('/api/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    
    if (response.data.access_token) {
      const token = response.data.access_token
      localStorage.setItem('token', token)
      
      // 设置 API 请求头
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      
      // 解析用户名
      const base64Url = token.split('.')[1]
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
      const payload = JSON.parse(window.atob(base64))
      username.value = payload.sub
      
      isLoggedIn.value = true
      showLoginDialog.value = false
      loginForm.value = { username: '', password: '' }
      
      // 登录成功后获取数据
      await fetchTeachers() // 先获取教师列表
      
      // 获取其他数据
      await Promise.all([
        fetchCurrentClasses(),
        fetchTeacherSchedule(username.value), // 获取当前登录用户的课表
        fetchPeriods()
      ])
    }
  } catch (error) {
    handleApiError(error)
    ElMessage.error('登录失败，请检查用户名和密码')
  } finally {
    loginLoading.value = false
  }
}

// 退出登录
const handleLogout = () => {
  localStorage.removeItem('token')
  // 清除 API 请求头
  delete api.defaults.headers.common['Authorization']
  isLoggedIn.value = false
  username.value = ''
  currentClasses.value = []
  teacherSchedule.value = null
  teachers.value = []
  selectedTeacher.value = ''
  showLoginDialog.value = true
}

// API错误处理
const handleApiError = (error) => {
  console.error('API error:', error)
  if (error.response?.status === 401) {
    handleLogout()
    ElMessage.error('登录已过期，请重新登录')
  }
}

// 获取当前各班级课程
const fetchCurrentClasses = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/current-classes')
    currentClasses.value = response.data.current_classes
  } catch (error) {
    handleApiError(error)
    ElMessage.error('获取当前课程信息失败')
  } finally {
    loading.value = false
  }
}

// 获取教师列表
const fetchTeachers = async () => {
  try {
    const response = await api.get('/api/teachers')
    teachers.value = response.data.teachers
  } catch (error) {
    handleApiError(error)
    ElMessage.error('获取教师列表失败')
  }
}

// 获取教师课表
const fetchTeacherSchedule = async (teacherName) => {
  if (!teacherName) {
    teacherSchedule.value = null
    return
  }

  teacherScheduleLoading.value = true
  try {
    const response = await api.get(`/api/teacher-schedule/${teacherName}`)
    teacherSchedule.value = response.data.schedule
  } catch (error) {
    handleApiError(error)
    ElMessage.error('获取教师课表失败')
  } finally {
    teacherScheduleLoading.value = false
  }
}

// 获取下周课表
const fetchNextWeekSchedule = async (teacherName) => {
  if (!teacherName) return
  
  teacherScheduleLoading.value = true
  try {
    const response = await api.get(`/api/teacher-schedule-nextweek/${teacherName}`)
    teacherSchedule.value = response.data.schedule
  } catch (error) {
    handleApiError(error)
    ElMessage.error('获取下周课表失败')
  } finally {
    teacherScheduleLoading.value = false
  }
}

// 切换周次
const toggleWeek = async (nextWeek) => {
  isNextWeek.value = nextWeek
  await refreshSchedule()
}

// 刷新课表
const refreshSchedule = async () => {
  if (selectedTeacher.value) {
    if (isNextWeek.value) {
      await fetchNextWeekSchedule(selectedTeacher.value)
    } else {
      await fetchTeacherSchedule(selectedTeacher.value)
    }
  }
}

// 处理教师选择变更
const handleTeacherChange = async (teacher) => {
  isNextWeek.value = false // 切换教师时重置为本周
  await fetchTeacherSchedule(teacher)
}

// 登录状态
const isLoggedIn = ref(false)

// 添加请求拦截器处理 401 错误
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      handleLogout()
    }
    return Promise.reject(error)
  }
)

// 自动刷新课表
const autoRefreshSchedule = async () => {
  if (isLoggedIn.value && selectedTeacher.value) {
    try {
      await Promise.all([
        fetchCurrentClasses(),
        isNextWeek.value ? 
          fetchNextWeekSchedule(selectedTeacher.value) : 
          fetchTeacherSchedule(selectedTeacher.value)
      ])
    } catch (error) {
      handleApiError(error)
    }
  }
}

// 设置自动刷新
let refreshInterval
onMounted(async () => {
  if (checkLoginStatus()) {
    try {
      await fetchTeachers()
      await Promise.all([
        fetchCurrentClasses(),
        fetchTeacherSchedule(username.value),
        fetchPeriods()
      ])
    } catch (error) {
      handleApiError(error)
    }
  }
  
  // 设置自动刷新
  refreshInterval = setInterval(autoRefreshSchedule, 60000*8)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.current-classes {
  padding: 20px;
}

.box-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .header-right {
    display: flex;
    gap: 10px;
    align-items: center;
    
    @media screen and (max-width: 768px) {
      flex-wrap: wrap;
      justify-content: flex-end;
      
      .el-input,
      .el-select {
        width: 100% !important;
        margin-bottom: 10px;
      }
      
      .el-button-group {
        width: 100%;
        display: flex;
        
        .el-button {
          flex: 1;
        }
      }
    }
  }
}

.title {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.mb-4 {
  margin-bottom: 1rem;
}

.class-name {
  color: #409EFF;
  font-weight: bold;
}

.course-name {
  color: #67C23A;
}

.teacher-name {
  color: #E6A23C;
}

.subject-name {
  color: #F56C6C;
}

.period-name {
  font-weight: bold;
  color: #303133;
  text-align: center;
}

.time-range {
  color: #909399;
  font-size: 12px;
  margin-left: 8px;
}

.schedule-cell {
  padding: 4px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.class-tag {
  color: #409EFF;
  border-color: #409EFF;
}

.subject-tag {
  color: #67C23A;
  border-color: #67C23A;
}

.schedule-cell:not(:last-child) {
  border-bottom: 1px dashed #EBEEF5;
}

.period-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.period-name {
  font-weight: bold;
  color: #303133;
}

.time-range {
  font-size: 12px;
  color: #909399;
}

/* 表格悬浮效果 */
:deep(.el-table__row:hover > td) {
  background-color: #F5F7FA !important;
}

/* 表格单元格内边距 */
:deep(.el-table td) {
  padding: 8px;
}

.user-info {
  font-size: 14px;
  color: #606266;
}

/* 移动设备适配 */
@media screen and (max-width: 768px) {
  .current-classes-container {
    padding: 0.5rem;
  }

  :deep(.el-table) {
    font-size: 14px;
  }

  :deep(.el-table .cell) {
    padding: 8px 4px;
  }

  .class-name, .course-name, .teacher-name, 
  .subject-name, .period-name, .time-range {
    font-size: 14px;
  }

  :deep(.el-dialog__body) {
    padding: 15px;
  }

  :deep(.el-form-item__label) {
    font-size: 14px;
  }
}

/* 登录对话框样式 */
:deep(.login-dialog) {
  border-radius: 8px;
  
  .el-dialog__header {
    padding: 15px 20px;
    margin-right: 0;
    border-bottom: 1px solid #eee;
  }

  .el-dialog__body {
    padding: 20px;
  }

  .el-form-item {
    margin-bottom: 20px;
  }

  .el-input {
    width: 100%;
  }
}
</style>
