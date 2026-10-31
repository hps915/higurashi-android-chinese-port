# -*- coding: utf-8 -*-
"""Apply subagent translations (trans_out_*.json) to project .rpy files.

Each entry: {file, line, zh}. The line must still be an untranslated say
line (no CJK); only the quoted text is replaced, any `with ...` suffix kept.
"""
import json
import os
import re
import sys

WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CJK = re.compile(r'[\u4e00-\u9fff]')
SAY = re.compile(r'^(\s*[\w.]+\s+")((?:[^"\\]|\\.)*)(")(.*)$')


def apply_batch(out_json, proj):
    data = json.load(open(out_json, encoding="utf-8"))
    by_file = {}
    for e in data:
        by_file.setdefault(e["file"], []).append(e)
    ok = skip_cn = miss = empty = 0
    for rel, entries in by_file.items():
        p = os.path.join(WORK, proj, "game", rel.replace("/", os.sep))
        if not os.path.exists(p):
            print(f"  !! missing file {rel}")
            miss += len(entries)
            continue
        lines = open(p, encoding="utf-8").read().split("\n")
        changed = False
        for e in entries:
            ln = e["line"]
            zh = (e.get("zh") or "").strip()
            if not zh:
                empty += 1
                continue
            if ln - 1 >= len(lines):
                miss += 1
                continue
            cur = lines[ln - 1]
            if CJK.search(cur):
                skip_cn += 1  # already chinese (drift); leave
                continue
            m = SAY.match(cur)
            if not m:
                miss += 1
                continue
            esc = zh.replace('"', '\\"')
            lines[ln - 1] = m.group(1) + esc + m.group(3) + (m.group(4) or "")
            changed = True
            ok += 1
        if changed:
            open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print(f"{os.path.basename(out_json)}: applied={ok} empty-skip={empty} already-zh={skip_cn} missed={miss}")


def main():
    for out, proj in (("trans_out_project_1.json", "project"),
                      ("trans_out_project_2.json", "project"),
                      ("trans_out_project_k_1.json", "project_k"),
                      ("trans_out_project_k_2.json", "project_k")):
        p = os.path.join(WORK, out)
        if os.path.exists(p):
            apply_batch(p, proj)
        else:
            print(f"!! {out} not found yet")


if __name__ == "__main__":
    main()
