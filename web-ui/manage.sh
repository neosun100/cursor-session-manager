#!/bin/bash
# Cursor Session Manager - 管理脚本

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

case "$1" in
    start)
        echo "🚀 启动 Cursor Session Manager..."
        docker-compose up -d
        echo "✅ 服务已启动"
        echo "📍 访问地址: http://localhost:8899"
        ;;
    
    stop)
        echo "🛑 停止服务..."
        docker-compose stop
        echo "✅ 服务已停止"
        ;;
    
    restart)
        echo "🔄 重启服务..."
        docker-compose restart
        echo "✅ 服务已重启"
        ;;
    
    status)
        echo "📊 检查服务状态..."
        echo ""
        echo "=== 容器状态 ==="
        docker ps | grep cursor-session-manager || echo "容器未运行"
        echo ""
        echo "=== 端口监听 ==="
        ss -tuln | grep 8899 || echo "端口未监听"
        echo ""
        echo "=== API 状态 ==="
        curl -s http://localhost:8899/api/status 2>/dev/null | python3 -m json.tool || echo "API 无响应"
        ;;
    
    logs)
        echo "📋 查看日志 (Ctrl+C 退出)..."
        docker-compose logs -f
        ;;
    
    update)
        echo "🔄 更新服务..."
        docker-compose down
        docker-compose build --no-cache
        docker-compose up -d
        echo "✅ 更新完成"
        ;;
    
    clean)
        echo "⚠️  警告: 这将删除容器（数据不会丢失）"
        read -p "确认继续? (y/N): " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            docker-compose down
            echo "✅ 容器已删除"
        else
            echo "❌ 已取消"
        fi
        ;;
    
    url)
        echo "🌐 访问地址:"
        echo ""
        echo "  本地访问:"
        echo "    http://localhost:8899"
        echo ""
        echo "  局域网访问:"
        LOCAL_IP=$(hostname -I | awk '{print $1}')
        echo "    http://$LOCAL_IP:8899"
        echo ""
        echo "  公网访问 (需要配置):"
        echo "    http://YOUR_PUBLIC_IP:8899"
        echo ""
        ;;
    
    test)
        echo "🧪 运行测试..."
        echo ""
        
        # 测试 API
        echo "1. 测试 API 状态..."
        if curl -s http://localhost:8899/api/status > /dev/null 2>&1; then
            echo "   ✅ API 正常"
        else
            echo "   ❌ API 异常"
            exit 1
        fi
        
        # 测试会话列表
        echo "2. 测试会话列表..."
        if curl -s http://localhost:8899/api/sessions > /dev/null 2>&1; then
            echo "   ✅ 会话列表正常"
        else
            echo "   ❌ 会话列表异常"
            exit 1
        fi
        
        # 测试前端
        echo "3. 测试前端页面..."
        if curl -s http://localhost:8899/ > /dev/null 2>&1; then
            echo "   ✅ 前端正常"
        else
            echo "   ❌ 前端异常"
            exit 1
        fi
        
        echo ""
        echo "✅ 所有测试通过！"
        echo "📍 打开浏览器访问: http://localhost:8899"
        ;;
    
    open)
        echo "🌐 正在打开浏览器..."
        if command -v xdg-open > /dev/null 2>&1; then
            xdg-open http://localhost:8899
        elif command -v open > /dev/null 2>&1; then
            open http://localhost:8899
        else
            echo "📍 请手动打开: http://localhost:8899"
        fi
        ;;
    
    help|"")
        echo ""
        echo "🔧 Cursor Session Manager - 管理脚本"
        echo "========================================"
        echo ""
        echo "用法: $0 <命令>"
        echo ""
        echo "命令:"
        echo "  start      启动服务"
        echo "  stop       停止服务"
        echo "  restart    重启服务"
        echo "  status     查看状态"
        echo "  logs       查看日志"
        echo "  update     更新服务"
        echo "  clean      清理容器"
        echo "  url        显示访问地址"
        echo "  test       运行测试"
        echo "  open       在浏览器中打开"
        echo "  help       显示帮助"
        echo ""
        echo "示例:"
        echo "  $0 start      # 启动服务"
        echo "  $0 status     # 查看状态"
        echo "  $0 logs       # 查看日志"
        echo "  $0 open       # 打开浏览器"
        echo ""
        echo "📍 访问地址: http://localhost:8899"
        echo ""
        ;;
    
    *)
        echo "❌ 未知命令: $1"
        echo "运行 '$0 help' 查看帮助"
        exit 1
        ;;
esac
