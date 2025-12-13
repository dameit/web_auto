<template>
  <header class="header">
    <!-- 左侧标题 -->
    <h1 class="main-page-title">web自动化操作平台</h1>

    <!-- 右侧登录按钮 -->
    <div class="header-right">
      <button class="login-btn" @click="goToLogin">
        <span class="btn-text">登录</span>
      </button>
    </div>
  </header>
</template>

<script>
export default {
  methods: {
    goToLogin() {
      // 使用路由跳转到登录页面
      this.$router.push("/login");
    },
  },
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
  margin: 0;
  font-size: 20px;
  font-weight: bold;
  letter-spacing: 1px;
}

.header-right {
  display: flex;
  align-items: center;
}

.login-btn {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 6px;
  padding: 8px 20px;
  margin: 0px 20px;
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

.btn-text {
  font-weight: 500;
}
</style>
