# -*- coding: utf-8 -*-
"""检测「非重复型」错位：译文与源英文语义完全不符。

用一个稳健代理指标：
  对每行计算 (中文有效字数 / 英文词数) 的比值。
  正常区间 1.0~2.6（中文比英文紧凑）。
  若某行比值明显偏离，且与相邻行的一样，则可能串行。

但更可靠的是：检查「译文长度突变」——
  相邻行比值差 > 4 倍，说明某行拿错了内容。
只报告，不修改。
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
TAG = re.compile(r'\{[^{}]*\}')
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
        n = 0
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
                for k in range(len(nr)):
                    zh = TAG.sub("", nr[k][2])
                    en = TAG.sub("", orow[k][2])
                    if not CJK.search(zh):
                        continue
                    zc = len(CJK.findall(zh))
                    ew = len(re.findall(r"[A-Za-z']+", en))
                    if ew < 4 or zc < 3:
                        continue
                    r = zc / float(ew)
                    if r < 0.55 or r > 4.2:
                        n += 1
                        if n <= 120:
                            print("  %s/%s L%d ratio=%.2f" % (cd, f, nr[k][0], r))
                            print("     EN: %s" % en[:100])
                            print("     ZH: %s" % zh[:100])
        print("  可疑 %d 条" % n)
        print()


if __name__ == "__main__":
    main()
