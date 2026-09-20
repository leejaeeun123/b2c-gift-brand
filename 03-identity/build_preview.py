# -*- coding: utf-8 -*-
"""시안 페이지 빌드 — SVG를 인라인해 file:// 에서도 보이게 한다"""
import io, os
d = os.path.dirname(os.path.abspath(__file__))
MOTIFS = [("plate","접시"),("bowl","볼"),("cup","잔"),("spoon","수저"),("fork","포크"),("knife","나이프"),
          ("flower","꽃"),("vase","화병과 꽃"),("candle","초"),("ribbon","리본"),("book","책"),
          ("heart","하트"),("clover","클로버"),("star","별"),("fish","물고기"),("pear","배"),
          ("urchin","성게"),("anemone","말미잘"),("starfish","불가사리"),("clam","진주조개"),
          ("coral","산호"),("seahorse","해마"),("wave","파도"),("seaweed","해초"),
          ("sea-clover","바다클로버"),("conch","소라"),("sparkle-star","반짝별"),("crab","게")]
CHARS  = [("turtle","거북이"),("dog","강아지")]
def read(p): return io.open(os.path.join(d,p),encoding="utf-8").read()
def cell(f,ko,pre): return '<div class="cell">%s<span>%s</span></div>'%(read(pre+f+".svg"),ko)
def ic(f,px=18): return read("motif-%s.svg"%f).replace('width="100" height="100"','width="%d" height="%d"'%(px,px))
html = read("_preview_tpl.html")
html = (html.replace("{{GRID}}","".join(cell(f,k,"motif-") for f,k in MOTIFS))
            .replace("{{CHAR}}","".join(cell(f,k,"char-") for f,k in CHARS))
            .replace("{{INK}}","".join(read("motif-%s.svg"%f).replace('color="#262320"','color="#FFFFFF"') for f,_ in MOTIFS[:7]))
            .replace("{{ICON1}}",ic("plate")).replace("{{ICON2}}",ic("cup")).replace("{{ICON3}}",ic("bowl")))
io.open(os.path.join(d,"motifs-preview.html"),"w",encoding="utf-8").write(html)
print("built")
