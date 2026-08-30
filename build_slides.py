# -*- coding: utf-8 -*-
"""deck-slides.html 빌드 — 발표용 16:9 슬라이드 덱. 03-identity의 SVG를 인라인해 단일 파일로 만든다.

deck.html(읽는 문서)과 별개다. 이쪽은 말하면서 넘기는 장표다.
재현: python build_slides.py
"""
import io, os, re

D = os.path.dirname(os.path.abspath(__file__))
ID = os.path.join(D, "03-identity")


def svg(name, cls=""):
    s = io.open(os.path.join(ID, name + ".svg"), encoding="utf-8").read()
    s = re.sub(r'\s(width|height|color)="[^"]*"', "", s)
    s = s.replace("<svg ", '<svg class="ico %s" ' % cls, 1)
    s = re.sub(r"<title>.*?</title>", "", s, flags=re.S)
    return s.strip()


MOTIFS = ["plate", "bowl", "cup", "spoon", "fork", "knife", "flower", "vase",
          "candle", "ribbon", "book", "heart", "clover", "star", "fish", "pear"]

CSS = u"""
:root{--ink:#1F1C19;--paper:#F7F3EC;--muted:#8C8177;--line:#DDD5C8;--soft:#E8E1D5;--card:#FFF}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:#15120F;overflow:hidden;
  font-family:Pretendard,'Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif;
  -webkit-font-smoothing:antialiased}
#stage{position:fixed;inset:0;display:grid;place-items:center}
.slide{position:absolute;width:1280px;height:720px;background:var(--paper);color:var(--ink);
  padding:56px 60px;display:none;flex-direction:column;transform-origin:center center}
.slide.on{display:flex}
.slide.dark{background:var(--ink);color:var(--paper)}
.num{font-size:13px;font-weight:700;letter-spacing:.18em;color:var(--muted);margin-bottom:8px}
h1{font-size:38px;font-weight:800;letter-spacing:-.02em;line-height:1.2}
.dark h1{color:var(--paper)}
.lead{margin-top:14px;font-size:16px;line-height:1.65;color:var(--muted);max-width:1000px}
.dark .lead{color:#D6CFC5}
.body{flex:1;margin-top:26px;display:flex;flex-direction:column;justify-content:center;gap:0}
.cards{display:grid;gap:16px}
/* 본문 묶음을 세로 가운데로 — 위아래 여백을 균등하게 */
.c{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:26px 26px;
  display:flex;flex-direction:column}
.c>.k.foot{margin-top:auto;margin-bottom:0;padding-top:14px;color:#6E6559}
.dark .c>.k.foot,.c.fill>.k.foot{color:#A79E92}
.c>p{flex:0 0 auto}
.dark .c{background:#2C2825;border-color:#3A3531}
.c.fill{background:var(--ink);border-color:var(--ink);color:var(--paper)}
.dark .c.fill{background:var(--paper);color:var(--ink)}
.c h3{font-size:20px;font-weight:800;margin-bottom:8px}
.c .k{font-size:12px;font-weight:700;letter-spacing:.1em;color:var(--muted);margin-bottom:6px}
.c p{font-size:14.5px;line-height:1.6;color:#3D3833}
.c.fill p,.dark .c p{color:#CFC7BB}
.dark .c.fill p{color:#3D3833}
.big{font-size:36px;font-weight:800;line-height:1.1;letter-spacing:-.02em}
table{width:100%;border-collapse:collapse;font-size:14.5px}
td,th{padding:19px 14px;text-align:left;vertical-align:middle;line-height:1.62}
th{font-size:12px;font-weight:700;letter-spacing:.08em;color:var(--muted);border-bottom:1px solid var(--line)}
tbody tr+tr td{border-top:1px solid var(--line)}
td.k{width:180px;font-weight:700;color:var(--muted)}
.dark td{color:#D6CFC5}.dark td.k{color:#A79E92}
.dark tbody tr+tr td{border-color:#332F2B}
.note{margin-top:20px;font-size:13.5px;line-height:1.6;color:#6E6559}
.dark .note{color:#A79E92}
.bar{background:var(--soft);border-radius:8px;padding:16px 20px;font-size:15px;font-weight:700;line-height:1.5}
.dark .bar{background:#2C2825;color:var(--paper)}
.quote{font-size:26px;font-weight:800;line-height:1.5;letter-spacing:-.02em;
  border-left:4px solid currentColor;padding-left:20px}
.ico{width:100%;height:100%;fill:currentColor;fill-rule:evenodd;display:block}
.mark{position:absolute;right:56px;bottom:44px;width:74px;height:74px;opacity:.13}
.dark .mark{opacity:.2}
.hero{position:absolute;right:74px;top:150px;width:300px;height:300px;opacity:.19;z-index:0}
.slide>.body,.slide>.note{position:relative;z-index:1}
.grid16{display:grid;grid-template-columns:repeat(8,1fr);gap:6px}
.grid16 span{border:1px solid var(--line);border-radius:8px;padding:8px;aspect-ratio:1}
.row{display:flex;gap:14px;align-items:stretch}
.step{display:flex;align-items:center;gap:22px;background:var(--card);border:1px solid var(--line);
  border-radius:10px;padding:24px 26px}
.step.fill{background:var(--ink);border-color:var(--ink);color:var(--paper)}
.step .n{font-size:34px;font-weight:800;color:var(--line);width:38px;text-align:center;flex:none}
.step.fill .n{color:var(--paper)}
.pill{display:inline-block;background:var(--paper);color:var(--ink);font-size:11px;font-weight:700;
  padding:4px 10px;border-radius:99px;vertical-align:middle;margin-left:12px;position:relative;top:-2px}
.chips{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}
.chip{background:var(--soft);border-radius:8px;padding:16px 16px}
.chip small{display:block;font-size:12px;font-weight:700;color:#4E483F;margin-bottom:5px}
.chip b{font-size:16px}
#hud{position:fixed;right:20px;bottom:10px;color:#8A8177;font-size:11.5px;
  font-variant-numeric:tabular-nums;z-index:9;letter-spacing:.06em}
#hint{position:fixed;left:20px;bottom:10px;color:#6B635A;font-size:11px;z-index:9}
@media print{
  html,body{overflow:visible;background:#fff}
  #stage{position:static;display:block}
  #hud,#hint{display:none!important}
  .slide{display:flex!important;position:relative;transform:none!important;
    page-break-after:always;break-after:page}
  @page{size:1280px 720px;margin:0}
}
"""

JS = u"""
const S=[...document.querySelectorAll('.slide')];let i=0;
function fit(){const k=Math.min(innerWidth/1280,innerHeight/720);
  S.forEach(s=>s.style.transform='scale('+k+')');}
function go(n){i=Math.max(0,Math.min(S.length-1,n));
  S.forEach((s,j)=>s.classList.toggle('on',j===i));
  document.getElementById('hud').textContent=String(i+1).padStart(2,'0')+' / '+String(S.length).padStart(2,'0');
  location.hash=i+1;}
addEventListener('keydown',e=>{
  if(['ArrowRight','PageDown',' ','Enter'].includes(e.key)){e.preventDefault();go(i+1)}
  if(['ArrowLeft','PageUp','Backspace'].includes(e.key)){e.preventDefault();go(i-1)}
  if(e.key==='Home')go(0); if(e.key==='End')go(S.length-1);});
addEventListener('click',e=>{if(e.target.closest('a'))return;go(i+(e.clientX<innerWidth*0.25?-1:1))});
addEventListener('resize',fit);
fit();go(Math.max(0,(parseInt(location.hash.slice(1))||1)-1));
"""


def slide(inner, dark=False):
    return u'<section class="slide%s">%s</section>\n' % (" dark" if dark else "", inner)


def head(num, t, lead=None):
    h = u'<div class="num">%s</div><h1>%s</h1>' % (num, t)
    if lead:
        h += u'<p class="lead">%s</p>' % lead
    return h


S = []

# 01 표지 ─────────────────────────────────────────────────
S.append(slide(u"""
  <div class="hero">%s</div>
  <div class="body" style="justify-content:flex-end;padding-bottom:14px">
    <div class="num" style="margin-bottom:14px">브랜드 기획</div>
    <div style="font-size:76px;font-weight:800;letter-spacing:-.03em;line-height:1">오하리상점</div>
    <div style="font-size:21px;letter-spacing:.22em;color:#A79E92;margin-top:16px">OHARI</div>
    <div style="width:60px;height:2px;background:#5A534C;margin:34px 0 22px"></div>
    <div style="font-size:24px;font-weight:700">상황에서 출발하는 테이블웨어 선물 편집숍</div>
    <div style="font-size:16px;color:var(--muted);margin-top:10px">3~7만 원 · 세트 · 자체 기획 상품</div>
  </div>
  <div style="font-size:13px;color:#8A8177">2026. 08. 30</div>
""" % svg("char-turtle"), dark=True))

# 02 한 장으로 ────────────────────────────────────────────
S.append(slide(u"""
  %s
  <div class="body">
    <div class="quote">주는 상황부터 고르게 하고,<br>무엇을 왜 골랐는지 말한 뒤, 우리 그림으로 싸서 보낸다.</div>
    <div class="cards" style="grid-template-columns:repeat(3,1fr);margin-top:38px">
      <div class="c"><div class="big">3~7만 원</div><div class="k" style="margin:12px 0 4px">캐주얼 선물 가격대</div><p>단품이 아니라 세트로 판다</p></div>
      <div class="c"><div class="big">세트</div><div class="k" style="margin:12px 0 4px">최소 판매 단위</div><p>조합이 곧 우리 주장이다</p></div>
      <div class="c"><div class="big">상황</div><div class="k" style="margin:12px 0 4px">진열 1차 카테고리</div><p>집들이 · 결혼 · 감사 · 생일 · 나에게</p></div>
    </div>
  </div>
  <div class="note">상위 정체성은 “선물가게”, 현재 취급이 “테이블웨어”. 이 순서를 뒤집지 않는다.</div>
""" % head(u"01", u"한 장으로")))

# 03 사업 개요 ────────────────────────────────────────────
S.append(slide(u"""
  %s
  <div class="body">
    <table><tbody>
      <tr><td class="k">상품</td><td>테이블웨어 세트. <b>단품은 팔지 않는다</b></td></tr>
      <tr><td class="k">소싱 · 상품화</td><td>도매 상가에서 사와 <b>자체 기획 세트</b>로 만든다 — 조합 + 자체 패키지·라벨 + 카드</td></tr>
      <tr><td class="k">가격대</td><td>30,000 ~ 70,000원</td></tr>
      <tr><td class="k">타겟</td><td>여성 중심 20대 후반 ~ 30대</td></tr>
      <tr><td class="k">취급 분야</td><td>테이블웨어만. 문구류 등 확장은 <b>보류</b>(폐기 아님)</td></tr>
      <tr><td class="k">판매 채널</td><td>자사몰 · 스마트스토어 → 텐바이텐 · 아이디어스 → 29CM → 카카오 선물하기</td></tr>
    </tbody></table>
    <div class="bar" style="margin-top:26px">상품이 도매라 복제 가능하다. 그래서 우리가 만드는 것은 셋뿐이다 — 조합 · 포장 · 문장.</div>
  </div>
""" % head(u"02", u"무엇을, 어떻게 파는가")))

# 04 카테고리 ─────────────────────────────────────────────
S.append(slide(u"""
  %s
  <div class="body">
    <div class="cards" style="grid-template-columns:repeat(3,1fr)">
      <div class="c fill"><h3>상황 <span class="pill">채택</span></h3><p>집들이 · 결혼 · 감사<br>생일 · 나에게</p><div class="k foot">우리 · 로파서울</div></div>
      <div class="c"><h3>작가 · 공방</h3><p>작가 이름별</p><div class="k foot">요소갤러리 · 쿠도</div></div>
      <div class="c"><h3>품목</h3><p>접시 · 볼 · 잔 · 컵</p><div class="k foot">소로이샵 · 대부분</div></div>
    </div>
    <div style="font-size:22px;font-weight:800;margin-top:34px">우리 1차 카테고리는 상황, 품목은 2차 필터로 내린다.</div>
    <p class="lead" style="margin-top:12px;color:#55504A">“집들이 선물”을 누르고 들어가서 그 안에서 접시·볼로 다시 거른다.<br>
    반대로 하면 “집들이 선물 뭐 사지”로 들어온 사람이 길을 잃는다 — 요소갤러리의 빈틈이 정확히 그것이다.</p>
  </div>
""" % (head(u"03", u"무엇으로 나눌 것인가",
            u"카테고리 = 손님이 가장 먼저 마주치는 상단 메뉴. 같은 그릇을 팔아도 무엇으로 나누느냐에 따라 다른 가게가 된다."),
       )))

# 05 차별점 ───────────────────────────────────────────────
S.append(slide(u"""
  %s
  <div class="body">
    <div style="font-size:34px;font-weight:800;letter-spacing:-.02em">고르는 사람의 안목과, 그것이 쌓인 기록</div>
    <p class="lead" style="margin-top:12px">③을 만족한 건 이것 하나였다. 그림도, 선물 완결 프로세스도, 추천 기능도 넘지 못했다 —<br>
    전부 복제되거나, 대기업이 이미 하고 있거나, 축적이 안 된다.</p>
    <table style="margin-top:24px;table-layout:fixed">
      <thead><tr><th style="width:130px">층</th><th>무엇인가</th>
        <th style="width:360px;text-align:left;border-left:1px solid #3A3531;padding-left:26px">복제 난이도</th></tr></thead>
      <tbody>
      <tr><td class="k" style="color:#D6CFC5">형식</td><td>조합을 제안한다, 기준을 쓴다</td>
        <td style="text-align:left;color:#B5ADA2;border-left:1px solid #3A3531;padding-left:26px">하루면 따라한다</td></tr>
      <tr><td class="k" style="color:#D6CFC5">내용</td><td>우리가 짠 조합, 우리가 쓴 기준</td>
        <td style="text-align:left;color:#B5ADA2;border-left:1px solid #3A3531;padding-left:26px">우리만큼 고민해야 한다</td></tr>
      <tr style="background:var(--paper)"><td class="k" style="color:var(--ink)">축적</td>
        <td style="color:var(--ink)">6개월 · 1년 치가 쌓인 것</td>
        <td style="text-align:left;color:var(--ink);font-weight:700;border-left:1px solid var(--line);padding-left:26px">복제 불가. 시간이 필요하다</td></tr>
    </tbody></table>
  </div>
  <div class="note">런칭 시점에는 여전히 차별점이 없다. 못 찾은 게 아니라 구조상 없는 것이고, 있는 척하면 비용은 나중에 훨씬 커진다.</div>
""" % head(u"04", u"차별점",
           u"조건 셋으로 걸렀다 — ① 손님이 인지할 것 ② 따라하기 어려울 것 ③ 시간이 갈수록 격차가 벌어질 것"), dark=True))

# 06 경쟁 ─────────────────────────────────────────────────
S.append(slide(u"""
  %s
  <div class="body">
    <div class="cards" style="grid-template-columns:repeat(4,1fr)">
      <div class="c"><h3 style="font-size:17px">요소갤러리 · 쿠도</h3><div class="k">작가 도자기 · 3~8만</div><p>작가가 1차 카테고리라<br>선물 동선이 없다</p></div>
      <div class="c"><h3 style="font-size:17px">여기담기</h3><div class="k">일러스트 그릇 · 자체 제조</div><p>브랜드지 편집숍이 아니다.<br>“한 상”을 못 짠다</p></div>
      <div class="c"><h3 style="font-size:17px">화소반</h3><div class="k">자체 제조 · 무장식</div><p>“장식 없음”은 이미 점유된 자리다</p></div>
      <div class="c"><h3 style="font-size:17px">스마트스토어</h3><div class="k">도매 · 2~4만</div><p>조악한 포장, 브랜드가 없다</p></div>
    </div>
    <div class="row" style="margin-top:22px">
      <div class="c fill" style="flex:1.7">
        <div class="k" style="color:var(--muted)">비어 있는 자리</div>
        <h3 style="font-size:24px;margin:6px 0 8px">손그림 톤 + 상황 진열 + 세트 + 3~7만 원</h3>
        <p>셋 다 하는 곳이 없는 이유는 어려워서가 아니라 각자 자기 강점의 반대편이기 때문이다.</p>
      </div>
      <div class="c" style="flex:1;background:var(--soft);border-color:var(--soft)">
        <div class="k">진짜로 자주 지는 상대</div>
        <h3 style="font-size:24px;margin:6px 0 8px">상품권</h3>
        <p>그릇 선물의 최대 리스크는 겹침이고, 상품권은 그게 0이다.</p>
      </div>
    </div>
  </div>
""" % head(u"05", u"누구와 겹치는가",
           u"카카오 선물하기·29CM는 경쟁자가 아니라 우리가 올라갈 매대다. 경쟁자는 그 매대에서 옆에 놓이는 브랜드다.")))

# 07 포지셔닝 ─────────────────────────────────────────────
S.append(slide(u"""
  %s
  <div class="body">
    <table>
      <thead><tr><th style="width:190px">항목</th><th>스마트스토어 3만</th>
        <th style="color:var(--ink);font-size:15px">우리 5만</th><th>로파서울 5만</th></tr></thead>
      <tbody>
        <tr><td class="k">상품</td><td>세트</td><td><b>세트 (2인 완결)</b></td><td>단품 1점</td></tr>
        <tr><td class="k">포장</td><td>뽁뽁이</td><td><b>그림 띠지 + 박스 + 완충</b></td><td>기본 포장</td></tr>
        <tr><td class="k">카드</td><td>없음</td><td><b>그림 카드 + 손글씨</b></td><td>별도 구매</td></tr>
        <tr><td class="k">안 겹칠 확률</td><td>낮음</td><td><b>중간</b></td><td>높음</td></tr>
      </tbody>
    </table>
    <div class="bar" style="margin-top:30px;font-weight:400;font-size:15.5px;line-height:1.7">
      <b>“안 겹칠 확률”은 로파서울에 진다.</b> 도매 상품이니 당연하다.<br>
      그래서 그 항목으로 싸우지 않고 <b>조합 · 포장 · 카드</b> 세 칸으로 5만 원을 설명한다. 세 칸 다 우리가 이긴다.
    </div>
  </div>
""" % head(u"06", u"같은 5만 원, 무엇이 다른가")))

# 08 네이밍 ───────────────────────────────────────────────
S.append(slide(u"""
  %s
  <div class="hero" style="top:96px;right:60px;width:240px;height:240px;opacity:.16">%s</div>
  <div class="body">
    <div style="font-size:64px;font-weight:800;letter-spacing:-.03em;line-height:1">오하리상점</div>
    <div style="font-size:18px;letter-spacing:.22em;color:#A79E92;margin-top:14px">OHARI</div>
    <table style="margin-top:26px;max-width:880px;table-layout:fixed"><tbody>
      <tr><td class="k" style="width:220px">뜻을 지지 않는 조어</td><td>업종은 “상점”이 설명한다. 어근은 소리만 담당한다</td></tr>
      <tr><td class="k">소리가 따뜻할 것</td><td>ㅇ·ㅎ·ㄹ에 받침 없음. 절제된 소리와는 온도가 어긋난다</td></tr>
      <tr><td class="k">흔한 어근 배제</td><td>“담아 · 모아”는 파생 브랜드가 이미 많다</td></tr>
      <tr><td class="k">손그림 가능</td><td>3음절 무받침. 워드마크가 곧 로고다</td></tr>
    </tbody></table>
  </div>
  <div class="note">KIPRIS 21류(식기) 비어 있음 · 인스타 커머스 계정 없음 · “오하리상점” 없음
    &nbsp;&nbsp;|&nbsp;&nbsp; 대외 표기는 항상 <b>오하리상점 / OHARI</b></div>
""" % (head(u"07", u"네이밍"), svg("char-turtle")), dark=True))

# 09 세계관 ───────────────────────────────────────────────
S.append(slide(u"""
  %s
  <div class="body">
    <div class="cards" style="grid-template-columns:repeat(3,1fr)">
      <div class="c"><h3>행운 (복)</h3><div class="k" style="font-style:italic;letter-spacing:0;text-transform:none">거북이는 복을 지고 다닌다</div><p>우리가 파는 건 그릇이 아니라 누군가에게 보내는 복</p></div>
      <div class="c fill"><h3>장수 (오래)</h3><div class="k" style="font-style:italic;letter-spacing:0">거북이는 오래 산다</div><p><b>소싱 기준.</b> 유행 타는 그릇은 안 들인다</p></div>
      <div class="c"><h3>느림</h3><div class="k" style="font-style:italic;letter-spacing:0">거북이는 천천히 간다</div><p>한 번에 많이 올리지 않고 골라서 낸다</p></div>
    </div>
    <div style="font-size:21px;font-weight:800;margin:24px 0 6px">‘오래’ 때문에 <u>도매에서 안 들이는 물건</u>이 생긴다.</div>
    <div style="font-size:14.5px;line-height:1.6;color:#3D3833;margin-bottom:18px">시즌 유행 색·패턴 · 캐릭터 라이선스 그릇 · 잘 깨지는 형태 · 전자레인지 불가 · 단종 잦은 SKU — 세계관이 장식이 아니라 <b>소싱 기준</b>이라는 뜻이다.</div>
    <div class="k" style="font-size:12px;font-weight:700;letter-spacing:.1em;color:var(--muted);margin-bottom:8px">상황 = 어떤 복을 지고 가는가</div>
    <div class="chips">
      <div class="chip"><small>집들이</small><b>새 식탁</b></div>
      <div class="chip"><small>결혼</small><b>둘이 쓰는 상</b></div>
      <div class="chip"><small>감사</small><b>오래 신세 진 상</b></div>
      <div class="chip"><small>생일</small><b>한 사람의 자리</b></div>
      <div class="chip"><small>나에게</small><b>내 상</b></div>
    </div>
  </div>
  <div class="note">회차 포맷 〈복 지고 간 상〉 — 세트 하나당 한 편, 300자. 어차피 써야 할 상품 설명에 형식과 번호를 붙인 것이라 제작비가 0에 수렴한다.</div>
""" % head(u"08", u"거북이 세계관",
           u"설정집이 아니라 지리. 상징을 업무에 붙이지 못하면 그건 설정이지 세계가 아니다.")))

# 10 아이덴티티 ───────────────────────────────────────────
grid = u"".join(u"<span>%s</span>" % svg("motif-" + m) for m in MOTIFS)
S.append(slide(u"""
  %s
  <div class="body">
    <div class="row" style="gap:40px;align-items:stretch">
      <div style="flex:1.15;display:flex;flex-direction:column">
        <div class="grid16">%s</div>
        <div class="row" style="align-items:center;gap:18px;margin-top:auto;padding-top:20px">
          <div style="width:66px;height:66px;flex:none">%s</div>
          <div>
            <div style="font-size:19px;font-weight:800">모티프 16종 + 거북이</div>
            <p style="font-size:13.5px;color:var(--muted);margin-top:5px;line-height:1.6">
              레퍼런스 시트를 그대로 벡터화한 정본.<br>손이 그은 선의 떨림과 비대칭이 남는다.</p>
          </div>
        </div>
      </div>
      <div style="flex:1;display:flex;flex-direction:column;justify-content:flex-start;gap:26px;padding-right:6px">
        <div><div class="k" style="font-size:12px;font-weight:700;letter-spacing:.1em;color:#6E6559">컬러</div>
          <p style="font-size:14.5px;line-height:1.6;margin-top:5px">잉크 단색. 포인트 컬러를 쓰지 않는다 — 따뜻함의 예산은 이미 그림이 쓰고 있다</p></div>
        <div><div class="k" style="font-size:12px;font-weight:700;letter-spacing:.1em;color:#6E6559">타이포</div>
          <p style="font-size:14.5px;line-height:1.6;margin-top:5px">Wanted Sans 400 / 700. 제목 자리를 손그림이 맡으므로 서체는 담백하게</p></div>
        <div><div class="k" style="font-size:12px;font-weight:700;letter-spacing:.1em;color:#6E6559">로고</div>
          <p style="font-size:14.5px;line-height:1.6;margin-top:5px">손그림 워드마크 단독. 심볼은 만들지 않는다 — 그림이 둘이면 서로를 깎는다</p></div>
        <div><div class="k" style="font-size:12px;font-weight:700;letter-spacing:.1em;color:#6E6559">회피</div>
          <p style="font-size:14.5px;line-height:1.6;margin-top:5px">파스텔 · 기계적 대칭 · 그라디언트 · “AI티”</p></div>
      </div>
    </div>
  </div>
""" % (head(u"09", u"아이덴티티", u"그림은 사람이 정하고, 코드가 두께·크기·색을 맞춘다. 형태를 코드로 만들지 않는다."),
       grid, svg("char-turtle"))))

# 10 포장 ─────────────────────────────────────────────────
S.append(slide(u"""
  %s
  <div class="body">
    <div class="row">
      <div class="c" style="flex:1"><h3>2겹 구조</h3>
        <p style="line-height:1.9">겉 &nbsp;·&nbsp; 무지 택배 상자 — 운송 · 완충 · 송장<br>
        안 &nbsp;·&nbsp; 자체 디자인 선물 박스 — 받는 사람이 여는 것</p>
        <div class="k foot" style="letter-spacing:0;text-transform:none">디자인 박스가 깨끗한 상태로 도착하고, 완충을 겉에서 해결한다</div></div>
      <div class="c fill" style="flex:1"><h3>박스 사양</h3>
        <p style="font-size:16px;color:var(--paper)"><b>기성 화이트 박스 · 한 사이즈 · 1도 블랙 · 디자인 1~2종</b></p>
        <div class="k foot" style="letter-spacing:0;text-transform:none">기성 규격이라 목형비가 없다. 남는 비용은 인쇄판비 · 개당 단가 · MOQ뿐</div></div>
    </div>
    <div class="bar" style="margin-top:22px">⚠ 한 사이즈의 대가 — 세트 구성의 상한과 하한이 박스로 정해진다. 박스에 안 들어가는 세트는 만들지 않는다.</div>
    <div style="margin-top:24px">
      <div class="k" style="font-size:12px;font-weight:700;letter-spacing:.1em;color:#6E6559">박스 안</div>
      <p style="font-size:15px;margin-top:8px">명함 &nbsp;·&nbsp; 엽서(회차 마지막 한 줄 + 거북이) &nbsp;·&nbsp; 띠지(상황 이름) &nbsp;·&nbsp; 법정 표시 라벨 7항목 &nbsp;·&nbsp; 손그림 인쇄 완충지</p>
    </div>
  </div>
""" % head(u"10", u"포장이 곧 상품이다",
           u"도매 상품이라 우리가 만드는 건 조합 · 포장 · 문장 셋뿐이다. 그래서 패키징이 최우선이다.")))

# 11 판매 채널 ────────────────────────────────────────────
S.append(slide(u"""
  %s
  <div class="body">
    <div class="cards" style="grid-template-columns:repeat(4,1fr)">
      <div class="c fill"><div class="k" style="color:var(--muted)">TIER 0</div><h3>0~6개월</h3>
        <p>자사몰 · 스마트스토어<br>톡스토어</p><div class="k foot" style="letter-spacing:0;font-style:italic">매출 · 리뷰 · CS 기록</div></div>
      <div class="c"><div class="k">TIER 1</div><h3>3~9개월</h3>
        <p>텐바이텐 · 아이디어스<br>오브젝트</p><div class="k foot" style="letter-spacing:0;font-style:italic">브랜드로 팔린 이력</div></div>
      <div class="c"><div class="k">TIER 2</div><h3>9~18개월</h3>
        <p>29CM</p><div class="k foot" style="letter-spacing:0;font-style:italic">톤이 맞는 트래픽</div></div>
      <div class="c"><div class="k">TIER 3</div><h3>12개월~</h3>
        <p>카카오 선물하기</p><div class="k foot" style="letter-spacing:0;font-style:italic">규모</div></div>
    </div>
    <div style="font-size:20px;font-weight:800;margin-top:28px">Tier 3이 마지막인 이유는 심사 기준에 “인지도”가 들어 있기 때문이다. 인지도는 Tier 0~2에서 만들어진다.</div>
    <p class="lead" style="margin-top:12px;color:#55504A"><b>자사몰 필수 기능 · 링크로 보내기</b> — 주소를 몰라 못 보내는 경우가 실제로 많다. Tier 3 이전에도 그 수요를 일부 받는다.</p>
  </div>
""" % (head(u"11", u"어디서 파는가",
            u"29CM는 자체 브랜드 상품만 받고, 카카오 선물하기는 자체 브랜드와 인지도를 심사한다. 둘 다 출발점이 아니라 목표다."),
       )))

# 12 로드맵 ───────────────────────────────────────────────
S.append(slide(u"""
  %s
  <div class="body" style="gap:14px;display:flex">
    <div class="step fill"><div class="n">1</div>
      <div style="width:190px"><div class="k" style="color:var(--muted)">0~9개월</div><div style="font-size:20px;font-weight:800">포장이 곧 상품</div></div>
      <div style="flex:1;font-size:14.5px;line-height:1.6">박스 · 띠지 · 카드 · 스티커 · 완충지에 그림이 산다</div>
      <div style="width:210px;text-align:right;font-weight:700;font-size:14.5px">고른 이유가 보이는 선물가게</div></div>
    <div class="step"><div class="n">2</div>
      <div style="width:190px"><div class="k">9~18개월</div><div style="font-size:20px;font-weight:800">소량 PB</div></div>
      <div style="flex:1;font-size:14.5px;line-height:1.6;color:#3D3833">도자기 전사 · 머그 프린트로 그림을 상품에 얹는다</div>
      <div style="width:210px;text-align:right;font-weight:700;font-size:14.5px">그 그림 그릇 파는 곳</div></div>
    <div class="step"><div class="n">3</div>
      <div style="width:190px"><div class="k">18개월~</div><div style="font-size:20px;font-weight:800">공방 콜라보 + 굿즈</div></div>
      <div style="flex:1;font-size:14.5px;line-height:1.6;color:#3D3833">특징 있는 공방과 “우리 그림 × 그 공방”으로 묶는다</div>
      <div style="width:210px;text-align:right;font-weight:700;font-size:14.5px">브랜드</div></div>
  </div>
  <div class="note">공방을 찾아 브랜드를 세우는 게 아니라, <b>브랜드를 세워 놓고 공방을 끌어온다.</b> 협상력이 반대로 붙는다.</div>
""" % head(u"12", u"3단계로 키운다")))

# 13 다음 ─────────────────────────────────────────────────
S.append(slide(u"""
  %s
  <div class="body">
    <div class="row" style="gap:44px">
      <div style="flex:1">
        <div class="k" style="font-size:12px;font-weight:700;letter-spacing:.14em;color:var(--muted);margin-bottom:16px">지금 바로</div>
        <table><tbody>
          <tr><td class="k" style="width:150px;color:var(--paper)">세트 구성 확정</td><td>박스 사이즈 · 라벨 표기 ·<br>회차 글이 전부 여기서 갈라진다</td></tr>
          <tr><td class="k" style="color:var(--paper)">상표 · 핸들 선점</td><td>KIPRIS 21류 출원 ·<br>인스타 · 도메인 · 스토어 URL</td></tr>
          <tr><td class="k" style="color:var(--paper)">로고</td><td>손그림 워드마크 —<br>손으로 쓴 시트를 벡터화</td></tr>
          <tr><td class="k" style="color:var(--paper)">축적 시작</td><td>〈복 지고 간 상〉을<br>런칭 전부터 쓴다</td></tr>
        </tbody></table>
      </div>
      <div style="flex:1">
        <div class="k" style="font-size:12px;font-weight:700;letter-spacing:.14em;color:var(--muted);margin-bottom:16px">알고 있는 리스크</div>
        <table><tbody>
          <tr><td class="k" style="width:160px;color:var(--paper)">초기엔 축적이 없다</td><td>런칭 6개월이 가장 취약하다.<br>인정하고 시작한다</td></tr>
          <tr><td class="k" style="color:var(--paper)">도매라 상품이 겹친다</td><td>단품으로 싸우지 않는다.<br>조합 · 포장으로 비교 기준을 옮긴다</td></tr>
          <tr><td class="k" style="color:var(--paper)">인쇄 MOQ · 재고</td><td>한 사이즈 + 1도로 줄였다.<br>부담되면 초기엔 스탬프</td></tr>
          <tr><td class="k" style="color:var(--paper)">사람 의존</td><td>해자의 뒷면이라 제거할 수 없다.<br>판단을 문서로 남긴다</td></tr>
        </tbody></table>
      </div>
    </div>
  </div>
  <div style="width:60px;height:2px;background:#6B635A;margin:22px 0 16px"></div>
  <div style="font-size:27px;font-weight:800;letter-spacing:-.02em;padding-bottom:6px">골라서 모으고, 싸서 보냅니다.</div>
""" % head(u"13", u"다음"), dark=True))

HTML = (u'<!doctype html><html lang="ko"><head><meta charset="utf-8">\n'
        u'<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        u'<title>오하리상점 — 브랜드 기획</title>\n<style>%s</style></head><body>\n'
        u'<div id="stage">\n%s</div>\n'
        u'<div id="hud"></div><div id="hint">← → 로 이동 · 인쇄하면 PDF</div>\n'
        u'<script>%s</script></body></html>\n') % (CSS, u"".join(S), JS)

out = os.path.join(D, "deck-slides.html")
io.open(out, "w", encoding="utf-8").write(HTML)
print("deck-slides.html built: %d slides, %.0f KB" % (len(S), len(HTML) / 1024))
