# -*- coding: utf-8 -*-
"""罪灭篇 3 处真错位修复（严格核实过的唯一 3 处）。

每项：(文件, 行号, 英文必须含, 新完整行内容)
全部改完立刻用 --verify 复核。
"""
import io
import os
import re
import sys

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
K = os.path.join(BASE, "work", "project_k", "game", "tsumihoroboshi")
SRC = os.path.join(BASE, "work", "apk_k", "assets", "x-game", "x-tsumihoroboshi")

SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*(.*)$')

# (文件, 行号, 英文必须含, 新行全文)
FIXES = [
    # 处1: tsum_021 L1373  语义反转
    ("tsum_021.rpy", 1373, "was never",
     u'    n "…我从来就不是她们的伙伴。"'),

    # 处2: tsum_001 L1313..1318  整段前移一格
    ("tsum_001.rpy", 1313, "{w=0.8}",
     u'    extend "{w=0.8}"'),
    ("tsum_001.rpy", 1315, "she frowned in confusion",
     u'    extend " 但是一瞬间，她的表情扭曲了…！"'),
    ("tsum_001.rpy", 1317, "What was going on",
     u'    n "怎么回事？！…不开枪吗？！"'),
    ("tsum_001.rpy", 1318, "Was her water gun broken",
     u'    extend " 那把枪坏了吗？"'),

    # 处3: tsum_001 L2038/2040/2041
    ("tsum_001.rpy", 2038, "",
     u'    extend ""'),
    ("tsum_001.rpy", 2040, "I expected she might settle",
     u'    n "还以为会判为平手，"'),
    ("tsum_001.rpy", 2041, "but I never thought",
     u'    n "竟然判重赛啊！"'),
]


def body_index(path):
    """返回 (行号列表, 各行 body 列表)"""
    ln_list, body_list = [], []
    for i, l in enumerate(io.open(path, encoding="utf-8", errors="replace").read().split("\n"), 1):
        m = SAY.match(l.rstrip())
        if m:
            ln_list.append(i)
            body_list.append(m.group(3))
    return ln_list, body_list


def main():
    apply = "--apply" in sys.argv
    ok = fail = 0
    for fname, ln, expect, newline in FIXES:
        zp = os.path.join(K, fname)
        sp = os.path.join(SRC, "x-" + fname)
        zl, zb = body_index(zp)
        _, eb = body_index(sp)
        if ln not in zl:
            print("!! 非 say 行 %s:%d" % (fname, ln))
            fail += 1
            continue
        k = zl.index(ln)
        ebody = eb[k] if k < len(eb) else ""
        if expect and expect not in ebody:
            print("!! 英文不符 %s:%d\n   期望含 %r\n   实际   %r"
                  % (fname, ln, expect, ebody[:70]))
            fail += 1
            continue
        print("OK %s:%d" % (fname, ln))
        print("   EN   %s" % ebody[:76])
        print("   旧行 %s" % io.open(zp, encoding="utf-8").read().split("\n")[ln - 1].strip()[:76])
        print("   新行 %s" % newline.strip()[:76])
        ok += 1
        if apply:
            lines = io.open(zp, encoding="utf-8").read().split("\n")
            lines[ln - 1] = newline
            io.open(zp, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print()
    print("成功 %d  失败 %d  (apply=%s)" % (ok, fail, apply))


if __name__ == "__main__":
    main()
