#!/usr/bin/env python3
"""
高级Git分支差异分析工具
需要安装unidiff库: pip install unidiff

功能:
- 获取当前分支与main分支的差异
- 支持与其他分支比较
- 提供多种输出格式
- 支持过滤特定文件类型
- 生成HTML报告
"""

import argparse
import subprocess
import sys
import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from unidiff import PatchSet


class GitDiffAnalyzer:
    """Git差异分析器"""
    
    def __init__(self, target_branch: str = "main", current_branch: Optional[str] = None):
        self.target_branch = target_branch
        self.current_branch = current_branch or self._get_current_branch()
    
    def _get_current_branch(self) -> str:
        """获取当前Git分支名称"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"获取当前分支失败: {e}")
            sys.exit(1)
    
    def get_diff(self, branch: Optional[str] = None) -> str:
        """获取当前分支与指定分支的diff"""
        branch = branch or self.target_branch
        try:
            result = subprocess.run(
                ["git", "diff", f"{branch}...HEAD"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"获取diff失败: {e}")
            sys.exit(1)
    
    def parse_diff(self, diff_text: str, file_filter: Optional[str] = None) -> Dict[str, Any]:
        """解析diff文本，提取有用信息"""
        if not diff_text.strip():
            return {"files": [], "stats": {"added": 0, "removed": 0}}
        
        patch = PatchSet(diff_text)
        result = {
            "files": [],
            "stats": {"added": 0, "removed": 0},
            "timestamp": datetime.now().isoformat(),
            "branches": {
                "current": self.current_branch,
                "target": self.target_branch
            }
        }
        
        for patched_file in patch:
            # 应用文件过滤器
            if file_filter and file_filter not in patched_file.path:
                continue
                
            # 计算添加和删除的行数
            added_lines = 0
            removed_lines = 0
            hunks_info = []
            
            for hunk in patched_file:
                added_lines += hunk.added
                removed_lines += hunk.removed
                
                hunk_info = {
                    "start_line": hunk.source_start,
                    "line_count": hunk.source_length,
                    "changes": hunk.added + hunk.removed,
                    "added": hunk.added,
                    "removed": hunk.removed
                }
                hunks_info.append(hunk_info)
            
            file_info = {
                "path": patched_file.path,
                "changes": added_lines + removed_lines,
                "added": added_lines,
                "removed": removed_lines,
                "is_new_file": patched_file.is_added_file,
                "is_removed_file": patched_file.is_removed_file,
                "is_binary": patched_file.is_binary_file,
                "hunks": hunks_info
            }
            
            result["files"].append(file_info)
            result["stats"]["added"] += added_lines
            result["stats"]["removed"] += removed_lines
        
        return result
    
    def format_summary(self, diff_info: Dict[str, Any]) -> str:
        """格式化diff摘要信息"""
        summary = []
        summary.append(f"分支差异: {diff_info['branches']['current']} → {diff_info['branches']['target']}")
        summary.append(f"总计: {diff_info['stats']['added']} 行新增, {diff_info['stats']['removed']} 行删除")
        summary.append("")
        
        for file_info in diff_info["files"]:
            status = ""
            if file_info["is_new_file"]:
                status = " (新文件)"
            elif file_info["is_removed_file"]:
                status = " (已删除)"
            elif file_info["is_binary"]:
                status = " (二进制文件)"
            
            summary.append(
                f"{file_info['path']}: +{file_info['added']}/-{file_info['removed']}{status}"
            )
        
        return "\n".join(summary)
    
    def export_json(self, diff_info: Dict[str, Any], output_path: str) -> None:
        """导出为JSON格式"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(diff_info, f, indent=2, ensure_ascii=False)
        print(f"JSON报告已保存到: {output_path}")
    
    def export_html(self, diff_info: Dict[str, Any], output_path: str) -> None:
        """导出为HTML格式"""
        html_content = self._generate_html_report(diff_info)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML报告已保存到: {output_path}")
    
    def _generate_html_report(self, diff_info: Dict[str, Any]) -> str:
        """生成HTML报告"""
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Git差异报告: {diff_info['branches']['current']} → {diff_info['branches']['target']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        .summary {{
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 4px 4px 0;
        }}
        .file-list {{
            margin-top: 20px;
        }}
        .file-item {{
            border-bottom: 1px solid #eee;
            padding: 10px 0;
        }}
        .file-path {{
            font-weight: bold;
            color: #2c3e50;
        }}
        .file-stats {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .added {{
            color: #27ae60;
        }}
        .removed {{
            color: #e74c3c;
        }}
        .new-file {{
            color: #3498db;
        }}
        .deleted-file {{
            color: #95a5a6;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.8em;
            text-align: right;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Git差异报告</h1>
        <div class="timestamp">生成时间: {diff_info['timestamp']}</div>
        
        <div class="summary">
            <h2>摘要</h2>
            <p><strong>分支:</strong> {diff_info['branches']['current']} → {diff_info['branches']['target']}</p>
            <p><strong>总变更:</strong> <span class="added">+{diff_info['stats']['added']}</span> 行新增, 
               <span class="removed">-{diff_info['stats']['removed']}</span> 行删除</p>
        </div>
        
        <div class="file-list">
            <h2>文件变更详情</h2>
"""
        
        for file_info in diff_info["files"]:
            status_class = ""
            status_text = ""
            
            if file_info["is_new_file"]:
                status_class = "new-file"
                status_text = " (新文件)"
            elif file_info["is_removed_file"]:
                status_class = "deleted-file"
                status_text = " (已删除)"
            elif file_info["is_binary"]:
                status_text = " (二进制文件)"
            
            html += f"""
            <div class="file-item">
                <div class="file-path {status_class}">{file_info['path']}{status_text}</div>
                <div class="file-stats">
                    <span class="added">+{file_info['added']}</span> / 
                    <span class="removed">-{file_info['removed']}</span> 行
                </div>
            </div>
"""
        
        html += """
        </div>
    </div>
</body>
</html>
"""
        return html


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Git分支差异分析工具")
    parser.add_argument("--target", "-t", default="main", help="目标分支 (默认: main)")
    parser.add_argument("--filter", "-f", help="过滤特定文件 (例如: .py)")
    parser.add_argument("--json", "-j", help="导出为JSON格式到指定路径")
    parser.add_argument("--html", "-H", help="导出为HTML格式到指定路径")
    parser.add_argument("--full", action="store_true", help="显示完整diff")
    
    args = parser.parse_args()
    
    analyzer = GitDiffAnalyzer(target_branch=args.target)
    print(f"当前分支: {analyzer.current_branch}")
    
    if analyzer.current_branch == args.target:
        print(f"当前已在{args.target}分支，无需比较")
        return
    
    print(f"正在获取与{args.target}分支的差异...")
    diff_text = analyzer.get_diff()
    
    if not diff_text.strip():
        print(f"当前分支与{args.target}分支没有差异")
        return
    
    diff_info = analyzer.parse_diff(diff_text, file_filter=args.filter)
    print("\n=== 差异摘要 ===")
    print(analyzer.format_summary(diff_info))
    
    # 导出选项
    if args.json:
        analyzer.export_json(diff_info, args.json)
    
    if args.html:
        analyzer.export_html(diff_info, args.html)
    
    # 显示完整diff
    if args.full:
        print("\n=== 完整Diff ===")
        print(diff_text)


if __name__ == "__main__":
    main()