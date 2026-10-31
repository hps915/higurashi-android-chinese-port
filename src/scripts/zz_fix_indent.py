# -*- coding: utf-8 -*-
"""把断句产生的续行缩进统一为 4 空格（与父级语句同级）。"""
import io
import os

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"

FIXES = [
    (os.path.join(BASE, "work", "project_k", "game", "minagoroshi", "mina_013.rpy"), 1997, 1999),
    (os.path.join(BASE, "work", "project_k", "game", "matsuribayashi",
                  "matsuribayashi_kakera_02.rpy"), 2262, 2264),
    (os.path.join(BASE, "work", "project_k", "game", "meakashi", "meak_007.rpy"), 658, 659),
    (os.path.join(BASE, "work", "project_k", "game", "minagoroshi", "mina_ep.rpy"), 45, 47),
    (os.path.join(BASE, "work", "project", "game", "himatsubushi", "hima_001.rpy"), 1098, 1099),
]

INDENT = 4


def main():
    for p, a, b in FIXES:
        lines = io.open(p, encoding='utf-8').read().split('\n')
        for i in range(a, b + 1):
            idx = i - 1
            if idx < len(lines):
                lines[idx] = ' ' * INDENT + lines[idx].lstrip()
        io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
        print("fixed", os.path.basename(p), a, b)


if __name__ == '__main__':
    main()
