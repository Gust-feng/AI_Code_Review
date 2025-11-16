#!/usr/bin/env python3
"""
测试unidiff库的API
"""

from unidiff import PatchSet

# 创建一个简单的diff文本
diff_text = """diff --git a/file1.txt b/file1.txt
index e69de29..4b825dc 100644
--- a/file1.txt
+++ b/file1.txt
@@ -0,0 +1,3 @@
+Line 1
+Line 2
+Line 3
diff --git a/file2.txt b/file2.txt
index e69de29..4b825dc 100644
--- a/file2.txt
+++ b/file2.txt
@@ -0,0 +1,2 @@
+Line A
+Line B
"""

# 解析diff
patch = PatchSet(diff_text)

# 打印PatchSet的属性
print("PatchSet属性:")
print(f"  added: {patch.added}")
print(f"  removed: {patch.removed}")
print(f"  added_files: {patch.added_files}")
print(f"  removed_files: {patch.removed_files}")
print(f"  modified_files: {patch.modified_files}")
print()

# 遍历每个文件
print("文件详情:")
for patched_file in patch:
    print(f"文件: {patched_file}")
    print(f"  属性: {[attr for attr in dir(patched_file) if not attr.startswith('_')]}")
    
    # 尝试获取文件统计信息
    try:
        print(f"  is_added_file: {patched_file.is_added_file}")
    except:
        print("  is_added_file: 属性不存在")
    
    try:
        print(f"  additions: {patched_file.additions}")
    except:
        print("  additions: 属性不存在")
    
    try:
        print(f"  deletions: {patched_file.deletions}")
    except:
        print("  deletions: 属性不存在")
    
    # 尝试获取hunks
    try:
        print(f"  hunks数量: {len(patched_file)}")
        for i, hunk in enumerate(patched_file):
            print(f"    Hunk {i}: {hunk}")
            print(f"      属性: {[attr for attr in dir(hunk) if not attr.startswith('_')]}")
    except Exception as e:
        print(f"  获取hunks失败: {e}")
    
    print()