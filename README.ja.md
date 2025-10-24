# 🔧 Cursor Session Manager

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)

> Cursor AI IDE のための強力なセッション管理ツール。Cursor Agent の会話履歴を簡単に保存、復元、管理できます。

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md)

---

## 📖 目次

- [機能](#-機能)
- [スクリーンショット](#-スクリーンショット)
- [クイックスタート](#-クイックスタート)
- [インストール](#-インストール)
- [使用方法](#-使用方法)
- [設定](#-設定)
- [アーキテクチャ](#-アーキテクチャ)
- [開発](#-開発)
- [コントリビューション](#-コントリビューション)
- [ライセンス](#-ライセンス)

---

## ✨ 機能

### コア機能

- 💾 **セッション保存** - Cursor Agent の完全な会話履歴を保存
- 🔄 **セッション復元** - 任意の過去の会話状態に切り替え
- 🤖 **自動保存** - インテリジェント自動保存（10秒/30秒/1分/2分/5分/10分毎）
- 🔍 **検索機能** - プロジェクト名や説明で素早くセッションを検索
- ✏️ **セッション編集** - セッション名と説明を更新
- 🗑️ **セッション削除** - 不要なセッションを削除
- 📁 **マルチプロジェクト** - 複数プロジェクトのセッションを管理

### Web インターフェース

- 🎨 **モダン UI** - 美しいグラデーションデザインとスムーズなアニメーション
- 📱 **レスポンシブ** - デスクトップ、タブレット、モバイルに対応
- 🌐 **パブリックアクセス** - Docker でどこでもデプロイ可能
- ⚡ **リアルタイム** - ライブステータス更新とセッション管理
- 🔐 **安全な操作** - 復元前に自動バックアップ

### 技術機能

- 🐳 **Docker** - ワンコマンドデプロイ
- 🚀 **FastAPI** - 高性能非同期 API
- 💾 **SQLite** - Cursor のセッションデータベースに直接アクセス
- 🎯 **スマート重複排除** - 変更時のみ保存、重複を回避
- 📊 **ヘルスチェック** - 組み込み監視と自動再起動

---

## 🚀 クイックスタート

### 必要な環境

- Docker & Docker Compose
- Cursor IDE がインストール済み
- Linux/Mac（Windows WSL2 も対応）

### ワンコマンド起動

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/cursor-session-manager.git
cd cursor-session-manager

# Docker Compose で起動
cd web-ui
docker-compose up -d

# インターフェースにアクセス
open http://localhost:8899
```

これだけです！サービスが起動しました。

---

## 📝 ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています - 詳細は [LICENSE](LICENSE) ファイルをご覧ください。

---

<div align="center">

**[⬆ トップに戻る](#-cursor-session-manager)**

Cursor ユーザーのために ❤️ を込めて作成

</div>
