"""손글씨 스캔에서 구간별 워드마크 path 추출 (오하리상점 / OHARI).

gen_logo_svg.py와 같은 트레이싱 설정을 쓰되 x 구간만 잘라 쓴다.
컬럼 공백 기준 글리프 경계: 한글 199~721, OHARI 836~1159 (원본 px).
"""
from pathlib import Path
import json
import numpy as np
from PIL import Image
import potrace

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "assets" / "logo-source.png"
SCALE = 2
PAD = 6
PARTS = {"ko": (199, 721), "en": (836, 1481), "ohari": (836, 1159)}

img = Image.open(SRC).convert("L")
arr = np.array(img.resize((img.width * SCALE, img.height * SCALE), Image.LANCZOS))
full = arr < 128


def trace(mask):
    ys, xs = np.nonzero(mask)
    m = mask[ys.min() - PAD:ys.max() + PAD + 1, xs.min() - PAD:xs.max() + PAD + 1]
    h, w = m.shape
    path = potrace.Bitmap(np.logical_not(m)).trace(
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
                d.append(f"C{seg.c1.x:.2f},{seg.c1.y:.2f} {seg.c2.x:.2f},{seg.c2.y:.2f} {e.x:.2f},{e.y:.2f}")
        d.append("Z")
    return {"w": w, "h": h, "d": "".join(d)}


out = {}
for name, (x0, x1) in PARTS.items():
    m = np.zeros_like(full)
    m[:, x0 * SCALE:x1 * SCALE] = full[:, x0 * SCALE:x1 * SCALE]
    out[name] = trace(m)
    print(name, out[name]["w"], out[name]["h"], len(out[name]["d"]))

(ROOT / "_wordmark_parts.json").write_text(json.dumps(out), encoding="utf-8")
