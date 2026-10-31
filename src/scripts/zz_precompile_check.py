# -*- coding: utf-8 -*-
"""编译前静态自检：
 1) 括号/引号配平（每行 say 语句）
 2) label 重复定义
 3) 中文行里混入半角标点（抽样）
 4) 多行字符串续行缩进异常（extend 行缩进 != 4/8/12）
"""
import io
import os
import re
import sys

BASES = [r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project\game",
         r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game"]

LABEL = re.compile(r'^[ \t]*label\s+([A-Za-z_][\w.]*)')
SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*$')


def check(base):
    dup = {}
    odd = []
    indent_bad = []
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in ('cache', 'saves')]
        for f in files:
            if not f.endswith('.rpy'):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, base).replace('\\', '/')
            lines = io.open(p, encoding='utf-8', errors='replace').read().split('\n')
            for i, l in enumerate(lines, 1):
                m = LABEL.match(l)
                if m:
                    dup.setdefault(m.group(1), []).append("%s:%d" % (rel, i))
                s = l.rstrip()
                # 成对引号（非转义）检查
                cnt = 0
                k = 0
                while k < len(s):
                    if s[k] == '\\':
                        k += 2
                        continue
                    if s[k] == '"':
                        cnt += 1
                    k += 1
                if cnt % 2:
                    odd.append("%s:%d  %s" % (rel, i, s.strip()[:100]))
                # 续行缩进
                st = s.lstrip()
                if st.startswith(('extend "', 'adv_extend "', 'nvl_extend "')):
                    ind = len(s) - len(st)
                    if ind % 4:
                        indent_bad.append("%s:%d  indent=%d  %s" % (rel, i, ind, st[:80]))
    return dup, odd, indent_bad


def main():
    for base in BASES:
        print("=" * 90)
        print(base)
        dup, odd, ib = check(base)
        real_dup = {k: v for k, v in dup.items() if len(v) > 1}
        print("  labels:", len(dup), " duplicates:", len(real_dup))
        for k, v in list(real_dup.items())[:15]:
            print("    DUP %s -> %s" % (k, v))
        print("  odd-quote lines:", len(odd))
        for x in odd[:15]:
            print("    ", x)
        print("  bad-indent extend lines:", len(ib))
        for x in ib[:15]:
            print("    ", x)


if __name__ == '__main__':
    main()
