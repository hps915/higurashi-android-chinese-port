# -*- coding: utf-8 -*-
"""Apply the 69 hand-checked zh translations to tsumihoroboshi say lines.

Each entry: (file, lineno, expected_old_body, new_body).
The script verifies the old body matches exactly before replacing, so a
mistargeted line aborts the whole batch instead of corrupting the script.
"""
import io
import os
import re
import sys

TSUMDIR = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game\tsumihoroboshi"
SAY_RE = re.compile(r'^(\s*)(?:([A-Za-z_]\w*)\s+)?"((?:[^"\\]|\\.)*)"\s*$')

EDITS = [
    # ---- tsum_005 ----
    ('tsum_005.rpy', 551,
     '...After all,{w=0.8} the letter inside the envelope had{w=0.8} a rough surface.',
     '…因为，{w=0.8}信封里的纸，{w=0.8}皱巴巴的。'),
    ('tsum_005.rpy', 569,
     'At that time,{w=1.0} I realized.',
     '这时，{w=1.0}我察觉到。'),
    ('tsum_005.rpy', 573,
     'I should say{w=1.0} I knew{w=0.8} because it was so obvious.',
     '因为事情是如此明白，{w=1.0}我知道了，{w=0.8}应该用这句话来表达。'),
    ('tsum_005.rpy', 625,
     'Those were{w=0.8} my last words to my mother...{w=1.0} no, to the woman who used to be my mother.',
     '那是，{w=0.8}我对妈妈，{w=1.0}……不，曾是我妈妈的女子，留下的最后一句话。'),
    ('tsum_005.rpy', 653,
     '.........When I try to remember what happened after that...{w=0.8} I feel disoriented.',
     '…………我想要回忆之后发生的事情，然而{w=0.8}……头脑一片模糊。'),
    ('tsum_005.rpy', 672,
     'When I was about to reach{w=0.8} that very last resolution...',
     '当时，{w=0.8}……是真真正正的，最后一刻。'),
    ('tsum_005.rpy', 687,
     'Yes, all of this was because of her curse.',
     '是的，这全都是，作祟。'),
    ('tsum_005.rpy', 689,
     'Oyashiro-sama brought a curse upon the Ryuugu family because we broke her rule and abandoned Hinamizawa.',
     '这是因为龙宫家违反了御社神大人定下的规矩，不能遵守雏见泽的规矩，从而从天而降的神罚。'),
    ('tsum_005.rpy', 692,
     'After I figured that out,{w=0.8}{cps=*0.4}.........{/cps} everything started to make sense to me, all the crazy things that happened after my mother was gone.',
     '一旦明白了这一点，{w=0.8}{cps=*0.4}………{/cps}就完全能解释，为什么妈妈离开以后我们的世界变得反常、脱轨了。'),
    ('tsum_005.rpy', 772,
     'If I... turned off this light...{w=0.8} would everything in this world disappear?',
     '如果我……把这盏灯关掉的话，{w=0.8}这世界里的一切都会消失吗？'),
    ('tsum_005.rpy', 797,
     'But{w=0.8}......... she did come{w=0.6} at that time.',
     '可是，{w=0.8}…………那时候，{w=0.6}真的来过。'),
    ('tsum_005.rpy', 843,
     "{i}He became miserable{w=0.8}... because of me.{/i}",
     '{i}因此，…深深伤害爸爸的那个人，{w=0.8}……是我。{/i}'),
    ('tsum_005.rpy', 901,
     "......I just don't like...{w=1.0} her perfume...",
     '……这个人的香水味，{w=1.0}……我一点也不喜欢…。'),

    # ---- tsum_006 ----
    ('tsum_006.rpy', 417,
     "There's actually...{w=1.0}... no reason for me to hate her.",
     '我真的，……{w=1.0}……没有理由恨她。'),
    ('tsum_006.rpy', 420,
     "But............ the bitter memories of my parents' divorce{w=1.0} and my many regrets{w=0.8} were gradually eating away at my heart.",
     '可是，…………一回想起父母离婚时的痛苦回忆，{w=1.0}一种反反复复的后悔，{w=0.8}慢慢侵蚀着内心深处。'),
    ('tsum_006.rpy', 435,
     'Should I fight{w=1.0} the enemy{w=0.9}... before it\'s too late?',
     '当一切还为时不晚，{w=1.0}……我是不是该与“敌人”{w=0.9}作斗争呢。'),
    ('tsum_006.rpy', 579,
     "......I keep feeling anxious, but that's just because{w=1.0} I'm still immature, and because I feel like I'm not ready to separate from my father.",
     '……我总是不安，但那只是因为我还没长大，{w=1.0}只是因为我还没做好离开爸爸的准备。'),
    ('tsum_006.rpy', 582,
     "I'm going to live with all my might...{w=1.0} in order to regain the peace of mind that I lost that day.",
     '为了找回那天以来所失去的心中的安宁，{w=1.0}……我会竭尽全力地活下去。'),
    ('tsum_006.rpy', 721,
     'From the front of the house, I heard voices of two young men saying,{w=1.0} \\"Well, we\'ll be going now.\\"',
     '玄关那边传来两名年轻男子整齐划一的声音，{w=1.0}\\"那么我们告辞了——！\\"'),
    ('tsum_006.rpy', 877,
     'I found the old furniture...{w=1.0} outside in the yard.',
     '我不经意地望了一眼院子，{w=1.0}…那些令人怀念的家具摆放在屋子前。'),
    ('tsum_006.rpy', 892,
     'But...{w=0.8}...... for some reason, this new living room makes me feel like{w=1.0} I no longer belonged here.',
     '可是，{w=0.8}…………不知为什么，我感到这个崭新的客厅里，{w=1.0}没有我的容身之所。'),
    ('tsum_006.rpy', 946,
     '.........Maybe I should think about working at a hostess club{w=1.0}...... like Rina-san does.',
     '………还是该像丽娜小姐那样，{w=1.0}……做夜店小姐呢。'),
    ('tsum_006.rpy', 950,
     "......A girl like me doesn't have a lot of choices.{w=1.0} Not a lot of companies would hire me or pay the amount of money that I'd need to live on my own...",
     '……我这样的女孩子为了找到工作、赚取养活自己薪水，{w=1.0}…恐怕没资格说这种漂亮话…。'),
    ('tsum_006.rpy', 954,
     'Come to think of it{w=0.8}{cps=*0.4}......{/cps} where is the place where I belong?',
     '我的容身之所，{w=0.8}{cps=*0.4}……{/cps}到底在哪里呢。'),
    ('tsum_006.rpy', 976,
     "I'm the bad one.{w=0.8} I'm the bad one.",
     '是我不对，{w=0.8}是我不对。'),

    # ---- tsum_013 ----
    ('tsum_013.rpy', 767,
     'Oyashiro-sama... was looking at me with gentleness and sadness in her eyes.',
     '御社神大人…用温柔而无比悲伤的眼神望着我。'),
    ('tsum_013.rpy', 769,
     'As she touched my wound...... the maggots started melting and disappeared in front of my eyes.',
     '然后，…轻轻地抚摸着我的伤口，……任我怎么洗也洗不掉的蛆虫，眼看着融化，消失了。'),
    ('tsum_013.rpy', 798,
     "But we...... broke Oyashiro-sama's rules, and we left Hinamizawa... That's why my family was broken, and I lost my mind...!",
     '可是我们……打破了御社神大人的戒律，搬离了雏见泽，…所以家里才会变得一团糟，我也变得不正常了…！'),
    ('tsum_013.rpy', 809,
     'She could make the maggots, the embodiment of the curse, disappear. But only temporarily, because I lived far from Hinamizawa.',
     '即使能消灭这些因作祟而显灵的蛆虫，要是我继续远离雏见泽，待在这个地方，也是治标不治本的。'),
    ('tsum_013.rpy', 815,
     'I must go back to Hinamizawa...... before her power to hold down the curse faded away.',
     '在压制作祟的力量削弱之前，……请回到雏见泽。'),
    ('tsum_013.rpy', 818,
     'She did. I heard her tell me that!',
     '是的，说了，说了，我的确听到了！'),
    ('tsum_013.rpy', 1105,
     "{i}'If they find out, they might erase me'{/i}.",
     '{i}“被那帮家伙知道了，说不定会被抹杀”{/i}。'),
    ('tsum_013.rpy', 1106,
     'She said and laughed.',
     '说着，她笑了起来。'),
    ('tsum_013.rpy', 1144,
     'Did Oyashiro-sama put her curse on Tomitake...... because he violated the sacred ritual dance...?',
     '玷污了祭祀御社神大人的神圣演舞………他因而遭到了作祟…？'),
    ('tsum_013.rpy', 1152,
     'Did that mean...... Oyashiro-sama put her curse on Miyo-san, too......?',
     '也就是说………三四小姐，……也遭到了御社神大人的作祟……？'),

    # ---- tsum_020 ----
    ('tsum_020.rpy', 300,
     'They said{cps=*0.4}............{/cps}{w=0.8} \\"Rena Ryuugu was seen in Gogura.\\"',
     '他们还说{cps=*0.4}…………{/cps}{w=0.8}\\"龙宫蕾娜人在谷仓\\"。'),
    ('tsum_020.rpy', 441,
     "Its shadow is very small... I can tell it isn't an adult.",
     '这个人影很瘦小，……绝对不可能是大人。'),
    ('tsum_020.rpy', 459,
     '{cps=*10.0}And{w=0.8}......... it{w=0.6} knocked{w=0.6}......{/cps}{nw}',
     '{cps=*10.0}然后{w=0.8}………它{w=0.6}敲了敲{w=0.6}……{/cps}{nw}'),
    ('tsum_020.rpy', 591,
     'But...... she pretended like that{w=0.8} for too long.',
     '不过，……这段时间，{w=0.8}太长了。'),
    ('tsum_020.rpy', 595,
     'And......... she finally showed{w=0.8} her true character.',
     '然后，…………她终于揭下了，{w=0.8}…她的假面具。'),
    ('tsum_020.rpy', 1129,
     "......Now I know why she was laughing at me in a sarcastic way...... She knew that I wouldn't have much time left...!!",
     '……现在我知道她为什么那样嘲讽地笑我了……她知道我已经活不长了…！！'),

    # ---- tsum_008 ----
    ('tsum_008.rpy', 284,
     'I didn\'t want her to leave it up in the air, so I told her, \\"I think I should give it back to him as soon as possible.{w=1.0} I\'m sure he\'s looking for it, too.\\"',
     '我不想就这样被小魅敷衍过去，于是就在她耳边说：\\"还是快点还给他比较好，{w=1.0}葛西先生一定在四处寻找呢。\\"'),
    ('tsum_008.rpy', 360,
     "......Ahaha, would that mean...{w=1.0} that {b}I{/b}'d be the one who gets demoned away this year?",
     '……啊哈哈，那么今年，{w=1.0}遭遇鬼隐的会是{b}我{/b}吗？'),
    ('tsum_008.rpy', 565,
     'I knew that...{cps=*10.0}{w=0.6} but I just wanted to run away.{w=0.8} I couldn\'t stop myself from running away.{w=0.8} And so, I did run away!{/cps}',
     '虽然我都懂，{cps=*10.0}{w=0.6}…还是想逃，{w=0.8}想一走了之，{w=0.8}远走高飞！！{/cps}'),
    ('tsum_008.rpy', 918,
     'I felt as if was letting another me use my body.',
     '我有一种奇妙的感觉，就好像是把身体交给了另一个自己。'),
    ('tsum_008.rpy', 969,
     "She has to divorce because she got pregnant. She has to get married because she got pregnant.{w=0.8} That's a lie!{w=0.8} That's a big lie...!!",
     '因为怀孕了不得不离婚，因为怀孕了不得不再婚，{w=0.8}撒谎，撒谎，{w=0.8}这是弥天大谎…！！'),
    ('tsum_008.rpy', 1055,
     "......But, I didn't know{w=1.0} what to do. I didn't know{w=1.5} what I should do.",
     '……可是，正因为没有退路，{w=1.0}她也不知到底该怎么办。{w=1.5}她不知道。'),

    # ---- tsum_007 ----
    ('tsum_007.rpy', 994,
     "Rina-san is{w=1.0} a 'bad person'.",
     '丽娜小姐，{w=1.0}就是“坏人”。'),
    ('tsum_007.rpy', 1122,
     '.........I remembered...{w=0.8} Around that time...{w=1.0} Rina-san was talking about moving into a new apartment.',
     '………是的，{w=0.8}…那时候，的确是，{w=1.0}…丽娜小姐提过要搬进新公寓。'),
    ('tsum_007.rpy', 1180,
     "......If, from the beginning, Rina-san was only seeing to check if he could end up being a big catch...{w=1.0} she must've been trying to find how much money she could squeeze out of him.",
     '……要是丽娜小姐这帮人从一开始就把爸爸当作敲诈对象的话，{w=1.0}她就应该早就试探过能从爸爸身上榨出多少钱了。'),
    ('tsum_007.rpy', 1251,
     'Then that meant......{w=1.0} I couldn\'t make him do anything.',
     '那么，……也就是说，{w=1.0}我对父亲什么也做不了。'),
    ('tsum_007.rpy', 1256,
     "......So, instead of making my father fight...{w=0.8} I'd have to fight in his place.",
     '……对，也就是说，我不该唆使父亲去抗争，也不该唆使其他人，{w=0.8}…而必须亲自去抗争。'),

    # ---- tsum_018 ----
    ('tsum_018.rpy', 165,
     "......If I'm going to end up the same way no matter what I choose to do...{w=0.8} I'll fight.",
     '……既然不管我怎么选择，最终都会走向同样的结局，{w=0.8}……我还是要抗争。'),
    ('tsum_018.rpy', 303,
     'Mii-chan is out of question.',
     '小魅就更不用说了。'),
    ('tsum_018.rpy', 736,
     "They're going to use the corpses......{w=0.8} to sell me out to the police for the murder of Rina and Teppei!",
     '总之，那帮家伙打算利用那些尸体，{w=0.8}……把我当作杀害丽娜和铁平的凶手出卖给警察！'),
    ('tsum_018.rpy', 855,
     "No......{w=1.0} That's why I'm going to talk to Ooishi.",
     '不……{w=1.0}…正因为如此，我才要去找大石。'),

    # ---- tsum_017 ----
    ('tsum_017.rpy', 1050,
     '......Chie-sensei confirmed that I came to school today, made a phone call...{w=0.7} and called them here...?!',
     '……知惠老师在确认我到校之后与他们取得联络，{w=0.7}…把他们找来了…？！'),
    ('tsum_017.rpy', 1124,
     '{cps=*20.0}Is that it\'s an order from higher up.{w=0.8} It says to make \\"Rena Ryuugu\\"{w=0.8} become \\"blank\\"!!{/cps}',
     '{cps=*20.0}这是来自幕后黑手的命令！{w=0.8}上面写着，要把“龙宫蕾娜”{w=0.8}填进“空白栏”！！{/cps}'),
    ('tsum_017.rpy', 1242,
     '{cps=*4.0}...............I......{w=0.8} told Keiichi-kun......{w=0.7} where I hid the scrapbooks.{/cps}',
     '{cps=*4.0}……………我……{w=0.8}告诉了圭一君……{w=0.7}剪贴簿藏在哪里。{/cps}'),

    # ---- tsum_019 ----
    ('tsum_019.rpy', 644,
     '.........If{w=0.6} her theory is true...{w=0.8} it might happen again.',
     '………假如，{w=0.6}…那个假说是真的，{w=0.8}……应该还会现身。'),
    ('tsum_019.rpy', 646,
     "...Ahh...{w=0.6} There's no way...... It can't be true......",
     '…啊啊，{w=0.6}…可是难道，……真会发生这么不可思议的事吗……？'),

    # ---- tsum_016 ----
    ('tsum_016.rpy', 631,
     'They secrete an antibody called {font=Times.ttf}immunoglobulin E{/font} (IgE).',
     '它们会分泌一种名为{font=Times.ttf}免疫球蛋白E{/font}（IgE）的抗体。'),
    ('tsum_016.rpy', 821,
     "In the fourth year...{w=0.8} Satoshi Houjou's aunt was beaten to death, probably by Satoshi himself.",
     '第4年，{w=0.8}…恐怕就是北条悟史打死了叔母的案子。'),

    # ---- tsum_021 ----
    ('tsum_021.rpy', 940,
     "Or......... maybe Keiichi-kun is right, and I'm wrong... Am I really just misunderstanding everything......?",
     '可是，………事情也许真的像圭一君所说的那样，…是我误会了……？'),

    # ---- tsum_012 ----
    ('tsum_012.rpy', 1234,
     'I prepared myself......{w=0.8} and got in.',
     '我做好了心理准备，{w=0.8}……坐进车里。'),

    # ---- tsum_011 ----
    ('tsum_011.rpy', 1771,
     'My heart{w=0.6} was full of.......{w=0.8} many{w=0.8} many emotions that day.',
     '今天这一天，{w=0.6}……过得实在，{w=0.8}太充实了，{w=0.8}太充实了。'),

    # ---- tsum_010 ----
    ('tsum_010.rpy', 420,
     '...And I also atoned for my sin{w=0.8} of not doing anything about my mother......{w=0.8} by doing what I did the previous night.',
     '…同时，母亲离婚当时，我什么都没做到，{w=0.8}…这份罪过也因昨天发生的事情，{w=0.8}……得到了救赎。'),

    # ---- tsum_009 ----
    ('tsum_009.rpy', 69,
     '......A tamed animal{w=1.0} is still tamed{w=0.8} even after the owner is dead.',
     '……就算主人死了，{w=1.0}家畜依然是家畜，{w=0.8}吗。'),

    # ---- tsum_003 ----
    ('tsum_003.rpy', 1987,
     "That's why...{w=1.0} I was trying to enjoy the happiness I received today so that I wouldn't regret it",
     '所以……{w=1.0}哪怕明天就是世界末日，'),
]


def main():
    apply = '--apply' in sys.argv
    by_file = {}
    for f, n, old, new in EDITS:
        by_file.setdefault(f, []).append((n, old, new))
    errors = []
    total = 0
    for f, items in by_file.items():
        p = os.path.join(TSUMDIR, f)
        raw = io.open(p, encoding='utf-8').read()
        lines = raw.split('\n')
        for n, old, new in items:
            line = lines[n - 1]
            m = SAY_RE.match(line)
            if not m:
                errors.append('%s:%d not a say line: %r' % (f, n, line))
                continue
            if m.group(3) != old:
                errors.append('%s:%d body mismatch\n  got: %r\n  exp: %r'
                              % (f, n, m.group(3), old))
                continue
            prefix = m.group(1) + ((m.group(2) + ' ') if m.group(2) else '')
            lines[n - 1] = '%s"%s"' % (prefix, new)
            total += 1
        if apply and not errors:
            out = '\n'.join(lines)
            if raw.endswith('\n') and not out.endswith('\n'):
                out += '\n'
            io.open(p, 'w', encoding='utf-8', newline='\n').write(out)
    if errors:
        print('ABORTED - %d problem(s):' % len(errors))
        for e in errors:
            print(' ', e)
        return 1
    print('would apply / applied %d edits (apply=%s)' % (total, apply))
    return 0


if __name__ == '__main__':
    sys.exit(main())
