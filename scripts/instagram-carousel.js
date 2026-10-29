/* TW&CO Instagram — responsive, accessible six-card autoplay carousel */
(()=>{'use strict';
 const track=document.getElementById('igCarousel');
 const prev=document.getElementById('igPrev'),next=document.getElementById('igNext'),position=document.getElementById('igPosition');
 if(!track||!prev||!next||!position)return;
 const cards=Array.from(track.querySelectorAll('.ig-card'));
 if(cards.length<2)return;
 const prefersReduce=matchMedia('(prefers-reduced-motion: reduce)');
 let active=0,paused=false,timer=0,inView=false;
 const show=(index,user=false)=>{
   active=(index+cards.length)%cards.length;
   track.scrollTo({left:cards[active].offsetLeft-cards[0].offsetLeft,behavior:prefersReduce.matches?'instant':'smooth'});
   position.innerHTML=String(active+1).padStart(2,'0')+' <span>/ '+String(cards.length).padStart(2,'0')+'</span>';
   if(user){paused=true;clearInterval(timer);timer=0;}
 };
 prev.addEventListener('click',()=>show(active-1,true));
 next.addEventListener('click',()=>show(active+1,true));
 track.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();show(active+1,true);}if(e.key==='ArrowLeft'){e.preventDefault();show(active-1,true);}});
 const nearest=()=>{let idx=0,dist=Infinity;for(let i=0;i<cards.length;i++){const v=Math.abs(cards[i].offsetLeft-cards[0].offsetLeft-track.scrollLeft);if(v<dist){dist=v;idx=i;}}active=idx;position.innerHTML=String(active+1).padStart(2,'0')+' <span>/ '+String(cards.length).padStart(2,'0')+'</span>';};
 let scrollRAF=0;
 track.addEventListener('scroll',()=>{cancelAnimationFrame(scrollRAF);scrollRAF=requestAnimationFrame(nearest);},{passive:true});
 const stop=()=>{clearInterval(timer);timer=0;};
 const start=()=>{stop();if(paused||!inView||document.hidden||prefersReduce.matches)return;timer=setInterval(()=>{if(track.matches(':hover')||track.matches(':focus-within'))return;show(active+1);},4800);};
 track.addEventListener('pointerdown',()=>{paused=true;stop();},{passive:true});
 track.addEventListener('focusin',stop);
 track.addEventListener('focusout',start);
 track.addEventListener('mouseenter',stop);
 track.addEventListener('mouseleave',start);
 document.addEventListener('visibilitychange',start);
 prefersReduce.addEventListener?.('change',start);
 if('IntersectionObserver' in window){const io=new IntersectionObserver(es=>{inView=es.some(e=>e.isIntersecting);start();},{threshold:.2});io.observe(track);}
 else{inView=true;start();}
})();
