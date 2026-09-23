# -*- coding: utf-8 -*-
"""deck.html 빌드 — 03-identity의 SVG를 인라인해 단일 파일로 만든다.

모든 SVG는 미리보기와 동시에 data URI 다운로드 링크로 박아 넣는다. 링크 하나로 공유하면
받는 쪽이 파일을 따로 받지 않고도 덱에서 바로 내려받는다.
재현: python build_deck.py
"""
import base64, io, os

D = os.path.dirname(os.path.abspath(__file__))
ID = os.path.join(D, "03-identity")
REF = os.path.join(D, "assets", "reference")


def raw(name):
    return io.open(os.path.join(ID, name + ".svg"), encoding="utf-8").read()


def svg(name, px=None, color=None):
    s = raw(name)
    if px:    s = s.replace('width="100" height="100"', 'width="%d" height="%d"' % (px, px))
    if color: s = s.replace('color="#262320"', 'color="%s"' % color)
    return s


def fit(name):
    """다운로드 칩 미리보기용 — 크기를 칸에 맞춘다."""
    s = raw(name)
    for a in ('width="%s"' % w for w in ("100", "634", "1056", "1302", "658", "2581")):
        s = s.replace(a, "", 1)
    for a in ('height="%s"' % h for h in ("100", "686", "320", "277", "324")):
        s = s.replace(a, "", 1)
    return s.replace("<svg ", '<svg preserveAspectRatio="xMidYMid meet" ', 1)


def datauri(name):
    b = io.open(os.path.join(ID, name + ".svg"), encoding="utf-8").read().encode("utf-8")
    return "data:image/svg+xml;base64," + base64.b64encode(b).decode()


def chip(name, label, dark=False):
    return ('<a class="dl%s" href="%s" download="%s.svg" title="%s.svg 내려받기">'
            '<span class="pv">%s</span><span class="nm">%s</span>'
            '<span class="fn">%s.svg</span></a>'
            % (" dark" if dark else "", datauri(name), name, name, fit(name), label, name))


def img(name, w=1400, q=80):
    """사진은 리사이즈 후 base64로 묻는다 — 파일 하나로 공유한다."""
    from PIL import Image
    im = Image.open(os.path.join(REF, name)).convert("RGB")
    im.thumbnail((w, w * 2), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


MOTIFS = [("plate","접시"),("bowl","볼"),("cup","잔"),("spoon","수저"),("fork","포크"),("knife","나이프"),
          ("flower","꽃"),("vase","화병과 꽃"),("candle","초"),("ribbon","리본"),("book","책"),
          ("heart","하트"),("clover","클로버"),("star","별"),("fish","물고기"),("pear","배")]
SEA = [("urchin","성게"),("anemone","말미잘"),("starfish","불가사리"),("clam","진주조개"),
       ("coral","산호"),("seahorse","해마"),("wave","파도"),("seaweed","해초"),
       ("sea-clover","바다클로버"),("conch","소라"),("sparkle-star","반짝별"),("crab","게")]
LOGOS = [("logo-signature-ink","시그니처 · 잉크",False),
         ("logo-signature-white","시그니처 · 화이트",True),
         ("logo-wordmark-ko-ink","오하리상점 · 잉크",False),
         ("logo-wordmark-ko-white","오하리상점 · 화이트",True),
         ("logo-wordmark-en-ink","OHARISTORE · 잉크",False),
         ("logo-wordmark-en-white","OHARISTORE · 화이트",True),
         ("logo-wordmark-ohari-ink","OHARI · 잉크",False),
         ("logo-wordmark-ohari-white","OHARI · 화이트",True)]

grid = lambda items: "".join(
    '<figure>%s<figcaption>%s</figcaption></figure>' % (svg("motif-" + f), k) for f, k in items)
mark = lambda n, px=22: svg("motif-" + n, px)

DL_LOGO = "".join(chip(n, k, d) for n, k, d in LOGOS)
DL_CHAR = chip("char-turtle", "거북이 · 정본") + chip("char-dog", "강아지 · 예비")
DL_V1 = "".join(chip("motif-" + f, k) for f, k in MOTIFS)
DL_V2 = "".join(chip("motif-" + f, k) for f, k in SEA)

html = io.open(os.path.join(D, "_deck_tpl.html"), encoding="utf-8").read()
for k, v in [
    ("{{MOTIFS}}", grid(MOTIFS)), ("{{SEA}}", grid(SEA)),
    ("{{TURTLE}}", svg("char-turtle")), ("{{DOG}}", svg("char-dog")),
    ("{{SIG}}", svg("logo-signature-ink")), ("{{SIG_W}}", svg("logo-signature-white")),
    ("{{KO}}", svg("logo-wordmark-ko-ink")), ("{{EN}}", svg("logo-wordmark-en-ink")),
    ("{{OHARI}}", svg("logo-wordmark-ohari-ink")),
    ("{{DL_LOGO}}", DL_LOGO), ("{{DL_CHAR}}", DL_CHAR),
    ("{{DL_V1}}", DL_V1), ("{{DL_V2}}", DL_V2),
    ("{{M_PLATE}}", mark("plate")), ("{{M_RIBBON}}", mark("ribbon")),
    ("{{M_HEART}}", mark("heart")), ("{{M_BOOK}}", mark("book")),
    ("{{M_CLOVER}}", mark("clover")), ("{{M_STAR}}", mark("star")),
    ("{{M_CUP}}", mark("cup")), ("{{M_FLOWER}}", mark("flower")),
    ("{{M_PEAR}}", mark("pear")), ("{{M_CANDLE}}", mark("candle")),
    ("{{T_SMALL}}", svg("char-turtle", 26)),
    ("{{R_DOG}}", img("inap-dog-mark.jpg")),
    ("{{R_STICKERBOOK}}", img("inap-stickerbook.jpg")),
    ("{{R_ANTS}}", img("inap-ants.jpg")),
    ("{{R_ANIMAL}}", img("inap-love-animal.jpg")),
    ("{{R_BEAR}}", img("inap-daelim-bath.jpg")),
    ("{{R_GRID}}", img("inap-square-grid.jpg")),
    ("{{R_SOKAMONO}}", img("sokamono-stickers.jpg")),
    ("{{R_SHEET}}", img("motif-sheet-v1.jpg")),
    ("{{R_SHEET2}}", img("motif-sheet-v2-sea.png")),
    ("{{P_TIE}}", img("packaging-ref-04.jpg", 1000)),
    ("{{P_BOX}}", img("packaging-ref-03.jpg", 1000)),
    ("{{P_COVER}}", img("packaging-ref-02.jpg", 1000)),
]:
    html = html.replace(k, v)

assert "{{" not in html, "치환 안 된 자리: " + html[html.index("{{"):html.index("{{") + 40]
io.open(os.path.join(D, "deck.html"), "w", encoding="utf-8").write(html)
print("deck.html built (%.0f KB)" % (len(html) / 1024))
