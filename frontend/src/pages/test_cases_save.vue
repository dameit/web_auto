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
              <span class="btn-text">选择BMC固件文件</span>
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

    <!-- 三个测试按钮 -->
    <div class="action-section">
      <div class="action-buttons-grid">
        <!-- 刷新前测试按钮 -->
        <button
          @click="startTest"
          class="action-test-btn refresh-pre-btn"
          :disabled="!beforeTestingClick"
          :class="{
            disabled: !hasSelectedSettings || currentTestingSetting,
            testing: currentTestingSetting,
          }"
        >
          <span class="test-icon">{{
            currentTestingSetting ? "⏳" : "▶"
          }}</span>
          <span class="test-text">
            {{
              currentTestingSetting
                ? `正在测试：${currentTestingSetting}`
                : "刷新前测试"
            }}
          </span>
          <span class="test-subtext">
            {{
              currentTestingSetting
                ? `(第${testingProgress}个/共${totalTesting}个配置项)`
                : `(${selectedCount}个配置项)`
            }}
          </span>
        </button>

        <!-- 刷新BMC固件按钮 -->
        <button
          @click="refreshFirmware"
          class="action-test-btn refresh-firmware-btn"
          :disabled="!fwRefreshClick"
          :class="{ disabled: !selectedFile || isRefreshingFirmware }"
        >
          <span class="test-icon">{{ isRefreshingFirmware ? "⏳" : "▶" }}</span>
          <span class="test-text">
            {{ isRefreshingFirmware ? "正在刷新固件..." : "刷新BMC固件" }}
          </span>
          <span class="test-subtext">
            {{ selectedFile ? "(固件已上传)" : "(请先选择固件)" }}
          </span>
        </button>

        <!-- 刷新后测试按钮 -->
        <button
          @click="afterRefreshTest"
          class="action-test-btn refresh-post-btn"
          :disabled="!afterTestingClick"
          :class="{
            disabled: !hasSelectedSettings || currentAfterTestingSetting,
            testing: currentAfterTestingSetting,
          }"
        >
          <span class="test-icon">{{
            currentAfterTestingSetting ? "⏳" : "▶"
          }}</span>
          <span class="test-text">
            {{
              currentAfterTestingSetting
                ? `正在测试：${currentAfterTestingSetting}`
                : "刷新后测试"
            }}
          </span>
          <span class="test-subtext">
            {{
              currentAfterTestingSetting
                ? `(第${afterTestingProgress}个/共${afterTotalTesting}个配置项)`
                : `(${selectedCount}个配置项)`
            }}
          </span>
        </button>
      </div>
    </div>

    <!-- 日志显示区域 -->
    <div
      class="test-logs-section"
      v-if="testLogs.length > 0 || isTesting || isAfterTesting"
    >
      <div class="logs-panel">
        <div class="panel-header">
          <div class="panel-title-area">
            <h3 class="panel-title">
              <span class="panel-title-icon">📝</span>
              测试日志
            </h3>
          </div>

          <div class="panel-actions">
            <button
              @click="clearTestLogs"
              class="action-btn clear-btn"
              :disabled="testLogs.length === 0"
            >
              <span class="action-icon">🗑️</span>
              清空日志
            </button>
          </div>
        </div>

        <div class="logs-container">
          <div class="logs-content" ref="logsContainer">
            <div v-for="(log, index) in testLogs" :key="index" class="log-item">
              <div class="log-time">{{ formatTime(log.time) }}</div>
              <div class="log-message">{{ log.message }}</div>
            </div>
          </div>
        </div>
      </div>
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
              <span v-if="selectedBeforeCount > 0" class="selected-count">
                (已选中{{ selectedBeforeCount }}张)
              </span>
            </div>
          </div>

          <div class="panel-actions">
            <div
              class="batch-controls-wrapper"
              v-if="beforeScreenshots.length > 0"
            >
              <div class="batch-controls">
                <button
                  @click="selectAllBefore"
                  class="action-btn select-all-btn"
                >
                  <span class="action-icon">✓</span>
                  <span class="action-text">全选</span>
                </button>
                <button
                  @click="deselectAllBefore"
                  class="action-btn deselect-all-btn"
                >
                  <span class="action-icon">✗</span>
                  <span class="action-text">取消</span>
                </button>
                <button
                  @click="downloadSelectedBefore"
                  class="action-btn download-btn"
                  :disabled="selectedBeforeCount === 0"
                >
                  <span class="action-icon">⬇</span>
                  <span class="action-text">下载</span>
                </button>
              </div>
              <button
                @click="clearBeforeScreenshots"
                class="action-btn clear-btn"
              >
                <span class="action-icon">🗑️</span>
                <span class="action-text">清空</span>
              </button>
            </div>
          </div>
        </div>

        <div class="screenshot-container">
          <div
            v-if="beforeScreenshots.length === 0"
            class="empty-screenshot-placeholder"
          >
            <div class="placeholder-icon">📷</div>
          </div>

          <div v-else class="screenshot-scroll-container">
            <div class="screenshot-grid">
              <div
                v-for="(screenshot, index) in beforeScreenshots"
                :key="'before-' + index"
                class="screenshot-item"
                :class="{ selected: screenshot.selected }"
                @click="toggleBeforeScreenshotSelection(index)"
              >
                <div class="screenshot-wrapper">
                  <!-- 添加选中标记 -->
                  <div class="selection-indicator" v-if="screenshot.selected">
                    <span class="checkmark">✓</span>
                  </div>
                  <img
                    :src="screenshot.url"
                    :alt="screenshot.name"
                    class="screenshot-image"
                    @load="onImageLoad"
                    @click.stop="previewImage('before', index)"
                  />
                  <div class="screenshot-overlay">
                    <div class="overlay-left">
                      <button
                        @click.stop="previewImage('before', index)"
                        class="preview-btn"
                        title="放大查看"
                      >
                        <span class="preview-icon">🔍</span>
                      </button>
                    </div>
                    <div class="overlay-right">
                      <button
                        @click.stop="removeBeforeScreenshot(index)"
                        class="remove-btn"
                        title="删除截图"
                      >
                        <span class="remove-icon">×</span>
                      </button>
                    </div>
                  </div>
                  <div class="screenshot-index">{{ index + 1 }}</div>
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
              <span v-if="selectedAfterCount > 0" class="selected-count">
                (已选中{{ selectedAfterCount }}张)
              </span>
            </div>
          </div>

          <div class="panel-actions">
            <div
              class="batch-controls-wrapper"
              v-if="afterScreenshots.length > 0"
            >
              <div class="batch-controls">
                <button
                  @click="selectAllAfter"
                  class="action-btn select-all-btn"
                >
                  <span class="action-icon">✓</span>
                  <span class="action-text">全选</span>
                </button>
                <button
                  @click="deselectAllAfter"
                  class="action-btn deselect-all-btn"
                >
                  <span class="action-icon">✗</span>
                  <span class="action-text">取消</span>
                </button>
                <button
                  @click="downloadSelectedAfter"
                  class="action-btn download-btn"
                  :disabled="selectedAfterCount === 0"
                >
                  <span class="action-icon">⬇</span>
                  <span class="action-text">下载</span>
                </button>
              </div>
              <button
                @click="clearAfterScreenshots"
                class="action-btn clear-btn"
              >
                <span class="action-icon">🗑️</span>
                <span class="action-text">清空</span>
              </button>
            </div>
          </div>
        </div>

        <div class="screenshot-container">
          <div
            v-if="afterScreenshots.length === 0"
            class="empty-screenshot-placeholder"
          >
            <div class="placeholder-icon">📷</div>
          </div>

          <div v-else class="screenshot-scroll-container">
            <div class="screenshot-grid">
              <div
                v-for="(screenshot, index) in afterScreenshots"
                :key="'after-' + index"
                class="screenshot-item"
                :class="{ selected: screenshot.selected }"
                @click="toggleAfterScreenshotSelection(index)"
              >
                <div class="screenshot-wrapper">
                  <!-- 添加选中标记 -->
                  <div class="selection-indicator" v-if="screenshot.selected">
                    <span class="checkmark">✓</span>
                  </div>
                  <img
                    :src="screenshot.url"
                    :alt="screenshot.name"
                    class="screenshot-image"
                    @load="onImageLoad"
                    @click.stop="previewImage('after', index)"
                  />
                  <div class="screenshot-overlay">
                    <div class="overlay-left">
                      <button
                        @click.stop="previewImage('after', index)"
                        class="preview-btn"
                        title="放大查看"
                      >
                        <span class="preview-icon">🔍</span>
                      </button>
                    </div>
                    <div class="overlay-right">
                      <button
                        @click.stop="removeAfterScreenshot(index)"
                        class="remove-btn"
                        title="删除截图"
                      >
                        <span class="remove-icon">×</span>
                      </button>
                    </div>
                  </div>
                  <div class="screenshot-index">{{ index + 1 }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 图片预览模态框 -->
    <div
      v-if="previewVisible"
      class="image-preview-modal"
      @click="closePreview"
    >
      <div class="preview-content" @click.stop>
        <div class="preview-header">
          <span class="preview-title">{{ currentPreview.name }}</span>
          <button @click="closePreview" class="close-preview-btn" title="关闭">
            <span class="close-icon">×</span>
          </button>
        </div>

        <div class="preview-body">
          <div class="image-container">
            <img
              :src="currentPreview.url"
              :alt="currentPreview.name"
              class="preview-image"
              @click.stop
            />
          </div>

          <div class="preview-navigation" v-if="totalPreviews > 1">
            <button
              @click="prevImage"
              class="nav-btn prev-btn"
              :disabled="previewIndex === 0"
            >
              <span class="nav-icon">←</span>
            </button>

            <div class="preview-counter">
              {{ previewIndex + 1 }} / {{ totalPreviews }}
            </div>

            <button
              @click="nextImage"
              class="nav-btn next-btn"
              :disabled="previewIndex === totalPreviews - 1"
            >
              <span class="nav-icon">→</span>
            </button>
          </div>

          <div class="preview-actions">
            <button
              @click="downloadCurrentPreview"
              class="action-btn download-btn"
            >
              <span class="action-icon">⬇</span>
              <span class="action-text">下载图片</span>
            </button>
            <button @click="closePreview" class="action-btn cancel-btn">
              <span class="action-text">关闭</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { file_save, start_test } from "@/api";
import { ElNotification } from "element-plus";
// 添加delay函数
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export default {
  name: "TestCasesSave",
  data() {
    const userInfo = localStorage.getItem("user_info");
    const user = JSON.parse(userInfo);
    const bmc_ip = user.bmc_ip;
    const os_ip = user.os_ip;
    return {
      bmcIp: bmc_ip || "请返回首页添加BMC IP",
      osIp: os_ip || "请返回首页添加OS IP",
      selectedFile: null,
      // 按钮点击后禁止再次点击
      beforeTestingClick: true,
      fwRefreshClick: true,
      afterTestingClick: true,
      // 刷新前测试相关状态
      currentTestingSetting: "", // 当前正在测试的配置项名称
      testingProgress: 0, // 当前测试进度（第几个）
      totalTesting: 0, // 总共要测试的数量
      // 刷新后测试相关状态
      currentAfterTestingSetting: "", // 刷新后当前正在测试的配置项名称
      afterTestingProgress: 0, // 刷新后当前测试进度（第几个）
      afterTotalTesting: 0, // 刷新后总共要测试的数量
      // 测试日志相关数据
      testLogs: [],
      isTesting: false,
      isAfterTesting: false,
      settings: [
        { id: "syslog", name: "Syslog设置", icon: "📋", selected: false },
        { id: "trap", name: "Trap设置", icon: "🚨", selected: false },
        { id: "snmp", name: "SNMP V1/V2设置", icon: "📡", selected: false },
        { id: "email", name: "SMTP设置", icon: "📧", selected: false },
        { id: "power", name: "上电开机策略", icon: "🔌", selected: false },
        { id: "network", name: "网络设置", icon: "🌐", selected: false },
        { id: "user", name: "用户/用户组", icon: "👥", selected: false },
        { id: "ldap", name: "LDAP/E-directory", icon: "🔐", selected: false },
        { id: "ad", name: "Active Directory", icon: "🏢", selected: false },
        { id: "bios", name: "BIOS设置", icon: "⚙️", selected: false },
        { id: "datetime", name: "日期&时间", icon: "🕐", selected: false },
        { id: "logs", name: "日志设置", icon: "📝", selected: false },
      ],
      beforeScreenshots: [],
      afterScreenshots: [],
      // 图片预览相关数据
      previewVisible: false,
      previewType: "", // 'before' 或 'after'
      previewIndex: 0,
      currentPreview: {
        url: "",
        name: "",
      },
    };
  },
  computed: {
    selectedCount() {
      return this.settings.filter((setting) => setting.selected).length;
    },
    hasSelectedSettings() {
      return this.selectedCount > 0;
    },
    // 测试前截图选中数量
    selectedBeforeCount() {
      return this.beforeScreenshots.filter((screenshot) => screenshot.selected)
        .length;
    },
    // 测试后截图选中数量
    selectedAfterCount() {
      return this.afterScreenshots.filter((screenshot) => screenshot.selected)
        .length;
    },
    // 获取当前预览类型的截图数组
    currentPreviews() {
      return this.previewType === "before"
        ? this.beforeScreenshots
        : this.afterScreenshots;
    },
    // 总预览图片数量
    totalPreviews() {
      return this.currentPreviews.length;
    },
  },

  methods: {
    // 添加日志
    addLog(message) {
      const log = {
        time: new Date(),
        message: message,
      };

      this.testLogs.push(log);

      // 滚动到底部
      this.$nextTick(() => {
        const container = this.$refs.logsContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },
    // 清空日志
    clearTestLogs() {
      this.testLogs = [];
      this.isTesting = false;
      this.isAfterTesting = false;
    },
    // 格式化时间
    formatTime(date) {
      const d = new Date(date);
      const year = d.getFullYear();
      const month = (d.getMonth() + 1).toString().padStart(2, "0");
      const day = d.getDate().toString().padStart(2, "0");
      const hours = d.getHours().toString().padStart(2, "0");
      const minutes = d.getMinutes().toString().padStart(2, "0");
      const seconds = d.getSeconds().toString().padStart(2, "0");
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    },

    // 图片预览相关方法
    previewImage(type, index) {
      this.previewType = type;
      this.previewIndex = index;
      this.updateCurrentPreview();
      this.previewVisible = true;

      // 防止背景滚动
      document.body.style.overflow = "hidden";
    },
    updateCurrentPreview() {
      if (
        this.currentPreviews.length > 0 &&
        this.previewIndex >= 0 &&
        this.previewIndex < this.totalPreviews
      ) {
        const screenshot = this.currentPreviews[this.previewIndex];
        this.currentPreview = {
          url: screenshot.url,
          name: screenshot.name,
        };
      }
    },

    prevImage() {
      if (this.previewIndex > 0) {
        this.previewIndex--;
        this.updateCurrentPreview();
      }
    },

    nextImage() {
      if (this.previewIndex < this.totalPreviews - 1) {
        this.previewIndex++;
        this.updateCurrentPreview();
      }
    },

    closePreview() {
      this.previewVisible = false;
      document.body.style.overflow = "";
    },

    downloadCurrentPreview() {
      if (!this.currentPreview.url) return;

      const screenshot = {
        name: this.currentPreview.name,
        url: this.currentPreview.url,
      };

      this.downloadSingleImage(screenshot);
    },

    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    async handleFileSelect(event) {
      const files = event.target.files;
      if (files.length > 0) {
        this.selectedFile = files[0];
        console.log("已选择文件:", this.selectedFile);
      }

      // 创建FormData对象
      const formData = new FormData();
      formData.append("file", this.selectedFile);
      const userInfo = localStorage.getItem("user_info");
      const user = JSON.parse(userInfo);
      const username = user.username;
      formData.append("username", username);
      const file_save_result = await file_save(formData);
      if (file_save_result.success) {
        console.log(`文件已保存到数据库`, file_save_result);
      } else {
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

    // 刷新固件功能（示例）
    async refreshFirmware() {
      if (!this.selectedFile) {
        ElNotification({
          title: "提示",
          message: "请先选择固件文件",
          type: "warning",
        });
        return;
      }

      this.isRefreshingFirmware = true;

      try {
        // 这里调用刷新固件的API
        // 示例代码，需要根据实际API调整
        this.addLog("├── 开始刷新BMC固件...");

        // 模拟刷新过程
        await delay(2000);

        this.addLog("└── BMC固件刷新完成");
        ElNotification({
          title: "成功",
          message: "BMC固件刷新完成",
          type: "success",
        });
      } catch (error) {
        this.addLog(`└── BMC固件刷新失败: ${error.message}`);
        ElNotification({
          title: "错误",
          message: "固件刷新失败",
          type: "error",
        });
      } finally {
        this.isRefreshingFirmware = false;
      }
    },

    // 切换测试前截图的选中状态
    toggleBeforeScreenshotSelection(index) {
      if (this.beforeScreenshots[index]) {
        this.beforeScreenshots[index].selected =
          !this.beforeScreenshots[index].selected;
      }
    },

    // 全选测试前截图
    selectAllBefore() {
      this.beforeScreenshots.forEach((screenshot) => {
        screenshot.selected = true;
      });
    },

    // 取消全选测试前截图
    deselectAllBefore() {
      this.beforeScreenshots.forEach((screenshot) => {
        screenshot.selected = false;
      });
    },

    // 下载选中的测试前截图
    async downloadSelectedBefore() {
      const selectedScreenshots = this.beforeScreenshots.filter(
        (s) => s.selected
      );

      if (selectedScreenshots.length === 0) {
        ElNotification({
          title: "提示",
          message: "请先选择要下载的截图",
          type: "warning",
        });
        return;
      }

      console.log(selectedScreenshots);
      // 批量下载
      for (let i = 0; i < selectedScreenshots.length; i++) {
        const screenshot = selectedScreenshots[i];

        try {
          // 下载当前图片
          await this.downloadSingleImage(screenshot);

          // 延迟一段时间，避免浏览器同时处理太多下载请求
          if (i < selectedScreenshots.length - 1) {
            await delay(500); // 500毫秒延迟
          }
        } catch (error) {
          console.error(`下载第 ${i + 1} 张图片失败:`, error);
        }
      }
    },

    // 切换测试后截图的选中状态
    toggleAfterScreenshotSelection(index) {
      if (this.afterScreenshots[index]) {
        this.afterScreenshots[index].selected =
          !this.afterScreenshots[index].selected;
      }
    },

    // 全选测试后截图
    selectAllAfter() {
      this.afterScreenshots.forEach((screenshot) => {
        screenshot.selected = true;
      });
    },

    // 取消全选测试后截图
    deselectAllAfter() {
      this.afterScreenshots.forEach((screenshot) => {
        screenshot.selected = false;
      });
    },

    // 下载选中的测试后截图
    async downloadSelectedAfter() {
      const selectedScreenshots = this.afterScreenshots.filter(
        (s) => s.selected
      );

      if (selectedScreenshots.length === 0) {
        ElNotification({
          title: "提示",
          message: "请先选择要下载的截图",
          type: "warning",
        });
        return;
      }

      console.log(selectedScreenshots);
      // 批量下载
      for (let i = 0; i < selectedScreenshots.length; i++) {
        const screenshot = selectedScreenshots[i];

        try {
          // 下载当前图片
          await this.downloadSingleImage(screenshot);

          // 延迟一段时间，避免浏览器同时处理太多下载请求
          if (i < selectedScreenshots.length - 1) {
            await delay(500); // 500毫秒延迟
          }
        } catch (error) {
          console.error(`下载第 ${i + 1} 张图片失败:`, error);
        }
      }
    },

    // 改进：下载单张图片
    downloadSingleImage(screenshot) {
      return new Promise((resolve, reject) => {
        try {
          // 直接处理 base64 数据
          const base64Data = screenshot.url.split(",")[1];

          // 将 base64 转换为 Blob
          const byteCharacters = atob(base64Data);
          const byteNumbers = new Array(byteCharacters.length);
          for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
          }
          const byteArray = new Uint8Array(byteNumbers);
          const blob = new Blob([byteArray], { type: "image/png" });

          // 创建下载链接
          const url = URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = url;

          // 设置下载文件名
          const sanitizedName = this.sanitizeFileName(screenshot.name);
          const extension = this.getImageExtension(screenshot.url);
          link.download = `${sanitizedName}.${extension}`;

          // 触发下载
          document.body.appendChild(link);
          link.click();

          // 清理
          setTimeout(() => {
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
            resolve();
          }, 100);
        } catch (error) {
          reject(error);
        }
      });
    },

    // 调整文件名
    sanitizeFileName(filename) {
      // 移除非法字符
      return filename
        .replace(/[<>:"/\\|?*]/g, "") // 移除非法字符
        .replace(/\s+/g, "_") // 替换空格为下划线
        .substring(0, 100); // 限制文件名长度
    },

    // 辅助方法：获取图片扩展名
    getImageExtension(url) {
      if (url.startsWith("data:")) {
        const mimeMatch = url.match(/data:image\/(\w+);/);
        if (mimeMatch && mimeMatch[1]) {
          return mimeMatch[1].toLowerCase();
        }
      }
      // 默认返回png
      return "png";
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

      console.log("开始刷新前测试以下配置项:", selectedSettings);
      const userInfo = localStorage.getItem("user_info");
      const user = JSON.parse(userInfo);
      const bmc_ip = user.bmc_ip;
      const bmc_username = user.bmc_username;
      const bmc_password = user.bmc_password;
      const is_before = true;
      this.beforeTestingClick = false;
      // 先清空之前的截图
      this.clearBeforeScreenshots();

      // 设置测试状态
      this.isTesting = true;
      this.totalTesting = selectedSettings.length;
      this.testingProgress = 0;
      this.currentTestingSetting = "";
      // 添加开始测试日志
      this.addLog(
        `├── 开始刷新前测试，共选择 ${selectedSettings.length} 个配置项：${selectedSettings}`
      );

      // 一个一个测
      for (let i = 0; i < selectedSettings.length; i++) {
        const settingName = selectedSettings[i];
        console.log(
          `正在测试第 ${i + 1}/${
            selectedSettings.length
          } 个配置项: ${settingName}`
        );
        // 更新当前测试状态
        this.testingProgress = i + 1;
        this.currentTestingSetting = settingName;
        try {
          const test_result = await start_test(
            bmc_ip,
            bmc_username,
            bmc_password,
            [settingName],
            is_before
          );
          if (test_result.success) {
            // 记录成功日志
            this.addLog(`└── ${settingName}：配置测试成功`);
            // 处理返回的截图数据
            if (
              test_result.screenshots &&
              test_result.screenshots_name &&
              test_result.screenshots.length > 0
            ) {
              this.processScreenshots(
                test_result.screenshots,
                test_result.screenshots_name,
                "before"
              );
            }
          } else {
            // 记录失败日志
            this.addLog(
              `└── ${settingName}：配置测试失败 - ${
                test_result.message || "未知错误"
              }`
            );
          }
        } catch (error) {
          // 记录异常日志
          this.addLog(`└── ${settingName}: 发生错误 - ${error.message}`);
        }
      }
      // 测试完成后清除状态
      this.currentTestingSetting = "";
      this.testingProgress = 0;
      this.totalTesting = 0;
      this.isTesting = false;
      // 在此设置按钮可以点击
      this.beforeTestingClick = true;
    },

    async afterRefreshTest() {
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

      console.log("开始刷新后测试以下配置项:", selectedSettings);
      const userInfo = localStorage.getItem("user_info");
      const user = JSON.parse(userInfo);
      const bmc_ip = user.bmc_ip;
      const bmc_username = user.bmc_username;
      const bmc_password = user.bmc_password;
      const is_before = false;
      this.afterTestingClick = false;
      // 先清空之前的截图
      this.clearAfterScreenshots();

      // 设置测试状态
      this.isAfterTesting = true;
      this.afterTotalTesting = selectedSettings.length;
      this.afterTestingProgress = 0;
      this.currentAfterTestingSetting = "";
      // 添加开始测试日志
      this.addLog(
        `├── 开始刷新后测试，共选择 ${selectedSettings.length} 个配置项：${selectedSettings}`
      );

      // 一个一个测
      for (let i = 0; i < selectedSettings.length; i++) {
        const settingName = selectedSettings[i];
        console.log(
          `正在测试第 ${i + 1}/${
            selectedSettings.length
          } 个配置项: ${settingName}`
        );
        // 更新当前测试状态
        this.afterTestingProgress = i + 1;
        this.currentAfterTestingSetting = settingName;
        try {
          const test_result = await start_test(
            bmc_ip,
            bmc_username,
            bmc_password,
            [settingName],
            is_before
          );
          if (test_result.success) {
            // 记录成功日志
            this.addLog(`└── ${settingName}：刷新后配置测试成功`);
            // 处理返回的截图数据
            if (
              test_result.screenshots &&
              test_result.screenshots_name &&
              test_result.screenshots.length > 0
            ) {
              this.processScreenshots(
                test_result.screenshots,
                test_result.screenshots_name,
                "after"
              );
            }
          } else {
            // 记录失败日志
            this.addLog(
              `└── ${settingName}：刷新后配置测试失败 - ${
                test_result.message || "未知错误"
              }`
            );
          }
        } catch (error) {
          // 记录异常日志
          this.addLog(`└── ${settingName}: 发生错误 - ${error.message}`);
        }
      }
      // 测试完成后清除状态
      this.currentAfterTestingSetting = "";
      this.afterTestingProgress = 0;
      this.afterTotalTesting = 0;
      this.isAfterTesting = false;
      // 在此设置刷新后测试按钮可以点击
      this.afterTestingClick = true;
    },

    // 通用处理截图数据
    processScreenshots(screenshotData, screenshotName, type) {
      const targetArray =
        type === "before" ? this.beforeScreenshots : this.afterScreenshots;

      screenshotData.forEach((screenshot, index) => {
        let imageUrl;
        let imageName = screenshotName[index];

        if (typeof screenshot === "string") {
          // 如果是base64字符串
          if (screenshot.startsWith("data:image")) {
            imageUrl = screenshot;
          } else {
            imageUrl = `data:image/png;base64,${screenshot}`;
          }
        } else if (screenshot.url) {
          // 如果返回的是对象
          imageUrl = screenshot.url;
          imageName = screenshot.name || imageName;
        }

        if (imageUrl) {
          targetArray.push({
            name: imageName,
            url: imageUrl,
            type: "image/png",
            size: 0,
            selected: false, // 添加选中状态
          });
        }
      });
    },

    onImageLoad(event) {
      // 图片加载完成后的处理
      event.target.classList.add("loaded");
    },

    removeBeforeScreenshot(index) {
      // 释放URL对象
      if (this.beforeScreenshots[index].url) {
        URL.revokeObjectURL(this.beforeScreenshots[index].url);
      }
      this.beforeScreenshots.splice(index, 1);

      ElNotification({
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

      ElNotification({
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

      ElNotification({
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

      ElNotification({
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
  margin-bottom: 30px;
}

.action-buttons-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.action-test-btn {
  display: flex;
  align-items: center;
  justify-content: center; /* 垂直居中 */
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

.refresh-pre-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;

  &:hover:not(.disabled) {
    background: linear-gradient(135deg, #059669 0%, #047857 100%);
    box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
  }

  &.testing {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  }
}

.refresh-firmware-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;

  &:hover:not(.disabled) {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
  }
}

.refresh-post-btn {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;

  &:hover:not(.disabled) {
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
    box-shadow: 0 8px 20px rgba(139, 92, 246, 0.3);
  }

  &.testing {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  }
}

.test-icon {
  font-size: 15px;
}

.test-text {
  font-size: 14px;
  font-weight: 600;
}

.test-subtext {
  font-size: 14px;
  opacity: 0.9;
  font-weight: 500;
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
  padding: 16px 20px;
  background: linear-gradient(90deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid #e2e8f0;
  min-height: 24px;
}

.panel-title-area {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  flex: 1;
}

.panel-title {
  margin: 0;
  font-size: 16px;
  color: #1e293b;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  line-height: 1.4;
}

.panel-title-icon {
  font-size: 18px;
}

.screenshot-count {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 13px;
  color: #64748b;

  .total-count {
    background: #f1f5f9;
    padding: 3px 10px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
  }

  .selected-count {
    display: flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%);
    padding: 3px 10px;
    border-radius: 12px;
    border: 1px solid #93c5fd;
    color: #3b82f6;
    font-weight: 500;

    .selected-dot {
      width: 8px;
      height: 8px;
      background: #3b82f6;
      border-radius: 50%;
    }
  }
}

.panel-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;

  .batch-controls-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;

    .batch-controls {
      display: flex;
      align-items: center;
      gap: 8px;
      background: #f8fafc;
      padding: 6px;
      border-radius: 10px;
      border: 1px solid #e2e8f0;
    }
  }
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  background: white;
  color: #475569;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  height: 32px;
  min-width: 60px;

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
    box-shadow: none !important;
  }
}

.add-btn {
  background: #f0f9ff;
  border-color: #7dd3fc;
  color: #0369a1;

  &:hover:not(:disabled) {
    background: #e0f2fe;
    border-color: #38bdf8;
  }
}

.clear-btn {
  background: #fef2f2;
  border-color: #fecaca;
  color: #dc2626;

  &:hover:not(:disabled) {
    background: #fee2e2;
    border-color: #fca5a5;
  }
}

.select-all-btn {
  background: #f0f9ff;
  border-color: #7dd3fc;
  color: #0369a1;
  min-width: 50px;

  &:hover:not(:disabled) {
    background: #e0f2fe;
    border-color: #38bdf8;
  }
}

.deselect-all-btn {
  background: #fef2f2;
  border-color: #fecaca;
  color: #dc2626;
  min-width: 50px;

  &:hover:not(:disabled) {
    background: #fee2e2;
    border-color: #fca5a5;
  }
}

.download-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  min-width: 60px;

  &:hover:not(:disabled) {
    background: linear-gradient(135deg, #059669 0%, #047857 100%);
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
  }

  &:disabled {
    background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
  }
}

.screenshot-container {
  flex: 1;
  padding: 20px;
  background: #fafafa;
  overflow: hidden;
}

/* 修改：简化空状态样式 */
.empty-screenshot-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #94a3b8;
  border: 2px dashed #cbd5e1;
  border-radius: 10px;
  padding: 30px;
  text-align: center;
}

.placeholder-icon {
  font-size: 48px;
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
  transition: all 0.2s ease;
  cursor: pointer;
  position: relative;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
  }

  &.selected {
    box-shadow: 0 0 0 3px #3b82f6;

    .screenshot-wrapper::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(59, 130, 246, 0.1);
      z-index: 1;
    }
  }
}

.screenshot-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  background: #f8fafc;
}

/* 新增：选中指示器 */
.selection-indicator {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 24px;
  height: 24px;
  background: #3b82f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);

  .checkmark {
    color: white;
    font-size: 14px;
    font-weight: bold;
  }
}

.screenshot-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #f8fafc;
  transition: opacity 0.3s ease;
  position: relative;
  z-index: 2;
  cursor: pointer;

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
  z-index: 5;

  .screenshot-item:hover & {
    opacity: 1;
  }

  .overlay-left,
  .overlay-right {
    display: flex;
    align-items: center;
    gap: 8px;
  }
}

/* 新增：放大查看按钮 */
.preview-btn {
  background: rgba(59, 130, 246, 0.9);
  color: white;
  border: none;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;

  &:hover {
    background: #2563eb;
    transform: scale(1.1);
  }
}

.preview-icon {
  display: inline-block;
  transform: scale(0.9);
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
  z-index: 5;
}

/* 图片预览模态框样式 */
.image-preview-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

.preview-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: slideUp 0.3s ease;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(90deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid #e2e8f0;
}

.preview-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
  margin-right: 20px;
}

.close-preview-btn {
  background: transparent;
  border: none;
  color: #64748b;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 20px;
  transition: all 0.2s ease;

  &:hover {
    background: #f1f5f9;
    color: #475569;
  }
}

.preview-body {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.image-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: #f8fafc;
  border-radius: 8px;
  margin-bottom: 20px;
  position: relative;
  min-height: 300px;
}

.preview-image {
  max-width: 100%;
  max-height: 60vh;
  object-fit: contain;
}

.preview-navigation {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.nav-btn {
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  color: #475569;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.2s ease;

  &:hover:not(:disabled) {
    background: #3b82f6;
    border-color: #3b82f6;
    color: white;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.preview-counter {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
  min-width: 80px;
  text-align: center;
}

.preview-actions {
  display: flex;
  justify-content: center;
  gap: 12px;

  .action-btn {
    min-width: 120px;
    height: 40px;
    font-size: 14px;
  }

  .download-btn {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    border: none;

    &:hover {
      background: linear-gradient(135deg, #059669 0%, #047857 100%);
    }
  }

  .cancel-btn {
    background: #f1f5f9;
    border-color: #cbd5e1;
    color: #475569;

    &:hover {
      background: #e2e8f0;
    }
  }
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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

  .panel-actions {
    flex-wrap: wrap;

    .batch-controls {
      width: 100%;
      justify-content: flex-end;
      margin-right: 0;
      padding-right: 0;
      border-right: none;
      border-bottom: 1px solid #e2e8f0;
      padding-bottom: 10px;
      margin-bottom: 10px;
    }
  }

  .preview-content {
    width: 95%;
    max-height: 85vh;
  }
}

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

  .panel-header {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }

  .panel-actions {
    width: 100%;
    justify-content: flex-end;

    .batch-controls-wrapper {
      width: 100%;
      justify-content: space-between;

      .batch-controls {
        flex: 1;
        justify-content: flex-start;
      }
    }
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
    gap: 12px;
  }

  .screenshot-count {
    flex-wrap: wrap;
    gap: 8px;
  }

  .action-btn {
    padding: 6px 10px;
    font-size: 12px;
    min-width: 50px;

    .action-text {
      font-size: 12px;
    }
  }

  .preview-content {
    width: 98%;
    max-height: 80vh;
  }

  .preview-actions {
    flex-direction: column;

    .action-btn {
      width: 100%;
    }
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
    width: 100%;
  }

  .panel-actions {
    width: 100%;

    .batch-controls-wrapper {
      flex-direction: column;
      width: 100%;
      gap: 8px;

      .batch-controls {
        width: 100%;
        justify-content: space-between;
      }

      .clear-btn {
        width: 100%;
      }
    }
  }

  .action-btn {
    flex: 1;
    min-width: auto;
  }

  .preview-navigation {
    gap: 10px;

    .nav-btn {
      width: 36px;
      height: 36px;
    }
  }

  .logs-panel {
    height: 250px;
  }

  .log-item {
    font-size: 12px;
    gap: 6px;
    padding: 2px 0;
  }

  .log-time {
    font-size: 12px;
    min-width: 75px;
  }
}

/* 测试日志区域样式 */
.test-logs-section {
  margin-bottom: 24px;
}

.logs-panel {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  height: 300px;
}

.logs-container {
  flex: 1;
  background: #f8fafc;
  overflow: hidden;
  position: relative; /* 确保滚动区域定位正确 */
}

.logs-content {
  height: 100%;
  overflow-y: auto;
  padding: 10px 15px 15px 15px; /* 调整内边距，底部增加一些空间 */
  box-sizing: border-box; /* 确保内边距包含在高度内（不会被截断！！！） */
}

.log-item {
  display: flex;
  align-items: flex-start;
  gap: 8px; /* 减小间隙 */
  padding: 3px 0; /* 减小上下内边距 */
  border-bottom: 1px solid #f1f5f9;
  font-size: 13px;
  line-height: 1.3; /* 减小行高 */
  margin-bottom: 1px; /* 添加微小底部间距 */
}

.log-time {
  color: #64748b;
  font-family: monospace;
  font-size: 14px; /* 稍微减小字体 */
  min-width: 100px; /* 调整为带年月日的宽度 */
  padding-top: 1px; /* 减小顶部内边距 */
  flex-shrink: 0; /* 防止时间被压缩 */
  margin-right: 15px;
}

.log-message {
  color: #334155;
  flex: 1;
  word-break: break-word;
  padding: 1px 0; /* 添加微小内边距 */
}
</style>
