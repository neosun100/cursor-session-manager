#!/usr/bin/env python3
"""
Cursor Agent 会话管理工具（通用版）
可以管理所有 Cursor 项目的会话状态
"""

import sqlite3
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import shutil

class CursorSessionManager:
    def __init__(self):
        # 会话存储目录（独立于项目）
        self.manager_dir = Path.home() / "cursor-session-manager"
        self.sessions_dir = self.manager_dir / "saved_sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        
        # Cursor 配置目录
        self.cursor_dir = Path.home() / ".cursor"
    
    def get_current_project_info(self):
        """获取当前工作的项目信息"""
        projects_dir = self.cursor_dir / "projects"
        
        if not projects_dir.exists():
            return None, None
        
        # 查找最近活跃的项目
        latest_project = None
        latest_time = 0
        
        for project_dir in projects_dir.iterdir():
            if project_dir.is_dir():
                worker_log = project_dir / "worker.log"
                if worker_log.exists():
                    mtime = worker_log.stat().st_mtime
                    if mtime > latest_time:
                        latest_time = mtime
                        latest_project = project_dir.name
        
        return latest_project, latest_time
    
    def find_current_session_db(self):
        """查找当前活跃的会话数据库"""
        chats_dir = self.cursor_dir / "chats"
        
        if not chats_dir.exists():
            return None, None
        
        latest_db = None
        latest_time = 0
        hash_folder = None
        
        for hash_dir in chats_dir.iterdir():
            if hash_dir.is_dir():
                for session_dir in hash_dir.iterdir():
                    if session_dir.is_dir():
                        db_file = session_dir / "store.db"
                        if db_file.exists():
                            mtime = db_file.stat().st_mtime
                            if mtime > latest_time:
                                latest_time = mtime
                                latest_db = db_file
                                hash_folder = hash_dir.name
        
        return latest_db, hash_folder
    
    def save_session(self, session_name=None, description=None):
        """保存当前会话"""
        print("\n" + "="*70)
        print("💾 保存当前 Cursor 会话")
        print("="*70)
        
        # 获取项目信息
        project_name, _ = self.get_current_project_info()
        if project_name:
            print(f"📁 当前项目: {project_name}")
        else:
            print("⚠️  无法确定当前项目")
        
        # 查找数据库
        current_db, hash_folder = self.find_current_session_db()
        if not current_db or not current_db.exists():
            print("❌ 未找到当前会话数据库")
            return False
        
        print(f"✅ 找到会话数据库: {current_db.parent.name}")
        print(f"   大小: {current_db.stat().st_size / 1024:.2f} KB")
        print(f"   最后修改: {datetime.fromtimestamp(current_db.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 交互式输入
        if not session_name:
            session_name = input("📝 会话名称（例如：修复UI颜色bug）: ").strip()
            if not session_name:
                session_name = "未命名会话"
        
        if not description:
            description = input("📋 会话描述（简要说明这次对话的内容）: ").strip()
            if not description:
                description = "无描述"
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c for c in session_name if c.isalnum() or c in (' ', '-', '_', '中', '文')).strip()
        safe_name = safe_name.replace(' ', '_')[:50]  # 限制长度
        
        base_name = f"{timestamp}_{safe_name}"
        
        # 创建项目子目录
        project_sessions_dir = self.sessions_dir / (project_name or "unknown_project")
        project_sessions_dir.mkdir(exist_ok=True)
        
        # 保存数据库
        backup_file = project_sessions_dir / f"{base_name}.db"
        shutil.copy2(current_db, backup_file)
        print(f"✅ 数据库已保存: {backup_file}")
        
        # 导出 JSON
        json_file = project_sessions_dir / f"{base_name}.json"
        self._export_db_to_json(current_db, json_file)
        print(f"✅ 数据已导出: {json_file}")
        
        # 保存元数据
        metadata = {
            'name': session_name,
            'description': description,
            'timestamp': timestamp,
            'datetime': datetime.now().isoformat(),
            'project': project_name,
            'hash_folder': hash_folder,
            'db_file': backup_file.name,
            'json_file': json_file.name,
            'size_kb': current_db.stat().st_size / 1024,
            'original_path': str(current_db)
        }
        
        meta_file = project_sessions_dir / f"{base_name}.meta.json"
        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 元数据已保存: {meta_file}")
        
        print("\n" + "="*70)
        print("✅ 会话保存完成！")
        print("="*70)
        print(f"\n保存位置: {project_sessions_dir}")
        print(f"会话ID: {timestamp}")
        print()
        
        return True
    
    def _export_db_to_json(self, db_path, json_file):
        """导出数据库到 JSON"""
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            all_data = {}
            for table_name in [t[0] for t in tables]:
                try:
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    column_names = [description[0] for description in cursor.description]
                    all_data[table_name] = [dict(zip(column_names, row)) for row in rows]
                except sqlite3.Error:
                    pass
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=2, ensure_ascii=False, default=str)
            
            conn.close()
        except Exception as e:
            print(f"⚠️  JSON 导出警告: {e}")
    
    def list_sessions(self, project_filter=None):
        """列出所有保存的会话"""
        print("\n" + "="*70)
        print("📋 已保存的会话列表")
        print("="*70 + "\n")
        
        all_sessions = []
        
        # 遍历所有项目目录
        for project_dir in self.sessions_dir.iterdir():
            if not project_dir.is_dir():
                continue
            
            if project_filter and project_dir.name != project_filter:
                continue
            
            for meta_file in project_dir.glob("*.meta.json"):
                try:
                    with open(meta_file, 'r', encoding='utf-8') as f:
                        meta = json.load(f)
                        meta['meta_file'] = meta_file
                        meta['project_dir'] = project_dir
                        all_sessions.append(meta)
                except Exception as e:
                    print(f"⚠️  读取 {meta_file.name} 失败: {e}")
        
        if not all_sessions:
            print("   (暂无保存的会话)")
            return []
        
        # 按项目和时间分组显示
        sessions_by_project = {}
        for session in all_sessions:
            proj = session.get('project', 'unknown')
            if proj not in sessions_by_project:
                sessions_by_project[proj] = []
            sessions_by_project[proj].append(session)
        
        idx = 1
        all_sessions_ordered = []
        
        for proj, sessions in sessions_by_project.items():
            print(f"\n📁 项目: {proj}")
            print("-" * 70)
            
            sessions.sort(key=lambda x: x['datetime'], reverse=True)
            
            for session in sessions:
                print(f"\n{idx}. 📅 {session['name']}")
                print(f"   时间: {session['datetime'][:19]}")
                print(f"   描述: {session['description']}")
                print(f"   ID: {session['timestamp']}")
                print(f"   大小: {session['size_kb']:.2f} KB")
                
                all_sessions_ordered.append(session)
                idx += 1
        
        print("\n" + "="*70)
        return all_sessions_ordered
    
    def restore_session(self, identifier=None):
        """恢复会话"""
        all_sessions = self.list_sessions()
        
        if not all_sessions:
            return False
        
        current_db, _ = self.find_current_session_db()
        if not current_db:
            print("\n❌ 未找到当前会话数据库")
            print("   请先打开 Cursor 并加载项目")
            return False
        
        # 选择会话
        selected = None
        if identifier:
            # 通过 ID 查找
            for session in all_sessions:
                if session['timestamp'] == identifier:
                    selected = session
                    break
            if not selected:
                print(f"\n❌ 未找到 ID 为 {identifier} 的会话")
                return False
        else:
            # 交互式选择
            try:
                choice = int(input(f"\n请选择要恢复的会话编号 (1-{len(all_sessions)}): "))
                if choice < 1 or choice > len(all_sessions):
                    print("❌ 无效的选择")
                    return False
                selected = all_sessions[choice - 1]
            except (ValueError, KeyboardInterrupt):
                print("\n❌ 操作已取消")
                return False
        
        print("\n" + "="*70)
        print(f"🎯 准备恢复会话")
        print("="*70)
        print(f"  名称: {selected['name']}")
        print(f"  项目: {selected['project']}")
        print(f"  时间: {selected['datetime'][:19]}")
        print(f"  描述: {selected['description']}")
        print("="*70)
        
        # 确认
        confirm = input("\n⚠️  此操作将替换当前会话。是否继续？(yes/no): ").strip().lower()
        if confirm not in ['yes', 'y']:
            print("❌ 已取消")
            return False
        
        # 自动备份当前会话
        print("\n💾 正在自动备份当前会话...")
        self.save_session(
            session_name=f"自动备份_{datetime.now().strftime('%H%M%S')}",
            description="恢复会话前的自动备份"
        )
        
        # 恢复
        backup_file = selected['project_dir'] / selected['db_file']
        if not backup_file.exists():
            print(f"❌ 备份文件不存在: {backup_file}")
            return False
        
        try:
            print(f"\n📋 正在恢复到: {current_db}")
            shutil.copy2(backup_file, current_db)
            
            # 清理 WAL 和 SHM 文件
            for ext in ['-wal', '-shm']:
                extra = Path(str(current_db) + ext)
                if extra.exists():
                    extra.unlink()
            
            print("\n" + "="*70)
            print("✅ 会话恢复成功！")
            print("="*70)
            print("\n📌 下一步操作：")
            print("   1. 关闭 Cursor（如果正在运行）")
            print("   2. 重新打开 Cursor")
            print("   3. 打开相应的项目")
            print("   4. 您将看到恢复后的会话历史")
            print()
            
            return True
            
        except Exception as e:
            print(f"❌ 恢复失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def delete_session(self, identifier):
        """删除指定的会话"""
        all_sessions = self.list_sessions()
        
        selected = None
        for session in all_sessions:
            if session['timestamp'] == identifier:
                selected = session
                break
        
        if not selected:
            print(f"❌ 未找到 ID 为 {identifier} 的会话")
            return False
        
        print(f"\n准备删除会话: {selected['name']}")
        confirm = input("确认删除？(yes/no): ").strip().lower()
        
        if confirm not in ['yes', 'y']:
            print("❌ 已取消")
            return False
        
        # 删除文件
        try:
            for ext in ['.db', '.json', '.meta.json']:
                file_path = selected['project_dir'] / (selected['timestamp'] + '_' + selected['name'] + ext)
                if file_path.exists():
                    file_path.unlink()
            
            print("✅ 会话已删除")
            return True
        except Exception as e:
            print(f"❌ 删除失败: {e}")
            return False

def main():
    manager = CursorSessionManager()
    
    if len(sys.argv) < 2:
        print("\n" + "="*70)
        print("🔧 Cursor Agent 会话管理工具")
        print("="*70)
        print("\n用法:")
        print("  python3 cursor_sessions.py save              - 保存当前会话")
        print("  python3 cursor_sessions.py list              - 列出所有会话")
        print("  python3 cursor_sessions.py restore           - 恢复会话（交互式）")
        print("  python3 cursor_sessions.py restore <ID>      - 恢复指定会话")
        print("  python3 cursor_sessions.py delete <ID>       - 删除指定会话")
        print("\n示例:")
        print("  python3 cursor_sessions.py save")
        print("  python3 cursor_sessions.py list")
        print("  python3 cursor_sessions.py restore 20251025_000709")
        print()
        print(f"💾 会话保存位置: {manager.sessions_dir}")
        print("="*70)
        print()
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    if command == 'save':
        manager.save_session()
    elif command == 'list':
        manager.list_sessions()
    elif command == 'restore':
        identifier = sys.argv[2] if len(sys.argv) > 2 else None
        manager.restore_session(identifier)
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("❌ 请指定要删除的会话 ID")
            sys.exit(1)
        manager.delete_session(sys.argv[2])
    else:
        print(f"❌ 未知命令: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
