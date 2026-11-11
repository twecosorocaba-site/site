(() => {
  'use strict';
  const preview=document.querySelector('.service-card--cambio-video .twco-cambio-preview');
  if(preview){
    preview.muted=true;
    preview.volume=0;
    const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
    function visible(e){const canPlay=e.isIntersecting&&!document.hidden&&!reduced.matches;
      if(canPlay)preview.play().catch(()=>{});else preview.pause();}
    preview.addEventListener('playing',()=>preview.classList.add('is-playing'));
    preview.addEventListener('pause',()=>preview.classList.remove('is-playing'));
    if('IntersectionObserver' in window){
      const observer=new IntersectionObserver(es=>es.forEach(visible),{threshold:.15});
      observer.observe(preview);
    }else if(!reduced.matches)preview.play().catch(()=>{});
    document.addEventListener('visibilitychange',()=>{if(document.hidden)preview.pause();});
  }
  const video=document.getElementById('twcoCambioVideo');
  const button=document.getElementById('twcoCambioPlayAudio');
  if(!video||!button)return;
  function playAudio(){
    video.muted=false;
    video.volume=1;
    const attempt=video.play();
    if(attempt&&typeof attempt.then==='function'){
      attempt.then(()=>{button.hidden=true;}).catch(()=>{button.hidden=false;});
    }
  }
  button.addEventListener('click',playAudio);
  video.addEventListener('play',()=>{button.hidden=true;});
  video.addEventListener('ended',()=>{button.hidden=false;});
  // Navegação para o serviço pode não preservar a permissão de autoplay com som.
  // Tenta reproduzir após o clique no card e apresenta o botão de áudio se o navegador bloquear.
  if(new URLSearchParams(window.location.search).get('assistir')==='1')playAudio();
})();

