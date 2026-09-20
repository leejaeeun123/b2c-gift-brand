# -*- coding: utf-8 -*-
"""deck-update-0920.html 빌드 — 2026-09-20 공유용 덱.

바다 모티프 12종 · 포장 방식 확정 · 단품 판매 결정을 팀원 공유용 한 장짜리 HTML로 만든다.
SVG는 인라인, 사진은 리사이즈 후 base64로 묻는다 → 파일 하나로 공유한다.
CSS는 deck-logo-package.html의 것을 그대로 가져와 한 벌로 유지한다.
`python build_deck_0920.py`
"""
from pathlib import Path
import base64, io, re
from PIL import Image

ROOT = Path(__file__).resolve().parent
ID = ROOT / "03-identity"
REF = ROOT / "assets" / "reference"

CSS = re.search(r"<style>.*?</style>",
                (ROOT / "deck-logo-package.html").read_text(encoding="utf-8"), re.S).group(0)


def svg(name, width):
    s = (ID / (name + ".svg")).read_text(encoding="utf-8")
    s = re.sub(r'\s(width|height)="\d+"', "", s, count=2)
    return s.replace("<svg ", '<svg style="width:%s;height:auto;display:block" ' % width, 1)


def photo(path, w=1200, q=78):
    im = Image.open(path).convert("RGB")
    im.thumbnail((w, w * 2), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


SEA = ["urchin", "anemone", "starfish", "clam", "coral", "seahorse",
       "wave", "seaweed", "sea-clover", "conch", "sparkle-star", "crab"]
SEA_KO = {"urchin": "성게", "anemone": "말미잘", "starfish": "불가사리", "clam": "진주조개",
          "coral": "산호", "seahorse": "해마", "wave": "파도", "seaweed": "해초",
          "sea-clover": "바다클로버", "conch": "소라", "sparkle-star": "반짝별", "crab": "게"}
V1 = ["plate", "bowl", "cup", "spoon", "fork", "knife", "flower", "vase"]

VARS = {
    "{SIG_BIG}": svg("logo-signature-ink", "min(220px, 36vw)"),
    "{SIG}": svg("logo-signature-ink", "150px"),
    "{SIG_W}": svg("logo-signature-white", "132px"),
    "{KO}": svg("logo-wordmark-ko-ink", "100%"),
    "{SEA_GRID}": "".join(
        '<figure class="m"><div class="mstage">%s</div><figcaption>%s</figcaption></figure>'
        % (svg("motif-" + n, "100%"), SEA_KO[n]) for n in SEA),
    "{V1_ROW}": "".join('<div class="mstage sm">%s</div>' % svg("motif-" + n, "100%") for n in V1),
    "{SHEET}": photo(REF / "motif-sheet-v2-sea.png", 900, 82),
    "{P_BOX}": photo(REF / "packaging-ref-03.jpg"),
    "{P_TIE}": photo(REF / "packaging-ref-04.jpg"),
    "{P_COVER}": photo(REF / "packaging-ref-02.jpg"),
}

BODY = """<!doctype html>
<html lang="ko">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>오하리상점 2026.09.20 업데이트</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gothic+A1:wght@300;400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
__CSS__
<style>
.mgrid{display:grid;gap:12px;grid-template-columns:repeat(3,1fr);margin-top:24px}
@media(min-width:760px){.mgrid{grid-template-columns:repeat(6,1fr)}}
.mstage{background:var(--paper);border:1px solid var(--ink-14);border-radius:8px;
  padding:14px;display:flex;align-items:center;justify-content:center}
.mstage.sm{padding:9px}
.v1row{display:grid;grid-template-columns:repeat(8,1fr);gap:8px;margin-top:16px;opacity:.45}
figure.m figcaption{margin-top:6px;font-size:11.5px;text-align:center}
.shot{width:100%;height:auto;display:block;border-radius:8px;border:1px solid var(--ink-14)}
.shots{display:grid;gap:14px;margin-top:22px}
@media(min-width:760px){.shots.two{grid-template-columns:1fr 1fr}}
.steps{margin-top:24px;display:grid;gap:10px}
.step{display:grid;grid-template-columns:auto 1fr;gap:16px;align-items:baseline;
  padding:15px 20px;background:var(--paper);border:1px solid var(--ink-14);border-radius:8px}
.step b{font:500 13px/1 'IBM Plex Mono',monospace;color:var(--ink-45)}
.step p{margin:0}
</style>

<section class="slide cover">
  <span class="num">01 / 09</span>
  <div class="inner">
    <div>
      <div class="eyebrow">2026.09.20 · 오하리상점</div>
      <h1>바다 모티프 12종,<br>포장 방식 확정,<br>단품 판매</h1>
      <p class="big" style="margin-top:22px">일러스트 정본이 28종으로 늘었고, 박스 안을 어떻게
        싸는지가 공정 단위로 정해졌습니다. 그리고 세트 구성품을 낱개로도 팔기로 했습니다.</p>
      <div class="meta">
        <span class="chip solid">일러스트 +12</span>
        <span class="chip solid">포장 확정</span>
        <span class="chip">원지 화이트 복귀</span>
        <span class="chip">단품 판매 개방</span>
      </div>
    </div>
    <div class="cover-mark">{SIG_BIG}</div>
  </div>
</section>

<section class="slide">
  <span class="num">02 / 09</span>
  <div class="inner">
    <div class="eyebrow">변경 없음 · 정본</div>
    <h2>로고는 그대로입니다</h2>
    <p>9월 13일에 확정한 시그니처 로고와 워드마크를 그대로 씁니다. 손글씨 스캔을 벡터로 뜬
      아웃라인 패스라 폰트 의존성이 없고, 잉크 · 화이트 두 벌이 준비돼 있습니다.</p>
    <div class="trio" style="margin-top:26px">
      <figure><div class="stage">{SIG}</div><figcaption>시그니처 · 잉크</figcaption></figure>
      <figure><div class="stage dark">{SIG_W}</div><figcaption>시그니처 · 화이트</figcaption></figure>
      <figure><div class="stage">{KO}</div><figcaption>한글 워드마크</figcaption></figure>
    </div>
    <div class="note">이번에 바뀐 건 로고가 아니라 <strong>그 옆에 놓일 그림의 수</strong>와
      <strong>박스를 싸는 방법</strong>입니다.</div>
  </div>
</section>

<section class="slide">
  <span class="num">03 / 09</span>
  <div class="inner">
    <div class="eyebrow">일러스트 · 신규</div>
    <h2>바다 모티프 12종</h2>
    <p>두 번째 레퍼런스 시트를 벡터로 떴습니다. 여름 시즌 · 해산물 품목 · 아동 선물 쪽으로
      넓힐 때 쓰는 세트입니다. 기본 세트는 여전히 1차 16종입니다.</p>
    <div class="mgrid">{SEA_GRID}</div>
    <div class="v1row">{V1_ROW}</div>
    <div class="note">획 두께 기준이 1차 시트와 같아서 <strong>둘을 한 화면에 섞어도 같은 손</strong>으로 보입니다.
      아래 흐린 줄이 기존 16종 중 일부입니다.</div>
  </div>
</section>

<section class="slide">
  <span class="num">04 / 09</span>
  <div class="inner">
    <div class="eyebrow">고르는 방식</div>
    <h2>16칸 중 12칸만 들였습니다</h2>
    <div class="cols side" style="margin-top:22px;align-items:start">
      <div><img class="shot" src="{SHEET}" alt="바다 모티프 레퍼런스 시트"></div>
      <div>
        <p>시트에서 <strong>파란 X를 그은 4칸은 벡터화하지 않았습니다.</strong>
          거북이 · 물고기 · 하트는 1차 시트에 이미 정본이 있어 겹치고, 리본은 포장에서
          실물로 쓰기 때문에 그림으로 또 쓰지 않습니다.</p>
        <ul>
          <li class="no">거북이 · 물고기 · 하트 — 1차 시트와 중복</li>
          <li class="no">리본 — 실물로 쓰는 것은 그리지 않는다</li>
          <li class="yes">이름이 겹치는 둘은 구분 — 클로버 · 별 ↔ 바다클로버 · 반짝별</li>
        </ul>
        <div class="note">형태는 손이 정하고 코드는 <strong>따기만</strong> 합니다.
          선의 떨림과 비대칭이 그대로 남습니다.</div>
      </div>
    </div>
  </div>
</section>

<section class="slide">
  <span class="num">05 / 09</span>
  <div class="inner">
    <div class="eyebrow">패키지 · 번복</div>
    <h2>크라프트에서 다시 화이트로</h2>
    <div class="cols two" style="margin-top:20px;align-items:start">
      <div>
        <p>9월 13일에 크라프트로 바꿨다가 <strong>흰색 박스로 되돌립니다.</strong>
          크라프트 위 검정 1도는 대비가 약해 시인쇄로 확인해야 했고, 뭉개지는 그림은
          골라내야 했습니다. 화이트에서는 그 제약이 통째로 사라집니다.</p>
        <div class="note">흰 박스의 약점(오염 · 찍힘)은 이미 막혀 있습니다 —
          <strong>겉에 무지 택배 상자를 따로 씌우기로</strong> 했으니 흰 박스는 운송을 겪지 않습니다.</div>
      </div>
      <div class="scroll"><table>
        <thead><tr><th></th><th>크라프트 9/13</th><th>화이트 9/20</th></tr></thead>
        <tbody>
          <tr><th>검정 대비</th><td>약하다</td><td><strong>강하다</strong></td></tr>
          <tr><th>쓸 수 있는 모티프</th><td>골라 써야 한다</td><td><strong>28종 전부</strong></td></tr>
          <tr><th>오염 · 찍힘</th><td>안 보인다</td><td>겉 상자로 방어</td></tr>
          <tr><th>속 습자지와</th><td>톤이 붙는다</td><td><strong>대비된다</strong></td></tr>
        </tbody>
      </table></div>
    </div>
  </div>
</section>

<section class="slide">
  <span class="num">06 / 09</span>
  <div class="inner">
    <div class="eyebrow">박스 안 · 확정</div>
    <h2>한 점씩 따로 쌉니다</h2>
    <p>세트를 통째로 습자지에 넣지 않습니다. <strong>상품 하나하나가 각각 하나의 선물</strong>이 되게 합니다.</p>
    <div class="steps">
      <div class="step"><b>01</b><p>뽁뽁이로 개별 포장 — 완충은 여기서 끝낸다</p></div>
      <div class="step"><b>02</b><p>그 위를 습자지로 감싼다 — <strong>보이는 표면은 전부 종이</strong></p></div>
      <div class="step"><b>03</b><p><strong>검정 마끈</strong>으로 십자로 묶고 리본 매듭</p></div>
      <div class="step"><b>04</b><p><strong>같은 높이</strong>로 나란히 담는다 — 낮은 품목은 습자지를 더 감아 높이를 맞춘다</p></div>
      <div class="step"><b>05</b><p>위를 습자지로 덮는다 — 뚜껑을 열면 종이 한 겹을 먼저 걷는다</p></div>
    </div>
  </div>
</section>

<section class="slide">
  <span class="num">07 / 09</span>
  <div class="inner">
    <div class="eyebrow">참조 · 이렇게 보이게</div>
    <h2>열었을 때의 화면</h2>
    <div class="shots two">
      <figure><img class="shot" src="{P_TIE}" alt="개별 포장과 마끈 리본">
        <figcaption>개별 꾸러미 + 십자 마끈 · 빈 자리는 구긴 습자지</figcaption></figure>
      <figure><img class="shot" src="{P_BOX}" alt="같은 높이 정렬과 카드">
        <figcaption>같은 높이로 정렬 · 카드는 꾸러미 위에</figcaption></figure>
    </div>
    <div class="shots">
      <figure><img class="shot" src="{P_COVER}" alt="덮는 습자지">
        <figcaption>맨 위를 습자지로 덮어 감싼다 — 뚜껑 다음의 한 겹</figcaption></figure>
    </div>
    <div class="note">참조 사진은 <strong>갈색 마끈 · 크라프트 박스</strong>지만
      우리는 <strong>검정 마끈 · 흰 박스</strong>입니다. 가져오는 건 색이 아니라
      <strong>낱개로 싸서 같은 높이로 담는 방식</strong>입니다.</div>
  </div>
</section>

<section class="slide">
  <span class="num">08 / 09</span>
  <div class="inner">
    <div class="eyebrow">헷갈리기 쉬운 것</div>
    <h2>마끈과 리본은 다른 물건입니다</h2>
    <div class="scroll" style="margin-top:20px"><table>
      <thead><tr><th></th><th>마끈</th><th>리본</th></tr></thead>
      <tbody>
        <tr><th>자리</th><td>박스 <strong>안</strong> · 상품 개별 포장</td><td>박스 <strong>바깥</strong>을 두르는 장식</td></tr>
        <tr><th>언제</th><td><strong>항상</strong> — 기본 포장에 포함</td><td><strong>쇼핑백 유료 옵션에서만</strong></td></tr>
        <tr><th>색 · 재질</th><td>검정 마끈(지끈) · 거친 결</td><td>미정 — 잉크 2색 원칙 안에서</td></tr>
      </tbody>
    </table></div>
    <div class="cols two" style="margin-top:26px;align-items:start">
      <div>
        <h3>왜 검정인가</h3>
        <p>잉크(#262320) 계열이라 2색 원칙 안에 그대로 들어옵니다. 매끈한 리본 끈이 아니라
          거친 결의 마끈이 손그림 톤과 맞습니다.</p>
      </div>
      <div>
        <h3>포장료 3,000~4,000원의 근거</h3>
        <p>점당 3공정(에어캡 · 습자지 · 마끈)이라 세트 4~6점이면 실제로 그만큼 손이 들어갑니다.
          <strong>이 공정 자체를 상세페이지에 사진으로</strong> 보여 줍니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="slide">
  <span class="num">09 / 09</span>
  <div class="inner">
    <div class="eyebrow">상품 구성 · 변경</div>
    <h2>단품도 팝니다</h2>
    <p class="big">세트 구성품을 낱개로도 엽니다. 다만 <strong>단품 경쟁은 여전히 하지 않습니다</strong> —
      같은 그릇 한 점을 값으로 겨루면 제조사에게 집니다.</p>
    <div class="cols two" style="margin-top:24px;align-items:start">
      <div class="card">
        <h3>왜 여는가</h3>
        <ul>
          <li class="yes">재고 — 덜 팔린 조합의 구성품을 푸는 유일한 밸브</li>
          <li class="yes">손님 — "하나만" · 깨져서 보충 · 소액 재구매</li>
          <li class="yes">진입 단가 — 3만 원 문턱 앞의 시험 구매를 받는다</li>
        </ul>
      </div>
      <div class="card">
        <h3>가드레일 4개</h3>
        <ul>
          <li class="no">단품가 합이 세트가보다 싸지는 것 — 세트가 항상 이득(+10~15%)</li>
          <li class="no">포장 손이 상품가를 넘는 소품의 낱개 판매 — 2점 이상 묶음으로</li>
          <li class="no">단품 전용 사입 — 세트에 이미 든 품목만</li>
          <li class="no">가격 비교 채널 노출 · 포장 등급 낮추기</li>
        </ul>
      </div>
    </div>
    <div class="note">자리도 나눕니다 — 세트는 <strong>상황 라벨 안의 1차 진열</strong>,
      단품은 <strong>세트 상세 하단과 전용 페이지</strong>. 낱개를 주장으로 삼지는 않습니다.</div>
  </div>
</section>

<footer class="slide">
  <div class="inner">
    <span>오하리상점 · b2c-gift-brand</span>
    <span>2026.09.20</span>
  </div>
</footer>
</html>"""

html = BODY.replace("__CSS__", CSS)
for k, v in VARS.items():
    html = html.replace(k, v)
out = ROOT / "deck-update-0920.html"
out.write_text(html, encoding="utf-8")
print(out, "%.1f MB" % (out.stat().st_size / 1e6))
