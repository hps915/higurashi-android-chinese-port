# -*- coding: utf-8 -*-
"""统计解题篇 screens.rpy / music_list_kai.rpy 的 _() 字符串覆盖情况。
覆盖来源：game/tl/schinese/ 下所有 .rpy 的 old/new 条目。
"""
import io
import os
import re

ROOT = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game"
TL = os.path.join(ROOT, "tl", "schinese")
FILES = ["screens.rpy", "music_list_kai.rpy"]
OUT = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\scripts\zz_ui_missing.txt"

CJK = re.compile(u'[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]')
OLD_RE = re.compile(r'^\s*old "((?:[^"\\]|\\.)*)"', re.M)


def extract_calls(text, call='_('):
    i = 0
    n = len(text)
    while True:
        j = text.find(call, i)
        if j < 0:
            return
        k = j + len(call)
        while k < n and text[k] in ' \t':
            k += 1
        if k >= n or text[k] not in '"\'':
            i = j + 1
            continue
        q = text[k]
        k += 1
        buf = []
        while k < n:
            c = text[k]
            if c == '\\' and k + 1 < n:
                buf.append(c)
                buf.append(text[k + 1])
                k += 2
                continue
            if c == q:
                break
            buf.append(c)
            k += 1
        yield j, ''.join(buf)
        i = k + 1


def load_olds():
    olds = set()
    for f in os.listdir(TL):
        if not f.endswith('.rpy'):
            continue
        t = io.open(os.path.join(TL, f), encoding='utf-8').read()
        for m in OLD_RE.finditer(t):
            olds.add(m.group(1))
    return olds


def main():
    olds = load_olds()
    seen = []
    idx = {}
    for fn in FILES:
        t = io.open(os.path.join(ROOT, fn), encoding='utf-8').read()
        for off, s in extract_calls(t):
            if s in olds or CJK.search(s):
                continue
            if s in idx:
                continue
            idx[s] = 1
            seen.append((s, "%s:%d" % (fn, t[:off].count('\n') + 1)))
    with io.open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        for s, loc in seen:
            f.write(s + u'\n')
    for s, loc in seen:
        print("%-58s %s" % (s, loc))
    print()
    print("missing:", len(seen), " covered-olds:", len(olds))


if __name__ == '__main__':
    main()
