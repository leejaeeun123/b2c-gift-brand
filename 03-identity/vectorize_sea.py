# -*- coding: utf-8 -*-
"""바다 모티프 시트(PNG) → 개별 모티프 SVG.
파란 X 표시된 4칸은 제외한다. 검정 잉크만 마스크로 잡아 X선은 자동 제거된다.
사용: python vectorize_sea.py [png경로]
"""
import cv2, numpy as np, io, os, sys
from vectorize import normalize, trace, stroke_width, TPL

SRC = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\jaeeu\Downloads\9144fa50-00b7-4e65-a4d8-4c354a11991b.png"
OUT = os.path.dirname(os.path.abspath(__file__))

GRID = [["turtle",     "urchin",  "anemone",   "fish"],
        ["starfish",   "clam",    "coral",     "seahorse"],
        ["wave",       "seaweed", "sea-clover","conch"],
        ["heart",      "sparkle-star", "bow",  "crab"]]
SKIP = {"turtle", "fish", "heart", "bow"}
KO = {"urchin":"성게","anemone":"말미잘","starfish":"불가사리","clam":"진주조개",
      "coral":"산호","seahorse":"해마","wave":"파도","seaweed":"해초",
      "sea-clover":"바다클로버","conch":"소라","sparkle-star":"반짝별","crab":"게"}

def load_ink(path):
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    b, g, r = img[:,:,0].astype(int), img[:,:,1].astype(int), img[:,:,2].astype(int)
    dark = (b+g+r)/3 < 140
    gray = (np.abs(b-g) < 45) & (np.abs(g-r) < 45) & (np.abs(b-r) < 45)
    return (dark & gray).astype(np.uint8)

if __name__ == "__main__":
    ink = load_ink(SRC)
    H, W = ink.shape
    TARGET = float(os.environ.get("TARGET", "5.2"))
    made = []
    for ri, row in enumerate(GRID):
        for ci, name in enumerate(row):
            if name in SKIP: continue
            y0, y1 = int(H*ri/4), int(H*(ri+1)/4)
            x0, x1 = int(W*ci/4), int(W*(ci+1)/4)
            cell = ink[y0:y1, x0:x1].copy()
            # 옆칸에서 넘어온 파편 제거 (면적 작고 테두리에 붙은 것)
            n, lab, st, _ = cv2.connectedComponentsWithStats(
                cv2.dilate(cell, np.ones((9,9), np.uint8)), 8)
            keep = np.zeros_like(cell)
            areas = [(st[i][4], i) for i in range(1, n)]
            if not areas: continue
            big = max(a for a, _ in areas)
            for a, i in areas:
                bx, by, bw2, bh2 = st[i][:4]
                edge = (bx <= 1 or by <= 1 or bx+bw2 >= cell.shape[1]-1
                        or by+bh2 >= cell.shape[0]-1)
                if a >= big*0.0008 and not (edge and a < big*0.25):
                    keep[(lab == i) & (cell > 0)] = 1
            ys, xs = np.nonzero(keep)
            sub = keep[ys.min():ys.max()+1, xs.min():xs.max()+1]
            sub = normalize(sub, TARGET)
            d = trace(sub)
            p = os.path.join(OUT, "motif-" + name + ".svg")
            io.open(p, "w", encoding="utf-8").write(TPL.format(t=KO[name], d=d))
            made.append(("motif-"+name, KO[name], sub.shape, len(d)))
    for n, k, sh, sz in made:
        print("  %-22s %-10s %-12s %6d bytes" % (n+".svg", k, sh, sz))
