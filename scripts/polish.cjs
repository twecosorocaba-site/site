/* Post-processamento pós-V19, sem alterar o ZIP com as imagens originais. */
'use strict';
const fs=require('fs');
const path=require('path');
const publicDir=path.resolve(process.env.TWCO_PUBLIC_DIR || 'public');
const scriptDir=__dirname;
const htmlPath=path.join(publicDir,'index.html');
const page=fs.readFileSync(htmlPath,'utf8');
const originalScriptPath=path.join(publicDir,'assets/experience.js');
let original=fs.readFileSync(originalScriptPath,'utf8');
// O script antigo tentava rolar até a resposta mesmo quando recolhida.
original=original.replace(/document\.getElementById\('diagnosticAnswer'\)\?\.scrollIntoView\(\{[^;]*\}\);/g,'');
fs.writeFileSync(originalScriptPath,original);
let html=page;
if(!html.includes('id="diagnosticForm"')||!html.includes('id="diagnosticAnswer"')
  || !html.includes('id="atendimento"') || !html.includes('id="servicos"'))
  throw new Error('Estrutura inesperada; abortando refinamento.');
html=html.replace(/(<p id="diagnosticReply">)[\s\S]*?(<\/p>)/,'$1$2');
html=html.replace('id="diagnosticAnswer" aria-live="polite"',
  'id="diagnosticAnswer" aria-live="polite" aria-hidden="true" inert');
html=html.replace('</head>',
  '<link rel="stylesheet" href="assets/experience-polish.css"/></head>');
html=html.replace('</body>',
  '<script defer src="assets/experience-polish.js"></script></body>');
fs.copyFileSync(path.join(scriptDir,'experience-polish.css'),
  path.join(publicDir,'assets/experience-polish.css'));
fs.copyFileSync(path.join(scriptDir,'experience-polish.js'),
  path.join(publicDir,'assets/experience-polish.js'));
fs.writeFileSync(htmlPath,html,'utf8');
// Movimento contínuo e discreto no carrossel de avaliações.
// Pausa em qualquer interação; permite arrastar no desktop e deslizar no celular.
const reviewsScriptPath=path.join(publicDir,'assets/site.js');
let reviewJs=fs.readFileSync(reviewsScriptPath,'utf8');
const originalTimer=/function resetTimer\(\)\{[^\n]*\}/;
const continuousTimer=`function resetTimer(){if(interval)cancelAnimationFrame(interval);let last=0;let position=viewport?.scrollLeft||0;const pixelsPerSecond=22;
 if(viewport){viewport.style.scrollSnapType='none';viewport.style.scrollBehavior='auto';viewport.style.cursor='grab';}
 function tick(now){interval=requestAnimationFrame(tick);if(!last){last=now;return;}
 const delta=Math.min(64,now-last);last=now;
 if(paused||document.hidden||isReduced.matches||!viewport||!items.length)return;
 const card=reviewTrack?.children[0];if(!card)return;
 const cycle=(card.getBoundingClientRect().width+18)*items.length;
 if(cycle<=0)return;position+=pixelsPerSecond*delta/1000;
 if(position>=cycle)position-=cycle;viewport.scrollLeft=position;}
 interval=requestAnimationFrame(tick);}`;
if((reviewJs.match(originalTimer)||[]).length!==1)throw new Error('Temporizador original não encontrado');
reviewJs=reviewJs.replace(originalTimer,continuousTimer);
const oldInteraction="viewport?.addEventListener('focusout',()=>isHover=false);";
const newInteraction=`viewport?.addEventListener('focusout',()=>isHover=false);
let reviewDrag=null;
function stopReviewDrag(e){if(!reviewDrag||e.pointerId!==reviewDrag.id)return;reviewDrag=null;viewport.style.cursor='grab';}
viewport?.addEventListener('pointerdown',e=>{
 paused=true;
 if(e.pointerType!=='mouse'||e.button!==0||e.target.closest('a,button'))return;
 reviewDrag={id:e.pointerId,x:e.clientX};
 viewport.setPointerCapture(e.pointerId);viewport.style.cursor='grabbing';
});
viewport?.addEventListener('pointermove',e=>{
 if(!reviewDrag||reviewDrag.id!==e.pointerId)return;
 viewport.scrollLeft-=e.clientX-reviewDrag.x;reviewDrag.x=e.clientX;
});
viewport?.addEventListener('pointerup',stopReviewDrag);
viewport?.addEventListener('pointercancel',stopReviewDrag);
viewport?.addEventListener('touchstart',()=>paused=true,{passive:true});
viewport?.addEventListener('wheel',()=>paused=true,{passive:true});
viewport?.addEventListener('keydown',()=>paused=true);
viewport?.addEventListener('focusin',()=>paused=true);`;
if(reviewJs.split(oldInteraction).length!==2)throw new Error('Interação original inesperada');
reviewJs=reviewJs.replace(oldInteraction,newInteraction);
fs.writeFileSync(reviewsScriptPath,reviewJs);

console.log('TW&CO Premium V20 — experiência refinada, demais seções intactas.');
