# -*- coding: utf-8 -*-
"""只读：把待修段落的「完整对齐序列」打印出来，用于制定精确的行移位方案。

对每个目标文件，输出 源包英文 与 工程中文 的逐行对照（含 extend/标签行）。
"""
import io
import os
import re

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
K = os.path.join(BASE, "work", "project_k", "game", "tsumihoroboshi")
SRC = os.path.join(BASE, "work", "apk_k", "assets", "x-game", "x-tsumihoroboshi")

SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*$')


def rows(p):
    out = []
    for i, l in enumerate(io.open(p, encoding="utf-8", errors="replace").read().split("\n"), 1):
        m = SAY.match(l.rstrip())
        if m:
            out.append((i, m.group(2) or "", m.group(3)))
    return out


def show(fname, a, b):
    zh = rows(os.path.join(K, fname))
    en = rows(os.path.join(SRC, "x-" + fname))
    print("=" * 100)
    print("%s  L%d..L%d" % (fname, a, b))
    for k, (ln, _id, zb) in enumerate(zh):
        if not (a <= ln <= b):
            continue
        eb = en[k][2] if k < len(en) else "<超出>"
        print("L%-5d | %-9s | ZH %-46s | EN %s" % (ln, _id or "-", zb[:46], eb[:52]))
    print()


def main():
    show("tsum_001.rpy", 1308, 1322)
    show("tsum_002.rpy", 625, 642)
    show("tsum_003.rpy", 672, 690)
    show("tsum_026.rpy", 3810, 3830)
    show("tsum_026.rpy", 3952, 3975)


if __name__ == "__main__":
    main()
