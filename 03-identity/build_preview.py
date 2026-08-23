# -*- coding: utf-8 -*-
import io, os
FILES=["plate","bowl","mug","glass","teapot","spoon","cutlery","tray","vase","candle","ribbon","letter","box","pear"]
KO={"plate":"접시","bowl":"볼","mug":"머그","glass":"잔","teapot":"주전자","spoon":"수저","cutlery":"포크와 나이프","tray":"트레이","vase":"화병과 꽃","candle":"초","ribbon":"리본 매듭","letter":"편지","box":"선물 상자","pear":"배"}
d=os.path.dirname(os.path.abspath(__file__))
svg={f:io.open(os.path.join(d,"motif-%s.svg"%f),encoding="utf-8").read() for f in FILES}
def cell(f,color=None,cls=""):
    s=svg[f]
    s=s.replace('color="#262320"','color="%s"'%color) if color else s
    return '<div class="cell %s">%s<span>%s</span></div>'%(cls,s,KO[f])
grid="".join(cell(f) for f in FILES)
inkrow="".join(svg[f].replace('color="#262320"','color="#F6F1E8"') for f in FILES[:7])
pers="".join(cell(f,"#D2502A") for f in FILES[:7])
cela="".join(cell(f,"#4A7A6B") for f in FILES[7:])
html=io.open(os.path.join(d,"_preview_tpl.html"),encoding="utf-8").read()
html=html.replace("{{GRID}}",grid).replace("{{INK}}",inkrow).replace("{{PERS}}",pers).replace("{{CELA}}",cela)
io.open(os.path.join(d,"motifs-preview.html"),"w",encoding="utf-8").write(html)
print("built")
