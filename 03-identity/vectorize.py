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
    made = []
    for i, (x, y, bw, bh) in enumerate(bs):
        name = NAMES[i] if i < len(NAMES) else "item%02d" % i
        sub = ink[y:y+bh, x:x+bw]
        d = trace(sub)
        pre = "char-" if name in CHARS else "motif-"
        p = os.path.join(OUT, pre + name + ".svg")
        io.open(p, "w", encoding="utf-8").write(TPL.format(t=KO.get(name, name), d=d))
        made.append((pre+name, KO.get(name, name), len(d)))
    for n, k, sz in made:
        print("  %-22s %-8s %6d bytes" % (n+".svg", k, sz))
