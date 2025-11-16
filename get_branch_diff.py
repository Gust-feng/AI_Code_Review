#!/usr/bin/env python3
"""
获取当前分支和main分支的diff信息
需要安装unidiff库: pip install unidiff
"""

import subprocess
import sys
from unidiff import PatchSet
from typing import List, Dict, Any


def get_current_branch() -> str:
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


def get_diff_with_main(branch: str = "main") -> str:
    """获取当前分支与指定分支的diff"""
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


def parse_diff(diff_text: str) -> Dict[str, Any]:
    """解析diff文本，提取有用信息"""
    if not diff_text.strip():
        return {"files": [], "stats": {"added": 0, "removed": 0}}
    
    patch = PatchSet(diff_text)
    result = {
        "files": [],
        "stats": {"added": 0, "removed": 0}
    }
    
    for patched_file in patch:
        # 计算添加和删除的行数
        added_lines = 0
        removed_lines = 0
        
        for hunk in patched_file:
            added_lines += hunk.added
            removed_lines += hunk.removed
        
        file_info = {
            "path": patched_file.path,
            "changes": added_lines + removed_lines,
            "added": added_lines,
            "removed": removed_lines,
            "is_new_file": patched_file.is_added_file,
            "is_removed_file": patched_file.is_removed_file,
            "is_binary": patched_file.is_binary_file
        }
        result["files"].append(file_info)
        result["stats"]["added"] += added_lines
        result["stats"]["removed"] += removed_lines
    
    return result


def format_diff_summary(diff_info: Dict[str, Any]) -> str:
    """格式化diff摘要信息"""
    summary = []
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


def main():
    """主函数"""
    current_branch = get_current_branch()
    print(f"当前分支: {current_branch}")
    
    if current_branch == "main":
        print("当前已在main分支，无需比较")
        return
    
    print("正在获取与main分支的差异...")
    diff_text = get_diff_with_main()
    
    if not diff_text.strip():
        print("当前分支与main分支没有差异")
        return
    
    diff_info = parse_diff(diff_text)
    print("\n=== 差异摘要 ===")
    print(format_diff_summary(diff_info))
    
    # 询问是否显示完整diff
    show_full = input("\n是否显示完整diff? (y/n): ").lower().strip()
    if show_full in ['y', 'yes']:
        print("\n=== 完整Diff ===")
        print(diff_text)


if __name__ == "__main__":
    main()