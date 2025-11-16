@echo off
REM Git分支差异分析工具启动脚本

echo Git分支差异分析工具
echo =====================
echo.

REM 检查是否安装了Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查是否安装了unidiff
python -c "import unidiff" >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未安装unidiff库，正在安装...
    pip install unidiff
    if %errorlevel% neq 0 (
        echo 安装unidiff失败，请手动运行: pip install unidiff
        pause
        exit /b 1
    )
)

REM 检查是否在Git仓库中
git rev-parse --git-dir >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 当前目录不是Git仓库
    pause
    exit /b 1
)

echo.
echo 选择要使用的工具:
echo 1. 简单版本 - 获取当前分支与main的差异
echo 2. 高级版本 - 提供更多选项和导出功能
echo 3. 退出
echo.

set /p choice="请输入选项 (1-3): "

if "%choice%"=="1" (
    echo.
    echo 运行简单版本...
    python get_branch_diff.py
) else if "%choice%"=="2" (
    echo.
    echo 运行高级版本...
    python git_diff_analyzer.py --help
    echo.
    set /p args="请输入参数 (直接回车使用默认参数): "
    if "%args%"=="" (
        python git_diff_analyzer.py
    ) else (
        python git_diff_analyzer.py %args%
    )
) else if "%choice%"=="3" (
    echo 退出...
    exit /b 0
) else (
    echo 无效选项
)

pause