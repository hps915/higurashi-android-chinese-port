# -*- coding: utf-8 -*-
"""修复 zz_short_align.py 引入的缺陷：行尾 `"{nw}` -> `"{nw}"`。

原因：脚本回写时把 {nw} 追加到已经带闭合引号的字符串外面，
产生了 `r "中文"{nw}` 这种语法错误。
正确形式应为 `r "中文{nw}"`。
"""
import io
import os
import re
import sys

BASES = [r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project\game",
         r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game"]

BAD = re.compile(r'^(.*)"\{nw\}$')


def main():
    apply = '--apply' in sys.argv
    total = 0
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
                    m = BAD.match(l.rstrip())
                    if not m:
                        continue
                    # 把 "{nw} 改成 {nw}"
                    lines[i] = m.group(1) + '{nw}"'
                    changed += 1
                if changed:
                    total += changed
                    rel = os.path.relpath(p, base).replace('\\', '/')
                    print("%-50s %d" % (rel, changed))
                    if apply:
                        io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print()
    print("TOTAL fixed:", total, "(apply=%s)" % apply)


if __name__ == '__main__':
    main()
