# -*- coding: utf-8 -*-
"""预览 halfwidth comma 修复效果（前 N 条）。"""
import io
import re

P = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game\matsuribayashi\mats_012.rpy"
CJK = re.compile(u'[\u4e00-\u9fff]')
SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|extend\s+)?"((?:[^"\\]|\\.)*)"\s*$')
PAT = re.compile(u'([\u4e00-\u9fff\u3001\u3002\uff0c\uff1f\uff01\u2026])([ \t]*,)[ \t]*([\u4e00-\u9fff])')


def main():
    lines = io.open(P, encoding='utf-8').read().split('\n')
    shown = 0
    for i, l in enumerate(lines, 1):
        m = SAY.match(l.rstrip())
        if not m:
            continue
        body = m.group(3)
        if not CJK.search(body):
            continue
        nb, n = PAT.subn(u'\\1\uff0c\\3', body)
        if n and shown < 8:
            print("%d BEFORE: %s" % (i, body[:84]))
            print("%d AFTER : %s" % (i, nb[:84]))
            print()
            shown += 1


if __name__ == '__main__':
    main()
