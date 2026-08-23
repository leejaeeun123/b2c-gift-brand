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

W = 6.2                # 기본 획 두께 — 마커펜
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

def wobble(pts, rng, amp=0.95, freq=0.028, phase=None):
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
def S(pts, closed=False, w=1.0, gap=0.0, smooth=True, amp=0.95, solid=False):
    return dict(pts=pts, closed=closed, w=w, gap=gap, smooth=smooth, amp=amp, solid=solid)

def DOT(x, y, r=3.2):
    """찍는 점 — 눈, 껍질 무늬"""
    return dict(dot=(x, y, r))

def motifs():
    M = []
    # 1 접시 — 테두리 물결 + 가운데 점
    M.append(("plate", "접시", [
        S(ellipse(50, 50, 37, 37, squash=0.80), closed=True),
        S(ellipse(50, 50, 27, 27, squash=0.78), closed=True, w=0.6, amp=1.4),
    ]))
    # 2 볼
    M.append(("bowl", "볼", [
        S([(16,38),(20,62),(34,76),(50,79),(66,76),(80,62),(84,38)]),
        S(ellipse(50, 38, 34, 34, squash=0.26), closed=True, w=0.85),
    ]))
    # 3 머그
    M.append(("mug", "머그", [
        S([(22,30),(24,58),(32,74),(50,78),(68,74),(76,58),(78,30)]),
        S(ellipse(50, 30, 28, 28, squash=0.30), closed=True, w=0.9),
        S([(78,42),(90,44),(92,56),(80,60)], w=0.9),
    ]))
    # 4 잔
    M.append(("glass", "잔", [
        S([(26,24),(32,56),(38,78),(50,80),(62,78),(68,56),(74,24)]),
        S(ellipse(50, 24, 24, 24, squash=0.30), closed=True, w=0.9),
    ]))
    # 5 주전자
    M.append(("teapot", "주전자", [
        S(ellipse(46, 58, 27, 25, squash=1.0), closed=True),
        S([(70,48),(84,42),(90,30)], w=0.9),
        S([(34,34),(46,28),(58,34)], w=0.85),
        S([(20,52),(8,58),(16,72),(26,74)], w=0.9),
    ]))
    # 6 수저
    M.append(("spoon", "수저", [
        S(ellipse(31, 27, 16, 16, squash=1.25), closed=True, w=0.9),
        S([(31,47),(32,84)]),
        S([(58,16),(60,82)], w=0.85, smooth=False),
        S([(72,16),(72,82)], w=0.85, smooth=False),
    ]))
    # 7 포크와 나이프
    M.append(("cutlery", "포크와 나이프", [
        S([(28,14),(28,30)], w=0.8, smooth=False),
        S([(38,14),(38,30)], w=0.8, smooth=False),
        S([(48,14),(48,30)], w=0.8, smooth=False),
        S([(28,30),(38,38),(48,30)], w=0.9),
        S([(38,38),(38,86)]),
        S([(68,14),(78,26),(76,46),(68,50)], w=0.95),
        S([(68,50),(68,86)]),
    ]))
    # 8 트레이
    M.append(("tray", "트레이", [
        S([(22,32),(78,32),(82,44),(82,62),(78,70),(22,70),(18,62),(18,44)], closed=True, smooth=False),
        S([(18,48),(8,50),(9,60),(18,58)], w=0.85, smooth=False),
        S([(82,48),(92,50),(91,60),(82,58)], w=0.85, smooth=False),
    ]))
    # 9 꽃 — 화병+꽃은 굵은 선에서 목이 뭉개져 전구처럼 읽혀 폐기. 꽃 한 송이로 단순화.
    petals = []
    for i in range(10):
        r = 23 if i % 2 == 0 else 9.5
        ang = -math.pi/2 + 2*math.pi*i/10
        petals.append((50 + r*math.cos(ang), 33 + r*math.sin(ang)))
    M.append(("flower", "꽃", [
        S(petals, closed=True, w=0.95, amp=0.6),
        DOT(50, 33, 5.0),
        S([(50,52),(51,88)]),
        S(ellipse(36, 66, 11, 11, squash=0.45, tilt=0.35), closed=True, w=0.8),
        S(ellipse(65, 74, 11, 11, squash=0.45, tilt=-0.35), closed=True, w=0.8),
    ]))
    # 10 초
    M.append(("candle", "초", [
        S([(36,44),(36,84),(64,84),(64,44)]),
        S(ellipse(50, 44, 14, 14, squash=0.30), closed=True, w=0.9),
        S([(50,38),(41,26),(50,12),(59,25),(50,38)], w=0.95),
    ]))
    # 11 리본 매듭
    M.append(("ribbon", "리본 매듭", [
        S([(44,48),(24,34),(12,44),(22,60),(44,54)], closed=True),
        S([(56,48),(76,34),(88,44),(78,60),(56,54)], closed=True),
        S([(46,58),(38,80)], w=0.9),
        S([(55,58),(64,78)], w=0.9),
        DOT(50, 51, 5.0),
    ]))
    # 12 편지
    M.append(("letter", "편지", [
        S([(14,30),(86,30),(86,74),(14,74)], closed=True, smooth=False),
        S([(14,30),(50,56),(86,30)], w=0.9, smooth=False),
    ]))
    # 13 선물 상자
    M.append(("box", "선물 상자", [
        S([(16,40),(84,40),(84,84),(16,84)], closed=True, smooth=False),
        S([(50,40),(50,84)], w=0.8, smooth=False),
        S([(16,54),(84,54)], w=0.8, smooth=False),
        S([(50,40),(34,24),(26,32),(50,40)], w=0.9),
        S([(50,40),(66,23),(74,31),(50,40)], w=0.9),
    ]))
    # 14 배
    M.append(("pear", "배", [
        S([(50,24),(36,36),(28,56),(36,78),(50,84),(64,78),(72,56),(64,36),(50,24)], closed=True),
        S([(50,25),(55,11)], w=0.9),
        S(ellipse(64, 14, 9, 9, squash=0.45, tilt=-0.35), closed=True, w=0.8),
    ]))
    return M

def characters():
    """거북이 — 행운을 등에 지고 천천히 간다"""
    dome  = [(18,62),(22,42),(33,29),(50,25),(67,29),(78,42),(82,62)]
    belly = [(20,63),(82,63)]
    head  = [(84,58),(90,50),(97,54),(96,64),(88,68),(81,65)]
    legF  = [(64,63),(65,76),(74,78)]
    legB  = [(36,63),(31,76),(22,78)]
    tail  = [(19,60),(9,64),(15,69)]
    dots  = [DOT(36,44,4.2), DOT(52,38,4.6), DOT(66,46,4.0), DOT(50,55,3.8)]

    C = []
    C.append(("turtle", "거북이", [
        S(dome), S(belly, w=0.85, smooth=False),
        S(head, w=0.9), DOT(90, 57, 2.6),
        S(legF, w=0.95), S(legB, w=0.95), S(tail, w=0.85),
    ] + dots))

    dy = 6
    sh = lambda pts: [(x, y+dy) for x, y in pts]
    C.append(("turtle-gift", "선물을 진 거북이", [
        S(sh(dome)), S(sh(belly), w=0.85, smooth=False),
        S(sh(head), w=0.9), DOT(90, 63, 2.6),
        S(sh(legF), w=0.95), S(sh(legB), w=0.95), S(sh(tail), w=0.85),
        DOT(38,52,4.0), DOT(66,54,3.8),
        S([(38,34),(62,34),(62,16),(38,16)], closed=True, smooth=False, w=0.85),
        S([(50,34),(50,16)], w=0.7, smooth=False),
        S([(50,16),(40,7),(34,13),(50,16)], w=0.8),
        S([(50,16),(60,6),(66,12),(50,16)], w=0.8),
    ]))

    # 작은 자리용 — 점무늬와 꼬리를 빼고 선을 줄인다
    C.append(("turtle-small", "작은 거북이", [
        S(dome), S(belly, w=0.9, smooth=False),
        S(head, w=0.95), DOT(90, 57, 3.0),
        S(legF, w=1.0), S(legB, w=1.0),
    ]))
    return C

TPL = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100"
     fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" color="#262320">
  <title>{title}</title>
{body}</svg>
'''

def build(outdir="."):
    made = []
    for name, ko, strokes in motifs() + [("char-"+n, k, st) for n, k, st in characters()]:
        rng = random.Random(SEED + sum(ord(c) for c in name))
        body = []
        for st in strokes:
            if "dot" in st:
                x, y, r = st["dot"]
                body.append('  <circle cx="%.1f" cy="%.1f" r="%.1f" fill="currentColor" stroke="none"/>' % (x, y, r))
                continue
            pts = st["pts"]
            if st["smooth"]:
                pts = catmull(pts, closed=st["closed"])
            elif st["closed"]:
                pts = pts + [pts[0]]
            pts = wobble(pts, rng, amp=st.get("amp", 0.95))
            if not st["closed"] and st["gap"] == 0:
                pts = overshoot(pts, rng.uniform(0.4, 1.0))
            w = round(W * st["w"] * rng.uniform(0.90, 1.10), 2)
            if st["solid"]:
                body.append('  <path d="%s Z" fill="currentColor" stroke="currentColor" stroke-width="%s"/>'
                            % (path_d(pts, 0), round(W*0.5, 2)))
            else:
                body.append('  <path d="%s" stroke-width="%s"/>' % (path_d(pts, st["gap"]), w))
        svg = TPL.format(title=ko, body="\n".join(body) + "\n")
        pref = "" if name.startswith("char-") else "motif-"
        p = os.path.join(outdir, "%s%s.svg" % (pref, name))
        io.open(p, "w", encoding="utf-8").write(svg)
        made.append((name, ko))
    return made

if __name__ == "__main__":
    m = build(os.path.dirname(os.path.abspath(__file__)))
    print("%d motifs" % len(m))
    for n, k in m:
        print("  motif-%s.svg  %s" % (n, k))
