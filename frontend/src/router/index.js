import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/schedule',
    name: 'Schedule',
    component: () => import('../views/Schedule.vue')
  },
  {
    path: '/announcement',
    name: 'Announcement',
    component: () => import('../views/Announcement.vue')
  },
  {
    path: '/basic-info',
    name: 'BasicInfo',
    component: () => import('../views/BasicInfo.vue')
  },
  {
    path: '/teacher-message',
    name: 'TeacherMessage',
    component: () => import('../views/TeacherMessage.vue')
  },
  {
    path: '/homework',
    name: 'Homework',
    component: () => import('../views/Homework.vue')
  },
  {
    path: '/fun',
    name: 'Fun',
    component: () => import('../views/Fun.vue')
  },
  {
    path: '/current-classes',
    name: 'CurrentClasses',
    component: () => import('../views/CurrentClasses.vue'),
    meta: {
      title: '实时课程'
    }
  },
  {
    path: '/',
    redirect: '/schedule'
  },
  {
    path: '/zhf',
    redirect: () => {
      window.location.href = '/src/assets/zhf.html';
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
