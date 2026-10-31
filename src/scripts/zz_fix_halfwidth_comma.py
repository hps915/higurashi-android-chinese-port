# -*- coding: utf-8 -*-
"""修正中文台词里的半角逗号 → 全角逗号（只处理「中文, 中文」这种明显误用）。

不动：
  - 问答编号 "问." / "解."（mina_ep 的说明书格式）
  - 数字/英文之间的标点
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
# 中文 + 半角逗号(+空格) + 中文
PAT = re.compile(u'([\u4e00-\u9fff\u3001\u3002\uff0c\uff1f\uff01\u2026])'
                 u'([ \t]*,)[ \t]*([\u4e00-\u9fff])')
# 句末也是：中文 + , + 结尾引号/行尾
PAT2 = re.compile(u'([\u4e00-\u9fff\u3001\u3002\uff0c\uff1f\uff01\u2026])([ \t]*,)[ \t]*$')

KEYWORDS = {
    "voice", "play", "stop", "queue", "show", "scene", "hide", "jump",
    "call", "label", "image", "with", "pause", "window", "nvl", "menu",
    "if", "elif", "else", "return", "pass", "python", "default", "define",
    "extend", "translate", "old", "new", "style", "text", "textbutton",
    "init", "screen", "use", "for", "while", "include", "options",
    "adv_extend", "nvl_extend",
}


def main():
    apply = "--apply" in sys.argv
    total = 0
    for label, gd in PROJECTS:
        for root, dirs, files in os.walk(gd):
            dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
            for f in sorted(files):
                if not f.endswith(".rpy"):
                    continue
                p = os.path.join(root, f)
                lines = io.open(p, encoding="utf-8").read().split("\n")
                changed = 0
                for i, line in enumerate(lines):
                    m = SAY.match(line.rstrip())
                    if not m:
                        continue
                    ident = (m.group(2) or "").strip()
                    if ident in KEYWORDS:
                        continue
                    b = m.group(3)
                    if not CJK.search(b):
                        continue
                    nb, n1 = PAT.subn(u'\\1\uff0c\\3', b)
                    nb, n2 = PAT2.subn(u'\\1\uff0c', nb)
                    if n1 + n2:
                        changed += n1 + n2
                        prefix = line[:line.rindex('"', 0, len(line) - len(line.lstrip()))] if False else None
                        # 重建行：保留缩进与说话人
                        st = line.lstrip()
                        indent = line[:len(line) - len(st)]
                        q = st.index('"')
                        lines[i] = indent + st[:q] + '"' + nb + '"'
                if changed:
                    total += changed
                    rel = os.path.relpath(p, gd).replace("\\", "/")
                    print("  %-46s %d" % (rel, changed))
                    if apply:
                        io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print()
    print("合计 %d 处 (apply=%s)" % (total, apply))


if __name__ == "__main__":
    main()
