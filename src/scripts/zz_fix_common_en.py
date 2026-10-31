# -*- coding: utf-8 -*-
"""第 8 轮 3.3：出题篇 zz_common 里 new 值仍含英文的条目补译（29 条）。"""
import io
import re
import sys

P = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project\game\tl\schinese\zz_common.rpy"

NEWMAP = {
    u"全员座谈会\\nHimatsubushi-hen": u"全员座谈会\\n暇溃篇",
    u"全员座谈会\\nOnikakushi-hen": u"全员座谈会\\n鬼隐篇",
    u"全员座谈会\\nTatarigoroshi-hen": u"全员座谈会\\n祟杀篇",
    u"全员座谈会\\nWatanagashi-hen": u"全员座谈会\\n绵流篇",
    u"DEAD END 交响曲": u"死亡终局交响曲",
    u"禁用 OP": u"禁用开场动画",
    u"启用 OP": u"启用开场动画",
    u"暇溃篇\\nBAD END": u"暇溃篇\\n坏结局",
    u"鬼隐篇\\nEND": u"鬼隐篇\\n结局",
    u"TIPS 菜单": u"知识菜单",
    u"祟杀篇\\nDay 10, calling Mion": u"祟杀篇\\n第10天 打电话给魅音",
    u"祟杀篇\\nDay 11, burying the body": u"祟杀篇\\n第11天 掩埋尸体",
    u"祟杀篇\\nDay 11, cold blood": u"祟杀篇\\n第11天 冷血",
    u"祟杀篇\\nDay 11, my own path": u"祟杀篇\\n第11天 我自己的路",
    u"祟杀篇\\nDay 12, he's alive?": u"祟杀篇\\n第12天 他还活着？",
    u"祟杀篇\\nDay 13, Satoko's house": u"祟杀篇\\n第13天 沙都子的家",
    u"祟杀篇\\nDay 14, END": u"祟杀篇\\n第14天 结局",
    u"祟杀篇\\nDay 8, evening": u"祟杀篇\\n第8天 傍晚",
    u"祟杀篇\\nDay 9, a plea to Mion": u"祟杀篇\\n第9天 向魅音恳求",
    u"祟杀篇\\nEpilogue, cassette tape": u"祟杀篇\\n尾声 录音带",
    u"绵流篇\\nDay 10, Rika-chan's safety": u"绵流篇\\n第10天 梨花的安全",
    u"绵流篇\\nDay 10, about the Three Families": u"绵流篇\\n第10天 关于御三家",
    u"绵流篇\\nDay 10, call from Shion": u"绵流篇\\n第10天 诗音的来电",
    u"绵流篇\\nDay 11, new call": u"绵流篇\\n第11天 新的来电",
    u"绵流篇\\nDay 11-02": u"绵流篇\\n第11天之二",
    u"绵流篇\\nDay 12, Sonozaki main house": u"绵流篇\\n第12天 园崎本家",
    u"绵流篇\\nDay 12, torture": u"绵流篇\\n第12天 拷问",
    u"绵流篇\\nDay 9, evening call": u"绵流篇\\n第9天 傍晚的来电",
    u"绵流篇\\nEpilogue, The End": u"绵流篇\\n尾声 剧终",
}

PAIR = re.compile(r'(^\s*old "(?:[^"\\]|\\.)*"\s*\n\s*new ")((?:[^"\\]|\\.)*)(")', re.M)


def main():
    apply = '--apply' in sys.argv
    t = io.open(P, encoding='utf-8').read()
    hits = []

    def sub(m):
        new = m.group(2)
        if new in NEWMAP:
            hits.append((new, NEWMAP[new]))
            return m.group(1) + NEWMAP[new] + m.group(3)
        return m.group(0)

    t2 = PAIR.sub(sub, t)
    print("replaced:", len(hits), "/ expected", len(NEWMAP))
    missed = set(NEWMAP) - set(x[0] for x in hits)
    for k in missed:
        print("  MISSING in file:", k)
    if apply:
        io.open(P, 'w', encoding='utf-8', newline='\n').write(t2)
        print("written")
    else:
        print("(dry-run)")


if __name__ == '__main__':
    main()
