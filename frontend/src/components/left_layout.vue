<template>
  <div class="main-layout">
    <!-- 左侧导航栏 + 主要内容 -->
    <div class="layout-content">
      <!-- 左侧导航栏 -->
      <aside class="sidebar">
        <nav class="sidebar-nav">

          <!-- 导航菜单项 -->
          <router-link to="/home" class="nav-item" exact-active-class="active">
            <div class="nav-item-content">
              <span class="nav-icon">🏠</span>
              <span class="nav-text">首页</span>
            </div>
          </router-link>

          <!-- 测试用例菜单（可展开） -->
          <div class="nav-item dropdown-item">
            <div class="nav-item-content"  @click="toggleTestCases">
              <span class="nav-icon">🧪</span>
              <span class="nav-text">测试用例</span>
              <span
                class="dropdown-arrow"
                :class="{ expanded: isTestCasesExpanded }"
              >
                ▼
              </span>
            </div>

            <!-- 子菜单（展开时显示） -->
            <div v-if="isTestCasesExpanded" class="submenu">
              <router-link
                to="/test-cases/save"
                class="submenu-item"
                active-class="submenu-active"
              >
                <span class="submenu-icon">💾</span>
                <span class="submenu-text">保存配置更新</span>
              </router-link>

              <router-link
                to="/test-cases/import-export"
                class="submenu-item"
                active-class="submenu-active"
              >
                <span class="submenu-icon">🔄</span>
                <span class="submenu-text">配置导入导出</span>
              </router-link>
            </div>
          </div>

          <!-- 其他菜单项 -->
          <router-link to="/scripts" class="nav-item" active-class="active">
            <div class="nav-item-content">
              <span class="nav-icon">📜</span>
              <span class="nav-text">自动化脚本</span>
            </div>
          </router-link>

          <router-link to="/monitor" class="nav-item" active-class="active">
            <div class="nav-item-content">
              <span class="nav-icon">📊</span>
              <span class="nav-text">健康监测</span>
            </div>
          </router-link>
        </nav>
      </aside>

      <!-- 主要内容区域 -->
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: "left_layout",
  data() {
    return {
      isTestCasesExpanded: false
    }
  },
  methods: {
    toggleTestCases() {
      this.isTestCasesExpanded = !this.isTestCasesExpanded
    }
  }
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
  width: 240px;
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
  border-right: 1px solid #e2e8f0;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  position: fixed;
  left: 0;
  top: 60px;
  bottom: 0;
  z-index: 998;
  overflow-y: auto;
}

.sidebar-nav {
  padding: 0;
  flex: 1;
}

/* 导航标题 */
.nav-header {
  padding: 20px 20px 15px;
  border-bottom: 1px solid #f0f2f5;
  margin-bottom: 10px;
}

.nav-title {
  margin: 0;
  font-size: 14px;
  color: #909399;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* 导航项基础样式 */
.nav-item {
  display: block;
  text-decoration: none;
  color: #475569;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;

  &.dropdown-item {
    cursor: pointer;
  }

  &:hover {
    background: linear-gradient(90deg, #e0f2fe 0%, #f0f9ff 100%);
    color: #0369a1;
    border-left-color: #7dd3fc;

    .nav-icon {
      color: #0ea5e9;
    }

    .nav-text {
      color: #0369a1;
    }
  }

  &.active {
    background: linear-gradient(90deg, #dbeafe 0%, #eff6ff 100%);
    color: #1d4ed8;
    border-left-color: #3b82f6;

    .nav-icon,
    .nav-text {
      color: #1d4ed8;
    }
  }
}

.nav-item-content {
  display: flex;
  align-items: center;
  padding: 14px 20px;
  position: relative;
}

.nav-icon {
  font-size: 16px;
  margin-right: 12px;
  width: 20px;
  text-align: center;
  color: #64748b;
  transition: color 0.2s ease;
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
  flex: 1;
  color: #334155;
  transition: color 0.2s ease;
}

/* 下拉箭头 */
.dropdown-arrow {
  font-size: 10px;
  color: #94a3b8;
  transition: transform 0.3s ease;
  margin-left: 8px;

  &.expanded {
    transform: rotate(180deg);
    color: #3b82f6;
  }
}

/* 子菜单样式 */
.submenu {
  background: linear-gradient(180deg, #f1f5f9 0%, #e2e8f0 100%);
  border-left: 3px solid #cbd5e1;
  margin-left: 32px;
  overflow: hidden;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
  }
  to {
    opacity: 1;
    max-height: 200px;
  }
}

.submenu-item {
  display: flex;
  align-items: center;
  padding: 12px 20px 12px 16px;
  text-decoration: none;
  color: #475569;
  transition: all 0.2s ease;
  border-left: 2px solid transparent;

  &:hover {
    background: linear-gradient(90deg, #e0f2fe 0%, #f0f9ff 100%);
    color: #0369a1;

    .submenu-icon {
      color: #0ea5e9;
    }
  }

  &.submenu-active {
    background: linear-gradient(90deg, #dbeafe 0%, #eff6ff 100%);
    color: #1d4ed8;
    border-left-color: #3b82f6;

    .submenu-icon {
      color: #1d4ed8;
    }
  }
}

.submenu-icon {
  font-size: 14px;
  margin-right: 10px;
  width: 16px;
  text-align: center;
  color: #64748b;
  transition: color 0.2s ease;
}

.submenu-text {
  font-size: 13px;
  font-weight: 400;
}

/* 主要内容区域样式 */
.main-content {
  flex: 1;
  margin-left: 240px; /* 左侧导航栏宽度 */
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
}

/* 响应式设计 */
@media (max-width: 992px) {
  .sidebar {
    width: 200px;
  }

  .main-content {
    margin-left: 200px;
  }
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    width: 220px;
    box-shadow: 2px 0 12px rgba(0, 0, 0, 0.1);

    &.mobile-open {
      transform: translateX(0);
    }
  }

  .main-content {
    margin-left: 0;
  }
}

/* 滚动条样式 */
.sidebar::-webkit-scrollbar {
  width: 4px;
}

.sidebar::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.sidebar::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
