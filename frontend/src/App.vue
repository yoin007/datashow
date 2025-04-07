<template>
  <div class="app-container">
    <el-container>
      <el-header class="app-header">
        <div class="header-content">
          <h1 class="app-title">班级数据展示系统</h1>
          <el-select
            v-model="classCode"
            placeholder="选择班级"
            @change="handleClassChange"
            class="class-select"
          >
            <el-option
              v-for="code in classCodes"
              :key="code"
              :label="code"
              :value="code"
            />
          </el-select>
        </div>
      </el-header>
      <el-container class="main-container">
        <el-aside :width="isCollapse ? '64px' : '200px'" class="app-aside">
          <el-menu
            :default-active="activeIndex"
            class="nav-menu"
            :collapse="isCollapse"
            @select="handleSelect"
          >
            <el-menu-item index="/schedule">
              <el-icon><Calendar /></el-icon>
              <template #title>课程表</template>
            </el-menu-item>
            <el-menu-item index="/homework">
              <el-icon><Notebook /></el-icon>
              <template #title>班级作业</template>
            </el-menu-item>
            <el-menu-item index="/announcement">
              <el-icon><Bell /></el-icon>
              <template #title>班级公告</template>
            </el-menu-item>
            <!-- <el-menu-item index="/teacher-message">
              <el-icon><Message /></el-icon>
              <template #title>老师留言</template>
            </el-menu-item> -->
            <el-menu-item index="/basic-info">
              <el-icon><InfoFilled /></el-icon>
              <template #title>班级信息</template>
            </el-menu-item>
            <el-menu-item index="/fun">
              <el-icon><MagicStick /></el-icon>
              <template #title>趣味功能</template>
            </el-menu-item>
            <el-menu-item index="/current-classes">
              <el-icon><Clock /></el-icon>
              <span>实时课程</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main class="app-main">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { RouterView, useRouter, useRoute } from 'vue-router'
import { ElContainer, ElAside, ElMain, ElMenu, ElMenuItem, ElSelect, ElOption, ElMessage } from 'element-plus'
import { Calendar, Notebook, Bell, Message, InfoFilled, MagicStick, Clock } from '@element-plus/icons-vue'
import api from './utils/api'

const router = useRouter()
const route = useRoute()
const classCode = ref('')
const classCodes = ref([])
const isCollapse = ref(false)

// 计算当前激活的菜单项
const activeIndex = computed(() => route.path)

const getClassCode = () => {
  const code = document.cookie.split('; ').find(row => row.startsWith('classCode='))
  return code ? code.split('=')[1] : null
}

const fetchClassCodes = async () => {
  try {
    const response = await api.get('/api/class-codes')
    if (response.data && Array.isArray(response.data.class_codes)) {
      classCodes.value = response.data.class_codes
      const savedCode = localStorage.getItem('selectedClassCode')
      if (savedCode && classCodes.value.includes(savedCode)) {
        classCode.value = savedCode
      }
    }
  } catch (error) {
    console.error('Error fetching class codes:', error)
    ElMessage.error('获取班级列表失败')
  }
}

const handleClassChange = (value) => {
  classCode.value = value
  localStorage.setItem('selectedClassCode', value)
  document.cookie = `classCode=${value}`
  window.location.reload()
}

const handleSelect = (path) => {
  router.push(path)
}

// 检查屏幕宽度并设置菜单状态
const checkScreenWidth = () => {
  isCollapse.value = window.innerWidth <= 768
}

onMounted(() => {
  fetchClassCodes()
  const savedClassCode = getClassCode()
  if (savedClassCode) {
    classCode.value = savedClassCode
  }
  
  checkScreenWidth()
  window.addEventListener('resize', checkScreenWidth)
})
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background-color: var(--primary-color);
  color: white;
  padding: 0;
  height: 60px;
  line-height: 60px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 2;
  flex-shrink: 0;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.app-title {
  margin: 0;
  font-size: 1.5rem;
  white-space: nowrap;
}

.class-select {
  width: 150px;
}

.main-container {
  flex: 1;
  min-height: 0;
  display: flex;
}

.app-aside {
  background-color: #fff;
  border-right: 1px solid var(--border-color);
  transition: width 0.3s;
  position: relative;
  z-index: 1;
  flex-shrink: 0;
}

.nav-menu {
  border-right: none;
  height: 100%;
}

.nav-menu:not(.el-menu--collapse) {
  width: 200px;
}

.app-main {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  background-color: var(--background-color);
  position: relative;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .app-header {
    height: auto;
    min-height: 60px;
    padding: 0.5rem;
  }

  .header-content {
    flex-direction: column;
    align-items: stretch;
    line-height: normal;
    height: auto;
  }

  .app-title {
    text-align: center;
    margin-bottom: 0.5rem;
  }

  .class-select {
    width: 100%;
  }

  .app-aside {
    width: 64px !important;
  }

  .nav-menu {
    width: 64px !important;
  }
}

@media (max-width: 576px) {
  .app-main {
    padding: 0.5rem;
  }
}
</style>
