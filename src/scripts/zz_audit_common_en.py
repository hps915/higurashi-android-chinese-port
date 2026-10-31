# -*- coding: utf-8 -*-
"""找出 zz_common 里 new 值仍含英文单词的条目（出题篇）。"""
import io
import re

P = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project\game\tl\schinese\zz_common.rpy"

PAIR = re.compile(r'^\s*old "((?:[^"\\]|\\.)*)"\s*\n\s*new "((?:[^"\\]|\\.)*)"', re.M)
WORD = re.compile(r'[A-Za-z]{2,}')


def main():
    t = io.open(P, encoding='utf-8').read()
    n = 0
    for m in PAIR.finditer(t):
        old, new = m.group(1), m.group(2)
        if WORD.search(new):
            n += 1
            ln = t[:m.start()].count('\n') + 1
            print("%5d  OLD %s" % (ln, old[:70]))
            print("       NEW %s" % new[:70])
    print()
    print("count:", n)


if __name__ == '__main__':
    main()
