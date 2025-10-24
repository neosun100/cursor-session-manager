# 🔧 Cursor Session Manager

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)

> 強大的 Cursor AI IDE 會話管理工具。輕鬆保存、恢復和管理您的 Cursor Agent 對話歷史。

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

---

## 📖 目錄

- [功能特性](#-功能特性)
- [介面預覽](#-介面預覽)
- [快速開始](#-快速開始)
- [安裝部署](#-安裝部署)
- [使用方法](#-使用方法)
- [配置說明](#-配置說明)
- [系統架構](#-系統架構)
- [開發指南](#-開發指南)
- [貢獻代碼](#-貢獻代碼)
- [開源協議](#-開源協議)

---

## ✨ 功能特性

### 核心功能

- 💾 **保存會話** - 保存 Cursor Agent 的完整對話歷史
- 🔄 **恢復會話** - 切換回任意歷史對話狀態
- 🤖 **自動保存** - 智能自動保存（每10秒/30秒/1分鐘/2分鐘/5分鐘/10分鐘）
- 🔍 **搜尋功能** - 按專案名稱或描述快速查找會話
- ✏️ **編輯會話** - 重新命名和更新會話描述
- 🗑️ **刪除會話** - 刪除不需要的會話
- 📁 **多專案管理** - 跨專案管理所有會話

### Web 介面

- 🎨 **現代化 UI** - 精美的漸變設計和流暢動畫
- 📱 **響應式設計** - 支援桌面、平板和手機
- 🌐 **公網訪問** - 使用 Docker 部署到任何地方
- ⚡ **即時更新** - 即時狀態更新和會話管理
- 🔐 **安全操作** - 恢復前自動備份當前狀態

### 技術特性

- 🐳 **Docker** - 一鍵部署
- 🚀 **FastAPI** - 高性能異步 API
- 💾 **SQLite** - 直接訪問 Cursor 的會話資料庫
- 🎯 **智能去重** - 只在內容變化時保存，避免重複
- 📊 **健康檢查** - 內建監控和自動重啟

---

## 🚀 快速開始

### 系統要求

- Docker & Docker Compose
- Cursor IDE 已安裝
- Linux/Mac（Windows WSL2 也可以）

### 一鍵啟動

```bash
# 克隆倉庫
git clone https://github.com/yourusername/cursor-session-manager.git
cd cursor-session-manager

# 使用 Docker Compose 啟動
cd web-ui
docker-compose up -d

# 訪問介面
open http://localhost:8899
```

---

## 📝 開源協議

本專案採用 MIT 協議 - 查看 [LICENSE](LICENSE) 檔案了解詳情。

---

<div align="center">

**[⬆ 返回頂部](#-cursor-session-manager)**

用 ❤️ 為 Cursor 用戶打造

</div>
