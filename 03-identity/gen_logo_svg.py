"""오하리상점 손글씨 로고 PNG -> 벡터 SVG (potracer).

입력: assets/logo-source.png (원본 손글씨 스캔)
출력: logo-wordmark-{ink,white}.svg, logo-wordmark.svg (currentColor)
재현: python 03-identity/gen_logo_svg.py
"""
from pathlib import Path
import numpy as np
from PIL import Image
import potrace

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "assets" / "logo-source.png"
INK = "#262320"
SCALE = 2          # 트레이싱 전 업스케일 (곡선 부드럽게)
PAD = 8            # 잉크 바운딩박스 여백 (업스케일 기준 px)

img = Image.open(SRC).convert("L")
arr = np.array(img.resize((img.width * SCALE, img.height * SCALE), Image.LANCZOS))
ink = arr < 128

ys, xs = np.nonzero(ink)
ink = ink[ys.min() - PAD:ys.max() + PAD + 1, xs.min() - PAD:xs.max() + PAD + 1]
H, W = ink.shape

# potracer는 False 영역을 채워진 것으로 본다 -> 반전해서 넘긴다
path = potrace.Bitmap(np.logical_not(ink)).trace(
    turdsize=8, alphamax=1.0, opticurve=True, opttolerance=0.2
)

d = []
for curve in path:
    s = curve.start_point
    d.append(f"M{s.x:.2f},{s.y:.2f}")
    for seg in curve:
        e = seg.end_point
        if seg.is_corner:
            d.append(f"L{seg.c.x:.2f},{seg.c.y:.2f}L{e.x:.2f},{e.y:.2f}")
        else:
            d.append(
                f"C{seg.c1.x:.2f},{seg.c1.y:.2f} {seg.c2.x:.2f},{seg.c2.y:.2f} {e.x:.2f},{e.y:.2f}"
            )
    d.append("Z")
dd = "".join(d)

tpl = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
    'width="{w}" height="{h}" role="img" aria-label="오하리상점 OHARI STORE">'
    '<path fill="{fill}" fill-rule="evenodd" d="{d}"/></svg>'
)
for name, fill in (("logo-wordmark.svg", "currentColor"),
                   ("logo-wordmark-ink.svg", INK),
                   ("logo-wordmark-white.svg", "#FFFFFF")):
    out = ROOT / name
    out.write_text(tpl.format(w=W, h=H, fill=fill, d=dd), encoding="utf-8")
    print(out, out.stat().st_size, f"{W}x{H}")
