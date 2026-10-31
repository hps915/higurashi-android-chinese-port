# -*- coding: utf-8 -*-
"""审计：解题篇 screens.rpy / music_list_kai.rpy 里 _("...") 的英文串，
统计哪些没有 zz_common 译文覆盖。输出到 work/scripts/zz_ui_missing.txt
"""
import io
import os
import re

ROOT = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game"
COMMON = os.path.join(ROOT, "tl", "schinese", "zz_common.rpy")
FILES = ["screens.rpy", "music_list_kai.rpy"]

UI_RE = re.compile(r'_\("((?:[^"\\]|\\.)*)"')
OLD_RE = re.compile(r'^\s*old "((?:[^"\\]|\\.)*)"', re.M)
CJK = re.compile(u'[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]')


def main():
    common = io.open(COMMON, encoding='utf-8').read()
    olds = set(m.group(1) for m in OLD_RE.finditer(common))

    seen = {}
    for fn in FILES:
        p = os.path.join(ROOT, fn)
        t = io.open(p, encoding='utf-8').read()
        for m in UI_RE.finditer(p, 0) if False else UI_RE.finditer(t):
            s = m.group(1)
            ln = t[:m.start()].count('\n') + 1
            seen.setdefault(s, []).append("%s:%d" % (fn, ln))

    missing = {s: l for s, l in seen.items() if s not in olds and not CJK.search(s)}
    have = len(seen) - len(missing)
    print("_() strings:", len(seen), " covered:", have, " missing:", len(missing))
    print()
    for s in sorted(missing):
        print("%-70s %s" % (s, missing[s][0]))


if __name__ == '__main__':
    main()
