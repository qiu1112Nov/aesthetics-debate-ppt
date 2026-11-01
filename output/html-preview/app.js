(() => {
 'use strict';
 const slides=[...document.querySelectorAll('.slide')],viewer=document.getElementById('viewer'),stage=document.getElementById('stage'),wrap=document.getElementById('stage-wrap');
 const prev=document.getElementById('prev'),next=document.getElementById('next'),zoom=document.getElementById('zoom'),dialog=document.getElementById('source-dialog');
 let current=0,enlarged=false;
 function fit(){const padding=innerWidth<=650?16:40,w=viewer.clientWidth-padding,h=viewer.clientHeight-padding;const scale=enlarged?Math.max(.65,Math.min(1,w/1920)):Math.min(w/1920,h/1080);stage.style.transform=`scale(${scale})`;wrap.style.width=`${1920*scale}px`;wrap.style.height=`${1080*scale}px`;}
 function show(index,updateHash=true){current=Math.max(0,Math.min(slides.length-1,index));slides.forEach((s,i)=>s.hidden=i!==current);prev.disabled=current===0;next.disabled=current===slides.length-1;const id=slides[current].dataset.page;document.getElementById('counter').value=`${id} · ${current+1}/5`;document.title=`${id} · 从观看山水到栖居山水`;if(updateHash)history.replaceState(null,'',`#${id}`);viewer.scrollTo(0,0);}
 prev.addEventListener('click',()=>show(current-1));next.addEventListener('click',()=>show(current+1));
 zoom.addEventListener('click',()=>{enlarged=!enlarged;document.body.classList.toggle('zoomed',enlarged);zoom.textContent=enlarged?'−':'＋';zoom.setAttribute('aria-pressed',String(enlarged));zoom.setAttribute('aria-label',enlarged?'恢复整页':'放大阅读');fit();});
 const full=document.getElementById('fullscreen');if(!document.documentElement.requestFullscreen)full.hidden=true;
 full.addEventListener('click',async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{full.hidden=true;}fit();});
 document.getElementById('sources').addEventListener('click',()=>dialog.showModal());document.getElementById('close-sources').addEventListener('click',()=>dialog.close());
 document.addEventListener('keydown',e=>{if(dialog.open||['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName))return;if(e.key===' '&&['BUTTON','A'].includes(document.activeElement.tagName))return;if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();show(current+1);}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();show(current-1);}if(e.key==='Home'){e.preventDefault();show(0);}if(e.key==='End'){e.preventDefault();show(slides.length-1);}});
 let touch;viewer.addEventListener('touchstart',e=>{touch=e.touches.length===1?{x:e.touches[0].clientX,y:e.touches[0].clientY}:null;},{passive:true});viewer.addEventListener('touchmove',e=>{if(e.touches.length!==1)touch=null;},{passive:true});viewer.addEventListener('touchend',e=>{if(!touch||enlarged||!e.changedTouches.length)return;const dx=e.changedTouches[0].clientX-touch.x,dy=e.changedTouches[0].clientY-touch.y;if(Math.abs(dx)>55&&Math.abs(dx)>Math.abs(dy)*1.4)show(current+(dx<0?1:-1));touch=null;},{passive:true});
 function fromHash(){const i=slides.findIndex(s=>`#${s.dataset.page}`===location.hash.toUpperCase());show(i<0?0:i,false);}
 addEventListener('hashchange',fromHash);addEventListener('resize',fit);document.addEventListener('fullscreenchange',fit);fromHash();fit();
})();
