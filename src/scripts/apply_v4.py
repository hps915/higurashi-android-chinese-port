# -*- coding: utf-8 -*-
"""v4 content patches:
  1. translate chapter-opening poem show-text lines (black-bg white monologues)
  2. translate the 7 menu choice blocks (official ycx + own translations)
  3. tl strings for save_names (chapter/day names) + prologue jump keys
  4. boot-guard text + official enable_opening text
  5. zz_op opening labels for chapters 2-8 + screen Start() rewiring
  6. copy converted ogv openings into the projects
"""
import ast
import json
import os
import re
import shutil

WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- poems
POEMS = {
    "Something went wrong.": "出错了。",
    # ---- onik_op ----
    "At first I was a bit anxious.": "起初，我还有一些隐隐的不安。",
    "Hurting someone was something I never even considered.": "伤害谁之类的，我连想都没有想过。",
    "Nevertheless, the anxiety then gave place": "然而，那份不安渐渐退去，",
    "to loneliness, doubt and more.": "取而代之涌上心头的，是孤独、怀疑，还有更多。",
    "And then... that wicked murderous intent eventually took control of my mind.": "然后……那股邪恶的杀意，最终支配了我的心灵。",
    "The boy took the first step": "少年迈出了第一步，",
    "towards an unrecoverable daily life.": "走向那段再也无法挽回的日常。",
    "Not even realizing that he was walking into the abyss.": "却浑然不觉，自己正一步步踏入深渊。",
    "A tragedy born from the desire to believe.": "这是一场因渴望去相信而生的悲剧。",
    "Are those tears of repentance or tears of resentment?": "那泪水，是悔恨的泪，还是怨恨的泪？",
    # ---- wata_001 ----
    "I really meant to say things differently.": "我明明，本想换一种方式来说的。",
    "I really didn't want to feel this way.": "我明明，本不想抱有这样的想法。",
    "Miscommunication drove in the wedge,": "传递错位的言语楔进裂痕，",
    "those stuck in apprehension driven to fear.": "困于猜疑的人们被推向恐惧。",
    "Nobody can stop it now,": "事到如今，谁也无法阻止，",
    "as cold hard emotion claws deeply and cruelly at my bared heart.": "冰冷坚硬的情感，正无情地撕扯着我袒露的心。",
    "At that time, why did I...? I whisper in remorse.": "那时候的我，为什么会……？我在悔恨中低声自问。",
    "But now, those words simply rang hollow.": "可如今，那些话只余下空洞的回响。",
    # ---- tata_001 ----
    "I wholeheartedly wanted to protect her.": "我打从心底里，想要守护她。",
    "I wanted, more than anybody else, what was best for her.": "比世上任何人都要强烈，我祈愿她能幸福。",
    "These emotions borne from kindness eventually became murderous intent,": "这份由善意而生的情感，最终化作了杀意，",
    "my pure white intentions stained in red and black.": "我纯白的初衷，被染上了红与黑的颜色。",
    "And even as I understood that it meant the destruction of the": "即使我早已明白，这意味着毁掉那份",
    "day-to-day life I so wanted to protect...": "我无比想守护的日常……",
    "Where did I go wrong?": "我究竟，是哪里做错了呢？",
    "Looking for the answer, the tragedy spreads ever wider.": "在寻找答案的同时，悲剧不断扩大。",
    # ---- tata_ep02 ----
    "...Was this recording really taken of Maebara Keiichi?\\nSome harbor suspicions.": "……这份录音，当真出自前原圭一之口吗？\\n有人对此抱有怀疑。",
    "To verify its authenticity, I had the others in the Maebara family check the tapes with his voice in it. However, the sound was not clear, and much time had passed, so the relatives I checked with couldn't remember what he sounded like. I was unable to gain positive proof it was actually his voice.": "为了验证真伪，我请前原家的其他人听了他声音的磁带。然而声音并不清晰，加上时日已久，受访的亲属们也记不清他的嗓音了。我始终无法得到确凿的证据，证明这确实是他的声音。",
    "...Doubts also remain regarding the date 11/28 written on the tape.": "……磁带上写着的日期 11/28，同样存在疑点。",
    "After Maebara Keiichi's failed suicide attempt on a certain August day two months after the disaster, he was diagnosed with a mental disorder and transported to a treatment facility.": "惨剧发生两个月后的八月某日，前原圭一自杀未遂，被诊断为精神失常，移送至治疗机构。",
    "The facility never allowed any news coverage, so it's extremely unlikely that a tape from the media dated after August 1983 would have his voice on it.": "该机构从不允许新闻媒体采访，因此 1983 年 8 月之后媒体手中几乎不可能存在录有他声音的磁带。",
    "However, the reporter had been criticized for his forceful methods of collecting data while he was active, so there is still a possibility that he broke into the facility and forced Keiichi Maebara to talk.": "不过，这名记者从业期间就曾因强行采访而备受非议，所以他闯入机构、强行让前原圭一开口的可能性，并不能被完全排除。",
    "Is this truly Keiichi Maebara's voice...?\\nThe authenticity of this recording... is still wrapped in mystery.": "这真的是前原圭一的声音吗……？\\n这份录音的真伪……至今仍笼罩在重重迷雾之中。",
    "Fifteen years after this tape was created, the reporter, just as Keiichi Maebara had predicted, died in an accident out on the sea.": "这份磁带制成十五年后，那名记者正如前原圭一所预言的那样，死于一场海上事故。",
    "And Keiichi Maebara...": "而前原圭一……",
    "Late on the night of 11/30/1983, two days after the interview, he suddenly died from a high fever, cause unknown.": "1983 年 11 月 30 日深夜，就在采访的两天之后，他因原因不明的高烧猝然离世。",
    "Records remain of the strange words he kept giving after pressing the call buttom the day before he died.": "据说在死前一天，他不断按着呼叫按钮，反复念着一些奇怪的话语。这些话语被记录了下来。",
    '\\"An extra set of footsteps...\\"': "“多了一串脚步声……”",
    # ---- hima_001 ----
    "It was an accident that happened in such a small village that anyone could forget.": "那是一场发生在小小村庄里的事故，小到任何人都会将它遗忘。",
    "One day, after the tragedy had come to a close, just as the scars had begun to heal.": "某一天，当悲剧落下帷幕，伤痕才刚刚开始愈合。",
    "A young man thinks nostalgically of the little girl he once met.": "一位青年满怀怀念地想起，自己曾经遇见的那个小女孩。",
    "The words he couldn't ask that day.": "那天，没能问出口的话语。",
    "The promise he couldn't fulfill that day.": "那天，没能兑现的约定。",
    "Those regrets and lamentations, opened the fate that was sealed,": "那些悔恨与悲叹，解开了被封印的命运，",
    "and became a single hope.": "并化作了一份唯一的希望。",
    "Fate isn't only about happiness,": "命运并非只关乎幸福，",
    "but there is no one that would wish for unhappiness.": "可世上也没有谁，会去祈愿不幸。",
    # ---- hima_004 ----
    "Why did this tragedy happen?": "为什么，会发生这场悲剧？",
    "We can't reach the truth by ourselves.": "仅凭我们自身，无法触及真相。",
    "If you are reading this.": "如果你读到了这份记录。",
    "Please discover the truth.": "请务必找出真相。",
    "This is our only wish.": "这是我们唯一的愿望。",
    "Kuraudo Ooishi\\nMamoru Akasaka": "大石藏人\\n赤坂卫",
    # ---- meak_001 ----
    "A love that is light and fleeting, like a soap bubble.": "那份爱轻渺而易逝，宛如肥皂泡沫。",
    "If it seeks the sky, it will break and vanish before long.\\nThe girl's thoughts weren't granted.": "倘若想飞向天空，很快便会破碎消散。\\n少女的心愿，终究未能实现。",
    "The tears that were shed changed to the color of blood,\\nand yearned for a sacrifice.": "流下的泪水化作血红，\\n渴求着祭品。",
    "The sadness that pierced her transformed into rage,\\nand ultimately to murderous intent.": "刺穿她的悲伤化作怒火，\\n最终成为杀意。",
    "Everything was absorbed in pure black, and the darkness continued to spread.": "一切被纯黑吞没，黑暗仍在不断蔓延。",
    "In the end, even to herself.": "到了最后，连她自己也不例外。",
    "Would it be better if I hadn't been born?": "如果我未曾出生，是不是反而更好？",
    "This bloodstained hand couldn't even grasp the air.": "这只染血的手，甚至连空气都抓不住。",
    "Chapter 5: Meakashi": "第五章：目明篇",
    "Shion Sonozaki": "园崎诗音",
    "{space=40}Keiichi Maebara{space=70}Rena Ryuugu\\n{space=70}Mion Sonozaki{space=107}Satoko Houjou\\n{space=75}Rika Furude": "{space=40}前原圭一{space=70}龙宫蕾娜\\n{space=70}园崎魅音{space=107}北条沙都子\\n{space=75}古手梨花",
    "Satoshi Houjou{space=70}Kuraudo Ooishi\\nJirou Tomitake{space=90}Miyo Takano\\nKyousuke Irie{space=86}Tatsuyoshi Kasai\\nRumiko Chie{space=70}Akane Sonozaki": "北条悟史{space=70}大石藏人\\n富竹次郎{space=90}鹰野三四\\n入江京介{space=86}葛西辰由\\n知惠美纪{space=70}园崎茜",
    # ---- meak_020 ----
    "......Huh?": "……咦？",
    "Huh? Huh? Huh...?": "咦？咦？咦……？",
    "Huh? ......What...?": "咦？……什么……？",
    "......What?": "……什么？",
    # ---- mina_op ----
    "The more she got hurt, the more her heart became timid.": "受的伤越多，她的心就变得越怯弱。",
    "The deeper her sadness became, the less she could enjoy happiness.": "悲伤越深，她就越发无法享受幸福。",
    "The same time, the same world had repeated a thousand times.": "相同的时间，相同的世界，已经重复了千百次。",
    "The girl who had forgotten how to smile locked her heart away and isolated herself.": "忘记了如何微笑的少女，锁上心扉，将自己隔绝开来。",
    "When she noticed a light coming in through a gap, she raised her head.": "当她注意到缝隙间透进的一缕光时，她抬起了头。",
    "Did Pandora's hope ever really exist?": "潘多拉的希望，当真存在过吗？",
    "With the courage taken back, the truth of the darkness can be revealed.": "取回勇气之时，黑暗的真相将昭然若揭。",
    "The future she had given up on, was now right in front of her eyes.": "她早已放弃的未来，如今就在她的眼前。",
    "Chapter 7: Minagoroshi": "第七章：皆杀篇",
    # ---- tsum_op ----
    "She believed that if she kept laughing she would be happy.": "她曾相信，只要一直笑着，就能得到幸福。",
    "She believed that if she cared about someone, that person would care for her as well.": "她曾相信，只要真心对待他人，对方也会真心待她。",
    "Leaving the sad memories behind, the girl turned forward to face tomorrow.": "少女将悲伤的回忆抛在身后，转身迎向明天。",
    "Without being spoiled, without relying on anyone, all alone,\\nto carve a path toward the future.": "不受娇惯，不依赖任何人，孤身一人，\\n也要开辟出通往未来的道路。",
    "What awaits her?": "等待她的，会是什么？",
    "Is it happiness? Is it unhappiness?": "是幸福？还是不幸？",
    "She wanted to love someone.": "她想去爱一个人。",
    "But the truth is, she wanted to be loved.": "可其实，她更想被人所爱。",
    "Chapter 6: Tsumihoroboshi": "第六章：罪灭篇",
    # ---- mats_007 ----
    "A big decision that inhabits a tiny soul.": "寄宿于渺小灵魂之中的，是重大的决断。",
    "If my life is heavier than the earth...": "倘若我的生命重于大地……",
    "Then my decision is heavier than the earth.": "那么我的决断，便重于大地。",
    "The fulfill a wish and weave a desired future.": "实现愿望，编织出心中期望的未来。",
    "The strength of a string is how strong your will is.": "丝线的强度，取决于意志的强度。",
    "A noble and strong wish will come true.": "高贵而强烈的愿望，终将实现。",
    "A wish that's guaranteed to come true is not called a wish.": "注定能够实现的愿望，不配称为愿望。",
    "That is fate, not a wish.": "那叫命运，而不叫愿望。",
    "I weave fate.": "我，编织命运。",
    "Fate is an absolute power to control people and the world, not just an individual.{space=175}": "命运是支配人类与世界、而不仅限于个人的绝对之力。{space=175}",
    "Chapter 8: Matsuribayashi": "第八章：祭囃篇",
}

# ---------------------------------------------------------------- menus
MENUS = {
    "Open the red box": "打开红色的箱子",
    "Open the blue box": "打开蓝色的箱子",
    "Skip additional choices": "跳过新增选项",
    "Prompt additional choices": "提示新增选项",
    "Plead for my life": "向他求饶",
    "Watch for an opportunity": "寻找机会",
    "At that time, I became aware of Keiichi's gaze": "这时，我注意到了圭一的目光",
    "And then, I turned around to face Keiichi": "然后，我转过头看着圭一",
    "I advised him on who he should give the doll to.": "我给他建议了娃娃该送给谁。",
    "I did nothing and watched the events unfold.": "我什么也没做，只是注视着事态发展。",
    "It'll be all right": "没问题的",
    "...Yeah, I guess": "……嗯，大概吧",
    "Satoko, are you still there?! There's no time!!": "沙都子，还没想到吗？！已经没有时间了！！",
    "Well, Satoko?! You should be able to figure it out!!": "沙都子，怎么样？！你应该能想明白的！！",
}

# ---------------------------------------------------------------- save names
HEN = {"Onikakushi": "鬼隐篇", "Watanagashi": "绵流篇", "Tatarigoroshi": "祟杀篇",
       "Himatsubushi": "暇溃篇", "Meakashi": "目明篇", "Tsumihoroboshi": "罪灭篇",
       "Minagoroshi": "皆杀篇", "Matsuribayashi": "祭囃篇"}
JUMPKEY = {"onik_prologue": "鬼隐篇 序章·OP", "tata_prologue": "祟杀篇 序章",
           "hima_prologue": "暇溃篇 序章", "meak_prologue": "目明篇 序章"}


def load_special_save():
    src = open(os.path.join(WORK, "scripts", "gen_cn_assets.py"), encoding="utf-8").read()
    m = re.search(r"SPECIAL_SAVE = (\{.*?\n\})", src, re.S)
    return ast.literal_eval(m.group(1)) if m else {}


SPECIAL = load_special_save()
SAVE_PAT = re.compile(r'^(\w+)-hen\.\s*(.*)$', re.S)


def zh_save_name(en):
    """'Onikakushi-hen.\\nProlouge.' -> '鬼隐篇\\n序章' (keep literal \\n)."""
    flat = en.replace("\\n", " ").strip()
    # ---- misc special shapes ----
    if flat == "Prologue":
        return "序章"
    m_acr = re.match(r'^All-cast Review Session\.\s*(\w+)-hen\.?$', flat)
    if m_acr:
        return "全员感谢会\\n" + HEN.get(m_acr.group(1).replace("Maturibayashi", "Matsuribayashi"), m_acr.group(1))
    CN_NUM = {2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九"}
    dm_part = re.match(r'^(\w+)-hen\.\s*Day (\d+)-(\d+)$', flat)
    if dm_part:
        hen = HEN.get(dm_part.group(1))
        if hen:
            sub = CN_NUM.get(int(dm_part.group(3)), str(dm_part.group(3)))
            return hen + "\\n第%s天·其%s" % (dm_part.group(2), sub)
    dm_ep = re.match(r'^(\w+)-hen\.\s*Epilogue,\s*(.+)$', flat)
    if dm_ep:
        hen = HEN.get(dm_ep.group(1))
        if hen:
            tail = {"cassette tape": "磁带", "The End": "THE END"}.get(dm_ep.group(2), dm_ep.group(2))
            return hen + "\\n尾声·" + tail
    # ---- kai special shapes ----
    if flat.startswith("Connecting Fragments."):
        from patch_screens import K_LIST
        extra = {"The final miracle": "最后的奇迹"}
        rest = flat[len("Connecting Fragments."):].strip()
        if rest in ("Prologue",):
            return "碎片连接。\\n序章"
        if rest in ("End",):
            return "碎片连接。\\n终章"
        return "碎片连接。\\n" + K_LIST.get(rest, extra.get(rest, rest))
    if flat.startswith("Staff Room."):
        rest = flat[len("Staff Room."):].strip()
        return "制作组房间\\n" + HEN.get(rest, rest)
    m = SAVE_PAT.match(flat)
    if not m:
        return None
    hen = HEN.get(m.group(1)) or HEN.get(m.group(1).replace("Maturibayashi", "Matsuribayashi"))
    if not hen:
        return None
    rest = m.group(2).strip()
    if rest in ("", "Prolouge.", "Prologue"):
        return hen + "\\n序章"
    if rest == "Epilogue":
        return hen + "\\n尾声"
    if rest in ("END", "BADEND"):
        return hen + "\\n" + ("END" if rest == "END" else "BAD END")
    if rest == "Onigari-no-ryuuou":
        return hen + "\\n鬼狩之柳王"
    if rest.startswith("Connecting Fragments."):
        tail = rest[len("Connecting Fragments."):].strip()
        sub = {"Prologue": "序章", "End": "终章"}.get(tail, tail)
        return hen + "\\n碎片连接。" + sub
    if rest == "#3 Koizumi-sensei":
        return hen + "\\n#3 小泉老师"
    if rest in SPECIAL:
        return hen + "\\n" + SPECIAL[rest]
    if re.match(r'^#\d+$', rest):
        return hen + "\\n" + rest
    dm = re.match(r'^Day (\d+)$', rest)
    if dm:
        return hen + "\\n第%s天" % dm.group(1)
    dm = re.match(r'^Day (\d+),\s*(.+)$', rest)
    if dm and ("Day %s, %s" % (dm.group(1), dm.group(2))) in SPECIAL:
        return hen + "\\n" + SPECIAL["Day %s, %s" % (dm.group(1), dm.group(2))]
    if dm:
        return hen + "\\n第%s天 %s" % (dm.group(1), dm.group(2))
    return None


# ---------------------------------------------------------------- appliers
def strip_wrap(t):
    prefixes = ["{font=Times.ttf}{b}", "{font=Times.ttf}", "{b}"]
    for p in prefixes:
        if t.startswith(p):
            t = t[len(p):]
            break
    m = re.match(r'^\{font=Times.ttf\}\{size=(\d+)\}', t)
    pfx = ""
    if m:
        pfx = "{font=Times.ttf}{size=%s}" % m.group(1)
        t = t[m.end():]
    for sfx in ["{/size}{/font}", "{/font}", "{/b}"]:
        if t.endswith(sfx):
            t = t[:-len(sfx)]
            break
    if pfx:
        t = re.sub(r'\{/size\}\{/font\}$', '', t) if False else t
    return pfx, t


def apply_poems():
    entries = json.load(open(os.path.join(WORK, "poem_lines.json"), encoding="utf-8"))
    ok = miss = 0
    by_file = {}
    for e in entries:
        by_file.setdefault((e["proj"], e["file"]), []).append(e)
    WRAP_LEAD = re.compile(r'^\{(font=Times\.ttf|size=\d+|b|color=#000)\}')
    WRAP_TAIL = re.compile(r'\{(/size|/font|/b)\}$')

    def split_wrap(raw):
        pfx = ""
        t = raw
        while True:
            m = WRAP_LEAD.match(t)
            if not m:
                break
            pfx += m.group(0)
            t = t[m.end():]
        sfx = ""
        while True:
            m = WRAP_TAIL.search(t)
            if not m:
                break
            sfx = m.group(0) + sfx
            t = t[:m.start()]
        return pfx, t, sfx

    for (proj, rel), items in by_file.items():
        p = os.path.join(WORK, proj, "game", rel.replace("/", os.sep))
        lines = open(p, encoding="utf-8").read().split("\n")
        changed = False
        for e in items:
            raw = e["text"]
            pfx, core, sfx = split_wrap(raw)
            zh = POEMS.get(core)
            if zh is None:
                print(f"  !! poem unmatched {rel}:{e['line']}: {core[:60]}")
                miss += 1
                continue
            newq = '"' + pfx + zh.replace('\\', '\\\\').replace('"', '\\"') + sfx + '"'
            lines[e["line"] - 1] = re.sub(r'show text "(?:[^"\\]|\\.)*"',
                                          'show text ' + newq.replace("\\", "\\\\"),
                                          lines[e["line"] - 1], count=1)
            changed = True
            ok += 1
        if changed:
            open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print(f"poems: {ok} translated, {miss} unmatched")


def apply_menus():
    items = json.load(open(os.path.join(WORK, "menu_items.json"), encoding="utf-8"))
    ok = miss = 0
    for e in items:
        zh = MENUS.get(e["text"])
        if not zh:
            print(f"  !! menu unmatched {e['file']}:{e['line']}: {e['text'][:50]}")
            miss += 1
            continue
        p = os.path.join(WORK, e["proj"], "game", e["file"].replace("/", os.sep))
        lines = open(p, encoding="utf-8").read().split("\n")
        lines[e["line"] - 1] = re.sub(r'"(?:[^"\\]|\\.)*"', '"' + zh.replace('"', '\\"') + '"',
                                      lines[e["line"] - 1], count=1)
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
        ok += 1
    print(f"menus: {ok} translated, {miss} unmatched")


def write_name_tl():
    """tl strings for full save_name strings + prologue jump keys."""
    for proj, chdir_first in (("project", None), ("project_k", None)):
        names = {}
        import subprocess
        # reuse extraction: walk .rpy for save_name
        PAT = re.compile(r'\$ save_name = __\("((?:[^"\\]|\\.)*)"\)')
        for dp, _, fs in os.walk(os.path.join(WORK, proj, "game")):
            for f in fs:
                if not f.endswith(".rpy"):
                    continue
                for l in open(os.path.join(dp, f), encoding="utf-8"):
                    m = PAT.search(l)
                    if m:
                        names[m.group(1)] = zh_save_name(m.group(1))
        entries = {k: v for k, v in names.items() if v}
        entries.update(JUMPKEY)
        # skip keys already translated in zz_common.rpy (duplicate old = error)
        common_p = os.path.join(WORK, proj, "game", "tl", "schinese", "zz_common.rpy")
        if os.path.exists(common_p):
            have = set(re.findall(r'^\s*old "((?:[^"\\]|\\.)*)"',
                                  open(common_p, encoding="utf-8").read(), re.M))
            entries = {k: v for k, v in entries.items() if k not in have}
        out = ["# -*- coding: utf-8 -*-", "# 章节存档名（自动生成）", "translate schinese strings:"]
        for k in sorted(entries):
            out.append(f'    old "{k}"')
            out.append(f'    new "{entries[k]}"')
        d = os.path.join(WORK, proj, "game", "tl", "schinese")
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "zz_names.rpy"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
        print(f"{proj}: zz_names.rpy ({len(entries)} entries)")


def misc_patches():
    for proj in ("project", "project_k"):
        # boot-guard text lives in script.rpy
        p = os.path.join(WORK, proj, "game", "script.rpy")
        src = open(p, encoding="utf-8").read()
        n = 0
        if 'show text "Something went wrong."' in src:
            src = src.replace('show text "Something went wrong."', 'show text "出错了。"')
            n += 1
        open(p, "w", encoding="utf-8", newline="\n").write(src)
        # screens.rpy: official OP prompt text
        p2 = os.path.join(WORK, proj, "game", "screens.rpy")
        src2 = open(p2, encoding="utf-8").read()
        old_t = "text u'视频开场可能包含轻微剧透。\\n仍要启用吗？'"
        if old_t in src2:
            src2 = src2.replace(old_t, "text u'OP 动画中包含剧透，是否要启用？'")
            n += 1
        open(p2, "w", encoding="utf-8", newline="\n").write(src2)
        print(f"{proj} misc: {n}")
    # tl strings for the OP prompt buttons
    for proj in ("project", "project_k"):
        p = os.path.join(WORK, proj, "game", "tl", "schinese", "zz_common.rpy")
        if not os.path.exists(p):
            continue
        src = open(p, encoding="utf-8").read()
        src = src.replace('new "启用开场动画"', 'new "启用 OP"').replace('new "禁用开场动画"', 'new "禁用 OP"')
        open(p, "w", encoding="utf-8", newline="\n").write(src)
    print("tl button text updated")


OPS_Q = [("zz_op_onik", "onik_op", "mv01"),
         ("zz_op_wata", "wata_001", "wata"),
         ("zz_op_tata", "tatarigoroshi_prologue", "tata"),
         ("zz_op_hima", "himatsubushi_prologue", "hima")]
OPS_K = [("zz_op_meak", "meakashi_prologue", "meak"),
         ("zz_op_tsum", "tsumihoroboshi_prologue", "tsum"),
         ("zz_op_mina", "minagoroshi_prologue", "mina"),
         ("zz_op_matu", "matsuribayashi_prologue", "matu")]

START_MAP_Q = {"onik_op": "zz_op_onik",
               "wata_001": "zz_op_wata", "tatarigoroshi_prologue": "zz_op_tata",
               "himatsubushi_prologue": "zz_op_hima"}
START_MAP_K = {"meakashi_prologue": "zz_op_meak", "tsumihoroboshi_prologue": "zz_op_tsum",
               "minagoroshi_prologue": "zz_op_mina", "matsuribayashi_prologue": "zz_op_matu"}

ZZ_OP_HEAD = """\
# -*- coding: utf-8 -*-
# 章节开场动画（自动生成）。
#
# 触发规则（第 7 轮）：从菜单/章节选择进入某章时，入口别名标签把该章名写进
# renpy._zz_op_pending；该章脚本里的锚点 call zz_op_at("xxx") 取用一次即清除。
# 于是"每次从菜单开新档都播"，而"跳关/读档"不经过别名标签，就不播。
#
# 播放规则：
#   * 设置里 OP=关：直接返回，不播也不打断快进；
#   * 到达锚点时若处于快进/自动模式，先自动关掉（快进指示器熄灭）；
#   * 起播后 0.9 秒起步保护：这段交互里没有任何点击行为，吞掉快进末尾残click；
#   * 保护期后换成可关闭的交互：手动点击可立即跳过 OP，不锁死；
#   * 播放全程把 music/ambient/repeated/sound/voice* 暂停（不是销毁），
#     结束后解除暂停，原曲从原位置继续 —— OP 里不会混入游戏 BGM，
#     播完也绝不会静音卡死。

default persistent.opening = True

init 9 python:
    if persistent._zz_op_migrate is None:
        persistent.opening = True
        persistent._zz_op_migrate = True

init -10 python:
    # 每章待播标记。挂在 renpy 模块上：不进存档、不参与回滚，进程内有效。
    if not hasattr(renpy, "_zz_op_pending"):
        renpy._zz_op_pending = set()

    # OP 期间需要静音的声道（movie 通道本身除外）。
    ZzOpChannels = ("music", "ambient", "repeated", "sound", "sound2",
                    "voice", "voice1", "voice2", "voice3", "voice4",
                    "voice5", "voice6", "voice7", "voice8")

    def zz_op_stop_modes():
        # 关掉快进（右下角双三角）与自动模式，返回是否改动过。
        changed = False
        try:
            if renpy.config.skipping:
                renpy.config.skipping = None
                changed = True
        except Exception:
            pass
        try:
            if _preferences.afm_enable:
                _preferences.afm_enable = False
                changed = True
        except Exception:
            pass
        if changed:
            renpy.restart_interaction()
        return changed

    def zz_op_pause_audio():
        # 暂停而不是停止：不销毁队列、不丢播放位置，解除暂停后原样继续。
        for ch in ZzOpChannels:
            try:
                renpy.audio.music.set_pause(True, channel=ch)
            except Exception:
                pass

    def zz_op_resume_audio():
        for ch in ZzOpChannels:
            try:
                renpy.audio.music.set_pause(False, channel=ch)
            except Exception:
                pass

    def zz_op_play(name):
        path = "movie/" + name + ".ogv"
        if not renpy.loader.loadable(path):
            print("ZZOP missing movie: " + path)
            return

        saved_rollback_side = renpy.config.enable_rollback_side
        zz_op_pause_audio()
        try:
            renpy.config.enable_rollback_side = False
            renpy.movie_start_fullscreen(path)

            # ① 起步保护 0.9 秒：只有定时器，没有任何点击行为 → 手点无效。
            renpy.ui.pausebehavior(0.9, False)
            renpy.ui.interact(suppress_overlay=True)

            # ② 正常播放：手点跳过，或视频播完（movie 通道停止）自然结束。
            renpy.ui.saybehavior()
            renpy.ui.soundstopbehavior("movie")
            renpy.ui.interact(suppress_overlay=True)
        finally:
            renpy.config.enable_rollback_side = saved_rollback_side
            try:
                renpy.movie_stop()
            except Exception:
                pass
            zz_op_resume_audio()

    def zz_op_take_pending(name):
        # 取用一次就清除；无论 OP 开关如何都清，避免旧标记留到下次。
        pending = getattr(renpy, "_zz_op_pending", None)
        if pending is None:
            pending = renpy._zz_op_pending = set()
        if name in pending:
            pending.discard(name)
            return True
        return False

    def zz_op_should_play(name):
        taken = zz_op_take_pending(name)
        print("ZZOP at %s: pending=%s opening=%s" % (name, taken, persistent.opening))
        return taken and persistent.opening

label zz_op_at(name):
    if zz_op_should_play(name):
        $ zz_op_stop_modes()
        scene black with Dissolve(0.4)
        $ zz_op_play(name)
        scene black with Dissolve(0.4)
    return
"""


# PC 版逐章 OP 插入点（逐章对照 PC Update/*.txt 的 ModCallScriptSection("&opening")）。
# 所有锚点都落在"序章已结束、Day 1 尚未开始"处，与 PC 一致。
# pre = 在 OP 之前追加的语句（PC 在这些位置会先淡出 BGM，避免 OP 后 BGM 拖到章名卡上）。
OP_ANCHORS = {
    "project": [
        # CH2 绵流：logo/警告卡之后、黑屏、Day 1 首句之前（PC: DrawScene("logo") 后调 OP）
        # 此处 music/ambient 已由脚本 stop，无需 pre
        ("watanagashi/wata_001.rpy", "wata", "before", r'^    play ambient lsys22$', []),
        # CH3 祟杀：序章 logo + 黑场之后、Day 1 之前（PC 同位置；此处已静音）
        ("tatarigoroshi/tata_001.rpy", "tata", "before", r'^    jump tata_001$', []),
        # CH4 暇溃：序章 title + 黑场之后、Day 1 之前（PC 同位置，PC 先 FadeOutBGM）
        ("himatsubushi/hima_001.rpy", "hima", "before", r'^    jump hima_001$',
         ['    stop music fadeout 1.0', '    stop ambient fadeout 1.0']),
    ],
    "project_k": [
        # CH5 目明：序章旁白结束、环境音已停、章名卡之前（PC 同位置）
        ("meakashi/meak_001.rpy", "meak", "before", r'^    play music t1_thanks$', []),
        # CH6 罪灭：序章末句之后、章名卡之前（PC 同位置，PC 先 FadeOutBGM）
        ("tsumihoroboshi/tsum_op.rpy", "tsum", "after", r'^    n "我们相信只有这种举动绝对不会伤害到蕾娜。"$',
         ['    stop music fadeout 1.0', '    stop ambient fadeout 1.0']),
        # CH7 皆杀：序章旁白 + 独白诗之后、注意卡/章名卡之前（PC 先 FadeOutBGM）
        ("minagoroshi/mina_op.rpy", "mina", "before", r'^    show text tyuui with Dissolve\(1\.0\)$',
         ['    stop music fadeout 1.0', '    stop ambient fadeout 1.0']),
        # CH8 祭囃：鹰野对决高潮之后、章名卡之前（PC: 黑场 + FadeOutBGM 后调 OP）
        ("matsuribayashi/mats_007.rpy", "matu", "after", r'^    extend " 尽管放马过来吧，你这————！！」"$',
         ['    stop music fadeout 1.0', '    stop ambient fadeout 1.0']),
        # CH1 鬼隐：原生 enable_opening 块改成 call zz_op_at("mv01")，见 patch_onik_native()
    ],
}


ZZ_OP_BEGIN = "    # zz-op-begin"
ZZ_OP_END = "    # zz-op-end"


def strip_op_calls():
    """删除两项目所有 OP 插入块（call zz_op_pre/zz_op_at + 标记行 + pre 语句）。
    onik_op.rpy 的调用由 patch_onik_native() 独占管理，这里跳过。"""
    n = 0
    for proj in ("project", "project_k"):
        root = os.path.join(WORK, proj, "game")
        for dp, _dn, fs in os.walk(root):
            for f in fs:
                if not f.endswith(".rpy") or f == "zz_op.rpy":
                    continue
                if proj == "project" and f == "onik_op.rpy":
                    continue
                p = os.path.join(dp, f)
                src = open(p, encoding="utf-8").read()
                if "zz-op-begin" not in src and "call zz_op_at(" not in src \
                        and "call zz_op_pre(" not in src:
                    continue
                keep = []
                skipping = False
                for l in src.split("\n"):
                    s = l.strip()
                    if s == "# zz-op-begin":
                        skipping = True
                        n += 1
                        continue
                    if s == "# zz-op-end":
                        skipping = False
                        continue
                    if skipping:
                        continue
                    # 兼容第 6 轮遗留的无标记 call 行
                    if s.startswith("call zz_op_pre(") or s.startswith("call zz_op_at("):
                        n += 1
                        continue
                    keep.append(l)
                out = "\n".join(keep)
                if out != src:
                    open(p, "w", encoding="utf-8", newline="\n").write(out)
    print(f"op: stripped {n} old op blocks")


def _find_unique(lines, pat, rel):
    hits = [i for i, l in enumerate(lines) if re.search(pat, l)]
    assert len(hits) == 1, f"op anchor not unique ({len(hits)} hits): {rel} / {pat}"
    return hits[0]


def insert_op_anchors():
    for proj, anchors in OP_ANCHORS.items():
        for rel, name, mode, pat, pre in anchors:
            p = os.path.join(WORK, proj, "game", rel.replace("/", os.sep))
            lines = open(p, encoding="utf-8").read().split("\n")
            hit = _find_unique(lines, pat, rel)
            block = [ZZ_OP_BEGIN] + list(pre) + [f'    call zz_op_at("{name}")', ZZ_OP_END]
            pos = hit if mode == "before" else hit + 1
            lines[pos:pos] = block
            open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
            print(f'  {rel}: zz_op_at("{name}") @ line {pos + len(block)} ({mode}, pre={len(pre)})')


def patch_onik_native():
    """鬼隐篇：去掉 darwin 原生"是否启用 OP"弹窗，改走统一的 call zz_op_at("mv01")。
    幂等：原生块、旧 call、两者都没有这三种状态都能收敛到"jump onik_000 前恰好一条 call"。"""
    p = os.path.join(WORK, "project", "game", "onikakushi", "onik_op.rpy")
    src = open(p, encoding="utf-8").read()

    native = re.compile(
        r'    call screen enable_opening with spiral2\n'
        r'\n'
        r'    if persistent\.opening:\n'
        r'        \$ renpy\.movie_cutscene\("movie/mv01\.ogv"\)\n'
        r'        scene black with Dissolve\(2\.0\)\n')
    removed = bool(native.search(src))
    src = native.sub("", src)

    call_line = '    call zz_op_at("mv01")\n'
    src = re.sub(r'    call zz_op_at\("mv01"\)\n', "", src)

    # 插到 `jump onik_000` 之前
    m = re.search(r'^    jump onik_000$', src, re.M)
    assert m, "onik_op: jump onik_000 not found"
    src = src[:m.start()] + call_line + "\n" + src[m.start():]

    open(p, "w", encoding="utf-8", newline="\n").write(src)
    print(f'onik_op: native_block_removed={removed}, call zz_op_at("mv01") ensured')


def write_ops_and_rewire():
    for proj, ops, smap in (("project", OPS_Q, START_MAP_Q),
                            ("project_k", OPS_K, START_MAP_K)):
        parts = [ZZ_OP_HEAD, ""]
        # 入口别名：从菜单/章节选择进入本章时置 pending（跳关/读档不经过这里）
        for alias, target, name in ops:
            parts.append(f"label {alias}:")
            parts.append(f'    $ renpy._zz_op_pending.add("{name}")')
            parts.append(f"    jump {target}")
            parts.append("")
        open(os.path.join(WORK, proj, "game", "zz_op.rpy"), "w", encoding="utf-8",
             newline="\n").write("\n".join(parts))
        # rewire Start() inside chapter_select / mode_prompt only (idempotent)
        p = os.path.join(WORK, proj, "game", "screens.rpy")
        lines = open(p, encoding="utf-8").read().split("\n")
        screen = None
        n = 0
        for i, l in enumerate(lines):
            m = re.match(r"^screen (\w+):", l)
            if m:
                screen = m.group(1)
                continue
            if screen in ("chapter_select", "mode_prompt"):
                for k, v in smap.items():
                    if f"Start('{k}')" in l:
                        lines[i] = l.replace(f"Start('{k}')", f"Start('{v}')"); n += 1
                    elif f'Start("{k}")' in l:
                        lines[i] = l.replace(f'Start("{k}")', f'Start("{v}")'); n += 1
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
        print(f"{proj}: zz_op.rpy written, {n} Start() rewired")
    strip_op_calls()
    insert_op_anchors()
    patch_onik_native()


def copy_movies():
    m = {"ch2": ("project", "wata"), "ch3": ("project", "tata"), "ch4": ("project", "hima"),
         "ch5": ("project_k", "meak"), "ch6": ("project_k", "tsum"),
         "ch7": ("project_k", "mina"), "ch8": ("project_k", "matu")}
    for ch, (proj, name) in m.items():
        src = os.path.join(WORK, "ops", ch + ".ogv")
        if not os.path.exists(src):
            print(f"  !! missing {ch}.ogv")
            continue
        d = os.path.join(WORK, proj, "game", "movie", name + ".ogv")
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if not os.path.exists(d) or os.path.getsize(d) != os.path.getsize(src):
            shutil.copy2(src, d)
            print(f"  copied {ch} -> {proj}/movie/{name}.ogv ({os.path.getsize(src)//1048576}MB)")


if __name__ == "__main__":
    import fix_percent_escape
    fix_percent_escape.main()
    apply_poems()
    apply_menus()
    write_name_tl()
    misc_patches()
    write_ops_and_rewire()
    copy_movies()
