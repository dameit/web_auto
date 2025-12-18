<template>
  <div class="home-container">
    <!-- 简洁的页面头部 -->
    <div class="page-header">
      <h1>连接配置</h1>
      <p>配置和管理BMC与OS的连接参数</p>
    </div>

    <div class="connection-grid">
      <!-- BMC连接卡片 -->
      <div class="connection-card">
        <div class="card-header">
          <div class="card-title">
            <div class="card-icon-wrapper">
              <span class="card-icon">🔧</span>
            </div>
            <div class="card-title-content">
              <h2>BMC 连接</h2>
              <p class="card-subtitle">基板管理控制器</p>
            </div>
          </div>
          <div class="connection-status">
            <div class="status-indicator-wrapper">
              <span
                :class="['status-indicator', bmc.status]"
                :title="getStatusText(bmc.status)"
              >
                {{ getStatusIcon(bmc.status) }}
              </span>
            </div>
            <div class="status-content">
              <span class="status-text">{{ getStatusText(bmc.status) }}</span>
            </div>
          </div>
        </div>

        <div class="card-divider"></div>

        <div class="connection-form">
          <!-- IP地址 -->
          <div class="form-group">
            <label for="bmc-ip">
              <span class="label-icon">🌐</span>
              BMC IP 地址
            </label>
            <input
              id="bmc-ip"
              type="text"
              v-model="bmc.ip"
              placeholder="例如: 192.168.1.100"
              class="form-input"
              maxlength="15"
              @input="validateIP('bmc')"
            />
          </div>

          <!-- 用户名 -->
          <div class="form-group">
            <label for="bmc-username">
              <span class="label-icon">👤</span>
              用户名
            </label>
            <input
              id="bmc-username"
              type="text"
              v-model="bmc.username"
              placeholder="请输入BMC用户名"
              class="form-input"
              maxlength="32"
              @input="validateLength('bmc', 'username', 32)"
            />
          </div>

          <!-- 密码 -->
          <div class="form-group">
            <label for="bmc-password">
              <span class="label-icon">🔒</span>
              密码
            </label>
            <div class="password-input">
              <input
                id="bmc-password"
                :type="bmc.showPassword ? 'text' : 'password'"
                v-model="bmc.password"
                placeholder="请输入BMC密码"
                class="form-input"
                maxlength="64"
                @input="validateLength('bmc', 'password', 64)"
              />
              <button
                type="button"
                class="btn-action toggle-password"
                @click="togglePasswordVisibility('bmc')"
                :title="bmc.showPassword ? '隐藏密码' : '显示密码'"
              >
                <span class="action-icon">{{
                  bmc.showPassword ? "🙈" : "👁️"
                }}</span>
              </button>
            </div>
          </div>

          <div class="card-divider"></div>

          <!-- 操作按钮 -->
          <div class="card-actions">
            <button
              class="btn btn-save"
              @click="saveConnection('bmc')"
            >
              <span class="btn-icon">💾</span>
              <span>保存配置</span>
            </button>
            <button
              class="btn btn-test"
              @click="testConnection('bmc')"
              :disabled="!canTestBmc"
              :class="{ testing: bmc.testing }"
            >
              <span v-if="bmc.testing" class="spinner"></span>
              <span v-else class="btn-content">
                <span class="btn-icon">🔍</span>
                <span>测试连接</span>
              </span>
            </button>
          </div>
        </div>
      </div>

      <!-- OS连接卡片 -->
      <div class="connection-card">
        <div class="card-header">
          <div class="card-title">
            <div class="card-icon-wrapper">
              <span class="card-icon">💻</span>
            </div>
            <div class="card-title-content">
              <h2>OS 连接</h2>
              <p class="card-subtitle">操作系统连接</p>
            </div>
          </div>
          <div class="connection-status">
            <div class="status-indicator-wrapper">
              <span
                :class="['status-indicator', os.status]"
                :title="getStatusText(os.status)"
              >
                {{ getStatusIcon(os.status) }}
              </span>
            </div>
            <div class="status-content">
              <span class="status-text">{{ getStatusText(os.status) }}</span>
            </div>
          </div>
        </div>

        <div class="card-divider"></div>

        <div class="connection-form">
          <!-- IP地址 -->
          <div class="form-group">
            <label for="os-ip">
              <span class="label-icon">🌐</span>
              OS IP 地址
            </label>
            <input
              id="os-ip"
              type="text"
              v-model="os.ip"
              placeholder="例如: 192.168.1.101"
              class="form-input"
              maxlength="15"
              @input="validateIP('os')"
            />
          </div>

          <!-- 用户名 -->
          <div class="form-group">
            <label for="os-username">
              <span class="label-icon">👤</span>
              用户名
            </label>
            <input
              id="os-username"
              type="text"
              v-model="os.username"
              placeholder="请输入OS用户名"
              class="form-input"
              maxlength="32"
              @input="validateLength('os', 'username', 32)"
            />
          </div>

          <!-- 密码 -->
          <div class="form-group">
            <label for="os-password">
              <span class="label-icon">🔒</span>
              密码
            </label>
            <div class="password-input">
              <input
                id="os-password"
                :type="os.showPassword ? 'text' : 'password'"
                v-model="os.password"
                placeholder="请输入OS密码"
                class="form-input"
                maxlength="64"
                @input="validateLength('os', 'password', 64)"
              />
              <button
                type="button"
                class="btn-action toggle-password"
                @click="togglePasswordVisibility('os')"
                :title="os.showPassword ? '隐藏密码' : '显示密码'"
              >
                <span class="action-icon">{{
                  os.showPassword ? "🙈" : "👁️"
                }}</span>
              </button>
            </div>
          </div>

          <div class="card-divider"></div>

          <!-- 操作按钮 -->
          <div class="card-actions">
            <button
              class="btn btn-save"
              @click="saveConnection('os')"
            >
              <span class="btn-icon">💾</span>
              <span>保存配置</span>
            </button>
            <button
              class="btn btn-test"
              @click="testConnection('os')"
              :disabled="!canTestOs"
              :class="{ testing: os.testing }"
            >
              <span v-if="os.testing" class="spinner"></span>
              <span v-else class="btn-content">
                <span class="btn-icon">🔍</span>
                <span>测试连接</span>
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { bmc_save, os_save, bmc_test_connect, os_test_connect } from '@/api'

export default {
  name: "HomeView",
  data() {
    return {
      bmc: {
        ip: "192.168.1.100",
        username: "",
        password: "",
        status: "disconnected",
        connected: false,
        testing: false,
        showPassword: false,
      },
      os: {
        ip: "192.168.1.101",
        username: "",
        password: "",
        status: "disconnected",
        connected: false,
        testing: false,
        showPassword: false,
      },
    };
  },
  computed: {
    canTestBmc() {
      return (
        this.bmc.ip &&
        this.bmc.username &&
        this.bmc.password &&
        !this.bmc.testing &&
        this.isValidIP(this.bmc.ip)
      );
    },
    canTestOs() {
      return (
        this.os.ip &&
        this.os.username &&
        this.os.password &&
        !this.os.testing &&
        this.isValidIP(this.os.ip)
      );
    },
  },

  methods: {
    async testConnection(type) {
      const target = this[type];

      if (!target.ip || !target.username || !target.password) {
        alert("请填写完整的连接信息");
        return;
      }

      if (!this.isValidIP(target.ip)) {
        alert("IP地址格式不正确");
        return;
      }

      target.testing = true;
      target.status = "disconnected";

      try {
        // new Promise(...)：创建一个 “异步等待容器”
        // 让当前的异步函数暂停执行 1500 毫秒（1.5 秒），等时间到了之后，再继续执行函数里后续的代码
        // 暂停1.5秒，再执行后续逻辑
        await new Promise((resolve) => setTimeout(resolve, 1500));

        let testResult;
        // 调用 API 测试连接
        if (type === 'bmc'){
          testResult = await bmc_test_connect(this.bmc.ip, this.bmc.username, this.bmc.password);
        }
        else{
          testResult = await os_test_connect(this.os.ip, this.os.username, this.os.password);
        }

        if (testResult) {
          target.status = "success";
          target.connected = true;
          this.saveConnection(type)
        } else {
          target.status = "failure";
          target.connected = false;
        }

        const message = testResult
          ? `✅ ${type.toUpperCase()} 连接成功！`
          : `❌ ${type.toUpperCase()} 连接失败，请检查信息！`;
        console.log(message);
      } catch (error) {
        target.status = "failure";
        target.connected = false;
        console.error(`${type.toUpperCase()} 连接测试出错:`, error);
        alert("连接测试出错，请检查网络！");
      } finally {
        target.testing = false;
      }
    },

    // 保存配置到数据库
    async saveConnection(type) {
      const target = this[type];

      if (!target.ip || !target.username || !target.password) {
        alert("请填写完整的连接信息");
        return;
      }

      if (!this.isValidIP(target.ip)) {
        alert("IP地址格式不正确");
        return;
      }

      try {
        // API调用保存到数据库
        const userInfo = localStorage.getItem('user_info');
        const user = JSON.parse(userInfo);
        const username = user.username
        console.log("当前用户为", username)
        let saveResult;
        if (type === 'bmc'){
          saveResult = await bmc_save(username, this.bmc.ip, this.bmc.username, this.bmc.password);
        }
        else{
          saveResult = await os_save(username, this.os.ip, this.os.username, this.os.password);
        }

        if (saveResult.success) {
          alert(`${type.toUpperCase()} 配置保存成功！`);

          console.log(`${type.toUpperCase()} 配置已保存到数据库`);
        } else {
          alert(`保存失败: ${saveResult.message || "未知错误"}`);
        }
      } catch (error) {
        console.error(`${type.toUpperCase()}保存配置出错:`, error);
        alert("保存配置出错，请检查网络！");
      } finally {
        target.saving = false;
      }
    },

    // 密码是否隐藏
    togglePasswordVisibility(type) {
      this[type].showPassword = !this[type].showPassword;
    },

    getStatusIcon(status) {
      switch (status) {
        case "success":
          return "✅";
        case "failure":
          return "❌";
        case "disconnected":
          return "⚪";
        default:
          return "⚪";
      }
    },

    getStatusText(status) {
      switch (status) {
        case "success":
          return "连接成功";
        case "failure":
          return "连接失败";
        case "disconnected":
          return "未连接";
        default:
          return "未知状态";
      }
    },

    validateIP(type) {
      const ip = this[type].ip;
      // 简单的IP格式验证
      const ipPattern = /^(\d{1,3}\.){3}\d{1,3}$/;
      if (ip && !ipPattern.test(ip)) {
        // 这里可以添加更详细的IP验证逻辑
        console.log(`${type.toUpperCase()} IP格式可能不正确`);
      }
    },

    isValidIP(ip) {
      const ipPattern = /^(\d{1,3}\.){3}\d{1,3}$/;
      if (!ipPattern.test(ip)) return false;

      const parts = ip.split(".");
      for (let part of parts) {
        const num = parseInt(part, 10);
        if (num < 0 || num > 255) return false;
      }
      return true;
    },

    validateLength(type, field, maxLength) {
      const value = this[type][field];
      if (value.length > maxLength) {
        this[type][field] = value.substring(0, maxLength);
      }
    },
  },

  mounted() {
    // 1. 首先尝试从用户信息中读取连接配置
    const userInfoStr = localStorage.getItem("user_info");

    if (userInfoStr) {
      try {
        const userInfo = JSON.parse(userInfoStr);

        // 如果用户信息中有BMC连接配置，使用它
        if (userInfo.bmc_ip) {
          Object.assign(this.bmc, {
            ip: userInfo.bmc_ip,
            username: userInfo.bmc_username,
            password: userInfo.bmc_password,
          });
        }

        // 如果用户信息中有OS连接配置，使用它
        if (userInfo.os_ip) {
          Object.assign(this.os, {
            ip: userInfo.os_ip,
            username: userInfo.os_username,
            password: userInfo.os_password,
          });
        }
      } catch (e) {
        console.warn("加载用户信息失败:", e);
      }
    }

    // 2. 如果用户信息中没有连接配置，回退到原有的存储方式
    if (
      !userInfoStr ||
      (!this.bmc.ip && !this.bmc.username) ||
      (!this.os.ip && !this.os.username)
    ) {
      const savedBmc = localStorage.getItem("bmcConnection");
      const savedOs = localStorage.getItem("osConnection");

      if (savedBmc) {
        try {
          const bmcData = JSON.parse(savedBmc);
          Object.assign(this.bmc, {
            ...bmcData,
            testing: false,
            showPassword: false,
          });
        } catch (e) {
          console.warn("加载BMC连接信息失败:", e);
        }
      }

      if (savedOs) {
        try {
          const osData = JSON.parse(savedOs);
          Object.assign(this.os, {
            ...osData,
            testing: false,
            showPassword: false,
          });
        } catch (e) {
          console.warn("加载OS连接信息失败:", e);
        }
      }
    }

    // 3. 如果没有保存任何信息，可以使用默认值（已经在data中设置）
    console.log("加载的BMC配置:", this.bmc);
    console.log("加载的OS配置:", this.os);
  },

  watch: {
    bmc: {
      handler(newVal) {
        localStorage.setItem(
          "bmcConnection",
          JSON.stringify({
            ip: newVal.ip,
            username: newVal.username,
            password: newVal.password,
            status: newVal.status,
            connected: newVal.connected,
          })
        );
      },
      deep: true,
    },
    os: {
      handler(newVal) {
        localStorage.setItem(
          "osConnection",
          JSON.stringify({
            ip: newVal.ip,
            username: newVal.username,
            password: newVal.password,
            status: newVal.status,
            connected: newVal.connected,
          })
        );
      },
      deep: true,
    },
  },
};
</script>

<style lang="scss" scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
  min-height: 100vh;

  /* 隐藏滚动条 */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */

  &::-webkit-scrollbar {
    display: none; /* Chrome, Safari, Opera */
  }
}

.page-header {
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(226, 232, 240, 0.8);
}

.page-header h1 {
  margin: 0 0 8px 0;
  color: #1e293b;
  font-size: 24px;
  font-weight: 600;
}

.page-header p {
  margin: 0;
  color: #64748b;
  font-size: 14px;
  font-weight: 400;
}

/* 连接卡片网格 */
.connection-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 28px;

  /* 隐藏滚动条 */
  scrollbar-width: none;
  -ms-overflow-style: none;

  &::-webkit-scrollbar {
    display: none;
  }
}

@media (max-width: 1100px) {
  .connection-grid {
    grid-template-columns: 1fr;
  }
}

.connection-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05), 0 8px 24px rgba(0, 0, 0, 0.08);
  padding: 32px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(226, 232, 240, 0.6);

  /* 隐藏滚动条 */
  scrollbar-width: none;
  -ms-overflow-style: none;

  &::-webkit-scrollbar {
    display: none;
  }

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08), 0 12px 32px rgba(0, 0, 0, 0.12);
    border-color: rgba(59, 130, 246, 0.3);
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 16px;
}

.card-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

.card-icon {
  font-size: 24px;
  color: white;
}

.card-title-content h2 {
  margin: 0 0 4px 0;
  color: #1e293b;
  font-size: 18px;
  font-weight: 600;
}

.card-subtitle {
  margin: 0;
  color: #64748b;
  font-size: 13px;
  font-weight: 400;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 12px;
  text-align: right;
}

.status-indicator-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: rgba(226, 232, 240, 0.4);
  border-radius: 50%;
  border: 2px solid rgba(226, 232, 240, 0.8);
}

.status-indicator {
  font-size: 18px;

  &.success {
    color: #10b981;
  }

  &.failure {
    color: #ef4444;
  }

  &.disconnected {
    color: #94a3b8;
  }
}

.status-content {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.status-text {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
}

.card-divider {
  height: 1px;
  background: linear-gradient(
    90deg,
    rgba(226, 232, 240, 0) 0%,
    rgba(226, 232, 240, 1) 50%,
    rgba(226, 232, 240, 0) 100%
  );
  margin: 24px 0;
}

/* 表单样式 */
.connection-form {
  .form-group {
    margin-bottom: 24px;
    position: relative;
  }
}

.connection-form label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  color: #475569;
  font-weight: 500;
  font-size: 14px;
}

.label-icon {
  font-size: 16px;
  opacity: 0.7;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.3s ease;
  background-color: white;
  color: #1e293b;
  box-sizing: border-box;

  &:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
    outline: none;
  }

  &:disabled {
    background-color: #f8fafc;
    color: #94a3b8;
    cursor: not-allowed;
    border-color: #e2e8f0;
  }

  &::placeholder {
    color: #94a3b8;
  }
}

.btn-action {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s ease;
  padding: 0;

  &:hover {
    background-color: #f1f5f9;
    color: #3b82f6;
  }

  &:active {
    transform: scale(0.95);
  }

  .action-icon {
    font-size: 18px;
    line-height: 1;
  }
}

.password-input {
  position: relative;

  .toggle-password {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: #64748b;
    cursor: pointer;
    font-size: 18px;
    padding: 0;
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;

    &:hover {
      background-color: #f1f5f9;
      color: #3b82f6;
    }
  }
}

/* 调整操作按钮布局 */
.card-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.card-actions .btn {
  flex: 1;
}

.btn {
  width: 100%;
  padding: 16px 24px;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  position: relative;
  overflow: hidden;
  box-sizing: border-box;

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }

  &:hover:not(:disabled) {
    transform: translateY(-2px);
  }

  &:active:not(:disabled) {
    transform: translateY(0);
  }
}

.btn-save {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);

  &:hover:not(:disabled) {
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 10px;
  position: relative;
  z-index: 1;
}

.btn-icon {
  font-size: 18px;
}

.btn-test {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);

  &:hover:not(:disabled) {
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
  }

  &.testing {
    background: linear-gradient(135deg, #64748b 0%, #475569 100%);
  }
}

/* 加载动画 */
.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .card-actions {
    flex-direction: column;
    gap: 12px;
  }

  .card-actions .btn {
    width: 100%;
  }
}

/* 输入框长度限制样式 */
.form-input {
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 密码输入框特别处理 */
.password-input .form-input {
  padding-right: 50px; /* 为切换密码按钮留出空间 */
}
</style>
