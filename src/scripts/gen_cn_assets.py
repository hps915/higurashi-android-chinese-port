# -*- coding: utf-8 -*-
"""Generate Chinese support files for the Ren'Py port project:
  game/zz_cn.rpy               fonts + character names + default language
  game/tl/schinese/zz_common.rpy  GUI/save-name string translations
and copy Noto CJK fonts into game/.
"""
import os
import re
import shutil
import sys

PROJ = (sys.argv[1] if len(sys.argv) > 1 else r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project\game")
FONTS = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\tools"

CHAPTERS = {"Onikakushi": "鬼隐", "Watanagashi": "绵流", "Tatarigoroshi": "祟杀",
            "Himatsubushi": "暇溃", "Meakashi": "目明", "Tsumihoroboshi": "罪灭",
            "Minagoroshi": "皆杀", "Matsuribayashi": "祭囃", "Maturibayashi": "祭囃"}

FRAGMENTS = {
    "A Fragment of Himatsubushi": "暇溃篇的碎片", "A Fragment of Matsuribayashi": "祭囃篇的碎片",
    "A Fragment of Meakashi": "目明篇的碎片", "A Fragment of Minagoroshi": "皆杀篇的碎片",
    "A Fragment of Onikakushi": "鬼隐篇的碎片", "A Fragment of Tatarigoroshi": "祟杀篇的碎片",
    "A Fragment of Tsumihoroboshi": "罪灭篇的碎片", "A Fragment of Watanagashi": "绵流篇的碎片",
    "A local explanatory meeting": "当地的说明会", "A murder with a dismembered body": "分尸杀人事件",
    "A notice of leave of absence": "请假通知", "A red capsule": "红色胶囊",
    "A roll of a one": "掷出一点", "A routine inspection": "例行检查",
    "An invitation to an end": "终结的邀请", "At a quarry in Yagouchi": "在谷河内的采石场",
    "C103 dose experiment": "C103 投药实验", "Dam construction operation withdrawal": "水坝工程撤回",
    "Death of Satoshi's aunt": "悟史叔母之死", "Deja-vu": "似曾相识",
    "Depression of a Shinto priest": "神主的忧郁", "Disappointment": "失望",
    "Distrust of the mother of a queen": "女王母亲的猜疑", "Flags from kids' meals": "儿童套餐的旗子",
    "Footsteps in the fourth year": "第四年的脚步声", "Formation of a club": "社团的结成",
    "H170": "H170", "Irie's background": "入江的过去", "Jirou Tomitake": "富竹次郎",
    "June 1983": "1983年6月", "Keiichi Maebara": "前原圭一", "Kyousuke Irie": "入江京介",
    "Mion Sonozaki": "园崎魅音", "Mysterious death of the Furude couple": "古手夫妇离奇死亡",
    "New wind": "新的风", "One, two, three, four": "一、二、三、四",
    "Preview of lots for sale": "土地预售预告", "Rena Ryuugu": "龙宫蕾娜",
    "Requesting assistance from a queen": "女王的求助", "Rika Furude": "古手梨花",
    "Satoko Houjou": "北条沙都子", "Satoshi Houjou": "北条悟史",
    "Suffering of a big brother": "哥哥的痛苦", "The Houjou siblings": "北条兄妹",
    "The final miracle": "最后的奇迹", "The first sacrifice": "最初的祭品",
    "The fourth sacrifice": "第四年的祭品", "The old guy": "老头子",
}

NAMES = {
    "a_keiichi": "圭一", "a_rena": "蕾娜", "a_mion": "魅音", "a_satoko": "沙都子",
    "a_rika": "梨花", "a_shion": "诗音", "a_satoshi": "悟史", "a_tomitake": "富竹",
    "a_miyo": "鹰野", "a_irie": "入江", "a_oishi": "大石", "a_akasaka": "赤坂",
    "a_kasai": "葛西", "a_oryou": "お魉", "a_kiichiro": "喜一郎", "a_kuma": "熊谷",
    "a_teppei": "铁平", "a_chie": "知惠", "a_kameda": "龟田", "a_tomita": "富田",
    "a_okamura": "冈村", "a_miyuki": "美雪", "a_yukie": "雪绘",
    "a_kimiyoshi": "公由", "a_komiyama": "小宫山", "a_makino": "牧野",
    "a_morikawa": "森川", "a_okuno": "奥野", "a_takasugi": "高杉", "a_fujiwara": "藤原",
    "a_all_boy": "男孩子们", "a_all_girl": "女孩子们", "a_announcer": "播音员",
    "a_boy": "少年", "a_bureau": "局员", "a_club": "部员们",
    "a_club_oldman": "部员与老爷爷", "a_cram_teacher": "补习班老师", "a_crowd": "人群",
    "a_dad": "圭一的父亲", "a_deling": "不良少年", "a_desk": "前台", "a_det": "刑警",
    "a_detectives": "刑警们", "a_doc": "医生", "a_emerge_center": "急救中心",
    "a_f_invest": "鉴证人员", "a_fest_stall": "祭典摊位", "a_fire": "消防本部",
    "a_gallery": "画廊", "a_girl": "少女", "a_group_member": "组员",
    "a_guardian": "监护人", "a_headqrts": "本部", "a_kei_others": "圭一他们",
    "a_man": "男人", "a_master": "老板", "a_men": "男人们", "a_mid_man": "中年男人",
    "a_mom": "圭一的母亲", "a_ngale": "护士", "a_nurse": "护士",
    "a_oki_ps": "兴宫警署", "a_old_person": "老人", "a_oldman": "老爷爷",
    "a_otaku": "御宅族", "a_otakus": "御宅族们", "a_police": "警察",
    "a_principal": "校长", "a_prof": "教授", "a_pupils": "学生们",
    "a_rena_dad": "蕾娜的父亲", "a_report": "记者", "a_s_member": "工作人员",
    "a_senior": "前辈", "a_sklrk": "云雀", "a_so_repres": "园崎家代表",
    "a_teacher": "前台", "a_thug": "歹徒", "a_unkn": "？？？", "a_villager": "村民",
    "a_waitr": "女服务生", "a_watchman": "更夫", "a_woman2": "女人",
}
COMPOSITE = {
    "a_re_mi": "{color=#FF8635}蕾娜{/color}＆{color=#5ec69a}魅音{/color}",
    "a_mi_sa_ri": "{color=#5ec69a}魅音{/color}＆{color=#FFE165}沙都子{/color}＆{color=#6972c1}梨花{/color}",
    "a_kei_rena_satoko": "{color=#956f6e}圭一{/color}＆{color=#FF8635}蕾娜{/color}＆{color=#FFE165}沙都子{/color}",
    "a_kei_tomi_oka": "{color=#956f6e}圭一{/color}＆{color=#a17d6b}富田{/color}＆{color=#7a7e7d}冈村{/color}",
    "a_rika_keiichi": "{color=#6972c1}梨花{/color}＆{color=#956f6e}圭一{/color}",
    "a_satoko_rena": "{color=#FFE165}沙都子{/color}＆{color=#FF8635}蕾娜{/color}",
    "a_tomi_oka": "{color=#a17d6b}富田{/color}＆{color=#7a7e7d}冈村{/color}",
    "a_mion_shion": "{color=#5ec69a}魅音{/color}＆{color=#5ec69a}诗音{/color}",
}

# 解题篇扩展角色（screens.rpy 里的完整名单）
NAMES.update({
    "a_hanyuu": "羽入", "a_rina": "理奈", "a_akane": "茜", "a_yoshiro": "吉朗",
    "a_okonogi": "小此木", "a_shimiko": "志美子", "a_miyoko": "美代子",
    "a_miyo2": "三四", "a_hifumi": "一二三", "a_eriko": "惠理子",
    "a_tomomi": "智美", "a_kikuko": "菊子", "a_koizumi": "小泉", "a_nomura": "野村",
    "a_niimi": "新见", "a_kanou": "加纳", "a_hondaya": "本田屋", "a_nagata": "永田",
    "a_nakagawa": "中川", "a_saitou": "斋藤", "a_aida": "会田", "a_harayama": "原山",
    "a_hibari": "云雀", "a_all": "大家", "a_elder": "长老", "a_elders": "长老们",
    "a_waitrs": "女服务生们", "a_clerk": "职员", "a_subord": "部下",
    "a_sale_per": "销售员", "a_referee": "裁判", "a_customs": "客人们",
    "a_delings": "不良少年们", "a_gardener": "园丁", "a_tel": "电话",
    "a_resident": "住户", "a_so_gang": "园崎组员", "a_gang": "组员",
    "a_forest_officer": "林业署职员", "a_ootaka": "大高", "a_chief": "部长",
    "a_mil_officer": "军官", "a_housewife": "主妇", "a_counselor": "辅导员",
    "a_office_worker": "上班族", "a_kids": "孩子们", "a_chairman": "会长",
    "a_sports": "运动员们", "a_town_council": "镇议员们", "a_mion_dad": "魅音的父亲",
    "a_so_lawer": "园崎家律师", "a_mayor": "镇长", "a_yamainu": "山狗",
    "a_yamainus": "山狗们", "a_gov_secretary": "政府秘书",
    "a_def_director": "防卫厅长官", "a_prime_minister": "首相",
    "a_force_member": "自卫队员", "a_old_woman": "老妇人", "a_punk": "小混混",
    "a_hotel": "旅馆员工", "a_staff": "工作人员", "a_senior_member": "资深成员",
    "a_politician": "政治家", "a_bcrat": "官僚", "a_bcrats": "官僚们",
    "a_landlady": "女房东", "a_homeroom": "班主任", "a_seminar_leader": "研讨会主讲",
    "a_coordinator": "协调员", "a_rika_dad": "梨花的父亲", "a_rika_mom": "梨花的母亲",
    "a_congressman": "国会议员", "a_laborer": "工人", "a_govern_official": "政府官员",
    "a_sa_dad": "沙都子的父亲", "a_woman_villager": "村妇",
    "a_estate_agent": "房产中介", "a_housekeeper": "女佣", "a_vendor": "小贩",
    "a_butcher": "肉铺老板", "a_blman": "黑衣人", "a_woman": "年轻女子",
    "a_guard": "警卫", "a_diplomat": "外交官", "a_disciple": "弟子",
    "a_followers": "信徒们", "a_old_member": "老成员", "a_guests": "客人们",
    "a_officers": "军官们", "a_public_safety": "公安人员", "a_bloodhound": "猎犬",
    "a_attendant_policeman": "随行警察", "a_hotel_receptionist": "旅馆前台",
    "a_miyoko_dad": "美代子的父亲", "a_oka": "冈", "a_f_invest": "鉴证人员",
})
# 编号代号（夜莺/凤凰/云雀/苍鹭 小队）
for _i in list(range(1, 14)):
    NAMES[f"a_ngale{_i}"] = f"夜莺{_i}"
for _i in [2, 3, 4, 5, 7, 9, 10, 18]:
    NAMES[f"a_phx{_i}"] = f"凤凰{_i}"
for _i in [1, 2, 4, 10, 11, 12, 13, 16]:
    NAMES[f"a_sklrk{_i}"] = f"云雀{_i}"
for _i in [1, 2, 3, 4, 5, 7, 8, 10, 19, 20, 21, 22, 23]:
    NAMES[f"a_heron{_i}"] = f"苍鹭{_i}"

COMPOSITE.update({
    "a_kei_rena": "{color=#956f6e}圭一{/color}＆{color=#FF8635}蕾娜{/color}",
    "a_mion_rika_shion": "{color=#5ec69a}魅音{/color}＆{color=#6972c1}梨花{/color}＆{color=#5ec69a}诗音{/color}",
    "a_kei_mion_rika_shion": "{color=#956f6e}圭一{/color}＆{color=#5ec69a}魅音{/color}＆{color=#6972c1}梨花{/color}＆{color=#5ec69a}诗音{/color}",
    "a_tomi_miyo": "{color=#945c44}富竹{/color}＆{color=f6d9a8}鹰野{/color}",
    "a_miyo_irie": "{color=f6d9a8}鹰野{/color}＆{color=#DBBC9E}入江{/color}",
    "a_irie_tomi_miyo": "{color=#DBBC9E}入江{/color}＆{color=#945c44}富竹{/color}＆{color=f6d9a8}鹰野{/color}",
    "a_kei_mion_rena": "{color=#956f6e}圭一{/color}＆{color=#5ec69a}魅音{/color}＆{color=#FF8635}蕾娜{/color}",
    "a_rena_mion_shion": "{color=#FF8635}蕾娜{/color}＆{color=#5ec69a}魅音{/color}＆{color=#5ec69a}诗音{/color}",
    "a_kei_rena_okamura": "{color=#956f6e}圭一{/color}＆{color=#FF8635}蕾娜{/color}＆{color=#7a7e7d}冈村{/color}",
    "a_mion_kei_satoko": "{color=#5ec69a}魅音{/color}＆{color=#956f6e}圭一{/color}＆{color=#FFE165}沙都子{/color}",
    "a_tomi_irie": "{color=#945c44}富竹{/color}＆{color=#DBBC9E}入江{/color}",
    "a_hifumi_koizumi": "一二三＆小泉",
})

UI_STRINGS = {
    "Use": "使用", "Don't use": "不使用", "Exit": "退出",
    "Next page": "下一页", "Previous page": "上一页", "TIPS Menu": "TIPS 菜单",
    "Hello!": "你好！", "Original": "原版", "Sui": "奉",
    "Original+Sui\\n(Recommended)": "原版+奉\\n（推荐）",
    "Disable opening": "禁用开场动画", "Enable opening": "启用开场动画",
    "Club mode": "社团模式", "School Mode": "学校模式",
    "Dark theme": "黑暗主题", "Scary theme": "恐怖主题", "Funny stuff": "搞笑",
    "Peaceful evenings": "平和的夜晚", "Daily life": "日常", "Tour": "巡视",
    "Meditation": "冥想", "Meditation1": "冥想1", "Silence": "静寂",
    "Gear": "机关", "Loss": "丧失", "Disaster": "灾难", "Torture": "拷问",
    "Breakdown": "崩溃", "Confession on the bridge": "桥上的告白",
    "Kneecap": "膝盖", "Tell a Thing": "说件事", "The Twins": "双子",
    "Lunch Time": "午餐时间", "Small Town": "小镇", "Spring Step": "春之步伐",
    "Spinning Seesaw": "旋转的跷跷板", "Charming": "魅惑", "Cold blood": "冷血",
    "Fascism": "法西斯主义", "DEAD END Symphony": "DEAD END 交响曲",
    # 章节选择界面的裸章节名
    "Onikakushi-hen": "鬼隐篇", "Watanagashi-hen": "绵流篇",
    "Tatarigoroshi-hen": "祟杀篇", "Himatsubushi-hen": "暇溃篇",
    "Meakashi-hen": "目明篇", "Tsumihoroboshi-hen": "罪灭篇",
    "Minagoroshi-hen": "皆杀篇", "Matsuribayashi-hen": "祭囃篇",
    "Maturibayashi-hen": "祭囃篇",
    # Ren'Py common UI
    "Are you sure?": "确定吗？",
    "Are you sure you want to quit?": "确定要退出吗？",
    "Are you sure you want to return to the main menu?": "确定要返回主菜单吗？",
    "This will let you return to the main menu. Any unsaved progress will be lost.": "这将返回主菜单，未保存的进度将会丢失。",
    "Save": "保存", "Load": "读取", "Main Menu": "主菜单", "Return": "返回",
    "Preferences": "设置", "Quit": "退出", "Start": "开始", "empty": "空",
    "Yes": "是", "No": "否", "Auto": "自动", "Skip": "跳过",
}

SPECIAL_SAVE = {
    "Prolouge.": "序章", "Prologue": "序章", "Epilogue": "尾声",
    "END": "END", "BADEND": "BAD END",
    "Day 15, I'm sorry": "第15天 对不起",
    "Day 9, night after the festival": "第9天 祭典后的夜晚",
    "Day 9, the punishment": "第9天 惩罚",
    "Day 14, evening": "第14天 傍晚",
    "Day 2, go back to Tokyo": "第2天 返回东京",
    "Day 2, informant": "第2天 情报贩子",
    "Day 2, meeting with Rika": "第2天 与梨花会面",
    "Day 2, regular report": "第2天 例行报告",
    "Day 3, a discovery": "第3天 发现",
    "Day 3, midnight reunion": "第3天 深夜再会",
    "Day 3, mysterious prophecy": "第3天 神秘的预言",
    "Day 3, rescue mission": "第3天 救出作战",
    "Day 3, to Hinamizawa": "第3天 前往雏见泽",
    "Day 10, a perfect crime": "第10天 完美的犯罪",
    "Day 10, breakdown": "第10天 崩溃",
    "Day 12, counterattack": "第12天 反击",
    "Day 13, the last tag": "第13天 最后的捉迷藏",
    "Day 14, the man who became a god": "第14天 成为神的男人",
    "Day 15, a congress of queens": "第15天 女王们的会议",
    "Day 16, the morning of the decisive battle": "第16天 决战之朝",
    "Day 17, the clash": "第17天 对决",
    "Day 18, aftermath": "第18天 尾声",
    "Day 3, the watcher": "第3天 窥视者",
    "Day 9, request": "第9天 请求",
    "Day 4, curiosity": "第4天 好奇心",
    "Day 8, a trap": "第8天 陷阱",
    "Day 5, sneaking": "第5天 潜入",
    "Day 6, the man who knows": "第6天 知情者",
    "Day 7, the plan": "第7天 计划",
    "Day 2, late night": "第2天 深夜",
}


def collect_save_names():
    """All __('...') save-name strings from project .rpy files."""
    strings = set()
    pat = re.compile(r'__\("((?:[^"\\]|\\.)*)"\)')
    for root, dirs, files in os.walk(PROJ):
        for f in files:
            if f.endswith(".rpy"):
                txt = open(os.path.join(root, f), encoding="utf-8").read()
                for m in pat.finditer(txt):
                    strings.add(m.group(1))
    return sorted(strings)


def translate_save_name(s):
    # formats: "Chapter-hen.\nRest" or bare "Prologue"
    parts = s.split("\\n")
    ch_part = parts[0]
    rest = parts[1] if len(parts) > 1 else None
    m = re.match(r"(\w+)-hen\.$", ch_part)
    zh_ch = None
    if m and m.group(1) in CHAPTERS:
        zh_ch = CHAPTERS[m.group(1)] + "篇"
    elif "All-cast Review Session" in ch_part:
        zh_ch = "全员座谈会"
    elif ch_part == "Connecting Fragments.":
        if rest and rest in FRAGMENTS:
            return "碎片连接\\n" + FRAGMENTS[rest]
        return "碎片连接\\n" + (rest or "")
    elif ch_part == "Staff Room.":
        m3 = re.match(r"(\w+)-hen$", rest or "")
        if m3 and m3.group(1) in CHAPTERS:
            return "Staff Room\\n" + CHAPTERS[m3.group(1)] + "篇"
        return "Staff Room\\n" + (rest or "")
    if rest is None:
        return SPECIAL_SAVE.get(s)
    zh_rest = SPECIAL_SAVE.get(rest)
    if zh_rest is None:
        m2 = re.match(r"Day (\d+)$", rest)
        if m2:
            zh_rest = f"第{int(m2.group(1))}天"
        else:
            zh_rest = rest
    if zh_ch is None:
        return None
    return zh_ch + "\\n" + zh_rest


def main():
    # 1. fonts
    for f in ("NotoSansCJKsc-Regular.otf", "NotoSansCJKsc-Bold.otf"):
        shutil.copy2(os.path.join(FONTS, f), os.path.join(PROJ, f))

    # 2. zz_cn.rpy
    names_code = "\n".join(f'    "{k}": u"{v}",' for k, v in sorted(NAMES.items()))
    comp_code = "\n".join(f'    "{k}": u"{v}",' for k, v in sorted(COMPOSITE.items()))
    zz = f'''# -*- coding: utf-8 -*-
# 中文支持：字体接管 + 角色名 + 默认语言（由移植管线自动生成）
init 999 python:

    config.language = "schinese"

    style.default.font = "NotoSansCJKsc-Regular.otf"

    for _f in ("Consola.ttf", "ConsolaB.ttf", "ConsolaI.ttf", "ConsolaZ.ttf",
               "CourierNew.ttf", "CourierNewB.ttf", "CourierNewI.ttf", "CourierNewZ.ttf",
               "Times.ttf", "DejaVuSans.ttf", "Sazanami.ttf"):
        config.font_replacement_map[(_f, False, False)] = ("NotoSansCJKsc-Regular.otf", False, False)
        config.font_replacement_map[(_f, True, False)] = ("NotoSansCJKsc-Bold.otf", False, False)
        config.font_replacement_map[(_f, False, True)] = ("NotoSansCJKsc-Regular.otf", False, False)
        config.font_replacement_map[(_f, True, True)] = ("NotoSansCJKsc-Bold.otf", False, False)

    _cn_names = {{
{names_code}
{comp_code}
    }}
    for _tag, _nm in _cn_names.items():
        _c = globals().get(_tag)
        if _c is not None:
            try:
                _c.name = _nm
            except Exception:
                pass

    def _zz_cn_apply():
        for _tag, _nm in _cn_names.items():
            _c = globals().get(_tag)
            if _c is not None:
                try:
                    _c.name = _nm
                except Exception:
                    pass

    # 解题篇会在运行时反复重建角色（mode_change），每次重建后重新应用中文名
    if 'mode_change' in globals():
        _zz_orig_mode_change = mode_change

        def mode_change(*args, **kwargs):
            _zz_orig_mode_change(*args, **kwargs)
            _zz_cn_apply()
'''
    with open(os.path.join(PROJ, "zz_cn.rpy"), "w", encoding="utf-8", newline="\n") as f:
        f.write(zz)

    # 3. tl/schinese/zz_common.rpy
    entries = dict(UI_STRINGS)
    untranslated = []
    for s in collect_save_names():
        zh = translate_save_name(s)
        if zh is None:
            untranslated.append(s)
        else:
            entries[s] = zh
    # day labels used by scenario jump screens
    for d in range(1, 40):
        entries[f"Day {d}"] = f"第{d}天"
    tl_dir = os.path.join(PROJ, "tl", "schinese")
    os.makedirs(tl_dir, exist_ok=True)
    lines = ["# -*- coding: utf-8 -*-",
             "# 界面与存档名字符串翻译（自动生成）", "translate schinese strings:"]
    for old, new in sorted(entries.items()):
        lines.append(f'    old "{old}"')
        lines.append(f'    new "{new}"')
    with open(os.path.join(tl_dir, "zz_common.rpy"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(f"zz_cn.rpy + tl/schinese/zz_common.rpy written ({len(entries)} strings)")
    if untranslated:
        print("UNTRANSLATED save names:")
        for s in untranslated:
            print("   ", s)


if __name__ == "__main__":
    main()
