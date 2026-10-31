# -*- coding: utf-8 -*-
"""修复 zz_common.rpy 里被误写成真实换行的 new 值。

zz_fix_savename.py 当初用 u'\n' 拼接（真实换行），应当写成字面反斜杠 n。
这里把「new "开头、下一行以中文开头且以"结尾」的模式合并回单行。
"""
import io
import os
import re
import sys

P = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game\tl\schinese\zz_common.rpy"
BS = chr(92)
CJK = re.compile(u'[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]')


def main():
    apply = '--apply' in sys.argv
    t = io.open(P, encoding='utf-8').read()
    lines = t.split('\n')
    out = []
    i = 0
    fixed = 0
    while i < len(lines):
        cur = lines[i]
        st = cur.strip()
        # 形如:  <indent>new "<中文>    且本行引号数为奇数
        if st.startswith('new "') and st.count('"') % 2 == 1:
            nxt = lines[i + 1] if i + 1 < len(lines) else ''
            nst = nxt.strip()
            # 下一行是纯中文 + 结束引号
            if nst.endswith('"') and nst.count('"') == 1 and CJK.search(nst):
                indent = cur[:len(cur) - len(cur.lstrip())]
                merged = indent + st + BS + 'n' + nst
                out.append(merged)
                fixed += 1
                i += 2
                continue
            # 下一行只有一个结束引号（new "目明篇  +  "）
            if nst == '"':
                indent = cur[:len(cur) - len(cur.lstrip())]
                merged = indent + st + BS + 'n"'
                out.append(merged)
                fixed += 1
                i += 2
                continue
        out.append(cur)
        i += 1
    print("merged lines:", fixed)
    if apply:
        io.open(P, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
        print("written")
    else:
        for j in range(1, min(len(out), 60)):
            pass
        print("(dry-run)")


if __name__ == '__main__':
    main()
