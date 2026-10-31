# -*- coding: utf-8 -*-
"""检查 matsuribayashi 里已 __() 包裹的 save_name 是否都有 zz_common 译文。"""
import io
import os
import re

ROOT = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game"
COMMON = os.path.join(ROOT, "tl", "schinese", "zz_common.rpy")
D = os.path.join(ROOT, "matsuribayashi")

WRE = re.compile(r'^\s*\$ save_name = __\("((?:[^"\\]|\\.)*)"', re.M)
OLD_RE = re.compile(r'^\s*old "((?:[^"\\]|\\.)*)"', re.M)

common = io.open(COMMON, encoding='utf-8').read()
olds = set(m.group(1).replace('\\n', '\n') for m in OLD_RE.finditer(common))

missing = {}
n = 0
for f in sorted(os.listdir(D)):
    if not f.endswith('.rpy'):
        continue
    t = io.open(os.path.join(D, f), encoding='utf-8').read()
    for m in WRE.finditer(t):
        n += 1
        inner = m.group(1).replace('\\n', '\n')
        if inner not in olds:
            missing.setdefault(inner, []).append("%s:%d" % (f, t[:m.start()].count('\n') + 1))

print("matsuribayashi wrapped save_name:", n)
print("distinct missing:", len(missing))
for k in sorted(missing):
    print("  MISS", repr(k), "x%d" % len(missing[k]), missing[k][0])
