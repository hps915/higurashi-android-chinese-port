# -*- coding: utf-8 -*-
"""Compare darwin .rpy dialogue statements against the extracted corpus per file.

Counts + samples a fuzzy join to estimate alignment quality for ch1.
"""
import json
import os
import re
import sys

RPY_DIR = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\apk_q\assets\x-game\x-onikakushi"
CORPUS = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\corpus\ch1.json"

# dialogue statements: CHAR "text"  or  extend "text"  (also n2/t/centered)
DLG = re.compile(r'^\s{4}(?:(extend)|([a-zA-Z_][\w]*)|([a-zA-Z_][\w]*)\s*\()?\s*"(.*)"\s*$')
VOICE = re.compile(r'^\s{4}voice\s+"(.*)"')
MENU_CAPTION = re.compile(r'^\s{8}"(.*)":')

def parse_rpy(path):
    stmts = []  # (kind, tag, text, voice)
    pending_voice = None
    menu_depth = 0
    for ln, line in enumerate(open(path, encoding="utf-8"), 1):
        mv = VOICE.match(line)
        if mv:
            pending_voice = mv.group(1)
            continue
        m = DLG.match(line)
        if m:
            tag = m.group(2) or m.group(3) or ("extend" if m.group(1) else None)
            text = m.group(4)
            stmts.append(("say", tag, text, pending_voice, ln))
            if pending_voice is None and tag != "extend":
                pass
            pending_voice = None
            continue
        mc = MENU_CAPTION.match(line)
        if mc and menu_depth > 0:
            stmts.append(("choice", None, mc.group(1), None, ln))
            continue
        if line.strip().startswith("menu"):
            menu_depth = 2
        elif line.strip() and not line.startswith(" " * 6) and not line.strip().startswith("#"):
            if menu_depth and line.startswith("    ") is False:
                menu_depth = 0
    return stmts


def main():
    corpus = json.load(open(CORPUS, encoding="utf-8"))
    by_file = {}
    for e in corpus:
        by_file.setdefault(e["file"], []).append(e)

    total_say = total_choice = 0
    print(f"{'file':<22}{'rpy_say':>8}{'rpy_choice':>11}{'corpus':>8}{'voiced_rpy':>11}{'voiced_c':>9}")
    for fn in sorted(by_file):
        rpy = os.path.join(RPY_DIR, "x-" + fn + ".rpy")
        if not os.path.exists(rpy):
            print(f"{fn:<22}  (no .rpy)")
            continue
        stmts = parse_rpy(rpy)
        says = [s for s in stmts if s[0] == "say" and s[2].strip() not in ("{nw}",)]
        choices = [s for s in stmts if s[0] == "choice"]
        voiced = [s for s in says if s[3]]
        entries = by_file[fn]
        voiced_c = [e for e in entries if e["voice"]]
        total_say += len(says)
        total_choice += len(choices)
        print(f"{fn:<22}{len(says):>8}{len(choices):>11}{len(entries):>8}{len(voiced):>11}{len(voiced_c):>9}")
    print(f"TOTAL rpy_say={total_say} rpy_choice={total_choice}")


if __name__ == "__main__":
    main()
