# -*- coding: utf-8 -*-
"""第 8 轮 3.3：错字 / 日文残留 / 传统字 / 断句 修复。"""
import io
import os
import sys

K = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project_k\game"
Q = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\work\project\game"

# (base, rel, lineno, must_contain, replacement_text)
JOBS = [
    # ---- 错字 ----
    (K, "meakashi/meak_001.rpy", 619, u"毎", None),        # 每
    (K, "meakashi/meak_011.rpy", 320, u"毎天", None),      # 每天
    (K, "minagoroshi/mina_013.rpy", 523, u"知恵", None),   # 知惠
    (K, "matsuribayashi/mats_021.rpy", 1559, u"手電筒", None),  # 手电筒
    (K, "meakashi/meakashi_vm.rpy", 734, u"掉炸机", None),      # 轰炸机
    # ---- 日文残留 ----
    (K, "matsuribayashi/mats_024.rpy", 935, u"彼らの", None),
]

REPLACE_MAP = {
    u"毎": u"每",
    u"毎天": u"每天",
    u"知恵": u"知惠",
    u"手電筒": u"手电筒",
    u"掉炸机": u"轰炸机",
    u"彼らの指挥官": u"他们的指挥官",
}


def fix_chars(base, rel, ln, needle, _unused):
    p = os.path.join(base, rel.replace('/', os.sep))
    if not os.path.exists(p):
        print("NOFILE %s" % rel)
        return
    lines = io.open(p, encoding='utf-8').read().split('\n')
    i = ln - 1
    if i >= len(lines):
        print("OOR %s:%d" % (rel, ln))
        return
    cur = lines[i]
    if needle not in cur:
        print("MISS %s:%d  needle=%r  line=%r" % (rel, ln, needle, cur.strip()[:90]))
        return
    new = cur
    for a, b in REPLACE_MAP.items():
        new = new.replace(a, b)
    if new == cur:
        print("NOCHANGE %s:%d" % (rel, ln))
        return
    lines[i] = new
    io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print("ok %s:%d" % (rel, ln))
    print("   old: %s" % cur.strip()[:110])
    print("   new: %s" % new.strip()[:110])


def main():
    apply = '--apply' in sys.argv
    if not apply:
        print("(dry-run)")
    # 逐条定位，先只报告
    for base, rel, ln, needle, repl in JOBS:
        p = os.path.join(base, rel.replace('/', os.sep))
        lines = io.open(p, encoding='utf-8').read().split('\n')
        i = ln - 1
        cur = lines[i] if i < len(lines) else ''
        hit = needle in cur
        print("%-40s %5d  %s" % (rel, ln, "HIT" if hit else "MISS"))
        if hit:
            new = cur
            for a, b in REPLACE_MAP.items():
                new = new.replace(a, b)
            print("      - %s" % cur.strip()[:110])
            print("      + %s" % new.strip()[:110])
    if apply:
        print("\napplying...")
        for base, rel, ln, needle, repl in JOBS:
            fix_chars(base, rel, ln, needle, repl)


if __name__ == '__main__':
    main()
