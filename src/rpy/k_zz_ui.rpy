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
        textbutton "音乐设置" action ShowMenu("music_change_kai") style "zz_menu_btn_small"



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


screen tips_meak:
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
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "002" or day_result == "meakashi_epilogue":
                textbutton "考察笔记的开篇" action [Hide("tips_meak", transition=fade), Jump("meak_tips_01")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 108 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 116
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "004" or day_result == "meakashi_epilogue":
                textbutton "模糊的日记" action [Hide("tips_meak", transition=fade), Jump("meak_tips_02")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 108 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 116
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "006" or day_result == "meakashi_epilogue":
                textbutton "皱巴巴的日记" action [Hide("tips_meak", transition=fade), Jump("meak_tips_03")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 170 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 178
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "008" or day_result == "meakashi_epilogue":
                textbutton "笔记第21页" action [Hide("tips_meak", transition=fade), Jump("meak_tips_04")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 170 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 178
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "008" or day_result == "meakashi_epilogue":
                textbutton "笔记第24页" action [Hide("tips_meak", transition=fade), Jump("meak_tips_05")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 232 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 240
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "010" or day_result == "meakashi_epilogue":
                textbutton "被撕碎的日记" action [Hide("tips_meak", transition=fade), Jump("meak_tips_06")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 232 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 240
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "012" or day_result == "meakashi_epilogue":
                textbutton "笔记第29页" action [Hide("tips_meak", transition=fade), Jump("meak_tips_07")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 294 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 302
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "014" or day_result == "meakashi_epilogue":
                textbutton "笔记第34页" action [Hide("tips_meak", transition=fade), Jump("meak_tips_08")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 294 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 302
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "014" or day_result == "meakashi_epilogue":
                textbutton "笔记第42页" action [Hide("tips_meak", transition=fade), Jump("meak_tips_09")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 356 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 364
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "015" or day_result == "meakashi_epilogue":
                textbutton "笔记第50页" action [Hide("tips_meak", transition=fade), Jump("meak_tips_10")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 356 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 364
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "015" or day_result == "meakashi_epilogue":
                textbutton "笔记第64页" action [Hide("tips_meak", transition=fade), Jump("meak_tips_11")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 418 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 426
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "015" or day_result == "meakashi_epilogue":
                textbutton "笔记第85页" action [Hide("tips_meak", transition=fade), Jump("meak_tips_12")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 418 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 426
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "017" or day_result == "meakashi_epilogue":
                textbutton "笔记第172页" action [Hide("tips_meak", transition=fade), Jump("meak_tips_13")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 480 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 488
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "017" or day_result == "meakashi_epilogue":
                textbutton "笔记第173页" action [Hide("tips_meak", transition=fade), Jump("meak_tips_14")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 480 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 488
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "017" or day_result == "meakashi_epilogue":
                textbutton "笔记第179页" action [Hide("tips_meak", transition=fade), Jump("meak_tips_15")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 542 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 550
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "019" or day_result == "meakashi_epilogue":
                textbutton "笔记第183页" action [Hide("tips_meak", transition=fade), Jump("meak_tips_16")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 542 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 550
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "019" or day_result == "meakashi_epilogue":
                textbutton "笔记第185页" action [Hide("tips_meak", transition=fade), Jump("meak_tips_17")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 604 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 612
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "021" or day_result == "meakashi_epilogue":
                textbutton "笔记第188页" action [Hide("tips_meak", transition=fade), Jump("meak_tips_18")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 604 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 612
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "023" or day_result == "meakashi_epilogue":
                textbutton "笔记第195页" action [Hide("tips_meak", transition=fade), Jump("meak_tips_19")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 666 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 674
            if persistent.chapter_meak or filter(lambda x: x.isdigit(), day_result) >= "023" or day_result == "meakashi_epilogue":
                textbutton "笔记第196页" action [Hide("tips_meak", transition=fade), Jump("meak_tips_20")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 666 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 674
            if persistent.chapter_meak or day_result == "meakashi_epilogue":
                textbutton "笔记第199页" action [Hide("tips_meak", transition=fade), Jump("meak_tips_21")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 728 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 736
            if persistent.chapter_meak:
                textbutton "幸福的日记" action [Hide("tips_meak", transition=fade), Jump("meak_tips_22")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 728 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 736
            if persistent.chapter_meak:
                textbutton "断绝关系" action [Hide("tips_meak", transition=fade), Jump("meak_tips_23")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 790 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 798
    textbutton "返回" action If(tips.startswith("mainmenu"), Return(), Show("day_completed", transition=fade)) xpos 1164 ypos 26 style "zz_back_btn"



screen tips_tumi:
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
            if persistent.chapter_tumi or filter(lambda x: x.isdigit(), day_result) >= "002":
                textbutton "好天气" action [Hide("tips_tumi", transition=fade), Jump("tsum_tips_001")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 108 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 116
            if persistent.chapter_tumi or filter(lambda x: x.isdigit(), day_result) >= "004":
                textbutton "名片" action [Hide("tips_tumi", transition=fade), Jump("tsum_tips_002")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 108 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 116
            if persistent.chapter_tumi or filter(lambda x: x.isdigit(), day_result) >= "006":
                textbutton "我的暑假绘画日记" action [Hide("tips_tumi", transition=fade), Jump("tsum_tips_003")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 170 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 178
            if persistent.chapter_tumi or filter(lambda x: x.isdigit(), day_result) >= "006":
                textbutton "雨云的预感" action [Hide("tips_tumi", transition=fade), Jump("tsum_tips_004")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 170 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 178
            if persistent.chapter_tumi or filter(lambda x: x.isdigit(), day_result) >= "008":
                textbutton "报价单" action [Hide("tips_tumi", transition=fade), Jump("tsum_tips_005")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 232 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 240
            if persistent.chapter_tumi or filter(lambda x: x.isdigit(), day_result) >= "010":
                textbutton "我最爱的红酒" action [Hide("tips_tumi", transition=fade), Jump("tsum_tips_006")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 232 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 240
            if persistent.chapter_tumi or filter(lambda x: x.isdigit(), day_result) >= "012":
                textbutton "营林署的通知" action [Hide("tips_tumi", transition=fade), Jump("tsum_tips_007")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 294 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 302
            if persistent.chapter_tumi or filter(lambda x: x.isdigit(), day_result) >= "014":
                textbutton "午饭外卖清单其一" action [Hide("tips_tumi", transition=fade), Jump("tsum_tips_008")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 294 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 302
            if persistent.chapter_tumi or filter(lambda x: x.isdigit(), day_result) >= "016":
                textbutton "午饭外卖清单其二" action [Hide("tips_tumi", transition=fade), Jump("tsum_tips_009")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 356 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 364
            if persistent.chapter_tumi or filter(lambda x: x.isdigit(), day_result) >= "018":
                textbutton "午饭外卖清单其三" action [Hide("tips_tumi", transition=fade), Jump("tsum_tips_010")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 356 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 364
            if persistent.chapter_tumi or filter(lambda x: x.isdigit(), day_result) >= "020":
                textbutton "\"那帮家伙\"" action [Hide("tips_tumi", transition=fade), Jump("tsum_tips_011")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 418 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 426
            if persistent.chapter_tumi or filter(lambda x: x.isdigit(), day_result) >= "022":
                textbutton "应该是雏见泽" action [Hide("tips_tumi", transition=fade), Jump("tsum_tips_012")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 418 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 426
            if persistent.chapter_tumi or filter(lambda x: x.isdigit(), day_result) >= "024":
                textbutton "前夕" action [Hide("tips_tumi", transition=fade), Jump("tsum_tips_013")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 480 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 488
            if persistent.chapter_tumi:
                textbutton "恶魔的剧本" action [Hide("tips_tumi", transition=fade), Jump("tsum_tips_014")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 480 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 488
    textbutton "返回" action If(tips.startswith("mainmenu"), Return(), Show("day_completed", transition=fade)) xpos 1164 ypos 26 style "zz_back_btn"



screen tips_mina:
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
            if persistent.chapter_mina or filter(lambda x: x.isdigit(), day_result) >= "002":
                textbutton "给我的孙女*代子" action [Hide("tips_mina", transition=fade), Jump("mina_tips_001")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 108 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 116
            if persistent.chapter_mina or filter(lambda x: x.isdigit(), day_result) >= "003":
                textbutton "与御社神大人的美好时光" action [Hide("tips_mina", transition=fade), Jump("mina_tips_002")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 108 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 116
            if persistent.chapter_mina or filter(lambda x: x.isdigit(), day_result) >= "006":
                textbutton "我与我自己" action [Hide("tips_mina", transition=fade), Jump("mina_tips_003")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 170 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 178
            if persistent.chapter_mina or filter(lambda x: x.isdigit(), day_result) >= "009":
                textbutton "飞行旅行前" action [Hide("tips_mina", transition=fade), Jump("mina_tips_004")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 170 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 178
            if persistent.chapter_mina or filter(lambda x: x.isdigit(), day_result) >= "011":
                textbutton "泼冷水" action [Hide("tips_mina", transition=fade), Jump("mina_tips_005")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 232 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 240
            if persistent.chapter_mina or filter(lambda x: x.isdigit(), day_result) >= "013":
                textbutton "接待记录" action [Hide("tips_mina", transition=fade), Jump("mina_tips_006")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 232 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 240
            if persistent.chapter_mina or filter(lambda x: x.isdigit(), day_result) >= "013":
                textbutton "忧郁与存折" action [Hide("tips_mina", transition=fade), Jump("mina_tips_007")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 294 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 302
            if persistent.chapter_mina or filter(lambda x: x.isdigit(), day_result) >= "015":
                textbutton "没有隐情" action [Hide("tips_mina", transition=fade), Jump("mina_tips_008")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 294 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 302
            if persistent.chapter_mina or filter(lambda x: x.isdigit(), day_result) >= "015":
                textbutton "瘟神与复学" action [Hide("tips_mina", transition=fade), Jump("mina_tips_009")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 356 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 364
            if persistent.chapter_mina or filter(lambda x: x.isdigit(), day_result) >= "017":
                textbutton "公务员的思想准备" action [Hide("tips_mina", transition=fade), Jump("mina_tips_010")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 356 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 364
            if persistent.chapter_mina or filter(lambda x: x.isdigit(), day_result) >= "021":
                textbutton "褪色的笔记" action [Hide("tips_mina", transition=fade), Jump("mina_tips_011")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 418 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 426
            if persistent.chapter_mina or filter(lambda x: x.isdigit(), day_result) >= "025":
                textbutton "另一本褪色的笔记" action [Hide("tips_mina", transition=fade), Jump("mina_tips_012")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 666 ypos 418 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 666 ypos 426
            if persistent.chapter_mina:
                textbutton "碎片游戏的结尾" action [Hide("tips_mina", transition=fade), Jump("mina_tips_013")] text_size 24 text_color "#3a2a18" text_hover_color "#8a1a1a" text_selected_color "#8a1a1a" xpos 104 ypos 480 xsize 520 ysize 56 text_align 0.0
            else:
                text "？？？" size 24 color "#a99a85" xpos 104 ypos 488
    textbutton "返回" action If(tips.startswith("mainmenu"), Return(), Show("day_completed", transition=fade)) xpos 1164 ypos 26 style "zz_back_btn"



screen extra_main:
    tag menu

    add "efe/black.jpg" alpha 0.75

    vbox:
        xalign 0.5
        yalign 0.42
        spacing 22

        if persistent.chapter >= 5:
            textbutton "制作组房间" action Show('omake_staff', transition=fade) style "zz_menu_btn"
        textbutton "附加房间" action Show('omake_rooms', transition=fade) style "zz_menu_btn"
        if not persistent.chapter == 8:
            textbutton "解锁全部章节" action Show('omake_unlock', transition=fade) style "zz_menu_btn"
        textbutton "退出" action Return() style "zz_menu_btn"

    on "show" action Play('music', persistent.z2_hig2, loop=True, fadeout=1.0, if_changed=True)
    on "replace" action Play('music', persistent.z2_hig2, loop=True, fadeout=1.0, if_changed=True)



screen omake_rooms:
    tag menu

    add "efe/black.jpg" alpha 0.75

    vbox:
        xalign 0.5
        yalign 0.42
        spacing 22

        textbutton "小知识" action Show("tips_main", transition=fade) style "zz_menu_btn"
        if persistent.graphics_sui:
            textbutton "CG 画廊" action Show("cg_gallery_kai_1", transition=fade) style "zz_menu_btn"
        textbutton "返回" action Show("extra_main", transition=fade) style "zz_menu_btn"

    on "show" action Play("music", persistent.z2_hig2, loop=True, fadeout=1.0, if_changed=True)
    on "replace" action Play("music", persistent.z2_hig2, loop=True, fadeout=1.0, if_changed=True)



screen omake_unlock:
    tag menu

    add "efe/black.jpg" alpha 0.75

    vbox:
        xalign 0.5
        yalign 0.42
        spacing 22

        if not persistent.chapter_meak:
            textbutton "解锁 目明篇" action [Hide("omake_unlock"), Jump("otsukaresama_meakashi")] style "zz_menu_btn"
        if not persistent.chapter_tumi:
            textbutton "解锁 罪灭篇" action [Hide("omake_unlock"), Jump("otsukaresama_tsumihoroboshi")] style "zz_menu_btn"
        if not persistent.chapter_mina:
            textbutton "解锁 皆杀篇" action [Hide("omake_unlock"), Jump("otsukaresama_minagoroshi")] style "zz_menu_btn"
        if not persistent.chapter_matu:
            textbutton "解锁 祭囃篇" action [Hide("omake_unlock"), Jump("otsukaresama_matsuribayashi")] style "zz_menu_btn"
        textbutton "返回" action Show("extra_main", transition=fade) style "zz_menu_btn"

    on "show" action Play("music", persistent.z2_hig2, loop=True, fadeout=1.0, if_changed=True)
    on "replace" action Play("music", persistent.z2_hig2, loop=True, fadeout=1.0, if_changed=True)



screen tips_main:
    tag menu

    add "efe/black.jpg" alpha 0.75

    vbox:
        xalign 0.5
        yalign 0.42
        spacing 22

        if persistent.chapter_meak:
            textbutton "目明篇" action [Hide("tips_main", transition=fade), SetVariable("tips", "mainmenu_meak"), Start("tips_context")] style "zz_menu_btn"
        if persistent.chapter_tumi:
            textbutton "罪灭篇" action [Hide("tips_main", transition=fade), SetVariable("tips", "mainmenu_tumi"), Start("tips_context")] style "zz_menu_btn"
        if persistent.chapter_mina:
            textbutton "皆杀篇" action [Hide("tips_main", transition=fade), SetVariable("tips", "mainmenu_mina"), Start("tips_context")] style "zz_menu_btn"
        if persistent.chapter_matu:
            textbutton "祭囃篇·最终" action [Hide("tips_main", transition=spiral2), SetVariable("start_chapter", "final_tip"), Start("smooth_transition")] style "zz_menu_btn"
        textbutton "返回" action Show("omake_rooms", transition=fade) style "zz_menu_btn"

    on "show" action Play("music", persistent.z2_hig2, loop=True, fadeout=1.0, if_changed=True)
    on "replace" action Play("music", persistent.z2_hig2, loop=True, fadeout=1.0, if_changed=True)



screen omake_staff:
    tag menu

    add "efe/black.jpg" alpha 0.75

    vbox:
        xalign 0.5
        yalign 0.42
        spacing 22

        if persistent.chapter_meak:
            textbutton "目明篇" action Start("staffroom_meakashi") style "zz_menu_btn"
        if persistent.chapter_tumi:
            textbutton "罪灭篇" action Start("staffroom_tsumihoroboshi") style "zz_menu_btn"
        if persistent.chapter_mina:
            textbutton "皆杀篇" action Start("staffroom_minagoroshi") style "zz_menu_btn"
        if persistent.chapter_matu:
            textbutton "祭囃篇" action Start("staffroom_matsuribayashi") style "zz_menu_btn"
        textbutton "返回" action Show("extra_main", transition=fade) style "zz_menu_btn"

    on "show" action Play("music", persistent.z2_hig2, loop=True, fadeout=1.0, if_changed=True)
    on "replace" action Play("music", persistent.z2_hig2, loop=True, fadeout=1.0, if_changed=True)



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

    renpy.image("tips_meak001", _zz_tip_card(["考察笔记的开篇"]))
    renpy.image("tips_meak003", _zz_tip_card(["模糊的日记"]))
    renpy.image("tips_meak005", _zz_tip_card(["皱巴巴的日记"]))
    renpy.image("tips_meak007", _zz_tip_card(["笔记第21页", "笔记第24页"]))
    renpy.image("tips_meak009", _zz_tip_card(["被撕碎的日记"]))
    renpy.image("tips_meak011", _zz_tip_card(["笔记第29页"]))
    renpy.image("tips_meak013", _zz_tip_card(["笔记第34页", "笔记第42页"]))
    renpy.image("tips_meak014", _zz_tip_card(["笔记第50页", "笔记第64页", "笔记第85页"]))
    renpy.image("tips_meak016", _zz_tip_card(["笔记第172页", "笔记第173页", "笔记第179页"]))
    renpy.image("tips_meak018", _zz_tip_card(["笔记第183页", "笔记第185页"]))
    renpy.image("tips_meak020", _zz_tip_card(["笔记第188页"]))
    renpy.image("tips_meak022", _zz_tip_card(["笔记第195页", "笔记第196页"]))
    renpy.image("tips_tsum001", _zz_tip_card(["好天气"]))
    renpy.image("tips_tsum003", _zz_tip_card(["名片"]))
    renpy.image("tips_tsum005", _zz_tip_card(["我的暑假绘画日记", "雨云的预感"]))
    renpy.image("tips_tsum007", _zz_tip_card(["报价单"]))
    renpy.image("tips_tsum009", _zz_tip_card(["我最爱的红酒"]))
    renpy.image("tips_tsum011", _zz_tip_card(["营林署的通知"]))
    renpy.image("tips_tsum013", _zz_tip_card(["午饭外卖清单其一"]))
    renpy.image("tips_tsum015", _zz_tip_card(["午饭外卖清单其二"]))
    renpy.image("tips_tsum017", _zz_tip_card(["午饭外卖清单其三"]))
    renpy.image("tips_tsum019", _zz_tip_card(["\"那帮家伙\""]))
    renpy.image("tips_tsum021", _zz_tip_card(["应该是雏见泽"]))
    renpy.image("tips_tsum023", _zz_tip_card(["前夕"]))
    renpy.image("tips_mina001", _zz_tip_card(["给我的孙女*代子"]))
    renpy.image("tips_mina002", _zz_tip_card(["与御社神大人的美好时光"]))
    renpy.image("tips_mina005", _zz_tip_card(["我与我自己"]))
    renpy.image("tips_mina008", _zz_tip_card(["飞行旅行前"]))
    renpy.image("tips_mina010", _zz_tip_card(["泼冷水"]))
    renpy.image("tips_mina012", _zz_tip_card(["接待记录", "忧郁与存折"]))
    renpy.image("tips_mina014", _zz_tip_card(["没有隐情", "瘟神与复学"]))
    renpy.image("tips_mina016", _zz_tip_card(["公务员的思想准备"]))
    renpy.image("tips_mina020", _zz_tip_card(["褪色的笔记"]))
    renpy.image("tips_mina024", _zz_tip_card(["另一本褪色的笔记"]))

translate schinese strings:

    old "mats_001"

    new "祭囃篇 #1"

    old "mats_002"

    new "祭囃篇 #2"

    old "mats_003"

    new "祭囃篇 #3"

    old "mats_004"

    new "祭囃篇 #4"

    old "mats_005"

    new "祭囃篇 #5"

    old "mats_006"

    new "祭囃篇 #6"

    old "mats_007"

    new "祭囃篇 #7"

    old "mats_008"

    new "祭囃篇 碎片连接。序章"

    old "mats_009"

    new "祭囃篇 #9"

    old "mats_010"

    new "祭囃篇 #10"

    old "mats_011"

    new "祭囃篇 #11"

    old "mats_012"

    new "祭囃篇 #12"

    old "mats_013"

    new "祭囃篇 #13"

    old "mats_014"

    new "祭囃篇 #14"

    old "mats_015"

    new "祭囃篇 #15"

    old "mats_016"

    new "祭囃篇 #16"

    old "mats_017"

    new "祭囃篇 #17"

    old "mats_018"

    new "祭囃篇 #18"

    old "mats_019"

    new "祭囃篇 #19"

    old "mats_020"

    new "祭囃篇 #20"

    old "mats_021"

    new "祭囃篇 #21"

    old "mats_022"

    new "祭囃篇 #22"

    old "mats_023"

    new "祭囃篇 #23"

    old "mats_024"

    new "祭囃篇 #24"

    old "mats_025"

    new "祭囃篇 END"

    old "mats_op"

    new "祭囃篇 序章"

    old "matsuribayashi_kakera_01"

    new "碎片连接。 C103 投药实验"

    old "matsuribayashi_kakera_02"

    new "碎片连接。 入江的过去"

    old "matsuribayashi_kakera_03"

    new "碎片连接。 分售宅地的预告"

    old "matsuribayashi_staffroom"

    new "制作组房间 Matsuribayashi-hen"

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

    old "Prologue"

    new "序章"

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
