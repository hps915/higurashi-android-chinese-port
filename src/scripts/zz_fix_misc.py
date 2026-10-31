# -*- coding: utf-8 -*-
"""第 8 轮 3.3（续）：繁体字、日文残留、多余标点、长句断句。"""
import io
import os
import sys

K = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game"
Q = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project\game"

# (base, rel, lineno, expected_substring, new_full_line_without_indent_and_ident)
JOBS = [
    # 繁体字 + 让步
    (K, "minagoroshi/mina_025.rpy", 1480, u"在不能讓步的情況",
     u'extend "实际上她遵照自己设定的规则，在不能让步的情况下就绝对不会让步。"'),
    # 多余单引号
    (Q, "tatarigoroshi/tata_011_02.rpy", 1169, u"好孩子不要在沼泽边玩耍！'",
     u'n "鬼渊沼泽・好孩子不要在沼泽边玩耍！"'),
    # 日文残留
    (Q, "tatarigoroshi/tatarigoroshi_tips.rpy", 2360, u"オヤシロさまだが",
     u'n "御社神大人（オヤシロさま），不太清楚到底写成怎样的汉字。"'),
    # 长句断句
    (Q, "himatsubushi/hima_001.rpy", 1098, u"可是示威游行的队伍",
     u'n "可是示威游行的队伍和机动队发生了激烈的冲突，乱斗了起来，出现了很多的流血受伤者以及被逮捕者。"\n'
     u'    extend "以这次事件为契机，正如鬼之渊死守同盟这个名字一样，抵抗运动越来越激进，让人如同看到鬼一样觉得恐怖…"'),
    (K, "minagoroshi/mina_ep.rpy", 45, u"问. 研究设施",
     u'n "问. 研究设施因为致命的意外造成隐密设施暴露在外部的情况下，通常是交给保护机密部队处理。"\n'
     u'    extend "但暴露的规模超过部队处理能力的情况下，为了保护机密，紧急应对说明书第34号是否适用呢？"\n'
     u'    extend "以及是否能由所长来判断情况是否超越处理能力呢？"'),
    (K, "meakashi/meak_007.rpy", 658, u"分尸杀人案",
     u'extend "……分尸杀人案，然后是北条夫妇的坠崖意外，连续两年发生事件之后，御社神大人的作祟在村里引起了轩然大波。"\n'
     u'    extend "在孩子们的内心深处留下了恐怖的阴影，那个时候的恐惧开始渐渐复苏了。"'),
    (K, "matsuribayashi/matsuribayashi_kakera_02.rpy", 2262, u"我要证明那项曾被肆意践踏的研究",
     u'nvl_extend " 我要证明那项曾被肆意践踏的研究，其实是足以令世界震惊的伟大成就，"\n'
     u'        extend "要让世人由衷地赞美在泥土下渐渐腐朽的祖父……并将其升华为神。这就是我活着的全部理由和目的。"\n'
     u'        extend "…………次郎先生。"'),
    # 粘连/衍文重译
    (K, "minagoroshi/mina_013.rpy", 1997, u"听给我听好沙都子的魅力",
     u'nvl_extend "听好了！沙都子的魅力，就是平常态度骄傲、让人难以靠近。"\n'
     u'        extend "可是遇到喜欢的人、或是碰到尴尬的事，也会露出害羞的一面。"\n'
     u'        extend "兼具这两种特质的她，是那种平时威严得难以接近、一旦遇上心上人就会变得害羞惹人怜爱的类型！！"'),
]

# 尖叫行单独处理（保持一条，改为分段但内容不变）
WAIL = [(Q, "watanagashi/wata_011_02.rpy", 1271),
        (K, "meakashi/meak_023.rpy", 1172)]


def main():
    apply = '--apply' in sys.argv
    for base, rel, ln, needle, new in JOBS:
        p = os.path.join(base, rel.replace('/', os.sep))
        lines = io.open(p, encoding='utf-8').read().split('\n')
        i = ln - 1
        if i >= len(lines):
            print("OOR  %s:%d" % (rel, ln))
            continue
        cur = lines[i]
        if needle not in cur:
            print("MISS %s:%d\n   want %r\n   got  %r" % (rel, ln, needle, cur.strip()[:120]))
            continue
        stripped = cur.lstrip()
        indent = cur[:len(cur) - len(stripped)]
        # 新行已含 indent 时以 new 内自带为准
        block = new.split('\n')
        newlines = []
        for k, b in enumerate(block):
            if k == 0:
                newlines.append(indent + b)
            else:
                # 保持 new 里显式写的缩进
                newlines.append(b)
        print("OK   %s:%d  (%d -> %d lines)" % (rel, ln, 1, len(newlines)))
        if apply:
            lines[i:i + 1] = newlines
            io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print("(apply=%s)" % apply)


if __name__ == '__main__':
    main()
