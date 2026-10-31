# -*- coding: utf-8 -*-
"""逐个输出相邻重复台词及其上下文，判断是真实重复还是正常排版。"""
import io
import os
import re
import sys

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
CJK = re.compile(u'[\u4e00-\u9fff]')
SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*$')


def main():
    gd = sys.argv[1]
    out = []
    for root, dirs, files in os.walk(gd):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in sorted(files):
            if not f.endswith(".rpy"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, gd).replace("\\", "/")
            lines = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
            prev = None
            prev_at = 0
            for i, line in enumerate(lines, 1):
                m = SAY.match(line.rstrip())
                if not m:
                    continue
                b = m.group(3)
                if not CJK.search(b) or len(b) < 10:
                    prev = b
                    prev_at = i
                    continue
                if b == prev:
                    out.append((rel, prev_at, i, lines[prev_at - 1].strip()[:110],
                                lines[i - 1].strip()[:110]))
                prev = b
                prev_at = i
    print("%s  相邻重复: %d" % (gd.split(os.sep)[-2], len(out)))
    for rel, a, b, la, lb in out:
        print("  %s  L%d & L%d" % (rel, a, b))
        print("      A: %s" % la)
        print("      B: %s" % lb)


if __name__ == "__main__":
    main()
