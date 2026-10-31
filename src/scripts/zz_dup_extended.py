# -*- coding: utf-8 -*-
"""扩展检测：找出所有「相邻重复」对，不论源英文是否相同。

对每一对，标注：
  - SAME_EN   : 源英文也相同 -> 合法（原文本身就是重复句）
  - DIFF_EN   : 源英文不同   -> 缺陷
"""
import io
import os
import re

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PAIRS = [
    ("解题篇", os.path.join(BASE, "work", "project_k", "game"),
     os.path.join(BASE, "work", "apk_k", "assets", "x-game")),
    ("出题篇", os.path.join(BASE, "work", "project", "game"),
     os.path.join(BASE, "work", "apk_q", "assets", "x-game")),
]
CJK = re.compile(u'[\u4e00-\u9fff]')
SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*$')


def rows(path):
    out = []
    for i, line in enumerate(io.open(path, encoding="utf-8", errors="replace").read().split("\n"), 1):
        m = SAY.match(line.rstrip())
        if not m:
            continue
        out.append((i, (m.group(2) or "").strip(), m.group(3)))
    return out


def main():
    for label, gd, srcdir in PAIRS:
        print("=" * 90)
        print("### %s" % label)
        same_en = 0
        diff_en = []
        for cd in sorted(d for d in os.listdir(gd) if os.path.isdir(os.path.join(gd, d))):
            sub = os.path.join(gd, cd)
            for f in sorted(os.listdir(sub)):
                if not f.endswith(".rpy"):
                    continue
                sp = os.path.join(srcdir, "x-" + cd, "x-" + f)
                if not os.path.exists(sp):
                    continue
                nr = rows(os.path.join(sub, f))
                orow = rows(sp)
                aligned = len(nr) == len(orow)
                prev_zh = None
                prev_en = None
                prev_no = 0
                for k in range(len(nr)):
                    zh = nr[k][2]
                    en = orow[k][2] if aligned else None
                    if not CJK.search(zh) or len(zh) < 10:
                        prev_zh, prev_en, prev_no = zh, en, nr[k][0]
                        continue
                    if zh == prev_zh:
                        if en is not None and prev_en is not None and en != prev_en:
                            diff_en.append((cd, f, prev_no, nr[k][0], prev_en, en, zh))
                        else:
                            same_en += 1
                    prev_zh, prev_en, prev_no = zh, en, nr[k][0]
        print("  合法重复(源英文也相同): %d" % same_en)
        print("  仍存缺陷(源英文不同): %d" % len(diff_en))
        for cd, f, a, b, pe, ce, zh in diff_en[:40]:
            print("   %s/%s L%d&L%d" % (cd, f, a, b))
            print("      EN_prev: %s" % (pe or "")[:95])
            print("      EN_cur : %s" % (ce or "")[:95])
            print("      ZH_both: %s" % zh[:95])
        print()


if __name__ == "__main__":
    main()
