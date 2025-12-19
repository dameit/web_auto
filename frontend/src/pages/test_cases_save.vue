<template>
  <div class="test-cases-save">
    <!-- 顶部IP信息和文件选择区域 -->
    <div class="top-info-section">
      <div class="top-info-container">
        <!-- IP信息显示在同一行 -->
        <div class="ip-info-row">
          <div class="ip-display">
            <span class="ip-label">BMC IP:</span>
            <span class="ip-value">{{ bmcIp }}</span>
          </div>
          <div class="ip-display">
            <span class="ip-label">OS IP:</span>
            <span class="ip-value">{{ osIp }}</span>
          </div>
        </div>

        <!-- 文件选择区域 -->
        <div class="file-selection-row">
          <div class="file-select-wrapper">
            <div class="file-select-btn" @click="triggerFileInput">
              <span class="btn-icon">📁</span>
              <span class="btn-text">选择配置文件</span>
            </div>
            <input
              type="file"
              ref="fileInput"
              @change="handleFileSelect"
              class="file-input"
            />
          </div>

          <div class="selected-file-info" v-if="selectedFile">
            <div class="file-info-content">
              <span class="file-icon">📄</span>
              <div class="file-details">
                <span class="file-name">{{ selectedFile.name }}</span>
                <span class="file-meta"
                  >{{ formatFileSize(selectedFile.size) }} •
                  {{ getFileType(selectedFile.name) }}</span
                >
              </div>
              <button
                @click="clearFile"
                class="clear-file-btn"
                title="清除文件"
              >
                <span class="clear-icon">×</span>
              </button>
            </div>
          </div>
          <div class="no-file-placeholder" v-else>未选择任何配置文件</div>
        </div>
      </div>
    </div>

    <!-- 设置标签区域 -->
    <div class="settings-section">
      <div class="section-header">
        <div class="section-title-area">
          <h3 class="section-title">配置选项</h3>
          <div class="selected-count-badge">
            <span class="count-number">{{ selectedCount }}</span>
            <span class="count-label">/{{ settings.length }}</span>
          </div>
        </div>

        <div class="selection-controls">
          <button @click="selectAll" class="control-btn select-all-btn">
            <span class="control-icon">✓</span>
            <span class="control-text">全选</span>
          </button>
          <button @click="deselectAll" class="control-btn deselect-all-btn">
            <span class="control-icon">✗</span>
            <span class="control-text">取消全选</span>
          </button>
        </div>
      </div>

      <div class="settings-grid">
        <div
          v-for="setting in settings"
          :key="setting.id"
          class="setting-item"
          :class="{ selected: setting.selected }"
          @click="toggleSetting(setting.id)"
        >
          <div class="setting-checkbox">
            <div class="checkbox-visual" :class="{ checked: setting.selected }">
              <span v-if="setting.selected" class="checkmark">✓</span>
            </div>
          </div>
          <div class="setting-content">
            <span class="setting-icon">{{ setting.icon }}</span>
            <span class="setting-text">{{ setting.name }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 开始测试按钮 -->
    <div class="action-section">
      <button
        @click="startTest"
        class="start-test-btn"
        :disabled="!hasSelectedSettings"
        :class="{ disabled: !hasSelectedSettings }"
      >
        <span class="test-icon">▶</span>
        <span class="test-text">开始测试</span>
        <span class="test-subtext">({{ selectedCount }}个配置项)</span>
      </button>
    </div>

    <!-- 测试截图区域 -->
    <div class="screenshots-section">
      <!-- 测试前截图区域 -->
      <div class="screenshot-panel">
        <div class="panel-header">
          <div class="panel-title-area">
            <h3 class="panel-title">
              <span class="panel-title-icon">📷</span>
              测试前配置截图
            </h3>
            <div class="screenshot-count" v-if="beforeScreenshots.length > 0">
              {{ beforeScreenshots.length }}张截图
            </div>
          </div>

          <div class="panel-actions">
            <button @click="addBeforeScreenshot" class="action-btn add-btn">
              <span class="action-icon">+</span>
              添加截图
            </button>
            <button
              @click="clearBeforeScreenshots"
              class="action-btn clear-btn"
              :disabled="beforeScreenshots.length === 0"
            >
              <span class="action-icon">🗑️</span>
              清空
            </button>
          </div>
        </div>

        <div class="screenshot-container">
          <div
            v-if="beforeScreenshots.length === 0"
            class="empty-screenshot-placeholder"
            @click="addBeforeScreenshot"
          >
            <div class="placeholder-icon">📷</div>
            <div class="placeholder-text">点击添加测试前截图</div>
            <div class="placeholder-hint">支持所有图片格式，无数量限制</div>
          </div>

          <div v-else class="screenshot-scroll-container">
            <div class="screenshot-grid">
              <div
                v-for="(screenshot, index) in beforeScreenshots"
                :key="'before-' + index"
                class="screenshot-item"
              >
                <div class="screenshot-wrapper">
                  <img
                    :src="screenshot.url"
                    :alt="screenshot.name"
                    class="screenshot-image"
                    @load="onImageLoad"
                  />
                  <div class="screenshot-overlay">
                    <button
                      @click.stop="removeBeforeScreenshot(index)"
                      class="remove-btn"
                      title="删除截图"
                    >
                      <span class="remove-icon">×</span>
                    </button>
                    <span class="screenshot-name">{{ screenshot.name }}</span>
                  </div>
                  <div class="screenshot-index">{{ index + 1 }}</div>
                </div>
              </div>

              <!-- 添加更多截图按钮 -->
              <div
                class="screenshot-item add-more-item"
                @click="addBeforeScreenshot"
              >
                <div class="add-more-content">
                  <span class="add-icon">+</span>
                  <span class="add-text">添加更多截图</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 测试后截图区域 -->
      <div class="screenshot-panel">
        <div class="panel-header">
          <div class="panel-title-area">
            <h3 class="panel-title">
              <span class="panel-title-icon">📷</span>
              测试后配置截图
            </h3>
            <div class="screenshot-count" v-if="afterScreenshots.length > 0">
              {{ afterScreenshots.length }}张截图
            </div>
          </div>

          <div class="panel-actions">
            <button @click="addAfterScreenshot" class="action-btn add-btn">
              <span class="action-icon">+</span>
              添加截图
            </button>
            <button
              @click="clearAfterScreenshots"
              class="action-btn clear-btn"
              :disabled="afterScreenshots.length === 0"
            >
              <span class="action-icon">🗑️</span>
              清空
            </button>
          </div>
        </div>

        <div class="screenshot-container">
          <div
            v-if="afterScreenshots.length === 0"
            class="empty-screenshot-placeholder"
            @click="addAfterScreenshot"
          >
            <div class="placeholder-icon">📷</div>
            <div class="placeholder-text">点击添加测试后截图</div>
            <div class="placeholder-hint">支持所有图片格式，无数量限制</div>
          </div>

          <div v-else class="screenshot-scroll-container">
            <div class="screenshot-grid">
              <div
                v-for="(screenshot, index) in afterScreenshots"
                :key="'after-' + index"
                class="screenshot-item"
              >
                <div class="screenshot-wrapper">
                  <img
                    :src="screenshot.url"
                    :alt="screenshot.name"
                    class="screenshot-image"
                    @load="onImageLoad"
                  />
                  <div class="screenshot-overlay">
                    <button
                      @click.stop="removeAfterScreenshot(index)"
                      class="remove-btn"
                      title="删除截图"
                    >
                      <span class="remove-icon">×</span>
                    </button>
                    <span class="screenshot-name">{{ screenshot.name }}</span>
                  </div>
                  <div class="screenshot-index">{{ index + 1 }}</div>
                </div>
              </div>

              <!-- 添加更多截图按钮 -->
              <div
                class="screenshot-item add-more-item"
                @click="addAfterScreenshot"
              >
                <div class="add-more-content">
                  <span class="add-icon">+</span>
                  <span class="add-text">添加更多截图</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 隐藏的文件输入元素，用于截图上传 -->
    <input
      type="file"
      ref="screenshotInput"
      @change="handleScreenshotUpload"
      multiple
      class="hidden-file-input"
      id="screenshotInput"
    />
  </div>
</template>

<script>
import { file_save, start_test } from "@/api";
import { ElNotification } from 'element-plus'

export default {
  name: "TestCasesSave",
  data() {
    // 后端返回了所有信息，login.vue登录时将这些信息存储到了user_info中
    const userInfo = localStorage.getItem("user_info");
    const user = JSON.parse(userInfo);
    const bmc_ip = user.bmc_ip;
    const os_ip = user.os_ip;
    return {
      bmcIp: bmc_ip || "请返回首页添加BMC IP",
      osIp: os_ip || "请返回首页添加OS IP",
      selectedFile: null,
      settings: [
        { id: "syslog", name: "Syslog设置", icon: "📋", selected: false },
        { id: "trap", name: "Trap设置", icon: "🚨", selected: false },
        { id: "snmp", name: "SNMP设置", icon: "📡", selected: false },
        { id: "email", name: "邮件告警", icon: "📧", selected: false },
        { id: "power", name: "通电开机策略", icon: "🔌", selected: false },
        { id: "network", name: "网络设置", icon: "🌐", selected: false },
        { id: "user", name: "用户/用户组", icon: "👥", selected: false },
        { id: "ldap", name: "LDAP", icon: "🔐", selected: false },
        { id: "ad", name: "AD", icon: "🏢", selected: false },
        { id: "bios", name: "BIOS设置", icon: "⚙️", selected: false },
        { id: "datetime", name: "日期&时间", icon: "🕐", selected: false },
        { id: "logs", name: "日志设置", icon: "📝", selected: false },
      ],
      beforeScreenshots: [],
      afterScreenshots: [],
      screenshotTarget: "before", // 'before' 或 'after'
    };
  },
  computed: {
    selectedCount() {
      return this.settings.filter((setting) => setting.selected).length;
    },
    hasSelectedSettings() {
      return this.selectedCount > 0;
    },
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    // event就是原生点击事件对象
    async handleFileSelect(event) {
      // event.target.files：文件选择框的选中文件列表
      // files 是 <input type="file"> 元素的内置属性，仅该类型的输入框有这个属性：
      const files = event.target.files;
      if (files.length > 0) {
        this.selectedFile = files[0];
        console.log("已选择文件:", this.selectedFile);
      }

      // 创建FormData对象（文件上传必须用FormData）
      const formData = new FormData();
      // 核心：将选中的文件对象添加到FormData，key为"file"（后端需对应这个key）
      formData.append("file", this.selectedFile);
      // 添加用户名
      const userInfo = localStorage.getItem("user_info");
      const user = JSON.parse(userInfo);
      const username = user.username;
      formData.append("username", username);
      const file_save_result = await file_save(formData);
      if (file_save_result.success) {
        console.log(`文件已保存到数据库`, file_save_result);
      } 
      else {
        console.log(`保存失败: ${file_save_result.message || "未知错误"}`);
      }
    },

    clearFile() {
      this.selectedFile = null;
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = "";
      }
    },

    formatFileSize(bytes) {
      if (bytes === 0) return "0 Bytes";
      const k = 1024;
      const sizes = ["Bytes", "KB", "MB", "GB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
    },

    getFileType(filename) {
      const extension = filename.split(".").pop().toLowerCase();
      const fileTypes = {
        txt: "文本文件",
        json: "JSON文件",
        xml: "XML文件",
        yaml: "YAML文件",
        yml: "YAML文件",
        conf: "配置文件",
        ini: "配置文件",
        cfg: "配置文件",
        csv: "CSV文件",
      };

      return fileTypes[extension] || `${extension.toUpperCase()}文件`;
    },

    // 是否选中
    toggleSetting(settingId) {
      const setting = this.settings.find((s) => s.id === settingId);
      if (setting) {
        setting.selected = !setting.selected;
      }
    },

    selectAll() {
      this.settings.forEach((setting) => {
        setting.selected = true;
      });
    },

    deselectAll() {
      this.settings.forEach((setting) => {
        setting.selected = false;
      });
    },

    async startTest() {
      if (!this.hasSelectedSettings) {
        ElNotification({
          title: "提示",
          message: "请至少选择一个配置项进行测试",
          type: "warning",
        });
        return;
      }

      const selectedSettings = this.settings
        .filter((setting) => setting.selected)
        .map((setting) => setting.name);

      console.log("开始测试以下配置项:", selectedSettings);

      const userInfo = localStorage.getItem("user_info");
      const user = JSON.parse(userInfo);
      const bmc_ip = user.bmc_ip;
      const bmc_username = user.bmc_username;
      const bmc_password = user.bmc_password;
      const test_result = await start_test(bmc_ip, bmc_username, bmc_password, selectedSettings)
      if (test_result.success) {
        console.log(`web自动化操作通过`, test_result);
      } 
      else {
        console.log(`web自动化操作失败: ${test_result.message || "未知错误"}`);
      }

      ElNotification({
        title: "开始测试",
        message: `开始测试 ${this.selectedCount} 个配置项...`,
        type: "success",
      });
    },

    addBeforeScreenshot() {
      this.screenshotTarget = "before";
      this.$refs.screenshotInput.click();
    },

    addAfterScreenshot() {
      this.screenshotTarget = "after";
      this.$refs.screenshotInput.click();
    },

    handleScreenshotUpload(event) {
      const files = event.target.files;
      if (files.length === 0) return;

      const timestamp = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });

      for (let i = 0; i < files.length; i++) {
        const file = files[i];

        // 创建URL以预览图片
        const imageUrl = URL.createObjectURL(file);

        const screenshot = {
          name: `截图_${timestamp}_${i + 1}`,
          url: imageUrl,
          file: file,
          type: file.type,
          size: file.size,
        };

        if (this.screenshotTarget === "before") {
          this.beforeScreenshots.push(screenshot);
        } else {
          this.afterScreenshots.push(screenshot);
        }
      }

      // 重置文件输入，以便可以再次选择相同的文件
      event.target.value = "";

      // 显示添加成功提示
      this.$notify({
        title: "截图添加成功",
        message: `成功添加 ${files.length} 张截图`,
        type: "success",
      });
    },

    onImageLoad(event) {
      // 图片加载完成后的处理，可以在这里添加懒加载或其他处理
      event.target.classList.add("loaded");
    },

    removeBeforeScreenshot(index) {
      // 释放URL对象
      if (this.beforeScreenshots[index].url) {
        URL.revokeObjectURL(this.beforeScreenshots[index].url);
      }
      this.beforeScreenshots.splice(index, 1);

      this.$notify({
        title: "截图已删除",
        message: "测试前截图已成功删除",
        type: "info",
      });
    },

    removeAfterScreenshot(index) {
      // 释放URL对象
      if (this.afterScreenshots[index].url) {
        URL.revokeObjectURL(this.afterScreenshots[index].url);
      }
      this.afterScreenshots.splice(index, 1);

      this.$notify({
        title: "截图已删除",
        message: "测试后截图已成功删除",
        type: "info",
      });
    },

    clearBeforeScreenshots() {
      // 释放所有URL对象
      this.beforeScreenshots.forEach((screenshot) => {
        if (screenshot.url) {
          URL.revokeObjectURL(screenshot.url);
        }
      });
      this.beforeScreenshots = [];

      this.$notify({
        title: "截图已清空",
        message: "所有测试前截图已清空",
        type: "info",
      });
    },

    clearAfterScreenshots() {
      // 释放所有URL对象
      this.afterScreenshots.forEach((screenshot) => {
        if (screenshot.url) {
          URL.revokeObjectURL(screenshot.url);
        }
      });
      this.afterScreenshots = [];

      this.$notify({
        title: "截图已清空",
        message: "所有测试后截图已清空",
        type: "info",
      });
    },
  },

  beforeDestroy() {
    // 组件销毁前释放所有图片URL
    this.beforeScreenshots.forEach((screenshot) => {
      if (screenshot.url) {
        URL.revokeObjectURL(screenshot.url);
      }
    });

    this.afterScreenshots.forEach((screenshot) => {
      if (screenshot.url) {
        URL.revokeObjectURL(screenshot.url);
      }
    });
  },
};
</script>

<style lang="scss" scoped>
.test-cases-save {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  background-color: #f8fafc;
  min-height: 100vh;
}

/* 顶部信息区域样式 */
.top-info-section {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.top-info-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.ip-info-row {
  display: flex;
  align-items: center;
  gap: 30px;
  flex: 1;
}

.ip-display {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f1f5f9;
  padding: 10px 16px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  min-width: 200px;
}

.ip-label {
  font-weight: 600;
  color: #475569;
  font-size: 14px;
}

.ip-value {
  color: #1e293b;
  font-family: "SF Mono", Monaco, "Courier New", monospace;
  font-weight: 500;
  font-size: 15px;
  letter-spacing: 0.5px;
}

.file-selection-row {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
  justify-content: flex-end;
}

.file-select-wrapper {
  position: relative;
}

.file-input {
  display: none;
}

.file-select-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  padding: 11px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  font-size: 14px;
  transition: all 0.25s ease;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
  border: none;
  white-space: nowrap;

  &:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
  }

  &:active {
    transform: translateY(0);
  }
}

.selected-file-info {
  background: white;
  padding: 10px 15px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  min-width: 250px;
  max-width: 350px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.file-info-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.file-icon {
  font-size: 18px;
  color: #3b82f6;
}

.file-details {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.file-name {
  font-weight: 500;
  color: #334155;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-meta {
  color: #64748b;
  font-size: 12px;
  margin-top: 2px;
}

.clear-file-btn {
  background: transparent;
  border: none;
  color: #94a3b8;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.2s ease;

  &:hover {
    background: #fef2f2;
    color: #ef4444;
  }
}

.no-file-placeholder {
  color: #94a3b8;
  font-style: italic;
  font-size: 14px;
  padding: 10px 15px;
}

/* 设置区域样式 */
.settings-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 18px;
  border-bottom: 1px solid #f1f5f9;
}

.section-title-area {
  display: flex;
  align-items: center;
  gap: 12px;
}

.section-title {
  margin: 0;
  font-size: 18px;
  color: #1e293b;
  font-weight: 600;
}

.selected-count-badge {
  display: flex;
  align-items: center;
  background: #f1f5f9;
  border-radius: 20px;
  padding: 4px 10px;
  font-size: 14px;
  border: 1px solid #e2e8f0;
}

.count-number {
  color: #3b82f6;
  font-weight: 600;
}

.count-label {
  color: #64748b;
}

.selection-controls {
  display: flex;
  gap: 10px;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 9px 16px;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  background: white;
  color: #475569;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    transform: translateY(-1px);
  }
}

.select-all-btn {
  &:hover {
    background: #f0f9ff;
    border-color: #7dd3fc;
    color: #0369a1;
  }
}

.deselect-all-btn {
  &:hover {
    background: #fef2f2;
    border-color: #fecaca;
    color: #dc2626;
  }
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.setting-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: #f1f5f9;
    border-color: #cbd5e1;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  }

  &.selected {
    background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%);
    border-color: #93c5fd;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
  }
}

.setting-checkbox {
  display: flex;
  align-items: center;
  justify-content: center;
}

.checkbox-visual {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  border: 2px solid #cbd5e1;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;

  &.checked {
    background: #3b82f6;
    border-color: #3b82f6;
  }
}

.checkmark {
  color: white;
  font-size: 12px;
  font-weight: bold;
}

.setting-content {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.setting-icon {
  font-size: 16px;
}

.setting-text {
  font-size: 14px;
  color: #334155;
  font-weight: 500;
}

/* 开始测试按钮区域 */
.action-section {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

.start-test-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  padding: 16px 40px;
  border-radius: 10px;
  border: none;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);

  &:hover:not(.disabled) {
    background: linear-gradient(135deg, #059669 0%, #047857 100%);
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
  }

  &:active:not(.disabled) {
    transform: translateY(-1px);
  }

  &.disabled {
    background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
    cursor: not-allowed;
    box-shadow: none;
  }
}

.test-icon {
  font-size: 18px;
}

.test-subtext {
  font-size: 14px;
  font-weight: 500;
  opacity: 0.9;
}

/* 截图区域样式 */
.screenshots-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 40px;
}

.screenshot-panel {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  height: 500px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 20px;
  background: linear-gradient(90deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid #e2e8f0;
}

.panel-title-area {
  display: flex;
  align-items: center;
  gap: 10px;
}

.panel-title {
  margin: 0;
  font-size: 16px;
  color: #1e293b;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-title-icon {
  font-size: 18px;
}

.screenshot-count {
  font-size: 13px;
  color: #64748b;
  background: #f1f5f9;
  padding: 4px 10px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.panel-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 15px;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  background: white;
  color: #475569;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover:not(:disabled) {
    transform: translateY(-1px);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.add-btn {
  &:hover:not(:disabled) {
    background: #f0f9ff;
    border-color: #7dd3fc;
    color: #0369a1;
  }
}

.clear-btn {
  &:hover:not(:disabled) {
    background: #fef2f2;
    border-color: #fecaca;
    color: #ef4444;
  }
}

.screenshot-container {
  flex: 1;
  padding: 20px;
  background: #fafafa;
  overflow: hidden;
}

.empty-screenshot-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #94a3b8;
  cursor: pointer;
  border: 2px dashed #cbd5e1;
  border-radius: 10px;
  padding: 30px;
  transition: all 0.2s ease;
  text-align: center;

  &:hover {
    border-color: #93c5fd;
    background: #f0f9ff;
    color: #3b82f6;
    transform: translateY(-2px);
  }
}

.placeholder-icon {
  font-size: 48px;
  margin-bottom: 15px;
  opacity: 0.7;
}

.placeholder-text {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 8px;
}

.placeholder-hint {
  font-size: 13px;
  max-width: 200px;
  line-height: 1.4;
}

.screenshot-scroll-container {
  height: 100%;
  overflow-y: auto;
  padding-right: 5px;
}

.screenshot-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 16px;
}

.screenshot-item {
  aspect-ratio: 4/3;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
  }
}

.screenshot-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  background: #f8fafc;
}

.screenshot-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  /* 等比缩放图片以适应容器 */
  background: #f8fafc;
  transition: opacity 0.3s ease;

  &:not(.loaded) {
    opacity: 0;
  }
}

.screenshot-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  opacity: 0;
  transition: opacity 0.2s ease;

  .screenshot-item:hover & {
    opacity: 1;
  }
}

.screenshot-name {
  color: white;
  font-size: 12px;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100px;
}

.remove-btn {
  background: rgba(239, 68, 68, 0.9);
  color: white;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;

  &:hover {
    background: #dc2626;
    transform: scale(1.1);
  }
}

.screenshot-index {
  position: absolute;
  top: 6px;
  left: 6px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
}

.add-more-item {
  border: 2px dashed #cbd5e1;
  background: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;

  &:hover {
    border-color: #93c5fd;
    background: #f0f9ff;

    .add-more-content {
      color: #3b82f6;
    }
  }
}

.add-more-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #94a3b8;
  transition: all 0.2s ease;
}

.add-icon {
  font-size: 24px;
  font-weight: 300;
}

.add-text {
  font-size: 13px;
  font-weight: 500;
}

.hidden-file-input {
  display: none;
}

/* 滚动条样式 */
.screenshot-scroll-container::-webkit-scrollbar {
  width: 6px;
}

.screenshot-scroll-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.screenshot-scroll-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.screenshot-scroll-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 响应式设计 */
@media (max-width: 1100px) {
  .top-info-container {
    flex-direction: column;
    align-items: stretch;
  }

  .ip-info-row {
    justify-content: center;
  }

  .file-selection-row {
    justify-content: center;
  }
}

@media (max-width: 992px) {
  .screenshots-section {
    grid-template-columns: 1fr;
  }

  .settings-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  }

  .screenshot-panel {
    height: 450px;
  }
}

@media (max-width: 768px) {
  .test-cases-save {
    padding: 15px;
  }

  .section-header {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
  }

  .selection-controls {
    justify-content: flex-end;
  }

  .ip-info-row {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }

  .ip-display {
    min-width: auto;
  }

  .file-selection-row {
    flex-direction: column;
    align-items: stretch;
  }

  .selected-file-info {
    max-width: 100%;
  }

  .screenshot-grid {
    grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  }

  .panel-header {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
  }

  .panel-actions {
    justify-content: flex-end;
  }
}

@media (max-width: 576px) {
  .settings-grid {
    grid-template-columns: 1fr 1fr;
  }

  .screenshot-panel {
    height: 400px;
  }

  .panel-title-area {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }

  .panel-actions {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
