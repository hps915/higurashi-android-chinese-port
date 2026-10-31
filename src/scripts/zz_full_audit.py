# -*- coding: utf-8 -*-
"""全面静态审计（无 GUI）。

检查项：
 A) APK 内的 .rpyc 是否与工程目录一致（按 CRC 对比）
 B) 未知文本标签（会 raise Unknown text tag）
 C) show/scene 引用的图像是否可解析（tags + 属性）
 D) 音频文件引用是否真实存在
 E) voice 引用是否存在的统计
"""
import io
import os
import re
import struct
import sys
import zipfile
import zlib

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PROJECTS = [
    ("出题篇", os.path.join(BASE, "work", "project", "game"),
     os.path.join(BASE, "寒蝉鸣泣之时-出题篇-安卓中文版.apk")),
    ("解题篇", os.path.join(BASE, "work", "project_k", "game"),
     os.path.join(BASE, "寒蝉鸣泣之时-解题篇-安卓中文版.apk")),
]

# Ren'Py 7.3.5 text.py 字面支持的标签
RUNTIME_TAGS = {
    "_start", "_end", "p", "space", "vspace", "w", "fast", "nw", "a",
    "b", "i", "u", "s", "plain", "", "font", "size", "color",
    "outlinecolor", "alpha", "k", "rt", "art", "rb", "cps", "vert",
    "horiz", "image",
}
# 工程内额外注册的
EXTRA_TAGS = {"vw"}


def to_apk_name(rel):
    parts = ["assets", "x-game"] + [("x-" + p) for p in rel.replace("\\", "/").split("/")]
    return "/".join(parts)


def check_apk_sync(label, game_dir, apk):
    print("[A] APK 内容同步校验 - %s" % label)
    if not os.path.exists(apk):
        print("    APK 不存在:", apk)
        return
    z = zipfile.ZipFile(apk)
    infos = {i.filename: i for i in z.infolist()}
    missing = []
    mismatch = []
    n = 0
    for root, dirs, files in os.walk(game_dir):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in files:
            if not f.endswith(".rpyc"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, game_dir).replace("\\", "/")
            name = to_apk_name(rel)
            n += 1
            if name not in infos:
                missing.append(rel)
                continue
            content = io.open(p, "rb").read()
            crc = zlib.crc32(content) & 0xFFFFFFFF
            if crc != infos[name].CRC:
                mismatch.append((rel, len(content), infos[name].file_size))
    print("    工程内 .rpyc:", n, " 包内缺失:", len(missing), " CRC 不一致:", len(mismatch))
    for m in missing[:12]:
        print("      MISSING", m)
    for m in mismatch[:12]:
        print("      DIFF", m)
    # 反向：包里有哪些 rpyc 是工程里没有的（残留）
    proj_names = set()
    for root, dirs, files in os.walk(game_dir):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in files:
            if f.endswith(".rpyc"):
                rel = os.path.relpath(os.path.join(root, f), game_dir).replace("\\", "/")
                proj_names.add(to_apk_name(rel))
    extra = [nm for nm in infos
             if nm.startswith("assets/x-game/") and nm.endswith(".rpyc") and nm not in proj_names]
    print("    包内多余 .rpyc:", len(extra))
    for e in extra[:12]:
        print("      EXTRA", e)
    z.close()


TAG_RE = re.compile(r'\{([^{}]*)\}')
SAY = re.compile(r'^(\s*)((?:[A-Za-z_]\w*)\s+|adv_extend\s+|extend\s+|nvl_extend\s+)?'
                 r'"((?:[^"\\]|\\.)*)"\s*$')


def check_text_tags(label, game_dir):
    print("[B] 未知文本标签 - %s" % label)
    bad = {}
    for root, dirs, files in os.walk(game_dir):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in sorted(files):
            if not f.endswith(".rpy"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, game_dir).replace("\\", "/")
            for i, line in enumerate(io.open(p, encoding="utf-8", errors="replace"), 1):
                m = SAY.match(line.rstrip())
                if not m:
                    continue
                body = m.group(3).replace("{{", "\x01").replace("}}", "\x02")
                for tm in TAG_RE.finditer(body):
                    raw = tm.group(1)
                    tag = raw.partition("=")[0].strip()
                    if tag.startswith("/") or tag.startswith("#"):
                        continue
                    if tag in RUNTIME_TAGS or tag in EXTRA_TAGS:
                        continue
                    bad.setdefault(tag, []).append("%s:%d" % (rel, i))
    if not bad:
        print("    无未知标签")
    for tag, locs in sorted(bad.items(), key=lambda kv: -len(kv[1])):
        print("    {%s} x%d  %s" % (tag, len(locs), locs[0]))
        for l in locs[:4]:
            print("        ", l)


IMG_DEF_CMD = re.compile(r'^\s*image\s+([^\s=]+(?:\s+[^\s=]+)*)\s*=')
RENPY_IMAGE = re.compile(r"renpy\.image\(\s*['\"]([^'\"]+)['\"]")
SHOW_CMD = re.compile(r'^\s*(show|scene)\s+([A-Za-z_][\w]*(?:\s+[^\s{]+)*)')


def collect_images(game_dir):
    """收集所有已定义的 image 名字（字面字符串集合）。"""
    names = set()
    for root, dirs, files in os.walk(game_dir):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in files:
            if not f.endswith(".rpy"):
                continue
            p = os.path.join(root, f)
            for line in io.open(p, encoding="utf-8", errors="replace"):
                s = line.rstrip()
                m = IMG_DEF_CMD.match(s)
                if m:
                    names.add(" ".join(m.group(1).split()))
                m2 = RENPY_IMAGE.search(s)
                if m2:
                    names.add(" ".join(m2.group(1).split()))
    return names


def check_images(label, game_dir):
    print("[C] show/scene 图像可解析性 - %s" % label)
    defined = collect_images(game_dir)
    # 建立 tag -> 属性集合
    by_tag = {}
    for nm in defined:
        parts = nm.split()
        by_tag.setdefault(parts[0], set()).add(" ".join(parts[1:]))
    missing = {}
    for root, dirs, files in os.walk(game_dir):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in sorted(files):
            if not f.endswith(".rpy"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, game_dir).replace("\\", "/")
            for i, line in enumerate(io.open(p, encoding="utf-8", errors="replace"), 1):
                m = SHOW_CMD.match(line.rstrip())
                if not m:
                    continue
                rest = m.group(2)
                # 去掉 ATL / 参数
                name = " ".join(rest.split())
                if name in ("black", "white", "text", "centered", "vcentered"):
                    pass
                parts = name.split()
                tag = parts[0]
                if tag in ("expression", "screen", "layer"):
                    continue
                if tag not in by_tag:
                    missing.setdefault(tag, []).append("%s:%d  %s" % (rel, i, name))
                    continue
                attrs = parts[1:]
                if not attrs:
                    continue
                known = by_tag[tag]
                # 1) 完整名直接命中
                cand = " ".join(attrs)
                if cand in known or "" in known:
                    continue
                # 2) 属性逐级尝试：Ren'Py 里 `show rena 1a warai_a1_ at ...`
                #    的 attrs 会先整体匹配，匹配不到再按 tag+attrs 前缀匹配。
                #    这里用「已定义图像的属性序列是否以 attrs 为前缀 / attrs 是否为其子集」放宽。
                aset = set(attrs)
                ok = False
                for k in known:
                    kp = k.split()
                    if not kp:
                        continue
                    if [a for a in attrs if a in kp] and aset <= set(kp):
                        ok = True
                        break
                    # 允许 attrs 中混入 `portrait` / `night` 这类修饰符
                    base = [a for a in attrs if a not in ("portrait", "night", "dusk", "sunset",
                                                          "sepia", "inverse", "real", "gray", "night_rain")]
                    if base and set(base) <= set(kp):
                        ok = True
                        break
                if not ok:
                    missing.setdefault(tag + " (attr)", []).append("%s:%d  %s" % (rel, i, name))
    if not missing:
        print("    全部可解析")
    for k, locs in sorted(missing.items(), key=lambda kv: -len(kv[1])):
        print("    %-26s x%-4d %s" % (k, len(locs), locs[0][:110]))
        for l in locs[1:4]:
            print("                              ", l[:110])


AUDIO_REF = re.compile(r'^\s*(?:play|queue|stop)\s+(?:\w+\s+)?"([^"]+)"')
VOICE_REF = re.compile(r'^\s*voice\s+"([^"]+)"')


def check_audio(label, game_dir):
    print("[D] 音频引用存在性 - %s" % label)
    named_audio = set()
    # 收集 audio 定义（脚本里 define/audio 目录外的具名音频）
    audio_dirs = ("music", "sound", "voice", "audio")
    miss_audio = {}
    miss_voice = {}
    for root, dirs, files in os.walk(game_dir):
        dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
        for f in sorted(files):
            if not f.endswith(".rpy"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, game_dir).replace("\\", "/")
            for i, line in enumerate(io.open(p, encoding="utf-8", errors="replace"), 1):
                for rx, bucket in ((AUDIO_REF, miss_audio), (VOICE_REF, miss_voice)):
                    m = rx.match(line.rstrip())
                    if not m:
                        continue
                    val = m.group(1)
                    if not val or val.startswith("<") or "%" in val:
                        continue
                    if not os.path.splitext(val)[1]:
                        continue  # 具名 audio，跳过
                    fp = os.path.join(game_dir, val.replace("/", os.sep))
                    if not os.path.exists(fp):
                        bucket.setdefault(val, []).append("%s:%d" % (rel, i))
    for name, bucket in (("play/queue/stop", miss_audio), ("voice", miss_voice)):
        tot = sum(len(v) for v in bucket.values())
        print("    %-16s 缺失种类 %d / 引用 %d" % (name, len(bucket), tot))
        for k, locs in list(sorted(bucket.items(), key=lambda kv: -len(kv[1])))[:8]:
            print("      %-60s x%d  %s" % (k, len(locs), locs[0]))


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for label, game_dir, apk in PROJECTS:
        print("=" * 96)
        print("###", label)
        if which in ("all", "a"):
            check_apk_sync(label, game_dir, apk)
        if which in ("all", "b"):
            check_text_tags(label, game_dir)
        if which in ("all", "c"):
            check_images(label, game_dir)
        if which in ("all", "d"):
            check_audio(label, game_dir)
        print()


if __name__ == "__main__":
    main()
