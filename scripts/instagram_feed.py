#!/usr/bin/env python3
"""TW&CO — last six verified Instagram posts, locally cached thumbnail covers.
First consult public profile; if Instagram rate-limits us, keep the verified
snapshot and reuse last published covers. No fabricated posts or stock photos.
"""
import datetime,html,json,re,ssl,urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
PUBLIC=ROOT/"public"
ASSETS=PUBLIC/"assets"
SNAP=json.loads((ROOT/"scripts/instagram-snapshot.json").read_text(encoding="utf-8"))
HANDLE="tw.co.premium"
PROFILE="https://www.instagram.com/tw.co.premium/"
HEADERS={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0 Safari/537.36", "x-ig-app-id":"936619743392459", "Referer":"https://www.instagram.com/"}
def request(url,timeout=15):
    req=urllib.request.Request(url,headers=HEADERS)
    with urllib.request.urlopen(req,timeout=timeout) as resp:
        return resp.read()
def valid(p):
    return re.fullmatch(r"[A-Za-z0-9_-]{6,18}",p.get("code","")) and p.get("permalink","").startswith(("https://www.instagram.com/p/","https://www.instagram.com/reel/"))
def live():
    data=json.loads(request("https://www.instagram.com/api/v1/users/web_profile_info/?username="+HANDLE,timeout=9))
    user=data["data"]["user"]
    assert user["username"]==HANDLE
    nodes=[e["node"] for e in user["edge_owner_to_timeline_media"]["edges"]]
    nodes.sort(key=lambda n:n.get("taken_at_timestamp",0), reverse=True)
    posts=[]
    for n in nodes:
        code=n.get("shortcode","")
        if not re.fullmatch(r"[A-Za-z0-9_-]{6,18}",code):continue
        kind=n.get("__typename","")
        captions=n.get("edge_media_to_caption",{}).get("edges",[])
        caption=captions[0]["node"].get("text","") if captions else ""
        posts.append({"code":code,"date":n.get("taken_at_timestamp",0),"type":kind,
           "caption":caption,"thumbnail_url":n.get("display_url",""),
           "permalink":"https://www.instagram.com/"+("reel" if kind=="GraphVideo" else "p")+"/"+code+"/"})
    if len(posts)<6: raise ValueError("Profile returned fewer than six posts")
    return posts[:6]
try:
    posts=live()
    source="Perfil público do Instagram"
except Exception as exc:
    print("Instagram unavailable, using verified snapshot:",type(exc).__name__)
    posts=SNAP["posts"][:6]
    source="Cópia verificada de 29/10/2026"
assert len(posts)==6 and len({p["code"] for p in posts})==6 and all(valid(p) for p in posts)
posts.sort(key=lambda p:p["date"],reverse=True)
ASSETS.joinpath("instagram").mkdir(parents=True,exist_ok=True)

# The previous public deploy is a safe last-resort cache if signed CDN URLs expire.
def cache_cover(post):
    target=ASSETS/"instagram"/(post["code"]+".jpg")
    options=[post.get("thumbnail_url",""),"https://site-site-71bd.vercel.app/assets/instagram/"+post["code"]+".jpg"]
    for option in options:
        if not option:continue
        try:
            b=request(option,timeout=16)
            if b[:3]==b"\xff\xd8\xff" and 4000<len(b)<4000000:
                target.write_bytes(b)
                return "assets/instagram/"+post["code"]+".jpg"
        except Exception as exc:print("Cover download blocked",post["code"],type(exc).__name__)
    return None

for p in posts:
    p["local_cover"]=cache_cover(p)

def caption_short(txt):
    txt=" ".join(txt.strip().split())
    if not txt:return "Confira esta publicação da TW&CO."
    end=txt.find(".")
    if 22<end<100:return txt[:end+1]
    return (txt[:92].rstrip()+"…") if len(txt)>92 else txt
def kind_name(kind):
    return {"GraphVideo":"Reel","GraphSidecar":"Carrossel","GraphImage":"Publicação"}.get(kind,"Publicação")
cards=[]
for i,p in enumerate(posts):
    title=caption_short(p.get("caption",""))
    date=datetime.datetime.fromtimestamp(p["date"],datetime.timezone.utc).strftime("%d/%m/%Y")
    cover=p["local_cover"]
    photo=(f'<img src="{html.escape(cover,quote=True)}" alt="{html.escape(title,quote=True)}" loading="lazy" decoding="async" width="480" height="600"/>' if cover else '<div class="ig-card-empty"><span>TW<span class="ig-amp">&</span>CO</span></div>')
    cards.append(f"""<a class="ig-card" href="{html.escape(p['permalink'],quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Abrir no Instagram: {html.escape(title,quote=True)}">
      <span class="ig-card-visual">{photo}<span class="ig-card-sheen"></span>
      <span class="ig-card-type">{kind_name(p['type'])}</span><span class="ig-card-open" aria-hidden="true">↗</span></span>
      <span class="ig-card-info"><span class="ig-card-date">{date} · @tw.co.premium</span><span class="ig-card-title">{html.escape(title)}</span></span>
    </a>""")

instagram=f"""<section class="instagram-section" id="instagram" aria-labelledby="instagram-heading">
 <div class="container">
   <div class="ig-heading">
     <div><span class="eyebrow">NOSSO INSTAGRAM</span><h2 id="instagram-heading">A oficina vista <span class="serif green">de perto.</span></h2><p>Nosso dia a dia, os bastidores e o cuidado que fazem parte de cada atendimento.</p></div>
     <div class="ig-heading-actions"><a class="ig-profile-link" href="{PROFILE}" target="_blank" rel="noopener noreferrer">Seguir @tw.co.premium <span aria-hidden="true">↗</span></a>
       <div class="ig-controls"><button type="button" id="igPrev" aria-label="Publicação anterior">←</button><span id="igPosition" aria-live="off">01 <span>/ 06</span></span><button type="button" id="igNext" aria-label="Próxima publicação">→</button></div>
     </div>
   </div>
   <div class="ig-carousel" id="igCarousel" tabindex="0" aria-label="Seis últimas publicações da TW&CO, role horizontalmente">
    {''.join(cards)}
   </div>
   <div class="ig-footnote"><span>Conteúdo original da TW&CO · Cada imagem abre sua publicação no Instagram.</span><a href="{PROFILE}" target="_blank" rel="noopener noreferrer">Ver perfil completo ↗</a></div>
 </div>
</section>"""

html_path=PUBLIC/"index.html"
page=html_path.read_text(encoding="utf-8")
anchor='<section class="location" id="contato">'
assert page.count(anchor)==1 and 'id="instagram"' not in page
page=page.replace(anchor,instagram+anchor)
page=page.replace('</head>','<link rel="stylesheet" href="assets/instagram-carousel.css"/></head>')
page=page.replace('</body>','<script defer src="assets/instagram-carousel.js"></script></body>')
html_path.write_text(page,encoding="utf-8")
(ASSETS/"instagram-posts.json").write_text(json.dumps({"handle":HANDLE,"source":source,"posts":[{k:p.get(k) for k in ("code","type","date","caption","permalink","local_cover")} for p in posts]},ensure_ascii=False,indent=2),encoding="utf-8")
print("INSTAGRAM READY",[(p["code"],p["local_cover"]) for p in posts])
