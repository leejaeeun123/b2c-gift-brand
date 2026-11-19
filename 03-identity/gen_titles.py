# -*- coding: utf-8 -*-
"""상세페이지 블록 제목(영문 손글씨 시트) → 줄별 SVG.

- 시트 한 장에 제목이 한 줄씩 세로로 놓여 있다. 잉크 없는 가로 띠에서 잘라 줄마다 SVG 1장.
- 모든 줄을 같은 배율로 딴다 → Figma에서 같은 비율로 넣으면 글자 크기가 서로 맞는다.
- 트레이싱은 potrace 베지어. 원본 시트가 작아(글자 높이 약 130px) 외곽이 울퉁불퉁하므로
  4배 업스케일 + 강한 블러(SIGMA)로 획을 둥글게 다듬고, 모서리 없이(alphamax 1.33) 곡선만으로 딴다.
사용: python gen_titles.py [png경로]   (SIGMA=원본 px 기준 블러 반경, 환경변수로 조정)
"""
import io, os, sys
import cv2, potrace
import numpy as np
from xml.sax.saxutils import escape
from gen_v3 import load, clean

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "motif-source", "titles-en-v1.png")
OUT = os.path.join(HERE, "v3")

# 위에서부터 순서대로 (slug, 문구)
ROWS = [
    ("title-set", "Set"),
    ("title-whats-inside", "What's Inside"),
    ("title-shipping-returns", "Shipping & Returns"),
    ("title-not-a-defect", "Not a Defect"),
    ("title-details", "Details"),
    ("title-single-item", "Single Item"),
]
S = 0.1      # 원본 px → viewBox 단위 (전 줄 공통)
PAD = 1.0
UP = 4       # 트레이싱 전 업스케일
SIGMA = float(os.environ.get("SIGMA", "3.0"))   # 원본 px 기준 — 클수록 둥글다
SUFFIX = os.environ.get("SUFFIX", "")


# Use & Care(text-use-and-care.svg)에 맞추는 기준값 — 원본 시트에서 잰 값
REF_SLANT = -0.04                 # 세로획을 곧게 세우는 전단 계수 (Use & Care)
CAP = 125.0                       # 이 시트의 큰 대문자 높이(px)
STROKE = float(os.environ.get("STROKE", str(0.137 * CAP)))   # Use & Care 획/큰 대문자 비 = 32/234
# Figma 삽입 배율 = 원본 px × 0.5 (Use & Care 큰 대문자 63px ÷ CAP) → 획 두께도 같아진다


def slant(sub):
    """세로획이 가장 곧게 서는 전단 계수 — 열 투영이 가장 뾰족해지는 값"""
    h, w = sub.shape
    best = (-1.0, 0.0)
    for k in np.arange(-0.35, 0.351, 0.01):
        M = np.float32([[1, k, -k*h/2 + 40], [0, 1, 0]])
        p = cv2.warpAffine(sub.astype(np.float32), M, (w + 80, h)).sum(axis=0)
        best = max(best, (float((p**2).sum()), float(k)))
    return best[1]


def stroke_width(m):
    dt = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5)
    v = dt[m > 0]
    return float(4*np.median(v)) if len(v) else 1.0


def smooth_d(sub, s, ox, oy):
    """마스크 → 기울기·획 두께를 기준에 맞추고 둥글게 다듬은 베지어 path"""
    m = np.pad(sub, 8).astype(np.float32)
    h, w = m.shape
    k = slant(sub) - REF_SLANT                      # Use & Care 와 같은 기울기로
    m = cv2.warpAffine(m, np.float32([[UP, UP*k, -UP*k*h/2], [0, UP, 0]]), (w*UP, h*UP), flags=cv2.INTER_CUBIC)
    m = cv2.GaussianBlur(m, (0, 0), SIGMA * UP) > 0.5
    cut = (stroke_width(m) - STROKE*UP) / 2         # 기준보다 굵으면 깎고, 가늘면 불린다
    if abs(cut) > 0.5:
        if cut > 0: m = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5) > cut
        else:       m = cv2.distanceTransform((~m).astype(np.uint8), cv2.DIST_L2, 5) < -cut
        m = cv2.GaussianBlur(m.astype(np.float32), (0, 0), SIGMA * UP * 0.6) > 0.5
    path = potrace.Bitmap(np.logical_not(m)).trace(turdsize=40, alphamax=1.33, opticurve=True, opttolerance=0.4)
    k = s / UP
    f = lambda p: "%.2f,%.2f" % (ox + (p.x - 8*UP)*k, oy + (p.y - 8*UP)*k)
    d = []
    for c in path:
        d.append("M" + f(c.start_point))
        for seg in c:
            if seg.is_corner: d.append("L%sL%s" % (f(seg.c), f(seg.end_point)))
            else: d.append("C%s %s %s" % (f(seg.c1), f(seg.c2), f(seg.end_point)))
        d.append("Z")
    return "".join(d)


def split_rows(ink, n):
    """잉크 없는 행 구간으로 n줄 분할 — 줄이 더 많이 나오면 가장 좁은 틈부터 병합(아포스트로피 등)"""
    row = ink.sum(axis=1) > 0
    runs, start = [], None
    for y, v in enumerate(row):
        if v and start is None: start = y
        if not v and start is not None: runs.append((start, y)); start = None
    if start is not None: runs.append((start, len(row)))
    while len(runs) > n:
        _, i = min((runs[i+1][0] - runs[i][1], i) for i in range(len(runs) - 1))
        runs[i:i+2] = [(runs[i][0], runs[i+1][1])]
    if len(runs) != n:
        raise SystemExit("줄 수 불일치: %d줄 감지, %d줄 필요" % (len(runs), n))
    out = []
    for y0, y1 in runs:
        sub = ink[y0:y1]; xs = np.nonzero(sub.sum(axis=0))[0]
        out.append(sub[:, xs.min():xs.max()+1])
    return out


def svg(sub, title):
    h, w = sub.shape
    W, H = w*S + PAD*2, h*S + PAD*2
    d = smooth_d(sub, S, PAD, PAD)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.2f %.2f" width="%.0f" height="%.0f"\n'
            '     fill="currentColor" fill-rule="evenodd" stroke="none" color="#262320">\n'
            '  <title>%s</title>\n  <path d="%s"/>\n</svg>\n') % (W, H, W*8, H*8, escape(title), d)


if __name__ == "__main__":
    ink, _ = load(SRC)
    ink = clean(ink)
    for sub, (slug, text) in zip(split_rows(ink, len(ROWS)), ROWS):
        io.open(os.path.join(OUT, slug + SUFFIX + ".svg"), "w", encoding="utf-8").write(svg(sub, text))
        print("%-26s %4dx%-4d px" % (slug + ".svg", sub.shape[1], sub.shape[0]))
