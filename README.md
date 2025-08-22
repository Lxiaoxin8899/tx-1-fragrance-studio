# Flavor Lab Pro - 电子烟雾化物配方设计工具

## 项目简介

Flavor Lab Pro 是一款专业的电子烟雾化物配方设计工具，专为调香师和电子烟油设计师开发。提供完整的配方管理、版本控制、智能分析和批量导出功能。

## 主要功能

### 核心功能
- 🎯 **专业配方管理** - 完整的配方创建、编辑、版本控制
- 🔄 **版本历史追踪** - 详细的变更记录和版本对比
- 📊 **智能分析系统** - 香调平衡、持久性、成本分析
- 💾 **数据备份恢复** - 自动备份和紧急恢复功能
- 📤 **多格式导出** - JSON、Excel、分析报告导出

### 特色功能
- 🎨 **现代化UI界面** - 基于PyQt6的现代化设计
- 🎛️ **实时数据验证** - 配方比例自动验证和警告
- 🔍 **高级筛选搜索** - 多条件配方筛选和搜索
- 📈 **统计报表** - 配方统计和成本分析报表
- 🛡️ **数据安全** - 完善的备份和恢复机制

## 技术栈

- **编程语言**: Python 3.8+
- **GUI框架**: PyQt6
- **数据库**: SQLite3
- **数据分析**: Pandas, NumPy
- **样式主题**: QDarkStyle, Qt-Material
- **构建工具**: setuptools

## 项目结构

```
tx-1-fragrance-studio/
├── config/                 # 配置文件
│   ├── project_config.py   # 项目配置管理
│   └── compliance_test_data.json
├── core/                   # 核心业务逻辑
│   ├── professional_recipe_manager.py  # 专业配方管理器
│   ├── recipe_edit_session.py         # 配方编辑会话
│   ├── recipe_export_processor.py     # 配方导出处理器
│   └── recipe_version_manager.py      # 配方版本管理器
├── database/               # 数据库管理
│   ├── database_manager.py # 数据库管理器
│   └── db_files/           # 数据库文件
├── models/                 # 数据模型
│   ├── material.py        # 材料模型
│   └── recipe.py          # 配方模型
├── services/              # 服务层
│   ├── auto_backup_service.py  # 自动备份服务
│   ├── material_service.py    # 材料服务
│   └── recipe_analyzer.py     # 配方分析器
├── utils/                  # 工具类
│   └── data_import_export.py # 数据导入导出工具
├── main.py                # 主入口文件
└── requirements.txt       # 依赖包列表
```

## 安装和运行

### 环境要求
- Python 3.8 或更高版本
- pip 包管理工具

### 安装步骤

1. 克隆项目代码
```bash
git clone https://github.com/Lxiaoxin8899/tx-1-fragrance-studio.git
cd tx-1-fragrance-studio
```

2. 安装依赖包
```bash
pip install -r requirements.txt
```

3. 运行应用程序
```bash
python main.py
```

或者使用提供的批处理文件：
```bash
run.bat
```

### 开发环境设置

1. 创建虚拟环境（推荐）
```bash
python -m venv .venv
```

2. 激活虚拟环境
- Windows:
```bash
.venv\Scripts\activate
```
- Linux/Mac:
```bash
source .venv/bin/activate
```

3. 安装开发依赖
```bash
pip install -r requirements.txt
```

## 使用说明

### 基本操作

1. **创建新配方**: 点击"新建配方"按钮，填写基本信息
2. **编辑配方**: 选择配方后点击"编辑"按钮进入编辑模式
3. **版本管理**: 在配方详情中查看和管理版本历史
4. **导出配方**: 右键菜单选择导出格式（JSON/Excel）
5. **分析配方**: 点击"分析"按钮查看智能分析报告

### 高级功能

- **批量操作**: 支持多选配方进行批量导出或删除
- **筛选搜索**: 使用顶部筛选栏快速定位配方
- **数据备份**: 自动定时备份，支持手动备份和恢复
- **成本分析**: 实时计算配方成本和材料占比

## 配置说明

项目配置存储在 `config/project_config.json` 文件中，主要配置项包括：

- **数据库设置**: 数据库路径、备份间隔等
- **界面设置**: 主题、字体、动画效果等
- **备份设置**: 自动备份频率、最大备份数等
- **导出设置**: 默认格式、包含内容等

## 开发指南

### 代码规范

- 遵循 PEP8 编码规范
- 使用类型注解（Type Hints）
- 模块化设计，高内聚低耦合
- 详细的文档注释

### 扩展开发

1. **添加新功能**: 在相应的模块中添加新类或方法
2. **修改界面**: 更新对应的UI文件或代码
3. **数据库变更**: 使用版本迁移工具更新数据库结构
4. **添加分析规则**: 在 `recipe_analyzer.py` 中添加新的分析逻辑

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 支持

如有问题或建议，请通过以下方式联系：
- 创建 GitHub Issue
- 发送邮件到项目维护者

## 版本历史

- **v2.0.0** (当前版本) - 现代化UI升级，增强版本管理功能
- **v1.0.0** - 初始版本，基础配方管理功能

---

**注意**: 本项目仅供电子烟雾化物配方设计和研究使用，请遵守相关法律法规。