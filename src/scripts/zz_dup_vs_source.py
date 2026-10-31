# -*- coding: utf-8 -*-
"""严格定位「译文重复」缺陷：
逐文件按行对比 源APK(英文) 与 工程(中文)，找出
  工程中相邻两行的中文完全相同，而源APK 对应两行的英文不同
这种情况 = 真实错译（第二行本该是别的内容）。
"""
import io
import os
import re
import sys

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
        s = line.rstrip()
        m = SAY.match(s)
        if not m:
            continue
        out.append((i, (m.group(2) or "").strip(), m.group(3)))
    return out


def main():
    for label, gd, srcdir in PAIRS:
        print("=" * 94)
        print("### %s" % label)
        chapter_dirs = [d for d in os.listdir(gd)
                        if os.path.isdir(os.path.join(gd, d))]
        total = 0
        for cd in sorted(chapter_dirs):
            for f in sorted(os.listdir(os.path.join(gd, cd))):
                if not f.endswith(".rpy"):
                    continue
                sp = os.path.join(srcdir, "x-" + cd, "x-" + f)
                if not os.path.exists(sp):
                    continue
                nr = rows(os.path.join(gd, cd, f))
                orow = rows(sp)
                if len(nr) != len(orow):
                    continue
                for k in range(1, len(nr)):
                    nzh, nz1, nz2 = nr[k - 1][2], nr[k - 1][1], nr[k][1]
                    cur = nr[k][2]
                    prev_en = orow[k - 1][2]
                    cur_en = orow[k][2]
                    if not (CJK.search(cur) and CJK.search(nzh)):
                        continue
                    if cur != nzh:
                        continue
                    if cur_en == prev_en:
                        continue   # 原文本来就重复，合法
                    total += 1
                    print("  %s/%s L%d&L%d" % (cd, f, nr[k - 1][0], nr[k][0]))
                    print("     EN_prev : %s" % prev_en[:95])
                    print("     EN_cur  : %s" % cur_en[:95])
                    print("     ZH_both : %s" % cur[:95])
        print("  >>> 真错译合计: %d" % total)
        print()


if __name__ == "__main__":
    main()
