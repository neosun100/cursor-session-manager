#!/bin/bash
# Cursor Session Manager - 快捷脚本

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

case "$1" in
    save|s)
        cd "$SCRIPT_DIR"
        python3 cursor_sessions.py save
        ;;
    list|l)
        cd "$SCRIPT_DIR"
        python3 cursor_sessions.py list
        ;;
    restore|r)
        cd "$SCRIPT_DIR"
        if [ -n "$2" ]; then
            python3 cursor_sessions.py restore "$2"
        else
            python3 cursor_sessions.py restore
        fi
        ;;
    delete|d)
        cd "$SCRIPT_DIR"
        if [ -n "$2" ]; then
            python3 cursor_sessions.py delete "$2"
        else
            echo "❌ 请指定要删除的会话 ID"
            echo "用法: $0 delete <会话ID>"
        fi
        ;;
    help|h|"")
        echo ""
        echo "🔧 Cursor Agent 会话管理工具 - 快捷命令"
        echo "=========================================="
        echo ""
        echo "用法: $0 <命令> [参数]"
        echo ""
        echo "命令:"
        echo "  save, s              保存当前会话"
        echo "  list, l              列出所有会话"
        echo "  restore, r [ID]      恢复会话（可选指定ID）"
        echo "  delete, d <ID>       删除指定会话"
        echo "  help, h              显示此帮助信息"
        echo ""
        echo "示例:"
        echo "  $0 save                    # 保存当前会话"
        echo "  $0 list                    # 查看所有会话"
        echo "  $0 restore                 # 交互式恢复"
        echo "  $0 restore 20251025_001147 # 恢复指定会话"
        echo ""
        echo "💾 会话存储位置: $SCRIPT_DIR/saved_sessions/"
        echo ""
        ;;
    *)
        echo "❌ 未知命令: $1"
        echo "运行 '$0 help' 查看帮助"
        exit 1
        ;;
esac
