# -*- coding: utf-8 -*-
"""레퍼런스 시트(PNG) → 개별 모티프 SVG.

선 그림이므로 윤곽선을 따서 evenodd로 채우면 원본과 사실상 같은 벡터가 된다.
재작도가 아니라 '따기'다 — 형태는 원본 그대로 보존된다.
사용: python vectorize.py [png경로]
"""
import cv2, numpy as np, io, os, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\jaeeu\Downloads\ChatGPT Image 2026년 8월 23일 오후 06_46_31.png"
OUT = os.path.dirname(os.path.abspath(__file__))

NAMES = ["turtle","heart","flower","vase",
         "bowl","plate","cup","fork",
         "knife","spoon","ribbon","book",
         "candle","fish","pear","dog","clover","star"]
KO = {"turtle":"거북이","heart":"하트","flower":"꽃","vase":"화병과 꽃","bowl":"볼","plate":"접시",
      "cup":"잔","fork":"포크","knife":"나이프","spoon":"수저","ribbon":"리본","book":"책",
      "candle":"초","fish":"물고기","pear":"배","dog":"강아지","clover":"클로버","star":"별"}
CHARS = {"turtle","dog"}          # 캐릭터로 분류 → char-*.svg

def load(path):
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    return (img < 128).astype(np.uint8)

def clusters(ink):
    h, w = ink.shape
    k = max(3, int(min(h, w) * 0.022)) | 1
    n, lab, stats, _ = cv2.connectedComponentsWithStats(
        cv2.dilate(ink, np.ones((k, k), np.uint8)), 8)
    bs = [list(stats[i][:4]) for i in range(1, n) if stats[i][4] >= h*w*0.0004]

    # 겹치거나 포함된 상자 병합 (접시 가운데 점 등)
    def overlap(a, b):
        return not (a[0]+a[2] < b[0] or b[0]+b[2] < a[0] or a[1]+a[3] < b[1] or b[1]+b[3] < a[1])
    changed = True
    while changed:
        changed = False
        for i in range(len(bs)):
            for j in range(i+1, len(bs)):
                if overlap(bs[i], bs[j]):
                    x0 = min(bs[i][0], bs[j][0]); y0 = min(bs[i][1], bs[j][1])
                    x1 = max(bs[i][0]+bs[i][2], bs[j][0]+bs[j][2])
                    y1 = max(bs[i][1]+bs[i][3], bs[j][1]+bs[j][3])
                    bs[i] = [x0, y0, x1-x0, y1-y0]; bs.pop(j); changed = True; break
            if changed: break

    # 세로로 붙어버린 덩어리는 빈 줄에서 분리 (클로버 + 별)
    out = []
    for x, y, bw, bh in bs:
        sub = ink[y:y+bh, x:x+bw]
        rowsum = sub.sum(axis=1)
        gaps, run = [], 0
        for r, v in enumerate(rowsum):
            if v == 0: run += 1
            else:
                if run > max(6, bh*0.03): gaps.append((r-run, r))
                run = 0
        if gaps and bh > bw*1.4:
            cuts = [0] + [ (g[0]+g[1])//2 for g in gaps ] + [bh]
            for a, b in zip(cuts, cuts[1:]):
                if b-a > bh*0.15:
                    seg = sub[a:b]
                    ys, xs = np.nonzero(seg)
                    if len(xs) == 0: continue
                    out.append([x+xs.min(), y+a+ys.min(), xs.max()-xs.min()+1, ys.max()-ys.min()+1])
        else:
            out.append([x, y, bw, bh])

    # 행 단위 정렬
    h_ = ink.shape[0]
    out.sort(key=lambda b: b[1])
    rows, cur, base = [], [], None
    for b in out:
        cy = b[1] + b[3]/2
        if base is None or abs(cy - base) < h_*0.075:
            cur.append(b); base = cy if base is None else (base+cy)/2
        else:
            rows.append(sorted(cur, key=lambda z: z[0])); cur = [b]; base = cy
    if cur: rows.append(sorted(cur, key=lambda z: z[0]))
    return [b for r in rows for b in r]

# ---------------------------------------------------------------- 보정 단계
FACE_SWAP = [("cup", "vase")]      # (대상, 가져올 얼굴)

def _parts(ink, box, frac=0.02):
    x, y, bw, bh = box
    sub = ink[y:y+bh, x:x+bw]
    n, lab, st, _ = cv2.connectedComponentsWithStats(sub, 8)
    return sub, lab, [(i, st[i]) for i in range(1, n) if st[i][4] < bw*bh*frac]

def face_box(parts, ylo=0.0, yhi=1.0, bh=1):
    """얼굴로 볼 조각들의 합집합 상자"""
    sel = [(i, st) for i, st in parts if ylo*bh <= st[1] <= yhi*bh]
    if not sel: return None, []
    x0 = min(st[0] for _, st in sel); y0 = min(st[1] for _, st in sel)
    x1 = max(st[0]+st[2] for _, st in sel); y1 = max(st[1]+st[3] for _, st in sel)
    return (x0, y0, x1-x0, y1-y0), sel

def swap_faces(ink, boxes, names):
    """한 모티프의 얼굴을 다른 모티프의 얼굴로 갈아 끼운다 (원본 픽셀 그대로 이식)"""
    for dst_name, src_name in FACE_SWAP:
        if dst_name not in names or src_name not in names: continue
        di, si = names.index(dst_name), names.index(src_name)
        dx, dy, dbw, dbh = boxes[di]; sx, sy, sbw, sbh = boxes[si]
        dsub, dlab, dparts = _parts(ink, boxes[di])
        ssub, slab, sparts = _parts(ink, boxes[si])
        dfb, dsel = face_box(dparts, 0.25, 0.85, dbh)
        sfb, ssel = face_box(sparts, 0.60, 0.95, sbh)      # 화병 얼굴은 아래쪽
        if not dfb or not sfb: continue
        # 대상 얼굴 지우기
        for i, st in dsel:
            ink[dy:dy+dbh, dx:dx+dbw][dlab == i] = 0
        # 원본 얼굴 오려서 눈 간격 비율로 확대 후 이식
        fx, fy, fw, fh = sfb
        patch = np.zeros((fh, fw), np.uint8)
        for i, st in ssel:
            m = (slab[fy:fy+fh, fx:fx+fw] == i)
            patch[m] = 1
        k = dfb[2] / max(1, fw)
        nw, nh = max(1, int(round(fw*k))), max(1, int(round(fh*k)))
        patch = cv2.resize(patch, (nw, nh), interpolation=cv2.INTER_NEAREST)
        cx = dx + dfb[0] + dfb[2]//2; cy = dy + dfb[1] + dfb[3]//2
        px, py = cx - nw//2, cy - nh//2
        region = ink[py:py+nh, px:px+nw]
        region[patch > 0] = 1
    return ink

def stroke_width(sub):
    """획 두께 추정 — 폭 w의 선은 거리변환이 0..w/2 균일 -> 중앙값의 4배"""
    dt = cv2.distanceTransform(sub, cv2.DIST_L2, 5)
    v = dt[sub > 0]
    return float(4*np.median(v)) if len(v) else 1.0

def normalize(sub, target, box=100.0, pad=4.0, cap=1.0):
    """viewBox로 줄였을 때의 '보이는 두께'를 target에 맞춘다"""
    h, w = sub.shape
    scale = (box - pad*2)/max(w, h)
    cur = stroke_width(sub)*scale
    if cur >= target: return sub          # 원본보다 얇게 깎지 않는다
    r = (target - cur)/scale/2*cap
    k = int(round(min(r, 4.0)))          # 과도한 변형은 디테일을 먹는다
    if k < 1: return sub
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*k+1, 2*k+1))
    return cv2.dilate(sub, ker)

def trace(sub, box=100.0, pad=4.0):
    """윤곽선 → SVG path (evenodd 채움)"""
    m = cv2.copyMakeBorder(sub, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=0)
    cs, _ = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    h, w = m.shape
    s = (box - pad*2) / max(w, h)
    ox = (box - w*s)/2; oy = (box - h*s)/2
    eps = max(0.45, min(w, h) * 0.0035)
    d = []
    for c in cs:
        if cv2.contourArea(c) < 6: continue
        c = cv2.approxPolyDP(c, eps, True).reshape(-1, 2)
        if len(c) < 3: continue
        pts = [(ox + x*s, oy + y*s) for x, y in c]
        d.append("M " + " L ".join("%.2f %.2f" % p for p in pts) + " Z")
    return " ".join(d)

TPL = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100"\n'
       '     fill="currentColor" fill-rule="evenodd" stroke="none" color="#262320">\n'
       '  <title>{t}</title>\n  <path d="{d}"/>\n</svg>\n')

if __name__ == "__main__":
    ink = load(SRC)
    bs = clusters(ink)
    print("clusters:", len(bs))
    ink = swap_faces(ink, bs, NAMES)

    # 기준 두께 = 하트의 보이는 두께
    hi = NAMES.index("heart"); hx, hy, hw, hh = bs[hi]
    hsub = ink[hy:hy+hh, hx:hx+hw]
    HEART = stroke_width(hsub) * (92.0/max(hw, hh))
    TARGET = float(os.environ.get("TARGET", "5.2"))
    print("heart=%.2f  target=%.2f (viewBox units)" % (HEART, TARGET))

    made = []
    for i, (x, y, bw, bh) in enumerate(bs):
        name = NAMES[i] if i < len(NAMES) else "item%02d" % i
        sub = normalize(ink[y:y+bh, x:x+bw], TARGET)
        d = trace(sub)
        pre = "char-" if name in CHARS else "motif-"
        p = os.path.join(OUT, pre + name + ".svg")
        io.open(p, "w", encoding="utf-8").write(TPL.format(t=KO.get(name, name), d=d))
        made.append((pre+name, KO.get(name, name), len(d)))
    for n, k, sz in made:
        print("  %-22s %-8s %6d bytes" % (n+".svg", k, sz))
