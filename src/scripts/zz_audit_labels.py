# -*- coding: utf-8 -*-
"""静态扫描 Ren'Py 工程：call/jump 目标标签是否存在。
用法: python work/scripts/zz_audit_labels.py <game_dir>
"""
import io
import os
import re
import sys

# label 行可能带参数（参数里还有嵌套括号），所以只匹配到名字为止
LABEL_RE = re.compile(r'^[ \t]*label\s+([A-Za-z_][\w.]*)', re.M)
CALL_RE = re.compile(r'^\s*(?:call|jump)\s+([A-Za-z_][\w.]*)', re.M)
# 排除 call screen / call expression 等
CALL_SCREEN = re.compile(r'^\s*call\s+screen\b', re.M)


def collect(game_dir):
    labels = {}
    calls = []
    for root, dirs, files in os.walk(game_dir):
        dirs[:] = [d for d in dirs if d not in ('cache', 'saves', 'tl')]
        for f in files:
            if not f.endswith('.rpy'):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, game_dir).replace('\\', '/')
            t = io.open(p, encoding='utf-8', errors='replace').read()
            # strip comments for label detection
            for m in LABEL_RE.finditer(t):
                labels.setdefault(m.group(1), rel)
            for m in CALL_RE.finditer(t):
                # `call screen xxx` 是引擎内建语句，不是标签跳转
                line_start = t.rfind('\n', 0, m.start()) + 1
                if t[line_start:m.start() + 40].lstrip().startswith('call screen'):
                    continue
                ln = t[:m.start()].count('\n') + 1
                calls.append((rel, ln, m.group(1)))
    return labels, calls


def main():
    game_dir = sys.argv[1] if len(sys.argv) > 1 else r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project\game"
    labels, calls = collect(game_dir)
    print("game_dir:", game_dir)
    print("labels:", len(labels), " calls/jumps:", len(calls))
    # sub-labels like x.dialog001 resolve if parent label exists? No - they must exist literally.
    missing = {}
    for rel, ln, tgt in calls:
        if tgt in labels:
            continue
        # allow property-style `call x.y` if `x.y` is not defined but `x` is and this is a
        # vm variant group where dot-labels are generated dynamically -> count separately
        missing.setdefault(tgt, []).append((rel, ln))
    if not missing:
        print("\nOK: 全部 call/jump 目标都有定义")
        return 0
    print("\nMISSING targets:", len(missing))
    for tgt in sorted(missing):
        locs = missing[tgt]
        print("  %-48s x%d  %s" % (tgt, len(locs), locs[0]))
        if len(locs) > 1:
            for r, l in locs[1:]:
                print("       ", r, l)
    return 1


if __name__ == '__main__':
    sys.exit(main())
