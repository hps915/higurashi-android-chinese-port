# -*- coding: utf-8 -*-
"""列出解题篇 screens.rpy / music_list_kai.rpy 里 _() 字符串的覆盖情况（已译 / 未译）。"""
import io
import os
import re

ROOT = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game"
COMMON = os.path.join(ROOT, "tl", "schinese", "zz_common.rpy")
FILES = ["screens.rpy", "music_list_kai.rpy"]

UI_RE = re.compile(r'_\(\s*["\']((?:[^"\\\'"]|\\.)*)["\']')
OLD_RE = re.compile(r'^\s*old "((?:[^"\\]|\\.)*)"', re.M)
CJK = re.compile(u'[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]')


def main():
    common = io.open(COMMON, encoding='utf-8').read()
    olds = set(m.group(1) for m in OLD_RE.finditer(common))
    seen = {}
    for fn in FILES:
        t = io.open(os.path.join(ROOT, fn), encoding='utf-8').read()
        for m in UI_RE.finditer(t):
            s = m.group(1)
            ln = t[:m.start()].count('\n') + 1
            seen.setdefault(s, []).append("%s:%d" % (fn, ln))
    cov = [s for s in seen if s in olds or CJK.search(s)]
    mis = [s for s in seen if s not in olds and not CJK.search(s)]
    print("=== COVERED (%d) ===" % len(cov))
    for s in sorted(cov):
        print("  ", s)
    print()
    print("=== MISSING (%d) ===" % len(mis))
    for s in sorted(mis):
        print("  ", s)


if __name__ == '__main__':
    main()
