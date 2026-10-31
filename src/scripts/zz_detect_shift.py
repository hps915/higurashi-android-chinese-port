# -*- coding: utf-8 -*-
"""严格检测译文偏移（只读）。

方法：用官方语料 ch6.json 建 EN->ZH 映射（精确 + 归一化）。
对工程每一行 k：
  ideal = corpus_zh(EN_k)
  若 ZH_k == ideal                      -> OK
  否则比较 ZH_k 与 corpus_zh(EN_{k+1}) / corpus_zh(EN_{k-1})
  若与 EN_{k+1} 的译文高度相似 -> 判定「前移一格」(SHIFT_FWD)
  若与 EN_{k-1} 的译文高度相似 -> 判定「后移一格」(SHIFT_BACK)
  否则 -> OTHER
输出统计与明细，供人工核实。
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
    out = []
    for i, l in enumerate(io.open(p, encoding="utf-8", errors="replace").read().split("\n"), 1):
        m = SAY.match(l.rstrip())
        if m:
            out.append((i, m.group(2) or "", m.group(3)))
    return out


def load_corpus():
    data = json.load(io.open(CORPUS, encoding='utf-8'))
    exact = {}
    for e in data:
        en, zh = e.get('en'), e.get('zh')
        if not en or not zh or not CJK.search(zh):
            continue
        exact.setdefault(norm(en), zhkey(zh))
    return exact


def main():
    corp = load_corpus()
    print("语料 EN->ZH:", len(corp))
    stats = {"OK": 0, "NO_CORPUS": 0, "SHIFT_FWD": 0, "SHIFT_BACK": 0, "OTHER": 0}
    details = []
    for f in sorted(os.listdir(K)):
        if not f.endswith(".rpy"):
            continue
        sp = os.path.join(SRC, "x-" + f)
        if not os.path.exists(sp):
            continue
        zh = rows(os.path.join(K, f))
        en = rows(sp)
        if len(zh) != len(en):
            print("!! 行数不一致:", f, len(zh), len(en))
            continue
        for k in range(len(zh)):
            zl, _zi, zb = zh[k]
            if not CJK.search(TAG.sub('', zb)):
                continue       # 纯标签行跳过
            ek = norm(en[k][2]) if k < len(en) else ''
            if not ek:
                continue
            ideal = corp.get(ek)
            if ideal is None:
                stats["NO_CORPUS"] += 1
                continue
            if zhkey(zb) == ideal:
                stats["OK"] += 1
                continue
            # 与邻居比较
            def sim_to(idx):
                if idx < 0 or idx >= len(en):
                    return 0.0
                cand = corp.get(norm(en[idx][2]))
                if not cand:
                    return 0.0
                return difflib.SequenceMatcher(None, zhkey(zb), cand).ratio()
            s_next = sim_to(k + 1)
            s_prev = sim_to(k - 1)
            s_here = difflib.SequenceMatcher(None, zhkey(zb), ideal).ratio()
            if s_next > 0.85 and s_next > s_here:
                stats["SHIFT_FWD"] += 1
                details.append(("SHIFT_FWD", f, zl, zb[:60], en[k][2][:60]))
            elif s_prev > 0.85 and s_prev > s_here:
                stats["SHIFT_BACK"] += 1
                details.append(("SHIFT_BACK", f, zl, zb[:60], en[k][2][:60]))
            else:
                stats["OTHER"] += 1
                details.append(("OTHER", f, zl, zb[:60], en[k][2][:60]))
    print()
    print("统计:", stats)
    print()
    print("明细（非 OK 部分）:")
    for kind, f, ln, zb, eb in details:
        print("  [%s] %s:%d" % (kind, f, ln))
        print("      ZH: %s" % zb)
        print("      EN: %s" % eb)


if __name__ == "__main__":
    main()
