# -*- coding: utf-8 -*-
"""deck-logo-package.html 빌드 — 2026-09-13 로고 확정 + 패키지 계획 공유용 덱.

03-identity의 SVG를 인라인해 단일 파일로 만든다. 링크 하나로 공유한다.
`python build_deck_0913.py`
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
ID = ROOT / "03-identity"


def svg(name, width, invert=False):
    s = (ID / (name + ".svg")).read_text(encoding="utf-8")
    s = re.sub(r'\s(width|height)="\d+"', "", s, count=2)
    return s.replace("<svg ", '<svg style="width:%s;height:auto;display:block" ' % width, 1)


SIG = svg("logo-signature-ink", "170px")
SIG_W = svg("logo-signature-white", "150px")
SIG_BIG = svg("logo-signature-ink", "min(240px, 38vw)")
SIG_SM = svg("logo-signature-ink", "58px")
KO = svg("logo-wordmark-ko-ink", "100%")
EN = svg("logo-wordmark-en-ink", "100%")
OHARI = svg("logo-wordmark-ohari-ink", "100%")
TURTLE = svg("char-turtle", "132px")

HTML = """<!doctype html>
<html lang="ko">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>오하리상점 로고 확정</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gothic+A1:wght@300;400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{
  --ink:#262320;
  --ink-70:rgba(38,35,32,.70);
  --ink-45:rgba(38,35,32,.45);
  --ink-14:rgba(38,35,32,.14);
  --ink-07:rgba(38,35,32,.07);
  --paper:#FFFFFF;
  --ground:#EFEAE0;
  --kraft:#C6A57B;
  --kraft-soft:#E4D3B8;
  color-scheme:light;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{
  margin:0;background:var(--ground);color:var(--ink);
  font:400 16px/1.7 'Gothic A1','Pretendard','Apple SD Gothic Neo',system-ui,sans-serif;
  -webkit-font-smoothing:antialiased;
  scroll-snap-type:y proximity;
}
.slide{
  min-height:100svh;scroll-snap-align:start;
  display:flex;flex-direction:column;justify-content:center;
  padding:clamp(40px,7vh,88px) clamp(24px,6vw,88px);
  border-bottom:1px solid var(--ink-14);position:relative;
}
.slide>.inner{width:100%;max-width:1080px;margin:0 auto}
.num{
  position:absolute;top:clamp(22px,4vh,40px);right:clamp(24px,6vw,56px);
  font:500 12px/1 'IBM Plex Mono',ui-monospace,monospace;letter-spacing:.14em;
  color:var(--ink-45);font-variant-numeric:tabular-nums;
}
.eyebrow{
  font:500 12px/1 'IBM Plex Mono',ui-monospace,monospace;letter-spacing:.18em;
  text-transform:uppercase;color:var(--ink-45);margin-bottom:20px;
}
h1{font-size:clamp(30px,5.2vw,52px);line-height:1.22;font-weight:700;margin:0;
   letter-spacing:-.02em;text-wrap:balance}
h2{font-size:clamp(24px,3.4vw,36px);line-height:1.28;font-weight:700;margin:0 0 14px;
   letter-spacing:-.02em;text-wrap:balance}
h3{font-size:15px;font-weight:700;margin:0 0 10px;letter-spacing:-.01em}
p{margin:0 0 14px;max-width:62ch;color:var(--ink-70)}
p.big{font-size:clamp(17px,2vw,20px);color:var(--ink);max-width:52ch}
strong{font-weight:700;color:var(--ink)}
.cols{display:grid;gap:clamp(20px,3vw,44px);align-items:center}
@media(min-width:860px){.cols.two{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
 .cols.side{grid-template-columns:minmax(0,340px) minmax(0,1fr)}}
.card{background:var(--paper);border:1px solid var(--ink-14);border-radius:8px;
  padding:clamp(22px,3vw,34px)}
.card.dark{background:var(--ink);color:var(--paper);border-color:transparent}
.card.kraft{background:var(--kraft-soft);border-color:rgba(38,35,32,.12)}
.stage{background:var(--paper);border:1px solid var(--ink-14);border-radius:8px;
  display:flex;align-items:center;justify-content:center;padding:clamp(26px,4vw,44px);
  min-height:210px}
.stage.dark{background:var(--ink);border-color:transparent}
.stage.kraft{background:var(--kraft-soft);border-color:rgba(38,35,32,.12)}
.trio{display:grid;gap:16px}
@media(min-width:760px){.trio{grid-template-columns:repeat(3,1fr)}}
.trio .stage{min-height:150px;padding:26px;flex:1}
.trio figure{display:flex;flex-direction:column;height:100%}
figure{margin:0}
figcaption{margin-top:9px;font-size:12.5px;color:var(--ink-45);letter-spacing:.01em}
dl.spec{display:grid;gap:2px 28px;margin:24px 0 0;
  grid-template-columns:repeat(auto-fit,minmax(140px,1fr))}
dl.spec div{padding:14px 0;border-top:1px solid var(--ink-14)}
dl.spec dt{font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-45);font-family:'IBM Plex Mono',monospace}
dl.spec dd{margin:6px 0 0;font-size:15px;font-weight:500;font-variant-numeric:tabular-nums}
table{width:100%;border-collapse:collapse;font-size:15px}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
th,td{text-align:left;padding:13px 14px;border-bottom:1px solid var(--ink-14);
  vertical-align:top}
thead th{font:500 11.5px/1 'IBM Plex Mono',monospace;letter-spacing:.12em;
  text-transform:uppercase;color:var(--ink-45);padding-bottom:10px}
tbody th{font-weight:700;white-space:nowrap;width:1%}
td{color:var(--ink-70)}
td strong{color:var(--ink)}
ul{margin:0;padding:0;list-style:none}
li{padding:9px 0 9px 26px;position:relative;border-bottom:1px solid var(--ink-07);
  color:var(--ink-70)}
li:last-child{border-bottom:0}
li.yes:before,li.no:before{position:absolute;left:0;top:9px;font-weight:700;
  font-family:'IBM Plex Mono',monospace}
li.yes:before{content:"+";color:var(--ink)}
li.no:before{content:"\\2212";color:var(--ink-45)}
li.todo:before{content:"";position:absolute;left:2px;top:17px;width:10px;height:10px;
  border:1.5px solid var(--ink-45);border-radius:2px}
li.todo{padding-left:26px}
.note{border-left:2px solid var(--ink);padding:4px 0 4px 20px;margin:22px 0 0;
  font-size:15px;color:var(--ink-70);max-width:66ch}
.note strong{color:var(--ink)}
.chip{display:inline-block;font-size:12.5px;font-weight:500;letter-spacing:.01em;
  padding:7px 15px;border:1px solid var(--ink-14);border-radius:99px;color:var(--ink-45)}
.chip.solid{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.meta{display:flex;gap:10px;flex-wrap:wrap;margin-top:28px}
code{font:500 13px/1.5 'IBM Plex Mono',ui-monospace,monospace;
  background:var(--ink-07);padding:2px 6px;border-radius:3px;color:var(--ink)}
.filelist{font-family:'IBM Plex Mono',monospace;font-size:13.5px}
.filelist td{padding:10px 14px}
.layers{display:grid;gap:14px}
.layer{display:grid;grid-template-columns:auto 1fr;gap:18px;align-items:start;
  padding:20px 22px;border-radius:8px;border:1px solid var(--ink-14);background:var(--paper)}
.layer .tag{font-size:12px;font-weight:700;color:var(--ink-45);white-space:nowrap;
  padding-top:3px;min-width:24px}
.layer.inner{background:var(--kraft-soft);border-color:rgba(38,35,32,.12)}
.cover .inner{display:grid;gap:clamp(28px,5vw,60px);align-items:center}
@media(min-width:860px){.cover .inner{grid-template-columns:minmax(0,1fr) auto}}
.cover-mark{display:flex;justify-content:center}
footer.slide{min-height:auto;padding-top:40px;padding-bottom:40px;border-bottom:0}
footer .inner{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;
  font:500 12px/1.6 'IBM Plex Mono',monospace;color:var(--ink-45);letter-spacing:.06em}
</style>

<section class="slide cover">
  <span class="num">01 / 10</span>
  <div class="inner">
    <div>
      <div class="eyebrow">2026.09.13 · 오하리상점</div>
      <h1>로고 확정과<br>패키지 가는 길</h1>
      <p class="big" style="margin-top:22px">손글씨 스캔을 벡터로 뜨고, 거북이를 심볼로 세워
        시그니처 로고를 확정했습니다. 이어서 크라프트 박스 1도 인쇄로 패키지 방향을 잡았습니다.</p>
      <div class="meta">
        <span class="chip solid">로고 확정</span>
        <span class="chip">패키지 계획 단계</span>
        <span class="chip">디자인 미착수</span>
      </div>
    </div>
    <div class="cover-mark">{SIG_BIG}</div>
  </div>
</section>

<section class="slide">
  <span class="num">02 / 10</span>
  <div class="inner">
    <div class="eyebrow">확정 · 정본</div>
    <h2>시그니처 로고</h2>
    <p>거북이 아래 손글씨 영문 OHARI를 놓은 세로 락업. 브랜드를 한 덩어리로 보여야 하는
      모든 자리에 이것을 씁니다.</p>
    <div class="trio" style="margin-top:26px">
      <figure><div class="stage">{SIG}</div><figcaption>잉크 · 흰 바탕</figcaption></figure>
      <figure><div class="stage dark">{SIG_W}</div><figcaption>화이트 · 어두운 바탕</figcaption></figure>
      <figure><div class="stage kraft">{SIG_SM}</div><figcaption>58px · 크라프트 위 축소</figcaption></figure>
    </div>
    <dl class="spec">
      <div><dt>거북이 폭</dt><dd>워드마크의 95%</dd></div>
      <div><dt>간격</dt><dd>거북이 잉크 높이의 24%</dd></div>
      <div><dt>정렬</dt><dd>잉크 바운딩박스 가운데</dd></div>
      <div><dt>비율</dt><dd>634 : 686</dd></div>
      <div><dt>색</dt><dd>#262320 / #FFFFFF</dd></div>
    </dl>
  </div>
</section>

<section class="slide">
  <span class="num">03 / 10</span>
  <div class="inner">
    <div class="eyebrow">기준선</div>
    <h2>박스가 아니라 잉크에 맞춘다</h2>
    <div class="cols two" style="margin-top:24px">
      <div>
        <p>거북이 SVG에는 아래쪽에 빈 여백이 약 25% 붙어 있습니다. 파일 박스를 기준으로 맞추면
          글씨가 실제보다 멀어 보입니다. 그래서 <strong>잉크가 실제로 그려진 영역</strong>을
          기준으로 간격과 가운데 정렬을 계산했습니다.</p>
        <p>간격은 26% → 12% → 24%를 거쳐 확정했습니다. 기준을 바꾸기 전 12%가
          기준을 바꾼 뒤의 62%에 해당했습니다. 같은 숫자가 다른 뜻이었던 셈입니다.</p>
        <div class="note">재조합이 필요하면 <code>gen_signature.py</code>를 돌립니다.
          확정 비율이 스크립트 안에 들어 있어 손으로 다시 맞출 일이 없습니다.</div>
      </div>
      <div class="stage">{TURTLE}</div>
    </div>
  </div>
</section>

<section class="slide">
  <span class="num">04 / 10</span>
  <div class="inner">
    <div class="eyebrow">워드마크</div>
    <h2>셋 다 같은 손글씨에서 나왔다</h2>
    <p>다시 쓴 글씨가 아니라 원본 스캔의 획 그대로입니다. 글리프 사이 공백을 잘라
      한글 · 영문 · OHARI 세 벌로 나눴습니다.</p>
    <div class="trio" style="margin-top:26px">
      <figure><div class="stage">{KO}</div><figcaption>오하리상점 — 사이트 · 상세 · 명함</figcaption></figure>
      <figure><div class="stage">{EN}</div><figcaption>OHARISTORE — 띠지 · 테이프</figcaption></figure>
      <figure><div class="stage">{OHARI}</div><figcaption>OHARI — 시그니처 구성 요소</figcaption></figure>
    </div>
  </div>
</section>

<section class="slide">
  <span class="num">05 / 10</span>
  <div class="inner">
    <div class="eyebrow">파일</div>
    <h2>내려받아 바로 쓰는 상태</h2>
    <p>전부 아웃라인 패스라 폰트 의존성이 없습니다. 잉크 · 화이트 두 벌씩 준비돼 있습니다.</p>
    <div class="cols two" style="margin-top:24px;align-items:start">
      <div class="card" style="padding:8px 10px">
        <div class="scroll"><table class="filelist">
          <tbody>
            <tr><th>logo-signature-{ink,white}</th><td>시그니처 로고</td></tr>
            <tr><th>logo-wordmark-ko-{ink,white}</th><td>오하리상점</td></tr>
            <tr><th>logo-wordmark-en-{ink,white}</th><td>OHARISTORE</td></tr>
            <tr><th>logo-wordmark-ohari-{ink,white}</th><td>OHARI</td></tr>
            <tr><th>char-turtle</th><td>거북이 심볼</td></tr>
          </tbody>
        </table></div>
      </div>
      <div>
        <h3>쓰는 자리</h3>
        <ul>
          <li class="yes">박스 뚜껑 · 스티커 · 파비콘 — 시그니처 로고</li>
          <li class="yes">사이트 헤더 · 상세페이지 — 한글 워드마크</li>
          <li class="yes">가로로 길고 낮은 자리 — 영문 워드마크</li>
          <li class="no">거북이를 다른 모티프로 바꿔 락업 만들기</li>
          <li class="no">한글과 영문을 임의로 두 줄 조합하기</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="slide">
  <span class="num">06 / 10</span>
  <div class="inner">
    <div class="eyebrow">패키지 · 방향</div>
    <h2>화이트에서 크라프트로</h2>
    <div class="cols two" style="margin-top:20px;align-items:start">
      <div>
        <p>8월 30일에는 기성 <strong>화이트</strong> 박스에 1도 인쇄로 정했습니다.
          오늘 <strong>크라프트</strong>로 바꿉니다. 오염과 찍힘이 안 보이고 단가가 내려갑니다.</p>
        <div class="note"><strong>대가가 하나 있습니다.</strong> 크라프트 위에서 검정 1도는
          대비가 약합니다. 그래도 그림을 굵게 다시 그리지는 않습니다 —
          첫 발주 전 실제 원지에 시인쇄해 보고, 뭉개지는 그림만 다른 모티프로 바꿉니다.
          선 굵기를 손대는 게 아니라 <strong>고르는 걸로</strong> 해결합니다.</div>
      </div>
      <div class="scroll"><table>
        <thead><tr><th></th><th>화이트 8/30</th><th>크라프트 9/13</th></tr></thead>
        <tbody>
          <tr><th>오염 · 찍힘</th><td>잘 보인다</td><td><strong>거의 안 보인다</strong></td></tr>
          <tr><th>단가</th><td>높다</td><td><strong>낮다</strong></td></tr>
          <tr><th>검정 대비</th><td><strong>강하다</strong></td><td>약하다</td></tr>
          <tr><th>톤</th><td>깔끔 · 담백</td><td>선물 · 수공예</td></tr>
        </tbody>
      </table></div>
    </div>
    <dl class="spec">
      <div><dt>인쇄</dt><dd>1도 · 윗면 또는 윗면+옆면</dd></div>
      <div><dt>MOQ</dt><dd>약 300개~</dd></div>
      <div><dt>규격</dt><dd>기성 · 목형비 없음</dd></div>
      <div><dt>올라가는 것</dt><dd>아이콘 일러스트 + 로고</dd></div>
    </dl>
  </div>
</section>

<section class="slide">
  <span class="num">07 / 10</span>
  <div class="inner">
    <div class="eyebrow">구조</div>
    <h2>두 겹으로 간다</h2>
    <p>선물 박스는 배송 상자가 아닙니다. 운송에서 생기는 일은 전부 겉 상자가 받습니다.</p>
    <div class="layers" style="margin-top:26px">
      <div class="layer">
        <span class="tag">겉</span>
        <div><h3>무지 택배 상자</h3>
          <p style="margin:0">운송 · 송장 · 완충. 찍힘과 오염을 여기서 다 받는다.
            송장은 오직 여기에만 붙는다.</p></div>
      </div>
      <div class="layer inner">
        <span class="tag">안</span>
        <div><h3>크라프트 선물 박스 · 1도 인쇄</h3>
          <p style="margin:0">브랜드. 받는 사람이 여는 것. 안에 습자지와 세트, 카드가 들어간다.
            배송 정보는 아무것도 붙이지 않는다.</p></div>
      </div>
    </div>
    <div class="note">두 번 여는 건 손해가 아니라 <strong>선물의 문법</strong>입니다.
      포장을 뜯는 행위 자체가 선물이니까요.</div>
  </div>
</section>

<section class="slide">
  <span class="num">08 / 10</span>
  <div class="inner">
    <div class="eyebrow">박스 위의 그림</div>
    <h2>300개가 정하는 기준</h2>
    <p class="big">한 번 찍으면 오래 씁니다. 그 사이에 취급 분야가 그릇에서 문구류로 넓어져도
      그대로 쓸 수 있어야 합니다.</p>
    <div class="cols two" style="margin-top:26px;align-items:start">
      <div class="card">
        <h3>쓴다 — 선물이라는 행위</h3>
        <ul>
          <li class="yes">선물 상자 · 리본 · 편지 · 손 · 하트 · 별 · 클로버 · 꽃</li>
          <li class="yes">거북이, 박스당 하나</li>
          <li class="yes">기존 모티프 정본 그대로 · 같은 크기 그리드</li>
        </ul>
      </div>
      <div class="card">
        <h3>피한다 — 지금 파는 물건</h3>
        <ul>
          <li class="no">접시 · 볼 · 수저처럼 품목을 특정하는 그림을 주인공으로</li>
          <li class="no">박스를 꽉 채우는 패턴</li>
          <li class="no">시즌 · 연도가 박히는 요소</li>
        </ul>
      </div>
    </div>
    <div class="note">품목 그림은 박스가 아니라 <strong>띠지와 카드</strong>에 둡니다.
      자주 바뀌는 정보는 자주 찍는 것에 올립니다.</div>
  </div>
</section>

<section class="slide">
  <span class="num">09 / 10</span>
  <div class="inner">
    <div class="eyebrow">배송 구성 · 가격</div>
    <h2>기본과 쇼핑백 옵션</h2>
    <div class="scroll" style="margin-top:20px"><table>
      <thead><tr><th></th><th>기본</th><th>쇼핑백 추가 · 유료 옵션</th></tr></thead>
      <tbody>
        <tr><th>선물 박스</th><td>크라프트 박스 + 습자지 + 세트 + 카드</td>
          <td>동일 <strong>+ 리본 묶음</strong></td></tr>
        <tr><th>쇼핑백</th><td>없음</td><td><strong>접은 상태로 동봉</strong></td></tr>
        <tr><th>겉</th><td colspan="2">무지 택배 상자 · 송장은 여기에만</td></tr>
      </tbody>
    </table></div>
    <div class="cols two" style="margin-top:26px;align-items:start">
      <div>
        <h3>왜 리본은 옵션에만</h3>
        <p>리본은 손으로 건넬 때 필요한 마감입니다. 택배로만 갈 구성에 묶으면
          상자 안에서 눌려서 도착합니다.</p>
      </div>
      <div>
        <h3>포장료는 포함이다</h3>
        <p>세트 가격에 <strong>기본 선물포장료 3,000~4,000원이 포함</strong>돼 있다고
          상세와 결제 단계에 명시합니다. 먼저 말해야
          "포장비가 왜 따로 없냐"가 아니라 <strong>"이 가격에 포장까지"</strong>로 읽힙니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="slide">
  <span class="num">10 / 10</span>
  <div class="inner">
    <div class="eyebrow">다음</div>
    <h2>견적 전에 손으로 할 것</h2>
    <ul style="margin-top:22px;max-width:74ch">
      <li class="todo">주력 세트 실측 → 기성 크라프트 규격 확정 (한 사이즈인지, S·M·L인지)</li>
      <li class="todo">인쇄 범위 — 윗면만 vs 윗면 + 옆면, 단가 차이 확인</li>
      <li class="todo">MOQ 300 기준 개당 단가 · 인쇄판비 · 리드타임 견적</li>
      <li class="todo">박스에 올릴 모티프 선택 + 크라프트 시인쇄로 뭉개짐 확인</li>
      <li class="todo">쇼핑백 규격 · 재질 · 인쇄 여부 · 옵션 가격</li>
      <li class="todo">리본 색 · 폭 — 잉크 2색 원칙 안에서</li>
    </ul>
    <div class="note">규격은 추정하지 않습니다. 도매 상가에서 실제로 살 접시와 볼을 재고,
      주력 세트를 한 번 담아 본 뒤 기성 규격표에서 고릅니다.</div>
  </div>
</section>

<footer class="slide">
  <div class="inner">
    <span>오하리상점 · b2c-gift-brand</span>
    <span>2026.09.13</span>
  </div>
</footer>
</html>"""

for key, val in [("{SIG_BIG}", SIG_BIG), ("{SIG_W}", SIG_W), ("{SIG_SM}", SIG_SM),
                 ("{SIG}", SIG), ("{KO}", KO), ("{EN}", EN), ("{OHARI}", OHARI),
                 ("{TURTLE}", TURTLE)]:
    HTML = HTML.replace(key, val)

out = ROOT / "deck-logo-package.html"
out.write_text(HTML, encoding="utf-8")
print(out)
