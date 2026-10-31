# -*- coding: utf-8 -*-
"""修正 H170 条目：去掉多余的「记录」后缀，与正文「H170」保持一致。"""
import io

P = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game\tl\schinese\zz_common.rpy"
BS = chr(92)

OLD = u'    new "碎片连接' + BS + u'nH170 记录"'
NEW = u'    new "碎片连接' + BS + u'nH170"'


def main():
    s = io.open(P, encoding='utf-8').read()
    if OLD not in s:
        print("未找到，当前含 H170 的行:")
        for l in s.split('\n'):
            if 'H170' in l:
                print(repr(l))
        return
    s = s.replace(OLD, NEW)
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
    print("已修正")
    for l in s.split('\n'):
        if 'H170' in l:
            print(repr(l))


if __name__ == '__main__':
    main()
