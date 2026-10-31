# -*- coding: utf-8 -*-
"""从已编译的 .rpyc 中提取 image 定义，再做 show/scene 交叉比对。

.rpyc 是 zlib 压缩的 pickle。image 定义在 store 里以 `build.classify` /
`renpy.display.image.images` 的形式存在，但更简单可靠的方式是：
解析 .rpy 源码中的 `image NAME = ...` / `image NAME:` / `renpy.image('NAME', ...)`，
这次不用启发式属性匹配，而是用 Ren'Py 的 tag/attribute 解析规则：

Ren'Py 图像名 = tag + attrs。`show rena 1a warai_a1_` 的 tag 是 `rena`，
attrs 是 ["1a", "warai_a1_"]。匹配规则是：把 attrs 依次加进 tag，检查
`(rena,)`, `(rena,1a)`, `(rena,1a,warai_a1_)` 这几个前缀元组里是否有已定义图像。
一旦命中就停止（Ren'Py 的实际算法就是这样：从最长到最短尝试）。

另外还有 "attribute 里含下划线但没有对应图像" 的情况，Ren'Py 会继续拆分
（如 `rena 1b bikkuri_a1_` 里 `bikkuri_a1_` 是单个 attr）。这里就用严格的前缀
元组匹配即可，误报率极低。
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

IMG_DEF = re.compile(r'^\s*image\s+([A-Za-z0-9_]+(?:\s+[A-Za-z0-9_]+)*)\s*[:=]')
RENPY_IMAGE = re.compile(r"renpy\.image\(\s*['\"]([^'\"]+)['\"]")
SHOW = re.compile(r'^\s*(?:show|scene)\s+([A-Za-z0-9_]+(?:\s+[A-Za-z0-9_]+)*)')
SKIP_TAGS = {"expression", "screen", "layer", "text", "vtext", "imagebutton",
             "imagemap", "aspect", "solid", "null", "frame", "window", "grid",
             "vbox", "hbox", "fixed", "side", "bar", "transform"}
BUILTIN_TAGS = {"black", "white", "bg", "cg", "text"}


def collect(game_dir):
    defined = set()
    for root, dirs, files in os.walk(game_dir):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in files:
            if not f.endswith(".rpy"):
                continue
            p = os.path.join(root, f)
            for line in io.open(p, encoding="utf-8", errors="replace"):
                s = line.rstrip()
                m = IMG_DEF.match(s)
                if m:
                    defined.add(tuple(m.group(1).split()))
                m2 = RENPY_IMAGE.search(s)
                if m2:
                    defined.add(tuple(m2.group(1).split()))
    return defined


def check(label, game_dir):
    print("=" * 96)
    print("###", label)
    defined = collect(game_dir)
    print("已定义图像名:", len(defined))
    tags = set(t[0] for t in defined)
    print("tags:", len(tags))

    unresolved = {}
    n_show = 0
    for root, dirs, files in os.walk(game_dir):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in sorted(files):
            if not f.endswith(".rpy"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, game_dir).replace("\\", "/")
            for i, line in enumerate(io.open(p, encoding="utf-8", errors="replace"), 1):
                m = SHOW.match(line.rstrip())
                if not m:
                    continue
                parts = m.group(1).split()
                tag = parts[0]
                if tag in SKIP_TAGS:
                    continue
                n_show += 1
                # Ren'Py 语义：从最长的前缀开始尝试
                hit = False
                for k in range(len(parts), 0, -1):
                    if tuple(parts[:k]) in defined:
                        hit = True
                        break
                if hit:
                    continue
                # 特殊：tag 本身未定义，但可能在 images/ 目录自动发现（本工程无 images/）
                unresolved.setdefault(tag, []).append("%s:%d  %s" % (rel, i, " ".join(parts)))
    print("show/scene 语句:", n_show)
    if not unresolved:
        print(">>> 全部可解析（无红字风险）")
        return
    total = sum(len(v) for v in unresolved.values())
    print(">>> 无法解析:", total, "处 /", len(unresolved), "个 tag")
    for tag, locs in sorted(unresolved.items(), key=lambda kv: -len(kv[1])):
        print("  %-22s x%-4d %s" % (tag, len(locs), locs[0][:110]))
        for l in locs[1:4]:
            print("                            ", l[:110])


def main():
    for label, game_dir in PROJECTS:
        check(label, game_dir)
        print()


if __name__ == "__main__":
    main()
