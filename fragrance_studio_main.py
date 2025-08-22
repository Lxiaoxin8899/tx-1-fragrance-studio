import sys
import os
import logging
from datetime import datetime

from PyQt6.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QVBoxLayout, 
                             QHBoxLayout, QWidget, QLabel, QMessageBox, QDialog,
                             QProgressBar, QAction, QLineEdit, QMenu, QToolBar)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QPixmap

from qfluentwidgets import NavigationInterface, NavigationItemPosition, FluentIcon

from core.database_manager import DatabaseManager
from core.backup_service import BackupService
from ui.welcome_panel import WelcomePanel
from ui.module_card import ModuleCard
from ui.backup_manager_dialog import BackupManagerDialog
from ui.data_recovery_wizard import DataRecoveryWizard
from ui.base_material_settings_dialog import BaseMaterialSettingsDialog
from ui.device_settings_dialog import DeviceSettingsDialog

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fragrance_studio.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FragranceStudioMain(QMainWindow):
    """调香工作室主窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化数据库管理器
        self.db_manager = None
        
        # 初始化备份服务
        self.backup_service = None
        
        # 初始化模块字典
        self.modules = {}
        self.current_module = None
        
        # 初始化UI
        self.init_ui()
        
        # 初始化数据库和备份服务
        self.init_services()
        
        # 设置窗口
        self.setup_window()
        
        # 设置菜单栏
        self.setup_menu_bar()
        
        # 设置工具栏
        self.setup_tool_bar()
        
        # 设置状态栏
        self.setup_status_bar()
        
        logger.info("调香工作室主窗口初始化完成")
    
    def init_ui(self):
        """初始化用户界面"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建堆叠窗口部件
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # 创建欢迎面板
        self.welcome_panel = WelcomePanel()
        self.stacked_widget.addWidget(self.welcome_panel)
        
        # 连接欢迎面板的信号
        self.welcome_panel.module_selected.connect(self.switch_to_module)
        
        logger.info("UI初始化完成")
    
    def init_services(self):
        """初始化数据库和备份服务"""
        try:
            # 初始化数据库管理器
            self.db_manager = DatabaseManager()
            
            # 初始化备份服务
            self.backup_service = BackupService(self.db_manager)
            
            # 启动自动备份服务
            self.backup_service.start_auto_backup()
            
            logger.info("数据库和备份服务初始化完成")
            
        except Exception as e:
            logger.error(f"初始化服务失败: {e}")
            QMessageBox.critical(self, "错误", f"初始化服务失败: {str(e)}")
    
    def setup_window(self):
        """设置窗口属性"""
        self.setWindowTitle("调香工作室")
        self.resize(1200, 800)
        
        # 设置窗口图标
        try:
            icon_path = os.path.join("resources", "icons", "app_icon.png")
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            logger.warning(f"设置窗口图标失败: {e}")
    
    def setup_modules(self):
        """设置功能模块"""
        try:
            # 专业材料管理模块
            from modules.professional_materials_manager.professional_materials_manager import ProfessionalMaterialsManager
            materials_manager = ProfessionalMaterialsManager(self.db_manager)
            self.modules['materials_manager'] = materials_manager
            self.stacked_widget.addWidget(materials_manager)
            
            logger.info("专业材料管理模块加载完成")
            
        except Exception as e:
            logger.error(f"加载专业材料管理模块失败: {e}")
            # 创建占位符
            placeholder = self.create_module_placeholder("专业材料管理", str(e))
            self.modules['materials_manager'] = placeholder
            self.stacked_widget.addWidget(placeholder)
        
        try:
            # 调香设计器模块
            from modules.fragrance_designer.fragrance_designer import FragranceDesigner
            fragrance_designer = FragranceDesigner(self.db_manager)
            self.modules['fragrance_designer'] = fragrance_designer
            self.stacked_widget.addWidget(fragrance_designer)
            
            logger.info("调香设计器模块加载完成")
            
        except Exception as e:
            logger.error(f"加载调香设计器模块失败: {e}")
            # 创建占位符
            placeholder = self.create_module_placeholder("调香设计器", str(e))
            self.modules['fragrance_designer'] = placeholder
            self.stacked_widget.addWidget(placeholder)
        
        try:
            # 配方管理模块V2
            from modules.recipe_manager_v2.recipe_manager_v2 import RecipeManagerV2
            recipe_manager_v2 = RecipeManagerV2(self.db_manager)
            self.modules['recipe_manager_v2'] = recipe_manager_v2
            self.stacked_widget.addWidget(recipe_manager_v2)
            
            # 连接编辑配方的信号
            recipe_manager_v2.edit_recipe_in_designer.connect(self.edit_recipe_in_designer)
            
            logger.info("配方管理模块V2加载完成")
            
        except Exception as e:
            logger.error(f"加载配方管理模块V2失败: {e}")
            # 创建占位符
            placeholder = self.create_module_placeholder("配方管理V2", str(e))
            self.modules['recipe_manager_v2'] = placeholder
            self.stacked_widget.addWidget(placeholder)
        
        try:
            # 专业数据分析模块
            from modules.professional_data_analyzer.professional_data_analyzer import ProfessionalDataAnalyzer
            professional_data_analyzer = ProfessionalDataAnalyzer(self.db_manager)
            self.modules['professional_data_analyzer'] = professional_data_analyzer
            self.stacked_widget.addWidget(professional_data_analyzer)
            
            logger.info("专业数据分析模块加载完成")
            
        except Exception as e:
            logger.error(f"加载专业数据分析模块失败: {e}")
            # 创建占位符
            placeholder = self.create_module_placeholder("配方分析", str(e))
            self.modules['professional_data_analyzer'] = placeholder
            self.stacked_widget.addWidget(placeholder)
    
    def create_module_placeholder(self, module_name: str, error_message: str = "") -> QWidget:
        """创建模块占位符"""
        placeholder = QWidget()
        layout = QVBoxLayout(placeholder)
        
        label = QLabel(f"{module_name} 模块加载失败")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 16px; color: #dc3545; margin: 20px;")
        layout.addWidget(label)
        
        if error_message:
            error_label = QLabel(f"错误信息: {error_message}")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_label.setStyleSheet("font-size: 12px; color: #6c757d; margin: 10px;")
            layout.addWidget(error_label)
        
        retry_button = QPushButton("重试加载")
        retry_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        retry_button.clicked.connect(lambda: self.setup_modules())
        layout.addWidget(retry_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        return placeholder
    
    def setup_menu_bar(self):
        """设置菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件(&F)')
        
        new_action = QAction('新建(&N)', self)
        file_menu.addAction(new_action)
        
        open_action = QAction('打开(&O)', self)
        file_menu.addAction(open_action)
        
        save_action = QAction('保存(&S)', self)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('退出(&X)', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 模块菜单
        modules_menu = menubar.addMenu('模块(&M)')
        
        materials_action = QAction('材料管理(&M)', self)
        materials_action.triggered.connect(lambda: self.switch_to_module('materials_manager'))
        modules_menu.addAction(materials_action)
        
        designer_action = QAction('调香设计器(&D)', self)
        designer_action.triggered.connect(lambda: self.switch_to_module('fragrance_designer'))
        modules_menu.addAction(designer_action)
        
        recipe_manager_action = QAction('配方管理(&R)', self)
        recipe_manager_action.triggered.connect(lambda: self.switch_to_module('recipe_manager'))
        modules_menu.addAction(recipe_manager_action)
        
        recipe_manager_v2_action = QAction('配方管理V2(&V)', self)
        recipe_manager_v2_action.triggered.connect(lambda: self.switch_to_module('recipe_manager_v2'))
        modules_menu.addAction(recipe_manager_v2_action)
        
        professional_analytics_action = QAction('配方分析(&A)', self)
        professional_analytics_action.triggered.connect(lambda: self.switch_to_module('professional_data_analyzer'))
        modules_menu.addAction(professional_analytics_action)
        
        # 工具菜单
        tools_menu = menubar.addMenu('工具(&T)')
        
        import_action = QAction('导入数据(&I)', self)
        tools_menu.addAction(import_action)
        
        export_action = QAction('导出数据(&E)', self)
        tools_menu.addAction(export_action)
        
        tools_menu.addSeparator()
        
        # 备份相关菜单
        backup_action = QAction('创建备份(&B)', self)
        backup_action.triggered.connect(self.create_manual_backup)
        tools_menu.addAction(backup_action)\极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
        
        backup_manager_action = QAction('备份管理(&M)', self)
        backup_manager_action.triggered.connect极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
(self.show_backup_manager)
        tools_menu.addAction(backup_manager_action)
        
        data_recovery_action = QAction('数据恢复(&R)', self)
        data_recovery_action.triggered.connect(self.show_data_recovery)
极速模式: 已开启极速模式, 剩余极速次数: 0, 极速极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
模式剩余时间: 0秒
        tools_menu.addAction(data_recovery_action)
        
        # 设置菜单
        settings_menu = menubar.addMenu('设置(&S)')
        
        preferences_action = QAction('首选项(&极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
P)', self)
        settings_menu.addAction(preferences_action)
        
        # 设备设置入口
        device_settings_action = QAction('设备设置(&D)', self)
        device_settings_action.triggered.connect(self.show_device_settings)
        settings_menu.addAction(device_settings_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助(&H)')
        
        about极速模式: 已开启极速模式, 极速模式剩余时间: 0秒
_action = QAction('关于(&A)', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_tool_bar(self):
        """设置工具栏"""
        toolbar = self.addToolBar('主工具栏')
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        
        # 主页按钮
        home_action = QAction('主页', self)
        home_action.setToolTip('返回主页')
        home_action.triggered.connect(self.show_welcome)\极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
        toolbar.addAction(home极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
时间: 0秒
_action)
        
        toolbar.addSeparator()
        
        # 快速访问按钮
        quick_actions = [
            ('调香设计', 'fragrance_designer', '打开调香设计器'),
            ('材料管理', 'materials_manager', '打开材料管理'),
            ('配方管理', 'recipe_manager', '打开配方管理'),
            ('配方管理V2', 'recipe_manager_v2', '打开配方管理V2'),
            ('配方分析', 'professional_data_analy极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
zer', '打开配方分析')
        ]
        
        for text, module_id, tooltip in quick_actions:
            action = QAction(text, self)
            action.setToolTip(tooltip)
            action.triggered.connect(lambda checked, m=module_id: self.switch_to_module(m))
            toolbar.addAction(action)
            
        toolbar.addSeparator()
        
        # 搜索框
        search_widget = QLineEdit()
        search_widget.setPlaceholderText('搜索配方、材料...')
        search_widget.setFixedWidth(200)
        search_widget.setStyleSheet("""
            QLineEdit {
                padding: 6px 12px;
                border: 1px solid #ced4da;
                border-radius: 4px;\极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #007bff;
                outline: none;
            }
        """)
        toolbar.addWidget(search_widget)
        
    def setup_status_bar(self):
        """设置状态栏"""极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
        status_bar = self.statusBar()
        
       极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
# 当前模块标签
        self.current_module_label = QLabel('当前模块: 主页')
        status_bar.addWidget(self.current_module_label)
        
        status_bar.addPermanentWidget(QLabel('|'))
        
        # 系统状态
        self.system_status_label = QLabel('系统状态: 就绪')
        status_bar.addPermanentWidget(self.system_status_label)
        
        status_bar.addPermanentWidget(QLabel('|'))
        
        # 时间显示
        self.time_label = QLabel()
        status_bar.addPermanentWidget(self.time_label)
       极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
        
        # 定时更新时间
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self极速模式: 已开启极速极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
.timer.start(1000)
        self.update_time()
        
    def update_time(self):
        """更新时间显示"""
        from datetime import datetime
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.time_label.setText(current_time)
        
    def switch_to_module(self, module_id: str):
        """切换到指定模块"""
        if module_id in self.modules:
            widget = self.modules[module_id]
            self.stacked_widget.setCurrentWidget(widget)
            self.current_module = module_id
            
            # 更新状态栏
            module_names = {
                'fragrance_designer': '调香设计器',
                'materials_manager': '材料管理',
                'recipe_manager': '专业配方管理',
                'recipe_manager_v2': '配方管理V极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
2',
                'professional_data_analyzer': '配方分析'
            }
            
            module_name = module_names.get(module_id, module_id)
            self.current_module_label.setText(f'当前模块: {module_name}')
            self.system_status_label.setText('系统状态: 运行中')
        else:
            QMessageBox.warning(self, '警告', f'模块 "{module_id}" 未找到或未加载')
            
    def show_welcome(self):
        """显示欢迎页面"""
        self.stacked_widget.setCurrentWidget(self.welcome_panel)\极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
        self.current_module = None
        self.current_module_label.setText('当前模块: 主页')
        self.system_status_label.setText('系统状态: 就绪')
        
    def show_about(self):
        """显示关于对话框"""
        about_text = """
        <h2>调香工作室 v1.0</h2>
        <p>专业香精调配与配方管理系统</p>
        <p><b>主要功能:</b></p>
        <ul>
            <li>专业调香设计器</li>
            <li>香精材料管理</li>
            <li>配方设计与版本控制</li>
            <li>数据分析与报表</li>
        </ul>
        <p><b>技术特性:</b></p>
       极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
<ul>
            <li>极速模式: 已开启极速模式, 剩余极速次数: 极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
0, 极速模式剩余时间: 极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
0秒
模块化架构设计</li>
            <li>现代化用户界面</li>
            <li>专业数据分析</极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
li>
            <li>智能推荐算法</li>
        </ul>
        <p>© 2024 调香工作室. 保留所有权利.</p>
        """
        
        QMessageBox.about(self, '关于调香工作室', about_text)
    
    def create_manual_backup(self):
        """创建手动备份"""
        if not self.backup_service:
            QMessageBox.warning(self, '警告', '备份服务未初始化，无法创建备份')
            return
        
        try:
            # 显示进度对话框
            self.backup_progress_dialog = QDialog(self)
            self.backup极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
_progress_dialog.setWindowTitle('创建备份')
            self.backup_progress_dialog.setFixedSize(350, 120)
            self.backup_progress_dialog.setModal(True)
            
            layout = QVBoxLayout(self.backup_progress_dialog)
            layout.addWidget(QLabel('正在创建备份，请稍候...'))
            
            progress = QProgressBar()
            progress.setRange(0, 0)  # 不确定进度
            layout.addWidget(progress)
            
            # 连接备份服务的信号
            self.backup_service.backup_completed.connect(self.on_backup_completed)
            self.backup_service.back极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
up_failed.connect(self.on_backup_failed)
            
            # 启动异步备份
            self.backup_progress_dialog.show()
            
            # 使用信号槽机制异步创建备份
            QTimer.singleShot(100, lambda: self.backup_service.create_manual_backup("手动备份"))
                
        except Exception as e:
            if hasattr(self, 'backup_progress_dialog'):
                self.backup_progress_dialog.close()
            QMessageBox.critical(self, '错误', f'创建备份时发生错误：{str(e)}')
    
    def on_backup_completed(self, backup_path, success):
        """备份完成回调"""
        if hasattr(self, '极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
backup_progress_dialog'):
            self.backup_progress极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
_dialog.close()
        
        # 断开信号连接极速模式: 极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
        self.backup_service.backup_completed.disconnect(self.on_backup_completed)
        self.backup_service.backup_failed.disconnect(self.on_backup_failed)
        
        if success:
            QMessageBox.information(self, '成功', f'备份创建成功！\n备份文件：{backup_path}')
            self.system_status_label.setText('系统状态: 备份完成')
        else:
            QMessageBox.warning(self, '失败', '备份创建失败，请检查系统日志')
    
    def on_backup极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
_failed(self, error_message):
        """备份失败回调"""\极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
        if hasattr(self, 'backup_progress_dialog'):
            self.backup_progress_dialog.close()
        
        # 断开信号连接
        self.backup_service.backup_completed.disconnect(self.on_backup_completed)
        self.backup_service.backup_failed.disconnect(self.on_backup_failed)
        
        QMessageBox.critical(self, '错误', f'创建备份失败：{error_message}')
    
    def show_backup_manager(self):
        """显示备份管理对话框"""
        if not self.backup_service:
            QMessageBox.warning(self, '警告', '备份服务未初始化，无法打开备份管理')
            return
        
        try:
            # 传入 db_manager 与 backup_service
            dialog = BackupManagerDialog(self.db_manager, self.backup_service, self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, '错误', f'极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 极速模式: 已开启极速模式, 剩余极极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
速次数: 0, 极速模式剩余时间: 0秒
0秒
打开备份管理失败：{str(e)}')
    
    def show_data_recovery(self):
        """显示数据恢复向导"""
        if not self.backup_service:
            QMessageBox.warning(self, '警告', '备份服务未初始化，无法进行数据恢复')
            return
        
        try:
            wizard = DataRecoveryWizard(self.backup_service, self)\极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
            wizard.exec()
        except Exception as e:
            QMessageBox.critical(self, '错误', f'打开数据恢复向导失败：{str(e)}')
    
    def show_base_material_settings极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
(self):
        """显示基础材料设置对话框"""
        dialog = BaseMaterialSettingsDialog(self)
        dialog.exec()
    
    def show_device_settings(self):
        """显示设备设置对话框"""
        if not hasattr(self, 'db_manager') or self.db_manager is None:
            QMessageBox.warning(self, '错误', '数据库未初始化，无法打开设备设置')
            return
        try:
            dialog = DeviceSettingsDialog(self.db_manager, self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, '错误', f'打开设备设置失败：{str(e)}')
        
    def closeEvent(self, event):
        """关闭事件处理"""
        reply = QMessageBox.question(
            self, '确认退出', 
            '确定要退出调香工作室吗？\n未保存的数据可能会丢失。',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 停止自动极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
备份服务
            if hasattr(self, 'backup_service') and self.backup_service:
                try:
                    self.backup_service.stop_auto_backup()
                    print("自动备份服务已停止")
                except Exception as e:
                    print(f"停止备份服务失败: {e}")
            
            # 保存应用状态
            self.save_application_state()
            event.accept()
        else:\极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
            event.ignore()
            
    def save_application_state(self):
        """保存应用程序状态"""
        # 这里可以添加保存窗口大小、位置、当前模块等状态的代码
        pass
    
    def edit_recipe_in_designer(self, recipe_data):
        """在调香设计器中编辑配方"""
        try:
            # 切换到调香设计器模块
            self.switch_to_module('fragrance_designer')
            
            # 如果调香设计器存在，将配方数据传递给它
            if 'fragrance_designer' in self.modules:
                fragrance_designer = self.modules['f极速模式: 已开启极速模式, 剩余极速次数: 0, 极速模式剩余时间: 0秒
ragrance_designer']
                
                # 检查调香设计器是否有加载配方的方法
                if hasattr(fragrance_designer, 'load_recipe_for_editing'):
                    fragrance_designer.load_recipe_for_editing(recipe_data)
                elif hasattr(fragrance_designer, 'formula_designer') and hasattr(fragrance_designer.formula_designer, 'load_recipe_for_editing'):
                    fragrance_designer.formula_designer.load_recipe_for_editing(recipe_data)
                else:
                    # 如果没有专门的加载方法，显示提示信息
                    QMessageBox.information(self, "提示", f"已切换到调香设计器\n配方名称: {recipe_data.get('name', '未知配方')}\n请手动加载配方数据")
                
                # 更新状态栏
                self.statusBar().showMessage(f"正在编辑配方: {recipe_data.get('name', '未知配方')}", 3000)
            else:
                QMessageBox.warning(self, "错误", "调香设计器模块未加载")
                
        except Exception as e:
            QMessageBox.warning(self, "错误", f"切换到调香设计器失败: {str(e)}")
            import traceback
            traceback.print_exc()





# 移除重复入口：统一由根目录 main.py 启动