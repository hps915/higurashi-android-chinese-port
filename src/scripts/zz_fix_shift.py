# -*- coding: utf-8 -*-
"""罪灭篇译文偏移修复（已人工逐条核实）。

每一条都写明：文件、行号、该行英文、修正后的中文。
全部为「整段前移一格」或「错填/重复」，统一改成正确对应关系。
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

# (文件, 行号, 期望的英文片段(用于校验), 新中文内容)
FIXES = [
    # --- tsum_001: 整段前移一格 ---
    ("tsum_001.rpy", 1313, "{w=0.8}", "{w=0.8}"),
    ("tsum_001.rpy", 1315, "she frowned in confusion", u" 但是一瞬间，她的表情扭曲了…！"),
    ("tsum_001.rpy", 1317, "What was going on", u"怎么回事？！…不开枪吗？！"),
    ("tsum_001.rpy", 1318, "Was her water gun broken", u" 那把枪坏了吗？"),
    ("tsum_001.rpy", 1320, "Or was it broken", u"还是说被谁弄坏了？！"),

    # --- tsum_014: L280 重复了 L277，应为「突然发痒」 ---
    ("tsum_014.rpy", 280, "started itching",
     u"与此同时，我的手腕、手肘、大腿内侧、脖子，突然开始发痒。"),

    # --- tsum_002: 大字特效段（RMT 警告）中文顺序错 ---
    ("tsum_002.rpy", 540, "RMT IS PROHIBITED", u"\"RMT 是禁止的！{w=0.5}"),
    ("tsum_002.rpy", 542, "REPORT!", u" 现金交易可是严格禁止的哟，"),
]


def main():
    apply = "--apply" in sys.argv
    ok = fail = 0
    for fname, ln, expect, newzh in FIXES:
        zp = os.path.join(K, fname)
        sp = os.path.join(SRC, "x-" + fname)
        lines = io.open(zp, encoding="utf-8").read().split("\n")
        i = ln - 1
        if i >= len(lines):
            print("!! 越界 %s:%d" % (fname, ln))
            fail += 1
            continue
        cur = lines[i]
        m = SAY.match(cur.rstrip())
        if not m:
            print("!! 非 say 行 %s:%d  %r" % (fname, ln, cur[:60]))
            fail += 1
            continue
        # 校验英文（按 say 行序号）
        zh_rows = []
        for j, l in enumerate(lines, 1):
            mm = SAY.match(l.rstrip())
            if mm:
                zh_rows.append(j)
        k = zh_rows.index(ln)
        en_lines = io.open(sp, encoding="utf-8", errors="replace").read().split("\n")
        en_rows = []
        for l in en_lines:
            mm = SAY.match(l.rstrip())
            if mm:
                en_rows.append(mm.group(3))
        en_body = en_rows[k] if k < len(en_rows) else ""
        if expect not in en_body:
            print("!! 英文不符 %s:%d\n   期望含 %r\n   实际   %r" % (fname, ln, expect, en_body[:70]))
            fail += 1
            continue

        stripped = cur.lstrip()
        indent = cur[:len(cur) - len(stripped)]
        q = stripped.index('"')
        prefix = stripped[:q]
        newline = indent + prefix + '"' + newzh.replace('"', '\\"') + '"'
        print("OK  %s:%d" % (fname, ln))
        print("    EN : %s" % en_body[:76])
        print("    旧 : %s" % m.group(3)[:76])
        print("    新 : %s" % newzh[:76])
        ok += 1
        if apply:
            lines[i] = newline
            io.open(zp, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print()
    print("成功 %d，失败 %d (apply=%s)" % (ok, fail, apply))


if __name__ == "__main__":
    main()
