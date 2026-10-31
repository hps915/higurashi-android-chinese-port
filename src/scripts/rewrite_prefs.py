# -*- coding: utf-8 -*-
"""Replace the PREFS template inside gen_zz_ui.py with a clean hbox-row layout."""
import re

P = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\scripts\gen_zz_ui.py"
NEW = '''PREFS = \'\'\'
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
            bar value Preference("music volume") style "pref_bar"
        hbox spacing 18:
            text "音效音量" size 22 color "#e8e2d2" min_width 200 yalign 0.5
            bar value Preference("sound volume") style "pref_bar"
        hbox spacing 18:
            text "语音音量" size 22 color "#e8e2d2" min_width 200 yalign 0.5
            bar value Preference("voice volume") style "pref_bar"

        null height 8
        text "文字" size 26 color "#e8c88a"
        null height 2
        hbox spacing 18:
            text "文字速度" size 22 color "#e8e2d2" min_width 200 yalign 0.5
            bar value Preference("text speed") style "pref_bar"
        hbox spacing 18:
            text "自动推进等待" size 22 color "#e8e2d2" min_width 200 yalign 0.5
            bar value Preference("auto-forward time") style "pref_bar"

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
        text "调整语音与文本的匹配程度：\\\n0 = PC 原版文本（未删改，部分语音缺失）\\\n2 = 默认（推荐）\\\n5 = 主机版文本（全语音，删改较多）" size 19 color "#b8ac93" line_leading 4

        null height 10
        text "显示" size 26 color "#e8c88a"
        null height 2
        hbox spacing 16:
            textbutton "全屏" action Preference("display", "fullscreen") style "zz_pref_btn"
            textbutton "窗口" action Preference("display", "window") style "zz_pref_btn"

        null height 10
        textbutton "音乐设置" action ShowMenu("__MUSIC__") style "zz_menu_btn_small"
\'\'\'
'''

src = open(P, encoding="utf-8").read()
m = re.search(r"PREFS = '''.*?'''\n", src, re.S)
if not m:
    raise SystemExit("PREFS block not found")
src = src[:m.start()] + NEW + src[m.end():]
open(P, "w", encoding="utf-8", newline="\n").write(src)
print("PREFS rewritten, old block size:", m.end() - m.start())
