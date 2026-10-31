# -*- coding: utf-8 -*-
"""第 8 轮 3.2：出题篇 adv_extend 英文行补译。

对 work/project/game 下所有 adv_extend 且内容为英文的行做定点替换。
映射以 (相对路径, 行号) 为键，行号以执行时刻为准（脚本会校验原文一致）。
"""
import io
import os
import sys

GAME = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project\game"

# (rel_path, lineno, expected_prefix, new_text_with_quotes)
REPL = [
    ("himatsubushi/hima_001.rpy", 193,
     'adv_extend "Make sure you get your textbooks',
     'adv_extend "今天要好好整理明天上课用的课本，整理完再去睡觉哦。"'),
    ("onikakushi/onik_009_02.rpy", 571,
     'adv_extend "So they probably left Hinamizawa',
     'adv_extend "所以才故意选在这个时候去旅行，企图远离雏见泽不是吗？"'),
    ("onikakushi/onik_010.rpy", 912,
     'adv_extend "But when the officer checked',
     'adv_extend "但警察查看他是否还有气息时，立刻发现了异常。"'),
    ("onikakushi/onik_011.rpy", 1215,
     'adv_extend "It puts people off when I say',
     'adv_extend "我一说自己是警察，对方就会不自在啊。"'),
    ("onikakushi/onik_012.rpy", 343,
     'adv_extend "But you see. There doesn\'t seem',
     'adv_extend "不过啊。能让富竹先生出现那种反应的药物，似乎一种都找不到呢。"'),
    ("onikakushi/onik_012.rpy", 455,
     'adv_extend "Villagers with incurable illnesses',
     'adv_extend "举例来说，还有患了不治之症的村民被搬到鬼之渊，然后病就被治好了的故事。"'),
    ("onikakushi/onik_014.rpy", 1243,
     'adv_extend "He joined a baseball team',
     'adv_extend "他加入了棒球队……可他其实并不怎么喜欢棒球啊……！"'),
    ("onikakushi/onik_015.rpy", 1166,
     'adv_extend "I\'ll be able to understand you',
     'adv_extend "我一定能够理解圭一君的。"'),
    ("onikakushi/onikakushi_omake.rpy", 242,
     'adv_extend "The overly graphic depiction',
     'adv_extend "那段刻画得过于写实的画面，就是为了让玩家误以为是作祟而设的圈套。"'),
    ("onikakushi/onikakushi_omake.rpy", 265,
     'adv_extend "What does the man himself have to say',
     'adv_extend "那本人对此又是怎么说的呢？"'),
    ("onikakushi/onikakushi_tips.rpy", 192,
     'adv_extend "The guys that didn\'t want to commute',
     'adv_extend "不想跑到兴宫去上学的那些人，就从林业署把房子租了下来，在这里上这种私塾一样的学校。"'),
    ("onikakushi/onikakushi_vm.rpy", 2050,
     'adv_extend "The next chapter will introduce',
     'adv_extend "下一章会介绍一些雏见泽的历史。"'),
    ("watanagashi/wata_010.rpy", 846,
     'adv_extend "Ooishi-san asked me,"',
     'adv_extend "大石先生问我，"'),
    ("watanagashi/wata_010.rpy", 847,
     'adv_extend "Shion asked me,"',
     'adv_extend "诗音问我，"'),
    ("watanagashi/wata_010.rpy", 848,
     'adv_extend "...and now Rika-chan was asking me..."',
     'adv_extend "……然后现在轮到梨花来问我了……"'),
    ("watanagashi/wata_ep_01.rpy", 214,
     'adv_extend "would these short few weeks',
     'adv_extend "我在雏见泽度过的这几个星期……{w=0.8}究竟会给我的人生留下什么？"'),
    ("watanagashi/wata_011_02.rpy", 341,
     'adv_extend "We think they were discussing',
     'adv_extend "我们认为他们当时正在商议如何应对又一次发生的连续离奇死亡事件。"'),
    ("watanagashi/wata_012_03.rpy", 333,
     'adv_extend "We passed places that looked like',
     'adv_extend "我们经过了一些像是曾有人住过的地方。"'),
]


def main():
    apply = '--apply' in sys.argv
    by_file = {}
    for rel, ln, exp, new in REPL:
        by_file.setdefault(rel, []).append((ln, exp, new))

    ok = fail = 0
    for rel, items in by_file.items():
        p = os.path.join(GAME, rel.replace('/', os.sep))
        lines = io.open(p, encoding='utf-8').read().split('\n')
        touched = False
        for ln, exp, new in items:
            idx = ln - 1
            if idx >= len(lines):
                print("OUT OF RANGE %s:%d" % (rel, ln))
                fail += 1
                continue
            cur = lines[idx].strip()
            if exp not in cur:
                print("MISMATCH %s:%d\n  want: %s\n  got : %s" % (rel, ln, exp, cur[:100]))
                fail += 1
                continue
            indent = lines[idx][:len(lines[idx]) - len(lines[idx].lstrip())]
            lines[idx] = indent + new
            ok += 1
            touched = True
        if touched and apply:
            io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print("replaced: %d  failed: %d  (apply=%s)" % (ok, fail, apply))


if __name__ == '__main__':
    main()
