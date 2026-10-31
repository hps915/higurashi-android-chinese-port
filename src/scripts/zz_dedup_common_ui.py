# -*- coding: utf-8 -*-
"""把 zz_common_ui.rpy 里与 zz_ui.rpy 重复的条目剔除，只保留 zz_ui 没有的。"""
import io
import os
import re
import sys

K = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game"
UI = os.path.join(K, "zz_ui.rpy")
COMMONUI = os.path.join(K, "tl", "schinese", "zz_common_ui.rpy")

PAIR = re.compile(r'^    old "((?:[^"\\]|\\.)*)"\n    new "((?:[^"\\]|\\.)*)"\n', re.M)


def main():
    ui_t = io.open(UI, encoding='utf-8').read()
    ui_olds = set(m.group(1) for m in PAIR.finditer(ui_t))
    # 也可能有 old/new 中间夹空行
    ui_olds |= set(re.findall(r'^\s*old "((?:[^"\\]|\\.)*)"', ui_t, re.M))

    cu = io.open(COMMONUI, encoding='utf-8').read()
    kept = []
    dropped = []
    for m in PAIR.finditer(cu):
        old, new = m.group(1), m.group(2)
        if old in ui_olds:
            dropped.append(old)
        else:
            kept.append((old, new))

    print("zz_ui olds:", len(ui_olds))
    print("zz_common_ui pairs:", len(kept) + len(dropped))
    print("  dropped (already in zz_ui):", len(dropped))
    print("  kept:", len(kept))

    lines = [u'# -*- coding: utf-8 -*-',
             u'# 第 8 轮：解题篇界面文案补译（zz_ui.rpy 未覆盖的部分）',
             u'# 由 work/scripts/zz_dedup_common_ui.py 生成',
             u'translate schinese strings:']
    for old, new in kept:
        lines.append(u'    old "%s"' % old)
        lines.append(u'    new "%s"' % new)
    io.open(COMMONUI, 'w', encoding='utf-8', newline='\n').write(u'\n'.join(lines) + u'\n')
    print("written", COMMONUI)


if __name__ == '__main__':
    main()
