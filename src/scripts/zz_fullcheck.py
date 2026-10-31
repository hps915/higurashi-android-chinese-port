# -*- coding: utf-8 -*-
"""全篇完整性核查（只读，不做修改）。

对指定工程执行以下检查并出总表：
  1) label 定义数 / call-jump 目标缺失
  2) 未知文本标签
  3) show/scene 图像可解析（严格前缀元组匹配）
  4) 音频引用（voice + play/queue）存在性
  5) 未翻译 say 行
  6) 括号码配平 / 续行缩进
  7) 存档名 __() 覆盖率
  8) zz_common 条目里 new 仍含英文

用法: python zz_fullcheck.py
"""
import io
import os
import re
import sys

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PROJECTS = [
    ("出题篇", os.path.join(BASE, "work", "project", "game")),
    ("解题篇", os.path.join(BASE, "work", "project_k", "game")),
]

CJK = re.compile(u'[\u3000-\u303f\u3040-\u30ff\u4e00-\u9fff\uff00-\uffef]')
TAG = re.compile(r'\{([^{}]*)\}')
RUNTIME_TAGS = {
    "_start", "_end", "p", "space", "vspace", "w", "fast", "nw", "a",
    "b", "i", "u", "s", "plain", "", "font", "size", "color",
    "outlinecolor", "alpha", "k", "rt", "art", "rb", "cps", "vert",
    "horiz", "image",
}
EXTRA_TAGS = {"vw"}
KEYWORDS = {
    "voice", "play", "stop", "queue", "show", "scene", "hide", "jump",
    "call", "label", "image", "with", "pause", "window", "nvl", "menu",
    "if", "elif", "else", "return", "pass", "python", "default", "define",
    "extend", "translate", "old", "new", "style", "text", "textbutton",
    "init", "screen", "use", "for", "while", "include", "options",
    "adv_extend", "nvl_extend",
}
LABEL = re.compile(r'^[ \t]*label\s+([A-Za-z_][\w.]*)', re.M)
CALL = re.compile(r'^\s*(?:call|jump)\s+([A-Za-z_][\w.]*)', re.M)
SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*$')
IMG_DEF = re.compile(r'^\s*image\s+([A-Za-z0-9_]+(?:\s+[A-Za-z0-9_]+)*)\s*[:=]', re.M)
RENPY_IMAGE = re.compile(r"renpy\.image\(\s*['\"]([^'\"]+)['\"]")
SHOW = re.compile(r'^\s*(?:show|scene)\s+([A-Za-z0-9_]+(?:\s+[A-Za-z0-9_]+)*)')
VOICE = re.compile(r'^\s*voice\s+(?:sustain\s+)?"([^"]+)"', re.M)
PLAY = re.compile(r'^\s*(?:play|queue)\s+\w+\s+"([^"]+)"', re.M)
SKIP_TAGS = {"expression", "screen", "layer", "text", "vtext", "imagemap",
             "solid", "null", "frame", "window", "grid", "vbox", "hbox",
             "fixed", "side", "transform", "aspect"}
RES_PATH = re.compile(r'^(efe|sound|tips|music|voice|background|characters|cg|movie|text|save|images)/', re.I)
OLD_RE = re.compile(r'^\s*old "((?:[^"\\]|\\.)*)"', re.M)
PAIR = re.compile(r'(?m)^\s*old "((?:[^"\\]|\\.)*)"\s*\n\s*new "((?:[^"\\]|\\.)*)"')
WORD = re.compile(r'[A-Za-z]{2,}')


def iter_rpy(game_dir):
    for root, dirs, files in os.walk(game_dir):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in sorted(files):
            if f.endswith(".rpy"):
                p = os.path.join(root, f)
                rel = os.path.relpath(p, game_dir).replace("\\", "/")
                yield rel, p


def read(p):
    return io.open(p, encoding="utf-8", errors="replace").read()


def check(game_dir):
    r = {}
    labels = set()
    calls = []
    unknown_tags = {}
    imgs = set()
    unresolved = {}
    missing_audio = {}
    untrans = {}
    odd_quote = 0
    bad_indent = 0
    last_label = None

    for rel, p in iter_rpy(game_dir):
        t = read(p)
        for m in LABEL.finditer(t):
            labels.add(m.group(1))
        for m in CALL.finditer(t):
            line_start = t.rfind("\n", 0, m.start()) + 1
            if t[line_start:m.start() + 40].lstrip().startswith("call screen"):
                continue
            calls.append((rel, t[:m.start()].count("\n") + 1, m.group(1)))
        for m in IMG_DEF.finditer(t):
            imgs.add(tuple(m.group(1).split()))
        for m in RENPY_IMAGE.finditer(t):
            imgs.add(tuple(m.group(1).split()))
        for i, line in enumerate(t.split("\n"), 1):
            s = line.rstrip()
            if s.count('"') % 2:
                # 粗略：非转义引号数为奇
                cnt = 0
                k = 0
                while k < len(s):
                    if s[k] == "\\":
                        k += 2
                        continue
                    if s[k] == '"':
                        cnt += 1
                    k += 1
                if cnt % 2:
                    odd_quote += 1
            st = s.lstrip()
            if st.startswith(("extend \"", "adv_extend \"", "nvl_extend \"")):
                ind = len(s) - len(st)
                if ind % 4:
                    bad_indent += 1

    # show/scene
    for rel, p in iter_rpy(game_dir):
        t = read(p)
        for i, line in enumerate(t.split("\n"), 1):
            m = SHOW.match(line.rstrip())
            if not m:
                continue
            parts = m.group(1).split()
            if parts[0] in SKIP_TAGS:
                continue
            hit = any(tuple(parts[:k]) in imgs for k in range(len(parts), 0, -1))
            if not hit:
                unresolved.setdefault(parts[0], []).append("%s:%d" % (rel, i))

    # tags
    for rel, p in iter_rpy(game_dir):
        t = read(p)
        for i, line in enumerate(t.split("\n"), 1):
            m = SAY.match(line.rstrip())
            if not m:
                continue
            body = m.group(3).replace("{{", "\x01").replace("}}", "\x02")
            for tm in TAG.finditer(body):
                tag = tm.group(1).partition("=")[0].strip()
                if tag.startswith("/") or tag.startswith("#"):
                    continue
                if tag in RUNTIME_TAGS or tag in EXTRA_TAGS:
                    continue
                unknown_tags.setdefault(tag, []).append("%s:%d" % (rel, i))

    # audio
    for rel, p in iter_rpy(game_dir):
        t = read(p)
        for rx in (VOICE, PLAY):
            for m in rx.finditer(t):
                v = m.group(1)
                if not (v.startswith("voice/") and os.path.splitext(v)[1]):
                    continue
                if not os.path.exists(os.path.join(game_dir, *v.split("/"))):
                    ln = t[:m.start()].count("\n") + 1
                    missing_audio.setdefault(v, []).append("%s:%d" % (rel, ln))

    # untranslated
    for rel, p in iter_rpy(game_dir):
        t = read(p)
        for i, line in enumerate(t.split("\n"), 1):
            m = SAY.match(line.rstrip())
            if not m:
                continue
            ident = (m.group(2) or "").strip()
            if ident and ident.strip() in KEYWORDS:
                continue
            body = m.group(3)
            if CJK.search(body):
                continue
            plain = TAG.sub("", body).strip()
            if not plain or RES_PATH.match(plain):
                continue
            if re.search(r'\.(png|jpe?g|webp|ogg|mp3|wav|ogv|mp4|ttf|otf)$', plain, re.I):
                continue
            if len(re.sub(r'[^A-Za-z0-9]', "", plain)) >= 12:
                untrans.setdefault(rel, []).append((i, plain[:100]))

    # save_name
    save_total = save_wrapped = 0
    for rel, p in iter_rpy(game_dir):
        t = read(p)
        for m in re.finditer(r'^\s*\$ save_name = (.+)$', t, re.M):
            save_total += 1
            if m.group(1).strip().startswith('__("'):
                save_wrapped += 1

    # zz_common English
    tl_dir = os.path.join(game_dir, "tl", "schinese")
    common_en = []
    if os.path.isdir(tl_dir):
        for f in os.listdir(tl_dir):
            if not f.endswith(".rpy"):
                continue
            t = read(os.path.join(tl_dir, f))
            for m in PAIR.finditer(t):
                if WORD.search(m.group(2)):
                    common_en.append((f, m.group(1)[:60], m.group(2)[:60]))

    r["labels"] = len(labels)
    r["call_missing"] = [c for c in calls if c[2] not in labels]
    r["unknown_tags"] = unknown_tags
    r["unresolved_img"] = unresolved
    r["missing_audio"] = missing_audio
    r["untrans"] = untrans
    r["odd_quote"] = odd_quote
    r["bad_indent"] = bad_indent
    r["save_total"] = save_total
    r["save_wrapped"] = save_wrapped
    r["common_en"] = common_en
    return r


def main():
    for label, gd in PROJECTS:
        print("=" * 94)
        print("### %s   %s" % (label, gd))
        r = check(gd)
        print("  label 定义: %d    call/jump 目标缺失: %d" % (r["labels"], len(r["call_missing"])))
        for c in r["call_missing"][:10]:
            print("      MISS %s" % (c,))
        print("  未知文本标签: %d 种" % len(r["unknown_tags"]))
        for k, v in list(r["unknown_tags"].items())[:10]:
            print("      {%s} x%d  %s" % (k, len(v), v[0]))
        print("  show/scene 无法解析: %d 种" % len(r["unresolved_img"]))
        for k, v in list(r["unresolved_img"].items())[:10]:
            print("      %-20s x%-4d %s" % (k, len(v), v[0]))
        print("  语音/音频缺失: %d 种" % len(r["missing_audio"]))
        for k, v in list(r["missing_audio"].items())[:8]:
            print("      %-56s x%d" % (k, len(v)))
        n_un = sum(len(v) for v in r["untrans"].values())
        print("  未翻译 say 行: %d" % n_un)
        for k, v in list(r["untrans"].items())[:8]:
            print("      %-34s %d" % (k, len(v)))
        print("  引号奇数行: %d    续行缩进异常: %d" % (r["odd_quote"], r["bad_indent"]))
        print("  save_name: %d 条，已 __() 包裹 %d" % (r["save_total"], r["save_wrapped"]))
        print("  tl 里 new 仍含英文: %d" % len(r["common_en"]))
        for x in r["common_en"][:6]:
            print("      %s  OLD=%s  NEW=%s" % x)
        print()


if __name__ == "__main__":
    main()
