"""Prepare the illustration and font masks. Contest execution needs only main.py."""
import argparse
import base64
import json
import math
import zlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONTS = {"serif":"DMSerifDisplay-Regular.ttf","sans":"Barlow-Regular.ttf","bold":"Barlow-SemiBold.ttf"}
STYLES = {"section":("bold",18),"mast":("serif",73),"date":("bold",25),"small":("bold",16),
          "lead":("serif",62),"copy":("sans",24),"chart":("bold",19),"caption":("sans",15),
          "subhead":("serif",41),"body":("sans",22),"fine":("sans",13)}

def build_atlas(lines):
    atlas = {}
    for role, *_, line in lines:
        name, size = STYLES[role]
        font = ImageFont.truetype(str(ASSETS / FONTS[name]), size)
        face = atlas.setdefault(role,{})
        for char in set(line) - face.keys():
            dx, dy, right, bottom = font.getbbox(char)
            w,h = right-dx,bottom-dy
            raw = bytes(font.getmask(char,mode="L"))
            assert len(raw) == w*h
            face[char] = [round(font.getlength(char)*64),dx,dy,w,h,base64.b64encode(raw).decode()]
    return zlib.compress(json.dumps(atlas,sort_keys=True,separators=(",",":")).encode(),9)

def star(cx,cy,r):
    return [(cx+math.cos(i*math.pi/5-math.pi/2)*(r if i%2==0 else r*.43),
             cy+math.sin(i*math.pi/5-math.pi/2)*(r if i%2==0 else r*.43)) for i in range(10)]

def sanctions_panel():
    # Classical bank architecture and twelve stars of the European flag.
    im=Image.new("RGB",(451,123),"#DBE5CA")
    d=ImageDraw.Draw(im)
    for x in range(-180,520,9):
        d.line((x,123,x+140,0),fill="#D0DDC0",width=1)
    for i in range(12):
        a=math.tau*i/12-math.pi/2
        d.polygon(star(82+math.cos(a)*42,61+math.sin(a)*42,5),fill="#326257")
    for shift in [-19,0,19]:
        x=250+shift
        d.polygon([(x-93,52),(x,14),(x+93,52)],fill="#69947A" if shift!=19 else "#285548")
    d.polygon([(161,53),(269,12),(375,53)],fill="#285548")
    d.polygon([(178,48),(269,17),(356,48)],fill="#B7CDAD")
    for x in range(178,358,29):
        d.rectangle((x,58,x+14,102),fill="#315E52")
        d.line((x+5,60,x+5,100),fill="#A8C7A4",width=2)
        d.rectangle((x-3,54,x+17,59),fill="#315E52")
    for y,pad in [(103,0),(110,7),(117,14)]:
        d.rectangle((166-pad,y,365+pad,y+5),fill="#315E52")
    return im

def shipping_panel():
    im=Image.new("RGB",(447,123),"#D9E8EB")
    d=ImageDraw.Draw(im)
    for y in range(-7,146,11):
        d.line([(x,y+4*math.sin(x/27+y/11)) for x in range(-5,460,3)],fill="#B5D1D4",width=1)
    for x,y,s in [(31,51,1.08),(171,31,.83),(294,62,.96)]:
        def points(coords): return [(x+a*s,y+b*s) for a,b in coords]
        d.polygon(points([(2,15),(115,15),(105,27),(17,27)]),fill="#244952")
        d.polygon(points([(19,14),(19,-1),(35,-1),(35,-7),(44,-7),(44,14)]),fill="#244952")
        for off in [54,68,82]:
            d.rectangle((x+off*s,y+6*s,x+(off+12)*s,y+13*s),fill="#638B8A")
        d.line(points([(0,30),(106,30)]),fill="#638B8A",width=2)
    return im

def make_plate(edition):
    im=Image.new("RGB",(1024,1024),"#F6F1E5")
    d=ImageDraw.Draw(im)
    d.rectangle((44,125,980,128),fill="#193638")
    d.rectangle((34,147,990,565),fill="#163B3B")
    # This date's lead is an archive photograph, captioned with its original year.
    portrait=Image.open(ASSETS/"huang-2023.jpg").convert("RGB")
    photo=ImageOps.fit(portrait,(378,383),method=Image.Resampling.LANCZOS,centering=(.53,.20))
    im.paste(photo,(612,147))
    d.rectangle((612,530,989,565),fill="#203031")
    d.line((61,430,569,430),fill="#527774",width=1)
    for i,value in enumerate(edition["chart"]["changes"]):
        x,y=241,494+31*i
        d.rectangle((x,y,x+190,y+8),fill="#3B5B58")
        d.rectangle((x,y,x+round(190*value/edition["chart"]["max"]),y+8),fill="#C9E98B")
    im.paste(sanctions_panel(),(44,632))
    im.paste(shipping_panel(),(533,632))
    d.line((513,594,513,956),fill="#C2C9B9")
    d.line((44,974,980,974),fill="#899A8F")
    return im

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("day")
    args=p.parse_args()
    folder=ROOT/"editions"/args.day
    data=json.loads((folder/"news.json").read_bytes())
    if data["art"]!="nov23":
        raise ValueError("Add the edition's artwork before preparing its plate")
    (folder/"plate.rgbz").write_bytes(zlib.compress(make_plate(data).tobytes(),9))
    (folder/"type.jsonz").write_bytes(build_atlas(data["lines"]))
