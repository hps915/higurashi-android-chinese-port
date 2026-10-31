# -*- coding: utf-8 -*-
"""Inject Chinese into the Kai (answer arcs) port.

The Kai port merges/splits the 07th-mod script files differently (e.g. 26
_kakera files -> 3 port files), so files are mapped by voice-ID overlap:
each port .rpy is matched against the corpus files whose voice sequences
occur inside it, candidates are ordered by first occurrence, concatenated,
and the standard align+rewrite runs on the result.

Usage: kai_inject.py <corpus.json> <src_root> <dst_root> <chapter_dir>
  src_root = apk_k/assets/x-game (pristine, x- prefixed)
  dst_root = project_k/game
  chapter_dir = meakashi|tsumihoroboshi|minagoroshi|matsuribayashi
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inject_cn import iter_says, rewrite_rpy_lines, xpath, norm_text


def build_candidates(corpus_by_file, says):
    voices_seq = [s[5] for s in says]
    voice_set = set(v for v in voices_seq if v)
    text_keys = set(norm_text(s[4]) for s in says if not s[5])
    cand = {}
    for cf, entries in corpus_by_file.items():
        cf_voices = set(e["voice"] for e in entries if e["voice"])
        if cf_voices:
            inter = cf_voices & voice_set
            if len(inter) >= 2:
                cand[cf] = (len(inter), cf_voices)
                continue
        # unvoiced fallback: text key overlap
        cf_texts = set(norm_text(str(e["en"])) for e in entries if not e["voice"])
        if len(cf_texts & text_keys) >= 3:
            cand[cf] = (len(cf_texts & text_keys), set())
    return cand, voices_seq


def main():
    corpus_path, src_root, dst_root, chapter_dir = sys.argv[1:5]
    corpus = json.load(open(corpus_path, encoding="utf-8"))
    by_file = {}
    for e in corpus:
        by_file.setdefault(e["file"], []).append(e)

    # drop vm variants and engine internals
    drop = [f for f in by_file if f.startswith("_z") or f.startswith("z") or f in
            ("&opening", "flow", "init", "dummy", "&choicesdialog")]
    for f in drop:
        del by_file[f]

    port_dir = os.path.join(dst_root, chapter_dir)
    src_dir = os.path.join(src_root, "x-" + chapter_dir)
    files = sorted(f for f in os.listdir(src_dir) if f.endswith(".rpy"))

    total_say = total_zh = 0
    for fn in files:
        port_name = fn[2:-4] if fn.startswith("x-") else fn[:-4]
        src = os.path.join(src_dir, fn)
        lines = open(src, encoding="utf-8").read().split("\n")
        says = list(iter_says(lines))
        if not says:
            continue
        cand, voices_seq = build_candidates(by_file, says)

        def first_pos(cf):
            vs = cand[cf][1]
            if not vs:
                return 500000
            for i, v in enumerate(voices_seq):
                if v in vs:
                    return i
            return 1000000

        sel = []
        for cf in sorted(cand, key=first_pos):
            score, vs = cand[cf]
            if vs and score >= 2:
                sel.append(cf)
            elif not vs:
                sel.append(cf)
        if not sel:
            print(f"  {port_name}: no corpus match ({len(says)} says stay English)")
            continue
        corpus_list = [e for cf in sel for e in by_file[cf]]
        dst = os.path.join(port_dir, port_name + ".rpy")
        n, r = rewrite_rpy_lines(lines, corpus_list, dst)
        total_say += n
        total_zh += r
        srcs = sel if len(sel) <= 4 else sel[:3] + [f"...{len(sel)-3} more"]
        print(f"  {port_name}: {r}/{n} chinese  <- {srcs}")
    print(f"TOTAL {chapter_dir}: {total_zh}/{total_say} ({100.0 * total_zh / max(1, total_say):.1f}%)")


if __name__ == "__main__":
    main()
