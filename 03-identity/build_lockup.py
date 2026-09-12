# -*- coding: utf-8 -*-
"""락업 시안 → lockup-options.html

2026-09-01 확정: 한글 정본(오하리상점) · 영문 정본(OHARI) **둘을 따로 만든다.**
  - 한글 = 스토어 대문·웹·상세페이지   - 영문 = 패키지(박스·띠지·스티커)
  - 하나의 락업에 한글+영문을 같이 넣지 않는다(구 B안 폐기).

⚠️ 글자 형태는 임시(폰트)다. 여기서 정하는 것은 **배치와 비례**뿐이다.
   형태(손그림 정본)는 확정 후 시트 → vectorize.py 로 만든다.
사용: python build_lockup.py
"""
import os, re

D = os.path.dirname(os.path.abspath(__file__))

def inline(name, cls, size):
    s = open(os.path.join(D, name), encoding="utf-8").read()
    s = re.sub(r'\s(width|height)="[^"]*"', '', s, count=2)
    s = s.replace('<svg', f'<svg class="{cls}" style="width:{size}px;height:{size}px"', 1)
    s = re.sub(r'<title>.*?</title>', '', s, flags=re.S)
    return s

TURTLE_S = inline("char-turtle.svg", "tt", 34)
TURTLE_M = inline("char-turtle.svg", "tt", 52)

HTML = """<!doctype html><meta charset="utf-8"><title>오하리상점 · 락업</title>
<style>
 :root{--paper:#FFFFFF;--ink:#262320;--line:rgba(38,35,32,.14);
       --muted:rgba(38,35,32,.55);--faint:rgba(38,35,32,.05)}
 *{box-sizing:border-box}
 body{background:var(--paper);color:var(--ink);margin:0;padding:56px 48px 120px;
      font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;
      font-size:15px;line-height:1.7}
 h1{font-size:22px;font-weight:700;margin:0 0 6px;letter-spacing:-.01em}
 .sub{color:var(--muted);font-size:13px;margin:0 0 8px;max-width:820px}
 .warn{border:1px solid var(--line);border-radius:10px;padding:14px 18px;max-width:820px;
       font-size:13px;color:var(--muted);margin:20px 0 0}
 .warn b{color:var(--ink)}
 h2{font-size:16px;font-weight:700;margin:66px 0 4px}
 h3{font-size:13px;font-weight:700;margin:26px 0 0;color:var(--muted);letter-spacing:.02em}
 .grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px;max-width:1060px;margin-top:20px}
 .opt{border:1px solid var(--line);border-radius:12px;overflow:hidden;background:var(--paper)}
 .stage{height:190px;display:flex;align-items:center;justify-content:center;border-bottom:1px solid var(--line)}
 .stage.sq{height:230px}
 .note{padding:16px 20px 20px}
 .note>b{display:block;font-size:14px;margin-bottom:4px}
 .note p{margin:0;font-size:13px;color:var(--muted);line-height:1.65}
 .note p b{color:var(--ink)}
 /* --- 워드마크 임시 조판 --- */
 .ko{font-weight:700;letter-spacing:-.02em;line-height:1;font-size:40px}
 .en{font-weight:700;line-height:1}
 .two{text-align:center;line-height:1.02}
 .two b{font-size:42px;font-weight:700;letter-spacing:-.02em;display:block}
 .two i{font-size:42px;font-weight:700;letter-spacing:.22em;display:block;margin-left:.22em;font-style:normal}
 .var{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;max-width:1060px;margin-top:14px}
 .var div{border:1px solid var(--line);border-radius:10px;padding:26px 14px 12px;text-align:center}
 .var span{display:block;font-size:11px;color:var(--muted);margin-top:16px}
 .mini{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;max-width:1060px;margin-top:14px}
 .mini div{border:1px solid var(--line);border-radius:10px;padding:18px 14px 12px;text-align:center}
 .mini span{display:block;font-size:11px;color:var(--muted);margin-top:10px}
 .onink{background:var(--ink);color:var(--paper);border-radius:12px;padding:34px 40px;margin-top:16px;
        display:flex;gap:56px;align-items:center;flex-wrap:wrap;max-width:1060px}
 .onink .tt{color:var(--paper)}
 table{border-collapse:collapse;margin-top:16px;font-size:13px;max-width:1060px;width:100%}
 th,td{border:1px solid var(--line);padding:9px 12px;text-align:left;vertical-align:top}
 th{background:var(--faint);font-weight:700}
 .no{color:var(--muted)}
 /* 적용 미리보기 */
 .apps{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;max-width:1060px;margin-top:18px}
 .app{border:1px solid var(--line);border-radius:12px;overflow:hidden}
 .app .cap{padding:10px 14px;font-size:12px;color:var(--muted);border-top:1px solid var(--line)}
 .store{height:230px;padding:16px;display:flex;flex-direction:column;gap:10px}
 .store .bar{display:flex;align-items:center;justify-content:center;border-bottom:1px solid var(--line);padding-bottom:12px}
 .store .thumbs{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;flex:1}
 .store .thumbs i{background:var(--faint);border-radius:6px;display:block}
 .box{height:230px;display:flex;align-items:center;justify-content:center;background:var(--faint)}
 .boxface{width:180px;height:130px;border:1px solid var(--line);background:var(--paper);border-radius:4px;
          display:flex;align-items:center;justify-content:center;box-shadow:0 6px 18px rgba(38,35,32,.06)}
 .tape{height:230px;display:flex;align-items:center;justify-content:center}
 .band{width:100%;border-top:1px solid var(--line);border-bottom:1px solid var(--line);
       padding:14px 0;display:flex;align-items:center;justify-content:center;gap:26px}
</style>

<h1>오하리상점 — 락업</h1>
<p class="sub"><b>2026-09-01 확정</b> — 한글과 영문을 하나의 락업에 묶지 않고 <b>정본 둘</b>로 나눈다.
한글은 스토어 대문·웹, 영문은 패키지. 구 B안(한글 아래 영문)은 폐기.</p>

<div class="warn">
<b>글자 형태는 임시다.</b> 화면 글씨는 Pretendard로 얹은 자리표시이고, 정본은 손그림이다.
지금 정하는 것은 <b>배치·비례·자간</b>이며, 확정되면 그 비례대로 시트를 만들고 <code>vectorize.py</code>로 딴다.
형태를 코드가 만들지 않는 규칙(<code>illustration-system.md</code> §1)은 로고에도 적용된다.
</div>

<h2>정본 둘</h2>
<div class="grid2">
  <div class="opt">
    <div class="stage"><span class="ko">오하리상점</span></div>
    <div class="note"><b>① 한글 정본 · 오하리상점</b>
    <p>한 줄 단독(구 A안). 스마트스토어 대문, 자사몰 헤더, 상세페이지, 인스타 프로필.<br>
    <b>'오하리' 단독으로 쓰지 않는다</b> — 사진관·돌잔치 계정과 검색이 섞인다.</p></div>
  </div>
  <div class="opt">
    <div class="stage"><span class="en" style="font-size:40px;letter-spacing:.22em">OHARI</span></div>
    <div class="note"><b>② 영문 정본 · OHARI</b>
    <p>패키지 전용. 박스 면, 띠지, 봉인 스티커, 쇼핑백.<br>
    글자가 5자라 <b>자간이 형태를 결정한다.</b> 아래에서 폭을 먼저 고른다.</p></div>
  </div>
</div>

<h2>영문 — 자간 <b>.22 확정</b></h2>
<p class="sub">패키지는 면이 넓고 글자가 하나뿐이라, 자간이 곧 톤이다. 넓힐수록 조용해지고 좁힐수록 손맛이 남는다.</p>
<div class="var">
  <div><span class="en" style="font-size:34px;letter-spacing:.06em">OHARI</span><span>좁게 .06 — 폐기</span></div>
  <div style="border-color:var(--ink)"><span class="en" style="font-size:34px;letter-spacing:.22em">OHARI</span><span><b>중간 .22 — 확정</b></span></div>
  <div><span class="en" style="font-size:34px;letter-spacing:.42em">OHARI</span><span>넓게 .42 — 폐기(작게 줄이면 흩어짐)</span></div>
</div>

<h2 hidden>한글 — 정사각 변형(폐기)</h2><div hidden>
<p class="sub">박스 도장·인스타 프로필처럼 정사각인 자리는 한 줄이 작아진다. 두 줄 변형을 함께 둔다.</p>
<div class="grid2">
  <div class="opt"><div class="stage sq"><div class="two"><b>오하리</b><i>상점</i></div></div>
    <div class="note"><b>세로 2줄 변형</b><p>아래 줄을 자간으로 늘려 폭을 맞춘다. 사각 덩어리라 도장·정사각 자리에 강하다.</p></div></div>
  <div class="opt"><div class="stage sq"><span class="ko" style="font-size:30px">오하리상점</span></div>
    <div class="note"><b>기본 한 줄(비교)</b><p>같은 정사각 안에서는 글자가 작아진다. 가로로 긴 자리에서만 유리.</p></div></div>
</div>

</div>
<h2>축약형</h2>
<p class="sub">파비콘 16px · 봉인 스티커 · 도자기 각인. 정본이 안 들어가는 자리에서 무엇을 남길지.</p>
<div class="mini" style="grid-template-columns:repeat(3,1fr);max-width:640px">
  <div>__TURTLE_S__<span><b>거북이 — 확정</b></span></div>
  <div style="opacity:.32"><span class="ko" style="font-size:32px">오</span><span>첫 글자 — 폐기</span></div>
  <div style="opacity:.32"><span class="en" style="font-size:32px">O</span><span>이니셜 — 폐기</span></div>
</div>

<h2>적용 미리보기</h2>
<div class="apps">
  <div class="app">
    <div class="store">
      <div class="bar"><span class="ko" style="font-size:22px">오하리상점</span></div>
      <div class="thumbs"><i></i><i></i><i></i><i></i><i></i><i></i></div>
    </div>
    <div class="cap">스마트스토어 대문 — <b>한글</b></div>
  </div>
  <div class="app">
    <div class="box"><div class="boxface"><span class="en" style="font-size:22px;letter-spacing:.22em">OHARI</span></div></div>
    <div class="cap">박스 상면 — <b>영문</b></div>
  </div>
  <div class="app">
    <div class="tape"><div class="band">
      <span class="en" style="font-size:15px;letter-spacing:.3em">OHARI</span>__TURTLE_S__<span class="en" style="font-size:15px;letter-spacing:.3em">OHARI</span>
    </div></div>
    <div class="cap">띠지 — <b>영문 + 거북이</b></div>
  </div>
</div>

<h2>잉크 반전</h2>
<div class="onink">
  <span class="ko">오하리상점</span>
  <span class="en" style="font-size:34px;letter-spacing:.22em">OHARI</span>
  __TURTLE_M__
</div>

<h2>사용 규칙</h2>
<table>
<tr><th>자리</th><th>쓰는 것</th><th>비고</th></tr>
<tr><td>스마트스토어·톡스토어 대문, 자사몰 헤더</td><td><b>한글</b></td><td>국내 검색 유입이 매출 축</td></tr>
<tr><td>상세페이지 상·하단, 인스타 프로필</td><td><b>한글</b></td><td>계정명도 오하리상점</td></tr>
<tr><td>박스·띠지·봉인 스티커·쇼핑백</td><td><b>영문</b></td><td>1도 인쇄. 면이 조용해야 그릇이 산다</td></tr>
<tr><td>메시지카드·엽서</td><td>영문 또는 거북이</td><td>받는 사람이 먼저 보는 면 — 브랜드가 앞서지 않게</td></tr>
<tr><td>라벨(재질·원산지 등 의무 표시)</td><td class="no">로고 아님 — 본문 서체</td><td>식약처 '식품용' 도안은 공식 원본 그대로</td></tr>
</table>

<h3>하지 않는 것</h3>
<table>
<tr><td>한글과 영문을 한 락업으로 붙여 쓰기</td><td class="no">정본이 둘이라는 결정 자체가 무의미해진다</td></tr>
<tr><td>축약 자리에 '오'·'O' 쓰기</td><td class="no">축약형은 거북이 단독으로 확정(2026-09-01)</td></tr>
<tr><td>대외 노출에 '오하리' 단독 표기</td><td class="no">사진관·돌잔치 계정과 검색이 섞인다</td></tr>
<tr><td>패키지에 한글 워드마크 크게 넣기</td><td class="no">면이 시끄러워지고 영문 정본의 자리가 사라진다</td></tr>
<tr><td>거북이를 워드마크 옆에 상시 붙이기</td><td class="no">심볼 금지 조항 — 그림이 둘이 되어 서로를 깎는다. 띠지·카드에서 단독으로만</td></tr>
</table>
"""

HTML = HTML.replace("__TURTLE_M__", TURTLE_M).replace("__TURTLE_S__", TURTLE_S)
out = os.path.join(D, "lockup-options.html")
open(out, "w", encoding="utf-8").write(HTML)
print("written:", out, len(HTML))
