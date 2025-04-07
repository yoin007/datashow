import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: false
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    console.log('Request URL:', config.url)
    return config
  },
  error => {
    console.error('Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    console.log('Response:', response.data)
    return response
  },
  error => {
    console.error('Response Error:', error.response || error)
    return Promise.reject(error)
  }
)

export default api
