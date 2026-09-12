"""오하리상점 워드마크 SVG 생성 (잉크/화이트).

입력: _wordmark_parts.json (gen_lockup_parts.py 산출)
출력: logo-wordmark-{ko,en,ohari}-{ink,white}.svg
  ko    오하리상점
  en    OHARISTORE
  ohari OHARI  (시그니처 로고 = 거북이 + OHARI 세로 락업에 쓰는 짧은 영문)
시그니처 로고 SVG는 비율 확정 후 별도로 생성한다.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
parts = json.loads((ROOT / "_wordmark_parts.json").read_text(encoding="utf-8"))
INK, WHITE = "#262320", "#FFFFFF"
LABEL = {"ko": "오하리상점", "en": "OHARISTORE", "ohari": "OHARI"}

SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
       'fill="{fill}" fill-rule="evenodd" role="img" aria-label="{label}">'
       '<title>{label}</title><path d="{d}"/></svg>')

for key, label in LABEL.items():
    p = parts[key]
    for tone, fill in (("ink", INK), ("white", WHITE)):
        out = ROOT / f"logo-wordmark-{key}-{tone}.svg"
        out.write_text(SVG.format(w=p["w"], h=p["h"], fill=fill, label=label, d=p["d"]),
                       encoding="utf-8")
        print(out.name, p["w"], "x", p["h"])
