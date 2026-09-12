# -*- coding: utf-8 -*-
"""손그림 톤 미리보기 → lockup-handdrawn.html

⚠️ 이것은 **정본이 아니다.** 정본은 그림 시트 → vectorize.py 경로로만 나온다
   (illustration-system.md §1 — 형태를 코드가 만들지 않는다).
   여기서 보는 것은 "손으로 그으면 대충 이 정도 밀도·무게" 라는 감각 하나다.

방법: 글자 아웃라인을 따서(fontTools) 점으로 잘게 나누고, 저주파 노이즈로 흔든 뒤
      글자마다 미세하게 회전·기울이고 베이스라인을 들쭉날쭉하게 앉힌다.
사용: python build_handdrawn.py
"""
import os, math, random, re
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen

D = os.path.dirname(os.path.abspath(__file__))
FONTS = {
    "malgunbd": r"C:\Windows\Fonts\malgunbd.ttf",
    "malgun":   r"C:\Windows\Fonts\malgun.ttf",
}
_cache = {}

def font(key):
    if key not in _cache:
        f = TTFont(FONTS[key], fontNumber=0)
        _cache[key] = (f, f.getGlyphSet(), f["cmap"].getBestCmap(), f["head"].unitsPerEm)
    return _cache[key]


# ---------- 아웃라인 → 점열 ----------
def bez3(p0, p1, p2, p3, n):
    out = []
    for i in range(1, n + 1):
        t = i / n; u = 1 - t
        out.append((u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0],
                    u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1]))
    return out

def bez2(p0, p1, p2, n):
    out = []
    for i in range(1, n + 1):
        t = i / n; u = 1 - t
        out.append((u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0],
                    u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1]))
    return out

def contours(ch, fkey):
    """글자 하나의 윤곽선을 점열 리스트로. em 단위."""
    f, gs, cmap, upm = font(fkey)
    gname = cmap.get(ord(ch))
    if gname is None:
        return [], 0
    pen = DecomposingRecordingPen(gs)
    gs[gname].draw(pen)
    cs, cur, start = [], [], (0, 0)
    for op, args in pen.value:
        if op == "moveTo":
            if cur: cs.append(cur)
            start = args[0]; cur = [start]
        elif op == "lineTo":
            cur.append(args[0])
        elif op == "curveTo":
            cur += bez3(cur[-1], args[0], args[1], args[2], 10)
        elif op == "qCurveTo":
            pts = list(args)
            on = pts[-1] if pts[-1] is not None else None
            offs = pts[:-1] if on is not None else pts
            p = cur[-1]
            for i, c in enumerate(offs):
                nxt = offs[i+1] if i+1 < len(offs) else on
                if nxt is None:
                    break
                if i + 1 < len(offs):
                    nxt = ((c[0]+nxt[0])/2, (c[1]+nxt[1])/2)
                cur += bez2(p, c, nxt, 8); p = cur[-1]
        elif op == "closePath":
            if cur: cs.append(cur); cur = []
    if cur: cs.append(cur)
    return cs, gs[gname].width


# ---------- 흔들기 ----------
def wobble(cs, amp, rnd, waves=3):
    """저주파 사인 합으로 윤곽선을 밀어낸다. 고주파로 흔들면 '자글거리는 노이즈'가 된다."""
    out = []
    for c in cs:
        n = len(c)
        if n < 4:
            out.append(c); continue
        ph = [(rnd.uniform(0, 6.28), rnd.uniform(1.2, 2.6), rnd.uniform(.5, 1.0)) for _ in range(waves)]
        nc = []
        for i, (x, y) in enumerate(c):
            t = i / n * 6.283
            d = sum(w * math.sin(t * f + p) for p, f, w in ph) / waves
            px, py = c[(i-1) % n]; nx, ny = c[(i+1) % n]
            tx, ty = nx - px, ny - py
            L = math.hypot(tx, ty) or 1
            nc.append((x - ty / L * d * amp, y + tx / L * d * amp))
        out.append(nc)
    return out


def glyph_path(ch, fkey, amp, rnd, scale, ox, oy, tilt, upm_pad=0):
    cs, adv = contours(ch, fkey)
    if not cs:
        return "", 0
    f, gs, cmap, upm = font(fkey)
    cs = wobble(cs, amp, rnd)
    a = math.radians(tilt)
    parts = []
    for c in cs:
        pts = []
        for x, y in c:
            x, y = x * scale, y * scale
            x += y * math.tan(a) * .06
            pts.append((ox + x, oy - y))
        d = "M %.2f %.2f " % pts[0] + " ".join("L %.2f %.2f" % p for p in pts[1:]) + " Z"
        parts.append(d)
    return " ".join(parts), adv * scale


def wordmark(text, fkey, size, tracking, amp, seed, jitter_y=0.0, jitter_s=0.0):
    """단어 하나를 손그림 톤 SVG로. 반환: (svg문자열, 폭, 높이)"""
    rnd = random.Random(seed)
    f, gs, cmap, upm = font(fkey)
    scale = size / upm
    x, paths, base = 0.0, [], size * 1.0
    for ch in text:
        s = scale * (1 + rnd.uniform(-jitter_s, jitter_s))
        dy = rnd.uniform(-jitter_y, jitter_y) * size
        tilt = rnd.uniform(-1.4, 1.4)
        d, adv = glyph_path(ch, fkey, amp, rnd, s, x, base + dy, tilt)
        if d: paths.append(d)
        x += adv + tracking * size
    w, h = x, size * 1.45
    body = "".join('<path d="%s"/>' % p for p in paths)
    svg = ('<svg viewBox="%.1f %.1f %.1f %.1f" style="height:%dpx;width:auto" '
           'fill="currentColor" fill-rule="nonzero" xmlns="http://www.w3.org/2000/svg">%s</svg>'
           % (-size*.06, size*.1, w + size*.12, h*.78, int(size*.9), body))
    return svg


# ---------- 페이지 ----------
KO = "오하리상점"
EN = "OHARI"
TRACK_EN = 0.22   # 확정
TRACK_KO = -0.02

def inline_turtle(size):
    s = open(os.path.join(D, "char-turtle.svg"), encoding="utf-8").read()
    s = re.sub(r'\s(width|height)="[^"]*"', '', s, count=2)
    s = re.sub(r'<title>.*?</title>', '', s, flags=re.S)
    return s.replace('<svg', f'<svg style="width:{size}px;height:{size}px;flex:none"', 1)

AMPS = [("약", 45), ("중", 100), ("강", 190)]

rows_ko = "".join(
    '<div><div class="stage">%s</div><span>흔들기 %s (amp %d)</span></div>'
    % (wordmark(KO, "malgunbd", 76, TRACK_KO, a, 11 + i), n, a)
    for i, (n, a) in enumerate(AMPS))
rows_en = "".join(
    '<div><div class="stage">%s</div><span>흔들기 %s (amp %d)</span></div>'
    % (wordmark(EN, "malgunbd", 68, TRACK_EN, a, 31 + i), n, a)
    for i, (n, a) in enumerate(AMPS))

# 굵기(원본 웨이트) 비교 — 중간 흔들기 고정
weights = "".join(
    '<div><div class="stage">%s</div><span>%s</span></div>'
    % (wordmark(KO, k, 66, TRACK_KO, 100, 77), lab)
    for k, lab in [("malgun", "가는 획 — 모티프 선(TARGET 5.2)에 가까움"),
                   ("malgunbd", "굵은 획 — 마커로 그은 느낌")])

# 베이스라인 들쭉날쭉
uneven = "".join(
    '<div><div class="stage">%s</div><span>%s</span></div>'
    % (wordmark(KO, "malgunbd", 66, TRACK_KO, 100, 91 + i, jy, js), lab)
    for i, (jy, js, lab) in enumerate([
        (0.0,  0.0,  "정렬 — 줄이 곧다"),
        (0.02, 0.03, "살짝 어긋남 — 손으로 쓴 티"),
        (0.05, 0.07, "많이 어긋남 — 낙서에 가까움")]))

TURTLE = inline_turtle(46)

HTML = """<!doctype html><meta charset="utf-8"><title>오하리상점 · 손그림 톤 미리보기</title>
<style>
 :root{--paper:#FFFFFF;--ink:#262320;--line:rgba(38,35,32,.14);--muted:rgba(38,35,32,.55);--faint:rgba(38,35,32,.05)}
 *{box-sizing:border-box}
 body{background:var(--paper);color:var(--ink);margin:0;padding:56px 48px 120px;
      font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;font-size:15px;line-height:1.7}
 h1{font-size:22px;font-weight:700;margin:0 0 6px}
 h2{font-size:16px;font-weight:700;margin:60px 0 4px}
 .sub{color:var(--muted);font-size:13px;margin:0;max-width:840px}
 .warn{border:1px solid var(--ink);border-radius:10px;padding:16px 18px;max-width:840px;font-size:13px;margin:22px 0 0}
 .warn b{display:block;margin-bottom:4px}
 .row{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;max-width:1080px;margin-top:18px}
 .row.two{grid-template-columns:repeat(2,1fr)}
 .row>div{border:1px solid var(--line);border-radius:12px;overflow:hidden}
 .stage{height:150px;display:flex;align-items:center;justify-content:center;color:var(--ink);padding:0 14px}
 .row span{display:block;font-size:12px;color:var(--muted);padding:10px 14px 14px;border-top:1px solid var(--line)}
 .onink{background:var(--ink);color:var(--paper);border-radius:12px;padding:36px 42px;margin-top:18px;
        display:flex;gap:56px;align-items:center;flex-wrap:wrap;max-width:1080px}
 .small{display:flex;gap:34px;align-items:flex-end;flex-wrap:wrap;margin-top:18px;
        border:1px solid var(--line);border-radius:12px;padding:26px 30px;max-width:1080px}
 .small figure{margin:0;text-align:center}
 .small figcaption{font-size:11px;color:var(--muted);margin-top:10px}
 .prompt{border:1px solid var(--line);border-radius:12px;padding:18px 22px;max-width:1080px;margin-top:18px;
         background:var(--faint);font-size:13px;white-space:pre-wrap;line-height:1.6;
         font-family:ui-monospace,Consolas,monospace}
</style>

<h1>오하리상점 — 손그림 톤 미리보기</h1>
<p class="sub">확정 반영: 영문 자간 <b>.22</b> · 한글 세로 2줄 <b>제외</b> · 축약형 <b>거북이 단독</b>.</p>

<div class="warn"><b>⚠️ 이건 정본이 아니다.</b>
글자 아웃라인(맑은 고딕)을 따서 선을 흔들고 글자마다 기울인 것이다. <b>형태는 여전히 폰트의 형태다.</b>
정본은 그림 시트 → <code>vectorize.py</code> 로만 나온다 — 코드가 만들 수 있는 건 떨림이지 형태 감각이 아니라는
기록이 <code>illustration-system.md</code> §1에 남아 있다(모티프를 코드로 그리려다 접은 이력).
여기서 볼 것은 하나다 — <b>손으로 가면 이 정도 밀도·무게가 맞는가.</b>
</div>

<h2>한글 — 흔들기 세기</h2>
<p class="sub">선을 얼마나 흔들 것인가. 강하게 갈수록 낙서에 가깝고, 작게 줄였을 때 먼저 무너진다.</p>
<div class="row">__KO__</div>

<h2>영문 — 흔들기 세기 <small style="font-weight:400;color:rgba(38,35,32,.55)">(자간 .22 고정)</small></h2>
<div class="row">__EN__</div>

<h2>획 굵기</h2>
<p class="sub">모티프 16종은 <code>TARGET = 5.2</code>로 두께를 맞춰 놨다. 로고가 그 옆에 섰을 때 같은 손으로 보여야 한다.</p>
<div class="row two">__W__</div>

<h2>줄 맞춤</h2>
<p class="sub">글자를 얼마나 어긋나게 앉힐 것인가. 어긋날수록 사람 손 같지만, 스토어 대문에서는 성의 없어 보일 수 있다.</p>
<div class="row">__U__</div>

<h2>작게 — 생존 확인</h2>
<p class="sub">파비콘·봉인 스티커·상세페이지 하단. 여기서 뭉개지면 선을 단순화한다. 귀여움보다 생존이 먼저다.</p>
<div class="small">
  <figure>__KO_S1__<figcaption>한글 28px</figcaption></figure>
  <figure>__KO_S2__<figcaption>한글 18px</figcaption></figure>
  <figure>__EN_S1__<figcaption>영문 20px</figcaption></figure>
  <figure>__EN_S2__<figcaption>영문 13px</figcaption></figure>
  <figure>__TURTLE__<figcaption>거북이 — 확정 축약형</figcaption></figure>
</div>

<h2>잉크 반전</h2>
<div class="onink">__KO_INV__ __EN_INV__ __TURTLE__</div>

<h2>정본으로 가는 다음 단계</h2>
<p class="sub">위에서 밀도·무게가 정해지면, 그 감각을 시트 제작 지시로 옮긴다. 아래를 그대로 쓰면 된다.</p>
<div class="prompt">[워드마크 시트 제작 지시]

흰 배경에 검정 선으로만. 컬러·그림자·질감 없음.

1행: 한글 &lsquo;오하리상점&rsquo; 한 줄 — 같은 문구를 5가지 손글씨 형태로 5번
2행: 영문 &lsquo;OHARI&rsquo; 대문자 한 줄 — 자간을 넉넉히 띄워 5번

- 선: 굵기가 고른 둥근 펜촉. 마커처럼 두껍지 않게.
- 손으로 그은 떨림·망설임·비대칭을 남긴다. 자로 잰 듯 반듯하면 실패.
- 캘리그라피·붓글씨 아님. 흘려 쓰지 않고 또박또박 그린 글자.
- 참조 시트: assets/reference/motif-sheet-v1.jpg — <b>같은 손</b>이어야 한다.
- 글자끼리 붙지 않게 여백을 두고, 각 안을 충분히 떨어뜨려 배치.

→ 나온 PNG를 vectorize.py로 따서 SVG 정본 6종 + currentColor 3종으로 내보낸다.</div>
"""

HTML = (HTML.replace("__KO__", rows_ko).replace("__EN__", rows_en)
            .replace("__W__", weights).replace("__U__", uneven)
            .replace("__KO_S1__", wordmark(KO, "malgunbd", 28, TRACK_KO, 100, 5))
            .replace("__KO_S2__", wordmark(KO, "malgunbd", 18, TRACK_KO, 100, 5))
            .replace("__EN_S1__", wordmark(EN, "malgunbd", 20, TRACK_EN, 100, 6))
            .replace("__EN_S2__", wordmark(EN, "malgunbd", 13, TRACK_EN, 100, 6))
            .replace("__KO_INV__", wordmark(KO, "malgunbd", 66, TRACK_KO, 100, 11))
            .replace("__EN_INV__", wordmark(EN, "malgunbd", 58, TRACK_EN, 100, 31))
            .replace("__TURTLE__", TURTLE))

out = os.path.join(D, "lockup-handdrawn.html")
open(out, "w", encoding="utf-8").write(HTML)
print("written:", out, len(HTML))
