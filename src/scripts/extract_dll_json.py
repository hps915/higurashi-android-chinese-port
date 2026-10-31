# -*- coding: utf-8 -*-
"""Extract the ycx-embedded Chinese tips.json and BGM-info JSON blobs from
each chapter's Assembly-CSharp.dll. Saves work/corpus/tips_zh.json and
work/corpus/bgm_zh.json."""
import json
import os

GAME_ROOT = r"D:\Galgame\寒蝉鸣泣之时"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "corpus")
CHAPTERS = {1: "寒蝉鸣泣之时：1鬼隐篇", 2: "寒蝉鸣泣之时：2绵流篇", 3: "寒蝉鸣泣之时：3祟杀篇",
            4: "寒蝉鸣泣之时：4暇溃篇", 5: "寒蝉鸣泣之时：5目明篇", 6: "寒蝉鸣泣之时：6罪灭篇",
            7: "寒蝉鸣泣之时：7皆杀篇", 8: "寒蝉鸣泣之时：8祭囃篇"}


def json_span(data, start):
    """Return end index (exclusive) of the JSON value starting at `start`."""
    depth = 0
    instr = False
    esc = False
    for j in range(start, min(start + 400000, len(data))):
        c = data[j]
        if esc:
            esc = False
            continue
        if c == 0x5C:  # backslash
            esc = True
            continue
        if c == 0x22:  # quote
            instr = not instr
            continue
        if instr:
            continue
        if c == 0x7B or c == 0x5B:  # { [
            depth += 1
        elif c == 0x7D or c == 0x5D:  # } ]
            depth -= 1
            if depth == 0:
                return j + 1
    return None


def main():
    tips_out = {}
    bgm_out = {}
    for ch, dname in CHAPTERS.items():
        dll = os.path.join(GAME_ROOT, dname, f"HigurashiEp0{ch}_Data",
                           "Managed", "Assembly-CSharp.dll")
        if not os.path.exists(dll):
            print(f"ch{ch}: no dll")
            continue
        data = open(dll, "rb").read()
        # tips blob
        i = data.find(b'{\r\n\t"0": [')
        if i >= 0:
            end = json_span(data, i)
            try:
                tips_out[ch] = json.loads(data[i:end].decode("utf-8"))["0"]
                print(f"ch{ch}: tips {len(tips_out[ch])} first={tips_out[ch][0]['Title']!r}")
            except Exception as e:
                print(f"ch{ch}: tips parse fail {e}")
        else:
            print(f"ch{ch}: no tips blob")
        # bgm blob: 2-space-indented json preceding the tips blob
        bgm_i = data.rfind(b'{\r\n  "', 0, i if i >= 0 else len(data))
        if bgm_i < 0:
            # try alternate indent
            bgm_i = data.rfind(b'{\r\n"', 0, i if i >= 0 else len(data))
        if bgm_i >= 0:
            end = json_span(data, bgm_i)
            try:
                bgm = json.loads(data[bgm_i:end].decode("utf-8"))
                # normalize: keep {track: name} for the main list
                names = {}
                for k, v in bgm.items():
                    if isinstance(v, dict):
                        for tk, tv in v.items():
                            if isinstance(tv, dict) and tv.get("name"):
                                names[tk] = tv["name"]
                    elif isinstance(v, str):
                        names[k] = v
                bgm_out[ch] = names
                print(f"ch{ch}: bgm {len(names)} names, e.g. {list(names.items())[:2]}")
            except Exception as e:
                print(f"ch{ch}: bgm parse fail {e}")
    json.dump(tips_out, open(os.path.join(OUT, "tips_zh.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    json.dump(bgm_out, open(os.path.join(OUT, "bgm_zh.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("saved", os.path.join(OUT, "tips_zh.json"), "and bgm_zh.json")


if __name__ == "__main__":
    main()
