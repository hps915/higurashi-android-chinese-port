# -*- coding: utf-8 -*-
"""严格核查：say 语句用到的说话人标识，是否都在工程里被定义成 Character。

做法：全文搜索所有 `ident = Character(...)` / `ident = nX.copy()` /
`ident = adv.copy()` 等赋值，再与 say 行里的标识求差集。
未定义标识在运行时会导致 NameError -> 报错页。
只读。
"""
import io
import os
import re
import sys

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
# 赋值语句：可选前导 "$ "，ident = <expression>
ASSIGN = re.compile(r'^\s*\$?\s*([A-Za-z_]\w*)\s*=\s*(.+)$', re.M)
# global 声明
GLOBAL = re.compile(r'^\s*global\s+([A-Za-z_][\w,\s]*)$', re.M)


def iter_rpy(gd):
    for root, dirs, files in os.walk(gd):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in sorted(files):
            if f.endswith(".rpy"):
                yield os.path.join(root, f)


def main():
    for label, gd in PROJECTS:
        defined = set()
        for p in iter_rpy(gd):
            t = io.open(p, encoding="utf-8", errors="replace").read()
            for m in ASSIGN.finditer(t):
                name, rhs = m.group(1), m.group(2)
                # 只要 rhs 是 Character / copy / adv 之类即可
                if "Character(" in rhs or ".copy(" in rhs or ".copy()" in rhs:
                    defined.add(name)
            for m in GLOBAL.finditer(t):
                for n in re.split(r'[,\s]+', m.group(1)):
                    if n:
                        defined.add(n)

        used = {}
        for p in iter_rpy(gd):
            rel = os.path.relpath(p, gd).replace("\\", "/")
            t = io.open(p, encoding="utf-8", errors="replace").read()
            for i, line in enumerate(t.split("\n"), 1):
                m = SAY.match(line.rstrip())
                if not m:
                    continue
                ident = (m.group(2) or "").strip()
                if not ident or ident in KEYWORDS:
                    continue
                used.setdefault(ident, []).append("%s:%d" % (rel, i))

        print("### %s" % label)
        print("  已定义 Character 名字: %d" % len(defined))
        print("  say 行用到的标识: %d 种" % len(used))
        undef = sorted(k for k in used if k not in defined)
        print("  未定义: %d 种" % len(undef))
        for k in undef:
            print("      %-18s 使用 %d 次  例: %s" % (k, len(used[k]), used[k][0]))
        print()


if __name__ == "__main__":
    main()
