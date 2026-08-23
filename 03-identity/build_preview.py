# -*- coding: utf-8 -*-
import io, os
FILES=["plate","bowl","mug","glass","teapot","spoon","cutlery","tray","flower","candle","ribbon","letter","box","pear"]
KO={"plate":"접시","bowl":"볼","mug":"머그","glass":"잔","teapot":"주전자","spoon":"수저","cutlery":"포크와 나이프","tray":"트레이","flower":"꽃","candle":"초","ribbon":"리본 매듭","letter":"편지","box":"선물 상자","pear":"배"}
d=os.path.dirname(os.path.abspath(__file__))
svg={f:io.open(os.path.join(d,"motif-%s.svg"%f),encoding="utf-8").read() for f in FILES}
CH=[("turtle","거북이"),("turtle-gift","선물을 진 거북이"),("turtle-small","작은 거북이")]
for k,_ in CH: svg[k]=io.open(os.path.join(d,"char-%s.svg"%k),encoding="utf-8").read()
KO.update(dict(CH))
def cell(f,color=None,cls=""):
    s=svg[f]
    s=s.replace('color="#262320"','color="%s"'%color) if color else s
    return '<div class="cell %s">%s<span>%s</span></div>'%(cls,s,KO[f])
grid="".join(cell(f) for f in FILES)
inkrow="".join(svg[f].replace('color="#262320"','color="#F6F1E8"') for f in FILES[:7])
ic=lambda f:svg[f].replace('width="100" height="100"','width="18" height="18"')
html=io.open(os.path.join(d,"_preview_tpl.html"),encoding="utf-8").read()
html=(html.replace("{{GRID}}",grid).replace("{{INK}}",inkrow)
        .replace("{{CHAR}}","".join(cell(k) for k,_ in [CH[1],CH[0],CH[2]]))
        .replace("{{ICON1}}",ic("plate")).replace("{{ICON2}}",ic("mug")).replace("{{ICON3}}",ic("tray")))
io.open(os.path.join(d,"motifs-preview.html"),"w",encoding="utf-8").write(html)
print("built")
