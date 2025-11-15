# 静态分析工具快捷脚本
# 用法: .\scan.ps1 [command]

param(
    [Parameter(Position=0)]
    [string]$Command = "all"
)

$VenvPath = "$PSScriptRoot\venv\Scripts"

function Scan-Python {
    Write-Host "🔍 扫描 Python 代码..." -ForegroundColor Cyan
    & "$VenvPath\ruff.exe" check agent_core
}

function Scan-Security {
    Write-Host "🔒 安全扫描..." -ForegroundColor Yellow
    & "$VenvPath\bandit.exe" -r agent_core -f screen
}

function Scan-MultiLang {
    Write-Host "🌍 多语言扫描..." -ForegroundColor Green
    & "$VenvPath\semgrep.exe" --config=auto .
}

function Scan-TypeCheck {
    Write-Host "📝 类型检查..." -ForegroundColor Magenta
    & "$VenvPath\mypy.exe" agent_core
}

switch ($Command.ToLower()) {
    "python" { Scan-Python }
    "security" { Scan-Security }
    "multi" { Scan-MultiLang }
    "type" { Scan-TypeCheck }
    "all" {
        Scan-Python
        Write-Host ""
        Scan-Security
        Write-Host ""
        Scan-MultiLang
    }
    default {
        Write-Host "用法: .\scan.ps1 [python|security|multi|type|all]" -ForegroundColor Red
        Write-Host "  python   - 扫描 Python 代码质量"
        Write-Host "  security - 安全漏洞扫描"
        Write-Host "  multi    - 多语言代码扫描"
        Write-Host "  type     - Python 类型检查"
        Write-Host "  all      - 运行所有扫描（默认）"
    }
}
