# 🔧 Cursor Session Manager

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)

> A powerful session management tool for Cursor AI IDE. Save, restore, and manage your Cursor Agent conversation history with ease.

[简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md)

---

## 📖 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Architecture](#-architecture)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Core Capabilities

- 💾 **Save Sessions** - Preserve your Cursor Agent conversation history
- 🔄 **Restore Sessions** - Switch back to any previous conversation state
- 🤖 **Auto-Save** - Intelligent automatic saving (every 10s/30s/1min/2min/5min/10min)
- 🔍 **Search** - Quickly find sessions by project name or description
- ✏️ **Edit** - Rename and update session descriptions
- 🗑️ **Delete** - Remove unwanted sessions
- 📁 **Multi-Project** - Manage sessions across different projects

### Web Interface

- 🎨 **Modern UI** - Beautiful gradient design with smooth animations
- 📱 **Responsive** - Works on desktop, tablet, and mobile
- 🌐 **Public Access** - Deploy anywhere with Docker
- ⚡ **Real-time** - Live status updates and session management
- 🔐 **Safe** - Automatic backup before restore operations

### Technical Features

- 🐳 **Docker** - One-command deployment
- 🚀 **FastAPI** - High-performance async API
- 💾 **SQLite** - Direct access to Cursor's session database
- 🎯 **Smart Deduplication** - Avoids duplicate saves
- 📊 **Health Checks** - Built-in monitoring and auto-restart

---

## 📸 Screenshots

### Main Interface
Beautiful card-based session management interface

### Auto-Save Configuration
Flexible auto-save intervals from 10 seconds to hours

### Session Restore
One-click restore with automatic backup

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Cursor IDE installed
- Linux/Mac (Windows WSL2 also works)

### One-Command Start

```bash
# Clone the repository
git clone https://github.com/yourusername/cursor-session-manager.git
cd cursor-session-manager

# Start with Docker Compose
cd web-ui
docker-compose up -d

# Access the interface
open http://localhost:8899
```

That's it! The service is now running.

---

## 📦 Installation

### Method 1: Docker Compose (Recommended)

```bash
# Navigate to project directory
cd cursor-session-manager/web-ui

# Start the service
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Method 2: Manual Docker

```bash
# Build image
docker build -t cursor-session-manager ./web-ui

# Run container
docker run -d \
  --name cursor-session-manager \
  -p 8899:8080 \
  -v ~/.cursor:/root/.cursor:ro \
  -v $(pwd)/saved_sessions:/root/cursor-session-manager/saved_sessions \
  --restart unless-stopped \
  cursor-session-manager
```

### Method 3: CLI Tool Only

```bash
# Install dependencies
pip install -r requirements.txt

# Use the CLI tool
python3 cursor_sessions.py save
python3 cursor_sessions.py list
python3 cursor_sessions.py restore
```

---

## 📚 Usage

### Web Interface

1. **Access the Dashboard**
   ```
   http://localhost:8899
   ```

2. **Enable Auto-Save**
   - Check the "Auto-Save" toggle in the status bar
   - Select interval (recommended: 1 minute)
   - System will save automatically

3. **Manual Save**
   - Click "💾 Save Current Session"
   - Enter session name and description
   - Click "Save"

4. **Restore Session**
   - Find the session card
   - Click "🔄 Restore" button
   - Confirm the operation
   - Restart Cursor IDE
   - Session restored!

5. **Manage Sessions**
   - **Edit**: Click "✏️ Edit" to rename/update description
   - **Delete**: Click "🗑️ Delete" to remove session
   - **Search**: Use search box to filter sessions

### CLI Usage

```bash
# Save current session
python3 cursor_sessions.py save

# List all sessions
python3 cursor_sessions.py list

# Restore a session (interactive)
python3 cursor_sessions.py restore

# Restore specific session by ID
python3 cursor_sessions.py restore 20251025_143520

# Delete a session
python3 cursor_sessions.py delete 20251025_143520
```

### Using the Shortcut Script

```bash
# Create alias (optional)
alias cs='~/cursor-session-manager/cs'

# Use shortcuts
cs save      # Save session
cs list      # List sessions
cs restore   # Restore session
```

---

## ⚙️ Configuration

### Auto-Save Intervals

Choose from multiple intervals:

| Interval | Use Case |
|----------|----------|
| Every 10 seconds | Rapid prototyping |
| Every 30 seconds | Fast iteration |
| Every 1 minute | Daily development (default) ⭐ |
| Every 2 minutes | Stable development |
| Every 5 minutes | Regular work |
| Every 10 minutes | Long-term projects |

### Port Configuration

Edit `docker-compose.yml`:

```yaml
ports:
  - "YOUR_PORT:8080"  # Change YOUR_PORT
```

### Public Access

For public internet access:

1. **Cloud Server**: Open port 8899 in security group
2. **Local + Tunnel**: Use ngrok, frp, or Cloudflare Tunnel

Example with ngrok:
```bash
ngrok http 8899
```

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────┐
│        Browser (Any Device)         │
│     http://YOUR_IP:8899            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Docker Container                   │
│  ┌────────────────────────────────┐ │
│  │  Frontend (HTML/JS/CSS)        │ │
│  │  - Modern UI                   │ │
│  │  - Real-time updates           │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │
│  │  Backend API (FastAPI)         │ │
│  │  - RESTful endpoints           │ │
│  │  - Session CRUD                │ │
│  └────────────────────────────────┘ │
│  Port: 0.0.0.0:8899 -> 8080        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         Host Filesystem             │
│  ~/.cursor/chats/                   │
│  (Cursor session database)          │
│                                     │
│  ~/cursor-session-manager/          │
│  saved_sessions/                    │
│  (Saved session backups)            │
└─────────────────────────────────────┘
```

### Technology Stack

- **Frontend**: Pure HTML5 + CSS3 + Vanilla JavaScript
- **Backend**: FastAPI (Python 3.11+)
- **Database**: SQLite (Cursor's native format)
- **Containerization**: Docker + Docker Compose
- **Web Server**: Uvicorn (ASGI)

### File Structure

```
cursor-session-manager/
├── cursor_sessions.py          # CLI tool
├── cs                          # Shortcut script
├── README.md                   # Main documentation (English)
├── README.zh-CN.md            # Chinese (Simplified)
├── README.zh-TW.md            # Chinese (Traditional)
├── README.ja.md               # Japanese
├── LICENSE                     # MIT License
├── .gitignore                 # Git ignore rules
│
├── web-ui/                    # Web interface
│   ├── Dockerfile             # Docker image config
│   ├── docker-compose.yml     # Docker Compose config
│   ├── requirements.txt       # Python dependencies
│   ├── manage.sh             # Management script
│   ├── README.md             # Web UI documentation
│   │
│   ├── backend/
│   │   └── app.py            # FastAPI application
│   │
│   └── frontend/
│       └── index.html        # Single-page application
│
└── saved_sessions/            # Session storage (git-ignored)
    └── [project-name]/
        ├── *.db              # Session databases
        ├── *.json            # Exported data
        └── *.meta.json       # Session metadata
```

---

## 🛠️ Development

### Local Development

```bash
# Install dependencies
pip install -r web-ui/requirements.txt

# Run backend locally
cd web-ui/backend
python app.py

# Access at http://localhost:8080
```

### Build Docker Image

```bash
cd web-ui
docker build -t cursor-session-manager .
```

### Run Tests

```bash
# Test API endpoints
curl http://localhost:8899/api/status
curl http://localhost:8899/api/sessions

# Test auto-save
curl -X POST http://localhost:8899/api/sessions/auto-save
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api` | GET | API status |
| `/api/status` | GET | System status |
| `/api/sessions` | GET | List all sessions |
| `/api/sessions/save` | POST | Save session manually |
| `/api/sessions/auto-save` | POST | Auto-save session |
| `/api/sessions/{id}/restore` | POST | Restore session |
| `/api/sessions/{id}/rename` | PUT | Rename session |
| `/api/sessions/{id}` | DELETE | Delete session |
| `/api/projects` | GET | List projects |

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs

- Use the [Issues](https://github.com/yourusername/cursor-session-manager/issues) page
- Include steps to reproduce
- Provide system information

### Suggesting Features

- Open a [Feature Request](https://github.com/yourusername/cursor-session-manager/issues/new)
- Explain the use case
- Describe the expected behavior

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Write clear commit messages
- Update documentation as needed
- Test your changes thoroughly

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Cursor](https://cursor.sh/)
- Containerized with [Docker](https://www.docker.com/)

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/cursor-session-manager/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/cursor-session-manager/discussions)

---

## 🗺️ Roadmap

- [ ] Authentication system
- [ ] Session export/import
- [ ] Session comparison
- [ ] Session tags and categories
- [ ] Advanced search filters
- [ ] Batch operations
- [ ] Session analytics
- [ ] Cloud sync support

---

<div align="center">

**[⬆ Back to Top](#-cursor-session-manager)**

Made with ❤️ for Cursor users

</div>
