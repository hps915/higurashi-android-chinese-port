# -*- coding: utf-8 -*-
"""第 8 轮 3.1c：解题篇 save_name 补翻译。

做两件事：
 1) 把 meakashi / tsumihoroboshi / minagoroshi / matsuribayashi 里
    形如 `$ save_name = "Xxx"` 的裸字符串改成 `$ save_name = __("Xxx")`
 2) 把用到的字符串追加到 tl/schinese/zz_common.rpy（去重）
顺带修 tsum_009.rpy 的拼写 "Tsumihorobosh-hen" -> "Tsumihoroboshi-hen"。
"""
import io
import os
import re

ROOT = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game"
COMMON = os.path.join(ROOT, "tl", "schinese", "zz_common.rpy")
DIRS = ("meakashi", "tsumihoroboshi", "minagoroshi", "matsuribayashi")

SAVE_RE = re.compile(r'^(\s*)\$ save_name = "((?:[^"\\]|\\.)*)"\s*$')
OLD_RE = re.compile(r'^\s*old "((?:[^"\\]|\\.)*)"', re.M)

# 英文原串（字面，含 \n 转义） -> 中文译文（用真实换行）
TRANS = {
    "Meakashi-hen.\\n": u"目明篇\n",
    "Meakashi-hen.\\nBADEND": u"目明篇\n坏结局",
    "Meakashi-hen.\\nEpilogue": u"目明篇\n尾声",
    "Staff Room.\\nMeakashi-hen": u"Staff Room\n目明篇",
    "Tsumihoroboshi-hen.\\n": u"罪灭篇\n",
    "Tsumihoroboshi-hen.\\nPrologue": u"罪灭篇\n序章",
    "Staff Room.\\nTsumihoroboshi-hen": u"Staff Room\n罪灭篇",
    "Minagoroshi-hen.\\n": u"皆杀篇\n",
    "Minagoroshi-hen.\\nEpilogue. Emergency Manual 34": u"皆杀篇\n尾声 紧急手册34",
    "Minagoroshi-hen.\\nEpilogue. Massacre": u"皆杀篇\n尾声 惨剧",
    "Minagoroshi-hen.\\nPrologue": u"皆杀篇\n序章",
    "Staff Room.\\nMinagoroshi-hen": u"Staff Room\n皆杀篇",
    "Connecting Fragments.\\nResearch is going well": u"碎片连接\n研究进展顺利",
    "Connecting Fragments.\\nThe second sacrifice": u"碎片连接\n第二个牺牲者",
    "Connecting Fragments.\\nThe third sacrifice": u"碎片连接\n第三个牺牲者",
    "Connecting Fragments.\\nAn accident at the Shirakawa park": u"碎片连接\n白川公园的事故",
}

# 拼写修正：旧串 -> 新串（在包裹之前做）
TYPO_FIX = {
    "Tsumihorobosh-hen.\\n": "Tsumihoroboshi-hen.\\n",
}


def main():
    used = set()
    changed_files = 0
    changed_lines = 0

    for d in DIRS:
        dd = os.path.join(ROOT, d)
        if not os.path.isdir(dd):
            continue
        for f in sorted(os.listdir(dd)):
            if not f.endswith('.rpy'):
                continue
            p = os.path.join(dd, f)
            src = io.open(p, encoding='utf-8').read()
            lines = src.split('\n')
            hit = 0
            for i, line in enumerate(lines):
                m = SAVE_RE.match(line)
                if not m:
                    continue
                indent, body = m.group(1), m.group(2)
                fixed = TYPO_FIX.get(body, body)
                lines[i] = u'%s$ save_name = __("%s")' % (indent, fixed)
                used.add(fixed)
                hit += 1
            if hit:
                io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
                changed_files += 1
                changed_lines += hit

    print("wrapped: %d files, %d statements" % (changed_files, changed_lines))
    print("distinct strings:", len(used))
    for s in sorted(used):
        if s not in TRANS:
            print("  !! NO TRANSLATION FOR:", repr(s))

    # 追加到 zz_common
    common = io.open(COMMON, encoding='utf-8').read()
    existing = set(m.group(1) for m in OLD_RE.finditer(common))

    add = [(s, TRANS[s]) for s in sorted(used) if s in TRANS and s not in existing]
    if not add:
        print("zz_common: nothing to add")
        return
    if not common.endswith('\n'):
        common += '\n'
    common += u'\n    # --- 第 8 轮：解题篇 save_name 章节名补译 ---\n'
    for old, new in add:
        common += u'    old "%s"\n    new "%s"\n' % (old, new)
    io.open(COMMON, 'w', encoding='utf-8', newline='\n').write(common)
    print("zz_common: added %d entries" % len(add))
    for old, new in add:
        print("   ", repr(old), "->", repr(new))


if __name__ == '__main__':
    main()
