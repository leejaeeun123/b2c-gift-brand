# -*- coding: utf-8 -*-
"""sourcing-comparison.html(10-18) → sourcing-comparison-2026-10-25.html
시안 섹션(00) 삽입 + 최종 발주처·대략 견적 반영. 이미지는 assets/package-proofs-261025/ 를 base64 인라인.
실행: python 04-packaging/build_sourcing_261025.py  (레포 루트에서)
"""
import base64, io, pathlib, re
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "04-packaging" / "sourcing-comparison.html"
OUT = ROOT / "04-packaging" / "sourcing-comparison-2026-10-25.html"
IMG = ROOT / "assets" / "package-proofs-261025"

def data_uri(rel, maxw=900):
    p = IMG / rel
    im = Image.open(p)
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    if p.suffix.lower() == ".png":
        im.save(buf, "PNG", optimize=True); mime = "image/png"
    else:
        im.convert("RGB").save(buf, "JPEG", quality=82, optimize=True); mime = "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode()

def mock(rel, cap):
    return f'<figure><img src="{data_uri("mockup/" + rel, 800)}" alt="{cap}"><figcaption>{cap}</figcaption></figure>'

def fig(rel, cap, cls="", maxw=900):
    return f'<figure class="{cls}"><img src="{data_uri(rel, maxw)}" alt="{cap}"><figcaption>{cap}</figcaption></figure>'

html = SRC.read_text(encoding="utf-8")

def sub(old, new, count=1):
    global html
    assert html.count(old) >= 1, f"not found: {old[:60]}"
    html = html.replace(old, new, count)

# ── CSS ────────────────────────────────────────────────────────────────
CSS = """
/* 시안 섹션 */
.designs{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}
.design{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px;display:flex;flex-direction:column;gap:10px;min-width:0}
.design.wide{grid-column:1/-1}
.design .dh{display:flex;justify-content:space-between;align-items:baseline;gap:8px;flex-wrap:wrap}
.design .dh h3{font-size:16px}
.design .dh .sz{font-size:12.5px;color:var(--muted)}
.design .imgs{display:flex;gap:12px;flex-wrap:wrap;align-items:flex-start}
.design figure{margin:0;flex:1 1 120px;min-width:0;display:flex;flex-direction:column;gap:6px}
.design .imgs figure{max-width:300px}
.design .imgs figure.sq{max-width:170px;flex:0 1 170px}
.design .imgs figure.tall{max-width:150px;flex:0 1 150px}
.design img{display:block;width:100%;height:auto;background:#fff;border:1px solid var(--line);border-radius:4px;padding:6px}
.design figcaption{font-size:12px;color:var(--muted);text-align:center}
.design .dn{font-size:13px;color:var(--muted);margin:0;line-height:1.55}
.design .dn a{color:var(--accent)}
.design .dn b{color:var(--ink)}
.box-faces{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media (max-width:760px){.box-faces{grid-template-columns:1fr}}
.box-faces .bf{display:flex;flex-direction:column;gap:8px}
.box-faces .bf .lbl{font-size:13px;font-weight:600}
.box-faces .bf .lbl small{font-weight:400;color:var(--muted);margin-left:6px}
.box-faces .net{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.box-faces .net figure{margin:0;display:flex;flex-direction:column;gap:4px}
.box-faces .net figure.full{grid-column:1/-1}
.box-faces .net img{display:block;width:100%;height:auto;background:#fff;border:1px solid var(--line);border-radius:4px;padding:6px}
.box-faces .net figcaption{font-size:11.5px;color:var(--muted);text-align:center}
.ref{display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.ref figure{margin:0;flex:0 0 160px}
.ref img{display:block;width:100%;border:1px solid var(--line);border-radius:4px}
.ref p{margin:0;font-size:13px;color:var(--muted);line-height:1.55;flex:1 1 260px}
.mock{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;padding-top:10px;border-top:1px dashed var(--line)}
@media (max-width:760px){.mock{grid-template-columns:1fr 1fr}}
.mock figure{margin:0;display:flex;flex-direction:column;gap:4px}
.mock img{display:block;width:100%;height:auto;aspect-ratio:3/4;object-fit:cover;border:1px solid var(--line);border-radius:4px}
.mock figcaption{font-size:11.5px;color:var(--muted);text-align:center}
.mock.two{grid-template-columns:repeat(2,minmax(0,360px));justify-content:start;border-top:0;padding-top:0}
.steps{margin:0;padding-left:18px;font-size:13px;color:var(--muted);line-height:1.7}
.steps b{color:var(--ink)}
.est{font-size:11px;border:1px solid var(--line-strong);border-radius:3px;padding:1px 5px;color:var(--muted);vertical-align:middle}
"""
sub("</style>", CSS + "</style>")

# ── header ─────────────────────────────────────────────────────────────
sub("<h1>오하리상점 선물세트 패키지 발주처 비교</h1>",
    "<h1>오하리상점 선물세트 패키지 시안 · 최종 발주처</h1>")
sub('<p class="lead">8개 품목(쇼핑백 추가 구성 포함)·10개 발주처의 가격을 한 표로 모았습니다. 장당 단가는 VAT 포함으로 통일했고, 품목명을 누르면 원문 상품 페이지로 이동합니다.</p>',
    '<p class="lead">10-25 완성 시안 7종(상자 2사이즈·원형 스티커·엽서·주의사항 네임택·명함·쇼핑백 스티커)과 최종 발주처, 대략 견적을 정리했습니다. 상자는 유패키지, 끈·습자지·에어캡은 10-18 결론 그대로, 인쇄물은 전부 성원애드피아입니다. 10-18 비교표는 아래 02~04에 그대로 두었습니다.</p>')
sub('<span>기준일 <b>2026-10-18</b></span>',
    '<span>기준일 <b>2026-10-25</b> (가격은 10-18 견적, 신규 3종은 추정)</span>')
sub('<a href="#summary">추천 요약</a>', '<a href="#designs">시안</a><a href="#summary">최종 발주처</a>')

# ── 00 시안 섹션 ────────────────────────────────────────────────────────
def box_net(folder, label, size, top_cap):
    f = lambda n, cap, cls="": f'<figure class="{cls}"><img src="{data_uri(folder + "/" + n, 1000)}" alt="{label} {cap}"><figcaption>{cap}</figcaption></figure>'
    return f"""<div class="bf"><div class="lbl">{label}<small>{size}</small></div>
      <div class="net">
        {f("top.jpg", top_cap, "full")}
        {f("side-front.jpg", "옆면 앞 — OHARISTORE")}
        {f("side-back.jpg", "옆면 뒤 — 테이블웨어 실루엣")}
        {f("side-left.jpg", "옆면 왼 — OHARI + 브랜드 문안")}
        {f("side-right.jpg", "옆면 오 — Slowly is wonderful. + 거북이")}
      </div></div>"""

DESIGNS = f"""
<section id="designs">
  <h2><span class="k">00</span>패키지 시안 (2026-10-25)</h2>
  <p class="note">인쇄물 시안 7종입니다. 각 카드의 발주처·견적은 01 최종 발주처와 연결되고, 사이즈는 시안 기준 확정값입니다. 상자 아랫면은 인쇄하지 않습니다(품명 스티커는 보류 · 자체 출력/발주 미정). 10-25 낮에 만든 종이 목업 사진을 함께 넣었습니다.</p>
  <div class="designs">
    <div class="design wide">
      <div class="dh"><h3>1. 선물세트 상자</h3><span class="sz">흰색 G형 일체형 · 먹1도 · 윗면 + 옆면 4면 · 큰 360×270×110 / 작은 270×220×110mm</span></div>
      <div class="ref">{fig("box-reference.jpg", "G형 일체형 상자 (유패키지 기성 규격)", "")}<p>G형 일체형: 뚜껑과 몸체가 한 장으로 이어진 조립식 상자. 기성 규격이라 목형비 없음. 큰 사이즈는 품목 3개, 작은 사이즈는 품목 1~2개 세트용.</p></div>
      <div class="box-faces">
        {box_net("box-large", "큰 사이즈", "360×270×110mm · 300장", "윗면 — 해초 패턴")}
        {box_net("box-small", "작은 사이즈", "270×220×110mm · 400장", "윗면 — 거북이 + 클로버")}
      </div>
      <div class="mock">
        {mock("boxes-01.jpg", "큰·작은 상자 나란히 — 윗면 패턴 + 옆면 OHARISTORE")}
        {mock("boxes-02.jpg", "큰 상자 옆면 실루엣 · 작은 상자 옆면 선 그림")}
        {mock("boxes-03.jpg", "쌓았을 때 — Slowly is wonderful. 면")}
        {mock("boxes-04.jpg", "큰 상자 정면 — 테이블웨어 실루엣")}
      </div>
      <p class="dn">종이 목업(10-25): 시안을 A4로 뽑아 기성 상자에 붙여 비례만 확인한 것. 발주처 <b>유패키지</b> · 큰 2,146원 × 300장 = 643,896원 · 작은 1,573원 × 400장 = 629,046원 (VAT·서울 택배 포함, 10-18 견적). 견적의 인쇄 면적 기준(윗면+옆면)과 시안이 일치. <a href="#box">상자 비교 보기</a></p>
    </div>
    <div class="design">
      <div class="dh"><h3>2. 포장 스티커 (원형)</h3><span class="sz">50×50mm · 세트당 1개 · 봉인용</span></div>
      <div class="imgs">{fig("sticker-round.png", "원형 — 거북이 + OHARI", "sq")}</div>
      <p class="dn">발주처 <b>성원애드피아</b> · 도무송 500장(1장 2개) 14,300원 · 약 15원/개. <a href="#sticker">스티커 비교 보기</a></p>
    </div>
    <div class="design">
      <div class="dh"><h3>3. 브랜드 엽서</h3><span class="sz">100×148mm · 양면 먹1도 · 세트당 1매</span></div>
      <div class="imgs">{fig("postcard-front.jpg", "앞 — OHARISTORE + 해초 패턴")}{fig("postcard-back.jpg", "뒤 — 거북이 + Slowly is wonderful. + 브랜드 문안")}</div>
      <p class="dn">발주처 <b>성원애드피아</b> · 디지털 엽서 먹1도 양면 100매 6,490원 · 65원/매. <a href="#postcard">엽서 비교 보기</a></p>
    </div>
    <div class="design">
      <div class="dh"><h3>4. 주의사항 네임택</h3><span class="sz">80×140mm · 양면 · 품목에 거는 택</span></div>
      <div class="imgs">{fig("nametag-front.jpg", "앞 — OHARI + 거북이 + 문구", "tall")}{fig("nametag-back.jpg", "뒤 — USE &amp; CARE 아이콘 4종", "tall")}</div>
      <p class="dn">발주처 <b>성원애드피아</b> · 엽서와 같은 디지털 인쇄로 비규격 사이즈 입력 · <span class="est">추정</span> 100매 약 6,500원 · 약 65원/매. 마끈 리본에 함께 묶는 구성. <a href="#print-new">신규 인쇄물 견적 보기</a></p>
    </div>
    <div class="design">
      <div class="dh"><h3>5. 명함</h3><span class="sz">90×50mm · 양면</span></div>
      <div class="imgs">{fig("namecard-front.jpg", "앞 — OHARISTORE")}{fig("namecard-back.jpg", "뒤 — 테이블웨어 실루엣")}</div>
      <p class="dn">발주처 <b>성원애드피아</b> · 견적서 10-25: 반누보 화이트 204g 양면칼라 200매 6,050원(30원/매) · 400매 12,100원 · 1,000매 25,300원(25원/매) · 배송비 별도. 운영용이라 세트 원가 미포함. <a href="#print-new">신규 인쇄물 견적 보기</a></p>
    </div>
    <div class="design">
      <div class="dh"><h3>6. 쇼핑백 스티커 (사각)</h3><span class="sz">70×160mm · 추가 구성 · 무지 쇼핑백용</span></div>
      <div class="imgs">{fig("sticker-bag.jpg", "사각 — OHARISTORE + 테이블웨어 실루엣", "tall")}</div>
      <p class="dn">발주처 <b>성원애드피아</b> · 도무송 사각라운드 비규격 · <span class="est">추정</span> 500개 약 15,000~20,000원 · 약 30~40원/개. 쇼핑백 자체는 래포리 재입고 대기. <a href="#bag">쇼핑백 비교 보기</a></p>
    </div>
    <div class="design wide">
      <div class="dh"><h3>7. 포장 구성 목업 — 상자를 열었을 때</h3><span class="sz">습자지 → 마끈 십자 + 네임택 → 트레이싱지 덮기 → 뚜껑 안쪽 원형 스티커</span></div>
      <div class="mock two">
        {mock("inside-01.jpg", "품목마다 습자지로 싸고 마끈 십자 매듭, 네임택·사각 스티커를 끈 아래에")}
        {mock("inside-02.jpg", "맨 위를 트레이싱지 한 장으로 덮고, 뚜껑 안쪽에 원형 스티커")}
      </div>
      <ol class="steps">
        <li><b>에어캡</b>으로 품목 개별 감싸기 (사진에는 생략)</li>
        <li><b>습자지</b> 2~3장으로 싸기 — 낮은 품목은 더 감아 높이 맞춤</li>
        <li><b>마끈 십자 + 리본 매듭</b>, 끈 아래에 <b>주의사항 네임택</b>(80×140) 끼우기. 사진의 사각 라벨 자리가 네임택 자리</li>
        <li>같은 높이로 나란히 넣고 맨 위를 <b>트레이싱지</b> 1장으로 덮기 (신규 품목 → 아래 3-1)</li>
        <li>뚜껑 안쪽 가운데 <b>원형 스티커</b>, 엽서는 트레이싱지 위</li>
      </ol>
      <p class="dn">완충 스티로폼은 <b>보류</b>(일단 에어캡+습자지로만). 상자 묶는 끈과 쇼핑백은 10-18 결론 그대로. <a href="#tissue">습자지</a> · <a href="#tracing">트레이싱지</a></p>
    </div>
  </div>
</section>
"""
sub('<section id="summary">', DESIGNS + '\n<section id="summary">')

# ── 01 최종 발주처 ──────────────────────────────────────────────────────
sub('<h2><span class="k">01</span>품목별 추천 발주처</h2>',
    '<h2><span class="k">01</span>최종 발주처 · 대략 견적</h2>\n  <p class="note">상자·끈·습자지·원형 스티커·엽서·에어캡은 10-18 비교 결론 그대로 확정. 주의사항 네임택·명함·쇼핑백 사각 스티커는 성원애드피아에서 함께 발주하며, 금액은 사이트 주문창 계산 전이라 기존 엽서·스티커 단가로 환산한 <span class="est">추정</span>값입니다.</p>')
sub('<div class="card"><div class="item">쇼핑백 (추가 구성 · 무지 + 사각 스티커)</div>',
    '<div class="card best"><div class="item">트레이싱지 (덮는 용) <span class="tag t-acc">신규</span></div><div class="vendor"><a href="https://hanapapermall.co.kr/product/detail.html?product_no=4228&amp;cate_no=307&amp;display_group=1" target="_blank" rel="noopener">하나페이퍼몰</a> 또는 오픈마켓 4절 100매</div><div class="price">4절 <span class="num">약 66 ~ 110원</span>/매</div><p class="why">큰 상자(360×270)를 한 장으로 덮으려면 4절(394×272) 이상. 하나페이퍼몰 전지 22매 9,500원(=4절 88매, 108원/매)은 습자지와 묶어 배송 1회, 단 품절 표기 확인 필요. G마켓·옥션 80g 4절 100매 6,590원(66원/매)이 최저.</p></div>\n'
    '    <div class="card best"><div class="item">주의사항 네임택 80×140</div><div class="vendor"><a href="https://www.swadpia.co.kr/goods/goods_view/COD3000/GOD3001" target="_blank" rel="noopener">성원애드피아</a> <span class="est">추정</span></div><div class="price"><span class="num">약 6,500원</span> / 100매 · <span class="num">약 65원</span>/매</div><p class="why">엽서와 같은 디지털 인쇄(토너·먹1도 양면)에 사이즈만 직접 입력. 엽서와 한 주문으로 묶어 택배비 1회.</p></div>\n'
    '    <div class="card best"><div class="item">쇼핑백 사각 스티커 70×160</div><div class="vendor"><a href="https://www.swadpia.co.kr/goods/goods_view/CST2000/GST2001" target="_blank" rel="noopener">성원애드피아</a> <span class="est">추정</span></div><div class="price"><span class="num">약 15,000 ~ 20,000원</span> / 500개 · <span class="num">약 30~40원</span>/개</div><p class="why">도무송 사각라운드 비규격. 원형 50mm(1장 2개 14,300원)보다 면적이 커 1장 1개로 환산.</p></div>\n'
    '    <div class="card best"><div class="item">명함 90×50</div><div class="vendor"><a href="https://www.swadpia.co.kr/" target="_blank" rel="noopener">성원애드피아</a> <span class="est">추정</span></div><div class="price"><span class="num">약 5,000 ~ 8,000원</span> / 200매</div><p class="why">아트지 양면 기준. 운영용이라 세트 원가 미포함.</p></div>\n'
    '    <div class="card"><div class="item">쇼핑백 (추가 구성 · 무지 + 사각 스티커)</div>')
sub("핸즈픽 31·33호는 상자가 안 들어가거나 너무 깊음. 사각 스티커는 성원 재견적.",
    "10-25 상품 페이지 재확인: 두 규격 모두 SOLD OUT 표기, 최대 주문수량 0(카테고리 목록에는 품절이 안 보일 수 있음). 핸즈픽 31·33호는 상자가 안 들어가거나 너무 깊음. 사각 스티커는 성원애드피아(위 카드).")

sub('<div class="vendor">발주 없음</div><div class="price">자체 출력 · 거래처 조달</div><p class="why">품명 스티커는 프린터 라벨지(한글 템플릿), 스티로폼은 아빠 거래처.</p>',
    '<div class="vendor">둘 다 <span class="tag t-warn">보류</span></div><div class="price">품명 스티커는 자체 출력/성원 발주 미정 · 스티로폼은 당분간 미사용</div><p class="why">10-25 결정. 스티로폼은 에어캡+습자지로만 완충.</p>')

# ── 02 상세: 사이즈 표기 + 신규 인쇄물 블록 ─────────────────────────────
sub('<span class="sz">약 100×130~148mm · 세트당 1매</span>', '<span class="sz">100×148mm (시안 확정) · 세트당 1매</span>')
sub('<span class="sz">세트당 1개 · 쇼핑백용 사각 스티커는 별도 구성</span>', '<span class="sz">50×50mm · 세트당 1개 · 쇼핑백용 사각 스티커 70×160은 아래 신규 인쇄물 블록</span>')

NEW_PRINT = """
  <div class="block" id="print-new">
    <div class="block-head"><h3>5-1. 신규 인쇄물 3종 — 성원애드피아 <span class="est">추정 견적</span></h3><span class="sz">10-25 시안에서 추가된 품목 · 사이트 주문창 계산 전</span></div>
    <div class="tbl"><table>
      <thead><tr><th>품목</th><th>사양</th><th class="r">추정 가격</th><th class="r">개당</th><th>환산 근거</th></tr></thead>
      <tbody>
        <tr class="best"><td class="vn">주의사항 네임택</td><td><a class="p" href="https://www.swadpia.co.kr/goods/goods_view/COD3000/GOD3001" target="_blank" rel="noopener">디지털 엽서/상품권</a> 사이즈 직접입력 80×140<small>토너 · 230g · 먹1도 양면</small></td><td class="r"><span class="num">약 6,500원</span> / 100매</td><td class="r num">약 65원</td><td>엽서 100×148 100매 6,490원과 같은 상품·용지. 면적이 작아 같거나 조금 낮을 것</td></tr>
        <tr class="best"><td class="vn">쇼핑백 사각 스티커</td><td><a class="p" href="https://www.swadpia.co.kr/goods/goods_view/CST2000/GST2001" target="_blank" rel="noopener">도무송형 스티커</a> 사각라운드 70×160<small>75 아트지 · 단면</small></td><td class="r"><span class="num">약 15,000 ~ 20,000원</span> / 500개</td><td class="r num">약 30~40원</td><td>원형 50mm 500장(1,000개) 14,300원. 면적 약 3배라 1장 1개 배치로 가정. 쇼핑백 옵션 선택분만 필요하니 수량은 줄여도 됨</td></tr>
        <tr class="best"><td class="vn">명함</td><td>명함 90×50<small>반누보 화이트 204g · 양면칼라</small></td><td class="r"><span class="num">약 5,000 ~ 8,000원</span> / 200매</td><td class="r num">약 25~40원</td><td>업계 일반 명함 시세. 운영용이라 세트 원가 미포함</td></tr>
      </tbody>
    </table></div>
    <p class="note">세 품목 모두 원형 스티커·엽서와 같은 주문으로 묶으면 택배비는 1회입니다. 정확한 금액은 성원애드피아 주문창에 사이즈·수량을 넣으면 바로 계산되므로, 발주 직전에 이 표의 추정값을 실제값으로 바꿔 주세요.</p>
  </div>
"""
sub('  <div class="block" id="etc">', NEW_PRINT + '\n  <div class="block" id="etc">')

# ── 03 발주처별 묶음: 성원 리스트 보강 ──────────────────────────────────
sub('<li><span><a class="p" href="https://www.swadpia.co.kr/goods/goods_view/COD3000/GOD3001" target="_blank" rel="noopener">엽서 먹1도 양면 100매</a></span><span class="num">6,490원</span></li>',
    '<li><span><a class="p" href="https://www.swadpia.co.kr/goods/goods_view/COD3000/GOD3001" target="_blank" rel="noopener">엽서 먹1도 양면 100매</a></span><span class="num">6,490원</span></li>\n'
    '        <li><span>주의사항 네임택 80×140 양면 100매 <span class="est">추정</span></span><span class="num">약 6,500원</span></li>\n'
    '        <li><span>쇼핑백 사각 스티커 70×160 500개 <span class="est">추정</span></span><span class="num">약 15,000~20,000원</span></li>\n'
    '        <li><span>명함 90×50 양면칼라 200매 (400매 12,100 · 1,000매 25,300)</span><span class="num">6,050원</span></li>')

# ── 04 세트 원가: 네임택 반영 ──────────────────────────────────────────
sub("세트 구성: 상자 1개 + 품목마다 에어캡·습자지 2~3장·마끈 리본 + 상자 묶는 끈 + 스티커 1개 + 엽서 1매.",
    "세트 구성: 상자 1개 + 품목마다 에어캡·습자지 2~3장·마끈 리본·주의사항 네임택 + 맨 위 트레이싱지 1매 + 상자 묶는 끈 + 스티커 1개 + 엽서 1매. 완충 스티로폼은 보류.")
sub('<span>마끈 리본 3개 × 약 0.6m</span><span class="num">90원</span>',
    '<span>마끈 리본 3개 × 약 0.6m</span><span class="num">90원</span>\n      <span>주의사항 네임택 3매 × 약 65원 <span class="est">추정</span></span><span class="num">195원</span>')
sub('<span class="tot">합계</span><span class="tot num">약 2,750 ~ 2,850원</span>',
    '<span>트레이싱지 1매 (4절)</span><span class="num">66 ~ 110원</span>\n      <span class="tot">합계</span><span class="tot num">약 3,020 ~ 3,160원</span>')
sub('<span>마끈 리본 1~2개</span><span class="num">30 ~ 60원</span>',
    '<span>마끈 리본 1~2개</span><span class="num">30 ~ 60원</span>\n      <span>주의사항 네임택 1~2매 × 약 65원 <span class="est">추정</span></span><span class="num">65 ~ 130원</span>')
sub('<span class="tot">합계 (품목 1개)</span><span class="tot num">약 1,870 ~ 1,900원</span>',
    '<span>트레이싱지 1매 (4절)</span><span class="num">66 ~ 110원</span>\n      <span class="tot">합계 (품목 1개)</span><span class="tot num">약 2,010 ~ 2,080원</span>')
sub('<span class="tot">합계 (품목 2개)</span><span class="tot num">약 2,000 ~ 2,080원</span>',
    '<span class="tot">합계 (품목 2개)</span><span class="tot num">약 2,200 ~ 2,320원</span>')
sub("상자가 큰 세트 자재비의 75%, 작은 세트의 80%를 차지합니다.",
    "상자가 큰 세트 자재비의 약 70%, 작은 세트의 75~80%를 차지합니다. 네임택·트레이싱지는 추정 단가라 ±50원 범위로 보면 됩니다. 스티로폼(보류)은 0원.")
sub('<tr><td>엽서</td><td class="r num">700매</td>',
    '<tr><td>트레이싱지 4절<small>700세트 × 1매</small></td><td class="r num">700매</td><td>하나페이퍼몰 전지 22매(=4절 88매) 9,500원 / G마켓 4절 100매 6,590원</td><td class="r num">8팩 / 7팩</td><td class="r num">76,000 / 46,130원</td></tr>\n      <tr><td>주의사항 네임택<small>1,700품목 × 1매</small></td><td class="r num">1,700매</td><td>성원 100매 약 6,500원</td><td class="r num">17건분</td><td class="r num">약 110,500원 + 택배</td></tr>\n      <tr><td>엽서</td><td class="r num">700매</td>')

sub('  <div class="block" id="sticker">',
    '  <div class="block" id="tracing">\n    <div class="block-head"><h3>3-1. 트레이싱지 (맨 위 덮는 용) <span class="tag t-acc">신규 10-25</span></h3><span class="sz">세트당 1매 · 큰 상자 안치수 약 360×270 → 4절(394×272) 또는 A3(420×297)</span></div>\n    <div class="tbl"><table>\n      <thead><tr><th>발주처</th><th>제품 · 사양</th><th class="r">가격</th><th class="r">매당</th><th>비고</th></tr></thead>\n      <tbody>\n        <tr class="best"><td class="vn">G마켓 · 옥션</td><td>트레싱지 트레팔지 미농지 4절 100매<small>80g</small></td><td class="r"><span class="num">6,590원</span><small>+ 배송비</small></td><td class="r num">66원</td><td><span class="tag t-best">최저</span> 다나와 \'트레이싱지 4절\' 최저가. 판매자·실제 규격(394×272인지) 확인</td></tr>\n        <tr class="best"><td class="vn">하나페이퍼몰</td><td><a class="p" href="https://hanapapermall.co.kr/product/detail.html?product_no=4228&amp;cate_no=307&amp;display_group=1" target="_blank" rel="noopener">트레싱지</a> 전지 22매 (= 2절 44 · 4절 88 · A3 52매)<small>50g / 82g 선택</small></td><td class="r"><span class="num">9,500원</span></td><td class="r num">108원 (4절)</td><td><span class="tag t-best">추천</span> 습자지와 같은 곳이라 배송 1회. 50g이 더 비치고 부드러움. 페이지에 SOLD OUT 이미지가 보여 재입고 확인</td></tr>\n        <tr><td class="vn">11번가</td><td>삼원 크리스탈 트레싱지 A3 80g 100매</td><td class="r"><span class="num">16,500원</span><small>+ 3,500원</small></td><td class="r num">165원</td><td>A3라 여유 있게 덮임. A4 100매는 8,800원이지만 A4(297×210)는 작은 상자(270×220)도 10mm 모자람</td></tr>\n        <tr><td class="vn">G마켓</td><td>신한 트레싱지 4절 75g 50매</td><td class="r"><span class="num">15,040원</span></td><td class="r num">301원</td><td>브랜드품. 비쌈</td></tr>\n        <tr><td class="vn">옥션</td><td>삼원 트레싱지 4절 100매 80g</td><td class="r"><span class="num">20,710원</span></td><td class="r num">207원</td><td>브랜드품. 비쌈</td></tr>\n      </tbody>\n    </table></div>\n    <p class="note">트레이싱지는 A4 100매 묶음이 3,000~9,000원대로 흔하지만 A4는 작은 상자도 덮지 못합니다. 4절 기준으로 보면 오픈마켓 6,590원(66원/매)이 최저이고, 하나페이퍼몰은 108원/매지만 습자지와 한 번에 받을 수 있습니다. 평량은 50~80g 중 얇은 쪽(50g)이 목업 사진처럼 아래 그림이 은은하게 비칩니다.</p>\n  </div>\n\n  <div class="block" id="sticker">')

sub('<li><span><a class="p" href="https://hanapapermall.co.kr/product/detail.html?product_no=4952" target="_blank" rel="noopener">포장용 색화지 2절 250매 화이트</a></span><span class="num">8,300원</span></li>',
    '<li><span><a class="p" href="https://hanapapermall.co.kr/product/detail.html?product_no=4952" target="_blank" rel="noopener">포장용 색화지 2절 250매 화이트</a></span><span class="num">8,300원</span></li>\n        <li><span><a class="p" href="https://hanapapermall.co.kr/product/detail.html?product_no=4228&amp;cate_no=307&amp;display_group=1" target="_blank" rel="noopener">트레싱지 전지 22매</a> (4절 88매 환산, 재입고 확인) · 대안 G마켓 4절 100매 6,590원</span><span class="num">9,500원</span></li>')

sub('<a href="#tissue">습자지</a><a href="#sticker">',
    '<a href="#tissue">습자지</a><a href="#tracing">트레이싱지</a><a href="#sticker">')

sub("<footer>모든 가격은 2026-10-18 기준 태스크·견적서 기재 금액이며,",
    "<footer>시안은 2026-10-25 기준. 가격은 2026-10-18 기준 태스크·견적서 기재 금액이며(네임택·사각 스티커·명함·트레이싱지는 추정 또는 오픈마켓 시세),")

# ── 10-25 실제 견적 반영 + 01 발주처별 묶음 ──────────────────────────────
import re as _re

VCSS = """

/* 표 가독성 (10-25) */
table{font-size:13.5px}
th,td{padding:12px 14px;line-height:1.55}
td small{font-size:12px;line-height:1.5;margin-top:4px}
td .num{display:inline-block;line-height:1.5}
td.r{min-width:118px}
td.r .num{display:block}
td.r small{text-align:right}
td:last-child{min-width:240px}
td.vn{min-width:128px}
.cart li{flex-wrap:wrap;line-height:1.5}
.cart li span:first-child{flex:1 1 180px}
.cart li span:last-child{flex:0 1 auto;max-width:100%;white-space:normal}
.cart li span:last-child.num{white-space:normal}
.vcard li span:first-child{flex:1 1 200px;min-width:0}
.vcard li{flex-wrap:wrap}
td.vn small{white-space:normal}
td .tag{margin:0 2px 4px 0}
.vn small{margin-top:3px}
.unit span{line-height:1.5;padding:5px 0}
.unit span.tot{padding-top:9px}
.vendors{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:14px}
.vcard{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px;display:flex;flex-direction:column;gap:8px}
.vcard.wide{grid-column:1/-1}
.vcard .vh{display:flex;justify-content:space-between;align-items:baseline;gap:8px;flex-wrap:wrap}
.vcard .vh h3{font-size:16px}
.vcard .vh h3 a{color:inherit;text-decoration:none;border-bottom:1px solid var(--line-strong)}
.vcard .vh .vs{font-size:12.5px;color:var(--muted)}
.vcard ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column}
.vcard li{display:flex;justify-content:space-between;gap:12px;padding:6px 0;border-top:1px dashed var(--line);font-size:13.5px}
.vcard li:first-child{border-top:0}
.vcard li .num{white-space:nowrap}
.vcard li small{display:block;color:var(--muted);font-size:12px}
.vcard .vt{display:flex;justify-content:space-between;gap:12px;padding-top:10px;border-top:2px solid var(--ink);font-weight:700;font-size:14.5px}
.vcard .vt small{font-weight:400;color:var(--muted);font-size:12px}
.vcard .vn{font-size:12.5px;color:var(--muted);margin:0;line-height:1.55}
.grand{margin-top:14px;background:#16130F;color:#FAF7F0;border-radius:var(--radius);padding:14px 18px;display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}
.grand .num{font-size:20px;font-weight:700}
.grand small{opacity:.75;font-size:12.5px;color:#FAF7F0}
.grand .num{color:#FAF7F0}
"""
sub("</style>", VCSS + "</style>")

SUMMARY = """<section id="summary">
  <h2><span class="k">01</span>최종 발주처 · 발주처별 합계</h2>
  <p class="note">같은 발주처 품목을 한 카드에 모았습니다. 금액은 10-25 자동견적·견적서 기준, <b>VAT 포함</b>으로 통일했고, 성원애드피아·래포리·하나페이퍼몰은 <b>배송비 별도</b>입니다. 상자는 큰 300 + 작은 400장 최소수량, 인쇄물은 최소수량 1회분입니다.</p>
  <div class="vendors">
    <div class="vcard wide">
      <div class="vh"><h3>① <a href="https://www.upackage.co.kr/" target="_blank" rel="noopener">유패키지</a> — 선물세트 상자 2종</h3><span class="vs">자동견적 NO. 2026102517371044 · 2026-10-25 · G형 · E골 · WT.S.K · 검정 1도 · 5면 인쇄(정면·후면·좌·우·윗면) · 서울 마포 택배</span></div>
      <ul>
        <li><span>큰 360×270×110 (내경 345×267×107) · 300장<small>상품 321,560 + 목형 150,000 + 인쇄판 121,860 + 택배 30,000 = 623,420원 (VAT 별도)</small></span><span class="num">685,762원<small>장당 2,286원</small></span></li>
        <li><span>작은 270×220×110 (내경 255×217×107) · 400장<small>상품 335,740 (839.35/장) + 목형 150,000 + 인쇄판 65,880 + 택배 30,000 = 581,620원 (VAT 별도)</small></span><span class="num">639,782원<small>장당 1,599원</small></span></li>
      </ul>
      <div class="vt"><span>유패키지 합계 <small>견적서 합계 1,325,540원 (VAT 별도) 기준</small></span><span class="num">1,458,094원</span></div>
      <p class="vn">⚠ 견적서 합계(1,325,540)가 두 줄 항목 합(1,205,040)보다 120,500원 많습니다(상품합계 723,030 / 추가금액 602,510). 자동견적 집계 방식 차이로 보이니 발주 전 유패키지에 확인. ⚠ 기성 규격인데 목형비 150,000원이 사이즈마다 잡혀 있어 함께 확인(인쇄 신규제작 때문일 수 있음). 10-18 수기 견적(585,360 / 571,860)보다 각각 올랐습니다.</p>
    </div>
    <div class="vcard">
      <div class="vh"><h3>② <a href="https://www.swadpia.co.kr/" target="_blank" rel="noopener">성원애드피아</a> — 인쇄물 5종</h3><span class="vs">견적서 2026-10-25 · 최소수량 · VAT 포함 · <b>배송비 별도</b></span></div>
      <ul>
        <li><span>포장 스티커 (원형 50×50) · 500장 = 1,000개<small>도무송 58×112 1장에 2개 · 아트 75g · 단면칼라</small></span><span class="num">14,300원<small>14원/개</small></span></li>
        <li><span>쇼핑백 스티커 (사각 70×160) · 500매<small>아트 75g · 단면칼라</small></span><span class="num">13,530원<small>27원/개</small></span></li>
        <li><span>브랜드 엽서 100×148 · 100매<small>랑데뷰 240g · 양면 먹1도 · 200매는 11,330원(57원/매)</small></span><span class="num">7,040원<small>70원/매</small></span></li>
        <li><span>주의사항 네임택 80×140 · 100매<small>랑데뷰 240g · 양면 먹1도 · 200매는 9,570원(48원/매)</small></span><span class="num">6,160원<small>62원/매</small></span></li>
        <li><span>명함 90×50 양면칼라 · 200매<small>반누보 화이트 204g · 400매 12,100원(30원) · 1,000매 25,300원(25원) · 운영용이라 세트 원가 미포함</small></span><span class="num">6,050원<small>30원/매</small></span></li>
      </ul>
      <div class="vt"><span>성원애드피아 합계 <small>5종 최소수량 · 배송비 별도</small></span><span class="num">47,080원</span></div>
      <p class="vn">엽서·네임택을 200매로 올리면 54,780원. 다섯 품목을 한 주문으로 묶어 배송비 1회.</p>
    </div>
    <div class="vcard">
      <div class="vh"><h3>③ <a href="https://hangarampackage.shop/" target="_blank" rel="noopener">래포리패키지</a> — 끈</h3><span class="vs">10-18 가격 · 배송비 3,500원 (10만 원 이상 무료)</span></div>
      <ul>
        <li><span>컬러 마끈 블랙 2mm × 50m (품목 리본) <span class="tag t-best">필수</span></span><span class="num">2,300원</span></li>
        <li><span>공단리본끈 버건디 6mm × 22m (상자 묶음) <span class="tag t-acc">추가</span></span><span class="num">900원</span></li>
        <li><span>공단리본끈 블랙 (상자 묶음 기본색 후보) <span class="tag t-warn">보류</span><small>양면 블랙 3mm × 45m 2,700원(60원/m) 확인됨 · 버건디와 같은 6mm 폭이 있는지 확인 후 결정</small></span><span class="num">—</span></li>
        <li><span>공단리본끈 녹색 (크리스마스 시즌 오픈 대비) <span class="tag t-warn">보류</span><small>시즌 한정색 · 가격·규격 미확인(버건디 6mm × 22m 900원과 같은 라인일 것) · 오픈 시점 확정 후 추가</small></span><span class="num">—</span></li>
        <li><span>고급 쇼핑백 화이트 40×28×12 / 30×25×15 (추가 구성)<small>10-25 재확인: 두 규격 모두 SOLD OUT · 재입고 시 2,500 / 3,300원</small></span><span class="num">—</span></li>
      </ul>
      <div class="vt"><span>래포리패키지 합계 <small>1롤씩 · 배송비 별도</small></span><span class="num">3,200원</span></div>
      <p class="vn">합계는 마끈 + 공단 버건디 1롤씩. 보류 2종(공단 블랙·녹색)은 오픈 시즌·기본색 확정 뒤 같은 주문에 얹으면 됨. 물량 기준 소모량(마끈 21롤 · 공단 59롤)은 04 세트 원가 표 참고. 스웨이드로 바꾸면 90m 롤 10,800원.</p>
    </div>
    <div class="vcard">
      <div class="vh"><h3>④ <a href="https://hanapapermall.co.kr/" target="_blank" rel="noopener">하나페이퍼몰</a> — 종이류</h3><span class="vs">배송비 별도</span></div>
      <ul>
        <li><span><a href="https://hanapapermall.co.kr/product/detail.html?product_no=4952" target="_blank" rel="noopener">포장용 색화지 2절 250매 화이트</a> (습자지 대용)</span><span class="num">8,300원<small>33원/매</small></span></li>
        <li><span><a href="https://hanapapermall.co.kr/product/detail.html?product_no=4228&amp;cate_no=307&amp;display_group=1" target="_blank" rel="noopener">트레싱지 전지 22매</a> = 4절 88매 (맨 위 덮는 용) <span class="tag t-acc">신규</span><small>50g / 82g 선택 · 페이지에 SOLD OUT 이미지, 재입고 확인 · 대안 G마켓 4절 100매 6,590원</small></span><span class="num">9,500원<small>108원/매</small></span></li>
      </ul>
      <div class="vt"><span>하나페이퍼몰 합계 <small>1팩씩 · 배송비 별도</small></span><span class="num">17,800원</span></div>
    </div>
    <div class="vcard">
      <div class="vh"><h3>⑤ 동네 철물점·잡화상 — 에어캡</h3><span class="vs">배송비 없음</span></div>
      <ul><li><span>에어캡 롤 (폭·길이 확인)<small>유패키지 18,000원은 대안</small></span><span class="num">약 5,000원</span></li></ul>
      <div class="vt"><span>합계</span><span class="num">약 5,000원</span></div>
    </div>
    <div class="vcard">
      <div class="vh"><h3>보류 2종</h3><span class="vs">오픈 전 결정</span></div>
      <ul>
        <li><span>품명 스티커 (상자 안 품목 표시) <span class="tag t-warn">보류</span><small>자체 출력(라벨지)으로 갈지 성원에 추가 발주할지 미정 · 발주 시 성원 주문에 얹기</small></span><span class="num">—</span></li>
        <li><span>완충 스티로폼 <span class="tag t-warn">보류</span><small>10-25 결정 · 에어캡 + 습자지로만 완충</small></span><span class="num">—</span></li>
      </ul>
    </div>
  </div>
  <div class="grand"><span>1회 최소 발주 합계 <small>상자 700장 + 인쇄물 최소수량 + 끈·종이 1단위 · VAT 포함</small></span><span><span class="num">약 1,531,000원</span> <small>+ 택배비 3건(성원·래포리·하나)</small></span></div>
</section>"""
html = _re.sub(r'<section id="summary">.*?</section>', lambda m: SUMMARY, html, count=1, flags=_re.S)
assert 'class="vendors"' in html

# 00 시안 카드 문구
sub('큰 2,146원 × 300장 = 643,896원 · 작은 1,573원 × 400장 = 629,046원 (VAT·서울 택배 포함, 10-18 견적). 견적의 인쇄 면적 기준(윗면+옆면)과 시안이 일치.',
    '10-25 자동견적: 큰 300장 685,762원(2,286원/장) · 작은 400장 639,782원(1,599원/장), VAT·목형·인쇄판·서울 택배 포함. 인쇄면은 윗면+옆 4면으로 시안과 일치.')
sub('도무송 500장(1장 2개) 14,300원 · 약 15원/개.', '견적서 10-25: 도무송 58×112 500장(1장 2개=1,000개) 14,300원 · 14원/개 · 배송비 별도.')
sub('디지털 엽서 먹1도 양면 100매 6,490원 · 65원/매.', '견적서 10-25: 랑데뷰 240g 양면 먹1도 100매 7,040원(70원/매) · 200매 11,330원(57원/매) · 배송비 별도.')
sub('엽서와 같은 디지털 인쇄로 비규격 사이즈 입력 · <span class="est">추정</span> 100매 약 6,500원 · 약 65원/매.', '견적서 10-25: 랑데뷰 240g 양면 먹1도 100매 6,160원(62원/매) · 200매 9,570원(48원/매) · 배송비 별도.')
sub('도무송 사각라운드 비규격 · <span class="est">추정</span> 500개 약 15,000~20,000원 · 약 30~40원/개.', '견적서 10-25: 아트 75g 단면칼라 500매 13,530원 · 27원/개 · 배송비 별도.')

# 02 상세: 신규 인쇄물 블록을 실제값으로
sub('<h3>5-1. 신규 인쇄물 3종 — 성원애드피아 <span class="est">추정 견적</span></h3><span class="sz">10-25 시안에서 추가된 품목 · 사이트 주문창 계산 전</span>',
    '<h3>5-1. 신규 인쇄물 3종 — 성원애드피아 견적서 (10-25)</h3><span class="sz">VAT 포함 · 배송비 별도</span>')
sub('<thead><tr><th>품목</th><th>사양</th><th class="r">추정 가격</th><th class="r">개당</th><th>환산 근거</th></tr></thead>',
    '<thead><tr><th>품목</th><th>사양</th><th class="r">가격</th><th class="r">개당</th><th>비고</th></tr></thead>')
sub('<td class="r"><span class="num">약 6,500원</span> / 100매</td><td class="r num">약 65원</td><td>엽서 100×148 100매 6,490원과 같은 상품·용지. 면적이 작아 같거나 조금 낮을 것</td>',
    '<td class="r"><span class="num">6,160원</span> / 100매<br><span class="num">9,570원</span> / 200매</td><td class="r num">62원<br>48원</td><td>견적서 기준(랑데뷰 240g · 양면 먹1도 · 목형비 1,500 포함). 품목당 1매라 200매부터 시작해도 됨</td>')
sub('<td class="r"><span class="num">약 15,000 ~ 20,000원</span> / 500개</td><td class="r num">약 30~40원</td><td>원형 50mm 500장(1,000개) 14,300원. 면적 약 3배라 1장 1개 배치로 가정. 쇼핑백 옵션 선택분만 필요하니 수량은 줄여도 됨</td>',
    '<td class="r"><span class="num">13,530원</span> / 500매</td><td class="r num">27원</td><td>견적서 기준(아트 75g · 단면칼라). 쇼핑백 옵션 선택분만 필요하니 500매면 충분</td>')
sub('<td class="r"><span class="num">약 5,000 ~ 8,000원</span> / 200매</td><td class="r num">약 25~40원</td><td>업계 일반 명함 시세. 운영용이라 세트 원가 미포함</td>',
    '<td class="r"><span class="num">6,050원</span> / 200매<br><span class="num">12,100원</span> / 400매<br><span class="num">25,300원</span> / 1,000매</td><td class="r num">30원<br>30원<br>25원</td><td>견적서 기준(반누보 화이트 204g · 양면칼라). 400매까지 단가 동일, 1,000매에서 17% 하락. 운영용이라 세트 원가 미포함</td>')
sub('세 품목 모두 원형 스티커·엽서와 같은 주문으로 묶으면 택배비는 1회입니다. 정확한 금액은 성원애드피아 주문창에 사이즈·수량을 넣으면 바로 계산되므로, 발주 직전에 이 표의 추정값을 실제값으로 바꿔 주세요.',
    '세 품목 모두 10-25 견적서 금액입니다. 원형 스티커·엽서와 한 주문으로 묶으면 택배비 1회. 견적서 PDF는 assets/quotes-261025/.')
sub('<span class="sz">100×148mm (시안 확정) · 세트당 1매</span>', '<span class="sz">100×148mm (시안 확정) · 세트당 1매 · 10-25 견적 100매 7,040 / 200매 11,330원</span>')

# 03 발주처별 묶음 (성원 li)
sub('<li><span>주의사항 네임택 80×140 양면 100매 <span class="est">추정</span></span><span class="num">약 6,500원</span></li>',
    '<li><span>주의사항 네임택 80×140 양면 100매 (200매 9,570원)</span><span class="num">6,160원</span></li>')
sub('<li><span>쇼핑백 사각 스티커 70×160 500개 <span class="est">추정</span></span><span class="num">약 15,000~20,000원</span></li>',
    '<li><span>쇼핑백 사각 스티커 70×160 500매</span><span class="num">13,530원</span></li>')

# 04 세트 원가
sub('<span>상자 (유패키지 300장)</span><span class="num">2,146원</span>', '<span>상자 (유패키지 300장 · 10-25 자동견적)</span><span class="num">2,286원</span>')
sub('<span>상자 (유패키지 400장)</span><span class="num">1,573원</span>', '<span>상자 (유패키지 400장 · 10-25 자동견적)</span><span class="num">1,599원</span>')
sub('<span>원형 스티커 1 + 엽서 1</span><span class="num">80원</span>', '<span>원형 스티커 1 + 엽서 1 (100매 / 200매 단가)</span><span class="num">71 ~ 84원</span>', 2)
sub('주의사항 네임택 3매 × 약 65원 <span class="est">추정</span></span><span class="num">195원</span>', '주의사항 네임택 3매 × 48~62원</span><span class="num">144 ~ 186원</span>')
sub('주의사항 네임택 1~2매 × 약 65원 <span class="est">추정</span></span><span class="num">65 ~ 130원</span>', '주의사항 네임택 1~2매 × 48~62원</span><span class="num">48 ~ 124원</span>')
sub('<span class="tot">합계</span><span class="tot num">약 3,020 ~ 3,160원</span>', '<span class="tot">합계</span><span class="tot num">약 3,090 ~ 3,290원</span>')
sub('약 2,010 ~ 2,080원', '약 2,000 ~ 2,100원')
sub('약 2,200 ~ 2,320원', '약 2,190 ~ 2,350원')
sub('네임택·트레이싱지는 추정 단가라 ±50원 범위로 보면 됩니다. 스티로폼(보류)은 0원.', '상자·인쇄물은 10-25 견적 실제값, 트레이싱지만 오픈마켓 시세입니다. 스티로폼(보류)은 0원.')
sub('<td class="r num">1,272,942원</td>', '<td class="r num">1,458,094원<small>10-25 자동견적 합계 · VAT 포함</small></td>')
sub('<td>성원 100매 약 6,500원</td><td class="r num">17건분</td><td class="r num">약 110,500원 + 택배</td>', '<td>성원 200매 9,570원</td><td class="r num">9건분</td><td class="r num">86,130원 + 택배</td>')
sub('<td class="r num">7건분</td><td class="r num">45,430원 + 택배</td>', '<td class="r num">4건분 (200매)</td><td class="r num">45,320원 + 택배</td>')
sub('<a class="p" href="https://www.swadpia.co.kr/goods/goods_view/COD3000/GOD3001" target="_blank" rel="noopener">성원 100매</a> 6,490원', '<a class="p" href="https://www.swadpia.co.kr/goods/goods_view/COD3000/GOD3001" target="_blank" rel="noopener">성원 200매</a> 11,330원')
sub('(네임택·사각 스티커·명함·트레이싱지는 추정 또는 오픈마켓 시세),', '상자·성원 인쇄물은 2026-10-25 자동견적·견적서 금액(트레이싱지만 오픈마켓 시세),')
sub('<span>기준일 <b>2026-10-25</b> (가격은 10-18 견적, 신규 3종은 추정)</span>', '<span>기준일 <b>2026-10-25</b> (상자·인쇄물은 10-25 견적, 끈·종이는 10-18)</span>')
sub('<a href="#designs">시안</a><a href="#summary">최종 발주처</a>', '<a href="#designs">시안</a><a href="#summary">발주처별 합계</a>')

sub('<p class="note">인쇄 조건과 가격을 함께 보면 유패키지 한 곳만 남습니다.',
    '<p class="note"><b>10-25 자동견적 갱신:</b> 위 표의 유패키지 두 줄은 10-18 수기 견적입니다. 10-25 사이트 자동견적(5면 검정 1도, 목형 150,000 + 인쇄판 포함, 서울 택배)은 큰 300장 685,762원(2,286원/장), 작은 400장 639,782원(1,599원/장), 견적서 합계 1,458,094원(VAT 포함)으로 올랐습니다. 01 발주처별 합계 참고.</p>\n    <p class="note">인쇄 조건과 가격을 함께 보면 유패키지 한 곳만 남습니다.')

# 03 발주처별 묶음 섹션 제거 — 01 발주처별 합계와 중복(숫자도 10-18 기준이라 충돌)
html = _re.sub(r'
<section id="carts">.*?</section>
', '
', html, count=1, flags=_re.S)
assert 'id="carts"' not in html
sub('<a href="#carts">발주처별 묶음</a>', '')
sub('<h2><span class="k">04</span>세트 1개당 자재비</h2>', '<h2><span class="k">03</span>세트 1개당 자재비</h2>')
sub('은 04 세트 원가 표 참고.', '은 03 세트 원가 표 참고.')
sub('10-18 비교표는 아래 02~04에 그대로 두었습니다.', '10-18 비교표는 아래 02에 그대로 두었습니다.')

OUT.write_text(html, encoding="utf-8")
print(OUT, f"{OUT.stat().st_size/1024:.0f} KB")
