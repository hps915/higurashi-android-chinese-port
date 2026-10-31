# -*- coding: utf-8 -*-
"""只读：输出 3 处待修区域的完整原始文件内容（含所有非 say 行），用于精确修复。"""
import io
import os

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
K = os.path.join(BASE, "work", "project_k", "game", "tsumihoroboshi")
SRC = os.path.join(BASE, "work", "apk_k", "assets", "x-game", "x-tsumihoroboshi")

REGIONS = [
    ("tsum_021.rpy", 1368, 1380, 1368, 1380),
    ("tsum_001.rpy", 1308, 1324, 1308, 1324),
    ("tsum_001.rpy", 2034, 2046, 2034, 2046),
]


def dump(path, a, b, label):
    lines = io.open(path, encoding="utf-8", errors="replace").read().split("\n")
    print("--- %s %s:%d..%d ---" % (label, os.path.basename(path), a, b))
    for i in range(a, min(b + 1, len(lines) + 1)):
        print("%5d | %s" % (i, lines[i - 1]))
    print()


def main():
    for f, za, zb, sa, sb in REGIONS:
        print("=" * 100)
        print("### %s" % f)
        print()
        dump(os.path.join(K, f), za, zb, "工程(中文)")
        dump(os.path.join(SRC, "x-" + f), sa, sb, "源包(英文)")


if __name__ == "__main__":
    main()
