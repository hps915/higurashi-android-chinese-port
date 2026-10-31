# -*- coding: utf-8 -*-
"""检查每个缺失资源引用，是否被 renpy.loadable(...) 守卫。

判定：引用所在行向上 3 行内出现 renpy.loadable(同名路径) -> 已守卫
结论分类：
  GUARDED    - 安全（文件不存在则不执行 show）
  UNGUARDED  - 隐患（会真的去加载不存在的图，触发兜底黑块）
"""
import io
import os
import re

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PROJECTS = [
    ("出题篇", os.path.join(BASE, "work", "project", "game")),
    ("解题篇", os.path.join(BASE, "work", "project_k", "game")),
]
PATH_RE = re.compile(r"'((?:background|characters|cg|efe|tips|text|overview|movie|images)/[^']*)'"
                     r'|"((?:background|characters|cg|efe|tips|text|overview|movie|images)/[^"]*)"')
EXT = (".png", ".jpg", ".jpeg", ".webp")


def iter_rpy(gd):
    for root, dirs, files in os.walk(gd):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in sorted(files):
            if f.endswith(".rpy"):
                yield os.path.join(root, f)


def main():
    for label, gd in PROJECTS:
        guarded = []
        unguarded = []
        for p in iter_rpy(gd):
            rel = os.path.relpath(p, gd).replace("\\", "/")
            lines = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
            for i, line in enumerate(lines):
                for m in PATH_RE.finditer(line):
                    path = m.group(1) or m.group(2)
                    if not path or not path.lower().endswith(EXT):
                        continue
                    full = os.path.join(gd, *path.split("/"))
                    if os.path.exists(full):
                        continue
                    # 检查上下文 6 行内是否有 loadable 守卫
                    ctx = "\n".join(lines[max(0, i - 6):i + 1])
                    if ("loadable(" in ctx or "loadable (" in ctx) and path in ctx:
                        guarded.append((rel, i + 1, path))
                    else:
                        unguarded.append((rel, i + 1, path))
        print("### %s" % label)
        print("  缺失资源引用：已守卫 %d 处，未守卫 %d 处"
              % (len(guarded), len(unguarded)))
        if unguarded:
            print("  未守卫明细:")
            for rel, ln, path in unguarded[:40]:
                print("     %s:%d  %s" % (rel, ln, path))
        print()


if __name__ == "__main__":
    main()
