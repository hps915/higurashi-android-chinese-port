# -*- coding: utf-8 -*-
"""修复 `r "中文"{nw}` -> `r "中文{nw}"`。

原版的正确写法是 {nw} 在字符串内部（如 `r "……{w=1.0}{nw}"`）。
zz_short_align.py 回写时误放到了引号外，导致 Ren'Py 报 "end of line expected"。
"""
import io
import os
import re
import sys

BASES = [r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project\game",
         r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game"]

BAD = re.compile(r'^(.*)"\{nw\}[ \t]*$')


def main():
    apply = '--apply' in sys.argv
    total = 0
    all_files = []
    for base in BASES:
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in ('cache', 'saves')]
            for f in files:
                if not f.endswith('.rpy'):
                    continue
                p = os.path.join(root, f)
                lines = io.open(p, encoding='utf-8').read().split('\n')
                changed = 0
                for i, l in enumerate(lines):
                    s = l.rstrip()
                    m = BAD.match(s)
                    if not m:
                        continue
                    lines[i] = m.group(1) + '{nw}"'
                    changed += 1
                if changed:
                    total += changed
                    rel = os.path.relpath(p, base).replace('\\', '/')
                    all_files.append((rel, changed))
                    if apply:
                        io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    for rel, n in all_files:
        print("%-52s %d" % (rel, n))
    print()
    print("TOTAL fixed:", total, "(apply=%s)" % apply)


if __name__ == '__main__':
    main()
