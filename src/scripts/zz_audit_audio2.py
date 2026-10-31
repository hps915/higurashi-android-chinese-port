# -*- coding: utf-8 -*-
"""精确统计语音/音频缺失，并区分「源 APK 本来就缺」与「本轮引入」。

做法：对每个缺失路径，检查源 APK 解包目录里是否存在同名文件。
"""
import io
import os
import re
import sys

BASE = r"D:\Galgame\寒蝉鸣泣之时\安卓移植版1"
PROJECTS = [
    ("出题篇", os.path.join(BASE, "work", "project", "game"),
     os.path.join(BASE, "work", "apk_q", "assets", "x-game")),
    ("解题篇", os.path.join(BASE, "work", "project_k", "game"),
     os.path.join(BASE, "work", "apk_k", "assets", "x-game")),
]

PLAY = re.compile(r'^\s*(?:play|queue|stop)\s+(?:[\w]+\s+)?(?:"([^"]*)"|([a-z_]\w*))')
VOICE = re.compile(r'^\s*voice\s+(?:sustain\s+)?"([^"]*)"')


def xpath(rel):
    parts = rel.replace("\\", "/").split("/")
    return "/".join(["x-" + p for p in parts])


def main():
    for label, game_dir, apk_dir in PROJECTS:
        print("=" * 92)
        print("###", label)
        miss_notnamed = {}
        miss_named = {}
        miss_voice = {}
        for root, dirs, files in os.walk(game_dir):
            dirs[:] = [d for d in dirs if d not in ("cache", "saves")]
            for f in sorted(files):
                if not f.endswith(".rpy"):
                    continue
                p = os.path.join(root, f)
                rel = os.path.relpath(p, game_dir).replace("\\", "/")
                for i, line in enumerate(io.open(p, encoding="utf-8", errors="replace"), 1):
                    s = line.rstrip()
                    m = VOICE.match(s)
                    if m:
                        v = m.group(1)
                        if v and "<" not in v and "%" not in v:
                            if not os.path.exists(os.path.join(game_dir, v.replace("/", os.sep))):
                                miss_voice.setdefault(v, []).append("%s:%d" % (rel, i))
                    m = PLAY.match(s)
                    if m:
                        q, named = m.group(1), m.group(2)
                        if q:
                            if "<" in q or "%" in q or not q:
                                continue
                            if not os.path.splitext(q)[1]:
                                continue
                            if not os.path.exists(os.path.join(game_dir, q.replace("/", os.sep))):
                                miss_notnamed.setdefault(q, []).append("%s:%d" % (rel, i))

        def split_by_origin(bucket):
            in_src, not_in_src = {}, {}
            for k, locs in bucket.items():
                cand = os.path.join(apk_dir, xpath(k))
                if os.path.exists(cand):
                    in_src[k] = locs
                else:
                    not_in_src[k] = locs
            return in_src, not_in_src

        for nm, bucket in (("voice (voice \"...\")", miss_voice),
                           ("play/queue (带扩展名)", miss_notnamed)):
            ins, out = split_by_origin(bucket)
            tot = sum(len(v) for v in bucket.values())
            print("  %-26s 缺失种类 %-6d 引用 %-6d" % (nm, len(bucket), tot))
            print("     源 APK 里本来就没有（继承缺陷）: %d 种 / %d 处"
                  % (len(out), sum(len(v) for v in out.values())))
            print("     源 APK 里有但工程丢了（本轮问题）: %d 种 / %d 处"
                  % (len(ins), sum(len(v) for v in ins.values())))
            for k, locs in list(sorted(ins.items(), key=lambda kv: -len(kv[1])))[:10]:
                print("       LOST %-58s x%d  %s" % (k, len(locs), locs[0]))
        print()


if __name__ == "__main__":
    main()
