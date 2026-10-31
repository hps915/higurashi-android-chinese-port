# -*- coding: utf-8 -*-
"""罪灭篇错位修复：把被错填的中文行清空 / 重新对齐。

策略（保守）：
  A) 「源为纯 {w=}/{nw}，工程却是中文」的行  -> 恢复为源包的标签内容
     这类行本来就该只显示标签，中文是被算法误填进去的。
  B) 检查这些位置后面紧跟的行，是否吃掉了本该独立的句子。
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
CJK = re.compile(u'[\u4e00-\u9fff]')
ONLY_TAG = re.compile(r'^(\s*\{[^{}]*\})+\s*$')

# 已人工核实的 5 处（文件, 行号, 源包该行内容）
TARGETS = [
    ("tsum_001.rpy", 1313, "{w=0.8}"),
    ("tsum_002.rpy", 633, "{w=0.2}{nw}"),
    ("tsum_003.rpy", 680, "{w=0.2}{nw}"),
    ("tsum_026.rpy", 3819, "{w=0.4}{nw}"),
    ("tsum_026.rpy", 3961, "{w=0.3}{nw}"),
]


def rows(p):
    out = []
    for i, l in enumerate(io.open(p, encoding="utf-8", errors="replace").read().split("\n"), 1):
        m = SAY.match(l.rstrip())
        if m:
            out.append((i, m.group(2) or "", m.group(3)))
    return out


def main():
    apply = "--apply" in sys.argv
    for fname, ln, srcbody in TARGETS:
        zp = os.path.join(K, fname)
        sp = os.path.join(SRC, "x-" + fname)
        lines = io.open(zp, encoding="utf-8").read().split("\n")
        i = ln - 1
        cur = lines[i]
        m = SAY.match(cur.rstrip())
        if not m:
            print("!! 不是 say 行 %s:%d" % (fname, ln))
            continue
        ident = (m.group(2) or "").strip()
        body = m.group(3)
        print("=" * 80)
        print("%s:%d   ident=%r" % (fname, ln, ident))
        print("  当前: %r" % body[:90])

        # 该句真正的中文应该在哪？看源包该行前后是否有被拆的句子
        zh = rows(zp)
        en = rows(sp)
        k = [j for j, (l2, _, _) in enumerate(zh) if l2 == ln][0]
        # 打印邻域供人工判断
        for off in range(-2, 3):
            j = k + off
            if 0 <= j < len(zh) and 0 <= j < len(en):
                mark = ">>" if off == 0 else "  "
                print("   %s L%-5d ZH:%-46s | EN:%s"
                      % (mark, zh[j][0], zh[j][2][:46], en[j][2][:46]))

        newline = None
        if ident:
            newline = '    %s "%s"' % (ident, srcbody) if False else None
        # 保留原缩进与说话人标识
        stripped = cur.lstrip()
        indent = cur[:len(cur) - len(stripped)]
        q = stripped.index('"')
        prefix = stripped[:q]
        newline = indent + prefix + '"' + srcbody.replace('"', '\\"') + '"'
        print("  修正为: %r" % newline)
        if apply:
            lines[i] = newline
            io.open(zp, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print()
    print("(apply=%s)" % apply)


if __name__ == "__main__":
    main()
