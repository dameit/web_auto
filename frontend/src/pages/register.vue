<template>
  <div class="register-container">
    <div class="register-box">
      <h1 class="register-title">用户注册</h1>

      <form class="register-form" @submit.prevent="handleRegister">
        <!-- 用户名 -->
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            id="username"
            type="text"
            v-model="form.username"
            placeholder="请输入用户名 (3-20位字符)"
            required
            minlength="3"
            maxlength="20"
          />
        </div>

        <!-- 密码 -->
        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            type="password"
            v-model="form.password"
            placeholder="请输入密码 (至少6位)"
            required
            minlength="6"
          />
          <div class="password-strength">密码强度: {{ passwordStrength }}</div>
        </div>

        <!-- 确认密码 -->
        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input
            id="confirmPassword"
            type="password"
            v-model="form.confirmPassword"
            placeholder="请再次输入密码"
            required
          />
          <div
            v-if="form.password && form.confirmPassword && !isPasswordMatch"
            class="error-message"
          >
            ❌ 两次输入的密码不一致
          </div>
          <div
            v-else-if="form.password && form.confirmPassword && isPasswordMatch"
            class="success-message"
          >
            ✅ 密码匹配
          </div>
        </div>

        <!-- 按钮区域 -->
        <div class="button-group">
          <button
            type="submit"
            class="btn btn-register"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? "注册中..." : "立即注册" }}
          </button>
          <button type="button" class="btn btn-back" @click="goToLogin">
            返回登录
          </button>
        </div>

        <!-- 已有账号提示 -->
        <div class="login-link">
          已有账号？
          <a href="javascript:void(0);" @click="goToLogin">立即登录</a>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
// 导入API
import { register } from '@/api'

export default {
  name: "RegisterView",
  data() {
    return {
      form: {
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
      },
      isSubmitting: false,
    };
  },
  computed: {
    // 检查密码是否匹配
    isPasswordMatch() {
      return this.form.password === this.form.confirmPassword;
    },
    // 密码强度计算
    passwordStrength() {
      const length = this.form.password.length;
      if (length === 0) return "未输入";
      if (length < 6) return "弱";
      if (length < 10) return "中";
      return "强";
    },
  },
  methods: {
    // 处理注册提交
    async handleRegister() {
      // 1. 表单验证
      if (!this.validateForm()) {
        return;
      }

      // 2. 防止重复提交
      this.isSubmitting = true;

      try {
        console.log("注册数据:", this.form);
        // 3. 调用真实API
        const result = await register({
          username: this.form.username,
          password: this.form.password,
          // 如果有其他字段也可以加上：
          // email: this.form.email,
          // nickname: this.form.username
        })
        console.log('注册成功，返回数据:', result)

        // 4. 注册成功处理
        alert("🎉 注册成功！请前往登录");

        // 5. 跳转到登录页
        this.$router.push("/login");
      } catch (error) {
        console.error("注册失败:", error);
        alert("注册失败，请稍后重试");
      } finally {
        this.isSubmitting = false;
      }
    },

    // 表单验证
    validateForm() {
      // 检查必填项
      if (
        !this.form.username ||
        !this.form.password ||
        !this.form.confirmPassword
      ) {
        alert("请填写所有必填项");
        return false;
      }

      // 检查用户名长度
      if (this.form.username.length < 3) {
        alert("用户名至少需要3个字符");
        return false;
      }

      // 检查密码长度
      if (this.form.password.length < 6) {
        alert("密码至少需要6位");
        return false;
      }

      // 检查密码是否匹配
      if (!this.isPasswordMatch) {
        alert("两次输入的密码不一致");
        return false;
      }

      return true;
    },

    // 跳转到登录页
    goToLogin() {
      this.$router.push("/login");
    },
  },
};
</script>

<style lang="scss" scoped>
.register-container {
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

.register-box {
  width: 100%;
  max-width: 450px;
  padding: 40px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.6s ease-out;
}

.register-title {
  text-align: center;
  margin: 0 0 30px 0;
  color: #333;
  font-size: 24px;
  font-weight: 600;
  position: relative;
  padding-bottom: 15px;
}

.register-title::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: linear-gradient(to right, #667eea, #764ba2);
  border-radius: 2px;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
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
}

.form-group input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.password-strength {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
}

.error-message {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 4px;
}

.success-message {
  color: #67c23a;
  font-size: 12px;
  margin-top: 4px;
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
}

.btn-register {
  background: linear-gradient(to right, #667eea, #764ba2);
  color: white;
}

.btn-register:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn-register:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-back {
  background-color: white;
  color: #667eea;
  border: 2px solid #667eea !important;
}

.btn-back:hover {
  background-color: #f8f9ff;
  transform: translateY(-2px);
}

.login-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
  font-size: 14px;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  margin-left: 5px;
}

.login-link a:hover {
  text-decoration: underline;
}

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

@media (max-width: 480px) {
  .register-box {
    margin: 20px;
    padding: 30px 24px;
  }

  .button-group {
    flex-direction: column;
  }
}
</style>
