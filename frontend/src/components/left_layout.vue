<template>
  <div class="main-layout">
    <!-- 顶部标题栏 -->
    <AppHeader />

    <!-- 左侧导航栏 + 主要内容 -->
    <div class="layout-content">
      <!-- 左侧导航栏 -->
      <aside class="sidebar">
        <nav class="sidebar-nav">
          <!-- 导航标题 -->
          <div class="nav-title">功能导航</div>

          <!-- 导航菜单项 -->
          <router-link
            to="/"
            class="nav-item"
            :class="{ active: $route.path === '/' }"
          >
            <span class="nav-icon">🏠</span>
            <span class="nav-text">首页</span>
          </router-link>

          <router-link
            to="/test-cases"
            class="nav-item"
            :class="{ active: $route.path === '/test-cases' }"
          >
            <span class="nav-icon">🧪</span>
            <span class="nav-text">测试用例</span>
          </router-link>
        </nav>
      </aside>
    </div>
  </div>
</template>

<script>
export default {
  name: "left_layout",
};
</script>

<style lang="scss" scoped>
.main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.layout-content {
  display: flex;
  flex: 1;
  margin-top: 60px; /* 顶部标题栏高度 */
}

/* 左侧导航栏样式 */
.sidebar {
  width: 220px;
  background-color: #304156;
  color: #bfcbd9;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  position: fixed;
  left: 0;
  top: 60px;
  bottom: 0;
  z-index: 999;

  &.collapsed {
    width: 64px;

    .nav-text {
      display: none;
    }

    .nav-title {
      display: none;
    }

    .nav-icon {
      margin-right: 0;
      font-size: 20px;
    }
  }
}

.sidebar-nav {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
}

.nav-title {
  padding: 15px 20px 10px;
  font-size: 12px;
  color: #8a9bb2;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: #bfcbd9;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  border-left: 3px solid transparent;

  &:hover {
    background-color: rgba(255, 255, 255, 0.05);
    color: #fff;
  }

  &.active {
    background-color: rgba(64, 158, 255, 0.1);
    color: #409eff;
    border-left-color: #409eff;

    .nav-icon {
      color: #409eff;
    }
  }
}

.nav-icon {
  font-size: 18px;
  margin-right: 10px;
  width: 24px;
  text-align: center;
  transition: all 0.3s ease;
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}

.collapse-btn {
  padding: 12px;
  background-color: rgba(0, 0, 0, 0.2);
  border: none;
  color: #bfcbd9;
  cursor: pointer;
  font-size: 12px;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: rgba(0, 0, 0, 0.3);
    color: #fff;
  }
}

/* 主要内容区域样式 */
.main-content {
  flex: 1;
  margin-left: 220px; /* 左侧导航栏宽度 */
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
  transition: margin-left 0.3s ease;

  .sidebar.collapsed ~ & {
    margin-left: 64px;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    width: 220px;

    &.mobile-open {
      transform: translateX(0);
    }
  }

  .main-content {
    margin-left: 0;
  }

  /* 移动端显示汉堡菜单按钮 */
  .mobile-menu-btn {
    display: block;
  }
}
</style>
