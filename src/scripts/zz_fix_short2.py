# -*- coding: utf-8 -*-
"""修补解题篇剩余 7 条短英文台词 + 出题篇同类问题。"""
import io
import os

K = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game"
Q = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project"

JOBS = [
    (K, "meakashi/meak_006.rpy", 1055, "So?", u"所以呢？"),
    (K, "meakashi/meak_006.rpy", 1058, "So?", u"所以呢？"),
    (K, "meakashi/meak_006.rpy", 1061, "So what?", u"那又怎样？"),
    (K, "meakashi/meak_020.rpy", 1881, "Shion......", u"诗音……"),
    (K, "meakashi/meak_020.rpy", 1901, "Mmph...", u"唔……"),
    (K, "meakashi/meak_020.rpy", 1921, "Live.", u"活下去。"),
    (K, "minagoroshi/mina_ep.rpy", 274, "January 1945", u"1945年1月"),
]


def apply(base, rel, ln, exp, new):
    p = os.path.join(base, rel.replace('/', os.sep))
    lines = io.open(p, encoding='utf-8').read().split('\n')
    i = ln - 1
    cur = lines[i]
    if exp not in cur:
        print("MISMATCH %s:%d  %r" % (rel, ln, cur.strip()[:90]))
        return False
    stripped = cur.lstrip()
    indent = cur[:len(cur) - len(stripped)]
    q = stripped.index('"')
    prefix = stripped[:q]
    lines[i] = indent + prefix + '"' + new + '"'
    io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print("ok %s:%d -> %s" % (rel, ln, lines[i].strip()))
    return True


def main():
    for job in JOBS:
        apply(*job)


if __name__ == '__main__':
    main()
