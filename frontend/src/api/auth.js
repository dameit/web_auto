import axios from 'axios'

// 创建axios实例
const apiClient = axios.create({
  baseURL: 'http://localhost:4900/api', // 后端API地址
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

// 注册API
export const register = async (userData) => {
  try {
    const response = await apiClient.post('/register', userData)
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.message || '注册失败')
  }
}

// 保存BMC配置API
export const bmc_save = async (username, ip, _username, _password) => {
  try {
    const response = await apiClient.post('/home/bmc_save', {
      username,
      ip,
      _username,
      _password
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.message || '保存BMC配置失败')
  }
}

// 保存OS配置API
export const os_save = async (username, ip, _username, _password) => {
  try {
    const response = await apiClient.post('/home/os_save', {
      username,
      ip,
      _username,
      _password
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.message || '保存OS配置失败')
  }
}

// 测试BMC连接API
export const bmc_test_connect = async (ip, username, password) => {
  try {
    const response = await apiClient.post('/home/bmc_test_connect', {
      ip,
      username,
      password
    })
    return true
  } catch (error) {
    throw new Error(error.response?.data?.message || '测试BMC连接失败')
  }
}

// 测试OS连接API
export const os_test_connect = async (ip, username, password) => {
  try {
    const response = await apiClient.post('/home/os_test_connect', {
      'ip': ip,
      'username': username,
      'password': password
    })
    return true
  } catch (error) {
    throw new Error(error.response?.data?.message || '测试OS连接失败')
  }
}

// 保存文件API
export const file_save = async (formData) => {
  try {
    const response = await apiClient.post('/test_cases/file_upload', formData, 
    {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.message || '文件路径保存失败')
  }
}

// 自动配置bmc web API
export const start_test = async (ip, username, password, test_cases, is_before) => {
  try {
    const response = await apiClient.post('/test_cases/start_test', {
      'ip': ip,
      'username': username,
      'password': password,
      'test_cases': test_cases,
      'is_before': is_before
    },
    {
      timeout : 120000,
    })

    // 关键：打印完整的响应信息
    console.log('✅ [前端] 收到响应，状态码:', response.status);
    console.log('📦 [前端] 响应数据:', response.data);
    console.log('🔧 [前端] 响应头:', response.headers);

    // response.data 是从后端收到的 jsonify()
    return response.data
  } catch (error) {
    // 更详细的错误信息
    console.error('❌ [前端] 请求失败详情:');
    console.error('    - 错误对象:', error);
    console.error('    - 响应数据:', error.response?.data);
    console.error('    - 状态码:', error.response?.status);
    console.error('    - 请求配置:', error.config);
    throw new Error(error.response?.data?.message || 'web自动化操作失败')
  }
}

// 更新bmc fw API
export const fw_update = async (bmc_ip, bmc_username, bmc_password, username) => {
  try {
    const response = await apiClient.post('/test_cases/fw_update', {
      'bmc_ip': bmc_ip,
      'bmc_username': bmc_username,
      'bmc_password': bmc_password,
      'username': username
    },
    {
      timeout : 120000,
    })

    // response.data 是从后端收到的 jsonify()
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.message || '更新BMC固件失败')
  }
}

