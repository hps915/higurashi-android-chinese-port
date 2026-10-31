# -*- coding: utf-8 -*-
"""只读：按 say 行序号对齐，批量输出指定行号范围的 ZH/EN 对照，用于人工核实。"""
import io
import os
import re

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
K = os.path.join(BASE, "work", "project_k", "game")
SRC = os.path.join(BASE, "work", "apk_k", "assets", "x-game")

SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*$')


def rows(p):
    out = []
    for i, l in enumerate(io.open(p, encoding="utf-8", errors="replace").read().split("\n"), 1):
        m = SAY.match(l.rstrip())
        if m:
            out.append((i, m.group(3)))
    return out


def show(fname, a, b):
    zh = rows(os.path.join(K, "tsumihoroboshi", fname))
    en = rows(os.path.join(SRC, "x-tsumihoroboshi", "x-" + fname))
    print("=" * 92)
    print("%s  (工程 %d 行 / 源 %d 行)" % (fname, len(zh), len(en)))
    for i, z in zh:
        if not (a <= i <= b):
            continue
        k = [idx for idx, (ln, _) in enumerate(zh) if ln == i][0]
        e = en[k][1] if k < len(en) else "<无>"
        print("  L%-5d ZH: %s" % (i, z[:80]))
        print("         EN: %s" % e[:80])
    print()


def main():
    show("tsum_025.rpy", 2505, 2520)
    show("tsum_022.rpy", 1780, 1795)
    show("tsum_001.rpy", 1310, 1325)
    show("tsum_001.rpy", 2035, 2045)
    show("tsum_014.rpy", 274, 284)
    show("tsum_018.rpy", 695, 705)
    show("tsumihoroboshi_tips.rpy", 336, 350)


if __name__ == "__main__":
    main()
