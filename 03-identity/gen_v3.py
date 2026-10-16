# -*- coding: utf-8 -*-
"""2026-10 아이덴티티 추가 이미지(16장) → SVG 일괄 변환.

- 사진 1장 = 전체 SVG 1장(v3/sheet-*.svg) + 요소별 SVG(v3/<sheet>/NN.svg)
- 파란 X(사용자 제외 표시)가 닿은 요소는 버린다. 파란 픽셀 자체도 잉크에서 뺀다.
- 기존 모티프와 같은 포맷(viewBox 100, currentColor, evenodd). 두께 보정은 하지 않는다(원본 그대로).
사용: python gen_v3.py
"""
import cv2, numpy as np, io, os, sys, json
from xml.sax.saxutils import escape
import potrace
from vectorize import TPL

SCALE = 2   # 트레이싱 전 업스케일 — 곡선이 더 매끈해진다


HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "v3")
DL = r"C:\Users\jaeeu\Downloads"

# (출력 slug, 원본 파일, 한글 제목, 분할 여부)
SRCS = [
 ("silhouette-tableware",  "옆면-뒷.png",                                   "식기 실루엣 띠(옆면)", True),
 ("silhouette-sea",        "바다 생물 일곱 실루엣.png",                      "바다 생물 실루엣 7종", True),
 ("silhouette-board",      "미니멀 흑백 주방용품과 동물 아이콘 보드.png",     "식기·거북이 실루엣 보드", True),
 ("text-a-little-care",    "작은 배려.png",                                  "A Little Care", False),
 ("text-use-and-care",     "손글씨 스타일의 Use & Care.png",                 "Use & Care", False),
 ("care-no-microwave",     "ChatGPT 이미지 2026년 10월 11일 오후 06_06_59-1.png", "전자레인지 사용 금지", False),
 ("care-no-fire-oven",     "직화 및 오븐 사용 금지 아이콘.png",               "직화·오븐 사용 금지", False),
 ("care-no-dishwasher",    "ChatGPT 이미지 2026년 10월 11일 오후 06_07_02-2.png", "식기세척기 사용 금지", False),
 ("pattern-seaweed-band",  "유기적인 검은 잉크 블롭 실루엣.png",              "해초 실루엣 띠", False),
 ("pattern-seaweed-bubbles","손그림 느낌의 추상 해초와 거품.png",             "해초와 거품", False),
 ("care-dishwasher",       "ChatGPT 이미지 2026년 10월 11일 오후 09_44_02-1.png", "식기세척기", False),
 ("care-microwave",        "ChatGPT 이미지 2026년 10월 16일 오후 09_12_39.png",   "전자레인지", False),
 ("line-sheet-a",          "4a5c7b52-aa24-4372-ac75-9085bf272d81=.png",     "선 그림 시트 A", True),
 ("line-sheet-b",          "2b851922-6212-4dda-ae0e-d74d197c0028.png",      "선 그림 시트 B", True),
 ("line-sheet-c",          "bc0ecf07-56b7-4501-90a1-8f742d4161e4.png",      "선 그림 시트 C", True),
 ("text-slowly",           "천천히, 멋지게.png",                             "Slowly is wonderful.", False),
 ("pattern-wave-band",     "흑백 유기적 물결 추상 배너.png",                  "물결 실루엣 띠", False),
]

def load(path):
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    if img.shape[2] == 4:                      # 알파 → 흰 배경 합성
        a = img[:, :, 3:4].astype(float) / 255
        img = (img[:, :, :3] * a + 255 * (1 - a)).astype(np.uint8)
    b, g, r = [img[:, :, i].astype(int) for i in range(3)]
    dark = (b + g + r) / 3 < 150
    gray = (np.abs(b - g) < 50) & (np.abs(g - r) < 50) & (np.abs(b - r) < 50)
    blue = (b > r + 50) & (b > g + 20)
    return (dark & gray & ~blue).astype(np.uint8), blue.astype(np.uint8)

def drop_crossed(ink, blue):
    """파란 X가 닿은 연결 성분 제거"""
    if blue.sum() == 0: return ink
    k = np.ones((7, 7), np.uint8)
    n, lab = cv2.connectedComponents(cv2.dilate(ink, k), 8)
    hit = set(np.unique(lab[cv2.dilate(blue, np.ones((15, 15), np.uint8)) > 0])) - {0}
    keep = ~np.isin(lab, list(hit))
    out = (ink & keep).astype(np.uint8)
    # 지운 덩어리의 상자 안에 남은 잔재(분리된 눈·코 등)도 함께 지운다
    for i in hit:
        ys, xs = np.nonzero(lab == i)
        out[ys.min():ys.max()+1, xs.min():xs.max()+1] = 0
    return out

def clean(ink, min_frac=0.00005):
    h, w = ink.shape
    n, lab, st, _ = cv2.connectedComponentsWithStats(ink, 8)
    out = np.zeros_like(ink)
    for i in range(1, n):
        if st[i][4] >= h * w * min_frac: out[lab == i] = 1
    return out

def boxes(ink, kfrac):
    """근접 성분을 묶어 요소(마스크) 목록 → 행/열 순 정렬. 각 항목 = (x, y, w, h, mask)"""
    h, w = ink.shape
    k = max(3, int(min(h, w) * kfrac)) | 1
    n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(ink, np.ones((k, k), np.uint8)), 8)
    items = [[list(st[i][:4]), {i}] for i in range(1, n) if st[i][4] >= h * w * 0.0002]
    def inter(a, b):
        x0 = max(a[0], b[0]); y0 = max(a[1], b[1])
        x1 = min(a[0]+a[2], b[0]+b[2]); y1 = min(a[1]+a[3], b[1]+b[3])
        return max(0, x1-x0) * max(0, y1-y0)
    # 작은 조각(접시 가운데 점, 거북이 눈 등)은 자기를 80% 이상 품는 상자 중 '가장 작은' 상자에 붙인다
    items.sort(key=lambda it: -it[0][2]*it[0][3])
    merged = []
    for box, labels in items:
        area = box[2]*box[3]
        cands = [m for m in merged if inter(m[0], box) > area*0.8]
        if cands:
            host = min(cands, key=lambda m: m[0][2]*m[0][3])
            hb = host[0]
            x0 = min(hb[0], box[0]); y0 = min(hb[1], box[1])
            x1 = max(hb[0]+hb[2], box[0]+box[2]); y1 = max(hb[1]+hb[3], box[1]+box[3])
            host[0] = [x0, y0, x1-x0, y1-y0]; host[1] |= labels
        else:
            merged.append([box, set(labels)])
    items = merged
    out = []
    for _, labels in items:
        m = (ink > 0) & np.isin(lab, list(labels))      # 이웃 요소 조각은 제외
        ys, xs = np.nonzero(m)
        if len(xs) == 0: continue
        x0, y0, x1, y1 = xs.min(), ys.min(), xs.max()+1, ys.max()+1
        out.append([x0, y0, x1-x0, y1-y0, m[y0:y1, x0:x1].astype(np.uint8)])
    out.sort(key=lambda b: b[1])
    rows, cur, base = [], [], None
    for b in out:
        cy = b[1] + b[3]/2
        if base is None or abs(cy - base) < h*0.08:
            cur.append(b); base = cy if base is None else (base+cy)/2
        else:
            rows.append(sorted(cur, key=lambda z: z[0])); cur = [b]; base = cy
    if cur: rows.append(sorted(cur, key=lambda z: z[0]))
    return [b for r in rows for b in r]

def potrace_d(sub, s, ox=0.0, oy=0.0):
    """마스크 → 매끈한 베지어 path (potrace). s=출력 스케일"""
    m = cv2.resize(sub, None, fx=SCALE, fy=SCALE, interpolation=cv2.INTER_LINEAR)
    m = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.2) > 0.5
    m = np.pad(m, 4)
    path = potrace.Bitmap(np.logical_not(m)).trace(turdsize=10, alphamax=1.0, opticurve=True, opttolerance=0.3)
    k = s / SCALE
    d = []
    for c in path:
        p = c.start_point
        d.append("M%.2f,%.2f" % (ox + (p.x-4)*k, oy + (p.y-4)*k))
        for seg in c:
            e = seg.end_point
            if seg.is_corner:
                d.append("L%.2f,%.2fL%.2f,%.2f" % (ox+(seg.c.x-4)*k, oy+(seg.c.y-4)*k, ox+(e.x-4)*k, oy+(e.y-4)*k))
            else:
                d.append("C%.2f,%.2f %.2f,%.2f %.2f,%.2f" % (ox+(seg.c1.x-4)*k, oy+(seg.c1.y-4)*k,
                         ox+(seg.c2.x-4)*k, oy+(seg.c2.y-4)*k, ox+(e.x-4)*k, oy+(e.y-4)*k))
        d.append("Z")
    return "".join(d)

def trace(sub, box=100.0, pad=4.0):
    """요소용 — 100 viewBox 가운데 정렬"""
    h, w = sub.shape
    s = (box - pad*2) / max(w, h)
    return potrace_d(sub, s, (box - w*s)/2, (box - h*s)/2)

def trace_rect(sub, title):
    """비정사각 전체 이미지용 — viewBox를 잉크 비율에 맞춘다"""
    h, w = sub.shape
    s = 96.0 / max(w, h)
    W, H = w*s + 4, h*s + 4
    d = potrace_d(sub, s, 2, 2)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.2f %.2f" width="%.0f" height="%.0f"\n'
            '     fill="currentColor" fill-rule="evenodd" stroke="none" color="#262320">\n'
            '  <title>%s</title>\n  <path d="%s"/>\n</svg>\n') % (W, H, W*8, H*8, escape(title), d)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    manifest = {}
    for slug, fn, ko, split in SRCS:
        ink, blue = load(os.path.join(DL, fn))
        ink = clean(drop_crossed(ink, blue))
        ys, xs = np.nonzero(ink)
        full = ink[ys.min():ys.max()+1, xs.min():xs.max()+1]
        io.open(os.path.join(OUT, slug + ".svg"), "w", encoding="utf-8").write(trace_rect(full, ko))
        entry = {"src": fn, "title": ko, "crossed_out": bool(blue.sum() > 0), "parts": []}
        if split:
            d = os.path.join(OUT, slug); os.makedirs(d, exist_ok=True)
            for f in os.listdir(d): os.remove(os.path.join(d, f))
            for i, (x, y, bw, bh, sub) in enumerate(boxes(ink, 0.008)):
                p = os.path.join(d, "%02d.svg" % i)
                io.open(p, "w", encoding="utf-8").write(TPL.format(t=escape("%s %02d" % (ko, i)), d=trace(sub)))
                entry["parts"].append({"file": "%02d.svg" % i, "box": [int(x), int(y), int(bw), int(bh)]})
        manifest[slug] = entry
        print("%-26s %-4s parts=%2d  blue=%s" % (slug, full.shape, len(entry["parts"]), bool(blue.sum() > 0)))
    io.open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8").write(json.dumps(manifest, ensure_ascii=False, indent=1))
