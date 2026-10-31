# -*- coding: utf-8 -*-
"""Inject Chinese text into decompiled darwin-port .rpy files.

Alignment: voice-IDs and normalized English text form keys; difflib
SequenceMatcher aligns the two sequences globally, replace-blocks are
paired locally by text similarity. Lines without a Chinese counterpart
keep their English text.

Usage: inject_cn.py <corpus.json> <src_rpy_dir> <dst_rpy_dir> <map_spec>
  map_spec: comma list of  corpusPrefix:rpyDir:tipsRpy  e.g.
            onik:onikakushi:onikakushi_tips
"""
import difflib
import json
import os
import re
import sys

DLG = re.compile(r'^(\s*)(extend|nvl_extend|n2|n|t|centered|a_\w+)\s+(".*")\s*$')
VOICE = re.compile(r'^\s*voice\s+"(.*)"')
LABEL = re.compile(r'^label\s+(\w+):')
TAG = re.compile(r'\{[^}]*\}')


def norm_voice(v):
    if not v:
        return None
    return v.replace("voice/", "").replace(".ogg", "")


def norm_text(s):
    s = TAG.sub("", s)
    s = s.replace('\\"', '"').replace("\\n", " ")
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s[:60]


def unescape_rpy(s):
    """rpy source text -> plain text."""
    return s[1:-1].replace('\\"', '"')  # keep other escapes as-is


def escape_rpy(zh):
    return zh.replace('"', '\\"')


def xpath(base, rel):
    """Map 'watanagashi/wata_001.rpy' -> base/x-watanagashi/x-wata_001.rpy"""
    return os.path.join(base, *("x-" + p for p in rel.replace("\\", "/").split("/")))


def iter_says(lines):
    """Yield say statements: (idx, line_no, indent, tag, text, voice)."""
    pending_voice = None
    idx = 0
    for ln, line in enumerate(lines, 1):
        mv = VOICE.match(line)
        if mv:
            pending_voice = norm_voice(mv.group(1))
            continue
        m = DLG.match(line)
        if m:
            text = unescape_rpy(m.group(3))
            if text.strip() == "{nw}":
                continue
            yield idx, ln, m.group(1), m.group(2), text, pending_voice
            pending_voice = None
            idx += 1


def align(rpy_says, corpus):
    """Return {rpy_idx: corpus_idx}."""
    keys_r = ["V:" + s[5] if s[5] else "T:" + norm_text(s[4]) for s in rpy_says]
    keys_c = ["V:" + e["voice"] if e["voice"] else "T:" + norm_text(str(e["en"])) for e in corpus]
    sm = difflib.SequenceMatcher(None, keys_r, keys_c, autojunk=False)
    pairs = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                pairs[i1 + k] = j1 + k
        elif tag == "replace":
            # local similarity pairing
            for i in range(i1, i2):
                best, best_r = None, 0.35
                for j in range(j1, j2):
                    r = difflib.SequenceMatcher(None, norm_text(rpy_says[i][4]),
                                                norm_text(str(corpus[j]["en"]))).ratio()
                    if r > best_r:
                        best, best_r = j, r
                if best is not None:
                    pairs[i] = best
    return pairs


def align2(rpy_says, corpus):
    """Anchored alignment: exact voice-key pairing first, then unvoiced gaps
    are filled positionally/by text similarity between neighbouring anchors.
    Far more robust than global SequenceMatcher for merged/variant files."""
    # 1. voice anchors (first occurrence; prefer entries with zh)
    vmap = {}
    for j, e in enumerate(corpus):
        v = e["voice"]
        if v:
            if v not in vmap:
                vmap[v] = j
            elif not str(corpus[vmap[v]].get("zh") or "").strip() and str(e.get("zh") or "").strip():
                vmap[v] = j
    pairs = {}
    for i, s in enumerate(rpy_says):
        if s[5] and s[5] in vmap:
            pairs[i] = vmap[s[5]]
    # 2. gaps between anchors (keep only monotonically increasing anchors)
    inc = []
    last_j = -1
    for i in sorted(pairs):
        if pairs[i] > last_j:
            inc.append((i, pairs[i]))
            last_j = pairs[i]
    anchor_items = inc
    bounds = [(-1, -1)] + anchor_items + [(len(rpy_says), len(corpus))]
    for (pi, pj), (ni, nj) in zip(bounds, bounds[1:]):
        lo_i, hi_i = pi + 1, ni          # unvoiced port lines pi+1 .. ni-1
        lo_j, hi_j = pj + 1, nj          # corpus entries pj+1 .. nj-1
        gap_r = [k for k in range(lo_i, hi_i) if k not in pairs]
        gap_c = list(range(lo_j, hi_j))
        if not gap_r or not gap_c:
            continue
        is_leading = (pi == -1)
        if len(gap_r) == len(gap_c):
            for a, b in zip(gap_r, gap_c):
                pairs[a] = b
            continue
        # unequal: local similarity pairing
        for a in gap_r:
            best, best_r = None, (0.5 if is_leading else 0.35)
            for b in gap_c:
                r = difflib.SequenceMatcher(None, norm_text(rpy_says[a][4]),
                                            norm_text(str(corpus[b]["en"]))).ratio()
                if r > best_r:
                    best, best_r = b, r
            if best is not None:
                pairs[a] = best
    # 3. exact text-key fallback (handles voice-set mismatches: port uses a
    #    ps3/xxx voice while the corpus has the same line under org/xxx)
    used = set(pairs.values())
    tmap = {}
    for j, e in enumerate(corpus):
        if j in used or not str(e.get("zh") or "").strip():
            continue
        k = norm_text(str(e["en"]))
        if k and k not in tmap:
            tmap[k] = j
    for i, s in enumerate(rpy_says):
        if i in pairs:
            continue
        k = norm_text(s[4])
        if not k:
            continue
        j = tmap.get(k)
        if j is not None:
            pairs[i] = j
            used.add(j)
            tmap.pop(k, None)
    # 4. token-indexed fuzzy fallback for leftovers
    import collections as _c
    tok_idx = _c.defaultdict(list)
    rest = set()
    for j, e in enumerate(corpus):
        if j in used or not str(e.get("zh") or "").strip():
            continue
        rest.add(j)
        for t in set(re.findall(r'[a-z]{3,}', norm_text(str(e["en"])))):
            tok_idx[t].append(j)
    for i, s in enumerate(rpy_says):
        if i in pairs:
            continue
        t = norm_text(s[4])
        if len(t) < 10:
            continue
        cand = set()
        for tok in set(re.findall(r'[a-z]{3,}', t)):
            cand.update(tok_idx.get(tok, ()))
        cand &= rest
        if not cand:
            continue
        best, best_r = None, 0.7
        for j in cand:
            r = difflib.SequenceMatcher(None, t, norm_text(str(corpus[j]["en"]))).ratio()
            if r > best_r:
                best, best_r = j, r
        if best is not None:
            pairs[i] = best
            used.add(best)
            rest.discard(best)
    return pairs


def rewrite_rpy(src_path, corpus_for_file, dst_path):
    lines = open(src_path, encoding="utf-8").read().split("\n")
    says = list(iter_says(lines))
    pairs = align2(says, corpus_for_file)

    zh_of = {}
    for i, j in pairs.items():
        zh = corpus_for_file[j]["zh"]
        if zh is not None and str(zh).strip():
            zh_of[i] = str(zh)

    out = []
    si = 0
    pending_voice = None
    replaced = 0
    for line in lines:
        mv = VOICE.match(line)
        if mv:
            pending_voice = norm_voice(mv.group(1))
            out.append(line)
            continue
        m = DLG.match(line)
        if m:
            text = unescape_rpy(m.group(3))
            if text.strip() == "{nw}":
                out.append(line)
                continue
            zh = zh_of.get(si)
            if zh:
                out.append(f'{m.group(1)}{m.group(2)} "{escape_rpy(zh)}"')
                replaced += 1
            else:
                out.append(line)
            pending_voice = None
            si += 1
            continue
        out.append(line)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out))
    return len(says), replaced


def load_corpus(path, prefix):
    by_file = {}
    for e in json.load(open(path, encoding="utf-8")):
        by_file.setdefault(e["file"], []).append(e)
    return by_file


def main():
    corpus_path, src_dir, dst_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    spec = sys.argv[4].split(":")  # e.g. onik:onikakushi:onikakushi_tips
    cpfx, rpy_dir, tips_name = spec[0], spec[1], spec[2]
    by_file = load_corpus(corpus_path, cpfx)

    total_say = total_zh = 0
    # map corpus file -> rpy relative path (or tips section)
    file_map = {}
    for f in by_file:
        if f.startswith("&") or f in ("flow", "init", "dummy"):
            continue
        if f.startswith(cpfx + "_tips_"):
            file_map[f] = (os.path.join(rpy_dir, tips_name + ".rpy"), f)
        elif f.startswith("omake"):
            file_map[f] = (os.path.join(rpy_dir, tips_name.replace("_tips", "_omake") + ".rpy"), None)
        elif f == cpfx + "_op":
            file_map[f] = (os.path.join(rpy_dir, cpfx + "_op.rpy"), None)
        else:
            file_map[f] = (os.path.join(rpy_dir, f + ".rpy"), None)

    # group by rpy path (tips target holds several corpus files by label)
    targets = {}
    for cf, (rpy_rel, section) in file_map.items():
        targets.setdefault(rpy_rel, []).append((cf, section))

    for rpy_rel, cfs in sorted(targets.items()):
        src = xpath(src_dir, rpy_rel)
        dst = os.path.join(dst_dir, rpy_rel)
        if not os.path.exists(src):
            print(f"  SKIP (no source): {rpy_rel} for {[c[0] for c in cfs]}")
            continue
        if len(cfs) == 1 and cfs[0][1] is None:
            n, r = rewrite_rpy(src, by_file[cfs[0][0]], dst)
            total_say += n
            total_zh += r
            print(f"  {rpy_rel}: {r}/{n} lines chinese")
        else:
            # tips file: split by label
            lines = open(src, encoding="utf-8").read().split("\n")
            sections = {}
            cur = None
            for i, line in enumerate(lines):
                ml = LABEL.match(line)
                if ml:
                    cur = ml.group(1)
                    sections[cur] = [] if cur not in sections else sections[cur]
                if cur:
                    sections[cur].append(line)
                    sections.setdefault("_lines_" + cur, []).append(i)
            # rewrite each section independently
            out_lines = list(lines)
            for cf, section in cfs:
                if section is None:
                    section = cf  # omake: whole file handled elsewhere
                if section not in sections:
                    print(f"  !! label {section} not found in {rpy_rel}")
                    continue
                # find line range of this label (until next label)
                lbl_order = [m.group(1) for m in (LABEL.match(l) for l in lines) if m]
                # simple: rewrite the section block
                start = next(i for i, l in enumerate(lines) if LABEL.match(l) and LABEL.match(l).group(1) == section)
                end = len(lines)
                for j in range(start + 1, len(lines)):
                    if LABEL.match(lines[j]):
                        end = j
                        break
                block = lines[start:end]
                tmp_in = os.path.join(dst_dir, "_tmp_section.rpy")
                n, r = rewrite_rpy_lines(block, by_file[cf], tmp_in)
                new_block = open(tmp_in, encoding="utf-8").read().split("\n")
                out_lines[start:end] = new_block
                total_say += n
                total_zh += r
                print(f"  {rpy_rel}[{section}]: {r}/{n} lines chinese")
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "w", encoding="utf-8", newline="\n") as f:
                f.write("\n".join(out_lines))
    print(f"TOTAL: {total_zh}/{total_say} lines chinese ({100.0*total_zh/max(1,total_say):.1f}%)")


def rewrite_rpy_lines(lines, corpus_for_file, dst_path):
    """Same as rewrite_rpy but works on a line list (no voice file context)."""
    says = list(iter_says(lines))
    pairs = align2(says, corpus_for_file)
    zh_of = {}
    for i, j in pairs.items():
        zh = corpus_for_file[j]["zh"]
        if zh is not None and str(zh).strip():
            zh_of[i] = str(zh)
    out = []
    si = 0
    for line in lines:
        m = DLG.match(line)
        if m:
            text = unescape_rpy(m.group(3))
            if text.strip() == "{nw}":
                out.append(line)
                continue
            zh = zh_of.get(si)
            out.append(f'{m.group(1)}{m.group(2)} "{escape_rpy(zh)}"' if zh else line)
            si += 1
            continue
        out.append(line)
    with open(dst_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out))
    return len(says), sum(1 for i in zh_of if i < len(says))


if __name__ == "__main__":
    main()
