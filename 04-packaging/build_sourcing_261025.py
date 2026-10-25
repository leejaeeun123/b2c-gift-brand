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
        {f("bottom.jpg", "아랫면 — 품명 스티커 자리", "full")}
      </div></div>"""

DESIGNS = f"""
<section id="designs">
  <h2><span class="k">00</span>패키지 시안 (2026-10-25)</h2>
  <p class="note">인쇄물 시안 7종입니다. 각 카드의 발주처·견적은 01 최종 발주처와 연결되고, 사이즈는 시안 기준 확정값입니다. 상자 아랫면의 회색 영역은 라벨지로 자체 출력하는 품명 스티커 자리입니다.</p>
  <div class="designs">
    <div class="design wide">
      <div class="dh"><h3>1. 선물세트 상자</h3><span class="sz">흰색 G형 일체형 · 먹1도 · 윗면 + 옆면 4면 + 아랫면 · 큰 360×270×110 / 작은 270×220×110mm</span></div>
      <div class="ref">{fig("box-reference.jpg", "G형 일체형 상자 (유패키지 기성 규격)", "")}<p>G형 일체형: 뚜껑과 몸체가 한 장으로 이어진 조립식 상자. 기성 규격이라 목형비 없음. 큰 사이즈는 품목 3개, 작은 사이즈는 품목 1~2개 세트용.</p></div>
      <div class="box-faces">
        {box_net("box-large", "큰 사이즈", "360×270×110mm · 300장", "윗면 — 해초 패턴")}
        {box_net("box-small", "작은 사이즈", "270×220×110mm · 400장", "윗면 — 거북이 + 클로버")}
      </div>
      <p class="dn">발주처 <b>유패키지</b> · 큰 2,146원 × 300장 = 643,896원 · 작은 1,573원 × 400장 = 629,046원 (VAT·서울 택배 포함, 10-18 견적). 이 견적의 인쇄 면적 기준은 윗면+옆면이었으므로 아랫면 인쇄 추가분은 발주 시 재확인. <a href="#box">상자 비교 보기</a></p>
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
      <p class="dn">발주처 <b>성원애드피아</b> · <span class="est">추정</span> 아트지 양면 200매 약 5,000~8,000원. 세트 동봉이 아니라 운영용이라 세트 원가에는 넣지 않음. <a href="#print-new">신규 인쇄물 견적 보기</a></p>
    </div>
    <div class="design">
      <div class="dh"><h3>6. 쇼핑백 스티커 (사각)</h3><span class="sz">70×160mm · 추가 구성 · 무지 쇼핑백용</span></div>
      <div class="imgs">{fig("sticker-bag.jpg", "사각 — OHARISTORE + 테이블웨어 실루엣", "tall")}</div>
      <p class="dn">발주처 <b>성원애드피아</b> · 도무송 사각라운드 비규격 · <span class="est">추정</span> 500개 약 15,000~20,000원 · 약 30~40원/개. 쇼핑백 자체는 래포리 재입고 대기. <a href="#bag">쇼핑백 비교 보기</a></p>
    </div>
  </div>
</section>
"""
sub('<section id="summary">', DESIGNS + '\n<section id="summary">')

# ── 01 최종 발주처 ──────────────────────────────────────────────────────
sub('<h2><span class="k">01</span>품목별 추천 발주처</h2>',
    '<h2><span class="k">01</span>최종 발주처 · 대략 견적</h2>\n  <p class="note">상자·끈·습자지·원형 스티커·엽서·에어캡은 10-18 비교 결론 그대로 확정. 주의사항 네임택·명함·쇼핑백 사각 스티커는 성원애드피아에서 함께 발주하며, 금액은 사이트 주문창 계산 전이라 기존 엽서·스티커 단가로 환산한 <span class="est">추정</span>값입니다.</p>')
sub('<div class="card"><div class="item">쇼핑백 (추가 구성 · 무지 + 사각 스티커)</div>',
    '<div class="card best"><div class="item">주의사항 네임택 80×140</div><div class="vendor"><a href="https://www.swadpia.co.kr/goods/goods_view/COD3000/GOD3001" target="_blank" rel="noopener">성원애드피아</a> <span class="est">추정</span></div><div class="price"><span class="num">약 6,500원</span> / 100매 · <span class="num">약 65원</span>/매</div><p class="why">엽서와 같은 디지털 인쇄(토너·먹1도 양면)에 사이즈만 직접 입력. 엽서와 한 주문으로 묶어 택배비 1회.</p></div>\n'
    '    <div class="card best"><div class="item">쇼핑백 사각 스티커 70×160</div><div class="vendor"><a href="https://www.swadpia.co.kr/goods/goods_view/CST2000/GST2001" target="_blank" rel="noopener">성원애드피아</a> <span class="est">추정</span></div><div class="price"><span class="num">약 15,000 ~ 20,000원</span> / 500개 · <span class="num">약 30~40원</span>/개</div><p class="why">도무송 사각라운드 비규격. 원형 50mm(1장 2개 14,300원)보다 면적이 커 1장 1개로 환산.</p></div>\n'
    '    <div class="card best"><div class="item">명함 90×50</div><div class="vendor"><a href="https://www.swadpia.co.kr/" target="_blank" rel="noopener">성원애드피아</a> <span class="est">추정</span></div><div class="price"><span class="num">약 5,000 ~ 8,000원</span> / 200매</div><p class="why">아트지 양면 기준. 운영용이라 세트 원가 미포함.</p></div>\n'
    '    <div class="card"><div class="item">쇼핑백 (추가 구성 · 무지 + 사각 스티커)</div>')
sub("핸즈픽 31·33호는 상자가 안 들어가거나 너무 깊음. 사각 스티커는 성원 재견적.",
    "핸즈픽 31·33호는 상자가 안 들어가거나 너무 깊음. 사각 스티커는 성원애드피아(위 카드).")

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
        <tr class="best"><td class="vn">명함</td><td>일반 명함 90×50<small>아트지 · 양면</small></td><td class="r"><span class="num">약 5,000 ~ 8,000원</span> / 200매</td><td class="r num">약 25~40원</td><td>업계 일반 명함 시세. 운영용이라 세트 원가 미포함</td></tr>
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
    '        <li><span>명함 90×50 양면 200매 <span class="est">추정</span></span><span class="num">약 5,000~8,000원</span></li>')

# ── 04 세트 원가: 네임택 반영 ──────────────────────────────────────────
sub("세트 구성: 상자 1개 + 품목마다 에어캡·습자지 2~3장·마끈 리본 + 상자 묶는 끈 + 스티커 1개 + 엽서 1매.",
    "세트 구성: 상자 1개 + 품목마다 에어캡·습자지 2~3장·마끈 리본·주의사항 네임택 + 상자 묶는 끈 + 스티커 1개 + 엽서 1매.")
sub('<span>마끈 리본 3개 × 약 0.6m</span><span class="num">90원</span>',
    '<span>마끈 리본 3개 × 약 0.6m</span><span class="num">90원</span>\n      <span>주의사항 네임택 3매 × 약 65원 <span class="est">추정</span></span><span class="num">195원</span>')
sub('<span class="tot">합계</span><span class="tot num">약 2,750 ~ 2,850원</span>',
    '<span class="tot">합계</span><span class="tot num">약 2,950 ~ 3,050원</span>')
sub('<span>마끈 리본 1~2개</span><span class="num">30 ~ 60원</span>',
    '<span>마끈 리본 1~2개</span><span class="num">30 ~ 60원</span>\n      <span>주의사항 네임택 1~2매 × 약 65원 <span class="est">추정</span></span><span class="num">65 ~ 130원</span>')
sub('<span class="tot">합계 (품목 1개)</span><span class="tot num">약 1,870 ~ 1,900원</span>',
    '<span class="tot">합계 (품목 1개)</span><span class="tot num">약 1,940 ~ 1,970원</span>')
sub('<span class="tot">합계 (품목 2개)</span><span class="tot num">약 2,000 ~ 2,080원</span>',
    '<span class="tot">합계 (품목 2개)</span><span class="tot num">약 2,130 ~ 2,210원</span>')
sub("상자가 큰 세트 자재비의 75%, 작은 세트의 80%를 차지합니다.",
    "상자가 큰 세트 자재비의 약 70%, 작은 세트의 75~80%를 차지합니다. 네임택은 추정 단가라 ±30원 범위로 보면 됩니다.")
sub('<tr><td>엽서</td><td class="r num">700매</td>',
    '<tr><td>주의사항 네임택<small>1,700품목 × 1매 · 추정</small></td><td class="r num">1,700매</td><td>성원 100매 약 6,500원</td><td class="r num">17건분</td><td class="r num">약 110,500원 + 택배</td></tr>\n      <tr><td>엽서</td><td class="r num">700매</td>')

sub("<footer>모든 가격은 2026-10-18 기준 태스크·견적서 기재 금액이며,",
    "<footer>시안은 2026-10-25 기준. 가격은 2026-10-18 기준 태스크·견적서 기재 금액이며(네임택·사각 스티커·명함은 추정),")

OUT.write_text(html, encoding="utf-8")
print(OUT, f"{OUT.stat().st_size/1024:.0f} KB")
