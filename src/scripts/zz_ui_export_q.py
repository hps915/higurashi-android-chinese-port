# -*- coding: utf-8 -*-
"""审计出题篇 screens.rpy / zz_ui.rpy / music_list.rpy 里 _() 的英文串覆盖。"""
import io
import os
import re
import sys

ROOT = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project\game"
TL = os.path.join(ROOT, "tl", "schinese")
FILES = ["screens.rpy", "zz_ui.rpy", "music_list.rpy", "cg_gallery.rpy", "readback.rpy"]

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


def main():
    olds = set()
    for f in os.listdir(TL):
        if f.endswith('.rpy'):
            t = io.open(os.path.join(TL, f), encoding='utf-8').read()
            for m in OLD_RE.finditer(t):
                olds.add(m.group(1))
    seen = []
    idx = set()
    for fn in FILES:
        p = os.path.join(ROOT, fn)
        if not os.path.exists(p):
            continue
        t = io.open(p, encoding='utf-8').read()
        for off, s in extract_calls(t):
            if s in olds or CJK.search(s):
                continue
            if s in idx:
                continue
            idx.add(s)
            seen.append((s, "%s:%d" % (fn, t[:off].count('\n') + 1)))
    for s, loc in seen:
        print("%-56s %s" % (s, loc))
    print()
    print("missing:", len(seen))


if __name__ == '__main__':
    main()
