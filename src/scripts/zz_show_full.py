# -*- coding: utf-8 -*-
"""完整输出指定段落的中英对照（不截断），用于精确修复。"""
import io
import os
import re
import sys

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
            out.append((i, l.rstrip(), m.group(3)))
    return out


def show(fname, a, b):
    zh = rows(os.path.join(K, fname))
    en = rows(os.path.join(SRC, "x-" + fname))
    print("#" * 108)
    print("# %s  %d..%d   (zh=%d en=%d)" % (fname, a, b, len(zh), len(en)))
    print("#" * 108)
    for k, (ln, raw, zb) in enumerate(zh):
        if not (a <= ln <= b):
            continue
        eb = en[k][2] if k < len(en) else "<超出>"
        print("--- idx %d  L%d" % (k, ln))
        print("  ZH | %s" % zb)
        print("  EN | %s" % eb)
    print()


def main():
    show("tsum_002.rpy", 536, 566)
    show("tsum_001.rpy", 1310, 1326)


if __name__ == "__main__":
    main()
