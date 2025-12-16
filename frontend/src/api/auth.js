import axios from 'axios'

// 创建axios实例
const apiClient = axios.create({
  baseURL: 'http://localhost:5000/api', // 后端API地址
  timeout: 10000, // 请求超时时间（10秒）
  headers: {
    'Content-Type': 'application/json'
  }
})

// 登录API
export const login = async (username, password) => {
  try {
    const response = await apiClient.post('/login', {
      username,
      password
    })
    return response.data
  } catch (error) {
    // 统一处理错误
    throw new Error(error.response?.data?.message || '登录失败，请检查网络连接')
  }
}

// 注册API（如果需要）
export const register = async (userData) => {
  try {
    const response = await apiClient.post('/register', userData)
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.message || '注册失败')
  }
}