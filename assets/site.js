(()=>{'use strict';
const $=s=>document.querySelector(s), $$=s=>Array.from(document.querySelectorAll(s));
const menuBtn=$('#menuBtn'),nav=$('#mainNav');
function closeMenu(){nav?.classList.remove('open');menuBtn?.setAttribute('aria-expanded','false');document.body.classList.remove('menu-open')}
menuBtn?.addEventListener('click',()=>{const open=!nav.classList.contains('open');nav.classList.toggle('open',open);menuBtn.setAttribute('aria-expanded',String(open));document.body.classList.toggle('menu-open',open)});
$$('#mainNav a').forEach(a=>a.addEventListener('click',closeMenu));window.addEventListener('keydown',e=>{if(e.key==='Escape'){closeMenu();$('#chatPanel')?.classList.remove('open');$('#chatLaunch')?.setAttribute('aria-expanded','false')}});
const chatBtn=$('#chatLaunch'),chatPanel=$('#chatPanel'),chatClose=$('#chatClose');
chatBtn?.addEventListener('click',()=>{const open=!chatPanel.classList.contains('open');chatPanel.classList.toggle('open',open);chatBtn.setAttribute('aria-expanded',String(open))});
chatClose?.addEventListener('click',()=>{chatPanel.classList.remove('open');chatBtn.setAttribute('aria-expanded','false')});
const snapshot={status:'verified_snapshot',source:'Google Maps',retrievedAt:'2026-10-29',reviews:[{author:'Wesley Luiz',rating:5,text:'oficina muito bem organizada e equipe atenciosa !'},{author:'Cecilia Oliveira',rating:5,text:'Recomendo sem dÃºvidas, informaÃ§Ãµes claras, Ã³timo atendimento e a entrega surpreende!'},{author:'Tamara TWeCO',rating:5,te¶»§q«^