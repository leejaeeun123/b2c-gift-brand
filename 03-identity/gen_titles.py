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
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "motif-source", "titles-v2.png")
OUT = os.path.join(HERE, "v3")

# 위에서부터 순서대로 (slug, 문구)
ROWS = [
    ("name-mulbangul-suljan-set", "물방울 술잔 세트"),
    ("title-set", "세트구성"),
    ("title-detail-points", "Detail Points"),
    ("title-food-styling", "Food Styling"),
    ("title-review", "Review"),
    ("title-gift-box", "Gift Box"),
    ("title-whats-inside", "What's Inside"),
    ("title-at-a-glance", "At a Glance"),
    ("title-not-a-defect", "Not a Defect"),
    ("title-shipping-returns", "Shipping & Return"),
    ("title-details", "Details"),
    ("title-single-item", "Single Item"),
]
CAP = 76.0                        # 이 시트(titles-v2)의 큰 대문자 높이(px). v1 시트는 125
S = 0.1 * 125.0 / CAP             # 원본 px → viewBox 단위. v1과 같은 출력 크기(큰 대문자 = 12.5단위)가 되게 맞춘다
PAD = 1.0
UP = 6       # 트레이싱 전 업스케일 (v2 시트는 글자가 작아 6배)
SIGMA = float(os.environ.get("SIGMA", "1.6"))   # 원본 px 기준 — 클수록 둥글다
SUFFIX = os.environ.get("SUFFIX", "")


# Use & Care(text-use-and-care.svg)에 맞추는 기준값 — 원본 시트에서 잰 값
REF_SLANT = -0.04                 # 세로획을 곧게 세우는 전단 계수 (Use & Care)
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
    # 의도: v2 시트는 재은이 쓴 기울기를 그대로 둔다 — 짧은 단어는 기울기 추정이 흔들려 글자가 뒤틀린다.
    #       v1처럼 Use & Care 기울기에 맞추려면 SLANT_FIX=1
    k = (slant(sub) - REF_SLANT) if os.environ.get("SLANT_FIX") == "1" else 0.0
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


def row_boxes(ink, n):
    """split_rows 와 같은 줄 구간을 (y0, y1, x0, x1) 상자로"""
    boxes, y = [], 0
    row = ink.sum(axis=1) > 0
    for sub in split_rows(ink, n):
        while not row[y]: y += 1
        y0 = y; y1 = y0 + sub.shape[0]
        xs = np.nonzero(ink[y0:y1].sum(axis=0))[0]
        boxes.append((y0, y1, int(xs.min()), int(xs.max()) + 1))
        y = y1
    return boxes


KERN = float(os.environ.get("KERN", "0.45"))    # 글자 사이 빈 폭에 곱하는 값 (1 = 쓴 그대로)
WORD = float(os.environ.get("WORD", "0.55"))    # 단어 사이 빈 폭에 곱하는 값
TALL = float(os.environ.get("TALL", "1.12"))    # 세로로 늘리는 배율 (1 = 쓴 그대로) — 재은 11-22 "세로로 조금만"


def tighten(gray, mask):
    """자간 좁히기 — 잉크 없는 세로 띠(글자 사이·단어 사이)만 줄이고 글자 모양은 건드리지 않는다.
    의도: 로고(OHARISTORE)의 글자 사이가 획 두께의 약 0.5배인데 v2 시트는 약 0.6배 + 단어 사이 3~4배라 넓어 보였다(재은 11-22).
          획이 가로로 겹쳐 빈 띠가 없는 글자쌍은 그대로 둔다."""
    col = mask.sum(axis=0) > 0
    runs, st = [], None
    for x, v in enumerate(col):
        if v and st is None: st = x
        if not v and st is not None: runs.append((st, x)); st = None
    if st is not None: runs.append((st, len(col)))
    sw = stroke_width(mask > 0)
    g_parts, m_parts = [], []
    for i, (a, b) in enumerate(runs):
        g_parts.append(gray[:, a:b]); m_parts.append(mask[:, a:b])
        if i + 1 < len(runs):
            gap = runs[i+1][0] - b
            new = max(1, int(round(gap * (WORD if gap > 1.6 * sw else KERN))))
            g_parts.append(np.full((gray.shape[0], new), 255, gray.dtype))
            m_parts.append(np.zeros((mask.shape[0], new), mask.dtype))
    return np.hstack(g_parts), np.hstack(m_parts)


def load_gray(path):
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    if img.ndim == 3 and img.shape[2] == 4:
        a = img[:, :, 3:4].astype(float) / 255
        img = (img[:, :, :3] * a + 255 * (1 - a)).astype(np.uint8)
    return img if img.ndim == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def faithful_d(gray, s, ox, oy):
    """쓴 모양 그대로 — 회색조를 키운 뒤 경계만 따서 획 두께·모서리·속공간을 바꾸지 않는다.
    의도: v1 방식(이진 마스크 블러 + 두께 정규화 + 모서리 없음)은 v2 시트에서 글자가 뭉툭하게 부풀었다(재은 11-22)."""
    g = cv2.copyMakeBorder(gray, 8, 8, 8, 8, cv2.BORDER_CONSTANT, value=255)
    big = cv2.resize(g, None, fx=UP, fy=UP, interpolation=cv2.INTER_CUBIC)
    big = cv2.GaussianBlur(big, (0, 0), 0.35 * UP)        # 확대 계단만 지우는 정도
    m = big < 128
    path = potrace.Bitmap(np.logical_not(m)).trace(turdsize=20, alphamax=1.0, opticurve=True, opttolerance=0.2)
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


def svg(sub, title, gray=None):
    h, w = sub.shape
    W, H = w*S + PAD*2, h*S + PAD*2
    d = faithful_d(gray, S, PAD, PAD) if gray is not None else smooth_d(sub, S, PAD, PAD)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.2f %.2f" width="%.0f" height="%.0f"\n'
            '     fill="currentColor" fill-rule="evenodd" stroke="none" color="#262320">\n'
            '  <title>%s</title>\n  <path d="%s"/>\n</svg>\n') % (W, H, W*8, H*8, escape(title), d)


if __name__ == "__main__":
    ink, _ = load(SRC)
    ink = clean(ink)
    gray = None if os.environ.get("STYLE") == "round" else load_gray(SRC)     # STYLE=round → v1 방식
    for sub, (y0, y1, x0, x1), (slug, text) in zip(split_rows(ink, len(ROWS)), row_boxes(ink, len(ROWS)), ROWS):
        crop = None if gray is None else gray[y0:y1, x0:x1]
        if crop is not None and (KERN != 1 or WORD != 1): crop, sub = tighten(crop, sub)
        if crop is not None and TALL != 1:
            crop = cv2.resize(crop, None, fx=1, fy=TALL, interpolation=cv2.INTER_CUBIC)
            sub = cv2.resize(sub, (crop.shape[1], crop.shape[0]), interpolation=cv2.INTER_NEAREST)
        io.open(os.path.join(OUT, slug + SUFFIX + ".svg"), "w", encoding="utf-8").write(svg(sub, text, crop))
        print("%-26s %4dx%-4d px" % (slug + ".svg", sub.shape[1], sub.shape[0]))
