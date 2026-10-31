# -*- coding: utf-8 -*-
"""v3 injector: name-based mapping + voice-overlap fallback.

Corpus file name patterns (per chapter, prefixes vary):
  z{base}_vm00_n01 / _z{base}_vm00_n01 / {base}_vm00_n01   -> {chapter}_vm.rpy
      section label: vm_{base}_00_n01   (vm0x -> 0x)
  {name}_tips_NN / _{name}_tips_NN                       -> {chapter}_tips.rpy
      section label: {name}_tips_NN  (digit-count normalized)
  omake_NN / zomake_NN (main, no _vm)                    -> {chapter}_omake.rpy whole file
  {X}                                                    -> {X}.rpy whole file
Port files with no name match (merged kakera etc.) get the voice-overlap
candidate treatment from kai_inject (leftover corpus files only).

Usage: inject_v3.py <corpus.json> <src_root> <dst_root> <chapter_dir>
  src_root = apk_q/assets/x-game (pristine, x- prefixed)
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inject_cn import iter_says, rewrite_rpy_lines, rewrite_rpy, xpath, norm_text, LABEL

VM_RE = re.compile(r'^(?:_?z)?(.+?)_vm(00|0x)_n01$')
TIPS_RE = re.compile(r'^(?:_)?(\w+_tips_\w+)$')
OMAKE_RE = re.compile(r'^(?:_?z)?omake\w*$')
SKIP_FILES = {"&opening", "&choicesdialog", "flow", "init", "dummy", "update"}


def label_spans(lines):
    """[(label, start, end)] for top-level (column 0) labels."""
    marks = []
    for i, line in enumerate(lines):
        m = LABEL.match(line)
        if m:
            marks.append((m.group(1), i))
    spans = []
    for k, (lbl, i) in enumerate(marks):
        end = marks[k + 1][1] if k + 1 < len(marks) else len(lines)
        spans.append((lbl, i, end))
    return spans


def match_label(labels, want):
    if want in labels:
        return want
    m = re.match(r'^(\w+_tips_)(\d+)$', want)
    if m:
        head, n = m.group(1), int(m.group(2))
        for l in labels:
            m2 = re.match(r'^(\w+_tips_)(\d+)$', l)
            if m2 and m2.group(1) == head and int(m2.group(2)) == n:
                return l
    return None


def rewrite_sections(src_path, dst_path, section_corpus):
    """section_corpus: {corpus_file: (label, entries)}. Rewrite label spans."""
    lines = open(src_path, encoding="utf-8").read().split("\n")
    spans = label_spans(lines)
    labels = [s[0] for s in spans]
    out = list(lines)
    done = 0
    for cf, (want, entries) in sorted(section_corpus.items()):
        actual = match_label(labels, want)
        if actual is None:
            print(f"    !! label {want} not found ({cf})")
            continue
        lbl, start, end = next(s for s in spans if s[0] == actual)
        block = out[start:end]
        # rewrite into temp then splice
        n, r = rewrite_rpy_lines(block, entries, "_tmp_section.rpy")
        out[start:end] = open("_tmp_section.rpy", encoding="utf-8").read().split("\n")
        done += 1
        print(f"    [{actual}] {r}/{n} chinese")
    if done:
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        with open(dst_path, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(out))
    return done


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
        cf_texts = set(norm_text(str(e["en"])) for e in entries if not e["voice"])
        if len(cf_texts & text_keys) >= 3:
            cand[cf] = (len(cf_texts & text_keys), set())
    return cand, voices_seq


def main():
    corpus_path, src_root, dst_root, chapter_dir = sys.argv[1:5]
    by_file = {}
    for e in json.load(open(corpus_path, encoding="utf-8")):
        by_file.setdefault(e["file"], []).append(e)

    src_ch = os.path.join(src_root, "x-" + chapter_dir)
    dst_ch = os.path.join(dst_root, chapter_dir)
    port_names = {f[2:-4] for f in os.listdir(src_ch) if f.endswith(".rpy")}
    handled_port = set()
    total_say = total_zh = 0

    def src_of(port_name):
        return os.path.join(src_ch, "x-" + port_name + ".rpy")

    def dst_of(port_name):
        return os.path.join(dst_ch, port_name + ".rpy")

    # ---- categorize corpus files
    vm_sec, tips_sec, omake_files, normal, leftover = {}, {}, [], {}, {}
    for f in by_file:
        if f in SKIP_FILES or f.startswith("&"):
            continue
        m = VM_RE.match(f)
        if m:
            base, g = m.group(1), m.group(2)
            # vm .mg holds only the differing lines; merge the base file's
            # entries so the full port section can be anchored
            merged = list(by_file[f])
            for alt in (base, "_" + base):
                if alt in by_file and alt != f:
                    merged += by_file[alt]
            vm_sec[f] = (f"vm_{base}_{g}_n01", merged)
            continue
        if "_vm" in f:
            continue  # vm pattern that didn't match (unexpected)
        m = TIPS_RE.match(f)
        if m:
            tips_sec[f] = (m.group(1), by_file[f])
            continue
        if OMAKE_RE.match(f):
            omake_files.append(f)
            continue
        if f in port_names:
            normal[f] = f
        else:
            leftover[f] = f

    # ---- vm sections
    vm_port = chapter_dir + "_vm"
    if vm_sec and vm_port in port_names:
        print(f"  == {vm_port}.rpy: {len(vm_sec)} vm variants")
        rewrite_sections(src_of(vm_port), dst_of(vm_port), vm_sec)
        handled_port.add(vm_port)
    elif vm_sec:
        print(f"  == no port vm file for {len(vm_sec)} variants")

    # ---- tips sections
    tips_port = chapter_dir + "_tips"
    if tips_sec and tips_port in port_names:
        print(f"  == {tips_port}.rpy: {len(tips_sec)} tips")
        rewrite_sections(src_of(tips_port), dst_of(tips_port), tips_sec)
        handled_port.add(tips_port)
    elif tips_sec:
        print(f"  == no port tips file for {len(tips_sec)} tips files")

    # ---- omake whole file
    omake_port = chapter_dir + "_omake"
    if omake_files and omake_port in port_names:
        merged = [e for f in sorted(omake_files) for e in by_file[f]]
        n, r = rewrite_rpy(src_of(omake_port), merged, dst_of(omake_port))
        total_say += n
        total_zh += r
        handled_port.add(omake_port)
        print(f"  == {omake_port}: {r}/{n} chinese <- {omake_files}")

    # ---- normal same-name files
    for f in sorted(normal):
        n, r = rewrite_rpy(src_of(f), by_file[f], dst_of(f))
        total_say += n
        total_zh += r
    handled_port |= set(normal.values())
    print(f"  == {len(normal)} same-name files done")

    # ---- overlap pass for remaining port files
    # candidates: all corpus except per-label vm/tips sections (main/omake/leftover,
    # so port vm files without their own variants still match main-script text)
    rem_corpus = {f: by_file[f] for f in list(normal) + list(leftover) + omake_files}
    for port in sorted(port_names - handled_port):
        src = src_of(port)
        lines = open(src, encoding="utf-8").read().split("\n")
        says = list(iter_says(lines))
        if not says or not rem_corpus:
            continue
        cand, voices_seq = build_candidates(rem_corpus, says)

        def first_pos(cf):
            vs = cand[cf][1]
            if not vs:
                return 500000
            for i, v in enumerate(voices_seq):
                if v in vs:
                    return i
            return 1000000

        sel = [cf for cf in sorted(cand, key=first_pos)
               if (cand[cf][1] and cand[cf][0] >= 2) or not cand[cf][1]]
        if not sel:
            continue
        corpus_list = [e for cf in sel for e in rem_corpus[cf]]
        n, r = rewrite_rpy_lines(lines, corpus_list, dst_of(port))
        total_say += n
        total_zh += r
        srcs = sel if len(sel) <= 4 else sel[:3] + [f"...+{len(sel)-3}"]
        print(f"  == {port}: {r}/{n} chinese <- {srcs}")
    print(f"TOTAL {chapter_dir}: {total_zh}/{total_say} named+overlap chinese")


if __name__ == "__main__":
    main()
