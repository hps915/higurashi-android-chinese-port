# -*- coding: utf-8 -*-
"""审计：解题篇 save_name 是否有 zz_common 翻译覆盖。
用法: python work/scripts/zz_audit_savename.py
"""
import io
import os
import re
import sys

ROOT = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game"
COMMON = os.path.join(ROOT, "tl", "schinese", "zz_common.rpy")

OLD_RE = re.compile(r'^\s*old "((?:[^"\\]|\\.)*)"', re.M)
SAVE_RE = re.compile(r'^(\s*)\$ save_name = (.*)$')


def unesc(s):
    return s.replace('\\n', '\n')


def main():
    common = io.open(COMMON, encoding='utf-8').read()
    olds = set(unesc(m.group(1)) for m in OLD_RE.finditer(common))

    groups = {}
    order = []
    for d in ("meakashi", "tsumihoroboshi", "minagoroshi", "matsuribayashi"):
        dd = os.path.join(ROOT, d)
        if not os.path.isdir(dd):
            continue
        for f in sorted(os.listdir(dd)):
            if not f.endswith('.rpy'):
                continue
            p = os.path.join(dd, f)
            for i, line in enumerate(io.open(p, encoding='utf-8'), 1):
                m = SAVE_RE.match(line.rstrip('\n'))
                if not m:
                    continue
                expr = m.group(2).strip()
                key = expr
                if key not in groups:
                    groups[key] = []
                    order.append(key)
                groups[key].append("%s/%s:%d" % (d, f, i))

    tot = already = 0
    missing = []
    nonliteral = []
    for key in order:
        locs = groups[key]
        tot += len(locs)
        if key.startswith('__("'):
            already += len(locs)
            inner = unesc(key[4:key.rfind('"')])
            if inner not in olds and not inner.startswith('Matsuribayashi-hen'):
                missing.append((key, locs, 'ALREADY__BUT_NO_COMMON'))
            continue
        if key.startswith('"'):
            inner = unesc(key[1:key.rfind('"')])
            if inner not in olds:
                missing.append((key, locs, 'BARE_NO_COMMON'))
            continue
        nonliteral.append((key, locs))

    print("save_name 语句总数:", tot)
    print("已用 __() 包裹:", already)
    print("未包裹且 zz_common 无译文:", sum(len(l) for _, l, _ in missing), "处 /", len(missing), "种字符串")
    print("非字面量表达式:", len(nonliteral))
    print()
    for key, locs, why in missing:
        print("%s  x%d  %s" % (why, len(locs), key[:110]))
        for l in locs:
            print("      ", l)
    print()
    for key, locs in nonliteral:
        print("NONLIT  x%d  %s" % (len(locs), key[:110]))
        for l in locs[:5]:
            print("      ", l)


if __name__ == '__main__':
    main()
