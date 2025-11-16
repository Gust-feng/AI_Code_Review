# Git分支差异分析工具启动脚本 (PowerShell版本)

Write-Host "Git分支差异分析工具" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan
Write-Host ""

# 检查是否安装了Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python版本: $pythonVersion"
} catch {
    Write-Host "错误: 未找到Python，请先安装Python" -ForegroundColor Red
    Read-Host "按Enter键退出"
    exit 1
}

# 检查是否安装了unidiff
try {
    $null = python -c "import unidiff" 2>&1
} catch {
    Write-Host "错误: 未安装unidiff库，正在安装..." -ForegroundColor Yellow
    pip install unidiff
    if ($LASTEXITCODE -ne 0) {
        Write-Host "安装unidiff失败，请手动运行: pip install unidiff" -ForegroundColor Red
        Read-Host "按Enter键退出"
        exit 1
    }
}

# 检查是否在Git仓库中
try {
    $null = git rev-parse --git-dir 2>&1
} catch {
    Write-Host "错误: 当前目录不是Git仓库" -ForegroundColor Red
    Read-Host "按Enter键退出"
    exit 1
}

Write-Host ""
Write-Host "选择要使用的工具:" -ForegroundColor Green
Write-Host "1. 简单版本 - 获取当前分支与main的差异"
Write-Host "2. 高级版本 - 提供更多选项和导出功能"
Write-Host "3. 退出"
Write-Host ""

$choice = Read-Host "请输入选项 (1-3)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "运行简单版本..." -ForegroundColor Green
        python get_branch_diff.py
    }
    "2" {
        Write-Host ""
        Write-Host "运行高级版本..." -ForegroundColor Green
        python git_diff_analyzer.py --help
        Write-Host ""
        $args = Read-Host "请输入参数 (直接回车使用默认参数)"
        if ([string]::IsNullOrEmpty($args)) {
            python git_diff_analyzer.py
        } else {
            python git_diff_analyzer.py $args
        }
    }
    "3" {
        Write-Host "退出..." -ForegroundColor Green
        exit 0
    }
    default {
        Write-Host "无效选项" -ForegroundColor Red
    }
}

Read-Host "按Enter键退出"