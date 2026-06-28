document.getElementById('yr')&&(document.getElementById('yr').textContent=new Date().getFullYear());
var progress=document.getElementById('progress');
function onScroll(){if(!progress)return;var y=window.scrollY,h=document.documentElement.scrollHeight-window.innerHeight;progress.style.width=(h>0?(y/h)*100:0)+'%';}
window.addEventListener('scroll',onScroll,{passive:true});onScroll();
var burger=document.getElementById('burger'),overlay=document.getElementById('overlay');
function toggleNav(o){document.body.classList.toggle('nav-open',o);if(burger)burger.setAttribute('aria-expanded',o);if(overlay)overlay.setAttribute('aria-hidden',!o);document.body.style.overflow=o?'hidden':'';}
burger&&burger.addEventListener('click',function(){toggleNav(!document.body.classList.contains('nav-open'));});
overlay&&overlay.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){toggleNav(false);});});
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.1,rootMargin:'0px 0px -8% 0px'});
document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});
var enBtn=document.getElementById('en'),psBtn=document.getElementById('ps');
function setLang(lang){var ps=lang==='ps';document.documentElement.lang=ps?'ps':'en';document.documentElement.dir=ps?'rtl':'ltr';document.body.dir=ps?'rtl':'ltr';
  enBtn&&enBtn.classList.toggle('on',!ps);psBtn&&psBtn.classList.toggle('on',ps);
  document.querySelectorAll('[data-en]').forEach(function(el){var t=ps?(el.dataset.ps||el.dataset.en):el.dataset.en;var s=el.querySelector('.t');if(s){s.textContent=t;}else{el.textContent=t;}});}
enBtn&&enBtn.addEventListener('click',function(){setLang('en');});
psBtn&&psBtn.addEventListener('click',function(){setLang('ps');});
