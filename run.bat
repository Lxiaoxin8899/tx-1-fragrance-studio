@echo off
chcp 65001
echo ================================
echo    Flavor Lab Pro 启动脚本
echo ================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

REM 检查虚拟环境
if exist .venv (
    echo 激活虚拟环境...
    call .venv\Scripts\activate
) else (
    echo 警告: 未找到虚拟环境，使用系统Python
)

REM 检查依赖包
python -c "import PyQt6" 2>nul
if errorlevel 1 (
    echo 安装依赖包...
    pip install -r requirements.txt
)

echo.
echo 启动 Flavor Lab Pro...
echo ================================
python main.py

REM 如果使用了虚拟环境，退出时停用
if exist .venv (
    deactivate
)

pause