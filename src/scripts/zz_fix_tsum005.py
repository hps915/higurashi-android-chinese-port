# -*- coding: utf-8 -*-
"""补译 tsum_005.rpy 最后 2 条短英文行。"""
import io
import os

P = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game\tsumihoroboshi\tsum_005.rpy"
BS = chr(92)

JOBS = [
    (413, u'    r "' + BS + '""…已经{w=1.0}太{w=1.2}迟了。"' + BS + '""'),
    (461, u'    r "我回答说，{w=0.6}' + BS + '""我认识。"' + BS + '""'),
]


def main():
    lines = io.open(P, encoding='utf-8').read().split('\n')
    for ln, new in JOBS:
        i = ln - 1
        print("BEFORE %d: %s" % (ln, lines[i].strip()))
        lines[i] = new
        print("AFTER  %d: %s" % (ln, lines[i].strip()))
    io.open(P, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print("written")


if __name__ == '__main__':
    main()
