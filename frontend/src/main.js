import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './style.css'
import App from './App.vue'
import router from './router'
import axios from 'axios'

const app = createApp(App)

// 全局配置axios
app.config.globalProperties.$axios = axios

app.use(ElementPlus)
app.use(router)

app.mount('#app')
