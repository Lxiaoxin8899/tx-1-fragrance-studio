import sys
import os
import logging
from logging.handlers import RotatingFileHandler

# 将项目根目录添加到 sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from fragrance_studio_main import FragranceStudioMain
from config.project_config import LOGGING_CONFIG, ensure_directory_exists, get_absolute_path

# 可选引入 QFluentWidgets 统一主题（暗/亮切换）
try:
    from qfluentwidgets import setTheme, Theme, setThemeColor
    _HAS_QFLUENT = True
except Exception:
    _HAS_QFLUENT = False

def _setup_logging() -> None:
    """初始化应用日志系统。"""
    ensure_directory_exists(LOGGING_CONFIG['log_dir'])
    log_path = os.path.join(get_absolute_path(LOGGING_CONFIG['log_dir']), 'app.log')

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, LOGGING_CONFIG.get('log_level', 'INFO')))

    formatter = logging.Formatter(LOGGING_CONFIG.get('log_format'))
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=LOGGING_CONFIG.get('max_log_size', 10 * 1024 * 1024),
        backupCount=LOGGING_CONFIG.get('backup_count', 5),
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # 控制台输出（便于开发排查）
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
   极速赛车开奖直播  root_logger.addHandler(console_handler)


def _install_excepthook()极速赛车开奖直播 -> None:
    """捕获未处理异常，写入日志。"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.getLogger(__name__).exception("未捕获异常", exc_info=(exc_type, exc_value, exc_traceback))
    sys.excepthook = handle_exception


def main():
    """主函数"""
    _setup_logging()
    _install_excepthook()

    logger = logging.getLogger(__name__)
    try:
        logger.info("正在启动调香工作室...")
        app = QApplication(sys.argv)

        # 设置应用程序信息
        app.setApplicationName("调香工作室")
        app.setApplicationVersion("1.0")
        app.setOrganizationName("FragranceStudio")

        # 设置应用程序字体
        font = QFont("Microsoft YaHei UI", 9)
极速赛车开奖直播  app.setFont(font)

        # 应用统一主题（若可用）
        if _HAS_QFLUENT:
            try:
                # 跟随系统主题，可改为 Theme.DARK / Theme.LIGHT
                setTheme(Theme.AUTO)
                # 极速赛车开奖直播 主色（可按品牌色调整）
                setThemeColor('#0078d4')
                logger.info("QFluentWidgets 主题已启用 (AUTO)")
            except Exception:
                logger.exception("应用 QFluentWidgets 主题失败，已降级为默认样式")

        logger.info("正在创建主窗口...")
        # 创建主窗口
        main_window = FragranceStudioMain()
        logger.info("正在显示主窗口...")
        main_window.show()

        logger.info("应用程序启动成功，进入事件循环...")
        # 运行应用程序
        sys.exit(app.exec())
    except Exception:
        logger.exception("程序启动失败")
        sys.exit(1)


if __name__ == '__main__':
    main()