# -*- coding: utf-8 -*-
"""Generate zz_ui.rpy for both port projects: native Chinese UI screens.

  - screen preferences (native rebuild, hbox rows, zz_bar sliders)
  - screen yesno_prompt
  - screen tips_* (native lists, official Chinese titles, context-aware back)
  - menu screens rebuilt natively (extra_main / omake_rooms / omake_unlock /
    omake_cast / tips_main / omake_staff)
  - tips popup image overrides (native text cards, per UnlockChapter)
  - translate strings: jump-label keys + kai literal day titles
"""
import json
import os
import re
import sys

WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(WORK, "corpus")

TIPS_SCREENS = {
    "project": {"tips_onik": ("chapter_onik", "onikakushi"), "tips_wata": ("chapter_wata", "watanagashi"),
                "tips_tata": ("chapter_tata", "tatarigoroshi"), "tips_hima": ("chapter_hima", "himatsubushi")},
    "project_k": {"tips_meak": ("chapter_meak", "meakashi"), "tips_tumi": ("chapter_tumi", "tsumihoroboshi"),
                  "tips_mina": ("chapter_mina", "minagoroshi")},
}
TIPS_CH = {"tips_onik": 1, "tips_wata": 2, "tips_tata": 3, "tips_hima": 4,
           "tips_meak": 5, "tips_tumi": 6, "tips_mina": 7}

MENU_SCREENS = ["extra_main", "omake_rooms", "omake_unlock", "omake_cast", "tips_main", "omake_staff"]

LABELS = {
    ("extra_main", "omake_cast"): "全员感谢会",
    ("extra_main", "omake_staff"): "制作组房间",
    ("extra_main", "omake_rooms"): "附加房间",
    ("extra_main", "omake_unlock"): "解锁全部章节",
    ("extra_main", "Return()"): "退出",
    ("omake_rooms", "tips_main"): "小知识",
    ("omake_rooms", "cg_gallery"): "CG 画廊",
    ("omake_rooms", "extra_main"): "返回",
    ("omake_unlock", "unlock_onik"): "解锁 鬼隐篇",
    ("omake_unlock", "unlock_wata"): "解锁 绵流篇",
    ("omake_unlock", "unlock_tata"): "解锁 祟杀篇",
    ("omake_unlock", "unlock_hima"): "解锁 暇溃篇",
    ("omake_unlock", "otsukaresama_meakashi"): "解锁 目明篇",
    ("omake_unlock", "otsukaresama_tsumihoroboshi"): "解锁 罪灭篇",
    ("omake_unlock", "otsukaresama_minagoroshi"): "解锁 皆杀篇",
    ("omake_unlock", "otsukaresama_matsuribayashi"): "解锁 祭囃篇",
    ("omake_unlock", "extra_main"): "返回",
    ("omake_cast", "onikakushi_omake"): "鬼隐篇",
    ("omake_cast", "watanagashi_omake"): "绵流篇",
    ("omake_cast", "tatarigoroshi_omake"): "祟杀篇",
    ("omake_cast", "himatsubushi_omake"): "暇溃篇",
    ("omake_cast", "extra_main"): "返回",
    ("omake_staff", "staffroom_meakashi"): "目明篇",
    ("omake_staff", "staffroom_tsumihoroboshi"): "罪灭篇",
    ("omake_staff", "staffroom_minagoroshi"): "皆杀篇",
    ("omake_staff", "staffroom_matsuribayashi"): "祭囃篇",
    ("omake_staff", "extra_main"): "返回",
    ("tips_main", "mainmenu_onik"): "鬼隐篇",
    ("tips_main", "mainmenu_wata"): "绵流篇",
    ("tips_main", "mainmenu_tata"): "祟杀篇",
    ("tips_main", "mainmenu_hima"): "暇溃篇",
    ("tips_main", "mainmenu_meak"): "目明篇",
    ("tips_main", "mainmenu_tumi"): "罪灭篇",
    ("tips_main", "mainmenu_mina"): "皆杀篇",
    ("tips_main", "final_tip"): "祭囃篇·最终",
    ("tips_main", "omake_rooms"): "返回",
}

KAI_JUMP = {
    "1982": "1982年", "1983": "1983年", "50 Fragments": "50枚碎片",
    "Against Oryou!": "对抗阿魉！", "Connecting Fragments": "连接碎片",
    "Conversation with Mion": "与魅音的对话",
    "Encounter with Satoshi-kun": "与悟史哥的相遇",
    "Second encounter with Satoshi-kun": "与悟史哥的重逢",
    "Evening call": "傍晚的来电", "Everything is better than ever": "一切都比以往更好",
    "From Rika's view": "梨花的视角", "Hinamizawa Fighters": "雏见泽斗士",
    "Hinamizawa School": "雏见泽学校", "In the town council": "在町内会",
    "Interrogate in the torture room": "拷问室里的审问",
    "Keiichi's counterattack": "圭一的反击", "Looking for a solution": "寻找对策",
    "Midnight of Watanagashi of 1983": "1983年绵流祭之夜",
    "Morning after Watanagshi": "绵流祭翌日早晨", "Mountain Dogs' turn": "山狗的行动",
    "Offer to host the auction": "提出主办拍卖会", "Ooishi's disappearance": "大石的失踪",
    "Ooishi's warning": "大石的警告", "Oyashiro-sama's curse": "御社神大人的祟杀",
    "Rika and Ooishi": "梨花与大石", "Rika's efforts": "梨花的努力",
    "Rika's fall off the cliff": "梨花坠崖", "Satoko attending school": "沙都子上学去了",
    "Shion calls Keiichi": "诗音致电圭一", "Sonozaki Main House": "园崎本家",
    "Takano's turn": "鹰野的行动", "Talking to Takano and Tomitake": "与鹰野和富竹谈话",
    "The Onigafuchi Guardians": "鬼渊守护会", "The aunt has died": "叔母死了",
    "The child consultation center": "儿童相谈所", "The day I die": "我死去的日子",
    "The disappearance": "消失", "The first morning of freedom": "重获自由的早晨",
    "The friends came": "伙伴们来了", "The last day": "最后一天", "The meeting": "会面",
    "The next day at school": "翌日的学校", "The next day...": "第二天……",
    "The spirit of Hinamizawa": "雏见泽之魂", "The world with the least luck": "最不走运的世界",
    "They don't have a sense of danger": "她们没有危机感",
    "Toy store in Okinomiya": "兴宫的玩具店", "Epilogue": "尾声", "Prologue": "序章", "Watanagashi": "绵流祭",
    "Watanagashi of 1982": "1982年的绵流祭", "Watanagashi of 1983": "1983年的绵流祭",
    "What could have been...": "如果那时……", "With Rena at the bus stop": "与蕾娜在巴士站",
}


def load_tips_titles():
    data = {}
    p = os.path.join(CORPUS, "tips_zh.json")
    if os.path.exists(p):
        raw = json.load(open(p, encoding="utf-8"))
        for ch, entries in raw.items():
            data[int(ch)] = entries
    for ch in (4, 5, 6):
        p2 = os.path.join(CORPUS, "tips_zh_%d.json" % ch)
        if os.path.exists(p2):
            data[ch] = json.load(open(p2, encoding="utf-8"))
    return data


def screen_block(src, name):
    m = re.search(rf'^screen {name}:\n(.*?)(?=^screen |\Z)', src, re.M | re.S)
    return m.group(0) if m else None


def parse_tips_gates(src, screen_name):
    blk = screen_block(src, screen_name)
    if not blk:
        return []
    out = []
    cond = "True"
    for line in blk.split("\n"):
        m = re.match(r'\s*if (.+):\s*$', line)
        if m:
            cond = m.group(1)
            continue
        hm = re.search(r'Jump\("(\w+)"\)', line) or re.search(r"Jump\('(\w+)'\)", line)
        if hm:
            out.append({"label": hm.group(1), "cond": cond})
    return out


def gen_tips_screens(src, proj):
    tips_data = load_tips_titles()
    parts = []
    for sname, (flag, _chdir) in TIPS_SCREENS[proj].items():
        ch = TIPS_CH[sname]
        entries = tips_data.get(ch, [])
        by_label = {e["Script"].lstrip("_"): e for e in entries}
        gates = parse_tips_gates(src, sname)
        lines = [f"screen {sname}:", "    tag menu", "",
                 "    key 'rollback' action NullAction()", "    key 'hide_windows' action NullAction()",
                 "    key 'game_menu' action NullAction()", "    key 'dismiss' action NullAction()", "",
                 '    add "tips/tips_bg.png"', ""]
        rows = []
        for i, g in enumerate(gates):
            e = by_label.get(g["label"])
            title = (e or {}).get("Title") or g["label"]
            row, col = i // 2, i % 2
            x = 104 if col == 0 else 666
            y = 108 + row * 62
            esc = title.replace('"', '\\"')
            rows.append((y, x, g, esc))
        height = 120 + ((len(rows) + 1) // 2) * 62
        lines += ["    viewport:", "        draggable True", "        mousewheel True",
                  f"        child_size (1280, {max(height, 720)})", "        fixed:"]
        for y, x, g, esc in rows:
            act = f'[Hide("{sname}", transition=fade), Jump("{g["label"]}")]'
            lines.append(f'            if {g["cond"]}:')
            lines.append(f'                textbutton "{esc}" action {act} text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos {x} ypos {y} xsize 520 ysize 56 text_align 0.0')
            lines.append('            else:')
            lines.append(f'                text "？？？" size 24 color "#a99a85" xpos {x} ypos {y+8}')
        lines += ['    textbutton "返回" action If(tips.startswith("mainmenu"), Return(), Show("day_completed", transition=fade)) xpos 1164 ypos 26 style "zz_back_btn"', "", ""]
        parts.append("\n".join(lines))
    return parts


def gen_menu_screen(src, name, proj):
    blk = screen_block(src, name)
    if not blk:
        return None
    items = []
    cond = None
    music = []
    for line in blk.split("\n"):
        m = re.match(r'\s*if (.+):\s*$', line)
        if m:
            cond = m.group(1)
            continue
        hm = re.match(r'\s*hotspot \([^)]*\)(?:\s+activate_sound [\'"][^\'"]+[\'"])?\s+action (.+)$', line)
        if hm:
            act = hm.group(1).strip()
            label = None
            for key, zh in LABELS.items():
                sname, sub = key
                if sname == name and sub in act:
                    label = zh
                    break
            if label is None:
                continue
            items.append((cond, act, label))
            cond = None
            continue
        mm = re.match(r"\s*on ['\"](show|replace|hide|replaced)['\"] action (.+)$", line)
        if mm:
            music.append(f'    on "{mm.group(1)}" action {mm.group(2)}')
    if not items:
        return None
    lines = [f"screen {name}:", "    tag menu", "", '    add "efe/black.jpg" alpha 0.75', "",
             "    vbox:", "        xalign 0.5", "        yalign 0.42", "        spacing 22", ""]
    for c, act, label in items:
        esc = label.replace('"', '\\"')
        if c:
            lines.append(f"        if {c}:")
            lines.append(f'            textbutton "{esc}" action {act} style "zz_menu_btn"')
        else:
            lines.append(f'        textbutton "{esc}" action {act} style "zz_menu_btn"')
    lines.append("")
    lines += music
    lines += ["", ""]
    return "\n".join(lines)


STYLES = '''
style zz_bar is bar:
    xsize 326
    ysize 19
    left_bar "efe/slider.png"
    right_bar "efe/slider.png"
    thumb "efe/thumb.png"
    hover_thumb "efe/thumb_hover.png"
    thumb_offset 12
    keyboard_focus True

style zz_menu_btn is button:
    background "efe/zz_capsule_idle.png"
    hover_background "efe/zz_capsule_hover.png"
    xminimum 360
    yminimum 78
    xalign 0.5

style zz_menu_btn_text is default:
    size 30
    color "#eef2fa"
    hover_color "#ffffff"
    selected_color "#ffe9a8"
    outlines [(1, "#0a1428", 1, 1)]
    xalign 0.5
    text_align 0.5

style zz_menu_btn_small is zz_menu_btn:
    xminimum 240
    yminimum 62

style zz_menu_btn_small_text is zz_menu_btn_text:
    size 26

style zz_pref_btn is button:
    background "efe/zz_small_idle.png"
    hover_background "efe/zz_small_hover.png"
    selected_background "efe/zz_small_hover.png"
    xminimum 140
    yminimum 46

style zz_pref_btn_text is default:
    size 22
    color "#dfe4f0"
    hover_color "#ffffff"
    selected_color "#ffe9a8"
    xalign 0.5
    text_align 0.5

style zz_yesno_btn is button:
    background "efe/zz_small_idle.png"
    hover_background "efe/zz_small_hover.png"
    xminimum 150
    yminimum 52

style zz_yesno_btn_text is default:
    size 28
    color "#f2ead8"
    hover_color "#ffffff"
    xalign 0.5

style zz_back_btn is button:
    background None
    hover_background None

style zz_back_btn_text is default:
    size 24
    color "#c8bfa8"
    hover_color "#ffffff"
    outlines [(1, "#000000", 1, 1)]
'''


PREFS = '''
screen preferences:
    tag menu

    add "efe/black.jpg" alpha 0.5
    add "efe/zz_prefs_panel.png" xpos 40 ypos 24

    imagebutton:
        idle "efe/back_off.png"
        hover "efe/back_on.png"
        xpos 1164 ypos 26
        action Return()

    text "设 置" xalign 0.5 ypos 44 size 36 color "#e8c88a"

    # ---------------- left column ----------------
    vbox xpos 88 ypos 104 spacing 8:
        text "音量" size 26 color "#e8c88a"
        null height 2
        hbox spacing 18:
            text "BGM 音量" size 22 color "#e8e2d2" min_width 200 yalign 0.5
            bar value Preference("music volume") style "zz_bar"
        hbox spacing 18:
            text "音效音量" size 22 color "#e8e2d2" min_width 200 yalign 0.5
            bar value Preference("sound volume") style "zz_bar"
        hbox spacing 18:
            text "语音音量" size 22 color "#e8e2d2" min_width 200 yalign 0.5
            bar value Preference("voice volume") style "zz_bar"

        null height 8
        text "文字" size 26 color "#e8c88a"
        null height 2
        hbox spacing 18:
            text "文字速度" size 22 color "#e8e2d2" min_width 200 yalign 0.5
            bar value Preference("text speed") style "zz_bar"
        hbox spacing 18:
            text "自动推进等待" size 22 color "#e8e2d2" min_width 200 yalign 0.5
            bar value Preference("auto-forward time") style "zz_bar"

    vbox xpos 88 ypos 464 spacing 8:
        text "对话框样式" size 22 color "#e8c88a"
        hbox spacing 16:
            textbutton "ADV 模式" action [SetField(persistent, "adv_mode", True), Function(mode_change, "adv")] style "zz_pref_btn"
            textbutton "NVL 模式" action [SetField(persistent, "adv_mode", False), Function(mode_change, "nvl")] style "zz_pref_btn"
        null height 6
        text "跳过文字" size 22 color "#e8c88a"
        hbox spacing 16:
            textbutton "全部" action Preference("skip", "all") style "zz_pref_btn"
            textbutton "仅已读" action Preference("skip", "seen") style "zz_pref_btn"

    # ---------------- right column ----------------
    vbox xpos 664 ypos 104 spacing 8:
        text "语音匹配等级" size 26 color "#e8c88a"
        hbox spacing 14 yalign 0.5:
            textbutton "－" action If(persistent.vm_level > 0, SetField(persistent, "vm_level", persistent.vm_level - 1)) style "zz_pref_btn"
            text "[persistent.vm_level]" size 38 color "#ffffff" yalign 0.5 min_width 70 text_align 0.5
            textbutton "＋" action If(persistent.vm_level < 5, SetField(persistent, "vm_level", persistent.vm_level + 1)) style "zz_pref_btn"
        text "调整语音与文本的匹配程度：\\n0 = PC 原版文本（未删改，部分语音缺失）\\n2 = 默认（推荐）\\n5 = 主机版文本（全语音，删改较多）" size 19 color "#b8ac93" line_leading 4 xsize 500

        null height 10
        text "显示" size 26 color "#e8c88a"
        null height 2
        hbox spacing 16:
            textbutton "全屏" action Preference("display", "fullscreen") style "zz_pref_btn"
            textbutton "窗口" action Preference("display", "window") style "zz_pref_btn"

        null height 10
        text "OP 动画" size 26 color "#e8c88a"
        null height 2
        hbox spacing 16:
            text "开场动画播放" size 22 color "#e8e2d2" min_width 200 yalign 0.5
            textbutton ("开" if persistent.opening else "关") action SetField(persistent, "opening", not persistent.opening) style "zz_pref_btn"
        text "OP 含剧透；快进到 OP 处会自动停下" size 19 color "#b8ac93" line_leading 4 xsize 500

        null height 10
        textbutton "音乐设置" action ShowMenu("__MUSIC__") style "zz_menu_btn_small"
'''

YESNO = '''
screen yesno_prompt:
    modal True
    zorder 5

    key "rollforward" action NullAction()
    key "hide_windows" action NullAction()
    key "toggle_skip" action NullAction()
    key "game_menu" action NullAction()

    add "efe/black.jpg" alpha 0.5

    frame at yesno_transition:
        background "efe/zz_dialog.png"
        xalign 0.5 yalign 0.5
        xsize 700 ysize 240

        text _(message):
            xalign 0.5 ypos 40
            size 30 color "#f2ead8"
            text_align 0.5
            xsize 640

        hbox:
            xalign 0.5 ypos 150
            spacing 80
            textbutton "是" action yes_action style "zz_yesno_btn"
            textbutton "否" action no_action style "zz_yesno_btn"
'''


def gen_popup_overrides(proj):
    tips_data = load_tips_titles()
    src = open(os.path.join(WORK, proj, "game", "screens.rpy"), encoding="utf-8").read()
    lines = ["transform zz_tip_pos(yp):",
             "    ypos yp",
             "    xalign 0.5",
             "",
             "init 25 python:",
             "    def _zz_tip_card(titles):",
             "        parts = [Image('efe/zz_tips_card.png')]",
             "        y = 350",
             "        for t in titles:",
             "            parts.append(At(Text(t, size=34, color='#f5eede', outlines=[(1, '#000', 1, 1)], font='NotoSansCJKsc-Bold.otf'), zz_tip_pos(y)))",
             "            y += 70",
             "        return Fixed(*parts)",
             ""]
    unlock_ch = {}
    for sname, (flag, _d) in TIPS_SCREENS[proj].items():
        ch = TIPS_CH[sname]
        tdata = tips_data.get(ch, [])
        by_label = {e["Script"].lstrip("_"): e for e in tdata}
        gates = parse_tips_gates(src, sname)
        gate_of = {}
        for g in gates:
            m = re.search(r'>=\s*["\']?(\d+)["\']?', g["cond"])
            gate_of[g["label"]] = m.group(1) if m else None
        bd = {}
        for g in gates:
            e = by_label.get(g["label"])
            if not e:
                continue
            if e.get("UnlockChapter") is not None:
                day = int(e["UnlockChapter"])
            else:
                pg = gate_of.get(g["label"])
                if not pg:
                    continue
                day = int(pg) - 1
            if day <= 0:
                continue
            bd.setdefault(day, [])
            if e["Title"] not in bd[day]:
                bd[day].append(e["Title"])
        unlock_ch[ch] = bd
    STEM_CH = {"onik": 1, "wata": 2, "tata": 3, "hima": 4, "meak": 5, "tsum": 6, "mina": 7}
    img_src = ""
    for f in ("script.rpy", "cg_gallery.rpy"):
        p = os.path.join(WORK, proj, "game", f)
        if os.path.exists(p):
            img_src += open(p, encoding="utf-8").read()
    pops = re.findall(r'image (tips_\w+) = "tips/(\w+)\.png"', img_src)
    n = 0
    for img, stem in pops:
        m = re.match(r'([a-z]+)', stem)
        dm = re.search(r'(\d+)', stem)
        if not m or not dm:
            continue
        ch = STEM_CH.get(m.group(1))
        if ch is None or ch not in unlock_ch:
            continue
        titles = unlock_ch[ch].get(int(dm.group(1)))
        if not titles:
            continue
        ts = ", ".join('"%s"' % t.replace('"', '\\"') for t in titles)
        lines.append(f'    renpy.image("{img}", _zz_tip_card([{ts}]))')
        n += 1
    return "\n".join(lines), n


def jump_label_strings(proj):
    sys.path.insert(0, os.path.join(WORK, "scripts"))
    import apply_v4
    entries = []
    for chdir in ("onikakushi", "watanagashi", "tatarigoroshi", "himatsubushi",
                  "meakashi", "tsumihoroboshi", "minagoroshi", "matsuribayashi"):
        d = os.path.join(WORK, proj, "game", chdir)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith(".rpy"):
                continue
            key = f[:-4]
            sn = None
            for line in open(os.path.join(d, f), encoding="utf-8"):
                m = re.search(r'save_name = __\("(.+?)"\)', line)
                if m:
                    sn = m.group(1)
                    break
            if sn:
                zh = apply_v4.zh_save_name(sn)
                if zh:
                    entries.append((key, zh.replace("\\n", " ").replace('"', '\\"')))
    common_p = os.path.join(WORK, proj, "game", "tl", "schinese", "zz_common.rpy")
    have = set()
    if os.path.exists(common_p):
        have = set(re.findall(r'^\s*old "((?:[^"\\]|\\.)*)"',
                              open(common_p, encoding="utf-8").read(), re.M))
    have |= {k for k, _ in entries}
    for k, v in KAI_JUMP.items():
        if k not in have:
            entries.append((k, v))
    return entries


def main():
    for proj, music in (("project", "music_change"), ("project_k", "music_change_kai")):
        src = open(os.path.join(WORK, proj, "game", "screens.rpy"), encoding="utf-8").read()
        parts = ["# -*- coding: utf-8 -*-",
                 "# 中文 UI 原生屏幕（自动生成：设置/确认框/Tips列表/附加菜单/弹窗）",
                 "", STYLES]
        parts.append(PREFS.replace("__MUSIC__", music))
        parts.append(YESNO)
        parts += gen_tips_screens(src, proj)
        for name in MENU_SCREENS:
            s = gen_menu_screen(src, name, proj)
            if s:
                parts.append(s)
        pop, n = gen_popup_overrides(proj)
        parts.append(pop)
        js = jump_label_strings(proj)
        parts.append("translate schinese strings:")
        for k, v in js:
            parts.append(f'    old "{k}"')
            parts.append(f'    new "{v}"')
        text = "\n\n".join(parts) + "\n"
        outp = os.path.join(WORK, proj, "game", "zz_ui.rpy")
        open(outp, "w", encoding="utf-8", newline="\n").write(text)
        print(f"{proj}: zz_ui.rpy written ({len(text)} bytes, popups={n}, jump-labels={len(js)})")


if __name__ == "__main__":
    main()
