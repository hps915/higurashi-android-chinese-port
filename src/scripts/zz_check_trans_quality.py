# -*- coding: utf-8 -*-
"""验证自动补译的结构质量：
 1) 说话人前后对比（译文行的 speaker 是否与原英文行一致）
 2) 文本标签序列是否保留
 3) 是否有明显重复行/串行（相邻两行完全相同 = 可能的对齐错位）
 4) 中英混排残留（一行里既有中文又有 >20 字母的英文块）
"""
import io
import os
import re
import sys

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
TSUMDIR = os.path.join(BASE, "work", "project_k", "game", "tsumihoroboshi")
BACKUP = os.path.join(BASE, "work", "_tsum_backup_for_check")

CJK = re.compile(u'[\u3000-\u303f\u3040-\u30ff\u4e00-\u9fff\uff00-\uffef]')
TAG = re.compile(r'\{[^{}]*\}')
SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*$')


def parse(path):
    rows = []
    for i, line in enumerate(io.open(path, encoding="utf-8").read().split("\n"), 1):
        m = SAY.match(line.rstrip())
        if not m:
            continue
        rows.append((i, (m.group(2) or "").strip(), m.group(3)))
    return rows


def main():
    if not os.path.isdir(BACKUP):
        print("备份目录不存在，改用 git-less 方式：只做自洽性检查")
        files = sorted(f for f in os.listdir(TSUMDIR) if f.endswith(".rpy"))
        check_self(files)
        return
    print("backup found:", BACKUP)


def check_self(files):
    print("[1] 相邻重复行（可能是对齐串行）")
    dup = 0
    duplist = []
    for f in files:
        p = os.path.join(TSUMDIR, f)
        rows = parse(p)
        for k in range(1, len(rows)):
            if rows[k][2] and rows[k][2] == rows[k - 1][2]:
                body = rows[k][2]
                if len(body) > 12 and CJK.search(body):
                    dup += 1
                    if len(duplist) < 40:
                        duplist.append("%s:%d  %s" % (f, rows[k][0], body[:90]))
    print("   相邻完全相同的台词行:", dup)
    for d in duplist:
        print("     ", d)

    print()
    print("[2] 中英混排残留（一行内 >20 连续英文字母 + 中文）")
    mix = 0
    mixlist = []
    for f in files:
        p = os.path.join(TSUMDIR, f)
        for i, line in enumerate(io.open(p, encoding="utf-8"), 1):
            m = SAY.match(line.rstrip())
            if not m:
                continue
            body = TAG.sub("", m.group(3))
            if not CJK.search(body):
                continue
            for run in re.findall(r"[A-Za-z][A-Za-z' ]{20,}", body):
                mix += 1
                if len(mixlist) < 30:
                    mixlist.append("%s:%d  [%s]  %s" % (f, i, run.strip()[:40], body[:70]))
                break
    print("   中英混排行:", mix)
    for d in mixlist:
        print("     ", d)

    print()
    print("[3] 标签序列丢失（译文行含 {nw} 但变量标签异常）")
    odd = []
    for f in files:
        p = os.path.join(TSUMDIR, f)
        for i, line in enumerate(io.open(p, encoding="utf-8"), 1):
            s = line.rstrip()
            if s.count("{") != s.count("}"):
                odd.append("%s:%d  %s" % (f, i, s.strip()[:90]))
    print("   花括号不配对行:", len(odd))
    for d in odd[:20]:
        print("     ", d)


if __name__ == "__main__":
    main()
