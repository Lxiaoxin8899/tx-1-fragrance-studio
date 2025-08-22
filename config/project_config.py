#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目配置文件管理
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class ProjectConfig:
    """项目配置管理类"""
    
    def __init__(self, config_file: str = 'config/project_config.json'):
        self.config_file = config_file
        self.config: Dict[str, Any] = self._load_default_config()
        self._load_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """加载默认配置"""
        return {
            'database': {
                'path': 'database/db_files/flavor_lab.db',
                'backup_interval': 3600,  # 1小时
                'max_backups': 10
            },
            'ui': {
                'stylesheet_enabled': True,
                'theme': 'light',
                'font_size': 10,
                'animation_enabled': True
            },
            'backup': {
                'auto_backup': True,
                'backup_interval': 1800,  # 30分钟
                'max_auto_backups': 20,
                'backup_path': 'backups/auto'
            },
            'export': {
                'default_format': 'json',
                'include_version_history': True,
                'include_analysis_data': True
            },
            'analysis': {
                'cost_calculation_enabled': True,
                'flavor_balance_analysis': True,
                'persistence_prediction': True
            }
        }
    
    def _load_config(self) -> None:
        """从文件加载配置"""
        config_path = Path(self.config_file)
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    self._merge_configs(loaded_config)
            except (json.JSONDecodeError, IOError):
                pass  # 使用默认配置
    
    def _merge_configs(self, new_config: Dict[str, Any]) -> None:
        """合并配置"""
        def merge_dicts(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    base[key] = merge_dicts(base[key], value)
                else:
                    base[key] = value
            return base
        
        self.config = merge_dicts(self.config, new_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('/')
        current = self.config
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        
        return current
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值"""
        keys = key.split('/')
        current = self.config
        
        for i, k in enumerate(keys[:-1]):
            if k not in current or not isinstance(current[k], dict):
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
        self._save_config()
    
    def _save_config(self) -> None:
        """保存配置到文件"""
        config_path = Path(self.config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except IOError:
            pass  # 忽略保存错误


# 全局配置实例
config = ProjectConfig()