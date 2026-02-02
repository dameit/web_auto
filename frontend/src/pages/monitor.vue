<template>
  <div class="health-monitoring">
    <!-- 顶部IP信息和系统状态 -->
    <div class="top-info-section">
      <div class="top-info-container">
        <!-- IP信息 -->
        <div class="ip-info-row">
          <div class="ip-display">
            <span class="ip-label">OS IP:</span>
            <span class="ip-value">{{ osIp }}</span>
          </div>
          <div class="system-status-display">
            <div class="status-indicator" :class="systemStatus"></div>
            <span class="status-label">系统状态:</span>
            <span class="status-value">{{ getStatusText(systemStatus) }}</span>
          </div>
        </div>

        <!-- 刷新控制 -->
        <div class="control-row">
          <div class="refresh-controls">
            <button
              @click="toggleAutoRefresh"
              class="control-btn auto-refresh-btn"
              :class="{ active: autoRefresh }"
            >
              <span class="control-icon">{{ autoRefresh ? "⏸️" : "▶️" }}</span>
              <span class="control-text">{{
                autoRefresh ? "自动刷新中" : "自动刷新"
              }}</span>
            </button>
            <button @click="manualRefresh" class="control-btn refresh-btn">
              <span class="control-icon">🔄</span>
              <span class="control-text">立即刷新</span>
            </button>
            <div class="refresh-interval-selector">
              <label for="interval">刷新间隔:</label>
              <select
                id="interval"
                v-model="refreshInterval"
                class="interval-select"
              >
                <option value="5">5秒</option>
                <option value="10">10秒</option>
                <option value="30">30秒</option>
                <option value="60">60秒</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 核心健康指标卡片 -->
    <div class="health-metrics-section">
      <div class="metrics-grid">
        <!-- CPU使用率卡片 -->
        <div class="metric-card cpu-card">
          <div class="card-header">
            <div class="card-title">
              <span class="card-icon">⚡</span>
              <h3 class="card-title-text">CPU使用率</h3>
            </div>
            <div class="card-actions">
              <span class="last-update"
                >更新: {{ formatTime(cpuMetrics.lastUpdate) }}</span
              >
            </div>
          </div>
          <div class="card-body">
            <div class="metric-display">
              <div class="gauge-container">
                <div class="gauge-chart" ref="cpuGauge"></div>
                <div class="gauge-value">
                  <span class="value-label">当前使用率</span>
                </div>
              </div>
              <div class="metric-details">
                <div class="detail-item">
                  <span class="detail-label">核心数:</span>
                  <span class="detail-value">{{ cpuMetrics.cores }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">频率:</span>
                  <span class="detail-value">{{ cpuMetrics.frequency }}MHz</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">型号:</span>
                  <span class="detail-value">{{ cpuMetrics.model }}</span>
                </div>
              </div>
            </div>
            <div class="trend-chart" ref="cpuTrend"></div>
          </div>
          <div class="card-footer">
            <div
              class="trend-indicator"
              :class="getTrendClass(cpuMetrics.trend)"
            >
              <span class="trend-icon">{{
                getTrendIcon(cpuMetrics.trend)
              }}</span>
              <span class="trend-text">{{
                getTrendText(cpuMetrics.trend)
              }}</span>
            </div>
            <div class="threshold-info">
              <span class="threshold-label">警告阈值:</span>
              <span class="threshold-value"
                >{{ cpuMetrics.warningThreshold }}%</span
              >
            </div>
          </div>
        </div>

        <!-- 内存使用率卡片 -->
        <div class="metric-card memory-card">
          <div class="card-header">
            <div class="card-title">
              <span class="card-icon">🧠</span>
              <h3 class="card-title-text">内存使用率</h3>
            </div>
            <div class="card-actions">
              <span class="last-update"
                >更新: {{ formatTime(memoryMetrics.lastUpdate) }}</span
              >
            </div>
          </div>
          <div class="card-body">
            <div class="metric-display">
              <div class="gauge-container">
                <div class="gauge-chart" ref="memoryGauge"></div>
              </div>
              <div class="metric-details">
                <div class="detail-item">
                  <span class="detail-label">总内存:</span>
                  <span class="detail-value">{{
                    memoryMetrics.total
                  }}GB</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">已使用:</span>
                  <span class="detail-value">{{
                    memoryMetrics.used
                  }}GB</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">可用:</span>
                  <span class="detail-value">{{
                    memoryMetrics.available
                  }}GB</span>
                </div>
              </div>
            </div>
            <div class="trend-chart" ref="memoryTrend"></div>
          </div>
          <div class="card-footer">
            <div
              class="trend-indicator"
              :class="getTrendClass(memoryMetrics.trend)"
            >
              <span class="trend-icon">{{
                getTrendIcon(memoryMetrics.trend)
              }}</span>
              <span class="trend-text">{{
                getTrendText(memoryMetrics.trend)
              }}</span>
            </div>
            <div class="threshold-info">
              <span class="threshold-label">警告阈值:</span>
              <span class="threshold-value"
                >{{ memoryMetrics.warningThreshold }}%</span
              >
            </div>
          </div>
        </div>

        <!-- 硬盘使用率卡片 -->
        <div class="metric-card disk-card">
          <div class="card-header">
            <div class="card-title">
              <span class="card-icon">💾</span>
              <h3 class="card-title-text">硬盘使用率</h3>
            </div>
            <div class="card-actions">
              <span class="last-update"
                >更新: {{ formatTime(diskMetrics.lastUpdate) }}</span
              >
            </div>
          </div>
          <div class="card-body">
            <div class="metric-display">
              <div class="gauge-container">
                <div class="gauge-chart" ref="diskGauge"></div>
                <div class="gauge-value">
                  <span class="value-number">{{ diskMetrics.current }}%</span>
                  <span class="value-label">当前使用率</span>
                </div>
              </div>
              <div class="metric-details">
                <div class="detail-item">
                  <span class="detail-label">总空间:</span>
                  <span class="detail-value">{{ diskMetrics.total }}GB</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">已使用:</span>
                  <span class="detail-value">{{ diskMetrics.used }}GB</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">可用:</span>
                  <span class="detail-value">{{ diskMetrics.free }}GB</span>
                </div>
              </div>
            </div>
            <div class="trend-chart" ref="diskTrend"></div>
          </div>
          <div class="card-footer">
            <div
              class="trend-indicator"
              :class="getTrendClass(diskMetrics.trend)"
            >
              <span class="trend-icon">{{
                getTrendIcon(diskMetrics.trend)
              }}</span>
              <span class="trend-text">{{
                getTrendText(diskMetrics.trend)
              }}</span>
            </div>
            <div class="threshold-info">
              <span class="threshold-label">警告阈值:</span>
              <span class="threshold-value"
                >{{ diskMetrics.warningThreshold }}%</span
              >
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 网络和系统信息 -->
    <div class="system-info-section">
      <div class="info-grid">
        <!-- 网络监控 -->
        <div class="info-card network-card">
          <div class="card-header">
            <div class="card-title">
              <span class="card-icon">🌐</span>
              <h3 class="card-title-text">网络监控</h3>
            </div>
          </div>
          <div class="card-body">
            <div class="network-stats">
              <div class="network-stat">
                <span class="stat-label">上传速度:</span>
                <span class="stat-value">{{ networkMetrics.uploadSpeed }}</span>
              </div>
              <div class="network-stat">
                <span class="stat-label">下载速度:</span>
                <span class="stat-value">{{
                  networkMetrics.downloadSpeed
                }}</span>
              </div>
              <div class="network-stat">
                <span class="stat-label">连接数:</span>
                <span class="stat-value">{{ networkMetrics.connections }}</span>
              </div>
              <div class="network-stat">
                <span class="stat-label">延迟:</span>
                <span class="stat-value">{{ networkMetrics.latency }}ms</span>
              </div>
            </div>
            <div class="network-chart" ref="networkChart"></div>
          </div>
        </div>

        <!-- 系统负载 -->
        <div class="info-card load-card">
          <div class="card-header">
            <div class="card-title">
              <span class="card-icon">📊</span>
              <h3 class="card-title-text">系统负载</h3>
            </div>
          </div>
          <div class="card-body">
            <div class="load-indicators">
              <div class="load-indicator">
                <div class="load-label">1分钟:</div>
                <div class="load-bar">
                  <div
                    class="load-fill"
                    :style="{ width: loadMetrics.load1 + '%' }"
                  ></div>
                  <span class="load-value">{{
                    loadMetrics.load1.toFixed(2)
                  }}</span>
                </div>
              </div>
              <div class="load-indicator">
                <div class="load-label">5分钟:</div>
                <div class="load-bar">
                  <div
                    class="load-fill"
                    :style="{ width: loadMetrics.load5 + '%' }"
                  ></div>
                  <span class="load-value">{{
                    loadMetrics.load5.toFixed(2)
                  }}</span>
                </div>
              </div>
              <div class="load-indicator">
                <div class="load-label">15分钟:</div>
                <div class="load-bar">
                  <div
                    class="load-fill"
                    :style="{ width: loadMetrics.load15 + '%' }"
                  ></div>
                  <span class="load-value">{{
                    loadMetrics.load15.toFixed(2)
                  }}</span>
                </div>
              </div>
            </div>
            <div class="load-chart" ref="loadChart"></div>
          </div>
        </div>

        <!-- 进程监控 -->
        <div class="info-card processes-card">
          <div class="card-header">
            <div class="card-title">
              <span class="card-icon">📈</span>
              <h3 class="card-title-text">进程监控</h3>
            </div>
          </div>
          <div class="card-body">
            <div class="processes-list">
              <div
                class="process-item"
                v-for="(process, index) in processes"
                :key="index"
              >
                <div class="process-name">{{ process.name }}</div>
                <div class="process-cpu">{{ process.cpu }}%</div>
                <div class="process-memory">{{ process.memory }}%</div>
                <div class="process-status" :class="process.status"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 警报历史 -->
    <div class="alerts-section" v-if="alerts.length > 0">
      <div class="section-header">
        <div class="section-title-area">
          <h3 class="section-title">
            <span class="section-title-icon">🚨</span>
            系统警报
          </h3>
          <div class="alerts-count">
            <span class="count-number">{{ alerts.length }}</span>
            <span class="count-label">个未处理警报</span>
          </div>
        </div>
        <div class="section-actions">
          <button @click="clearAlerts" class="action-btn clear-btn">
            <span class="action-icon">🗑️</span>
            清空警报
          </button>
        </div>
      </div>
      <div class="alerts-list">
        <div
          v-for="alert in alerts"
          :key="alert.id"
          class="alert-item"
          :class="alert.level"
        >
          <div class="alert-icon">
            <span v-if="alert.level === 'critical'">🔴</span>
            <span v-else-if="alert.level === 'warning'">🟡</span>
            <span v-else>🔵</span>
          </div>
          <div class="alert-content">
            <div class="alert-title">{{ alert.title }}</div>
            <div class="alert-message">{{ alert.message }}</div>
          </div>
          <div class="alert-time">{{ formatRelativeTime(alert.time) }}</div>
          <button @click="dismissAlert(alert.id)" class="alert-dismiss">
            ×
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// 推荐安装 ECharts 5.x + echarts-liquidfill 3.x（最稳定）:
// npm install echarts@5.4.3 echarts-liquidfill@3.1.0 --save
import * as echarts from "echarts";
import "echarts-liquidfill";
import { monitor_update } from "@/api"

export default {
  name: "HealthMonitoring",
  data() {
    const userInfo = localStorage.getItem("user_info");
    const user = JSON.parse(userInfo) || {};
    return {
      bmcIp: user.bmc_ip || "未配置",
      osIp: user.os_ip || "未配置",
      systemStatus: "healthy",
      autoRefresh: true,
      refreshInterval: 10,
      refreshTimer: null,

      // CPU指标数据
      cpuMetrics: {
        current: null,
        trend: "stable",
        cores: null,
        frequency: null,
        model: null,
        warningThreshold: 80,
        history: [],
        lastUpdate: new Date(),
      },

      // 内存指标数据
      memoryMetrics: {
        current: null,
        trend: "rising",
        total: null,
        used: null,
        available: null,
        warningThreshold: 85,
        history: [],
        lastUpdate: new Date(),
      },

      // 硬盘指标数据
      diskMetrics: {
        current: null,
        trend: "stable",
        total: null,
        used: null,
        free: null,
        warningThreshold: 90,
        history: [],
        lastUpdate: new Date(),
      },

      // 网络指标数据
      networkMetrics: {
        uploadSpeed: "2.4 Mbps",
        downloadSpeed: "15.6 Mbps",
        connections: 42,
        latency: 24,
        history: [],
      },

      // 系统负载数据
      loadMetrics: {
        load1: 1.2,
        load5: 1.8,
        load15: 1.5,
        history: [],
      },

      // 进程列表
      processes: [
        { name: "nginx", cpu: 12.4, memory: 8.2, status: "running" },
        { name: "mysql", cpu: 5.6, memory: 15.3, status: "running" },
        { name: "node", cpu: 8.9, memory: 6.7, status: "running" },
        { name: "python", cpu: 3.2, memory: 4.8, status: "running" },
        { name: "docker", cpu: 2.1, memory: 3.4, status: "running" },
      ],

      // 警报列表
      alerts: [
        {
          id: 1,
          level: "warning",
          title: "内存使用率偏高",
          message: "当前内存使用率已达 67.8%",
          time: new Date(Date.now() - 15 * 60000),
        },
        {
          id: 2,
          level: "info",
          title: "系统运行正常",
          message: "所有指标均在正常范围内",
          time: new Date(Date.now() - 30 * 60000),
        },
      ],

      // ECharts实例
      charts: {},
    };
  },

  computed: {
    statusColors() {
      return {
        healthy: "#10B981",
        warning: "#F59E0B",
        critical: "#EF4444",
        offline: "#6B7280",
      };
    },
  },

  mounted() {
    this.initCharts();
    this.startAutoRefresh();
    this.generateHistoryData();
  },

  beforeDestroy() {
    this.stopAutoRefresh();
    Object.values(this.charts).forEach((chart) => {
      if (chart) chart.dispose();
    });
  },

  methods: {
    // 初始化所有图表
    initCharts() {
      // CPU仪表图
      this.charts.cpuGauge = echarts.init(this.$refs.cpuGauge);
      this.updateCpuGauge();

      // CPU趋势图
      this.charts.cpuTrend = echarts.init(this.$refs.cpuTrend);
      this.updateCpuTrend();

      // 内存仪表图
      this.charts.memoryGauge = echarts.init(this.$refs.memoryGauge);
      this.updateMemoryGauge();

      // 内存趋势图
      this.charts.memoryTrend = echarts.init(this.$refs.memoryTrend);
      this.updateMemoryTrend();

      // 硬盘仪表图
      this.charts.diskGauge = echarts.init(this.$refs.diskGauge);
      this.updateDiskGauge();

      // 硬盘趋势图
      this.charts.diskTrend = echarts.init(this.$refs.diskTrend);
      this.updateDiskTrend();

      // 网络图表
      this.charts.network = echarts.init(this.$refs.networkChart);
      this.updateNetworkChart();

      // 负载图表
      this.charts.load = echarts.init(this.$refs.loadChart);
      this.updateLoadChart();
    },

    // 更新CPU仪表图
    updateCpuGauge() {
      const option = {
        series: [
          {
            type: "gauge",
            center: ["50%", "60%"],
            radius: "90%",
            startAngle: 180,
            endAngle: 0,
            min: 0,
            max: 100,
            splitNumber: 10,
            itemStyle: {
              color: this.getGaugeColor(
                this.cpuMetrics.current,
                this.cpuMetrics.warningThreshold
              ),
            },
            progress: {
              show: true,
              width: 20,
            },
            pointer: {
              show: false,
            },
            axisLine: {
              lineStyle: {
                width: 20,
              },
            },
            axisTick: {
              distance: -25,
              splitNumber: 5,
              lineStyle: {
                width: 2,
                color: "#999",
              },
            },
            splitLine: {
              distance: -30,
              length: 10,
              lineStyle: {
                width: 3,
                color: "#999",
              },
            },
            axisLabel: {
              distance: -20,
              color: "#999",
              fontSize: 12,
            },
            anchor: {
              show: false,
            },
            title: {
              show: false,
            },
            detail: {
              valueAnimation: true,
              fontSize: 30,
              offsetCenter: [0, "70%"],
            },
            data: [
              {
                value: this.cpuMetrics.current,
                name: "CPU使用率",
              },
            ],
          },
        ],
      };
      this.charts.cpuGauge.setOption(option);
    },

    // 更新CPU趋势图
    updateCpuTrend() {
      const data =
        this.cpuMetrics.history.length > 0
          ? this.cpuMetrics.history.map((h) => h.value)
          : this.generateMockHistory(20, 30, 60);

      const option = {
        tooltip: {
          trigger: "axis",
        },
        grid: {
          left: "5%",
          right: "5%",
          bottom: "10%",
          top: "10%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          show: false,
          boundaryGap: false,
        },
        yAxis: {
          type: "value",
          show: false,
          max: 100,
        },
        series: [
          {
            data: data,
            type: "line",
            smooth: true,
            lineStyle: {
              width: 2,
              color: "#3B82F6",
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: "rgba(59, 130, 246, 0.5)" },
                { offset: 1, color: "rgba(59, 130, 246, 0.1)" },
              ]),
            },
            symbol: "none",
          },
        ],
      };
      this.charts.cpuTrend.setOption(option);
    },

    // 更新内存仪表图
    updateMemoryGauge() {
      const option = {
        series: [
          {
            type: "liquidFill",
            data: [this.memoryMetrics.current / 100],
            radius: "80%",
            center: ["50%", "50%"],
            backgroundStyle: {
              color: "#EFF6FF",
            },
            outline: {
              show: false,
            },
            color: [
              this.getGaugeColor(
                this.memoryMetrics.current,
                this.memoryMetrics.warningThreshold
              ),
            ],
            label: {
              formatter: (value) => {
                return `${(value.data * 100).toFixed(1)}%`;
              },
              fontSize: 24,
              color: "#1E293B",
            },
          },
        ],
      };
      this.charts.memoryGauge.setOption(option);
    },

    // 更新内存趋势图
    updateMemoryTrend() {
      const option = {
        tooltip: {
          trigger: "axis",
        },
        grid: {
          left: "5%",
          right: "5%",
          bottom: "10%",
          top: "10%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          show: false,
          boundaryGap: false,
        },
        yAxis: {
          type: "value",
          show: false,
          max: 100,
        },
        series: [
          {
            type: "line",
            smooth: true,
            lineStyle: {
              width: 2,
              color: "#10B981",
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: "rgba(16, 185, 129, 0.5)" },
                { offset: 1, color: "rgba(16, 185, 129, 0.1)" },
              ]),
            },
            symbol: "none",
          },
        ],
      };
      this.charts.memoryTrend.setOption(option);
    },

    // 更新硬盘仪表图
    updateDiskGauge() {
      const option = {
        series: [
          {
            type: "pie",
            radius: ["60%", "80%"],
            center: ["50%", "50%"],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: "#fff",
              borderWidth: 2,
            },
            label: {
              show: false,
            },
            emphasis: {
              label: {
                show: false,
              },
            },
            data: [
              {
                value: this.diskMetrics.current,
                name: "已使用",
                itemStyle: {
                  color: this.getGaugeColor(
                    this.diskMetrics.current,
                    this.diskMetrics.warningThreshold
                  ),
                },
              },
              {
                value: 100 - this.diskMetrics.current,
                name: "未使用",
                itemStyle: { color: "#E2E8F0" },
              },
            ],
          },
        ],
      };
      this.charts.diskGauge.setOption(option);
    },

    // 更新硬盘趋势图
    updateDiskTrend() {
      const option = {
        tooltip: {
          trigger: "axis",
        },
        grid: {
          left: "5%",
          right: "5%",
          bottom: "10%",
          top: "10%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          show: false,
          boundaryGap: false,
        },
        yAxis: {
          type: "value",
          show: false,
          max: 100,
        },
        series: [
          {
            type: "line",
            smooth: true,
            lineStyle: {
              width: 2,
              color: "#8B5CF6",
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: "rgba(139, 92, 246, 0.5)" },
                { offset: 1, color: "rgba(139, 92, 246, 0.1)" },
              ]),
            },
            symbol: "none",
          },
        ],
      };
      this.charts.diskTrend.setOption(option);
    },

    // 更新网络图表
    updateNetworkChart() {
      const option = {
        tooltip: {
          trigger: "axis",
        },
        legend: {
          show: false,
        },
        grid: {
          left: "3%",
          right: "3%",
          bottom: "3%",
          top: "3%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          show: false,
          boundaryGap: false,
        },
        yAxis: {
          type: "value",
          show: false,
        },
        series: [
          {
            name: "上传",
            type: "line",
            smooth: true,
            lineStyle: {
              width: 2,
              color: "#3B82F6",
            },
            symbol: "none",
          },
          {
            name: "下载",
            type: "line",
            smooth: true,
            lineStyle: {
              width: 2,
              color: "#10B981",
            },
            symbol: "none",
          },
        ],
      };
      this.charts.network.setOption(option);
    },

    // 更新负载图表
    updateLoadChart() {
      const option = {
        tooltip: {
          trigger: "axis",
        },
        grid: {
          left: "3%",
          right: "3%",
          bottom: "3%",
          top: "3%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          show: false,
          boundaryGap: false,
        },
        yAxis: {
          type: "value",
          show: false,
        },
        series: [
          {
            name: "1分钟",
            type: "line",
            smooth: true,
            lineStyle: {
              width: 2,
              color: "#F59E0B",
            },
            symbol: "none",
          },
          {
            name: "5分钟",
            type: "line",
            smooth: true,
            lineStyle: {
              width: 2,
              color: "#8B5CF6",
            },
            symbol: "none",
          },
          {
            name: "15分钟",
            type: "line",
            smooth: true,
            lineStyle: {
              width: 2,
              color: "#EF4444",
            },
            symbol: "none",
          },
        ],
      };
      this.charts.load.setOption(option);
    },

    // 获取仪表盘颜色
    getGaugeColor(value, threshold) {
      if (value >= threshold) return "#EF4444";
      if (value >= threshold * 0.7) return "#F59E0B";
      return "#10B981";
    },

    // 生成历史数据
    generateHistoryData() {
      // 生成CPU历史数据
      this.cpuMetrics.history = this.generateMockHistory(20, 30, 60);

      // 生成内存历史数据
      this.memoryMetrics.history = this.generateMockHistory(20, 50, 70);

      // 生成硬盘历史数据
      this.diskMetrics.history = this.generateMockHistory(20, 40, 55);
    },

    // 生成模拟历史数据
    generateMockHistory(count, min, max) {
      const data = [];
      const now = new Date();
      for (let i = count; i >= 0; i--) {
        const time = new Date(now.getTime() - i * 60000); // 每分钟一个点
        const value = min + Math.random() * (max - min);
        data.push({
          time: time,
          value: parseFloat(value.toFixed(1)),
        });
      }
      return data;
    },

    // 开始自动刷新
    startAutoRefresh() {
      if (this.refreshTimer) clearInterval(this.refreshTimer);
      this.refreshTimer = setInterval(() => {
        this.refreshMetrics();
      }, this.refreshInterval * 1000);
    },

    // 停止自动刷新
    stopAutoRefresh() {
      if (this.refreshTimer) {
        clearInterval(this.refreshTimer);
        this.refreshTimer = null;
      }
    },

    // 切换自动刷新
    toggleAutoRefresh() {
      this.autoRefresh = !this.autoRefresh;
      if (this.autoRefresh) {
        this.startAutoRefresh();
      } else {
        this.stopAutoRefresh();
      }
    },

    // 手动刷新
    manualRefresh() {
      this.refreshMetrics();
    },

    // 刷新所有指标
    async refreshMetrics() {
      const userInfo = localStorage.getItem("user_info");
      const user = JSON.parse(userInfo);
      const os_ip = user.os_ip;
      const os_username = user.os_username;
      const os_password = user.os_password;
      const all_monitor_data = await monitor_update(os_ip, os_username, os_password);
      const monitor_data = all_monitor_data['monitor_data']
      // 模拟数据更新
      this.updateCpuMetrics(monitor_data);
      this.updateMemoryMetrics(monitor_data);
      this.updateDiskMetrics(monitor_data);
      this.updateNetworkMetrics();
      this.updateLoadMetrics();
      this.updateProcesses();

      // 更新图表
      this.updateAllCharts();

      // 检查警报
      this.checkAlerts();
    },

    // 更新CPU指标
    updateCpuMetrics(monitor_data) {
      this.cpuMetrics.current = monitor_data["cpu_used"];
      this.cpuMetrics.model = monitor_data["cpu_model"];
      this.cpuMetrics.cores = monitor_data["cpu_cores"];
      this.cpuMetrics.frequency = monitor_data["cpu_frequency"];
      this.cpuMetrics.trend = this.calculateTrend(
        this.cpuMetrics.history,
        this.cpuMetrics.current
      );
      this.cpuMetrics.lastUpdate = new Date();

      // 更新历史数据
      this.cpuMetrics.history.push({
        time: new Date(),
        value: this.cpuMetrics.current,
      });
      if (this.cpuMetrics.history.length > 30) {
        this.cpuMetrics.history.shift();
      }
    },

    // 更新内存指标
    updateMemoryMetrics(monitor_data) {
      this.memoryMetrics.current = monitor_data["mem_used"];
      this,this.memoryMetrics.total = monitor_data["mem_total"];
      this.memoryMetrics.used = monitor_data["mem_isused"];
      this.memoryMetrics.available = monitor_data["mem_total"] - monitor_data["mem_isused"];
      this.memoryMetrics.trend = this.calculateTrend(
        this.memoryMetrics.history,
        this.memoryMetrics.current
      );
      this.memoryMetrics.lastUpdate = new Date();

      // 更新历史数据
      this.memoryMetrics.history.push({
        time: new Date(),
        value: this.memoryMetrics.current,
      });
      if (this.memoryMetrics.history.length > 30) {
        this.memoryMetrics.history.shift();
      }
    },

    // 更新硬盘指标
    updateDiskMetrics(monitor_data) {
      // 使用后端返回的实际数据
      this.diskMetrics.current = monitor_data["disk_used"];
      this.diskMetrics.total = monitor_data["disk_total"]
      this.diskMetrics.used = monitor_data["disk_isused"];
      this.diskMetrics.free = this.diskMetrics.total - this.diskMetrics.used;
      this.diskMetrics.trend = this.calculateTrend(
        this.diskMetrics.history,
        this.diskMetrics.current
      );
      this.diskMetrics.lastUpdate = new Date();

      // 更新历史数据
      this.diskMetrics.history.push({
        time: new Date(),
        value: this.diskMetrics.current,
      });
      if (this.diskMetrics.history.length > 30) {
        this.diskMetrics.history.shift();
      }
    },

    // 更新网络指标
    updateNetworkMetrics() {
      this.networkMetrics.uploadSpeed = `${(Math.random() * 5).toFixed(
        1
      )} Mbps`;
      this.networkMetrics.downloadSpeed = `${(10 + Math.random() * 10).toFixed(
        1
      )} Mbps`;
      this.networkMetrics.connections = 30 + Math.floor(Math.random() * 30);
      this.networkMetrics.latency = 10 + Math.floor(Math.random() * 40);
    },

    // 更新负载指标
    updateLoadMetrics() {
      this.loadMetrics.load1 = Math.random() * 3;
      this.loadMetrics.load5 = Math.random() * 2.5;
      this.loadMetrics.load15 = Math.random() * 2;
    },

    // 更新进程列表
    updateProcesses() {
      this.processes = this.processes.map((process) => ({
        ...process,
        cpu: Math.max(
          0,
          Math.min(100, process.cpu + (Math.random() - 0.5) * 5)
        ),
        memory: Math.max(
          0,
          Math.min(100, process.memory + (Math.random() - 0.5) * 3)
        ),
      }));
    },

    // 更新所有图表
    updateAllCharts() {
      this.updateCpuGauge();
      this.updateCpuTrend();
      this.updateMemoryGauge();
      this.updateMemoryTrend();
      this.updateDiskGauge();
      this.updateDiskTrend();
      this.updateNetworkChart();
      this.updateLoadChart();
    },

    // 计算趋势
    calculateTrend(history, currentValue) {
      if (history.length < 2) return "stable";
      const prevValue = history[history.length - 2].value;
      const diff = currentValue - prevValue;

      if (diff > 2) return "rising";
      if (diff < -2) return "falling";
      return "stable";
    },

    // 检查警报
    checkAlerts() {
      // 检查CPU警报
      if (this.cpuMetrics.current > this.cpuMetrics.warningThreshold) {
        this.addAlert(
          "warning",
          "CPU使用率过高",
          `当前CPU使用率已达 ${this.cpuMetrics.current.toFixed(1)}%`
        );
      }

      // 检查内存警报
      if (this.memoryMetrics.current > this.memoryMetrics.warningThreshold) {
        this.addAlert(
          "warning",
          "内存使用率过高",
          `当前内存使用率已达 ${this.memoryMetrics.current.toFixed(1)}%`
        );
      }

      // 检查硬盘警报
      if (this.diskMetrics.current > this.diskMetrics.warningThreshold) {
        this.addAlert(
          "warning",
          "硬盘空间不足",
          `当前硬盘使用率已达 ${this.diskMetrics.current.toFixed(1)}%`
        );
      }

      // 检查温度警报
      if (this.cpuMetrics.temperature > 80) {
        this.addAlert(
          "critical",
          "CPU温度过高",
          `当前CPU温度已达 ${this.cpuMetrics.temperature}°C`
        );
      }
    },

    // 添加警报
    addAlert(level, title, message) {
      // 检查是否已存在相同警报
      const exists = this.alerts.some(
        (alert) => alert.title === title && alert.message === message
      );

      if (!exists) {
        this.alerts.unshift({
          id: Date.now(),
          level,
          title,
          message,
          time: new Date(),
        });

        // 限制警报数量
        if (this.alerts.length > 20) {
          this.alerts.pop();
        }
      }
    },

    // 关闭警报
    dismissAlert(alertId) {
      this.alerts = this.alerts.filter((alert) => alert.id !== alertId);
    },

    // 清空警报
    clearAlerts() {
      this.alerts = [];
    },

    // 格式化时间
    formatTime(date) {
      if (!date) return "--:--:--";
      const d = new Date(date);
      const hours = d.getHours().toString().padStart(2, "0");
      const minutes = d.getMinutes().toString().padStart(2, "0");
      const seconds = d.getSeconds().toString().padStart(2, "0");
      return `${hours}:${minutes}:${seconds}`;
    },

    // 格式化相对时间
    formatRelativeTime(date) {
      const now = new Date();
      const diff = now - new Date(date);
      const minutes = Math.floor(diff / 60000);
      const hours = Math.floor(minutes / 60);

      if (minutes < 1) return "刚刚";
      if (minutes < 60) return `${minutes}分钟前`;
      if (hours < 24) return `${hours}小时前`;
      return `${Math.floor(hours / 24)}天前`;
    },

    // 格式化字节大小
    formatBytes(bytes) {
      if (bytes === 0) return "0 Bytes";
      const k = 1024;
      const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
    },

    // 获取状态文本
    getStatusText(status) {
      const statusMap = {
        healthy: "健康",
        warning: "警告",
        critical: "严重",
        offline: "离线",
      };
      return statusMap[status] || "未知";
    },

    // 获取趋势图标
    getTrendIcon(trend) {
      const trendMap = {
        rising: "📈",
        falling: "📉",
        stable: "➡️",
      };
      return trendMap[trend] || "➡️";
    },

    // 获取趋势文本
    getTrendText(trend) {
      const trendMap = {
        rising: "上升",
        falling: "下降",
        stable: "稳定",
      };
      return trendMap[trend] || "未知";
    },

    // 获取趋势类名
    getTrendClass(trend) {
      return `trend-${trend}`;
    },

    // 获取温度类名
    getTemperatureClass(temp) {
      if (temp > 80) return "temp-critical";
      if (temp > 70) return "temp-warning";
      return "temp-normal";
    },
  },

  watch: {
    refreshInterval(newVal) {
      if (this.autoRefresh) {
        this.startAutoRefresh();
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.health-monitoring {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  background-color: #f8fafc;
  min-height: 100vh;
}

/* 顶部信息区域样式 - 保持与测试页面一致 */
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

.system-status-display {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f1f5f9;
  padding: 10px 16px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  min-width: 200px;
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 6px;

  &.healthy {
    background-color: #10b981;
    box-shadow: 0 0 8px rgba(16, 185, 129, 0.5);
  }

  &.warning {
    background-color: #f59e0b;
    box-shadow: 0 0 8px rgba(245, 158, 11, 0.5);
  }

  &.critical {
    background-color: #ef4444;
    box-shadow: 0 0 8px rgba(239, 68, 68, 0.5);
  }

  &.offline {
    background-color: #6b7280;
    box-shadow: 0 0 8px rgba(107, 114, 128, 0.5);
  }
}

.status-label {
  font-weight: 600;
  color: #475569;
  font-size: 14px;
}

.status-value {
  color: #1e293b;
  font-weight: 500;
  font-size: 15px;
  margin-left: 6px;
}

.control-row {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
  justify-content: flex-end;
}

.refresh-controls {
  display: flex;
  align-items: center;
  gap: 16px;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: white;
  color: #475569;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: #f8fafc;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  &.auto-refresh-btn {
    &.active {
      background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
      color: white;
      border: none;
    }
  }

  &.refresh-btn {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    border: none;

    &:hover {
      background: linear-gradient(135deg, #059669 0%, #047857 100%);
    }
  }
}

.control-icon {
  font-size: 16px;
}

.control-text {
  white-space: nowrap;
}

.refresh-interval-selector {
  display: flex;
  align-items: center;
  gap: 8px;

  label {
    font-size: 14px;
    color: #64748b;
    font-weight: 500;
  }
}

.interval-select {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  background: white;
  color: #334155;
  font-size: 14px;
  min-width: 100px;

  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
}

/* 健康指标卡片区域 */
.health-metrics-section {
  margin-bottom: 24px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.metric-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  }

  &.cpu-card {
    border-top: 4px solid #3b82f6;
  }

  &.memory-card {
    border-top: 4px solid #10b981;
  }

  &.disk-card {
    border-top: 4px solid #8b5cf6;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(90deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid #e2e8f0;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.card-icon {
  font-size: 20px;
}

.card-title-text {
  margin: 0;
  font-size: 16px;
  color: #1e293b;
  font-weight: 600;
}

.last-update {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
}

.card-body {
  flex: 1;
  padding: 20px;
}

.metric-display {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  gap: 20px;
}

.gauge-container {
  position: relative;
  width: 120px;
  height: 120px;
  flex-shrink: 0;
}

.gauge-chart {
  width: 100%;
  height: 100%;
}

.gauge-value {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.value-number {
  display: block;
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.2;
}

.value-label {
  display: block;
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
  margin-top: 2px;
}

.metric-details {
  flex: 1;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f1f5f9;

  &:last-child {
    border-bottom: none;
  }
}

.detail-label {
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
}

.detail-value {
  font-size: 13px;
  color: #1e293b;
  font-weight: 600;

  &.temp-critical {
    color: #ef4444;
  }

  &.temp-warning {
    color: #f59e0b;
  }

  &.temp-normal {
    color: #10b981;
  }
}

.trend-chart {
  height: 80px;
  width: 100%;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
}

.trend-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;

  &.trend-rising {
    background: #fef3c7;
    color: #92400e;
  }

  &.trend-falling {
    background: #d1fae5;
    color: #065f46;
  }

  &.trend-stable {
    background: #eff6ff;
    color: #1e40af;
  }
}

.trend-icon {
  font-size: 14px;
}

.threshold-info {
  display: flex;
  align-items: center;
  gap: 4px;
}

.threshold-label {
  font-size: 12px;
  color: #64748b;
}

.threshold-value {
  font-size: 12px;
  color: #1e293b;
  font-weight: 600;
}

/* 系统信息区域 */
.system-info-section {
  margin-bottom: 24px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.info-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  border-top: 4px solid #f59e0b;

  &.network-card {
    border-top-color: #3b82f6;
  }

  &.load-card {
    border-top-color: #8b5cf6;
  }

  &.processes-card {
    border-top-color: #10b981;
  }
}

.network-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 20px;
}

.network-stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: #f8fafc;
  border-radius: 8px;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
}

.stat-value {
  font-size: 13px;
  color: #1e293b;
  font-weight: 600;
}

.network-chart,
.load-chart {
  height: 100px;
  width: 100%;
}

.load-indicators {
  margin-bottom: 20px;
}

.load-indicator {
  margin-bottom: 12px;

  &:last-child {
    margin-bottom: 0;
  }
}

.load-label {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 4px;
  font-weight: 500;
}

.load-bar {
  position: relative;
  height: 20px;
  background: #f1f5f9;
  border-radius: 10px;
  overflow: hidden;
}

.load-fill {
  height: 100%;
  background: linear-gradient(90deg, #8b5cf6 0%, #7c3aed 100%);
  border-radius: 10px;
  transition: width 0.3s ease;
}

.load-value {
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  font-size: 11px;
  color: white;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.processes-list {
  max-height: 200px;
  overflow-y: auto;
}

.process-item {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr auto;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f1f5f9;

  &:last-child {
    border-bottom: none;
  }
}

.process-name {
  font-size: 13px;
  color: #334155;
  font-weight: 500;
}

.process-cpu,
.process-memory {
  font-size: 13px;
  color: #1e293b;
  font-weight: 600;
  text-align: center;
}

.process-status {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-left: 10px;

  &.running {
    background-color: #10b981;
    box-shadow: 0 0 6px rgba(16, 185, 129, 0.5);
  }

  &.stopped {
    background-color: #ef4444;
    box-shadow: 0 0 6px rgba(239, 68, 68, 0.5);
  }

  &.sleeping {
    background-color: #f59e0b;
    box-shadow: 0 0 6px rgba(245, 158, 11, 0.5);
  }
}

/* 警报区域 */
.alerts-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 40px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
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
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title-icon {
  font-size: 20px;
}

.alerts-count {
  display: flex;
  align-items: center;
  background: #f1f5f9;
  border-radius: 20px;
  padding: 4px 10px;
  font-size: 14px;
  border: 1px solid #e2e8f0;
}

.count-number {
  color: #ef4444;
  font-weight: 600;
  margin-right: 4px;
}

.count-label {
  color: #64748b;
}

.section-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  background: white;
  color: #475569;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover:not(:disabled) {
    transform: translateY(-1px);
  }

  &.clear-btn {
    background: #fef2f2;
    border-color: #fecaca;
    color: #dc2626;

    &:hover:not(:disabled) {
      background: #fee2e2;
      border-color: #fca5a5;
    }
  }
}

.alerts-list {
  max-height: 300px;
  overflow-y: auto;
}

.alert-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 10px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;

  &:last-child {
    margin-bottom: 0;
  }

  &:hover {
    background: #f1f5f9;
    transform: translateX(4px);
  }

  &.critical {
    border-left: 4px solid #ef4444;
    background: #fef2f2;

    &:hover {
      background: #fee2e2;
    }
  }

  &.warning {
    border-left: 4px solid #f59e0b;
    background: #fffbeb;

    &:hover {
      background: #fef3c7;
    }
  }

  &.info {
    border-left: 4px solid #3b82f6;
    background: #eff6ff;

    &:hover {
      background: #dbeafe;
    }
  }
}

.alert-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.alert-content {
  flex: 1;
}

.alert-title {
  font-size: 15px;
  color: #1e293b;
  font-weight: 600;
  margin-bottom: 4px;
}

.alert-message {
  font-size: 13px;
  color: #64748b;
}

.alert-time {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 500;
  flex-shrink: 0;
}

.alert-dismiss {
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
  flex-shrink: 0;

  &:hover {
    background: #f1f5f9;
    color: #64748b;
  }
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .metrics-grid,
  .info-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 992px) {
  .top-info-container {
    flex-direction: column;
    align-items: stretch;
  }

  .ip-info-row {
    justify-content: center;
    flex-wrap: wrap;
  }

  .control-row {
    justify-content: center;
    width: 100%;
  }

  .metrics-grid,
  .info-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
  }

  .section-actions {
    justify-content: flex-end;
  }
}

@media (max-width: 768px) {
  .health-monitoring {
    padding: 15px;
  }

  .metric-display {
    flex-direction: column;
    align-items: stretch;
  }

  .gauge-container {
    align-self: center;
  }

  .alert-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .alert-time {
    align-self: flex-end;
  }
}

@media (max-width: 576px) {
  .ip-info-row {
    flex-direction: column;
    align-items: stretch;
  }

  .refresh-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .metric-card,
  .info-card {
    margin-bottom: 20px;
  }
}
</style>
