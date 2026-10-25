# -*- coding: utf-8 -*-
"""케어 아이콘 추가분 — 오븐 사용 가능 / 오븐 사용 금지 (2026-10-25)
gen_v3.py의 열 분할 + potrace 곡선 파이프라인을 그대로 재사용한다.
원본: Downloads/오븐과 금지 표시 아이콘_d.png (가로 2열)
"""
import io, os, json
from xml.sax.saxutils import escape
from gen_v3 import load, clean, split_cols, trace, DL, OUT
from vectorize import TPL

SHEET = ("오븐과 금지 표시 아이콘_d.png", [("care-oven", "오븐 사용 가능"), ("care-no-oven", "오븐 사용 금지")])

if __name__ == "__main__":
    fn, names = SHEET
    ink, blue = load(os.path.join(DL, fn)); ink = clean(ink)
    mp = os.path.join(OUT, "manifest.json")
    manifest = json.load(io.open(mp, encoding="utf-8")) if os.path.exists(mp) else {}
    for sub, (slug, ko) in zip(split_cols(ink, len(names)), names):
        io.open(os.path.join(OUT, slug + ".svg"), "w", encoding="utf-8").write(TPL.format(t=escape(ko), d=trace(sub)))
        manifest[slug] = {"src": fn, "title": ko, "crossed_out": False, "parts": []}
        print("%-16s %s" % (slug, sub.shape))
    json.dump(manifest, io.open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
