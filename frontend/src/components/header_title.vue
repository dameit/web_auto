<template>
  <header class="header">
    <!-- 左侧标题 -->
    <h1 class="main-page-title">web自动化操作平台</h1>

    <!-- 右侧用户信息或登录按钮 -->
    <div class="header-right">
      <div v-if="isLoggedIn" class="user-info">
        <span class="username">{{ username }}</span>
        <button class="logout-btn" @click="handleLogout">
          <span class="btn-text">退出</span>
        </button>
      </div>
      <button v-else class="login-btn" @click="goToLogin">
        <span class="btn-text">登录</span>
      </button>
    </div>

  </header>
</template>

<script>
export default {
  data() {
    return {
      isLoggedIn: false,
      username: ''
    };
  },

  mounted() {
    this.checkLoginStatus();
    
    // 监听路由变化，每次页面切换都检查登录状态
    this.$router.afterEach(() => {
      setTimeout(() => {
        this.checkLoginStatus();
      }, 100);
    });
  },
  
  methods: {
    checkLoginStatus() {
      const userInfo = localStorage.getItem('user_info');
      if (userInfo) {
        try {
          const user = JSON.parse(userInfo);
          this.isLoggedIn = true;
          this.username = user.username || user.name || '用户';
        } catch (e) {
          console.error('解析用户信息失败:', e);
        }
      }
      localStorage.setItem("is_login_in", this.isLoggedIn)
    },

    // 跳转到登录页
    goToLogin() {
      this.$router.push("/login");
      this.isLoggedIn = localStorage.getItem("login_success")
    },

    // 处理退出登录
    async handleLogout() {
      try {
        // 1. 重置组件状态
        this.isLoggedIn = false;
        this.username = ''

        alert('已成功退出登录')

        // 2. 跳转到登录页
        this.$router.push("/login");

      } catch (error) {
        console.error('退出登录时出错:', error);
        // 即使出错也清除本地数据并跳转
        this.clearLoginData();
        this.isLoggedIn = false;
        this.username = '';
        this.$router.push("/login");
      }
    } 
  }
};
</script>

<style lang="scss" scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 60px;
  background-color: #409eff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between; /* 左右两端对齐 */
  padding: 0 0px; /* 左右内边距 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.main-page-title {
  margin: 0px 20px;
  font-size: 20px;
  font-weight: bold;
  letter-spacing: 1px;
}

.header-right {
  display: flex;
  align-items: center;
  margin-right: 20px; /* 添加右边距 */
}

.login-btn, .logout-btn {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 6px;
  padding: 8px 20px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;

  &:hover {
    background-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }

  &:active {
    transform: translateY(0);
  }
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.username {
  font-size: 14px;
  font-weight: 500;
  color: white;
  padding: 6px 12px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}
</style>