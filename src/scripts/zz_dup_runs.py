# -*- coding: utf-8 -*-
"""三行窗口检测：A / B / C 三行中文相同但英文不同（连续串行）。

连续 2 行以上同文，若有任一行英文不同即缺陷。
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
        print("### %s" % label)
        runs = []
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
                if len(nr) != len(orow):
                    continue
                # 找连续同文段
                i = 0
                while i < len(nr):
                    zh = nr[i][2]
                    if not CJK.search(zh) or len(zh) < 10:
                        i += 1
                        continue
                    j = i + 1
                    while j < len(nr) and nr[j][2] == zh:
                        j += 1
                    if j - i >= 2:
                        ens = [orow[k][2] for k in range(i, j)]
                        if len(set(ens)) > 1:
                            runs.append((cd, f, nr[i][0], nr[j - 1][0], len(ens), zh, ens))
                    i = j
        print("  连续同文段且英文不同: %d" % len(runs))
        for cd, f, a, b, n, zh, ens in runs[:20]:
            print("   %s/%s L%d..L%d (%d 行连排同文)" % (cd, f, a, b, n))
            print("      ZH: %s" % zh[:90])
            for e in ens:
                print("      EN: %s" % e[:90])
        print()


if __name__ == "__main__":
    main()
