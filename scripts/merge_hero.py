"""TW&CO V22 — one continuous hero, no independent roof overlay.
Uses only approved original pixels. Stdlib PNG processing (no new imagery).
"""
import sys,struct,zlib,binascii,re
from pathlib import Path
MAGIC=b'\x89PNG\r\n\x1a\n'
def decode(file):
 b=Path(file).read_bytes();assert b[:8]==MAGIC
 p=8;parts=[];head=None
 while p<len(b):
  n=int.from_bytes(b[p:p+4],'big');t=b[p+4:p+8];d=b[p+8:p+8+n];p+=12+n
  if t==b'IHDR':head=struct.unpack('>IIBBBBB',d)
  if t==b'IDAT':parts.append(d)
  if t==b'IEND':break
 w,h,depth,mode,_,_,interlace=head
 assert depth==8 and mode in (2,6) and interlace==0,head
 ch=4 if mode==6 else 3;stride=w*ch
 src=zlib.decompress(b''.join(parts));pos=0;previous=bytearray(stride);rows=[]
 for y in range(h):
  f=src[pos];pos+=1;encoded=src[pos:pos+stride];pos+=stride
  row=bytearray(stride)
  for i,v in enumerate(encoded):
   a=row[i-ch] if i>=ch else 0;up=previous[i];c=previous[i-ch] if i>=ch else 0
   if f==0:pred=0
   elif f==1:pred=a
   elif f==2:pred=up
   elif f==3:pred=(a+up)//2
   elif f==4:
    q=a+up-c;aa=abs(q-a);bb=abs(q-up);cc=abs(q-c)
    pred=a if aa<=bb and aa<=cc else up if bb<=cc else c
   else:raise ValueError('Invalid PNG filter')
   row[i]=(v+pred)&255
  rows.append(row);previous=row
 return w,h,ch,rows
def smooth(v):
 v=max(0.,min(1.,v));return v*v*(3-2*v)
def pngchunk(t,d):
 return len(d).to_bytes(4,'big')+t+d+(binascii.crc32(t+d)&0xffffffff).to_bytes(4,'big')
source,roof,clean,result=map(Path,sys.argv[1:])
w,h,n,original=decode(source)
rw,rh,rn,roofpixels=decode(roof)
cw,ch,cn,treated=decode(clean)
assert (w,h,n)==(rw,rh,3)==(cw,ch,cn) and rn==4
data=bytearray()
for y in range(h):
 row=bytearray(treated[y])
 if y<123:
  # Header dark outside of the photographic roof, exact roof pixels inside.
  roofrow=roofpixels[y]
  for x in range(w):
   i=x*3;k=x*4;alpha=roofrow[k+3]/255.
   for chn,background in enumerate((3,27,19)):
    row[i+chn]=round(background*(1-alpha)+original[y][i+chn]*alpha)
 elif y<157:
  # Undo V19 treatment on the actual roof immediately below the header.
  vertical=smooth((157-y)/14)
  for x in range(895,w):
   alpha=vertical*smooth((x-895)/145)
   if not alpha:continue
   i=x*3
   for chn in range(3):
    row[i+chn]=round(row[i+chn]*(1-alpha)+original[y][i+chn]*alpha)
 data.append(0);data.extend(row)
result.write_bytes(MAGIC+pngchunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+pngchunk(b'IDAT',zlib.compress(data,7))+pngchunk(b'IEND',b''))
# Remove the source of all future CSS seams: there must be ONE photo element.
index=result.parent.parent/'index.html'
html=index.read_text('utf-8')
assert 'assets/hero-clean-v19.png' in html
html=html.replace('assets/hero-clean-v19.png','assets/'+result.name)
html,count=re.subn(r'<img[^>]+class="roof-front"[^>]*>\s*','',html)
assert count==1,('Expected exactly one removed roof layer',count)
assert html.count('class="hero-scene"')==1
index.write_text(html,'utf-8')
print('SEAMLESS V22',w,h,result.stat().st_size,'bytes; single photographic hero')
