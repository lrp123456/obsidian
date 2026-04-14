#!/usr/bin/env python3
"""
快速递归查询文件夹下的文件数量
用法: python count_files.py [目录路径]
"""

import os
import sys
from pathlib import Path


def count_files(directory: str = ".") -> dict:
    """
    递归统计目录下所有文件的数量和大小

    Returns:
        dict: 包含 total_files, total_dirs, total_size 的字典
    """
    total_files = 0
    total_dirs = 0
    total_size = 0

    for root, dirs, files in os.walk(directory):
        # 跳过隐藏目录（可选）
        # dirs[:] = [d for d in dirs if not d.startswith('.')]

        total_dirs += len(dirs)
        total_files += len(files)

        for file in files:
            file_path = os.path.join(root, file)
            try:
                total_size += os.path.getsize(file_path)
            except (OSError, FileNotFoundError):
                # 跳过无法访问的文件
                pass

    return {
        "total_files": total_files,
        "total_dirs": total_dirs,
        "total_size": total_size,
    }


def format_size(size_bytes: int) -> str:
    """将字节数格式化为可读字符串"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def print_report(directory: str = ".") -> None:
    """打印统计报告"""
    path = Path(directory).resolve()

    if not path.exists():
        print(f"错误: 目录不存在 - {path}")
        sys.exit(1)

    if not path.is_dir():
        print(f"错误: 不是目录 - {path}")
        sys.exit(1)

    print(f"正在统计目录: {path}")
    print("-" * 50)

    result = count_files(str(path))

    print(f"文件数量:     {result['total_files']:,}")
    print(f"目录数量:     {result['total_dirs']:,}")
    print(f"总大小:       {format_size(result['total_size'])}")
    print("-" * 50)


if __name__ == "__main__":
    # 默认统计当前目录，可指定其他目录
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    print_report(directory)
