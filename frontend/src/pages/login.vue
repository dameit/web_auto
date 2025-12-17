<template>
  <div class="login-container">
    <!-- 登录框 -->
    <div class="login-box">
      <!-- 标题 -->
      <h1 class="login-title">web自动化操作平台</h1>

      <!-- 错误提示 -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- 登录表单 -->
      <form class="login-form" @submit.prevent="handleLogin">
        <!-- 用户名输入框 -->
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            id="username"
            type="text"
            v-model="form.username"
            @input="clearErrorMessage"
            placeholder="请输入用户名"
            required
          />
        </div>

        <!-- 密码输入框 -->
        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            type="password"
            v-model="form.password"
            @input="clearErrorMessage"
            placeholder="请输入密码"
            required
          />
        </div>

        <!-- 按钮区域 -->
        <div class="button-group">
          <button 
            type="submit" 
            class="btn btn-login" 
            :disabled="isLoading"
          >
            {{ isLoading ? '登录中...' : '登录' }}
          </button>
          <button
            type="button"
            class="btn btn-register"
            @click="handleRegister"
            :disabled="isLoading"
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
      errorMessage: '',    // 错误信息
    };
  },

  methods: {
    // 处理登录
    async handleLogin() {
      console.log("登录信息:", this.form);
      
      // 清空之前的错误信息
      this.errorMessage = '';
      
      // 表单验证
      if (!this.validateForm()) {
        return;
      }
      
      // 设置加载状态
      this.isLoading = true;
      
      try {
        console.log('正在登录，提交数据:', this.form);
        // 调用登录API
        const result = await login(this.form.username, this.form.password);
        console.log('登录成功，返回数据:', result);
        
        // 处理登录成功
        await this.handleLoginSuccess(result);
        
      } catch (error) {
        console.error('登录失败:', error);
        // 处理登录失败
        this.handleLoginError(error);
      } finally {
        // 无论成功失败，都取消加载状态
        this.isLoading = false;
      }
    },
    
    // 表单验证
    validateForm() {
      if (!this.form.username.trim()) {
        this.errorMessage = '请输入用户名';
        return false;
      }
      
      if (!this.form.password.trim()) {
        this.errorMessage = '请输入密码';
        return false;
      }
      
      // 可以添加更多验证规则
      if (this.form.username.length < 3) {
        this.errorMessage = '用户名至少需要3个字符';
        return false;
      }
      
      if (this.form.password.length < 6) {
        this.errorMessage = '密码至少需要6个字符';
        return false;
      }
      
      return true;
    },
    
    // 处理登录成功
    async handleLoginSuccess(result) {
      // 检查API返回的数据
      if (!result || !result.user) {
        this.errorMessage = '登录失败：服务器返回数据异常';
        return;
      }
      
      try {
        // 确保用户信息包含用户名
        const userInfo = {
          username: this.form.username,
          ...result.user
        };
        
        console.log('保存用户信息到 localStorage:', userInfo);
        localStorage.setItem('user_info', JSON.stringify(userInfo));
        
        // 如果有token，保存token
        if (result.token) {
          localStorage.setItem('auth_token', result.token);
        }
        
        // 显示成功提示
        // this.showSuccessMessage('登录成功！');
        
        // 延迟跳转，让用户看到成功提示
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // 跳转到主页
        this.$router.push('/home');
        
      } catch (error) {
        console.error('保存用户信息失败:', error);
        this.errorMessage = '登录失败：保存用户信息时出错';
      }
    },
    
    // 处理登录失败
    handleLoginError(error) {
      console.error('登录失败详情:', error);
      
      // 根据错误类型显示不同的错误信息
      if (error.response) {
        // 服务器返回了错误响应
        const status = error.response.status;
        const data = error.response.data;
        
        if (status === 401) {
          this.errorMessage = data.message || '用户名或密码错误';
        } else if (status === 400) {
          this.errorMessage = data.message || '请求参数错误';
        } else if (status === 404) {
          this.errorMessage = '登录接口不存在';
        } else if (status >= 500) {
          this.errorMessage = '服务器错误，请稍后重试';
        } else {
          this.errorMessage = `登录失败: ${status}`;
        }
        
      } else if (error.request) {
        // 请求已发送但没有收到响应
        this.errorMessage = '网络连接失败，请检查网络设置';
      } else {
        // 其他错误
        this.errorMessage = error.message || '登录失败，请稍后重试';
      }
      
      // 显示错误提示
      // this.showErrorMessage(this.errorMessage);
    },
    
    // 显示成功消息
    showSuccessMessage(message) {
      // 这里先用alert，你可以替换成更优雅的方式
      alert(message);
    },
    
    // 显示错误消息
    showErrorMessage(message) {
      // 这里可以换成你的UI组件库的提示方式
      console.error('登录错误:', message);
      // 使用alert作为简单提示
      alert(message);
    },
    
    // 清空错误信息
    clearErrorMessage() {
      this.errorMessage = '';
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
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1001;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.6s ease-out;
}

.login-title {
  text-align: center;
  margin: 0 0 30px 0;
  color: #333;
  font-size: 24px;
  font-weight: 600;
  position: relative;
  padding-bottom: 15px;
}

.login-title::after {
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

/* 错误信息样式 */
.error-message {
  background-color: #fee;
  color: #f56c6c;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 20px;
  border: 1px solid #fbc4c4;
  font-size: 14px;
  text-align: center;
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: #555;
  font-weight: 500;
  font-size: 14px;
}

.form-group input {
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
  outline: none;
  
  &:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  &:disabled {
    background-color: #f5f5f5;
    cursor: not-allowed;
  }
}

.button-group {
  display: flex;
  gap: 16px;
  margin-top: 10px;
}

.btn {
  flex: 1;
  padding: 14px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none !important;
  }
}

.btn-login {
  background: linear-gradient(to right, #667eea, #764ba2);
  color: white;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
  }
}

.btn-register {
  background-color: white;
  color: #667eea;
  border: 2px solid #667eea !important;
  
  &:hover:not(:disabled) {
    background-color: #f8f9ff;
    transform: translateY(-2px);
  }
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