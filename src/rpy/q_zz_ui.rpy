# -*- coding: utf-8 -*-

# 中文 UI 原生屏幕（自动生成：设置/确认框/Tips列表/附加菜单/弹窗）




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
        text "调整语音与文本的匹配程度：\n0 = PC 原版文本（未删改，部分语音缺失）\n2 = 默认（推荐）\n5 = 主机版文本（全语音，删改较多）" size 19 color "#b8ac93" line_leading 4 xsize 500

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
        textbutton "音乐设置" action ShowMenu("music_change") style "zz_menu_btn_small"



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


screen tips_onik:
    tag menu

    key 'rollback' action NullAction()
    key 'hide_windows' action NullAction()
    key 'game_menu' action NullAction()
    key 'dismiss' action NullAction()

    add "tips/tips_bg.png"

    viewport:
        draggable True
        mousewheel True
        child_size (1280, 740)
        fixed:
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '002':
                textbutton "我们是学年混合?" action [Hide("tips_onik", transition=fade), Jump("onik_tips_01")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 108 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 116
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '002':
                textbutton "我们没有统一的制服?" action [Hide("tips_onik", transition=fade), Jump("onik_tips_02")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 108 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 116
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '003':
                textbutton "前原豪宅" action [Hide("tips_onik", transition=fade), Jump("onik_tips_03")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 170 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 178
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '003':
                textbutton "大坝现场分尸案 (报纸版)" action [Hide("tips_onik", transition=fade), Jump("onik_tips_04")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 170 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 178
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '004':
                textbutton "雏见泽大坝计划" action [Hide("tips_onik", transition=fade), Jump("onik_tips_05")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 232 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 240
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '004':
                textbutton "周刊特别报道" action [Hide("tips_onik", transition=fade), Jump("onik_tips_06")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 232 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 240
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '005':
                textbutton "蕾娜到底叫什么名字?" action [Hide("tips_onik", transition=fade), Jump("onik_tips_07")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 294 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 302
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '009':
                textbutton "传阅板" action [Hide("tips_onik", transition=fade), Jump("onik_tips_08")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 294 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 302
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '010':
                textbutton "北条夫妇坠崖事件" action [Hide("tips_onik", transition=fade), Jump("onik_tips_09")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 356 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 364
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '010':
                textbutton "古手神社神主绝症去世" action [Hide("tips_onik", transition=fade), Jump("onik_tips_10")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 356 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 364
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '010':
                textbutton "家庭主妇被害事件" action [Hide("tips_onik", transition=fade), Jump("onik_tips_11")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 418 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 426
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '010':
                textbutton "无线电记录" action [Hide("tips_onik", transition=fade), Jump("onik_tips_12")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 418 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 426
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '011':
                textbutton "犯罪者超过四人?" action [Hide("tips_onik", transition=fade), Jump("onik_tips_13")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 480 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 488
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '011':
                textbutton "搜查记录" action [Hide("tips_onik", transition=fade), Jump("onik_tips_14")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 480 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 488
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '012':
                textbutton "本部署长公文" action [Hide("tips_onik", transition=fade), Jump("onik_tips_15")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 542 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 550
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '013':
                textbutton "是什么药引发的自杀?" action [Hide("tips_onik", transition=fade), Jump("onik_tips_16")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 542 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 550
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '013':
                textbutton "威胁" action [Hide("tips_onik", transition=fade), Jump("onik_tips_17")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 604 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 612
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '014':
                textbutton "没精神呢" action [Hide("tips_onik", transition=fade), Jump("onik_tips_18")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 604 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 612
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '015':
                textbutton "人格分裂???" action [Hide("tips_onik", transition=fade), Jump("onik_tips_19")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 666 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 674
            if persistent.chapter_onik or filter(lambda x: x.isdigit(), day_result) >= '015':
                textbutton "在 Seventh Mart" action [Hide("tips_onik", transition=fade), Jump("onik_tips_20")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 666 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 674
    textbutton "返回" action If(tips.startswith("mainmenu"), Return(), Show("day_completed", transition=fade)) xpos 1164 ypos 26 style "zz_back_btn"



screen tips_wata:
    tag menu

    key 'rollback' action NullAction()
    key 'hide_windows' action NullAction()
    key 'game_menu' action NullAction()
    key 'dismiss' action NullAction()

    add "tips/tips_bg.png"

    viewport:
        draggable True
        mousewheel True
        child_size (1280, 864)
        fixed:
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '002':
                textbutton "魅音的叔叔是谁?" action [Hide("tips_wata", transition=fade), Jump("wata_tips_01")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 108 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 116
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '003':
                textbutton "真的有诗音这个人吗?" action [Hide("tips_wata", transition=fade), Jump("wata_tips_02")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 108 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 116
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '003':
                textbutton "Angel Mort 介绍报道" action [Hide("tips_wata", transition=fade), Jump("wata_tips_03")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 170 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 178
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '004':
                textbutton "多谢款待" action [Hide("tips_wata", transition=fade), Jump("wata_tips_04")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 170 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 178
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '005':
                textbutton "三人组的始末" action [Hide("tips_wata", transition=fade), Jump("wata_tips_05")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 232 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 240
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '006':
                textbutton "好久不见" action [Hide("tips_wata", transition=fade), Jump("wata_tips_06")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 232 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 240
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '008':
                textbutton "来自剪贴簿其一" action [Hide("tips_wata", transition=fade), Jump("wata_tips_07")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 294 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 302
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '008':
                textbutton "来自剪贴簿其二" action [Hide("tips_wata", transition=fade), Jump("wata_tips_08")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 294 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 302
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '008':
                textbutton "来自剪贴簿其三" action [Hide("tips_wata", transition=fade), Jump("wata_tips_09")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 356 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 364
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '008':
                textbutton "终于要到祭典了" action [Hide("tips_wata", transition=fade), Jump("wata_tips_10")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 356 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 364
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '009':
                textbutton "来自剪贴簿其四" action [Hide("tips_wata", transition=fade), Jump("wata_tips_11")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 418 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 426
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '009':
                textbutton "来自剪贴簿其五" action [Hide("tips_wata", transition=fade), Jump("wata_tips_12")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 418 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 426
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '009':
                textbutton "祭典后半夜" action [Hide("tips_wata", transition=fade), Jump("wata_tips_13")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 480 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 488
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '010':
                textbutton "来自剪贴簿其六" action [Hide("tips_wata", transition=fade), Jump("wata_tips_14")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 480 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 488
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '010':
                textbutton "来自剪贴簿其七" action [Hide("tips_wata", transition=fade), Jump("wata_tips_15")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 542 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 550
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '010':
                textbutton "深夜来电" action [Hide("tips_wata", transition=fade), Jump("wata_tips_16")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 542 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 550
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '011' or day_result == 'wata_010_03':
                textbutton "来自剪贴簿其八" action [Hide("tips_wata", transition=fade), Jump("wata_tips_17")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 604 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 612
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '011' or day_result == 'wata_010_03':
                textbutton "四人的惩罚还没结束吗?" action [Hide("tips_wata", transition=fade), Jump("wata_tips_18")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 604 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 612
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '011':
                textbutton "来自剪贴簿其九" action [Hide("tips_wata", transition=fade), Jump("wata_tips_19")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 666 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 674
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '011':
                textbutton "园崎家的家主是谁?" action [Hide("tips_wata", transition=fade), Jump("wata_tips_20")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 666 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 674
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '011':
                textbutton "来自剪贴簿其十" action [Hide("tips_wata", transition=fade), Jump("wata_tips_21")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 728 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 736
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '011':
                textbutton "请求被拒绝" action [Hide("tips_wata", transition=fade), Jump("wata_tips_22")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 728 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 736
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '012':
                textbutton "来自剪贴簿其十一" action [Hide("tips_wata", transition=fade), Jump("wata_tips_23")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 790 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 798
            if persistent.chapter_wata or filter(lambda x: x.isdigit(), day_result) >= '012':
                textbutton "麻将馆\"铃\"" action [Hide("tips_wata", transition=fade), Jump("wata_tips_24")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 790 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 798
    textbutton "返回" action If(tips.startswith("mainmenu"), Return(), Show("day_completed", transition=fade)) xpos 1164 ypos 26 style "zz_back_btn"



screen tips_tata:
    tag menu

    key 'rollback' action NullAction()
    key 'hide_windows' action NullAction()
    key 'game_menu' action NullAction()
    key 'dismiss' action NullAction()

    add "tips/tips_bg.png"

    viewport:
        draggable True
        mousewheel True
        child_size (1280, 740)
        fixed:
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '002':
                textbutton "沙都子的陷阱讲座 (初级)" action [Hide("tips_tata", transition=fade), Jump("tata_tips_01")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 108 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 116
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '003':
                textbutton "沙都子的陷阱讲座 (中级)" action [Hide("tips_tata", transition=fade), Jump("tata_tips_02")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 108 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 116
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '004':
                textbutton "沙都子的陷阱讲座 (高级)" action [Hide("tips_tata", transition=fade), Jump("tata_tips_03")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 170 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 178
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '005':
                textbutton "幽灵经理" action [Hide("tips_tata", transition=fade), Jump("tata_tips_04")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 170 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 178
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '005':
                textbutton "初步验尸报告副本" action [Hide("tips_tata", transition=fade), Jump("tata_tips_05")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 232 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 240
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '005':
                textbutton "东三局" action [Hide("tips_tata", transition=fade), Jump("tata_tips_06")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 232 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 240
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '008':
                textbutton "研究记录其一" action [Hide("tips_tata", transition=fade), Jump("tata_tips_07")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 294 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 302
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '008':
                textbutton "大石座位上的便条" action [Hide("tips_tata", transition=fade), Jump("tata_tips_08")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 294 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 302
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '009' or day_result == 'tata_008_02':
                textbutton "31 号案件" action [Hide("tips_tata", transition=fade), Jump("tata_tips_09")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 356 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 364
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '009':
                textbutton "条文" action [Hide("tips_tata", transition=fade), Jump("tata_tips_10")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 356 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 364
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '009':
                textbutton "厚生省的统计" action [Hide("tips_tata", transition=fade), Jump("tata_tips_11")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 418 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 426
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '010':
                textbutton "突发事件" action [Hide("tips_tata", transition=fade), Jump("tata_tips_12")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 418 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 426
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '010':
                textbutton "D2-3 第44号" action [Hide("tips_tata", transition=fade), Jump("tata_tips_13")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 480 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 488
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '011':
                textbutton "家庭主妇杀害事件责任科公启" action [Hide("tips_tata", transition=fade), Jump("tata_tips_14")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 480 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 488
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '012':
                textbutton "地狱之火" action [Hide("tips_tata", transition=fade), Jump("tata_tips_15")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 542 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 550
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '012':
                textbutton "第五年的牺牲者" action [Hide("tips_tata", transition=fade), Jump("tata_tips_16")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 542 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 550
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '013':
                textbutton "查询申请" action [Hide("tips_tata", transition=fade), Jump("tata_tips_17")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 604 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 612
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '013':
                textbutton "记仇簿" action [Hide("tips_tata", transition=fade), Jump("tata_tips_18")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 604 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 612
            if persistent.chapter_tata or filter(lambda x: x.isdigit(), day_result) >= '014':
                textbutton "研究记录其二" action [Hide("tips_tata", transition=fade), Jump("tata_tips_19")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 666 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 674
    textbutton "返回" action If(tips.startswith("mainmenu"), Return(), Show("day_completed", transition=fade)) xpos 1164 ypos 26 style "zz_back_btn"



screen tips_hima:
    tag menu

    key 'rollback' action NullAction()
    key 'hide_windows' action NullAction()
    key 'game_menu' action NullAction()
    key 'dismiss' action NullAction()

    add "tips/tips_bg.png"

    viewport:
        draggable True
        mousewheel True
        child_size (1280, 720)
        fixed:
            if persistent.chapter_hima or filter(lambda x: x.isdigit(), day_result) >= '002':
                textbutton "与雪绘的通话" action [Hide("tips_hima", transition=fade), Jump("hima_tips_01")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 108 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 116
            if persistent.chapter_hima or filter(lambda x: x.isdigit(), day_result) >= '002':
                textbutton "宴会致辞稿" action [Hide("tips_hima", transition=fade), Jump("hima_tips_02")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 108 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 116
            if persistent.chapter_hima or filter(lambda x: x.isdigit(), day_result) >= '002':
                textbutton "齿轮、火灾与蜂蜜的味道" action [Hide("tips_hima", transition=fade), Jump("hima_tips_03")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 170 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 178
            if persistent.chapter_hima or filter(lambda x: x.isdigit(), day_result) >= '002':
                textbutton "行李箱里的小鸡" action [Hide("tips_hima", transition=fade), Jump("hima_tips_04")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 170 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 178
            if persistent.chapter_hima or filter(lambda x: x.isdigit(), day_result) >= '003' or day_result == 'hima_002_03':
                textbutton "进展顺利" action [Hide("tips_hima", transition=fade), Jump("hima_tips_05")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 232 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 240
            if persistent.chapter_hima or filter(lambda x: x.isdigit(), day_result) >= '003' or day_result == 'hima_002_03':
                textbutton "恋上雨云" action [Hide("tips_hima", transition=fade), Jump("hima_tips_06")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 232 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 240
            if persistent.chapter_hima or filter(lambda x: x.isdigit(), day_result) >= '003' or day_result == 'hima_002_03':
                textbutton "麦茶、红茶与石臼" action [Hide("tips_hima", transition=fade), Jump("hima_tips_07")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 294 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 302
            if persistent.chapter_hima or filter(lambda x: x.isdigit(), day_result) >= '003':
                textbutton "暗礁的调查" action [Hide("tips_hima", transition=fade), Jump("hima_tips_08")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 294 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 302
            if persistent.chapter_hima or filter(lambda x: x.isdigit(), day_result) >= '003':
                textbutton "选箱子游戏" action [Hide("tips_hima", transition=fade), Jump("hima_tips_09")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 356 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 364
            if persistent.chapter_hima or filter(lambda x: x.isdigit(), day_result) >= '003':
                textbutton "魔鬼也动情" action [Hide("tips_hima", transition=fade), Jump("hima_tips_10")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 356 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 364
            if persistent.chapter_hima or filter(lambda x: x.isdigit(), day_result) >= '004' or day_result == 'hima_003_04':
                textbutton "非常温柔的人" action [Hide("tips_hima", transition=fade), Jump("hima_tips_11")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 418 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 426
            if persistent.chapter_hima or filter(lambda x: x.isdigit(), day_result) >= '004':
                textbutton "母亲的日记其一" action [Hide("tips_hima", transition=fade), Jump("hima_tips_12")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 418 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 426
            if persistent.chapter_hima or filter(lambda x: x.isdigit(), day_result) >= '004':
                textbutton "母亲的日记其二" action [Hide("tips_hima", transition=fade), Jump("hima_tips_13")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 480 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 488
            if persistent.chapter_hima or filter(lambda x: x.isdigit(), day_result) >= '004':
                textbutton "母亲的日记其三" action [Hide("tips_hima", transition=fade), Jump("hima_tips_14")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 480 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 488
    textbutton "返回" action If(tips.startswith("mainmenu"), Return(), Show("day_completed", transition=fade)) xpos 1164 ypos 26 style "zz_back_btn"



screen extra_main:
    tag menu

    add "efe/black.jpg" alpha 0.75

    vbox:
        xalign 0.5
        yalign 0.42
        spacing 22

        if persistent.chapter >= 1:
            textbutton "全员感谢会" action Show('omake_cast', transition=fade) style "zz_menu_btn"
        textbutton "附加房间" action Show('omake_rooms', transition=fade) style "zz_menu_btn"
        if not persistent.chapter == 4:
            textbutton "解锁全部章节" action Show('omake_unlock', transition=fade) style "zz_menu_btn"
        textbutton "退出" action Return() style "zz_menu_btn"

    on "show" action Play('music', persistent.msys05, loop=True, fadeout=1.0, if_changed=True)
    on "replace" action Play('music', persistent.msys05, loop=True, fadeout=1.0, if_changed=True)



screen omake_rooms:
    tag menu

    add "efe/black.jpg" alpha 0.75

    vbox:
        xalign 0.5
        yalign 0.42
        spacing 22

        textbutton "小知识" action Show('tips_main', transition=fade) style "zz_menu_btn"
        textbutton "CG 画廊" action Show('cg_gallery_1', transition=fade) style "zz_menu_btn"
        textbutton "返回" action Show('extra_main', transition=fade) style "zz_menu_btn"

    on "show" action Play('music', persistent.msys05, loop=True, fadeout=1.0, if_changed=True)
    on "replace" action Play('music', persistent.msys05, loop=True, fadeout=1.0, if_changed=True)



screen omake_unlock:
    tag menu

    add "efe/black.jpg" alpha 0.75

    vbox:
        xalign 0.5
        yalign 0.42
        spacing 22

        if not persistent.chapter_onik:
            textbutton "解锁 鬼隐篇" action [Hide('omake_unlock'), Jump('unlock_onik')] style "zz_menu_btn"
        if not persistent.chapter_wata:
            textbutton "解锁 绵流篇" action [Hide('omake_unlock'), Jump('unlock_wata')] style "zz_menu_btn"
        if not persistent.chapter_tata:
            textbutton "解锁 祟杀篇" action [Hide('omake_unlock'), Jump('unlock_tata')] style "zz_menu_btn"
        if not persistent.chapter_hima:
            textbutton "解锁 暇溃篇" action [Hide('omake_unlock'), Jump('unlock_hima')] style "zz_menu_btn"
        textbutton "返回" action Show('extra_main', transition=fade) style "zz_menu_btn"

    on "show" action Play('music', persistent.msys05, loop=True, fadeout=1.0, if_changed=True)
    on "replace" action Play('music', persistent.msys05, loop=True, fadeout=1.0, if_changed=True)



screen omake_cast:
    tag menu

    add "efe/black.jpg" alpha 0.75

    vbox:
        xalign 0.5
        yalign 0.42
        spacing 22

        if persistent.chapter_onik:
            textbutton "鬼隐篇" action Start('onikakushi_omake') style "zz_menu_btn"
        if persistent.chapter_wata:
            textbutton "绵流篇" action Start('watanagashi_omake') style "zz_menu_btn"
        if persistent.chapter_tata:
            textbutton "祟杀篇" action Start('tatarigoroshi_omake') style "zz_menu_btn"
        if persistent.chapter_hima:
            textbutton "暇溃篇" action Start('himatsubushi_omake') style "zz_menu_btn"
        textbutton "返回" action Show('extra_main', transition=fade) style "zz_menu_btn"

    on "show" action Play('music', persistent.msys05, loop=True, fadeout=1.0, if_changed=True)
    on "replace" action Play('music', persistent.msys05, loop=True, fadeout=1.0, if_changed=True)



screen tips_main:
    tag menu

    add "efe/black.jpg" alpha 0.75

    vbox:
        xalign 0.5
        yalign 0.42
        spacing 22

        if persistent.chapter_onik:
            textbutton "鬼隐篇" action [Hide('tips_main', transition=fade), SetVariable('tips', 'mainmenu_onik'), Start('tips_context')] style "zz_menu_btn"
        if persistent.chapter_wata:
            textbutton "绵流篇" action [Hide('tips_main', transition=fade), SetVariable('tips', 'mainmenu_wata'), Start('tips_context')] style "zz_menu_btn"
        if persistent.chapter_tata:
            textbutton "祟杀篇" action [Hide('tips_main', transition=fade), SetVariable('tips', 'mainmenu_tata'), Start('tips_context')] style "zz_menu_btn"
        if persistent.chapter_hima:
            textbutton "暇溃篇" action [Hide('tips_main', transition=fade), SetVariable('tips', 'mainmenu_hima'), Start('tips_context')] style "zz_menu_btn"
        textbutton "返回" action Show('omake_rooms', transition=fade) style "zz_menu_btn"

    on "show" action Play('music', persistent.msys05, loop=True, fadeout=1.0, if_changed=True)
    on "replace" action Play('music', persistent.msys05, loop=True, fadeout=1.0, if_changed=True)



transform zz_tip_pos(yp):
    ypos yp
    xalign 0.5

init 25 python:
    def _zz_tip_card(titles):
        parts = [Image('efe/zz_tips_card.png')]
        y = 350
        for t in titles:
            parts.append(At(Text(t, size=34, color='#f5eede', outlines=[(1, '#000', 1, 1)], font='NotoSansCJKsc-Bold.otf'), zz_tip_pos(y)))
            y += 70
        return Fixed(*parts)

    renpy.image("tips_onik001", _zz_tip_card(["我们是学年混合?", "我们没有统一的制服?"]))
    renpy.image("tips_onik002", _zz_tip_card(["前原豪宅", "大坝现场分尸案 (报纸版)"]))
    renpy.image("tips_onik003", _zz_tip_card(["雏见泽大坝计划", "周刊特别报道"]))
    renpy.image("tips_onik004", _zz_tip_card(["蕾娜到底叫什么名字?"]))
    renpy.image("tips_onik005", _zz_tip_card(["传阅板"]))
    renpy.image("tips_onik009_02", _zz_tip_card(["本部署长公文"]))
    renpy.image("tips_onik010", _zz_tip_card(["是什么药引发的自杀?", "威胁"]))
    renpy.image("tips_onik011", _zz_tip_card(["没精神呢"]))
    renpy.image("tips_onik013", _zz_tip_card(["人格分裂???", "在 Seventh Mart"]))
    renpy.image("tips_wata001", _zz_tip_card(["魅音的叔叔是谁?"]))
    renpy.image("tips_wata002", _zz_tip_card(["真的有诗音这个人吗?", "Angel Mort 介绍报道"]))
    renpy.image("tips_wata003", _zz_tip_card(["多谢款待"]))
    renpy.image("tips_wata004", _zz_tip_card(["三人组的始末"]))
    renpy.image("tips_wata005", _zz_tip_card(["好久不见"]))
    renpy.image("tips_wata007", _zz_tip_card(["来自剪贴簿其一", "来自剪贴簿其二", "来自剪贴簿其三", "终于要到祭典了"]))
    renpy.image("tips_wata008", _zz_tip_card(["来自剪贴簿其四", "来自剪贴簿其五", "祭典后半夜"]))
    renpy.image("tips_wata010_02", _zz_tip_card(["来自剪贴簿其六", "来自剪贴簿其七", "深夜来电"]))
    renpy.image("tips_wata010_04", _zz_tip_card(["来自剪贴簿其六", "来自剪贴簿其七", "深夜来电"]))
    renpy.image("tips_tata001", _zz_tip_card(["沙都子的陷阱讲座 (初级)"]))
    renpy.image("tips_tata002", _zz_tip_card(["沙都子的陷阱讲座 (中级)"]))
    renpy.image("tips_tata003", _zz_tip_card(["沙都子的陷阱讲座 (高级)"]))
    renpy.image("tips_tata004", _zz_tip_card(["幽灵经理", "初步验尸报告副本", "东三局"]))
    renpy.image("tips_tata005", _zz_tip_card(["研究记录其一", "大石座位上的便条"]))
    renpy.image("tips_tata008", _zz_tip_card(["条文", "厚生省的统计"]))
    renpy.image("tips_tata011_03", _zz_tip_card(["突发事件", "D2-3 第44号"]))
    renpy.image("tips_tata013_02", _zz_tip_card(["家庭主妇杀害事件责任科公启"]))
    renpy.image("tips_hima001", _zz_tip_card(["与雪绘的通话", "宴会致辞稿", "齿轮、火灾与蜂蜜的味道", "行李箱里的小鸡"]))
    renpy.image("tips_hima003_03", _zz_tip_card(["进展顺利", "恋上雨云", "麦茶、红茶与石臼"]))
    renpy.image("tips_hima003_05", _zz_tip_card(["进展顺利", "恋上雨云", "麦茶、红茶与石臼"]))

translate schinese strings:

    old "onik_000"

    new "鬼隐篇 序章"

    old "onik_001"

    new "鬼隐篇 第1天"

    old "onik_002"

    new "鬼隐篇 第2天"

    old "onik_003"

    new "鬼隐篇 第3天"

    old "onik_004"

    new "鬼隐篇 第4天"

    old "onik_005"

    new "鬼隐篇 第5天"

    old "onik_009"

    new "鬼隐篇 第9天"

    old "onik_009_02"

    new "鬼隐篇 第9天 祭典后的夜晚"

    old "onik_010"

    new "鬼隐篇 第10天"

    old "onik_011"

    new "鬼隐篇 第11天"

    old "onik_012"

    new "鬼隐篇 第12天"

    old "onik_013"

    new "鬼隐篇 第13天"

    old "onik_014"

    new "鬼隐篇 第14天"

    old "onik_014_02"

    new "鬼隐篇 第14天 傍晚"

    old "onik_015"

    new "鬼隐篇 第15天"

    old "onik_015_02"

    new "鬼隐篇 第15天"

    old "onik_015_03"

    new "鬼隐篇 END"

    old "onik_op"

    new "序章"

    old "onikakushi_omake"

    new "全员感谢会 鬼隐篇"

    old "wata_001"

    new "绵流篇 第1天"

    old "wata_002"

    new "绵流篇 第2天"

    old "wata_003"

    new "绵流篇 第3天"

    old "wata_004"

    new "绵流篇 第4天"

    old "wata_005"

    new "绵流篇 第5天"

    old "wata_006"

    new "绵流篇 第6天"

    old "wata_007"

    new "绵流篇 第7天"

    old "wata_008"

    new "绵流篇 第8天"

    old "wata_009"

    new "绵流篇 第9天"

    old "wata_009_02"

    new "绵流篇 第9天 evening call"

    old "wata_010"

    new "绵流篇 第10天"

    old "wata_010_02"

    new "绵流篇 第10天 call from Shion"

    old "wata_010_03"

    new "绵流篇 第10天 Rika-chan's safety"

    old "wata_010_04"

    new "绵流篇 第10天 about the Three Families"

    old "wata_011"

    new "绵流篇 第11天"

    old "wata_011_02"

    new "绵流篇 第11天·其二"

    old "wata_012"

    new "绵流篇 第12天"

    old "wata_012_02"

    new "绵流篇 第12天 Sonozaki main house"

    old "wata_012_03"

    new "绵流篇 第12天 torture"

    old "wata_ep_01"

    new "绵流篇 尾声"

    old "wata_ep_02"

    new "绵流篇 尾声·THE END"

    old "watanagashi_omake"

    new "全员感谢会 绵流篇"

    old "tata_001"

    new "祟杀篇 序章"

    old "tata_002"

    new "祟杀篇 第2天"

    old "tata_003"

    new "祟杀篇 第3天"

    old "tata_004"

    new "祟杀篇 第4天"

    old "tata_005"

    new "祟杀篇 第5天"

    old "tata_008"

    new "祟杀篇 第8天"

    old "tata_008_02"

    new "祟杀篇 第8天 evening"

    old "tata_009"

    new "祟杀篇 第9天"

    old "tata_009_02"

    new "祟杀篇 第9天 a plea to Mion"

    old "tata_010"

    new "祟杀篇 第10天"

    old "tata_010_02"

    new "祟杀篇 第10天 崩溃"

    old "tata_010_03"

    new "祟杀篇 第10天 完美的犯罪"

    old "tata_010_04"

    new "祟杀篇 第10天 calling Mion"

    old "tata_011"

    new "祟杀篇 第11天 my own path"

    old "tata_011_02"

    new "祟杀篇 第11天 cold blood"

    old "tata_011_03"

    new "祟杀篇 第11天 burying the body"

    old "tata_012"

    new "祟杀篇 第12天 he's alive?"

    old "tata_013"

    new "祟杀篇 第13天 Satoko's house"

    old "tata_013_02"

    new "祟杀篇 第13天"

    old "tata_014"

    new "祟杀篇 第14天 END"

    old "tata_ep01"

    new "祟杀篇 尾声"

    old "tata_ep02"

    new "祟杀篇 尾声·磁带"

    old "tatarigoroshi_omake"

    new "全员感谢会 祟杀篇"

    old "hima_001"

    new "暇溃篇 序章"

    old "hima_002"

    new "暇溃篇 第2天 与梨花会面"

    old "hima_002_02"

    new "暇溃篇 第2天 返回东京"

    old "hima_002_03"

    new "暇溃篇 第2天 例行报告"

    old "hima_003"

    new "暇溃篇 第3天 发现"

    old "hima_003_02"

    new "暇溃篇 第3天 前往雏见泽"

    old "hima_003_03"

    new "暇溃篇 第3天 救出作战"

    old "hima_003_04"

    new "暇溃篇 第3天 深夜再会"

    old "hima_003_05"

    new "暇溃篇 第3天 神秘的预言"

    old "hima_004"

    new "暇溃篇 尾声"

    old "hima_badend"

    new "暇溃篇 BAD END"

    old "himatsubushi_omake"

    new "全员感谢会 暇溃篇"

    old "1982"

    new "1982年"

    old "1983"

    new "1983年"

    old "50 Fragments"

    new "50枚碎片"

    old "Against Oryou!"

    new "对抗阿魉！"

    old "Connecting Fragments"

    new "连接碎片"

    old "Conversation with Mion"

    new "与魅音的对话"

    old "Encounter with Satoshi-kun"

    new "与悟史哥的相遇"

    old "Second encounter with Satoshi-kun"

    new "与悟史哥的重逢"

    old "Evening call"

    new "傍晚的来电"

    old "Everything is better than ever"

    new "一切都比以往更好"

    old "From Rika's view"

    new "梨花的视角"

    old "Hinamizawa Fighters"

    new "雏见泽斗士"

    old "Hinamizawa School"

    new "雏见泽学校"

    old "In the town council"

    new "在町内会"

    old "Interrogate in the torture room"

    new "拷问室里的审问"

    old "Keiichi's counterattack"

    new "圭一的反击"

    old "Looking for a solution"

    new "寻找对策"

    old "Midnight of Watanagashi of 1983"

    new "1983年绵流祭之夜"

    old "Morning after Watanagshi"

    new "绵流祭翌日早晨"

    old "Mountain Dogs' turn"

    new "山狗的行动"

    old "Offer to host the auction"

    new "提出主办拍卖会"

    old "Ooishi's disappearance"

    new "大石的失踪"

    old "Ooishi's warning"

    new "大石的警告"

    old "Oyashiro-sama's curse"

    new "御社神大人的祟杀"

    old "Rika and Ooishi"

    new "梨花与大石"

    old "Rika's efforts"

    new "梨花的努力"

    old "Rika's fall off the cliff"

    new "梨花坠崖"

    old "Satoko attending school"

    new "沙都子上学去了"

    old "Shion calls Keiichi"

    new "诗音致电圭一"

    old "Sonozaki Main House"

    new "园崎本家"

    old "Takano's turn"

    new "鹰野的行动"

    old "Talking to Takano and Tomitake"

    new "与鹰野和富竹谈话"

    old "The Onigafuchi Guardians"

    new "鬼渊守护会"

    old "The aunt has died"

    new "叔母死了"

    old "The child consultation center"

    new "儿童相谈所"

    old "The day I die"

    new "我死去的日子"

    old "The disappearance"

    new "消失"

    old "The first morning of freedom"

    new "重获自由的早晨"

    old "The friends came"

    new "伙伴们来了"

    old "The last day"

    new "最后一天"

    old "The meeting"

    new "会面"

    old "The next day at school"

    new "翌日的学校"

    old "The next day..."

    new "第二天……"

    old "The spirit of Hinamizawa"

    new "雏见泽之魂"

    old "The world with the least luck"

    new "最不走运的世界"

    old "They don't have a sense of danger"

    new "她们没有危机感"

    old "Toy store in Okinomiya"

    new "兴宫的玩具店"

    old "Epilogue"

    new "尾声"

    old "Watanagashi"

    new "绵流祭"

    old "Watanagashi of 1982"

    new "1982年的绵流祭"

    old "Watanagashi of 1983"

    new "1983年的绵流祭"

    old "What could have been..."

    new "如果那时……"

    old "With Rena at the bus stop"

    new "与蕾娜在巴士站"
