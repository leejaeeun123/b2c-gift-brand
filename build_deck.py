# -*- coding: utf-8 -*-
"""deck.html 빌드 — 03-identity의 SVG를 인라인해 단일 파일로 만든다."""
import io, os
D = os.path.dirname(os.path.abspath(__file__))
ID = os.path.join(D, "03-identity")

def svg(name, px=None, color=None):
    s = io.open(os.path.join(ID, name + ".svg"), encoding="utf-8").read()
    if px:    s = s.replace('width="100" height="100"', 'width="%d" height="%d"' % (px, px))
    if color: s = s.replace('color="#262320"', 'color="%s"' % color)
    return s

MOTIFS = [("plate","접시"),("bowl","볼"),("cup","잔"),("spoon","수저"),("fork","포크"),("knife","나이프"),
          ("flower","꽃"),("vase","화병과 꽃"),("candle","초"),("ribbon","리본"),("book","책"),
          ("heart","하트"),("clover","클로버"),("star","별"),("fish","물고기"),("pear","배")]

grid   = "".join('<figure>%s<figcaption>%s</figcaption></figure>' % (svg("motif-"+f), k) for f, k in MOTIFS)
turtle = svg("char-turtle")
dog    = svg("char-dog")
mark   = lambda n, px=22: svg("motif-"+n, px)

html = io.open(os.path.join(D, "_deck_tpl.html"), encoding="utf-8").read()
html = (html.replace("{{MOTIFS}}", grid)
            .replace("{{TURTLE}}", turtle).replace("{{DOG}}", dog)
            .replace("{{M_PLATE}}", mark("plate")).replace("{{M_RIBBON}}", mark("ribbon"))
            .replace("{{M_HEART}}", mark("heart")).replace("{{M_BOOK}}", mark("book"))
            .replace("{{M_CLOVER}}", mark("clover")).replace("{{M_STAR}}", mark("star"))
            .replace("{{M_CUP}}", mark("cup")).replace("{{M_FLOWER}}", mark("flower"))
            .replace("{{M_PEAR}}", mark("pear")).replace("{{M_CANDLE}}", mark("candle"))
            .replace("{{T_SMALL}}", svg("char-turtle", 26)))
io.open(os.path.join(D, "deck.html"), "w", encoding="utf-8").write(html)
print("deck.html built (%.0f KB)" % (len(html)/1024))
