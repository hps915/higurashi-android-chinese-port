# -*- coding: utf-8 -*-
"""重新严格评估：区分「真错位」与「意译」。

判据更保守：
  真错位 = 中文与「上一行/下一行」的语料译文相似度 > 0.90
           且 与「本行」语料译文相似度 < 0.35
意译   = 与邻行相似度不高（说明是独立翻译的），即使与本行不匹配也算正常
"""
import difflib
import io
import json
import os
import re

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
K = os.path.join(BASE, "work", "project_k", "game", "tsumihoroboshi")
SRC = os.path.join(BASE, "work", "apk_k", "assets", "x-game", "x-tsumihoroboshi")
CORPUS = os.path.join(BASE, "work", "corpus", "ch6.json")

CJK = re.compile(u'[\u4e00-\u9fff]')
TAG = re.compile(r'\{[^{}]*\}')
SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*$')


def norm(s):
    s = TAG.sub('', s)
    s = re.sub(r'<[^<>]*>', '', s)
    s = s.replace('\\"', '"').replace("\\'", "'")
    s = re.sub(r'[^A-Za-z0-9]+', ' ', s)
    return s.strip().lower()


def zhkey(s):
    return re.sub(r'[\s\u3000]+', '', TAG.sub('', s))


def rows(p):
    return [(i, m.group(3)) for i, l in enumerate(
        io.open(p, encoding="utf-8", errors="replace").read().split("\n"), 1)
        if (m := SAY.match(l.rstrip()))]


def main():
    data = json.load(io.open(CORPUS, encoding='utf-8'))
    corp = {}
    for e in data:
        en, zh = e.get('en'), e.get('zh')
        if en and zh and CJK.search(zh):
            corp.setdefault(norm(en), zhkey(zh))
    print("语料:", len(corp))

    real = []
    checked = 0
    for f in sorted(os.listdir(K)):
        if not f.endswith(".rpy"):
            continue
        sp = os.path.join(SRC, "x-" + f)
        if not os.path.exists(sp):
            continue
        zh = rows(os.path.join(K, f))
        en = rows(sp)
        if len(zh) != len(en):
            print("!! 行数不一致 %s" % f)
            continue
        for k in range(len(zh)):
            zl, zb = zh[k]
            plain = TAG.sub('', zb)
            if len(zhkey(plain)) < 4:
                continue
            ek = norm(en[k][1])
            if not ek:
                continue
            ideal = corp.get(ek)
            if ideal is None:
                continue
            checked += 1
            cur = zhkey(zb)
            s_here = difflib.SequenceMatcher(None, cur, ideal).ratio()
            if s_here > 0.55:
                continue   # 大体正确
            # 和邻行比
            best = 0.0
            best_k = None
            for d in (-1, 1):
                j = k + d
                if 0 <= j < len(en):
                    cand = corp.get(norm(en[j][1]))
                    if cand:
                        s = difflib.SequenceMatcher(None, cur, cand).ratio()
                        if s > best:
                            best, best_k = s, d
            if best > 0.90 and best > s_here * 2:
                real.append((f, zl, zb[:56], en[k][1][:56], best_k, round(best, 2)))
    print("可对照行:", checked)
    print("判定为真错位:", len(real))
    for f, ln, zb, eb, d, s in real:
        print("  %s:%d  (与%s一行相似度 %.2f)" % (f, ln, "下" if d > 0 else "上", s))
        print("     ZH: %s" % zb)
        print("     EN: %s" % eb)


if __name__ == "__main__":
    main()
