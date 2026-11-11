/* Integra o vídeo fornecido pela TW&CO somente no card Câmbio e fluidos
   e na página correspondente, preservando as outras áreas. */
'use strict';
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'..');
const OUT=path.resolve(process.env.TWCO_PUBLIC_DIR||path.join(ROOT,'public'));
const assetDir=path.join(OUT,'assets');
const full=path.join(ROOT,'media/cambio-fluidos.mp4');
const preview=path.join(ROOT,'media/cambio-fluidos-card.mp4');
for(const file of [full,preview])assert.ok(fs.statSync(file).size>100_000,'Mídia inválida: '+file);
fs.copyFileSync(full,path.join(assetDir,'cambio-fluidos.mp4'));
fs.copyFileSync(preview,path.join(assetDir,'cambio-fluidos-card.mp4'));
fs.copyFileSync(path.join(__dirname,'cambio-video.css'),path.join(assetDir,'cambio-video.css'));
fs.copyFileSync(path.join(__dirname,'cambio-video.js'),path.join(assetDir,'cambio-video.js'));

function injectAssets(document,label){
 const head='<link rel="stylesheet" href="/assets/cambio-video.css"/>';
 const script='<script defer src="/assets/cambio-video.js"></script>';
 assert.equal(document.split('</head>').length,2,label+': </head> inesperado');
 assert.equal(document.split('</body>').length,2,label+': </body> inesperado');
 return document.replace('</head>',head+'</head>').replace('</body>',script+'</body>');
}
const homePath=path.join(OUT,'index.html');
let home=fs.readFileSync(homePath,'utf8');
const text='<h3>Câmbio e fluidos</h3>';
assert.equal(home.split(text).length,2,'Card de câmbio deve existir uma vez');
const p=home.indexOf(text),start=home.lastIndexOf('<a ',p),end=home.indexOf('</a>',p)+4;
assert.ok(start>=0&&end>p,'Card de câmbio incompleto');
let card=home.slice(start,end);
assert.ok(card.includes('class="service-card"')&&card.includes('servico-cambio.webp'),'Card diferente do esperado');
card=card.replace('class="service-card"','class="service-card service-card--cambio-video"');
card=card.replace(/href="[^"]+"/,'href="/servicos/cambio-e-fluidos/?assistir=1"');
card=card.replace(/ target="_blank"/g,'').replace(/ rel="noopener noreferrer"/g,'');
const marker='<div class="service-media">';
const mp=card.indexOf(marker);assert.ok(mp>=0,'Imagem do serviço não encontrada');
const mediaEnd=card.indexOf('</div>',mp);assert.ok(mediaEnd>mp,'Container media ausente');
const thumb='<video class="twco-cambio-preview" src="/assets/cambio-fluidos-card.mp4" poster="/assets/servico-cambio.webp" muted autoplay playsinline loop preload="metadata" aria-hidden="true" tabindex="-1"></video>';
card=card.slice(0,mediaEnd)+thumb+card.slice(mediaEnd);
home=injectAssets(home.slice(0,start)+card+home.slice(end),'home');
fs.writeFileSync(homePath,home,'utf8');

const servicePath=path.join(OUT,'servicos/cambio-e-fluidos/index.html');
let detail=fs.readFileSync(servicePath,'utf8');
const figureBegin='<figure><img src="/assets/servico-cambio.webp"';
const ix=detail.indexOf(figureBegin);assert.ok(ix>=0&&detail.indexOf(figureBegin,ix+1)===-1,'Figure de câmbio inesperado');
const close=detail.indexOf('</figure>',ix);assert.ok(close>ix,'Fim da figura não encontrado');
const feature='<figure class="twco-cambio-feature"><div class="twco-cambio-player">'+
 '<video id="twcoCambioVideo" src="/assets/cambio-fluidos.mp4" poster="/assets/servico-cambio.webp" playsinline preload="metadata" controls aria-label="Vídeo da troca de fluido de transmissão automática na TW&CO"></video>'+
 '<button type="button" id="twcoCambioPlayAudio" class="twco-cambio-audio-button" aria-controls="twcoCambioVideo">▶ Assistir com áudio</button></div>'+
 '<figcaption>Conheça o atendimento da TW&CO para transmissão automática.</figcaption></figure>';
detail=detail.slice(0,ix)+feature+detail.slice(close+'</figure>'.length);
detail=injectAssets(detail,'service');
fs.writeFileSync(servicePath,detail,'utf8');

assert.ok(home.includes('Câmbio e fluidos')&&home.includes('cambio-fluidos-card.mp4'));
assert.ok(detail.includes('cambio-fluidos.mp4')&&detail.includes('Assistir com áudio'));
console.log('TWCO VIDEO: card silencioso com clique para página; vídeo completo com áudio na página de câmbio.');

