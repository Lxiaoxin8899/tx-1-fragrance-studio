# 项目结构说明

## 核心文件
- `main.py` - 应用主入口
- `fragrance_studio_main.py` - 主界面类
- `requirements.txt` - 项目依赖
- `run.bat` - Windows启动脚本

## 核心模块
- `core/` - 核心业务逻辑
  - `recipe_edit_session.py` - 配方编辑会话管理
  - `recipe_export_processor.py` - 配方导出处理器
  - `recipe_version_manager.py` - 配方版本管理
- `database/` - 数据库管理
  - `database_manager.py` - 数据库管理器
  - `version_migration_v2.py` - 版本迁移脚本
- `models/` - 数据模型
  - `material.py` - 材料模型
  - `recipe.py` - 配方模型
- `services/` - 服务层
  - `auto_backup_service.py` - 自动备份服务
  - `backup_worker.py` - 备份工作器
  - `material_service.py` - 材料服务
  - `recipe_analyzer.py` - 配方分析器
- `ui/` - 用户界面
  - `fragrance_designer.py` - 调香设计器界面
  - `backup_manager_dialog.py` - 备份管理对话框
  - `data_recovery_wizard.py` - 数据恢复向导
  - `version_history_widget.py` - 版本历史组件
- `utils/` - 工具函数
  - `data_import_export.py` - 数据导入导出工具

## 数据文件
- `data/` - 配方数据文件（JSON格式）
- `backups/` - 备份文件目录
  - `auto/` - 自动备份
  - `emergency/` - 紧急备份
  - `manual/` - 手动备份
- `logs/` - 应用日志

## 资源配置
- `resources/` - 资源文件
  - `icons/` - 图标资源
  - `fonts/` - 字体文件
  - `styles.qss` - 样式表

## 配置文档
- `config/` - 配置文件
  - `project_config.py` - 项目配置
  - 各种配置数据文件

## 文档目录
- `docs/` - 项目文档
  - 功能说明文档
  - 设计文档
  - 使用指南

## 测试相关
- `tests/` - 单元测试
- `test_*.py` - 功能测试脚本