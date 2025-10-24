#!/usr/bin/env python3
"""
Cursor Session Manager - Web API Backend
提供 RESTful API 用于管理 Cursor 会话
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path
import shutil
import uvicorn

app = FastAPI(title="Cursor Session Manager API")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置路径
CURSOR_DIR = Path.home() / ".cursor"
SESSIONS_DIR = Path.home() / "cursor-session-manager" / "saved_sessions"
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

# 数据模型
class SessionInfo(BaseModel):
    id: str
    name: str
    description: str
    project: str
    datetime: str
    size_kb: float
    db_file: str

class SessionRename(BaseModel):
    new_name: str
    new_description: Optional[str] = None

class SessionSave(BaseModel):
    name: str
    description: str

# 工具函数
def find_current_session_db():
    """查找当前活跃的会话数据库"""
    chats_dir = CURSOR_DIR / "chats"
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

def get_current_project():
    """获取当前项目名称"""
    projects_dir = CURSOR_DIR / "projects"
    if not projects_dir.exists():
        return "unknown"
    
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
    
    return latest_project or "unknown"

def export_db_to_json(db_path, json_file):
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
        return True
    except Exception as e:
        print(f"Export error: {e}")
        return False

# API 端点
@app.get("/api")
async def root():
    return {
        "status": "running",
        "message": "Cursor Session Manager API",
        "version": "1.0.0"
    }

@app.get("/api/sessions", response_model=List[SessionInfo])
async def list_sessions(project: Optional[str] = None):
    """获取所有保存的会话"""
    all_sessions = []
    
    for project_dir in SESSIONS_DIR.iterdir():
        if not project_dir.is_dir():
            continue
        
        if project and project_dir.name != project:
            continue
        
        for meta_file in project_dir.glob("*.meta.json"):
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                    session = SessionInfo(
                        id=meta['timestamp'],
                        name=meta['name'],
                        description=meta['description'],
                        project=meta['project'],
                        datetime=meta['datetime'],
                        size_kb=meta['size_kb'],
                        db_file=str(project_dir / meta['db_file'])
                    )
                    all_sessions.append(session)
            except Exception as e:
                print(f"Error reading {meta_file}: {e}")
    
    # 按时间倒序排列
    all_sessions.sort(key=lambda x: x.datetime, reverse=True)
    return all_sessions

@app.post("/api/sessions/auto-save")
async def auto_save_session(max_keep: int = 3):
    """自动保存当前会话"""
    current_db, hash_folder = find_current_session_db()
    
    if not current_db or not current_db.exists():
        raise HTTPException(status_code=404, detail="未找到当前会话数据库")
    
    project_name = get_current_project()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 智能检测会话是否有变化（避免重复保存）
    project_sessions_dir = SESSIONS_DIR / project_name
    project_sessions_dir.mkdir(exist_ok=True)
    
    recent_sessions = sorted(project_sessions_dir.glob("*.meta.json"), 
                            key=lambda x: x.stat().st_mtime, reverse=True)
    
    if recent_sessions:
        latest_meta = recent_sessions[0]
        try:
            with open(latest_meta, 'r', encoding='utf-8') as f:
                latest_data = json.load(f)
            
            current_size = current_db.stat().st_size / 1024
            size_diff = abs(current_size - latest_data.get('size_kb', 0))
            
            # 检查会话是否真正有变化
            # 1. 大小差异小于 1KB 表示可能无变化
            # 2. 读取数据库内容进行更精确的对比
            if size_diff < 1:
                # 读取数据库内容进行对比
                latest_db_path = project_sessions_dir / latest_data['db_file']
                if latest_db_path.exists():
                    try:
                        # 对比数据库文件的 MD5 或内容
                        import hashlib
                        
                        def get_db_hash(db_path):
                            with open(db_path, 'rb') as f:
                                return hashlib.md5(f.read()).hexdigest()
                        
                        current_hash = get_db_hash(current_db)
                        latest_hash = get_db_hash(latest_db_path)
                        
                        if current_hash == latest_hash:
                            return {
                                "status": "skipped",
                                "message": "会话内容无变化，跳过保存",
                                "session_id": latest_data['timestamp']
                            }
                    except:
                        # 如果对比失败，继续保存
                        pass
        except:
            pass
    
    # 生成自动保存的会话名称（包含项目名称）
    # 将项目名中的连字符和下划线替换为空格，使其更易读
    readable_project = project_name.replace('-', ' ').replace('_', ' ').replace('home neo upload', '').strip()
    session_name = f"{readable_project} - {datetime.now().strftime('%m月%d日 %H:%M')}"
    description = f"自动保存于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # 创建安全的文件名
    base_name = f"{timestamp}_自动保存"
    
    # 创建项目目录
    project_sessions_dir.mkdir(exist_ok=True)
    
    # 保存数据库
    backup_file = project_sessions_dir / f"{base_name}.db"
    shutil.copy2(current_db, backup_file)
    
    # 导出 JSON
    json_file = project_sessions_dir / f"{base_name}.json"
    export_db_to_json(current_db, json_file)
    
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
        'original_path': str(current_db),
        'auto_saved': True
    }
    
    meta_file = project_sessions_dir / f"{base_name}.meta.json"
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    # 清理旧的自动保存（只保留最近的 max_keep 个）
    cleanup_old_auto_saves(project_sessions_dir, max_keep)
    
    return {
        "status": "success",
        "message": "自动保存成功",
        "session_id": timestamp,
        "name": session_name
    }

def cleanup_old_auto_saves(project_dir: Path, max_keep: int):
    """清理旧的自动保存，只保留最近的 max_keep 个
    
    Args:
        project_dir: 项目会话目录
        max_keep: 保留的自动保存数量
    """
    try:
        # 获取所有自动保存的会话
        auto_save_sessions = []
        for meta_file in project_dir.glob("*.meta.json"):
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    # 只处理自动保存的会话
                    if metadata.get('auto_saved', False):
                        auto_save_sessions.append({
                            'meta_file': meta_file,
                            'metadata': metadata,
                            'mtime': meta_file.stat().st_mtime
                        })
            except:
                continue
        
        # 按时间倒序排列
        auto_save_sessions.sort(key=lambda x: x['mtime'], reverse=True)
        
        # 删除超出数量的旧会话
        if len(auto_save_sessions) > max_keep:
            for session in auto_save_sessions[max_keep:]:
                try:
                    # 删除 meta.json
                    session['meta_file'].unlink()
                    
                    # 删除 .db 文件
                    db_file = project_dir / session['metadata']['db_file']
                    if db_file.exists():
                        db_file.unlink()
                    
                    # 删除 .json 文件
                    json_file = project_dir / session['metadata']['json_file']
                    if json_file.exists():
                        json_file.unlink()
                    
                    print(f"已清理旧会话: {session['metadata']['name']}")
                except Exception as e:
                    print(f"清理会话失败: {e}")
    except Exception as e:
        print(f"清理旧会话时出错: {e}")

@app.post("/api/sessions/save")
async def save_session(session_save: SessionSave):
    """手动保存当前会话"""
    current_db, hash_folder = find_current_session_db()
    
    if not current_db or not current_db.exists():
        raise HTTPException(status_code=404, detail="未找到当前会话数据库")
    
    project_name = get_current_project()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 创建安全的文件名
    safe_name = "".join(c for c in session_save.name if c.isalnum() or c in (' ', '-', '_', '中', '文')).strip()
    safe_name = safe_name.replace(' ', '_')[:50]
    base_name = f"{timestamp}_{safe_name}"
    
    # 创建项目目录
    project_sessions_dir = SESSIONS_DIR / project_name
    project_sessions_dir.mkdir(exist_ok=True)
    
    # 保存数据库
    backup_file = project_sessions_dir / f"{base_name}.db"
    shutil.copy2(current_db, backup_file)
    
    # 导出 JSON
    json_file = project_sessions_dir / f"{base_name}.json"
    export_db_to_json(current_db, json_file)
    
    # 保存元数据
    metadata = {
        'name': session_save.name,
        'description': session_save.description,
        'timestamp': timestamp,
        'datetime': datetime.now().isoformat(),
        'project': project_name,
        'hash_folder': hash_folder,
        'db_file': backup_file.name,
        'json_file': json_file.name,
        'size_kb': current_db.stat().st_size / 1024,
        'original_path': str(current_db),
        'auto_saved': False
    }
    
    meta_file = project_sessions_dir / f"{base_name}.meta.json"
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    return {
        "status": "success",
        "message": "会话保存成功",
        "session_id": timestamp,
        "name": session_save.name
    }

@app.post("/api/sessions/{session_id}/restore")
async def restore_session(session_id: str):
    """恢复指定的会话"""
    # 查找会话
    session_meta = None
    session_file = None
    
    for project_dir in SESSIONS_DIR.iterdir():
        if not project_dir.is_dir():
            continue
        
        for meta_file in project_dir.glob(f"{session_id}_*.meta.json"):
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    session_meta = json.load(f)
                    session_file = project_dir / session_meta['db_file']
                    break
            except:
                continue
        
        if session_meta:
            break
    
    if not session_meta or not session_file.exists():
        raise HTTPException(status_code=404, detail="会话不存在")
    
    # 查找当前数据库
    current_db, _ = find_current_session_db()
    if not current_db:
        raise HTTPException(status_code=404, detail="未找到当前会话数据库")
    
    # 先备份当前会话
    backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    auto_backup_name = f"自动备份_{backup_timestamp}"
    
    await save_session(SessionSave(
        name=auto_backup_name,
        description="恢复会话前的自动备份"
    ))
    
    # 恢复会话
    try:
        shutil.copy2(session_file, current_db)
        
        # 清理 WAL 和 SHM 文件
        for ext in ['-wal', '-shm']:
            extra = Path(str(current_db) + ext)
            if extra.exists():
                extra.unlink()
        
        return {
            "status": "success",
            "message": "会话恢复成功，请重启 Cursor",
            "session_name": session_meta['name']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"恢复失败: {str(e)}")

@app.put("/api/sessions/{session_id}/rename")
async def rename_session(session_id: str, rename_data: SessionRename):
    """重命名会话"""
    # 查找会话元数据文件
    meta_file_path = None
    
    for project_dir in SESSIONS_DIR.iterdir():
        if not project_dir.is_dir():
            continue
        
        for meta_file in project_dir.glob(f"{session_id}_*.meta.json"):
            meta_file_path = meta_file
            break
        
        if meta_file_path:
            break
    
    if not meta_file_path:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    # 读取并更新元数据
    try:
        with open(meta_file_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        metadata['name'] = rename_data.new_name
        if rename_data.new_description:
            metadata['description'] = rename_data.new_description
        
        with open(meta_file_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return {
            "status": "success",
            "message": "会话已重命名",
            "new_name": rename_data.new_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"重命名失败: {str(e)}")

@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """删除会话"""
    deleted = False
    
    for project_dir in SESSIONS_DIR.iterdir():
        if not project_dir.is_dir():
            continue
        
        for file_pattern in [f"{session_id}_*.db", f"{session_id}_*.json", f"{session_id}_*.meta.json"]:
            for file_path in project_dir.glob(file_pattern):
                try:
                    file_path.unlink()
                    deleted = True
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
    
    if not deleted:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    return {"status": "success", "message": "会话已删除"}

@app.get("/api/status")
async def get_status():
    """获取系统状态"""
    current_db, _ = find_current_session_db()
    project = get_current_project()
    
    status = {
        "cursor_running": current_db is not None,
        "current_project": project,
        "sessions_count": len(list(SESSIONS_DIR.rglob("*.meta.json"))),
        "sessions_dir": str(SESSIONS_DIR)
    }
    
    if current_db:
        status["current_session"] = {
            "size_kb": current_db.stat().st_size / 1024,
            "last_modified": datetime.fromtimestamp(current_db.stat().st_mtime).isoformat()
        }
    
    return status

@app.get("/api/projects")
async def list_projects():
    """获取所有项目列表"""
    projects = []
    
    for project_dir in SESSIONS_DIR.iterdir():
        if project_dir.is_dir():
            session_count = len(list(project_dir.glob("*.meta.json")))
            projects.append({
                "name": project_dir.name,
                "sessions_count": session_count
            })
    
    return projects

# 挂载静态文件（前端）
app.mount("/", StaticFiles(directory="/app/frontend", html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
