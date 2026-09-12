# -*- coding: utf-8 -*-
"""logo-guide.html 빌드 — 로고 시스템 정리 + 패키지 계획(진행 중) 한 장.

SVG를 인라인해 단일 파일로 만든다. `python 03-identity/build_logo_guide.py`
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def svg(name, width=None, color=None):
    s = (ROOT / (name + ".svg")).read_text(encoding="utf-8")
    s = re.sub(r'\s(width|height)="\d+"', "", s, count=2)
    style = "width:" + width if width else "width:100%"
    if color:
        style += ";color:" + color
    return s.replace("<svg ", '<svg style="%s;height:auto" ' % style, 1)


def file_row(name, desc):
    return ('<tr><td><a href="%s.svg" download><code>%s.svg</code></a></td>'
            '<td>%s</td></tr>' % (name, name, desc))


SIG = svg("logo-signature-ink", "150px")
SIG_W = svg("logo-signature-white", "150px")
SIG_SM = svg("logo-signature-ink", "64px")
KO = svg("logo-wordmark-ko-ink", "220px")
EN = svg("logo-wordmark-en-ink", "260px")
OHARI = svg("logo-wordmark-ohari-ink", "150px")
KO_W = svg("logo-wordmark-ko-white", "220px")
EN_W = svg("logo-wordmark-en-white", "260px")
TURTLE = svg("char-turtle", "120px")

FILES = "".join(file_row(n, d) for n, d in [
    ("logo-signature-ink", "시그니처 로고 · 잉크 <b>(정본)</b>"),
    ("logo-signature-white", "시그니처 로고 · 화이트 (어두운 배경)"),
    ("logo-wordmark-ko-ink", "한글 워드마크 · 잉크"),
    ("logo-wordmark-ko-white", "한글 워드마크 · 화이트"),
    ("logo-wordmark-en-ink", "영문 워드마크 OHARISTORE · 잉크"),
    ("logo-wordmark-en-white", "영문 워드마크 OHARISTORE · 화이트"),
    ("logo-wordmark-ohari-ink", "OHARI · 잉크 (시그니처 구성 요소)"),
    ("logo-wordmark-ohari-white", "OHARI · 화이트"),
    ("char-turtle", "거북이 심볼 (currentColor)"),
])

HTML = """<!doctype html><html lang="ko"><meta charset="utf-8">
<title>오하리상점 — 로고 시스템 &amp; 패키지 계획</title>
<style>
:root{--paper:#FFFFFF;--ink:#262320;--bg:#F6F1E8}
*{box-sizing:border-box}
body{margin:0;padding:0 0 100px;background:var(--bg);color:var(--ink);
 font:15px/1.75 'Pretendard','Apple SD Gothic Neo',system-ui,sans-serif;
 -webkit-font-smoothing:antialiased}
.wrap{max-width:940px;margin:0 auto;padding:0 28px}
header{padding:72px 0 40px}
header h1{font-size:26px;margin:0 0 6px;letter-spacing:-.01em}
header p{margin:0;color:#26232099;font-size:14px}
.status{display:inline-block;margin-top:14px;font-size:12px;padding:3px 10px;border-radius:99px;
 background:#26232010;color:#262320aa}
section{margin-top:64px}
h2{font-size:17px;margin:0 0 6px;letter-spacing:-.01em}
h2 .num{color:#26232055;font-weight:400;margin-right:8px}
h3{font-size:14px;margin:32px 0 12px;color:#262320cc}
.lead{color:#26232099;font-size:14px;margin:0 0 20px;padding-bottom:14px;
 border-bottom:1px solid #26232018}
.card{background:var(--paper);border:1px solid #26232014;border-radius:6px;padding:32px}
.grid{display:flex;flex-wrap:wrap;gap:20px}
.grid>figure{margin:0;flex:1 1 200px}
figure .box{background:var(--paper);border:1px solid #26232014;border-radius:6px;
 min-height:190px;display:flex;align-items:center;justify-content:center;padding:28px}
figure .box.dark{background:var(--ink);color:var(--bg);border-color:transparent}
figcaption{margin-top:9px;font-size:12px;color:#26232099}
table{width:100%;border-collapse:collapse;font-size:14px;margin-top:8px}
th,td{text-align:left;padding:11px 12px;border-bottom:1px solid #26232014;vertical-align:top}
th{font-weight:600;color:#26232099;font-size:12.5px;letter-spacing:.02em}
td:first-child{white-space:nowrap;width:1%}
code{font:12.5px/1.5 ui-monospace,'SF Mono',Menlo,monospace;background:#26232010;
 padding:2px 6px;border-radius:3px}
a{color:inherit}
ul{margin:10px 0 0;padding-left:20px} li{margin:5px 0}
.two{display:flex;flex-wrap:wrap;gap:20px}
.two>div{flex:1 1 320px;background:var(--paper);border:1px solid #26232014;
 border-radius:6px;padding:22px 24px}
.two h4{margin:0 0 8px;font-size:13.5px}
.ok:before{content:"○ ";color:#262320} .no:before{content:"× ";color:#262320}
.spec{display:flex;gap:32px;flex-wrap:wrap;margin-top:20px}
.spec div{font-size:13px} .spec b{display:block;font-size:12px;color:#26232099;font-weight:500}
.todo li{color:#262320aa}
.flag{background:#26232008;border-left:2px solid var(--ink);padding:14px 18px;margin:18px 0;
 font-size:13.5px}
footer{margin-top:72px;padding-top:20px;border-top:1px solid #26232018;
 font-size:12px;color:#26232077}
</style>
<div class="wrap">
<header>
 <h1>오하리상점 — 로고 시스템 &amp; 패키지 계획</h1>
 <p>손글씨 워드마크 · 거북이 심볼 · 크라프트 1도 인쇄 박스</p>
 <div class="status">2026-09-13 · 로고 확정 / 패키지 계획 단계</div>
</header>

<section>
 <h2><span class="num">01</span>시그니처 로고</h2>
 <p class="lead">정본. 거북이(심볼) 아래 손글씨 영문 OHARI를 놓은 세로 락업.
  브랜드를 한 덩어리로 보여야 하는 모든 자리에 이것을 쓴다.</p>
 <div class="grid">
  <figure><div class="box">{SIG}</div><figcaption>시그니처 로고 · 잉크</figcaption></figure>
  <figure><div class="box dark">{SIG_W}</div><figcaption>화이트 (어두운 배경·크라프트 역출)</figcaption></figure>
  <figure><div class="box">{SIG_SM}</div><figcaption>64px 축소 — 이 크기까지 읽힌다</figcaption></figure>
 </div>
 <div class="spec">
  <div><b>거북이 폭</b>워드마크 폭의 95%</div>
  <div><b>간격</b>거북이 잉크 높이의 24%</div>
  <div><b>정렬</b>잉크 바운딩박스 가운데</div>
  <div><b>비율</b>634 : 686 (세로형)</div>
  <div><b>색</b>잉크 #262320 / 화이트 #FFFFFF</div>
 </div>
 <div class="flag">기준선은 <b>SVG 박스가 아니라 잉크</b>다. 거북이 SVG에는 아래쪽에 빈 여백이 있어서,
  박스 기준으로 맞추면 글씨가 실제보다 멀어 보인다. 재조합할 때는 <code>gen_signature.py</code>를 쓴다.</div>
</section>

<section>
 <h2><span class="num">02</span>워드마크</h2>
 <p class="lead">전부 같은 손글씨 원본 스캔에서 딴 것이다. 다시 쓴 글씨가 아니라 획이 원본 그대로다.</p>
 <div class="grid">
  <figure><div class="box">{KO}</div><figcaption>한글 — 오하리상점</figcaption></figure>
  <figure><div class="box">{EN}</div><figcaption>영문 — OHARISTORE</figcaption></figure>
  <figure><div class="box">{OHARI}</div><figcaption>OHARI — 시그니처 구성 요소</figcaption></figure>
 </div>
 <div class="grid" style="margin-top:20px">
  <figure><div class="box dark">{KO_W}</div><figcaption>한글 · 화이트</figcaption></figure>
  <figure><div class="box dark">{EN_W}</div><figcaption>영문 · 화이트</figcaption></figure>
 </div>
 <table>
  <tr><th>자리</th><th>무엇을 쓰나</th></tr>
  <tr><td>박스 뚜껑 · 스티커 · 파비콘</td><td><b>시그니처 로고</b> (거북이 + OHARI)</td></tr>
  <tr><td>사이트 헤더 · 상세페이지 · 명함</td><td>한글 워드마크 <b>오하리상점</b></td></tr>
  <tr><td>가로로 길고 낮은 자리 (띠지·테이프)</td><td>영문 워드마크 <b>OHARISTORE</b></td></tr>
  <tr><td>아주 작은 자리 (24px 이하)</td><td>거북이 심볼 단독</td></tr>
 </table>
</section>

<section>
 <h2><span class="num">03</span>심볼 — 거북이</h2>
 <p class="lead">행운을 등에 지고 간다. 레퍼런스 시트를 벡터화한 정본이라 코드로 다시 그리지 않는다.</p>
 <div class="two">
  <div style="flex:0 0 200px;text-align:center;padding:28px">{TURTLE}</div>
  <div>
   <h4>규칙</h4>
   <ul>
    <li class="ok">한 화면·한 박스에 <b>하나</b>만 등장한다</li>
    <li class="ok">등껍질 무늬는 <b>점</b>이다. 선으로 칸을 나누면 수박이 된다</li>
    <li class="no"><b>배송·물류 맥락에는 쓰지 않는다</b> — 송장·발송 안내·지연 공지.
     "느리다"로 읽힌다</li>
    <li class="no">위에서 본 등껍질은 만들지 않는다 (구명튜브·거미줄로 읽힘)</li>
   </ul>
  </div>
 </div>
</section>

<section>
 <h2><span class="num">04</span>사용 규칙</h2>
 <div class="two">
  <div>
   <h4>지킨다</h4>
   <ul>
    <li class="ok">색은 <b>잉크 #262320 / 화이트 #FFFFFF</b> 2색뿐. 포인트 컬러 없음</li>
    <li class="ok">여백은 로고 안 거북이 높이의 <b>&frac12; 이상</b> 사방으로</li>
    <li class="ok">최소 크기 — 시그니처 <b>가로 48px</b> · 워드마크 <b>가로 90px</b></li>
    <li class="ok">크라프트·어두운 바탕에서는 화이트 버전을 쓴다</li>
   </ul>
  </div>
  <div>
   <h4>하지 않는다</h4>
   <ul>
    <li class="no">기울이기 · 늘이기 · 그림자 · 테두리 · 그라데이션</li>
    <li class="no">거북이를 다른 모티프로 바꿔 락업 만들기</li>
    <li class="no">한글과 영문을 임의로 두 줄 조합하기 (정본은 거북이 + OHARI뿐)</li>
    <li class="no">사진 위에 직접 올리기 — 흰 면을 깔고 올린다</li>
   </ul>
  </div>
 </div>
</section>

<section>
 <h2><span class="num">05</span>파일</h2>
 <p class="lead">전부 <code>03-identity/</code>. 폰트 의존성 0(아웃라인 패스). 클릭하면 내려받는다.</p>
 <div class="card" style="padding:8px 16px"><table>
  <tr><th>파일</th><th>용도</th></tr>{FILES}
 </table></div>
 <table style="margin-top:20px">
  <tr><th>재현</th><th></th></tr>
  <tr><td><code>gen_logo_svg.py</code></td><td>원본 PNG 스캔 → 전체 가로 워드마크 벡터화</td></tr>
  <tr><td><code>gen_lockup_parts.py</code></td><td>스캔을 구간별로 잘라 ko / en / ohari 패스 추출</td></tr>
  <tr><td><code>gen_lockup.py</code></td><td>워드마크 6종(잉크·화이트) 출력</td></tr>
  <tr><td><code>gen_signature.py</code></td><td>시그니처 로고 출력 (확정 비율 내장)</td></tr>
 </table>
</section>

<section>
 <h2><span class="num">06</span>패키지 계획 <span class="status" style="margin:0 0 0 6px">계획 단계 · 디자인 미착수</span></h2>
 <p class="lead">크라프트지 박스에 1도 인쇄. 아직 확정이 아니라 <b>방향</b>이다.</p>

 <h3>구조 — 2겹</h3>
 <table>
  <tr><th>층</th><th>무엇</th><th>역할</th></tr>
  <tr><td>겉</td><td>무지 택배 상자</td><td>운송·송장·완충. 찍힘과 오염을 여기서 다 받는다</td></tr>
  <tr><td>안</td><td><b>크라프트 선물 박스</b> (1도 인쇄)</td><td>브랜드. 받는 사람이 여는 것.
   안에 습자지 + 세트 + 카드</td></tr>
 </table>

 <h3>인쇄</h3>
 <table>
  <tr><th>항목</th><th>계획</th></tr>
  <tr><td>원지</td><td><b>크라프트지</b> — 기성 규격(목형비 없음)</td></tr>
  <tr><td>인쇄</td><td><b>1도</b> — 윗면만, 또는 윗면 + 옆면</td></tr>
  <tr><td>내용</td><td>아이콘 스타일 일러스트 + 오하리상점 로고</td></tr>
  <tr><td>MOQ</td><td>약 <b>300개~</b></td></tr>
  <tr><td>규격</td><td>한 사이즈 우선. 주력 세트(M급) 실측 후 기성 규격표에서 고른다</td></tr>
 </table>

 <h3>일러스트 방향 — 확장을 견디는 아이콘</h3>
 <div class="flag">MOQ 300개면 한 번 찍은 박스를 <b>오래 쓴다.</b> 그 사이에 취급 분야가 그릇에서
  문구류 등으로 늘어나도 그대로 쓸 수 있어야 한다. 그래서 박스 위 그림은
  <b>접시·볼처럼 품목을 특정하는 그림이 아니라, 선물이라는 행위 자체를 가리키는 아이콘</b>으로 간다.</div>
 <div class="two">
  <div>
   <h4>쓴다</h4>
   <ul>
    <li class="ok">선물 상자 · 리본 · 편지 · 손 · 하트 · 별 · 클로버 · 꽃</li>
    <li class="ok">거북이 (박스당 하나)</li>
    <li class="ok">기존 모티프 정본을 그대로 — 같은 크기 그리드로 정렬</li>
   </ul>
  </div>
  <div>
   <h4>피한다</h4>
   <ul>
    <li class="no">접시·볼·수저처럼 <b>현재 취급 품목을 특정</b>하는 그림을 주인공으로 쓰는 것</li>
    <li class="no">박스를 꽉 채우는 패턴 — 여백이 없으면 저가로 읽힌다</li>
    <li class="no">시즌·연도가 박히는 요소</li>
   </ul>
  </div>
 </div>
 <p style="font-size:13.5px;color:#262320aa;margin-top:14px">품목 그림(접시·볼·잔)은 박스가 아니라
  <b>띠지·카드</b>에 둔다. 자주 바뀌는 정보는 자주 찍는 것에 올린다.</p>

 <h3>배송 구성 — 기본 / 쇼핑백 옵션</h3>
 <table>
  <tr><th></th><th>기본</th><th>쇼핑백 추가 (유료 옵션)</th></tr>
  <tr><td>선물 박스</td><td>크라프트 박스 + 습자지 + 세트 + 카드</td><td>동일 <b>+ 리본 묶음</b></td></tr>
  <tr><td>쇼핑백</td><td>없음</td><td><b>접은 상태로 동봉</b></td></tr>
  <tr><td>겉</td><td colspan="2">무지 택배 상자 (송장은 여기에만)</td></tr>
 </table>
 <ul>
  <li>리본은 <b>쇼핑백 옵션에서만</b> 묶는다 — 손으로 전달하는 구성에서만 필요하다</li>
  <li>쇼핑백을 펴서 넣으면 택배 부피가 커진다. <b>접어서 동봉</b>이 전제</li>
  <li>선물 박스에는 송장·가격 등 어떤 배송 정보도 붙이지 않는다</li>
 </ul>

 <h3>가격 표기</h3>
 <div class="flag">세트 가격에 <b>기본 선물포장료 3,000~4,000원이 포함</b>되어 있다는 사실을
  상품 상세와 결제 단계에 명시한다. 포장이 옵션이 아니라 상품의 일부라는 걸 먼저 말해야,
  "포장비가 왜 따로 없냐"가 아니라 "이 가격에 포장까지"로 읽힌다.</div>
 <ul>
  <li>상세페이지 — 가격 근처 한 줄 + 포장 구성 사진 섹션</li>
  <li>쇼핑백은 <b>유료 옵션</b>으로 별도 표기 (가격 미정)</li>
 </ul>

 <h3>남은 결정</h3>
 <ul class="todo">
  <li>주력 세트 실측 → 기성 크라프트 규격 확정 (S·M·L 중 몇 종으로 갈지)</li>
  <li>인쇄 범위 — 윗면만 vs 윗면 + 옆면 (단가 차이 확인)</li>
  <li>MOQ 300 기준 개당 단가·인쇄판비·리드타임 견적</li>
  <li>쇼핑백 규격·재질·인쇄 여부, 옵션 가격</li>
  <li>리본 색·폭 (잉크 2색 원칙 안에서)</li>
  <li>박스 위 일러스트 실제 원화 — 아이콘 세트에서 고르거나 새 시트로 그린다</li>
 </ul>
 <div class="flag"><b>이전 결정과 달라진 점.</b> <code>04-packaging/box-system.md</code>에는
  "무지 크라프트를 쓰지 않고 기성 <b>화이트</b> 박스에 1도 인쇄"로 적혀 있다.
  지금 계획은 <b>크라프트 + 1도</b>다. 흰 박스의 오염 리스크가 사라지고 단가가 내려가는 대신,
  1도 검정이 크라프트 위에서는 대비가 약해진다. 다만 <b>기존 모티프와 로고는 그대로 쓴다</b> —
  굵게 다시 그리지 않고, 첫 발주 전 실제 원지에 시인쇄해 확인한 뒤 뭉개지는 그림만 다른 모티프로 바꾼다.</div>
</section>

<footer>오하리상점 · b2c-gift-brand / 03-identity · 빌드: <code>python 03-identity/build_logo_guide.py</code></footer>
</div>
</html>"""

for key, val in [("{SIG}", SIG), ("{SIG_W}", SIG_W), ("{SIG_SM}", SIG_SM), ("{KO}", KO),
                 ("{EN}", EN), ("{OHARI}", OHARI), ("{KO_W}", KO_W), ("{EN_W}", EN_W),
                 ("{TURTLE}", TURTLE), ("{FILES}", FILES)]:
    HTML = HTML.replace(key, val)

out = ROOT / "logo-guide.html"
out.write_text(HTML, encoding="utf-8")
print(out)
