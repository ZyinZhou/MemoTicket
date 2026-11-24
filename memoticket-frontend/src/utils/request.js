import axios from 'axios'
import { ElMessage } from 'element-plus'

// ==========================================
// ⚠️ 开启此开关，即可在没有后端的情况下测试整个前端！
const USE_MOCK = false; 
// ==========================================

const request = axios.create({
  baseURL: 'http://127.0.0.1:5000', 
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
    if (res.code !== 200) {
      ElMessage.error(res.msg || '请求失败')
      return Promise.reject(new Error(res.msg || 'Error'))
    }
    return res
  },
  error => {
    const msg = error.response?.data?.msg || error.message || '网络错误'
    ElMessage.error(msg)
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user_id')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// ==========================================
// 核心：Mock 拦截器 (拦截真实请求，返回假数据)
// ==========================================
if (USE_MOCK) {
  request.interceptors.request.use(config => {
    // 使用自定义 adapter 拦截请求
    config.adapter = (cfg) => {
      return new Promise((resolve) => {
        let data = {};
        const url = cfg.url || '';
        const method = cfg.method || 'get';

        console.log(`[Mock拦截] ${method.toUpperCase()} ${url}`);

        // 1. 登录接口
        if (url.includes('/api/login') && method === 'post') {
          data = { code: 200, msg: "登录成功", user_id: 1, token: "mock-token-123" };
        } 
        // 2. 注册接口
        else if (url.includes('/api/register') && method === 'post') {
          data = { code: 200, msg: "注册成功" };
        }
        // 3. 获取兴趣列表
        else if (url.includes('/api/interests') && method === 'get') {
          data = { code: 200, data: [
            { id: 1, name: '二次元动漫' }, { id: 2, name: '独立游戏' }, 
            { id: 3, name: '户外徒步' }, { id: 4, name: '科幻电影' }
          ]};
        }
        // 4. 获取票根列表 (带假数据)
        else if (url === '/api/tickets' && method === 'get') {
          data = { code: 200, data: [
            { id: 1, title: "《奥本海默》", type: "电影", rating: 5, eventDate: "2026-11-01", venue: "万达影城" },
            { id: 2, title: "《青川怪谈》", type: "剧本杀", rating: 4, eventDate: "2026-11-10", venue: "迷之屋" }
          ]};
        }
        // 5. 获取票根详情
        else if (url.match(/\/api\/tickets\/\d+/) && method === 'get') {
          data = { code: 200, data: {
            id: 1, title: "《奥本海默》", type: "电影", rating: 5, 
            content: "非常震撼的电影，视听盛宴！", eventDate: "2026-11-01", venue: "万达影城"
          }};
        }
        // 6. 删除票根
        else if (url.match(/\/api\/tickets\/\d+/) && method === 'delete') {
          data = { code: 200, msg: "删除成功" };
        }
        // 7. 创建/修改票根
        else if (url.includes('/api/tickets') && (method === 'post' || method === 'put')) {
          data = { code: 200, msg: "操作成功", data: { id: 99, createTime: "2026-11-15 12:00:00" } };
        }
        // 其他未定义接口，默认返回成功
        else {
          data = { code: 200, msg: "Mock默认成功", data: {} };
        }

        // 模拟网络延迟 300ms
        setTimeout(() => {
          resolve({ data, status: 200, statusText: 'OK', headers: {}, config: cfg });
        }, 300);
      });
    };
    return config;
  });
}

export default request;