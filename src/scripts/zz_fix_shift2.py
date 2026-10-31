# -*- coding: utf-8 -*-
"""罪灭篇「整段前移一格」精确修复（已逐段人工核对）。

原理：源包把一句拆成
   extend "前半"
   extend "{w=0.x}"        <- 纯计时
   extend "后半"
工程把中文错位一格，导致最后多出一句重复。

修法：按正确对应关系逐行赋值，多余行改回标签。
每项：(文件, 行号, 该行英文必须包含的片段, 新中文)
"""
import io
import os
import re
import sys

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
K = os.path.join(BASE, "work", "project_k", "game", "tsumihoroboshi")
SRC = os.path.join(BASE, "work", "apk_k", "assets", "x-game", "x-tsumihoroboshi")

SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*$')

W = "{w=0.8}"

FIXES = [
    # ===== tsum_001 L1313..1320：整段前移一格 =====
    ("tsum_001.rpy", 1313, "{w=0.8}", W),
    ("tsum_001.rpy", 1315, "she frowned in confusion", u" 但是一瞬间，她的表情扭曲了…"),
    ("tsum_001.rpy", 1317, "What was going on", u"怎么回事？！…不开枪吗？！"),
    ("tsum_001.rpy", 1318, "Was her water gun broken", u" 那把枪坏了吗？"),
    # L1320 带 with Shake 后缀，单独处理（见 SPECIAL）

    # ===== tsum_014 L280：重复了 L277，应为「突然发痒」=====
    ("tsum_014.rpy", 280, "started itching",
     u"与此同时，我的手腕、手肘、大腿内侧、脖子也突然开始发痒。"),

    # ===== tsum_002 L540..560：大字 RMT 警告段，中文前移一格 =====
    ("tsum_002.rpy", 540, "RMT IS PROHIBITED",
     u'"{cps=*6.0}{b}{size=52}RMT 是禁止的！{w=0.5}{/size}{/b}{/cps}{nw}"'),
    ("tsum_002.rpy", 542, "REPORT!",
     u' "{cps=*6.0}{b}{size=52}举报！{/size}{/b}{/cps}{nw}"'),
    ("tsum_002.rpy", 546, "REPORT!",
     u' "{cps=*6.0}{b}{size=52}举报！{/size}{/b}{/cps}{nw}"'),
    ("tsum_002.rpy", 550, "ACCOUNT,",
     u' "{cps=*6.0}{b}{size=52}冻结账号，{/size}{/b}{/cps}{nw}"'),
    ("tsum_002.rpy", 554, "BANNED",
     u' "{cps=*6.0}{b}{size=52}封禁！！"{/size}{/b}{/cps}{nw}"'),
    ("tsum_002.rpy", 560, "", u" "),   # 多余重复，清空
]

# L1320 特殊：带 with Shake 后缀
SPECIAL_1320 = ("tsum_001.rpy", 1320, "Or did somebody break it",
                u'    extend "{cps=*20.0}还是说被谁弄坏了？！{/cps}" with Shake((0, 0, 0, 0), 0.3, dist=50)')


def body_rows(path):
    """返回 [(行号, 原始行, body)]"""
    out = []
    for i, l in enumerate(io.open(path, encoding="utf-8", errors="replace").read().split("\n"), 1):
        m = SAY.match(l.rstrip())
        if m:
            out.append((i, l.rstrip(), m.group(3)))
    return out


def main():
    apply = "--apply" in sys.argv
    ok = fail = 0
    for fname, ln, expect, newzh in FIXES:
        zp = os.path.join(K, fname)
        sp = os.path.join(SRC, "x-" + fname)
        lines = io.open(zp, encoding="utf-8").read().split("\n")
        zh_rows = [j for j, l in enumerate(lines, 1) if SAY.match(l.rstrip())]
        if ln not in zh_rows:
            print("!! 非 say 行 %s:%d" % (fname, ln))
            fail += 1
            continue
        k = zh_rows.index(ln)
        en_bs = [m.group(3) for l in io.open(sp, encoding="utf-8", errors="replace").read().split("\n")
                 if (m := SAY.match(l.rstrip()))]
        en_body = en_bs[k] if k < len(en_bs) else ""
        if expect and expect not in en_body:
            print("!! 英文不符 %s:%d  期望%r 实际%r" % (fname, ln, expect, en_body[:60]))
            fail += 1
            continue
        cur = lines[ln - 1]
        st = cur.lstrip()
        indent = cur[:len(cur) - len(st)]
        q = st.index('"')
        prefix = st[:q]
        newline = indent + prefix + '"' + newzh.replace('"', '\\"') + '"'
        print("OK %s:%d" % (fname, ln))
        print("   EN  %s" % en_body[:74])
        print("   旧  %s" % SAY.match(cur.rstrip()).group(3)[:74])
        print("   新  %s" % newzh[:74])
        ok += 1
        if apply:
            lines[ln - 1] = newline
            io.open(zp, "w", encoding="utf-8", newline="\n").write("\n".join(lines))

    # 特殊项 L1320
    fname, ln, expect, full_new = SPECIAL_1320
    zp = os.path.join(K, fname)
    sp = os.path.join(SRC, "x-" + fname)
    lines = io.open(zp, encoding="utf-8").read().split("\n")
    zh_rows = [j for j, l in enumerate(lines, 1) if SAY.match(l.rstrip())]
    k = zh_rows.index(ln) if ln in zh_rows else -1
    en_bs = [m.group(3) for l in io.open(sp, encoding="utf-8", errors="replace").read().split("\n")
             if (m := SAY.match(l.rstrip()))]
    en_body = en_bs[k] if 0 <= k < len(en_bs) else ""
    print()
    print("SPECIAL %s:%d" % (fname, ln))
    print("   EN  %s" % en_body[:74])
    print("   旧  %s" % lines[ln - 1].strip()[:80])
    print("   新  %s" % full_new.strip()[:80])
    if expect and expect not in en_body:
        print("   !! 英文不符")
        fail += 1
    else:
        ok += 1
        if apply:
            lines[ln - 1] = full_new
            io.open(zp, "w", encoding="utf-8", newline="\n").write("\n".join(lines))

    print()
    print("成功 %d  失败 %d  (apply=%s)" % (ok, fail, apply))


if __name__ == "__main__":
    main()
