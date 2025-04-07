<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElTimeline, ElTimelineItem, ElCard, ElEmpty } from 'element-plus'
import api from '../utils/api'

const announcements = ref([])
const loading = ref(false)
const classCode = ref('')

const getClassCode = () => {
  const code = document.cookie.split('; ').find(row => row.startsWith('classCode='))
  return code ? code.split('=')[1] : null
}

const fetchAnnouncements = async () => {
  const classCode = getClassCode()
  if (!classCode) {
    ElMessage.error('请先选择班级')
    return
  }

  loading.value = true
  try {
    const response = await api.get(`/api/announcements/${classCode}`)
    if (response.data && Array.isArray(response.data.announcements)) {
      announcements.value = response.data.announcements.sort((a, b) => 
        new Date(b.date) - new Date(a.date)
      )
    } else {
      announcements.value = []
      ElMessage.warning('暂无公告')
    }
  } catch (error) {
    console.error('Error fetching announcements:', error)
    ElMessage.error('获取公告失败')
    announcements.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchAnnouncements()
  classCode.value = getClassCode()
})
</script>

<template>
  <div class="announcement-container">
    <h2>{{ classCode ? `${classCode}公告` : '公告' }}</h2>
      <!-- <div style="text-align: center;">
        <a href="https://18.r302.cc/QXgeZWb" target="_blank" rel="noopener noreferrer">
          <img src="/src/assets/xiaoshi.png" alt="校史百题大赛">
        </a>
      </div> -->
    <el-empty v-if="!loading && announcements.length === 0" description="暂无公告" />
    <el-timeline v-else>
      <el-timeline-item
        v-for="announcement in announcements"
        :key="announcement.id"
        :timestamp="announcement.date"
        type="primary"
        size="large"
        placement="top"
      >
        <el-card class="announcement-card">
          <template #header>
            <div class="card-header">
              <h4>{{ announcement.title }}  ({{ announcement.author }})</h4>
            </div>
          </template>
          <p class="announcement-content">{{ announcement.content }}</p>
        </el-card>
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<style scoped>
.announcement-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

h2 {
  margin-bottom: 20px;
  color: #409EFF;
  text-align: center;
}

.announcement-card {
  margin-bottom: 10px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h4 {
  margin: 0;
  color: #303133;
  font-size: 16px;
}

.announcement-content {
  margin: 10px 0 0;
  color: #606266;
  line-height: 1.6;
  text-indent: 2em;
}

:deep(.el-timeline-item__node--large) {
  width: 14px;
  height: 14px;
}

:deep(.el-timeline-item__timestamp) {
  color: #909399;
  font-size: 14px;
  margin-bottom: 8px;
}
</style>
