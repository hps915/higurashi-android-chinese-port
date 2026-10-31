# -*- coding: utf-8 -*-
"""核查：所有 image 定义指向的资源文件是否真实存在。

解析 `image NAME = "path"` / `renpy.image('NAME', "path")` /
`im.MatrixColor("path", ...)` / `im.Scale('path', ...)` 里的路径，
检查文件是否存在。只读。
"""
import io
import os
import re

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PROJECTS = [
    ("出题篇", os.path.join(BASE, "work", "project", "game")),
    ("解题篇", os.path.join(BASE, "work", "project_k", "game")),
]

# 匹配任何 "xxx.png/jpg" 之类的资源路径字面量
PATH_RE = re.compile(r'"((?:background|characters|cg|efe|tips|text|overview|movie|images)/[^"]*)"'
                     r'|\'((?:background|characters|cg|efe|tips|text|overview|movie|images)/[^\']*)\'')
EXT = (".png", ".jpg", ".jpeg", ".webp", ".ogg", ".mp3", ".ogv", ".mp4")
IMG_ONLY = (".png", ".jpg", ".jpeg", ".webp")


def iter_rpy(gd):
    for root, dirs, files in os.walk(gd):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in sorted(files):
            if f.endswith(".rpy"):
                yield os.path.join(root, f)


def main():
    for label, gd in PROJECTS:
        missing = {}
        checked = 0
        for p in iter_rpy(gd):
            rel = os.path.relpath(p, gd).replace("\\", "/")
            t = io.open(p, encoding="utf-8", errors="replace").read()
            for m in PATH_RE.finditer(t):
                path = m.group(1) or m.group(2)
                if not path or not path.lower().endswith(EXT):
                    continue
                checked += 1
                full = os.path.join(gd, *path.split("/"))
                if not os.path.exists(full):
                    ln = t[:m.start()].count("\n") + 1
                    missing.setdefault(path, []).append("%s:%d" % (rel, ln))
        print("### %s" % label)
        print("  引用的资源路径: %d 次" % checked)
        print("  文件不存在: %d 种" % len(missing))
        # 按引用点数量排序，只关心被代码实际引用的
        rows = sorted(missing.items(), key=lambda kv: -len(kv[1]))
        for path, locs in rows[:30]:
            print("   %-46s x%-3d  %s" % (path, len(locs), locs[0]))
        print()


if __name__ == "__main__":
    main()
