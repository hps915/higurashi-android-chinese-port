# -*- coding: utf-8 -*-
"""汇总所有已人工核实的罪灭篇翻译缺陷（只读，输出清单供修复）。"""
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
            out.append((i, m.group(3)))
    return out


# (文件, 起始行, 结束行)  这些是我已核实有问题的段落
REGIONS = [
    ("tsum_001.rpy", 1308, 1322),
    ("tsum_001.rpy", 2035, 2045),
    ("tsum_001.rpy", 552, 562),
    ("tsum_001.rpy", 875, 886),
    ("tsum_002.rpy", 535, 562),
    ("tsum_003.rpy", 672, 690),
    ("tsum_014.rpy", 274, 284),
    ("tsum_018.rpy", 695, 705),
    ("tsum_021.rpy", 1358, 1380),
    ("tsum_022.rpy", 775, 790),
    ("tsum_022.rpy", 1780, 1795),
    ("tsum_025.rpy", 2505, 2520),
    ("tsum_026.rpy", 3810, 3830),
    ("tsum_026.rpy", 3952, 3975),
    ("tsumihoroboshi_tips.rpy", 336, 350),
]


def main():
    for f, a, b in REGIONS:
        zh = rows(os.path.join(K, f))
        en = rows(os.path.join(SRC, "x-" + f))
        print("=" * 104)
        print("%s  %d..%d" % (f, a, b))
        for k, (ln, zb) in enumerate(zh):
            if not (a <= ln <= b):
                continue
            eb = en[k][1] if k < len(en) else "<超出>"
            print("L%-5d|ZH %-48s|EN %s" % (ln, zb[:48], eb[:48]))
        print()


if __name__ == "__main__":
    main()
