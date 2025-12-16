<template>
  <div class="login-container">
    <!-- 登录框 -->
    <div class="login-box">
      <!-- 标题 -->
      <h1 class="login-title">web自动化操作平台</h1>

      <!-- 登录表单 -->
      <form class="login-form" @submit.prevent="handleLogin">
        <!-- 用户名输入框 -->
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            id="username"
            type="text"
            v-model="form.username"
            placeholder="请输入用户名"
            required
          />
        </div>

        <!-- 密码输入框 -->
        <div class="form-group">
          <label for="password">密码</label>
          <!-- v-model="form.password" 双向数据绑定，最重要！ 将输入框的值与Vue数据 form.password 实时同步 -->
          <input
            id="password"
            type="password"
            v-model="form.password"
            placeholder="请输入密码"
            required
          />
        </div>

        <!-- 按钮区域 -->
        <div class="button-group">
          <button type="submit" class="btn btn-login">登录</button>
          <button
            type="button"
            class="btn btn-register"
            @click="handleRegister"
          >
            注册
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
// 导入API
import { login } from '@/api'

export default {
  data() {
    return {
      // 表单数据
      form: {
        username: "",
        password: "",
      },
      isLoading: false,    // 加载状态
    };
  },
  methods: {
    // 处理登录
    async handleLogin() {
      console.log("登录信息:", this.form);
      // 这里可以添加实际的登录逻辑，比如API调用
      // 设置加载状态
      this.isLoading = true
      try {
        console.log('正在登录，提交数据:', this.form)
        // 3. 调用登录API
        const result = await login(this.form.username, this.form.password)
        console.log('登录成功，返回数据:', result)
        // 4. 处理登录成功
        this.handleLoginSuccess(result)
      } catch (error) {
        console.error('登录失败:', error)
        // 5. 处理登录失败
        this.handleLoginError(error)
      } finally {
        // 无论成功失败，都取消加载状态
        this.isLoading = false
      }
      // 登录成功后通常跳转到主页
      // this.$router.push('/home')
    },
    handleLoginSuccess(result) {
      // 保存token到本地存储
      if (result.token) {
        localStorage.setItem('auth_token', result.token)
        localStorage.setItem('user_info', JSON.stringify(result.user || {}))
        
        // 设置axios默认请求头（后续所有请求自动携带token）
        const axios = require('axios')
        axios.defaults.headers.common['Authorization'] = `Bearer ${result.token}`
      }
      
      // 显示成功提示
      this.showSuccessMessage('登录成功！')
      
      // 跳转到主页（延迟1秒，让用户看到成功提示）
      setTimeout(() => {
        this.$router.push('/home')
      }, 1000)
    },
    
    // 处理登录失败
    handleLoginError(error) {
      // 显示错误信息
      this.errorMessage = error.message || '登录失败，请检查用户名和密码'
      
      // 可以针对不同错误类型做不同处理
      if (error.message.includes('网络')) {
        this.errorMessage = '网络连接失败，请检查网络设置'
      }
    },
    
    // 显示成功消息
    showSuccessMessage(message) {
      // 可以使用更优雅的提示方式，这里先用alert
      alert(message)
      
      // 如果安装了UI库（如Element Plus），可以这样：
      // this.$message.success(message)
    },
    // 处理注册
    handleRegister() {
      console.log("跳转到注册页面");
      // 跳转到注册页面
      this.$router.push("/register");
    },
  },
};
</script>

<style lang="scss" scoped>
.login-container {
  /* 让登录容器占满整个视口高度并居中 */
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  /* 登录框样式 */
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.6s ease-out;
}

.login-title {
  /* 标题样式 */
  text-align: center;
  margin: 0 0 30px 0;
  color: #333;
  font-size: 24px;
  font-weight: 600;
  position: relative;
  padding-bottom: 15px;
}

.login-title::after {
  /* 标题下方的装饰线 */
  content: "";
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: linear-gradient(to right, #5e8fbc, #6e97de);
  border-radius: 2px;
}

.login-form {
  /* 表单样式 */
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  /* 每个表单组的样式 */
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  /* 标签样式 */
  color: #555;
  font-weight: 500;
  font-size: 14px;
}

.form-group input {
  /* 输入框样式 */
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
  outline: none;
}

.form-group input:focus {
  /* 输入框获取焦点时的样式 */
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.button-group {
  /* 按钮组样式 */
  display: flex;
  gap: 16px;
  margin-top: 10px;
}

.btn {
  /* 按钮基础样式 */
  flex: 1;
  padding: 14px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.btn-login {
  /* 登录按钮样式 */
  background: linear-gradient(to right, #667eea, #764ba2);
  color: white;
}

.btn-login:hover {
  /* 登录按钮悬停效果 */
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn-register {
  /* 注册按钮样式 */
  background-color: white;
  color: #667eea;
  border: 2px solid #667eea !important;
}

.btn-register:hover {
  /* 注册按钮悬停效果 */
  background-color: #f8f9ff;
  transform: translateY(-2px);
}

/* 淡入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计：在小屏幕上调整 */
@media (max-width: 480px) {
  .login-box {
    margin: 20px;
    padding: 30px 24px;
  }

  .button-group {
    flex-direction: column;
  }
}
</style>
