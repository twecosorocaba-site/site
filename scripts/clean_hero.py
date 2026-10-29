"""Build a clean photo-only hero from the approved original.
All UI (menu, titles, buttons) remains HTML, not baked into the image.
Python stdlib only; original building, vehicles and plates stay pixel-identical on the right.
"""
import sys, zlib, struct, binascii
from pathlib import Path
source=Path(sys.argv[1]);output=Path(sys.argv[2])
buf=source.read_bytes()
assert buf[:8]==b'\x89PNG\r\n\x1a\n'
chunks=[];pos=8
while pos<len(buf):
 length=struct.unpack('>I',buf[pos:pos+4])[0];typ=buf[pos+4:pos+8];dat=buf[pos+8:pos+8+length]
 chunks.append((typ,dat));pos+=12+length
 if typ==b'IEND':break
header=next(data for typ,data in chunks if typ==b'IHDR')
w,h,bitdepth,colortype,compression,filtermethod,interlace=struct.unpack('>IIBBBBB',header)
assert (bitdepth,colortype,interlace)==(8,2,0)
raw=zlib.decompress(b''.join(data for typ,data in chunks if typ==b'IDAT'))
stride=w*3;previous=bytearray(stride);ptr=0;dst=bytearray()
def smooth(v):
 if v<=0:return 0.0
 if v>=1:return 1.0
 return v*v*(3-2*v)
for y in range(h):
 f=raw[ptr];ptr+=1;enc=raw[ptr:ptr+stride];ptr+=stride
 row=bytearray(stride)
 for i,b in enumerate(enc):
  a=row[i-3] if i>=3 else 0
  up=previous[i]
  c=previous[i-3] if i>=3 else 0
  if f==0:v=b
  elif f==1:v=b+a
  elif f==2:v=b+up
  elif f==3:v=b+(a+up)//2
  elif f==4:
   p=a+up-c;pa=abs(p-a);pb=abs(p-up);pc=abs(p-c)
   pr=a if pa<=pb and pa<=pc else up if pb<=pc else c
   v=b+pr
  else:raise ValueError('Unsupported PNG filter')
  row[i]=v&255
 previous=row.copy()
 fy=smooth((y-123)/23)
 for x in range(w):
  alpha=smooth((x-653)/365)*fy
  if alpha>=1:continue
  i=x*3
  for channel,background in enumerate((2,22,15)):
   row[i+channel]=int(background*(1-alpha)+row[i+channel]*alpha)
 dst.append(0);dst.extend(row)
def chunk(typ,data):
 return struct.pack('>I',len(data))+typ+data+struct.pack('>I',binascii.crc32(typ+data)&0xffffffff)
output.parent.mkdir(parents=True,exist_ok=True)
output.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',header)+chunk(b'IDAT',zlib.compress(bytes(dst),level=7))+chunk(b'IEND',b''))
print('Hero clean:',w,h,output.stat().st_size)
html=output.parent.parent/'index.html'
s=html.read_text(encoding='utf-8')
assert 'assets/hero-referencia-exata.png' in s
html.write_text(s.replace('assets/hero-referencia-exata.png','assets/'+output.name),encoding='utf-8')
css=output.parent/'site.css'
with css.open('a',encoding='utf-8') as file:
 file.write('''
/* V19 single-photo hero: opaque navigation, no doubled raster UI. */
@media (min-width:861px) {
.hero-curtain {background:none!important;opacity:0!important;}
.hero-header-bg {background:#031b13!important;}
.hero-scene {filter:none!important;}
}
''')
