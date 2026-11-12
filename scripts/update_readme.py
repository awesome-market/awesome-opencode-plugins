#!/usr/bin/env python3
"""Regenerate the Top-20 new-arrival tables in README.md / README.zh.md.

Reads the latest generated day file under site/data/days/, rebuilds the
markdown table between the <!-- BOARD:TOP20 --> markers in each README,
and writes the file only when the table changed. Pure stdlib.
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOP_N = 20

EN = dict(
    readme="README.md",
    quote="> Plugins listed in the last 90 days, ranked by current stars "
          "(≥10★). Full boards and history curves on the "
          '<a href="https://opencode-plugins.zhuikan.com">live site</a>.',
    header="| Plugin | Stars | Description |\n| :--- | ---: | :--- |",
    desc_key="en",
)
ZH = dict(
    readme="README.zh.md",
    quote="> 近 90 天内上架、按当前 Star 排序（≥10★）。完整榜单与历史曲线见"
          '<a href="https://opencode-plugins.zhuikan.com">在线榜单</a>。',
    header="| 插件 | Stars | 简介 |\n| :--- | ---: | :--- |",
    desc_key="zh",
)


def latest_rows():
    days = sorted(glob.glob(os.path.join(ROOT, "site/data/days/*.json")))
    if not days:
        raise SystemExit("no site/data/days/*.json — run rank.py first")
    d = json.load(open(days[-1]))
    board = d["boards"]["new"]
    return (board.get("items") or board.get("rows"))[:TOP_N]


def esc(t):
    return (t or "").replace("|", "\\|")


def trim(t, n=80):
    t = " ".join((t or "").split())
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"


def repo_meta(fn):
    fp = os.path.join(ROOT, "data/repos", fn.replace("/", "__") + ".json")
    if not os.path.exists(fp):
        return {}
    return json.load(open(fp))


def build_table(rows, cfg):
    out = [cfg["header"]]
    for r in rows:
        fn = r["full_name"]
        m = repo_meta(fn)
        dd = m.get("description") or ""
        desc = dd if isinstance(dd, str) else (dd.get(cfg["desc_key"])
                                               or dd.get("en") or dd.get("zh") or "")
        url = m.get("url") or ""
        link = f"[**{esc(fn)}**]({url})" if url else f"**{esc(fn)}**"
        out.append(f"| {link} | {r.get('stars', 0):,} | {esc(trim(desc))} |")
    return "\n".join(out)


def update(readme, block):
    path = os.path.join(ROOT, readme)
    text = open(path, encoding="utf-8").read()
    pat = re.compile(
        r"(<!-- BOARD:TOP20 -->).*?(<!-- /BOARD:TOP20 -->)", re.S)
    if not pat.search(text):
        print(f"skip {readme}: markers missing")
        return False
    new = pat.sub(lambda m: m.group(1) + "\n" + block + "\n" + m.group(2), text)
    if new == text:
        print(f"{readme}: up to date")
        return False
    open(path, "w", encoding="utf-8").write(new)
    print(f"{readme}: table refreshed")
    return True


def main():
    rows = latest_rows()
    n = 0
    for cfg in (EN, ZH):
        table = "\n".join([cfg["quote"], "", build_table(rows, cfg)])
        n += update(cfg["readme"], table)
    print(f"{n} file(s) updated")


if __name__ == "__main__":
    main()
