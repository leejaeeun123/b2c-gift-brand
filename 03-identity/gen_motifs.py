# -*- coding: utf-8 -*-
"""모티프 SVG 생성기 — 손그림 규칙을 코드로 고정한다.

규칙(illustration-system.md와 1:1):
  - 선 하나로 그린다. 면을 칠하지 않는다.
  - 선 끝은 둥글다(round cap). 획은 살짝 흔들린다.
  - 닫힌 도형도 완전히 닫지 않는다 — 종이에 그린 선처럼 끝이 조금 열린다.
  - 대칭을 피한다. 좌우가 미세하게 다르다.
출력: motif-*.svg (viewBox 0 0 100 100, currentColor)
"""
import math, random, io, os

W = 2.6                # 기본 획 두께
SEED = 20260823

def catmull(points, closed=False, samples=8):
    """Catmull-Rom -> 촘촘한 점열"""
    p = list(points)
    if closed:
        p = [p[-1]] + p + [p[0], p[1]]
    else:
        p = [p[0]] + p + [p[-1]]
    out = []
    for i in range(len(p) - 3):
        p0, p1, p2, p3 = p[i], p[i+1], p[i+2], p[i+3]
        for s in range(samples):
            t = s / samples
            t2, t3 = t*t, t*t*t
            x = 0.5*((2*p1[0]) + (-p0[0]+p2[0])*t + (2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2 + (-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            y = 0.5*((2*p1[1]) + (-p0[1]+p2[1])*t + (2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2 + (-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
            out.append((x, y))
    return out

def wobble(pts, rng, amp=0.34, freq=0.045, phase=None):
    """손떨림 — 사인 노이즈 2겹. 난수는 위상만 흔든다(형태는 유지)."""
    ph1 = rng.uniform(0, 6.28) if phase is None else phase
    ph2 = rng.uniform(0, 6.28)
    out = []
    for i, (x, y) in enumerate(pts):
        d = math.sin(i*freq + ph1)*amp + math.sin(i*freq*2.7 + ph2)*amp*0.4
        # 진행 방향의 법선으로 밀어낸다
        j = min(i+1, len(pts)-1)
        dx, dy = pts[j][0]-x, pts[j][1]-y
        n = math.hypot(dx, dy) or 1
        out.append((x - dy/n*d, y + dx/n*d))
    return out

def overshoot(pts, amt):
    """열린 선 끝을 진행 방향으로 조금 더 그어 손그림 느낌을 준다"""
    if amt <= 0 or len(pts) < 3:
        return pts
    def ext(a, b, k):
        dx, dy = b[0]-a[0], b[1]-a[1]
        n = math.hypot(dx, dy) or 1
        return (b[0]+dx/n*k, b[1]+dy/n*k)
    return [ext(pts[1], pts[0], amt)] + pts + [ext(pts[-2], pts[-1], amt)]

def path_d(pts, open_gap=0.0):
    """열린 끝: 닫힌 도형이라도 뒤쪽 일부를 잘라 종이 느낌을 남긴다"""
    if open_gap > 0:
        pts = pts[:max(4, int(len(pts)*(1-open_gap)))]
    d = "M %.2f %.2f" % pts[0]
    for x, y in pts[1:]:
        d += " L %.2f %.2f" % (x, y)
    return d

def ellipse(cx, cy, rx, ry, n=26, squash=1.0, tilt=0.0):
    pts = []
    for i in range(n):
        a = 2*math.pi*i/n
        x = rx*math.cos(a); y = ry*math.sin(a)*squash
        pts.append((cx + x*math.cos(tilt) - y*math.sin(tilt),
                    cy + x*math.sin(tilt) + y*math.cos(tilt)))
    return pts

def arc(cx, cy, rx, ry, a0, a1, n=18):
    return [(cx + rx*math.cos(a0 + (a1-a0)*i/(n-1)),
             cy + ry*math.sin(a0 + (a1-a0)*i/(n-1))) for i in range(n)]

# ---- 모티프 정의: (파일명, 한글명, 스트로크 리스트) --------------------------
# 스트로크 = dict(pts=점열, closed=bool, w=두께배수, gap=열린정도, smooth=bool)
def S(pts, closed=False, w=1.0, gap=0.0, smooth=True):
    return dict(pts=pts, closed=closed, w=w, gap=gap, smooth=smooth)

def motifs():
    M = []
    # 1 접시
    M.append(("plate", "접시", [
        S(ellipse(50, 52, 36, 36, squash=0.62), closed=True, gap=0.04),
        S(ellipse(50, 53, 23, 23, squash=0.58), closed=True, w=0.8, gap=0.03),
    ]))
    # 2 볼
    M.append(("bowl", "볼", [
        S(ellipse(50, 38, 32, 32, squash=0.34), closed=True, gap=0.05),
        S(arc(50, 39, 32, 34, 0.05, math.pi-0.05)),
        S([(41,71),(50,73),(59,71)], w=0.8),
    ]))
    # 3 머그
    M.append(("mug", "머그", [
        S(ellipse(45, 32, 22, 22, squash=0.36), closed=True, gap=0.05),
        S([(23,32),(24,52),(28,68),(45,73),(62,68),(66,52),(67,32)]),
        S(arc(70, 46, 13, 13, -1.25, 1.25), w=0.9),
    ]))
    # 4 잔
    M.append(("glass", "잔", [
        S(ellipse(50, 22, 20, 20, squash=0.32), closed=True, gap=0.05),
        S([(30,23),(34,50),(37,73)]),
        S([(70,23),(66,50),(63,73)]),
        S([(37,73),(50,76),(63,73)], w=0.9),
        S([(33,44),(50,47),(67,44)], w=0.7),
    ]))
    # 5 주전자
    M.append(("teapot", "주전자", [
        S(ellipse(46, 58, 25, 23, squash=1.0), closed=True, gap=0.05),
        S([(68,50),(80,44),(88,34)], w=0.95),
        S([(88,34),(84,44)], w=0.9),
        S([(33,37),(46,33),(59,37)], w=0.9),
        S([(46,33),(46,27)], w=0.85),
        S(arc(24, 58, 13, 15, 1.5, 4.6), w=0.9),
    ]))
    # 6 수저
    M.append(("spoon", "수저", [
        S(ellipse(34, 26, 12, 12, squash=1.35, tilt=0.12), closed=True, gap=0.05),
        S([(34,42),(35,62),(35,80)]),
        S([(58,18),(60,80)], w=0.85, smooth=False),
        S([(70,18),(70,80)], w=0.85, smooth=False),
    ]))
    # 7 포크와 나이프
    M.append(("cutlery", "포크와 나이프", [
        S([(30,16),(30,34)], w=0.8, smooth=False),
        S([(38,16),(38,34)], w=0.8, smooth=False),
        S([(46,16),(46,34)], w=0.8, smooth=False),
        S(arc(38, 34, 9, 7, math.pi, 2*math.pi), w=0.9),
        S([(38,40),(38,84)]),
        S([(68,16),(76,26),(74,44),(68,48)], w=0.95),
        S([(68,48),(68,84)]),
    ]))
    # 8 트레이
    M.append(("tray", "트레이", [
        S([(24,34),(76,34),(80,42),(80,62),(76,68),(24,68),(20,62),(20,42)], closed=True, gap=0.03, smooth=False),
        S([(20,46),(12,46),(12,56),(20,56)], w=0.85, smooth=False),
        S([(80,46),(88,46),(88,56),(80,56)], w=0.85, smooth=False),
        S([(27,41),(73,41)], w=0.7, smooth=False),
    ]))
    # 9 화병과 꽃
    M.append(("vase", "화병과 꽃", [
        S([(36,46),(33,66),(38,80),(50,83),(62,80),(67,66),(64,46)]),
        S([(36,46),(50,50),(64,46)], w=0.85),
        S([(50,50),(51,28)], w=0.9),
        S(ellipse(51, 20, 9, 9, squash=0.9), closed=True, gap=0.06, w=0.9),
        S([(51,34),(63,26)], w=0.8),
        S(ellipse(66, 23, 5, 5, squash=0.9), closed=True, gap=0.08, w=0.8),
    ]))
    # 10 초
    M.append(("candle", "초", [
        S([(38,44),(38,82),(62,82),(62,44)], closed=False),
        S(ellipse(50, 44, 12, 12, squash=0.32), closed=True, gap=0.06, w=0.9),
        S([(50,40),(44,30),(50,16),(56,29),(50,40)], w=0.95),
    ]))
    # 11 리본 매듭
    M.append(("ribbon", "리본 매듭", [
        S([(46,48),(28,36),(18,44),(26,58),(46,52)], closed=True, gap=0.05),
        S([(54,48),(72,36),(82,44),(74,58),(54,52)], closed=True, gap=0.05),
        S(ellipse(50, 50, 6, 6, squash=1.0), closed=True, gap=0.07, w=0.9),
        S([(47,56),(40,76)], w=0.9),
        S([(54,56),(62,74)], w=0.9),
    ]))
    # 12 편지
    M.append(("letter", "편지", [
        S([(18,32),(82,32),(82,72),(18,72)], closed=True, gap=0.03, smooth=False),
        S([(18,32),(50,54),(82,32)], w=0.9, smooth=False),
    ]))
    # 13 선물 상자
    M.append(("box", "선물 상자", [
        S([(20,40),(80,40),(80,80),(20,80)], closed=True, gap=0.03, smooth=False),
        S([(50,40),(50,80)], w=0.85, smooth=False),
        S([(20,52),(80,52)], w=0.85, smooth=False),
        S([(50,40),(36,26),(28,32),(50,40)], w=0.9),
        S([(50,40),(64,25),(72,32),(50,40)], w=0.9),
    ]))
    # 14 배
    M.append(("pear", "배", [
        S([(50,26),(38,36),(32,52),(38,72),(50,78),(62,72),(68,52),(62,36),(50,26)], closed=True, gap=0.04),
        S([(50,26),(52,16)], w=0.9),
        S([(52,18),(64,14)], w=0.8),
    ]))
    return M

TPL = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100"
     fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" color="#262320">
  <title>{title}</title>
{body}</svg>
'''

def build(outdir="."):
    made = []
    for name, ko, strokes in motifs():
        rng = random.Random(SEED + sum(ord(c) for c in name))
        body = []
        for st in strokes:
            pts = st["pts"]
            if st["smooth"]:
                pts = catmull(pts, closed=st["closed"])
            elif st["closed"]:
                pts = pts + [pts[0]]
            pts = wobble(pts, rng, amp=0.34 if st["w"] >= 1 else 0.26)
            if not st["closed"] and st["gap"] == 0:
                pts = overshoot(pts, rng.uniform(0.8, 1.8))
            w = round(W * st["w"] * rng.uniform(0.90, 1.10), 2)
            body.append('  <path d="%s" stroke-width="%s"/>' % (path_d(pts, st["gap"]), w))
        svg = TPL.format(title=ko, body="\n".join(body) + "\n")
        p = os.path.join(outdir, "motif-%s.svg" % name)
        io.open(p, "w", encoding="utf-8").write(svg)
        made.append((name, ko))
    return made

if __name__ == "__main__":
    m = build(os.path.dirname(os.path.abspath(__file__)))
    print("%d motifs" % len(m))
    for n, k in m:
        print("  motif-%s.svg  %s" % (n, k))
