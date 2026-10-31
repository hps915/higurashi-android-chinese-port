# -*- coding: utf-8 -*-
"""修复 tsum_002 L540-560 整段错位（第 4 处真错位）。

应改为：
  L540 RMT IS PROHIBITED! -> 现金交易可是严格禁止的哟，
  L542 REPORT!            -> 举报！
  L546 REPORT!            -> 举报！
  L550 ACCOUNT,           -> 冻结账号，
  L554 BANNED!!           -> 封禁！！
  L560 (空)               -> 清空
并保留原有的 {size=52} 大字特效标签。
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

PREFIX = u'    extend " {cps=*6.0}{b}{size=52}'
SUFFIX = u'{/size}{/b}{/cps}{nw}"'

# (行号, 英文必须含, 中文内容, 是否保留结尾转义引号)
FIXES = [
    (540, "RMT IS PROHIBITED", u"现金交易可是严格禁止的哟，", False),
    (542, "REPORT!", u"举报！", False),
    (546, "REPORT!", u"举报！", False),
    (550, "ACCOUNT,", u"冻结账号，", False),
    # BANNED!! 是这段台词的最后一句，原文以 \" 闭合，必须保留
    (554, "BANNED", u"封禁！！", True),
    (560, "", u"", False),
]


def body_list(p):
    ln, bd = [], []
    for i, l in enumerate(io.open(p, encoding="utf-8", errors="replace").read().split("\n"), 1):
        m = SAY.match(l.rstrip())
        if m:
            ln.append(i)
            bd.append(m.group(3))
    return ln, bd


def main():
    apply = "--apply" in sys.argv
    zp = os.path.join(K, "tsum_002.rpy")
    sp = os.path.join(SRC, "x-tsum_002.rpy")
    zl, zbd = body_list(zp)
    _, ebd = body_list(sp)
    lines = io.open(zp, encoding="utf-8").read().split("\n")

    ok = fail = 0
    for ln, expect, zh, close_quote in FIXES:
        if ln not in zl:
            print("!! 非 say 行 L%d" % ln)
            fail += 1
            continue
        k = zl.index(ln)
        eb = ebd[k] if k < len(ebd) else ""
        if expect and expect not in eb:
            print("!! 英文不符 L%d  期望%r 实际%r" % (ln, expect, eb[:60]))
            fail += 1
            continue
        if zh:
            if close_quote:
                new = PREFIX + zh + u'\\"{/size}{/b}{/cps}{nw}"'
            else:
                new = PREFIX + zh + SUFFIX
        else:
            new = u'    extend ""'
        print("L%-4d" % ln)
        print("   EN  %s" % eb[:74])
        print("   旧  %s" % lines[ln - 1].strip()[:74])
        print("   新  %s" % new.strip()[:74])
        ok += 1
        if apply:
            lines[ln - 1] = new
    if apply:
        io.open(zp, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print()
    print("成功 %d 失败 %d (apply=%s)" % (ok, fail, apply))


if __name__ == "__main__":
    main()
