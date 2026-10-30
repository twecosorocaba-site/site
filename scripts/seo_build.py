#!/usr/bin/env python3
"""TW&CO Premium: build-time technical SEO, helpful local pages, and AI-readable summaries.
Only business facts confirmed in the current website are asserted.
Does not create fake reviews, awards, credentials, service hours or geographic offices.
"""
from __future__ import annotations
import datetime,html,json,os,re,shutil
from pathlib import Path
from urllib.parse import quote
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'public'
ASSET=OUT/'assets'
BASE=os.environ.get('TWCO_SITE_URL','https://www.tweco.com.br').rstrip('/')
assert BASE.startswith('https://') and not BASE.endswith('/preview')
DATE='2026-10-30'
PHONE='+55 15 99663-8821'
WHATSAPP='5515996638821'
ADDR='Rua Júlio Ribeiro, 876'
CITY='Vila Santana, Sorocaba, SP'
BUSINESS='TW&CO Premium'
MAP='https://maps.app.goo.gl/KH8BSwpBCeTkNb8z7'
IG='https://www.instagram.com/tw.co.premium/'
LOGO='assets/logo-twco.svg'
HERO='assets/hero-seamless-v22.png'
OG='assets/banner-oficina-aprovado.webp'
LINKS=[
 ('/', 'Início'),
 ('/servicos/', 'Serviços'),
 ('/oficina-mecanica-sorocaba/', 'Oficina em Sorocaba'),
 ('/sobre/', 'A oficina'),
 ('/contato/', 'Contato')
]
SERVICES=[
 {
 'slug':'mecanica-especializada','label':'Mecânica especializada','photo':'assets/servico-mecanica.webp',
 'description':'Manutenção preventiva e corretiva em Sorocaba, com avaliação individual de cada veículo e orientação técnica clara.',
 'intro':'Cuidar de um veículo vai além de substituir uma peça: começa por compreender o uso, o histórico e o sintoma relatado. Na TW&CO Premium, a manutenção é conduzida com atenção a esses detalhes e comunicação direta com o cliente.',
 'points':[
 ('O que avaliar antes de começar','Identificar o motivo da visita, conversar sobre o comportamento do veículo e verificar o histórico disponível ajudam a definir o próximo passo de maneira mais consciente.'),
 ('Manutenção preventiva','A revisão periódica busca identificar desgaste, vazamentos e condições de funcionamento antes de uma falha mais séria. Os itens avaliados dependem do modelo e das recomendações do fabricante.'),
 ('Manutenção corretiva','Quando há um defeito ou sintoma específico, o ideal é confirmar sua origem antes de escolher um reparo; trocar peças por tentativa pode aumentar custos sem resolver a causa.')],
 'faqs':[('Quando devo levar meu carro para avaliação?','Consulte o plano de manutenção do fabricante e procure uma avaliação quando perceber ruídos, vazamentos, falhas ou mudanças no comportamento do veículo.'),
 ('Vocês atendem carros de diferentes marcas?','A TW&CO apresenta serviços mecânicos para veículos premium e multimarcas. A equipe pode confirmar a disponibilidade para seu modelo pelo WhatsApp.')],
 'search':'mecânica especializada manutenção preventiva corretiva Sorocaba'
 },
 {
 'slug':'suspensao-e-freios','label':'Suspensão e freios','photo':'assets/servico-freios.webp',
 'description':'Avaliação de suspensão e freios em Sorocaba, incluindo ruídos, vibrações, estabilidade e componentes de segurança.',
 'intro':'A suspensão influencia estabilidade, conforto e contato dos pneus com a pista. Já o sistema de freios é fundamental para a segurança. Ruídos, trepidações e alterações na resposta do pedal são motivos para procurar orientação técnica.',
 'points':[
 ('Suspensão e direção','Folgas, desgaste de buchas, amortecedores e outros componentes podem provocar ruídos ou mudanças na dirigibilidade. Somente uma inspeção ajuda a identificar a origem.'),
 ('Sistema de freios','Pastilhas, discos, fluido e componentes hidráulicos precisam ser avaliados conforme o projeto e o estado de cada veículo.'),
 ('Quando procurar ajuda','Barulho ao passar em lombadas, vibração ao frear e alteração no pedal merecem atenção. Em caso de suspeita de falha no freio, não continue dirigindo; procure assistência segura.')],
 'faqs':[('Barulho na suspensão significa amortecedor ruim?','Não necessariamente. O ruído pode ter causas diferentes e precisa de avaliação presencial.'),
 ('Posso dirigir com o pedal de freio alterado?','Se houver perda de eficiência ou comportamento anormal na frenagem, a recomendação é parar em segurança e solicitar assistência profissional.')],
 'search':'suspensão freios amortecedores pastilhas revisão Sorocaba'
 },
 {
 'slug':'diagnostico-automotivo','label':'Diagnóstico automotivo','photo':'assets/servico-diagnostico.webp',
 'description':'Diagnóstico e avaliação de sintomas mecânicos e eletrônicos em Sorocaba, com análise técnica antes de indicar reparos.',
 'intro':'Uma luz acesa no painel, dificuldade na partida ou alteração no funcionamento do motor pode ter mais de uma explicação. O objetivo de uma avaliação responsável é levantar evidências para encontrar a causa do problema, sem depender de suposições.',
 'points':[
 ('Entendimento do sintoma','O que aconteceu, quando começou e em quais condições a falha aparece são informações importantes para a investigação.'),
 ('Verificações técnicas','Inspeções e testes adequados ao veículo podem ajudar a isolar a causa. A ferramenta sozinha não substitui uma análise profissional.'),
 ('Orientação transparente','Depois da avaliação, o cliente deve entender o que foi identificado, quais são as alternativas possíveis e o que exige prioridade.')],
 'faqs':[('Toda luz no painel indica problema grave?','Não. O significado depende do símbolo, do modelo e do comportamento do veículo. Alertas críticos exigem que se siga imediatamente a orientação do manual.'),
 ('Um scanner identifica sozinho o defeito?','Códigos de falha são pistas, não diagnósticos definitivos. A confirmação pode exigir verificações adicionais.')],
 'search':'diagnóstico scanner avaliação automotiva Sorocaba'
 },
 {
 'slug':'cambio-e-fluidos','label':'Câmbio e fluidos','photo':'assets/servico-cambio.webp',
 'description':'Avaliação de câmbio e fluidos automotivos em Sorocaba, com atenção à especificação correta e às recomendações de manutenção.',
 'intro':'O funcionamento da transmissão e de outros sistemas depende de fluidos com a especificação apropriada. A necessidade de substituição, o método e o intervalo variam conforme o veículo, sua utilização e as recomendações do fabricante.',
 'points':[
 ('Câmbio automático','Trancos, demora nas trocas ou comportamento irregular são sinais que justificam uma avaliação antes de qualquer intervenção.'),
 ('Fluidos e especificações','Usar um produto inadequado pode causar problemas. Tipo, quantidade, procedimento e periodicidade devem respeitar o projeto do veículo.'),
 ('Equipamentos e procedimento','A oficina possui equipamento Fluid 500 ATF registrado em suas fotografias. A aplicação de procedimentos específicos deve ser confirmada pela equipe para cada modelo.')],
 'faqs':[('Todo carro precisa trocar fluido de câmbio na mesma quilometragem?','Não. O intervalo e o procedimento dependem do modelo, das condições de uso e das recomendações do fabricante.'),
 ('Trancos na troca de marcha indicam só falta de fluido?','Não. Esse sintoma pode ter causas diferentes; uma avaliação é necessária antes de recomendar manutenção.')],
 'search':'câmbio automático troca de fluido transmissão Sorocaba'
 }
]
GUIDES=[
 {'slug':'quando-procurar-diagnostico','title':'Quando procurar um diagnóstico automotivo?',
 'description':'Entenda quais sinais do veículo merecem uma avaliação técnica e por que diagnosticar antes de trocar peças.',
 'intro':'Quando o carro muda de comportamento, é tentador tentar adivinhar a peça responsável. Mas um mesmo sintoma pode ter causas diferentes, e uma boa investigação costuma começar pela observação e pelo histórico do veículo.',
 'sections':[
 ('Sinais que merecem atenção','Falhas na partida, perda incomum de desempenho, ruídos persistentes, vibrações e luzes no painel são motivos para consultar o manual e procurar orientação técnica.'),
 ('Descrever bem o problema ajuda','Anote em quais situações o sintoma aparece, quando começou, se ocorre com motor frio ou quente e se houve alguma manutenção recente. Essas informações podem direcionar a avaliação.'),
 ('O que não fazer','Evite substituir componentes apenas por tentativa. Em alertas graves, superaquecimento ou suspeita de falha nos freios, estacione em local seguro e solicite assistência adequada.'),
 ('Como buscar atendimento em Sorocaba','Na TW&CO Premium, você pode relatar o sintoma pelo site e encaminhá-lo à equipe via WhatsApp para combinar uma avaliação presencial.')],
 'image':'assets/servico-diagnostico.webp'},
 {'slug':'revisao-preventiva','title':'Revisão preventiva: quais cuidados observar?',
 'description':'Checklist orientativo para conversar sobre manutenção preventiva: fluidos, freios, pneus, sinais de desgaste e manual do veículo.',
 'intro':'A revisão preventiva não é uma lista igual para todos os carros. O manual, a quilometragem, o tempo de uso e o ambiente em que o veículo circula influenciam a avaliação.',
 'sections':[
 ('Fluidos e vazamentos','Mudanças de nível, manchas no chão e sinais de vazamento merecem inspeção. A escolha do fluido deve seguir a especificação do fabricante.'),
 ('Freios e pneus','Avaliar desgaste, pressão dos pneus e alterações de comportamento durante a frenagem ajuda a identificar riscos antes que o problema aumente.'),
 ('Suspensão e direção','Barulhos em irregularidades, vibrações e mudanças na estabilidade são bons motivos para uma verificação técnica.'),
 ('Documente o histórico','Manter notas e registros de manutenção ajuda a equipe a compreender o que já foi feito e planejar as próximas revisões.'),
 ('Converse com a oficina','Compartilhe o histórico disponível e as dúvidas com a TW&CO Premium para avaliar os cuidados adequados ao seu veículo.')],
 'image':'assets/servico-mecanica.webp'}
]
URLS=[]
def absolute(path):return BASE+path
def asseturl(path):return BASE+'/'+path.lstrip('/')
def escape(s):return html.escape(str(s),quote=True)
def json_script(obj):return '<script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+'</script>'
ORGID=absolute('/#empresa')
BASE_BUS={
 '@type':'AutoRepair','@id':ORGID,'name':'TW&CO Premium',
 'alternateName':'TW&CO Serviço Mecânico Especializado Premium',
 'url':absolute('/'),'logo':asseturl(LOGO),'image':[asseturl(OG),asseturl(HERO)],
 'telephone':PHONE,
 'address':{'@type':'PostalAddress','streetAddress':ADDR,'addressLocality':'Sorocaba','addressRegion':'SP','postalCode':None,'addressCountry':'BR'},
 'hasMap':MAP,'sameAs':[IG,MAP],
 'description':'Oficina mecânica especializada em manutenção e avaliação automotiva, localizada na Vila Santana, em Sorocaba (SP).'
}
BASE_BUS['address'].pop('postalCode')
BUS_SCHEMA={'@context':'https://schema.org','@graph':[BASE_BUS,{'@type':'WebSite','@id':absolute('/#website'),'name':BUSINESS,'url':absolute('/'),'inLanguage':'pt-BR','publisher':{'@id':ORGID}}]}
def breadcrumbs(items):
 return {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':absolute(path)} for i,(name,path) in enumerate(items)]}
def webpage_schema(path,title,desc,extra=None):
 graph=[{'@type':'WebPage','@id':absolute(path)+'#webpage','url':absolute(path),'name':title,'description':desc,'inLanguage':'pt-BR','isPartOf':{'@id':absolute('/#website')},'about':{'@id':ORGID}},breadcrumbs([('Início','/')]+([] if path=='/' else [(title,path)]))]
 if extra:graph.extend(extra)
 return {'@context':'https://schema.org','@graph':graph}
def nav(active=''):
 links=''.join(f'<a href="{absolute(p)}"'+(' aria-current="page"' if p==active else '')+f'>{escape(label)}</a>' for p,label in LINKS)
 return f'<header class="inner-header"><div class="inner-wrap"><a class="inner-brand" href="{BASE}/"><img src="/{LOGO}" width="175" height="59" alt="TW&CO Premium"/></a><nav aria-label="Navegação principal">{links}</nav><a class="small-cta" href="{wa_link("Olá! Gostaria de conversar com a TW&CO Premium.")}" target="_blank" rel="noopener noreferrer">Falar com a equipe ↗</a></div></header>'
def wa_link(text):
 return 'https://wa.me/'+WHATSAPP+'?text='+quote(text)
def inner_head(title,desc,path,photo=None):
 canonical=absolute(path);og=asseturl(photo or OG)
 return f'''<!DOCTYPE html><html lang="pt-BR"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="robots" content="index,follow,max-image-preview:large"/><meta name="theme-color" content="#041a12"/>
<title>{escape(title)}</title><meta name="description" content="{escape(desc)}"/>
<link rel="canonical" href="{escape(canonical)}"/><link rel="alternate" hreflang="pt-BR" href="{escape(canonical)}"/>
<meta property="og:type" content="website"/><meta property="og:locale" content="pt_BR"/>
<meta property="og:site_name" content="{BUSINESS}"/><meta property="og:title" content="{escape(title)}"/>
<meta property="og:description" content="{escape(desc)}"/><meta property="og:url" content="{escape(canonical)}"/>
<meta property="og:image" content="{escape(og)}"/><meta name="twitter:card" content="summary_large_image"/>
<link rel="icon" type="image/svg+xml" href="/favicon.svg"/><link rel="manifest" href="/site.webmanifest"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link rel="stylesheet" href="/assets/seo-pages.css"/>
<link rel="stylesheet" href="/assets/mobile-polish.css" media="(max-width: 860px)"/>
'''
def foot():
 services=''.join(f'<a href="{BASE}/servicos/{d["slug"]}/">{escape(d["label"])}</a>' for d in SERVICES)
 return f'''<footer class="inner-footer"><div class="inner-wrap footer-grid"><div><a href="{BASE}/"><img src="/{LOGO}" alt="TW&CO Premium" width="160" height="53"/></a><p>Serviço mecânico especializado com atendimento na Vila Santana, Sorocaba.</p><small>© 2026 TW&CO Premium.</small></div><div><strong>Serviços</strong>{services}</div><div><strong>Contato</strong><a href="{absolute('/contato/')}">{ADDR} — {CITY}</a><a href="{wa_link('Olá! Vim pelo site da TW&CO.')}" target="_blank" rel="noopener noreferrer">{PHONE}</a><a href="{IG}" target="_blank" rel="noopener noreferrer">Instagram</a><a href="{MAP}" target="_blank" rel="noopener noreferrer">Ver no Google Maps ↗</a></div></div></footer>'''
def crumbs(items):
 return '<nav aria-label="Navegação estrutural" class="crumbs">'+ ' / '.join(f'<a href="{absolute(p)}">{escape(n)}</a>' if i<len(items)-1 else '<span aria-current="page">'+escape(n)+'</span>' for i,(n,p) in enumerate(items))+'</nav>'
def cta(subject):
 return f'<div class="inner-cta"><div><span class="eyebrow">ATENDIMENTO PERSONALIZADO</span><h2>Seu carro merece <em>atenção de verdade.</em></h2><p>Conte o que está acontecendo. Nossa equipe pode orientar o próximo passo e combinar uma avaliação presencial.</p></div><a class="primary-btn" target="_blank" rel="noopener noreferrer" href="{wa_link("Olá! Gostaria de saber mais sobre "+subject+" na TW&CO Premium, em Sorocaba.")}">Conversar pelo WhatsApp ↗</a></div>'
def write_page(path,title,desc,body,photo=None,extra=None,crumbslist=None):
 output=OUT/path.strip('/')
 output.mkdir(parents=True,exist_ok=True)
 intro=inner_head(title,desc,path,photo)
 schema=webpage_schema(path,title,desc,extra)
 doc=intro+json_script(schema)+'</head><body><a class="skip" href="#conteudo">Pular ao conteúdo</a>'+nav(path)
 doc+='<main id="conteudo"><div class="inner-wrap">'+crumbs(crumbslist or [('Início','/'),(title,path)])+body+'</div></main>'+foot()+'</body></html>'
 (output/'index.html').write_text(doc,encoding='utf-8')
 URLS.append({'path':path,'image':photo or OG,'modified':DATE})
def service_card(s):
 url='/servicos/'+s['slug']+'/'
 return f'''<a class="inner-service-card" href="{absolute(url)}"><img loading="lazy" decoding="async" src="/{s['photo']}" width="640" height="390" alt="{escape(s['label'])} na TW&CO Premium"/><span class="inner-service-info"><strong>{escape(s['label'])}</strong><span>{escape(s['description'])}</span><b>Conheça o serviço ↗</b></span></a>'''
def render_service(s):
 path='/servicos/'+s['slug']+'/'
 title=f'{s["label"]} em Sorocaba | TW&CO Premium'
 desc=s['description']
 points=''.join(f'<article class="explain-card"><span class="tiny">{str(i).zfill(2)} / CUIDADO TÉCNICO</span><h3>{escape(h)}</h3><p>{escape(txt)}</p></article>' for i,(h,txt) in enumerate(s['points'],1))
 questions=''.join(f'<details class="qa"><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q,a in s['faqs'])
 related=''.join(service_card(other) for other in SERVICES if other['slug']!=s['slug'])
 body=f'''<section class="inner-hero"><div><span class="eyebrow">TW&CO PREMIUM · SOROCABA</span><h1>{escape(s['label'])}<br/><em>com precisão.</em></h1><p>{escape(s['intro'])}</p><a class="primary-btn" href="{wa_link("Olá! Quero solicitar uma avaliação de "+s["label"]+" na TW&CO Premium.")}" target="_blank" rel="noopener noreferrer">Solicitar avaliação ↗</a></div><figure><img src="/{s['photo']}" width="640" height="390" fetchpriority="high" alt="{escape(s['label'])}: ambiente da oficina TW&CO Premium em Sorocaba"/><figcaption>Fotografia da TW&CO Premium, em Sorocaba.</figcaption></figure></section>
 <section class="inner-section"><div class="section-label">NOSSA ABORDAGEM</div><h2>O cuidado começa <em>nos detalhes.</em></h2><div class="explain-grid">{points}</div></section>
 <section class="inner-section qa-section"><div><span class="section-label">DÚVIDAS FREQUENTES</span><h2>Entenda antes de <em>decidir.</em></h2></div><div>{questions}</div></section>
 {cta(s['label'])}
 <section class="inner-section"><span class="section-label">OUTROS SERVIÇOS</span><h2>Também cuidamos <em>destes detalhes.</em></h2><div class="inner-services-grid">{related}</div></section>'''
 service={'@type':'Service','@id':absolute(path)+'#service','name':s['label'],'serviceType':s['label'],'areaServed':{'@type':'City','name':'Sorocaba'},'provider':{'@id':ORGID},'url':absolute(path),'description':desc}
 write_page(path,title,desc,body,s['photo'],[service], [('Início','/'),('Serviços','/servicos/'),(s['label'],path)])
 # Static FAQ is helpful for visitors, without unsupported rich-result claims.
# Home page, with stable image/roof structure left unchanged.
home=OUT/'index.html'
page=home.read_text('utf-8')
page=re.sub(r'<meta content="[^"]+" name="description"/>','<meta name="description" content="Oficina mecânica especializada na Vila Santana, Sorocaba. Manutenção, suspensão, freios, diagnóstico e câmbio. Conheça a TW&CO Premium."/>',page,count=1)
page=re.sub(r'<meta content="website" property="og:type"/>.*?<meta content="[^"]*" property="og:description"/>','',page,count=1,flags=re.S)
page=re.sub(r'<script type="application/ld\+json">.*?</script>','',page,count=1,flags=re.S)
page=page.replace('</head>',f'''<link rel="canonical" href="{BASE}/"/>
<link rel="alternate" hreflang="pt-BR" href="{BASE}/"/>
<link rel="icon" type="image/svg+xml" href="/favicon.svg"/>
<link rel="manifest" href="/site.webmanifest"/>
<meta name="robots" content="index,follow,max-image-preview:large"/>
<meta property="og:locale" content="pt_BR"/><meta property="og:type" content="website"/>
<meta property="og:site_name" content="TW&CO Premium"/>
<meta property="og:title" content="TW&CO Premium — Oficina Mecânica Especializada em Sorocaba"/>
<meta property="og:description" content="Cuidado, precisão e atendimento especializado para seu veículo em Sorocaba."/>
<meta property="og:url" content="{BASE}/"/><meta property="og:image" content="{asseturl(OG)}"/>
<meta name="twitter:card" content="summary_large_image"/>
<link rel="preload" as="image" fetchpriority="high" href="/assets/hero-seamless-v22.png" media="(min-width: 861px)"/>
{json_script(BUS_SCHEMA)}
<style>.home-discovery{{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:12px;padding:27px 0 0;font-size:11px;color:#9dbeaa}}.home-discovery a{{display:inline-flex;border:1px solid #22624175;border-radius:30px;padding:8px 13px;color:#b1e0c2;white-space:nowrap}}.home-discovery a:hover{{color:#00e477;border-color:#00e477}}@media(max-width:760px){{.home-discovery{{gap:9px;padding-top:19px}}}}</style>
</head>''',1)
# Remove redundant original hero preloads (new preloads added with priority).
page=re.sub(r'<link as="image" href="assets/hero-seamless-v22\.png" media="\(min-width: 861px\)" rel="preload"/>','',page)
# Keep mobile preload: LCP optimization on mobile.
# Preserve existing logo and the approved media; change only destinations of the 4 service cards.
for s in SERVICES:
 # Home cards sequence: mechanics, suspension, diagnostic, gear.
 pass
destinations=[SERVICES[0],SERVICES[1],SERVICES[2],SERVICES[3]]
counter=[0]
def replace_service_anchor(m):
 i=counter[0];counter[0]+=1
 if i>=4:return m.group(0)
 return '<a class="service-card" href="'+absolute('/servicos/'+destinations[i]['slug']+'/')+'" aria-label="Saiba mais sobre '+escape(destinations[i]['label'])+'">'
page,num=re.subn(r'<a class="service-card"[^>]*>',replace_service_anchor,page)
assert counter[0]==4,('Unexpected number of service cards',counter[0])
# Add a small internal discovery path below existing service grid; no hero redesign.
anchor='<section class="attention"'
assert anchor in page
section_end=page.rfind('</section>',0,page.index(anchor))
seo_nav=f'<nav aria-label="Mais informações da TW&CO" class="home-discovery"><span>Conheça nossos serviços em Sorocaba:</span> '+''.join(f'<a href="{absolute("/servicos/"+s["slug"]+"/")}">{escape(s["label"])} ↗</a>' for s in SERVICES)+'</nav>'
page=page[:section_end]+seo_nav+page[section_end:]
page=page.replace('</head>','<link rel="stylesheet" href="/assets/mobile-polish.css" media="(max-width: 860px)"/></head>',1)
home.write_text(page,encoding='utf-8')
URLS.append({'path':'/','image':HERO,'modified':DATE})
# Hub
cards=''.join(service_card(s) for s in SERVICES)
write_page('/servicos/','Serviços mecânicos em Sorocaba | TW&CO Premium',
 'Conheça os serviços da TW&CO Premium em Sorocaba: mecânica especializada, suspensão, freios, diagnóstico, câmbio e fluidos.',
 f'<section class="simple-hero"><span class="eyebrow">O QUE FAZEMOS</span><h1>Especialização para <em>cada detalhe.</em></h1><p>Conheça nossas áreas de atendimento. Para saber o procedimento indicado para seu veículo, converse com a equipe.</p></section><section class="inner-section"><div class="inner-services-grid">{cards}</div></section>{cta("os serviços mecânicos")}',
 OG)
for s in SERVICES:render_service(s)
# About — only confirmed business details.
write_page('/sobre/','Conheça a TW&CO Premium em Sorocaba | A oficina',
 'Conheça a estrutura da TW&CO Premium, sua recepção e o ambiente de trabalho na Vila Santana, em Sorocaba.',
 f'<section class="inner-hero"><div><span class="eyebrow">CONHEÇA A OFICINA</span><h1>Mais do que um serviço, <em>atenção de verdade.</em></h1><p>A TW&CO Premium recebe veículos em sua oficina na Vila Santana, Sorocaba, e valoriza comunicação transparente com o cliente e cuidado com cada detalhe.</p><a class="primary-btn" href="{wa_link("Olá! Gostaria de conhecer a TW&CO Premium.")}" target="_blank" rel="noopener noreferrer">Fale com a equipe ↗</a></div><figure><img src="/assets/atendimento-wide.webp" width="640" height="390" fetchpriority="high" alt="Recepção e atendimento na oficina TW&CO Premium"/><figcaption>Ambiente real da TW&CO Premium.</figcaption></figure></section><section class="inner-section"><span class="section-label">ESTRUTURA</span><h2>Um ambiente pensado para <em>cuidar.</em></h2><div class="explain-grid"><article class="explain-card"><h3>Atendimento próximo</h3><p>Da chegada à orientação sobre o serviço, a conversa com o cliente faz parte do cuidado com o veículo.</p></article><article class="explain-card"><h3>Equipamentos e área de serviço</h3><p>A oficina possui elevadores automotivos e equipamentos fotografados em seu espaço físico, utilizados conforme a necessidade de cada trabalho.</p></article><article class="explain-card"><h3>Serviços especializados</h3><p>Mecânica, diagnóstico, suspensão, freios, câmbio e fluidos compõem as principais áreas apresentadas pela empresa.</p></article></div></section>{cta("a oficina")}',
 'assets/atendimento-wide.webp')
# Location landing: text unique from hub
write_page('/oficina-mecanica-sorocaba/','Oficina mecânica na Vila Santana, Sorocaba | TW&CO',
 'Procura uma oficina mecânica em Sorocaba? Conheça a TW&CO Premium na Rua Júlio Ribeiro, 876, Vila Santana.',
 f'<section class="inner-hero"><div><span class="eyebrow">VILA SANTANA · SOROCABA</span><h1>Sua oficina mecânica <em>em Sorocaba.</em></h1><p>Na Rua Júlio Ribeiro, 876, a TW&CO Premium reúne atendimento para veículos premium e multimarcas. Estamos na Vila Santana e recebemos dúvidas sobre revisão, ruídos, freios, suspensão, diagnóstico e câmbio.</p><a href="{MAP}" target="_blank" rel="noopener noreferrer" class="primary-btn">Como chegar ↗</a></div><figure><img src="/{HERO}" fetchpriority="high" width="1672" height="941" alt="Fachada da TW&CO Premium em Sorocaba com dois veículos em frente à oficina"/><figcaption>Fachada da oficina na Vila Santana, Sorocaba.</figcaption></figure></section><section class="inner-section"><span class="section-label">NA OFICINA</span><h2>Serviços e <em>orientação técnica.</em></h2><div class="inner-services-grid">{cards}</div></section><section class="inner-section"><span class="section-label">LOCALIZAÇÃO</span><h2>Onde nos <em>encontrar.</em></h2><p>{ADDR} — {CITY}. Para confirmar o atendimento do seu modelo e verificar a disponibilidade, fale com a equipe antes de visitar.</p><p><a class="text-link" href="{MAP}" target="_blank" rel="noopener noreferrer">Abrir localização no Google Maps ↗</a></p></section>{cta("atendimento em Sorocaba")}',
 HERO)
write_page('/contato/','Contato e localização | TW&CO Premium Sorocaba',
 'Fale com a TW&CO Premium pelo WhatsApp, veja o endereço Rua Júlio Ribeiro, 876, Vila Santana, Sorocaba, e encontre a oficina no Google Maps.',
 f'<section class="simple-hero"><span class="eyebrow">FALE COM A TW&CO</span><h1>Vamos conversar sobre <em>o seu veículo?</em></h1><p>Envie uma mensagem para a equipe, compartilhe sua dúvida e combine uma avaliação. Atendimento presencial na Vila Santana, Sorocaba.</p></section><section class="inner-section"><div class="contact-boxes"><article><span class="section-label">WHATSAPP</span><h2>{PHONE}</h2><a class="text-link" href="{wa_link("Olá! Gostaria de agendar uma avaliação na TW&CO Premium.")}" target="_blank" rel="noopener noreferrer">Iniciar conversa ↗</a></article><article><span class="section-label">ENDEREÇO</span><h2>{ADDR}</h2><p>{CITY}</p><a class="text-link" href="{MAP}" target="_blank" rel="noopener noreferrer">Abrir rota no Google Maps ↗</a></article><article><span class="section-label">INSTAGRAM</span><h2>@tw.co.premium</h2><a class="text-link" href="{IG}" target="_blank" rel="noopener noreferrer">Ver publicações ↗</a></article></div></section><section class="inner-section"><span class="section-label">VISITA PRESENCIAL</span><h2>Orientação antes de <em>trazer o carro.</em></h2><p>Para que a equipe possa indicar o melhor próximo passo, informe o modelo do veículo e o que está acontecendo. Os horários e a disponibilidade podem ser confirmados diretamente com o atendimento.</p></section>',
 OG)
# Educational content with clear safety qualifications.
write_page('/guia/','Guia de cuidados automotivos | TW&CO Premium',
 'Conteúdos educativos sobre diagnóstico automotivo e cuidados de revisão preventiva para motoristas em Sorocaba.',
 '<section class="simple-hero"><span class="eyebrow">INFORMAÇÃO QUE AJUDA</span><h1>Cuidar bem começa <em>por entender.</em></h1><p>Informações gerais para você conversar melhor com sua oficina. As orientações não substituem inspeção presencial nem o manual do fabricante.</p></section><section class="inner-section"><div class="inner-services-grid">'+''.join(f'<a class="inner-service-card" href="{BASE}/guia/{g["slug"]}/"><img src="/{g["image"]}" width="640" height="390" loading="lazy" alt="{escape(g["title"])}"/><span class="inner-service-info"><strong>{escape(g["title"])}</strong><span>{escape(g["description"])}</span><b>Ler guia ↗</b></span></a>' for g in GUIDES)+'</div></section>',
 OG)
for g in GUIDES:
 path='/guia/'+g['slug']+'/'
 secs=''.join(f'<article class="guide-block"><h2>{escape(heading)}</h2><p>{escape(copy)}</p></article>' for heading,copy in g['sections'])
 body=f'<section class="inner-hero"><div><span class="eyebrow">GUIA DE CUIDADOS AUTOMOTIVOS</span><h1>{escape(g["title"])}</h1><p>{escape(g["intro"])}</p><p class="caution">Informação educativa, não substitui diagnóstico ou orientações do fabricante.</p></div><figure><img src="/{g["image"]}" width="640" height="390" fetchpriority="high" alt="{escape(g["title"])} — oficina TW&CO"/><figcaption>Imagem da oficina TW&CO Premium.</figcaption></figure></section><section class="inner-section guide-content">{secs}</section>{cta(g["title"])}'
 article={'@type':'Article','headline':g['title'],'description':g['description'],'datePublished':DATE,'dateModified':DATE,'inLanguage':'pt-BR','image':asseturl(g['image']),'author':{'@id':ORGID},'publisher':{'@id':ORGID},'mainEntityOfPage':absolute(path)}
 write_page(path,g['title']+' | TW&CO Premium Sorocaba',g['description'],body,g['image'],[article],[('Início','/'),('Guias','/guia/'),(g['title'],path)])
# Machine-readable aids. llms.txt is optional; Google Search itself does not use it for ranking.
(OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n',encoding='utf-8')
(OUT/'llms.txt').write_text(f'''# TW&CO Premium — Serviço Mecânico Especializado

> Oficina mecânica presencial em Sorocaba, São Paulo, com atuação em manutenção, suspensão, freios, diagnóstico e câmbio/fluidos. Dados obtidos do site oficial, sem alegações de certificações ou horários não confirmados.

- Site: {BASE}/
- Endereço: {ADDR} — {CITY}, Brasil
- WhatsApp / telefone: {PHONE}
- Instagram: {IG}
- Localização: {MAP}

## Páginas principais
''' + '\n'.join(f'- [{s["label"]}]({absolute("/servicos/"+s["slug"]+"/")})' for s in SERVICES) +
 f'''\n- [Oficina em Sorocaba]({absolute('/oficina-mecanica-sorocaba/')})
- [Sobre a oficina]({absolute('/sobre/')})
- [Contato]({absolute('/contato/')})
- [Guia automotivo]({absolute('/guia/')})

## Nota
Os serviços precisam de avaliação da equipe para confirmação de aplicação a cada veículo. Este arquivo é um resumo opcional para sistemas que o suportem, não uma diretiva do Google Search.
''',encoding='utf-8')
(OUT/'llms-full.txt').write_text(
 (OUT/'llms.txt').read_text(encoding='utf-8')+
 '\n## Detalhamento dos serviços\n'+
 '\n\n'.join('### '+s['label']+'\n'+s['intro']+'\n'+'\n'.join('- '+h+': '+copy for h,copy in s['points']) for s in SERVICES)+
 '\n\n## Conteúdo educativo\n'+'\n\n'.join('### '+g['title']+'\n'+g['intro'] for g in GUIDES),
 encoding='utf-8')
ai=OUT/'ai'
ai.mkdir(exist_ok=True)
(ai/'empresa.md').write_text(f'# TW&CO Premium\nOficina mecânica em {ADDR}, {CITY}. Telefone {PHONE}. Site {BASE}/. Atendimento mediante confirmação com a equipe.\n',encoding='utf-8')
(ai/'servicos.md').write_text('# Serviços da TW&CO Premium\n\n'+'\n'.join(f'- [{s["label"]}]({absolute("/servicos/"+s["slug"]+"/")}): {s["description"]}' for s in SERVICES)+'\n',encoding='utf-8')
(ai/'perguntas-frequentes.md').write_text('# Perguntas frequentes\n\n'+'\n\n'.join(f'## {q}\n{a}' for s in SERVICES for q,a in s['faqs']),encoding='utf-8')
# Documented design resources: existing logo is the favicon (no approximated logo artwork).
shutil.copyfile(ASSET/'logo-twco.svg',OUT/'favicon.svg')
(OUT/'site.webmanifest').write_text(json.dumps({'name':'TW&CO Premium — Oficina Mecânica','short_name':'TW&CO','start_url':'/','scope':'/','display':'standalone','background_color':'#031710','theme_color':'#00e477','lang':'pt-BR','icons':[{'src':'/favicon.svg','sizes':'any','type':'image/svg+xml','purpose':'any'}]},ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'404.html').write_text(inner_head('Página não encontrada | TW&CO Premium','A página solicitada não foi encontrada.','/404/')+'<meta name="robots" content="noindex,follow"/></head><body>'+nav()+'<main class="error-page"><div class="inner-wrap"><h1>Não encontramos essa página.</h1><p>Você pode voltar ao início ou entrar em contato com a equipe.</p><a class="primary-btn" href="/">Voltar ao site ↗</a></div></main>'+foot()+'</body></html>',encoding='utf-8')
# Sitemaps: sitemap.xml as entrypoint index, pages + image discovery separately.
ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9')
ET.register_namespace('image','http://www.google.com/schemas/sitemap-image/1.1')
N='http://www.sitemaps.org/schemas/sitemap/0.9'
IM='http://www.google.com/schemas/sitemap-image/1.1'
def generate_sitemap(filename,images=False):
 root=ET.Element('{%s}urlset'%N)
 for u in sorted(URLS,key=lambda x:x['path']):
  el=ET.SubElement(root,'{%s}url'%N)
  ET.SubElement(el,'{%s}loc'%N).text=absolute(u['path'])
  ET.SubElement(el,'{%s}lastmod'%N).text=u['modified']
  if images:
   image=ET.SubElement(el,'{%s}image'%IM);ET.SubElement(image,'{%s}loc'%IM).text=asseturl(u['image'])
 ET.ElementTree(root).write(OUT/filename,encoding='utf-8',xml_declaration=True)
generate_sitemap('sitemap-pages.xml')
generate_sitemap('sitemap-images.xml',images=True)
index=ET.Element('{%s}sitemapindex'%N)
for f in ('sitemap-pages.xml','sitemap-images.xml'):
 node=ET.SubElement(index,'{%s}sitemap'%N)
 ET.SubElement(node,'{%s}loc'%N).text=absolute('/'+f)
 ET.SubElement(node,'{%s}lastmod'%N).text=DATE
ET.ElementTree(index).write(OUT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
print('SEO COMPLETE: ',len(URLS),'indexable URLs, image sitemap, canonical and local graph')
