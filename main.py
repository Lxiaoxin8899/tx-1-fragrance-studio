#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电子烟雾化物配方设计工具 - 主入口文件
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from config.project_config import ProjectConfig
from core.professional_recipe_manager import ProfessionalRecipeManager
from services.auto_backup_service import AutoBackupService
from utils.logging_setup import setup_logging


def main():
    """应用程序主函数"""
    # 设置日志
    setup_logging()
    
    # 创建应用实例
    app = QApplication(sys.argv)
    app.setApplicationName("Flavor Lab Pro")
    app.setApplicationVersion("2.0.0")
    
    # 加载配置
    config = ProjectConfig()
    
    # 设置应用样式
    if config.get('ui/stylesheet_enabled', True):
        stylesheet_path = os.path.join('resources', 'styles.qss')
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, 'r', encoding='utf-8') as f:
                app.setStyleSheet(f.read())
    
    # 创建主窗口
    main_window = ProfessionalRecipeManager()
    main_window.show()
    
    # 启动自动备份服务
    backup_service = AutoBackupService()
    backup_service.start()
    
    # 运行应用
    exit_code = app.exec()
    
    # 停止备份服务
    backup_service.stop()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()