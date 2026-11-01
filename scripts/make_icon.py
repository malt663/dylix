#!/usr/bin/env python3
"""Render theos助手's app icon into the iOS icon catalog."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

folder = Path(__file__).resolve().parents[1] / 'Resources/Assets.xcassets/AppIcon.appiconset'
folder.mkdir(parents=True, exist_ok=True)
scale = 3
size = 1024 * scale
# Deep graphite field with a restrained blue illumination behind the mark.
image = Image.new('RGB', (size, size))
pixels = image.load()
for y in range(size):
    t = y / size
    base = (int(15 - 5*t), int(22 - 7*t), int(34 - 8*t))
    for x in range(size):
        dx, dy = (x/scale-520)/520, (y/scale-470)/520
        glow = max(0.0, 1.0-(dx*dx+dy*dy))**3 * 18
        pixels[x, y] = (min(255,base[0]), min(255,int(base[1]+glow*.35)), min(255,int(base[2]+glow)))

# A precise terminal frame and a bold T-shaped tool glyph, no text or tiny detail.
draw = ImageDraw.Draw(image)
blue = '#72A7FF'
white = '#F3F6FC'
muted = '#273B59'
def pts(seq): return [(int(x*scale), int(y*scale)) for x,y in seq]
def line(seq, fill, width): draw.line(pts(seq), fill=fill, width=width*scale, joint='curve')
def rounded(box, radius, outline, width):
    draw.rounded_rectangle(tuple(int(v*scale) for v in box), radius=radius*scale, outline=outline, width=width*scale)

# Open-corner terminal frame.
line([(300,340),(300,300),(390,300)], muted, 18)
line([(634,300),(724,300),(724,340)], muted, 18)
line([(300,684),(300,724),(390,724)], muted, 18)
line([(634,724),(724,724),(724,684)], muted, 18)
# Monogram: rounded top beam and a strong centered stem.
draw.rounded_rectangle((397*scale,382*scale,627*scale,450*scale), radius=24*scale, fill=blue)
draw.rounded_rectangle((478*scale,421*scale,546*scale,668*scale), radius=25*scale, fill=white)
# Small blue socket at the foot hints at a connected build toolchain.
draw.rounded_rectangle((451*scale,638*scale,573*scale,706*scale), radius=24*scale, fill=blue)

entries=[]
def save(idiom,points,factor):
    filename=f'{idiom}-{points}-{factor}.png'
    px=round(points*factor)
    image.resize((px,px),Image.Resampling.LANCZOS).save(folder/filename)
    entries.append(dict(idiom=idiom,size=f'{points}x{points}',scale=f'{factor}x',filename=filename))
for idiom,sizes,factors in [('iphone',[20,29,40,60],[2,3]),('ipad',[20,29,40,76],[1,2])]:
    for point in sizes:
        for factor in factors:
            save(idiom,point,factor)
save('ipad',83.5,2)
save('ios-marketing',1024,1)
(folder/'Contents.json').write_text(json.dumps(dict(images=entries,info=dict(author='xcode',version=1)),indent=2))
print(folder)
