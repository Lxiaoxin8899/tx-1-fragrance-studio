#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库管理模块 - 负责SQLite数据库的连接、版本迁移和数据操作
"""

import sqlite3
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime


class DatabaseManager:
    """数据库管理类"""
    
    def __init__(self, db_path: str = 'database/db_files/flavor_lab.db'):
        self.db_path = db_path
        self.connection = None
        self.logger = logging.getLogger(__name__)
        self._ensure_database()
    
    def _ensure_database(self) -> None:
        """确保数据库文件和目录存在"""
        db_file = Path(self.db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not db_file.exists():
            self.logger.info(f"创建新的数据库文件: {self.db_path}")
            self._create_tables()
        else:
            self.logger.info(f"使用现有数据库文件: {self.db_path}")
    
    def connect(self) -> sqlite3.Connection:
        """连接到数据库"""
        if self.connection is None:
            self.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                isolation_level=None
            )
            self.connection.row_factory = sqlite3.Row
            self._enable_foreign_keys()
        return self.connection
    
    def _enable_foreign_keys(self) -> None:
        """启用外键约束"""
        with self.connect() as conn:
            conn.execute('PRAGMA foreign_keys = ON')
    
    def _create_tables(self) -> None:
        """创建数据库表结构"""
        with self.connect() as conn:
            # 材料表
            conn.execute('''
                CREATE TABLE materials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    category TEXT NOT NULL,
                    description TEXT,
                    price_per_ml REAL DEFAULT 0.0,
                    density REAL DEFAULT 1.0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 配方表
            conn.execute('''
                CREATE TABLE recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    version INTEGER DEFAULT 1,
                    parent_recipe_id INTEGER,
                    description TEXT,
                    total_volume_ml REAL DEFAULT 0.0,
                    nicotine_strength_mg REAL DEFAULT 0.0,
                    pg_ratio REAL DEFAULT 0.0,
                    vg_ratio REAL DEFAULT 0.0,
                    flavor_ratio REAL DEFAULT 0.0,
                    designer_name TEXT,
                    customer_name TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (parent_recipe_id) REFERENCES recipes (id)
                )
            ''')
            
            # 配方组成表
            conn.execute('''
                CREATE TABLE recipe_compositions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipe_id INTEGER NOT NULL,
                    material_id INTEGER NOT NULL,
                    percentage REAL NOT NULL,
                    weight_grams REAL DEFAULT 0.0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE,
                    FOREIGN KEY (material_id) REFERENCES materials (id)
                )
            ''')
            
            # 版本历史表
            conn.execute('''
                CREATE TABLE version_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipe_id INTEGER NOT NULL,
                    version INTEGER NOT NULL,
                    change_type TEXT NOT NULL,
                    change_description TEXT,
                    created_by TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
                )
            ''')
            
            self.logger.info("数据库表结构创建完成")
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """执行查询并返回结果"""
        try:
            with self.connect() as conn:
                cursor = conn.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            self.logger.error(f"数据库查询错误: {e}")
            raise
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """执行更新操作并返回影响的行数"""
        try:
            with self.connect() as conn:
                cursor = conn.execute(query, params)
                conn.commit()
                return cursor.rowcount
        except sqlite3.Error as e:
            self.logger.error(f"数据库更新错误: {e}")
            raise
    
    def close(self) -> None:
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.logger.info("数据库连接已关闭")


# 全局数据库管理器实例
db_manager = DatabaseManager()