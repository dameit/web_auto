# web_auto - 自动化测试与监控系统

![项目架构](https://via.placeholder.com/800x400?text=Web+Auto+Architecture)

一个基于前后端分离架构的自动化测试与监控系统，主要用于服务器BMC（Baseboard Management Controller）和操作系统层面的自动化配置、测试和监控。

## 📋 项目简介

`web_auto` 是一个企业级自动化测试平台，支持：
- ✅ BMC配置自动化（Syslog、SNMP、SMTP、LDAP、AD等）
- ✅ OS系统监控（CPU、内存、硬盘、网络等实时指标）
- ✅ 固件更新自动化（Redfish协议）
- ✅ 测试用例批量执行与结果管理
- ✅ 用户权限与配置管理

适用于数据中心运维、服务器厂商测试验证等场景。

## 🏗️ 技术架构

### 前端技术栈
- **框架**: Vue 3 + Vite
- **UI组件库**: Element Plus
- **图表库**: ECharts (5.4.3) + echarts-liquidfill (3.1.0)
- **状态管理**: Vue Router 4
- **构建工具**: Vite 7.2.4

### 后端技术栈
- **框架**: Flask 2.x
- **数据库**: MySQL
- **SSH连接**: Paramiko
- **HTTP请求**: requests
- **自动化测试**: Selenium WebDriver
- **Redfish协议**: 自定义实现

### 核心功能模块
```
├── backend/          # Flask后端服务
│   ├── app.py        # 主应用入口
│   └── redfish_update_fw.py  # Redfish固件更新
├── common/           # 公共模块
│   ├── config_read.py    # 配置读取
│   ├── my_post.py        # HTTP请求封装
│   ├── mysql_connect.py  # 数据库连接
│   └── ssh_connect.py    # SSH连接封装
├── frontend/         # Vue3前端
│   ├── src/
│   │   ├── api/          # API接口封装
│   │   ├── components/   # 公共组件
│   │   ├── pages/        # 页面组件
│   │   └── router/       # 路由配置
├── pages/            # 测试用例模块
│   ├── test_*.py       # 各类测试用例实现
├── config.ini        # 系统配置文件
└── run.py            # 启动脚本
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 20.19+ 或 22.12+
- MySQL 5.7+
- Chrome浏览器（用于Selenium）

### 安装步骤

#### 1. 后端安装
```bash
# 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库（需先创建web_auto数据库）
# 修改config.ini中的数据库配置
```

#### 2. 前端安装
```bash
cd frontend
npm install
```

#### 3. 启动服务
```bash
# 启动后端（在项目根目录）
python run.py

# 启动前端（在frontend目录）
npm run dev
```

### 访问地址
- 前端: `http://localhost:5173`
- 后端API: `http://localhost:4900/api/`

## 🔧 核心功能说明

### 1. 用户认证系统
- 注册/登录功能
- 用户配置存储（BMC/OS连接信息）
- 权限管理

### 2. 系统监控
- 实时监控CPU、内存、硬盘使用率
- 网络性能监控（上传/下载速度、延迟）
- 系统负载监控（1/5/15分钟负载）
- 进程监控
- 警报系统（阈值告警）

### 3. 自动化测试
支持以下测试用例：
- **Syslog设置**: 远程日志配置
- **Trap设置**: SNMP Trap配置  
- **SMTP设置**: 邮件告警配置
- **SNMP V1/V2**: 社区字符串配置
- **上电开机策略**: 电源策略配置
- **网络设置**: 主机名配置
- **用户/用户组**: 用户管理
- **LDAP/E-directory**: 外部用户服务
- **Active Directory**: AD集成
- **BIOS设置**: BIOS参数配置
- **日期&时间**: NTP时间同步
- **日志设置**: 日志存储策略

### 4. BMC固件更新
- 基于Redfish协议的固件更新
- 文件上传管理
- 更新任务监控

## 📝 配置说明

### config.ini 配置项
```ini
[database]
host = 192.168.45.128
port = 3306
username = root
password = Admin@8000
database = web_auto

[redfish_path]
session_post_api = https://ip/redfish/v1/SessionService/Sessions
local_file_upload_api = https://ip/redfish/v1/UpdateService/FirmwareInventory
bmc_file_update_api = https://ip/redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate
bmc_file_update_target = /redfish/v1/UpdateService/FirmwareInventory/ActiveBMC
task_api = https://ip/redfish/v1/TaskService/Tasks/task_num

[file_save_path]
save_path = file_upload
screenshot_save_path = screenshot_save
```

### 测试用例配置
每个测试用例在 `config.ini` 中有独立的配置段，包含：
- `meau_expand`: 菜单展开定位
- `path`: 导航路径
- `config`: 操作步骤（click/input/select等）

## 🤖 使用示例

### 监控页面
访问 `/monitor` 查看实时系统指标：
- CPU使用率仪表盘
- 内存使用率液态填充图
- 硬盘使用率环形图
- 网络性能趋势图
- 系统负载条形图

### 执行测试用例
1. 在首页配置BMC/OS连接信息
2. 选择需要执行的测试用例
3. 点击"开始测试"
4. 查看执行结果和截图

## 📊 数据格式说明

### 监控数据格式
```json
{
  "cpu_used": "7.7",
  "cpu_model": "Hygon C86-3G (OPN:3350M)",
  "cpu_cores": "4",
  "cpu_frequency": "2300",
  "mem_used": "44.4",
  "mem_total": "3.6",
  "mem_isused": "1.6",
  "disk_used": "69",
  "disk_total": "18",
  "disk_isused": "13"
}
```

### 测试用例执行格式
```json
{
  "ip": "192.168.1.100",
  "username": "admin",
  "password": "password",
  "test_cases": ["Syslog设置", "SNMP V1/V2设置"],
  "is_before": true
}
```

## 🤝 贡献指南

欢迎贡献代码！请遵循以下流程：
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 📞 联系方式

如有问题，请联系项目维护者。