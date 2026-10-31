# -*- coding: utf-8 -*-
import json
corpus = json.load(open("../corpus/ch1.json", encoding="utf-8"))
zh_all = [str(e["zh"]) for e in corpus if e["zh"]]
issues = {"quote": 0, "backslash": 0, "brace": 0, "bracket": 0, "literal_n": 0}
samples = {}
BS = chr(92)
for z in zh_all:
    if '"' in z:
        issues["quote"] += 1
        samples.setdefault("quote", z)
    if BS in z:
        issues["backslash"] += 1
        samples.setdefault("backslash", z)
    if "{" in z or "}" in z:
        issues["brace"] += 1
        samples.setdefault("brace", z)
    if "[" in z or "]" in z:
        issues["bracket"] += 1
        samples.setdefault("bracket", z)
    if BS + "n" in z:
        issues["literal_n"] += 1
        samples.setdefault("literal_n", z)
print(issues)
for k, v in samples.items():
    print(k, "→", repr(v[:90]))
