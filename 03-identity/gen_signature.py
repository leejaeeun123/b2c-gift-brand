"""시그니처 로고 SVG 생성 — 거북이(심볼) + OHARI(손글씨 영문) 세로 락업.

확정값 (2026-09-13)
  거북이 폭 = 워드마크 잉크 폭의 95%
  간격      = 거북이 잉크 높이의 24%  (거북이 SVG 박스 여백 제외한 옵티컬 기준)
  정렬      = 잉크 바운딩박스 가운데
출력: logo-signature-{ink,white}.svg
"""
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parent
parts = json.loads((ROOT / "_wordmark_parts.json").read_text(encoding="utf-8"))
turtle_d = re.search(r'd="([^"]+)"', (ROOT / "char-turtle.svg").read_text(encoding="utf-8")).group(1)

TX0, TX1, TY0, TY1 = 6.94, 92.79, 24.99, 74.74   # 거북이 잉크 바운딩박스
TIW, TIH = TX1 - TX0, TY1 - TY0
PAD = 12                                          # 워드마크 트레이싱 여백
TURTLE_W, GAP = 0.95, 0.24
INK, WHITE = "#262320", "#FFFFFF"
LABEL = "오하리상점 OHARI"


def body_and_box(key="ohari"):
    p = parts[key]
    ww, wh = p["w"] - PAD * 2, p["h"] - PAD * 2
    s = ww * TURTLE_W / TIW
    tw, th = TIW * s, TIH * s
    g = th * GAP
    W, H = ww, th + g + wh
    tx, ty = (ww - tw) / 2 - TX0 * s, -TY0 * s
    body = (f'<g transform="translate({tx:.2f},{ty:.2f}) scale({s:.4f})"><path d="{turtle_d}"/></g>'
            f'<g transform="translate({-PAD},{th + g - PAD:.2f})"><path d="{p["d"]}"/></g>')
    return body, W, H


SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
       'width="{w:.0f}" height="{h:.0f}" fill="{fill}" fill-rule="evenodd" '
       f'role="img" aria-label="{LABEL}"><title>{LABEL}</title>{{body}}</svg>')

body, W, H = body_and_box()
for tone, fill in (("ink", INK), ("white", WHITE)):
    out = ROOT / f"logo-signature-{tone}.svg"
    out.write_text(SVG.format(w=W, h=H, fill=fill, body=body), encoding="utf-8")
    print(out.name, f"{W:.0f} x {H:.0f}")
