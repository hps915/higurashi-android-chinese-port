# -*- coding: utf-8 -*-
"""第 8 轮：解题篇 zz_common 英文残留 + 误写换行 修复。"""
import io
import re
import sys

P = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game\tl\schinese\zz_common.rpy"

# new 值 -> 新 new 值（键里 \\n 表示文件中的字面反斜杠 n）
NEWMAP = {
    u"碎片连接\\nC103 投药实验": u"碎片连接\\nC103 投药实验",
    u"碎片连接\\nH170": u"碎片连接\\nH170 记录",
    u"DEAD END 交响曲": u"死亡终局交响曲",
    u"禁用 OP": u"禁用开场动画",
    u"启用 OP": u"启用开场动画",
    u"祭囃篇\\n#3 Koizumi-sensei": u"祭囃篇\\n#3 小泉老师",
    u"祭囃篇\\nConnecting Fragments. End": u"祭囃篇\\n碎片连接 终",
    u"祭囃篇\\nConnecting Fragments. Prologue": u"祭囃篇\\n碎片连接 序",
    u"祭囃篇\\nEND": u"祭囃篇\\n结局",
    u"祭囃篇\\nOnigari-no-ryuuou": u"祭囃篇\\n鬼狩之龙王",
    u"Staff Room\\n祭囃篇": u"Staff Room\\n祭囃篇",
    u"TIPS 菜单": u"知识菜单",
}

PAIR = re.compile(r'(^\s*old "(?:[^"\\]|\\.)*"\s*\n\s*new ")((?:[^"\\]|\\.)*)(")', re.M)

# 误写成真实换行的三条（new "Staff Room<换行>目明篇"）
BROKEN = [
    (u'new "Staff Room\n目明篇"', u'new "Staff Room\\n目明篇"'),
    (u'new "Staff Room\n皆杀篇"', u'new "Staff Room\\n皆杀篇"'),
    (u'new "Staff Room\n罪灭篇"', u'new "Staff Room\\n罪灭篇"'),
]


def main():
    apply = '--apply' in sys.argv
    t = io.open(P, encoding='utf-8').read()

    hits = []

    def sub(m):
        new = m.group(2)
        if new in NEWMAP and NEWMAP[new] != new:
            hits.append((new, NEWMAP[new]))
            return m.group(1) + NEWMAP[new] + m.group(3)
        return m.group(0)

    t2 = PAIR.sub(sub, t)
    print("new-value replacements:", len(hits))
    for a, b in hits:
        print("   %-45s -> %s" % (a[:45], b[:45]))

    n_broken = 0
    for old, new in BROKEN:
        if old in t2:
            t2 = t2.replace(old, new)
            n_broken += 1
    print("broken-newline fixes:", n_broken, "/", len(BROKEN))

    if apply:
        io.open(P, 'w', encoding='utf-8', newline='\n').write(t2)
        print("written")
    else:
        print("(dry-run)")


if __name__ == '__main__':
    main()
