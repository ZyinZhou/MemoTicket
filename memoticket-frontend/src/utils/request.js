import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: 'http://127.0.0.1:5000', // 确认后端跑在 5000 端口
  timeout: 5000
})

// 请求拦截器：自动携带 Token
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    const res = response.data
    // 如果后端返回的 code 不是 200，说明业务报错
    if (res.code !== 200) {
      ElMessage.error(res.msg || '请求失败')
      return Promise.reject(new Error(res.msg || 'Error'))
    }
    return res // 成功则返回整个 res 对象
  },
  error => {
    // 处理网络层面或 HTTP 状态码层面的错误
    const msg = error.response?.data?.msg || error.message || '网络错误'
    ElMessage.error(msg)
    
    // 如果是 401，说明 token 过期，踢回登录页
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user_id')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default request