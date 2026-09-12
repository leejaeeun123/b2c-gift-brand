"""시그니처 로고(거북이 + OHARI 세로 락업) 간격 시안 HTML — 옵티컬 기준.

거북이 SVG 박스에는 잉크 바깥 여백이 있으므로, 거북이 '잉크' 바운딩박스를 기준으로
정렬·간격을 계산한다. 간격 = 거북이 잉크 높이 x ratio.
워드마크는 트레이싱 시 넣은 PAD(6px x SCALE 2 = 12px)를 양쪽에서 제거해 잉크만 쓴다.
"""
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parent
parts = json.loads((ROOT / "_wordmark_parts.json").read_text(encoding="utf-8"))
turtle_d = re.search(r'd="([^"]+)"', (ROOT / "char-turtle.svg").read_text(encoding="utf-8")).group(1)

# 거북이 잉크 바운딩박스 (char-turtle.svg viewBox 0 0 100 100 기준)
TX0, TX1, TY0, TY1 = 6.94, 92.79, 24.99, 74.74
TIW, TIH = TX1 - TX0, TY1 - TY0
PAD = 12            # 워드마크 트레이싱 여백
TURTLE_W = 0.95     # 거북이 잉크 폭 / 워드마크 잉크 폭


def sig(key, gap, width=210):
    p = parts[key]
    ww, wh = p["w"] - PAD * 2, p["h"] - PAD * 2      # 워드마크 잉크 크기
    s = ww * TURTLE_W / TIW                           # 거북이 스케일
    tw, th = TIW * s, TIH * s
    g = th * gap
    W, H = ww, th + g + wh
    # 거북이: 잉크 좌상단을 (가운데, 0)에 맞춘다
    tx, ty = (ww - tw) / 2 - TX0 * s, -TY0 * s
    return (f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="{width}" fill="currentColor" '
            f'fill-rule="evenodd">'
            f'<g transform="translate({tx:.2f},{ty:.2f}) scale({s:.4f})"><path d="{turtle_d}"/></g>'
            f'<g transform="translate({-PAD},{th + g - PAD:.2f})"><path d="{p["d"]}"/></g></svg>')


OPTS = [("24%", 0.24), ("20%", 0.20), ("16%", 0.16), ("12%", 0.12)]


def row(key, w, cls=""):
    return f'<div class="row {cls}">' + "".join(
        f'<figure><div class="box">{sig(key, g, w)}</div>'
        f'<figcaption>간격 {n}</figcaption></figure>' for n, g in OPTS) + "</div>"


HTML = f"""<!doctype html><meta charset="utf-8"><title>오하리상점 시그니처 로고 — 간격 시안</title>
<style>
 body{{margin:0;padding:48px 40px 80px;background:#F6F1E8;color:#262320;
   font:15px/1.7 'Pretendard','Apple SD Gothic Neo',system-ui,sans-serif}}
 h1{{font-size:22px;margin:0 0 4px}} h2{{font-size:15px;margin:56px 0 16px;
   padding-bottom:8px;border-bottom:1px solid #26232022;letter-spacing:.02em}}
 p.note{{color:#26232099;margin:0 0 8px;font-size:13px}}
 .row{{display:flex;flex-wrap:wrap;gap:28px;align-items:flex-start}}
 figure{{margin:0}} .box{{background:#fff;border:1px solid #26232014;border-radius:4px;
   padding:26px 22px;display:flex;justify-content:center;align-items:center}}
 .dark .box{{background:#262320;color:#F6F1E8}}
 .sm .box{{padding:18px}}
 figcaption{{margin-top:8px;font-size:12px;color:#26232099;text-align:center}}
</style>
<h1>오하리상점 — 시그니처 로고 간격 시안</h1>
<p class="note">거북이 <b>잉크 기준</b>으로 다시 계산했습니다(박스 아래 빈 여백 제거).
 간격 = 거북이 잉크 높이 대비 %. 거북이 폭은 워드마크 폭의 95% 고정.</p>

<h2>1. 간격 4안</h2>
{row("ohari", 210)}

<h2>2. 어두운 배경</h2>
{row("ohari", 210, "dark")}

<h2>3. 축소 (96px · 스티커·파비콘 크기)</h2>
{row("ohari", 96, "sm")}
"""
(ROOT / "lockup-vertical.html").write_text(HTML, encoding="utf-8")
print(ROOT / "lockup-vertical.html")
