# -*- coding: utf-8 -*-
"""修正 tsum_005.rpy 413/461 行的引号转义（上一次写成了 \\"" 而非 \\"）。"""
import io

P = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game\tsumihoroboshi\tsum_005.rpy"
BS = chr(92)

FIX = [
    (413, u'    r "' + BS + u'"\u2026\u5df2\u7ecf{w=1.0}\u592a{w=1.2}\u8fdf\u4e86\u3002' + BS + u'""'),
    (461, u'    r "\u6211\u56de\u7b54\u8bf4\uff0c{w=0.6}' + BS + u'"\u6211\u8ba4\u8bc6\u3002' + BS + u'""'),
]


def main():
    lines = io.open(P, encoding='utf-8').read().split('\n')
    for ln, new in FIX:
        i = ln - 1
        print("BEFORE:", repr(lines[i]))
        lines[i] = new
        print("AFTER :", repr(lines[i]))
    io.open(P, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print("written")


if __name__ == '__main__':
    main()
