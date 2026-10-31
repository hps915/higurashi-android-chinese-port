# -*- coding: utf-8 -*-
"""Extract bilingual dialogue corpus from a Higurashi install (all 8 chapters).

  ch1   : EN .mg (CompiledUpdateScripts) + ZH .mg (CompiledChineseScripts), stock ops
  ch2-5,7: same, per-chapter opcode tables (from installed DLL enums)
  ch6   : EN .txt (07th-mod/tsumihoroboshi repo) + ZH .mg
  ch8   : ZH .txt (Update/*.txt, Chinese in arg4) + EN .txt (07th-mod/matsuribayashi repo)

Output per chapter: corpus/chN.json  {file, idx, line, jp, en, zh, voice, op}
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mgparse
from mgparse import load, set_opsig
from parse_txt import parse_file as parse_txt_file

STOCK_OPSIG = dict(mgparse.OPSIG)  # snapshot before any set_opsig swaps

GAME_ROOT = r"D:\Galgame\寒蝉鸣泣之时"
TOOLS = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1\tools"
OUTDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "corpus")

CHAPTERS = {
    1: "寒蝉鸣泣之时：1鬼隐篇", 2: "寒蝉鸣泣之时：2绵流篇", 3: "寒蝉鸣泣之时：3祟杀篇",
    4: "寒蝉鸣泣之时：4暇溃篇", 5: "寒蝉鸣泣之时：5目明篇", 6: "寒蝉鸣泣之时：6罪灭篇",
    7: "寒蝉鸣泣之时：7皆杀篇", 8: "寒蝉鸣泣之时：8祭囃篇",
}

EXTRA_SIGS = {
    "ActivateScreenEffectForcedly": "b", "ChangeBustshot": "isib", "DisplayWindow": "",
    "DrawFragment": "ssi", "SetColorOfMessage": "biii", "SetValidityOfLoading": "b",
    "StopFragment": "i", "Update": "", "GetRandomNumber": "i",
    "NullOp": "", "Return": "", "HideWindow": "", "RotateBG": "iiii",
}

VOICE_OPS = {"PlayVoice": 1, "ModPlayVoiceLS": 2}


def simplify_events(events):
    out = []
    pending_voice = None
    cur_line = -1
    for e in events:
        if e[0] == "linenum":
            cur_line = e[1]
            continue
        if e[0] != "op":
            out.append((e[0],))
            continue
        _, op, name, params = e
        if name in VOICE_OPS:
            fn = params[VOICE_OPS[name]]
            if isinstance(fn, str) and fn:
                pending_voice = fn
            out.append(("voice", fn))
            continue
        if name in ("OutputLine", "OutputLineAll"):
            if name == "OutputLine":
                jp, loc = params[1], params[3]
            else:
                jp, loc = params[1], None
            has_text = isinstance(jp, str) and jp.strip() not in ("", "\\n", "\\n\\n")
            entry = {"line": cur_line, "op": name,
                     "jp": jp if has_text else None,
                     "loc": loc if has_text else None,
                     "voice": pending_voice if has_text else None}
            if has_text:
                pending_voice = None
            out.append(("text", entry))
            continue
        out.append(("op", op))
    return out


def entries_from_mg(path):
    ev = simplify_events(load(path)["events"])
    out = []
    for kind, *rest in ev:
        if kind == "text" and rest[0]["jp"] is not None:
            out.append(rest[0])
    return out, ev


def skeleton_from_mg(path):
    _, ev = entries_from_mg(path)
    return ev


def txt_entries(path):
    out = []
    for e in parse_txt_file(path):
        out.append({"line": e["line"], "op": e["op"], "jp": e["jp"],
                    "loc": e["loc"], "voice": e["voice"]})
    return out


def merge_pair(en_list, zh_list, file, stats):
    """Pair EN and ZH entries by global alignment on the Japanese text."""
    import difflib
    keys_en = [e["jp"] for e in en_list]
    keys_zh = [e["jp"] for e in zh_list]
    sm = difflib.SequenceMatcher(None, keys_en, keys_zh, autojunk=False)
    corpus = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                en, zh = en_list[i1 + k], zh_list[j1 + k]
                zh_loc = zh["loc"] if zh["loc"] and str(zh["loc"]).strip() else en["loc"]
                if en.get("voice") != zh.get("voice"):
                    stats["voice_mismatch"] += 1
                corpus.append({"file": file, "line": en.get("line"), "jp": en["jp"],
                               "en": en["loc"], "zh": zh_loc, "voice": en.get("voice"),
                               "op": en["op"]})
        elif tag == "replace":
            n = min(i2 - i1, j2 - j1)
            stats["jp_mismatch"] += max(i2 - i1, j2 - j1) - n
            for k in range(n):
                en, zh = en_list[i1 + k], zh_list[j1 + k]
                zh_loc = zh["loc"] if zh["loc"] and str(zh["loc"]).strip() else en["loc"]
                corpus.append({"file": file, "line": en.get("line"), "jp": en["jp"],
                               "en": en["loc"], "zh": zh_loc, "voice": en.get("voice"),
                               "op": en["op"]})
        elif tag == "delete":
            stats["en_skip"] += i2 - i1
        elif tag == "insert":
            stats["zh_skip"] += j2 - j1
    return corpus


def load_perch_tables():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "opsig_perch.json")
    tables = json.load(open(p, encoding="utf-8"))
    out = {}
    for ch, tbl in tables.items():
        fixed = {}
        for v, (name, sig) in tbl.items():
            if sig == "?" or sig is None:
                sig = EXTRA_SIGS.get(name)
            fixed[int(v)] = (name, sig)
        out[int(ch)] = fixed
    return out


def extract_chapter(ch, perch):
    game_dir = os.path.join(GAME_ROOT, CHAPTERS[ch])
    sa = os.path.join(game_dir, f"HigurashiEp{ch:02d}_Data", "StreamingAssets")

    if ch == 8:
        zh_dir = os.path.join(sa, "Update")
        en_dir = os.path.join(TOOLS, "matsuribayashi", "Update")
    elif ch == 6:
        zh_dir = os.path.join(sa, "CompiledChineseScripts")
        en_dir = os.path.join(TOOLS, "tsumihoroboshi", "Update")
    else:
        zh_dir = os.path.join(sa, "CompiledChineseScripts")
        en_dir = os.path.join(sa, "CompiledUpdateScripts")

    def names(d, ext):
        try:
            return {f[:-len(ext)] for f in os.listdir(d) if f.endswith(ext)}
        except FileNotFoundError:
            return set()

    if ch == 8:
        en_names = names(en_dir, ".txt")
        zh_names = names(zh_dir, ".txt")
    elif ch == 6:
        en_names = names(en_dir, ".txt")
        zh_names = names(zh_dir, ".mg")
    else:
        en_names = names(en_dir, ".mg")
        zh_names = names(zh_dir, ".mg")
    common = sorted(en_names & zh_names)

    stats = {"files": len(common), "dialogue": 0, "jp_mismatch": 0, "voice_mismatch": 0,
             "en_skip": 0, "zh_skip": 0, "zh_empty": 0, "mg_fail": 0}
    mismatches = []
    corpus = []

    if ch in perch:
        set_opsig(perch[ch])
    else:
        set_opsig(STOCK_OPSIG)

    for name in common:
        if ch == 8:
            en_list = txt_entries(os.path.join(en_dir, name + ".txt"))
            zh_list = txt_entries(os.path.join(zh_dir, name + ".txt"))
        elif ch == 6:
            en_list = txt_entries(os.path.join(en_dir, name + ".txt"))
            try:
                zh_list, _ = entries_from_mg(os.path.join(zh_dir, name + ".mg"))
            except Exception as ex:
                stats["mg_fail"] += 1
                if len(mismatches) < 50:
                    mismatches.append({"file": name, "error": f"mg parse: {ex}"})
                continue
        else:
            try:
                en_list, _ = entries_from_mg(os.path.join(en_dir, name + ".mg"))
                zh_list, _ = entries_from_mg(os.path.join(zh_dir, name + ".mg"))
            except Exception as ex:
                stats["mg_fail"] += 1
                if len(mismatches) < 50:
                    mismatches.append({"file": name, "error": f"mg parse: {ex}"})
                continue
        c = merge_pair(en_list, zh_list, name, stats)
        corpus.extend(c)
        stats["dialogue"] += len(c)
        if len(en_list) != len(zh_list) and len(mismatches) < 50:
            mismatches.append({"file": name, "en": len(en_list), "zh": len(zh_list)})

    # restore stock table
    set_opsig(STOCK_OPSIG)
    return corpus, stats, mismatches


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    perch = load_perch_tables()
    chapters = [int(x) for x in sys.argv[1:]] or list(CHAPTERS)
    for ch in chapters:
        corpus, stats, mismatches = extract_chapter(ch, perch)
        with open(os.path.join(OUTDIR, f"ch{ch}.json"), "w", encoding="utf-8") as f:
            json.dump(corpus, f, ensure_ascii=False, indent=1)
        with open(os.path.join(OUTDIR, f"ch{ch}_report.json"), "w", encoding="utf-8") as f:
            json.dump({"stats": stats, "mismatches": mismatches[:100]}, f, ensure_ascii=False, indent=1)
        print(f"ch{ch}: files={stats['files']} dialogue={stats['dialogue']} "
              f"jp_mismatch={stats['jp_mismatch']} voice_mismatch={stats['voice_mismatch']} "
              f"en_skip={stats['en_skip']} zh_skip={stats['zh_skip']} mg_fail={stats['mg_fail']}")
        if mismatches:
            print("  sample issues:", mismatches[:3])


if __name__ == "__main__":
    main()
