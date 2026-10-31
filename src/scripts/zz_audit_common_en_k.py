# -*- coding: utf-8 -*-
"""审计解题篇 tl/schinese 下所有 new 值仍含英文单词的条目。"""
import io
import os
import re

P = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game\tl\schinese"

PAIR = re.compile(r'^\s*old "((?:[^"\\]|\\.)*)"\s*\n\s*new "((?:[^"\\]|\\.)*)"', re.M)
WORD = re.compile(r'[A-Za-z]{2,}')


def main():
    total = 0
    for f in sorted(os.listdir(P)):
        if not f.endswith('.rpy'):
            continue
        t = io.open(os.path.join(P, f), encoding='utf-8').read()
        hits = []
        for m in PAIR.finditer(t):
            if WORD.search(m.group(2)):
                hits.append(m.group(2))
        if hits:
            total += len(hits)
            print("%-24s %d" % (f, len(hits)))
            for h in hits[:8]:
                print("      ", h[:80])
    print()
    print("TOTAL:", total)


if __name__ == '__main__':
    main()
