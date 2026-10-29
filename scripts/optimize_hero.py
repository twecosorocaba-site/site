#!/usr/bin/env python3
"""TW&CO hero: high-fidelity WebP optimization, from the approved PNG.
This only changes encoding, not framing, layer geometry or content.
Keeps source original in repository ZIP; updates all generated references.
"""
from pathlib import Path
from PIL import Image,ImageChops,ImageStat

root=Path('public')
source=root/'assets/hero-seamless-v22.png'
out=root/'assets/hero-seamless-v22.webp'
assert source.exists()
img=Image.open(source).convert('RGB')
img.save(out,format='WEBP',quality=95,method=6)
check=Image.open(out).convert('RGB')
assert check.size==img.size
diff=ImageStat.Stat(ImageChops.difference(img,check)).mean
assert max(diff)<2.5,('Image differences too great',diff)
assert out.stat().st_size < source.stat().st_size*0.6,'Image reduction too small'
old='hero-seamless-v22.png'
new='hero-seamless-v22.webp'
for ext in ('*.html','*.xml','*.txt','*.md','*.json'):
 for p in root.rglob(ext):
  text=p.read_text(encoding='utf-8')
  if old in text:
   p.write_text(text.replace(old,new),encoding='utf-8')
print('HERO OPTIMIZED: original',source.stat().st_size,'webp',out.stat().st_size,
      'saved',round(100*(1-out.stat().st_size/source.stat().st_size),1),'%',
      'mean absolute RGB error',*[round(v,3) for v in diff])
