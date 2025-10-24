# 🔧 Cursor Session Manager

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)

> 强大的 Cursor AI IDE 会话管理工具。轻松保存、恢复和管理您的 Cursor Agent 对话历史。

[English](README.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md)

---

## 📖 目录

- [功能特性](#-功能特性)
- [界面预览](#-界面预览)
- [快速开始](#-快速开始)
- [安装部署](#-安装部署)
- [使用方法](#-使用方法)
- [配置说明](#-配置说明)
- [系统架构](#-系统架构)
- [开发指南](#-开发指南)
- [贡献代码](#-贡献代码)
- [开源协议](#-开源协议)

---

## ✨ 功能特性

### 核心功能

- 💾 **保存会话** - 保存 Cursor Agent 的完整对话历史
- 🔄 **恢复会话** - 切换回任意历史对话状态
- 🤖 **自动保存** - 智能自动保存（每10秒/30秒/1分钟/2分钟/5分钟/10分钟）
- 🔍 **搜索功能** - 按项目名称或描述快速查找会话
- ✏️ **编辑会话** - 重命名和更新会话描述
- 🗑️ **删除会话** - 删除不需要的会话
- 📁 **多项目管理** - 跨项目管理所有会话

### Web 界面

- 🎨 **现代化 UI** - 精美的渐变设计和流畅动画
- 📱 **响应式设计** - 支持桌面、平板和手机
- 🌐 **公网访问** - 使用 Docker 部署到任何地方
- ⚡ **实时更新** - 实时状态更新和会话管理
- 🔐 **安全操作** - 恢复前自动备份当前状态

### 技术特性

- 🐳 **Docker** - 一键部署
- 🚀 **FastAPI** - 高性能异步 API
- 💾 **SQLite** - 直接访问 Cursor 的会话数据库
- 🎯 **智能去重** - 只在内容变化时保存，避免重复
- 📊 **健康检查** - 内置监控和自动重启

---

## 📸 界面预览

### 主界面
精美的卡片式会话管理界面

### 自动保存配置
灵活的自动保存间隔，从10秒到小时级

### 会话恢复
一键恢复，自动备份保护

---

## 🚀 快速开始

### 系统要求

- Docker & Docker Compose
- Cursor IDE 已安装
- Linux/Mac（Windows WSL2 也可以）

### 一键启动

```bash
# 克隆仓库
git clone https://github.com/yourusername/cursor-session-manager.git
cd cursor-session-manager

# 使用 Docker Compose 启动
cd web-ui
docker-compose up -d

# 访问界面
open http://localhost:8899
```

就这么简单！服务已经运行了。

---

## 📦 安装部署

### 方法 1：Docker Compose（推荐）

```bash
# 进入项目目录
cd cursor-session-manager/web-ui

# 启动服务
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 方法 2：手动 Docker

```bash
# 构建镜像
docker build -t cursor-session-manager ./web-ui

# 运行容器
docker run -d \
  --name cursor-session-manager \
  -p 8899:8080 \
  -v ~/.cursor:/root/.cursor:ro \
  -v $(pwd)/saved_sessions:/root/cursor-session-manager/saved_sessions \
  --restart unless-stopped \
  cursor-session-manager
```

### 方法 3：仅使用 CLI 工具

```bash
# 安装依赖
pip install -r requirements.txt

# 使用 CLI 工具
python3 cursor_sessions.py save
python3 cursor_sessions.py list
python3 cursor_sessions.py restore
```

---

## 📚 使用方法

### Web 界面使用

1. **访问控制面板**
   ```
   http://localhost:8899
   ```

2. **开启自动保存**
   - 勾选状态栏的"自动保存"开关
   - 选择保存间隔（推荐：每1分钟）
   - 系统会自动保存，只在内容变化时保存

3. **手动保存**
   - 点击"💾 保存当前会话"
   - 输入会话名称和描述
   - 点击"保存"

4. **恢复会话**
   - 找到会话卡片
   - 点击"🔄 恢复"按钮
   - 确认操作
   - 重启 Cursor IDE
   - 会话已恢复！

5. **管理会话**
   - **编辑**：点击"✏️ 编辑"修改名称/描述
   - **删除**：点击"🗑️ 删除"移除会话
   - **搜索**：使用搜索框过滤会话

### CLI 命令行使用

```bash
# 保存当前会话
python3 cursor_sessions.py save

# 列出所有会话
python3 cursor_sessions.py list

# 恢复会话（交互式）
python3 cursor_sessions.py restore

# 恢复指定会话
python3 cursor_sessions.py restore 20251025_143520

# 删除会话
python3 cursor_sessions.py delete 20251025_143520
```

### 使用快捷脚本

```bash
# 创建别名（可选）
alias cs='~/cursor-session-manager/cs'

# 使用快捷命令
cs save      # 保存会话
cs list      # 列出会话
cs restore   # 恢复会话
```

---

## ⚙️ 配置说明

### 自动保存间隔

支持多种间隔选项：

| 间隔 | 适用场景 |
|------|----------|
| 每10秒 | 快速原型开发 |
| 每30秒 | 快速迭代 |
| 每1分钟 | 日常开发（默认）⭐ |
| 每2分钟 | 稳定开发 |
| 每5分钟 | 常规工作 |
| 每10分钟 | 长期项目 |

### 智能去重机制

系统会自动检测内容变化：
- ✅ **有变化**：保存新会话
- ⏭️ **无变化**：跳过保存，避免重复

检测方式：
1. 对比文件大小
2. 计算文件 MD5 哈希值
3. 完全相同则跳过

### 端口配置

编辑 `docker-compose.yml`：

```yaml
ports:
  - "YOUR_PORT:8080"  # 修改 YOUR_PORT
```

### 公网访问

对于公网访问：

1. **云服务器**：在安全组开放 8899 端口
2. **本地 + 隧道**：使用 ngrok、frp 或 Cloudflare Tunnel

使用 ngrok 示例：
```bash
ngrok http 8899
```

---

## 🏗️ 系统架构

### 架构图

```
┌─────────────────────────────────────┐
│        浏览器（任意设备）            │
│     http://YOUR_IP:8899            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Docker 容器                        │
│  ┌────────────────────────────────┐ │
│  │  前端 (HTML/JS/CSS)            │ │
│  │  - 现代化 UI                   │ │
│  │  - 实时更新                    │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │
│  │  后端 API (FastAPI)            │ │
│  │  - RESTful 接口                │ │
│  │  - 会话 CRUD                   │ │
│  └────────────────────────────────┘ │
│  端口: 0.0.0.0:8899 -> 8080        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         主机文件系统                 │
│  ~/.cursor/chats/                   │
│  (Cursor 会话数据库)                │
│                                     │
│  ~/cursor-session-manager/          │
│  saved_sessions/                    │
│  (保存的会话备份)                   │
└─────────────────────────────────────┘
```

### 技术栈

- **前端**：纯 HTML5 + CSS3 + 原生 JavaScript
- **后端**：FastAPI (Python 3.11+)
- **数据库**：SQLite（Cursor 原生格式）
- **容器化**：Docker + Docker Compose
- **Web 服务器**：Uvicorn (ASGI)

---

## 🛠️ 开发指南

### 本地开发

```bash
# 安装依赖
pip install -r web-ui/requirements.txt

# 本地运行后端
cd web-ui/backend
python app.py

# 访问 http://localhost:8080
```

### 构建 Docker 镜像

```bash
cd web-ui
docker build -t cursor-session-manager .
```

### API 测试

```bash
# 测试 API 端点
curl http://localhost:8899/api/status
curl http://localhost:8899/api/sessions

# 测试自动保存
curl -X POST http://localhost:8899/api/sessions/auto-save
```

---

## 🤝 贡献代码

欢迎贡献！以下是参与方式：

### 报告 Bug

- 使用 [Issues](https://github.com/yourusername/cursor-session-manager/issues) 页面
- 包含复现步骤
- 提供系统信息

### 功能建议

- 提交 [Feature Request](https://github.com/yourusername/cursor-session-manager/issues/new)
- 说明使用场景
- 描述期望行为

### 提交 Pull Request

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📝 开源协议

本项目采用 MIT 协议 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🙏 致谢

- 基于 [FastAPI](https://fastapi.tiangolo.com/) 构建
- 为 [Cursor](https://cursor.sh/) 提供支持
- 使用 [Docker](https://www.docker.com/) 容器化

---

## 📞 支持

- **问题反馈**：[GitHub Issues](https://github.com/yourusername/cursor-session-manager/issues)
- **讨论交流**：[GitHub Discussions](https://github.com/yourusername/cursor-session-manager/discussions)

---

## 🗺️ 开发路线

- [ ] 用户认证系统
- [ ] 会话导出/导入
- [ ] 会话对比功能
- [ ] 会话标签分类
- [ ] 高级搜索过滤
- [ ] 批量操作支持
- [ ] 会话数据分析
- [ ] 云端同步支持

---

<div align="center">

**[⬆ 返回顶部](#-cursor-session-manager)**

用 ❤️ 为 Cursor 用户打造

</div>
