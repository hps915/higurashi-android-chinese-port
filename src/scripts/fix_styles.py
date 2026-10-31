# -*- coding: utf-8 -*-
"""Repair gen_zz_ui.py after the botched regex surgery: every
style "<chr(1)>" placeholder gets its correct style name back,
inferred from line context."""
import re

P = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\scripts\gen_zz_ui.py"
src = open(P, encoding="utf-8").read()
BAD = 'style "' + chr(1) + '"'
lines = src.split("\n")
fixed = 0
leftover = []


def name_for(line):
    # --- style definitions (in STYLES block) ---
    if "capsule_idle" in line and "is button" in line:
        return "zz_menu_btn"
    if "background None" in line:
        return "zz_back_btn"
    if "zz_small_idle" in line and "selected_background" in line:
        return "zz_pref_btn"
    if "zz_small_idle" in line:
        return "zz_yesno_btn"
    if "is zz_menu_btn" in line and "xminimum 240" not in line and "size 26" not in line:
        return "zz_menu_btn_small"
    if "size 30" in line and "is default" in line:
        return "zz_menu_btn_text"
    if "size 26" in line and "is default" in line:
        return "zz_menu_btn_small_text"
    if "size 22" in line and "is default" in line:
        return "zz_pref_btn_text"
    if "size 28" in line and "is default" in line:
        return "zz_yesno_btn_text"
    if "size 24" in line and "is default" in line:
        return "zz_back_btn_text"
    # --- screen template lines ---
    if "音乐设置" in line:
        return "zz_menu_btn_small"
    if "返回" in line and "action Return()" in line:
        return "zz_back_btn"
    if '"是"' in line or '"否"' in line:
        return "zz_yesno_btn"
    if "{act} style" in line or "action {act}" in line:
        return "zz_menu_btn"
    return "zz_pref_btn"  # ADV/NVL/skip/vm/display buttons


for i, line in enumerate(lines):
    if BAD in line:
        nm = name_for(line)
        # definition lines: style X is PARENT:
        m = re.match(r'^(\s*)style "' + re.escape(chr(1)) + r'" is (\w+):', line)
        if m:
            lines[i] = f'{m.group(1)}style {nm} is {m.group(2)}:'
        else:
            lines[i] = line.replace(BAD, f'style "{nm}"')
        fixed += 1
        if nm == "zz_pref_btn" and "is button" in line:
            leftover.append(line)

out = "\n".join(lines)
open(P, "w", encoding="utf-8", newline="\n").write(out)
print("fixed lines:", fixed)
# sanity: no control chars remain
print("control chars left:", chr(1) in out)
# print the definition lines for eyeball check
for l in out.split("\n"):
    if re.match(r'\s*style zz_\w+ is \w+:', l):
        print("  DEF:", l.strip())
