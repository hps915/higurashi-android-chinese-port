# -*- coding: utf-8 -*-
"""全面扫描半角标点混入中文台词（不限单行，含全角/半角混用）。"""
import io
import os
import re

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PROJECTS = [
    ("出题篇", os.path.join(BASE, "work", "project", "game")),
    ("解题篇", os.path.join(BASE, "work", "project_k", "game")),
]
CJK = re.compile(u'[\u4e00-\u9fff]')
SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*$')
KEYWORDS = {
    "voice", "play", "stop", "queue", "show", "scene", "hide", "jump",
    "call", "label", "image", "with", "pause", "window", "nvl", "menu",
    "if", "elif", "else", "return", "pass", "python", "default", "define",
    "extend", "translate", "old", "new", "style", "text", "textbutton",
    "init", "screen", "use", "for", "while", "include", "options",
    "adv_extend", "nvl_extend",
}
# 半角标点紧跟中文字符（允许中间有空格/引号）
PAT = re.compile(u'[\u4e00-\u9fff][ \t]*([,\.\?!;:])[ \t]*[\u4e00-\u9fff]')


def main():
    for label, gd in PROJECTS:
        hits = []
        for root, dirs, files in os.walk(gd):
            dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
            for f in sorted(files):
                if not f.endswith(".rpy"):
                    continue
                p = os.path.join(root, f)
                rel = os.path.relpath(p, gd).replace("\\", "/")
                for i, line in enumerate(io.open(p, encoding="utf-8", errors="replace"), 1):
                    m = SAY.match(line.rstrip())
                    if not m:
                        continue
                    b = m.group(3)
                    if not CJK.search(b):
                        continue
                    plain = re.sub(r'\{[^{}]*\}', '', b)
                    for mm in PAT.finditer(plain):
                        hits.append((rel, i, plain[:90], mm.group(1)))
                        break
        print("### %s  中文夹半角标点: %d 处" % (label, len(hits)))
        for rel, i, txt, ch in hits[:40]:
            print("   %s:%d [%s]  %s" % (rel, i, ch, txt))
        print()


if __name__ == "__main__":
    main()
