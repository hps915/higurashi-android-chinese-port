# -*- coding: utf-8 -*-
"""内容质量深度核查（只读）。

 1) 中文文本里混入半角标点（。，、…… 之内的 , . ? ! 等）
 2) 说话人标识是否都在 zz_cn / screens 里定义过
 3) 同一句台词连续重复（可能串行）
 4) 文本标签不平衡（{i} 无 {/i} 之类）
"""
import io
import os
import re
from collections import Counter

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


def iter_rpy(game_dir):
    for root, dirs, files in os.walk(game_dir):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in sorted(files):
            if f.endswith(".rpy"):
                p = os.path.join(root, f)
                yield os.path.relpath(p, game_dir).replace("\\", "/"), p


def read(p):
    return io.open(p, encoding="utf-8", errors="replace").read()


def main():
    for label, gd in PROJECTS:
        print("=" * 92)
        print("### %s" % label)

        # 1) 半角标点混入中文
        halfwidth = []
        for rel, p in iter_rpy(gd):
            t = read(p)
            for i, line in enumerate(t.split("\n"), 1):
                m = SAY.match(line.rstrip())
                if not m:
                    continue
                b = m.group(3)
                if not CJK.search(b):
                    continue
                # 去掉标签、转义引号后看
                plain = re.sub(r'\{[^{}]*\}', '', b)
                # 中文句子里出现半角 , . ? ! 且前后都是中文
                for mm in re.finditer(u'[\u4e00-\u9fff][,\.\?!][\u4e00-\u9fff]', plain):
                    halfwidth.append((rel, i, plain[max(0, mm.start() - 12):mm.start() + 14]))
                    break
        print("  中文中夹半角标点: %d" % len(halfwidth))
        for x in halfwidth[:12]:
            print("      %s:%d  %s" % x)

        # 2) 说话人标识是否定义
        defined = set()
        for fn in ("zz_cn.rpy", "screens.rpy", "script.rpy", "characters.rpy"):
            fp = os.path.join(gd, fn)
            if os.path.exists(fp):
                t = read(fp)
                for m in re.finditer(r'^\s*(?:global\s+)?([A-Za-z_]\w*)\s*=\s*(?:Character|n3\.copy|n\.copy)', t, re.M):
                    defined.add(m.group(1))
                for m in re.finditer(r'^(\s+)([a-z]\w*)\s*=\s*n3\.copy', t, re.M):
                    defined.add(m.group(2))
        used = Counter()
        for rel, p in iter_rpy(gd):
            t = read(p)
            for line in t.split("\n"):
                m = SAY.match(line.rstrip())
                if not m:
                    continue
                ident = (m.group(2) or "").strip()
                if not ident or ident in KEYWORDS:
                    continue
                used[ident] += 1
        print("  使用中的说话人标识: %d 种" % len(used))
        missing = [k for k in used if k not in defined]
        print("  未在定义集合里的: %d" % len(missing))
        for k in sorted(missing)[:15]:
            print("      %-16s 用 %d 次" % (k, used[k]))

        # 3) 相邻重复
        dup = []
        for rel, p in iter_rpy(gd):
            lines = read(p).split("\n")
            prev = None
            prev_no = 0
            for i, line in enumerate(lines, 1):
                m = SAY.match(line.rstrip())
                if not m:
                    continue
                b = m.group(3)
                if not CJK.search(b) or len(b) < 10:
                    prev = b
                    prev_no = i
                    continue
                if b == prev:
                    dup.append((rel, i, b[:60]))
                prev = b
                prev_no = i
        print("  相邻完全相同的台词: %d" % len(dup))
        for x in dup[:10]:
            print("      %s:%d  %s" % x)

        # 4) 标签不平衡
        unbalanced = []
        for rel, p in iter_rpy(gd):
            t = read(p)
            for i, line in enumerate(t.split("\n"), 1):
                m = SAY.match(line.rstrip())
                if not m:
                    continue
                b = m.group(3)
                opens = re.findall(r'\{([^{}/][^{}]*)\}', b)
                closes = re.findall(r'\{/([^{}]*)\}', b)
                o = [x.partition("=")[0].strip() for x in opens]
                c = [x.strip() for x in closes]
                o = [x for x in o if x and x not in ("nw", "p", "w", "fast", "space",
                                                     "vspace", "cps", "_start", "_end")]
                if sorted(o) != sorted(c):
                    unbalanced.append((rel, i, o, c, b[:60]))
        print("  标签开闭不平衡: %d" % len(unbalanced))
        for x in unbalanced[:10]:
            print("      %s:%d  open=%s close=%s" % (x[0], x[1], x[2], x[3]))
        print()


if __name__ == "__main__":
    main()
