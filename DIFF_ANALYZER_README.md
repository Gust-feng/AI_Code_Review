# Git分支差异分析工具

这个工具集帮助你分析Git分支之间的差异，提供了简单和高级两种使用方式。

## 文件说明

1. **get_branch_diff.py** - 简单版本的差异分析工具
2. **git_diff_analyzer.py** - 高级版本的差异分析工具，支持多种输出格式
3. **run_diff_analyzer.bat** - Windows批处理脚本，方便启动工具

## 安装依赖

确保已安装Python和Git，然后安装unidiff库：

```bash
pip install unidiff
```

## 使用方法

### 方法1: 使用批处理脚本（推荐）

在Windows环境下，直接双击运行 `run_diff_analyzer.bat`，然后按照提示操作。

### 方法2: 直接运行Python脚本

#### 简单版本

```bash
python get_branch_diff.py
```

这个脚本会：
1. 获取当前分支名称
2. 与main分支比较差异
3. 显示差异摘要
4. 询问是否显示完整diff

#### 高级版本

```bash
# 基本用法
python git_diff_analyzer.py

# 指定目标分支
python git_diff_analyzer.py --target develop

# 只查看Python文件的差异
python git_diff_analyzer.py --filter .py

# 导出为JSON格式
python git_diff_analyzer.py --json diff_report.json

# 导出为HTML格式
python git_diff_analyzer.py --html diff_report.html

# 显示完整diff
python git_diff_analyzer.py --full

# 组合使用
python git_diff_analyzer.py --target develop --filter .py --html report.html --full
```

## 参数说明

- `--target, -t`: 目标分支（默认: main）
- `--filter, -f`: 过滤特定文件（例如: .py）
- `--json, -j`: 导出为JSON格式到指定路径
- `--html, -H`: 导出为HTML格式到指定路径
- `--full`: 显示完整diff

## 示例输出

```
当前分支: feature/new-feature
正在获取与main分支的差异...

=== 差异摘要 ===
分支差异: feature/new-feature → main
总计: 125 行新增, 42 行删除

src/utils/helper.py: +45/-12
src/main.py: +30/-5
README.md: +50/-25 (新文件)
```

## 注意事项

1. 确保在Git仓库目录下运行脚本
2. 如果当前分支就是目标分支，脚本会提示无需比较
3. 二进制文件会显示但不会详细分析内容差异
4. HTML报告提供了美观的可视化界面，适合分享和存档

## 故障排除

如果遇到"未找到unidiff"错误，请运行：
```bash
pip install unidiff
```

如果遇到"当前目录不是Git仓库"错误，请确保在Git仓库目录下运行脚本。