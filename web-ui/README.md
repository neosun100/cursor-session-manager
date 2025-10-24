# Cursor Session Manager - Web UI

## 🌐 Web 管理界面

这是一个完整的 Web UI 管理系统，用于管理 Cursor Agent 会话。

### ✨ 功能特性

- 📊 实时查看所有保存的会话
- 💾 一键保存当前会话
- 🔄 一键恢复任意会话
- ✏️ 编辑会话名称和描述
- 🗑️ 删除不需要的会话
- 📁 按项目分组显示
- 🌐 支持公网访问
- 🚀 Docker 一键部署

### 🚀 快速启动

#### 方法 1: Docker Compose（推荐）

```bash
cd ~/cursor-session-manager/web-ui
docker-compose up -d
```

#### 方法 2: Docker 命令

```bash
cd ~/cursor-session-manager/web-ui

# 构建镜像
docker build -t cursor-session-manager .

# 运行容器
docker run -d \
  --name cursor-session-manager \
  -p 8899:8080 \
  -v ~/.cursor:/root/.cursor:ro \
  -v ~/cursor-session-manager/saved_sessions:/root/cursor-session-manager/saved_sessions \
  --restart unless-stopped \
  cursor-session-manager
```

### 🌐 访问地址

启动后可以通过以下方式访问：

- **本地访问**: http://localhost:8899
- **局域网访问**: http://YOUR_LOCAL_IP:8899
- **公网访问**: http://YOUR_PUBLIC_IP:8899

### 📋 管理命令

```bash
# 查看日志
docker-compose logs -f

# 停止服务
docker-compose stop

# 启动服务
docker-compose start

# 重启服务
docker-compose restart

# 停止并删除容器
docker-compose down

# 重新构建并启动
docker-compose up -d --build
```

### 🔧 配置说明

#### 端口配置

默认映射到主机的 `8899` 端口，可以在 `docker-compose.yml` 中修改：

```yaml
ports:
  - "0.0.0.0:YOUR_PORT:8080"  # 修改 YOUR_PORT
```

#### 数据持久化

会话数据存储在：`~/cursor-session-manager/saved_sessions/`

即使删除容器，数据也不会丢失。

### 🌍 公网访问配置

#### 方法 1: 云服务器直接访问

如果运行在云服务器上：

1. 确保安全组/防火墙开放 8899 端口
2. 直接访问：`http://YOUR_SERVER_IP:8899`

#### 方法 2: 本地服务器 + 内网穿透

如果运行在本地，可以使用内网穿透工具：

**使用 frp:**
```bash
# frpc.ini
[cursor-session-manager]
type = tcp
local_ip = 127.0.0.1
local_port = 8899
remote_port = 8899
```

**使用 ngrok:**
```bash
ngrok http 8899
```

**使用 Cloudflare Tunnel:**
```bash
cloudflared tunnel --url http://localhost:8899
```

### 📊 API 文档

启动后访问：http://localhost:8899/docs

### 🔒 安全建议

如果需要公网访问，建议：

1. **添加认证**: 在前端添加登录功能
2. **使用 HTTPS**: 配置 SSL 证书
3. **限制 IP**: 在防火墙限制允许访问的 IP
4. **使用反向代理**: 通过 Nginx 添加安全层

### 🐛 故障排除

#### 容器无法启动

```bash
# 查看日志
docker-compose logs

# 检查端口占用
netstat -tuln | grep 8899
```

#### 无法访问 Cursor 数据

确保 `~/.cursor` 目录存在且有读取权限：

```bash
ls -la ~/.cursor
```

#### 公网无法访问

1. 检查防火墙是否开放端口：
```bash
sudo ufw allow 8899
```

2. 检查容器是否正在运行：
```bash
docker ps | grep cursor-session-manager
```

3. 检查端口绑定：
```bash
docker port cursor-session-manager
```

### 📝 使用流程

1. **启动服务**: `docker-compose up -d`
2. **打开浏览器**: 访问 http://localhost:8899
3. **保存会话**: 点击"保存当前会话"按钮
4. **管理会话**: 在界面上查看、编辑、恢复或删除会话
5. **恢复会话**: 点击"恢复"按钮，然后重启 Cursor

### 🎯 最佳实践

1. **定期保存**: 完成重要工作后立即保存
2. **描述清晰**: 使用清晰的名称和描述
3. **定期清理**: 删除不再需要的旧会话
4. **备份数据**: 定期备份 `saved_sessions` 目录

### 🔄 自动保存（计划中）

未来版本将支持：
- 自动检测 Cursor 活动
- 定时自动保存
- 智能保存策略

---

## 📞 技术支持

如有问题，请检查：
1. Docker 服务是否正常运行
2. 端口是否被占用
3. 挂载的目录是否有权限
4. 防火墙是否开放端口
