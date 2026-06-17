const IMG_FILES = {
  "d_big": "d_big.jpg",
  "d_t1": "d_t1.jpg",
  "d_t2": "d_t2.jpg",
  "d_t3": "d_t3.jpg",
  "d_aerial": "d_aerial.jpg",
  "elev_front": "elev_front.png",
  "elev_left": "elev_left.png",
  "elev_rear": "elev_rear.png",
  "elev_right": "elev_right.png",
  "plan_ground": "plan_ground.png",
  "plan_first": "plan_first.png",  "eeg_logo": "tvx_logo.svg",
  "front": "front.jpg",
  "drone": "drone.jpg",
  "side": "side.jpg",
  "light1": "light1.jpg",
  "light2": "light2.jpg",
  "sun": "sun.jpg"
};

// Load images from manifest (assets/images/*). Hero img is already inlined; below-fold images get loading="lazy".
document.querySelectorAll('[data-img]').forEach(el=>{
  const k=el.getAttribute('data-img');
  if(!IMG_FILES[k])return;
  const src='assets/images/'+IMG_FILES[k];
  const target=el.tagName==='IMG'?el:el.querySelector('img');
  if(!target)return;
  const eagerKeys={light1:1,drone:1,front:1,sun:1,light2:1,side:1};
  if(!eagerKeys[k]){ target.loading='lazy'; target.decoding='async'; }
  target.src=src;
});

// Logo (PNG)
const _eeg=document.querySelector('.agency-logo');
if(_eeg && IMG_FILES.eeg_logo) _eeg.src='assets/images/'+IMG_FILES.eeg_logo;


// ---- preloader: tie to actual page load, honour the fill animation, fail-safe ----
let preDone=false;
function finishPreloader(){
  if(preDone) return;
  preDone=true;
  document.getElementById('pre').classList.add('done');
  startHero();
}
// fillup animation runs 1.6s — keep at least that, then exit on window.load
const PRE_MIN=1700;
const startMark=performance.now();
window.addEventListener('load',()=>{
  const elapsed=performance.now()-startMark;
  const wait=Math.max(0, PRE_MIN-elapsed);
  setTimeout(finishPreloader, wait);
});
// Safety net: never block longer than 4s, even if a font/image stalls
setTimeout(finishPreloader, 4000);

// ---- hero intro choreography ----
function startHero(){
  const chars=[...document.querySelectorAll('.hero h1 .ch')];
  chars.forEach((c,i)=>{
    c.animate(
      [{opacity:0,transform:'translateY(120%) rotate(6deg)'},{opacity:1,transform:'none'}],
      {duration:1100,delay:200+i*110,easing:'cubic-bezier(.16,1,.3,1)',fill:'forwards'});
  });
  const sub=document.getElementById('heroSub'), addr=document.getElementById('heroAddr');
  sub.animate([{opacity:0,transform:'translateY(20px)'},{opacity:1,transform:'none'}],
    {duration:900,delay:800,easing:'cubic-bezier(.16,1,.3,1)',fill:'forwards'});
  addr.animate([{opacity:0,transform:'translateY(20px)'},{opacity:.7,transform:'none'}],
    {duration:900,delay:1050,easing:'cubic-bezier(.16,1,.3,1)',fill:'forwards'});
}

// ---- split tease into words for sequential reveal ----
(function(){
  function wrap(node){
    const out=document.createDocumentFragment();
    node.childNodes.forEach(ch=>{
      if(ch.nodeType===3){
        ch.textContent.split(/(\s+)/).forEach(tok=>{
          if(tok.trim()){const s=document.createElement('span');s.className='line-word';s.textContent=tok;out.appendChild(s);}
          else out.appendChild(document.createTextNode(tok));
        });
      } else if(ch.nodeType===1){
        const el=ch.cloneNode(false); el.classList.add('line-word'); el.textContent=ch.textContent; out.appendChild(el);
      }
    });
    return out;
  }
  // split each tease movement independently, preserving <em>/<span> emphasis
  document.querySelectorAll('.tease-mv').forEach(p=>{
    const tmp=document.createElement('div'); tmp.innerHTML=p.innerHTML;
    p.innerHTML=''; p.appendChild(wrap(tmp));
  });
})();

// ---- reveal observer ----
const io=new IntersectionObserver((es)=>{
  es.forEach(e=>{ if(e.isIntersecting){
    if(e.target.classList.contains('tease-mv')){
      // stagger restarts per movement, so the second stanza gets its own entrance
      [...e.target.querySelectorAll('.line-word')].forEach((w,i)=>{
        w.style.transitionDelay=(i*42)+'ms'; w.classList.add('in');
      });
    } else {
      e.target.classList.add('in');
      if(e.target.querySelector && e.target.querySelector('.count')) runCount(e.target);
    }
    io.unobserve(e.target);
  }});
},{threshold:.16,rootMargin:'0px 0px -8% 0px'});
document.querySelectorAll('.rv').forEach((el,i)=>{el.style.transitionDelay=((i%5)*70)+'ms';io.observe(el);});
document.querySelectorAll('.tease-mv').forEach(el=>io.observe(el));
document.querySelectorAll('.spec .metrics .cell').forEach(c=>io.observe(c));

// ---- number counters ----
function runCount(scope){
  scope.querySelectorAll('.count').forEach(el=>{
    const to=parseFloat(el.dataset.to), dec=parseInt(el.dataset.dec||"0");
    const dur=1600, t0=performance.now();
    function tick(t){
      let p=Math.min((t-t0)/dur,1);
      p=1-Math.pow(1-p,3); // easeOutCubic
      const val=(to*p).toFixed(dec);
      el.textContent=Number(val).toLocaleString(undefined,{minimumFractionDigits:dec,maximumFractionDigits:dec});
      if(p<1)requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });
}

// ---- OpenStreetMap (Leaflet) ----
function initSitemap(){
  const el=document.getElementById('sitemap');
  if(!el||typeof L==='undefined'||el.dataset.inited)return;
  el.dataset.inited='1';
  const SITE=[4.37583,113.98639];
  const map=L.map(el,{
    center:SITE,
    zoom:16,
    minZoom:11,
    maxZoom:18,
    scrollWheelZoom:false,
    zoomControl:true,
    attributionControl:true,
    dragging:true,
    tap:true
  });
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
    maxZoom:18,
    attribution:'&copy; OpenStreetMap'
  }).addTo(map);

  const siteIcon=L.divIcon({
    className:'',
    html:'<div class="m-mark-site"><span class="m-mark-pulse"></span><span class="m-mark-dot"></span><span class="m-mark-label">No410</span></div>',
    iconSize:[28,28],
    iconAnchor:[14,14]
  });
  L.marker(SITE,{icon:siteIcon,title:'No410 · Lot 410, Block 10, M.C.L.D.',keyboard:false}).addTo(map);

  const destIcon=L.divIcon({
    className:'',
    html:'<div class="m-mark-dest"></div>',
    iconSize:[14,14],
    iconAnchor:[7,7]
  });
  const DESTS=[
    ['Miri Town Centre','~8 min',4.396,113.991],
    ['Bintang & Imperial','~8 min',4.404,113.992],
    ['Riam / Schools','~5 min',4.392,113.982],
    ['Luak Esplanade','~7 min',4.346,113.953],
    ['Miri Airport','~10 min',4.323,113.987]
  ];

  DESTS.forEach(d=>{
    L.marker([d[2],d[3]],{icon:destIcon,title:d[0]+' · '+d[1]}).addTo(map);
  });

  // Click to enable scroll-zoom; leaving disables again — keeps page scroll unhijacked.
  el.addEventListener('click',()=>map.scrollWheelZoom.enable());
  el.addEventListener('mouseleave',()=>map.scrollWheelZoom.disable());
}
if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',()=>setTimeout(initSitemap,0));}
else{setTimeout(initSitemap,0);}
window.addEventListener('load',initSitemap);

// ---- plan floor switcher ----
(function(){
  const tabs=document.querySelectorAll('.plan-tab');
  const imgs=document.querySelectorAll('[data-plan-img]');
  const panels=document.querySelectorAll('[data-plan-panel]');
  const ftag=document.getElementById('planFtag');
  const labels={ground:'Ground Floor · Scale 1:150',first:'First Floor · Scale 1:150'};
  tabs.forEach(t=>t.addEventListener('click',()=>{
    const f=t.dataset.plan;
    tabs.forEach(x=>x.classList.toggle('active',x===t));
    imgs.forEach(im=>im.classList.toggle('show',im.dataset.planImg===f));
    panels.forEach(p=>p.classList.toggle('show',p.dataset.planPanel===f));
    if(ftag) ftag.textContent=labels[f];
  }));
})();

// ---- horizontal-pan bleeds (scroll-pinned panorama) ----
function initHScrollBleed(bleed){
  const par=bleed.querySelector('.bleed-pin .par');
  const img=par&&par.querySelector('img');
  const hint=bleed.querySelector('.scroll-hint');
  if(!par||!img)return;
  let overflow=0;
  function measure(){
    const vw=window.innerWidth;
    const vh=window.innerHeight;
    overflow=Math.max(0, par.offsetWidth - vw);
    bleed.style.height=(vh + overflow)+'px';
    update();
  }
  let raf=null;
  function update(){
    const rect=bleed.getBoundingClientRect();
    let progress=0;
    if(overflow>0){
      progress=Math.max(0, Math.min(1, -rect.top / overflow));
    }
    par.style.transform='translate3d('+(-progress*overflow)+'px,0,0)';
    if(hint){ hint.style.opacity = progress>0.04 ? '0' : ''; }
  }
  function onScroll(){
    if(raf)return;
    raf=requestAnimationFrame(()=>{ update(); raf=null; });
  }
  function ready(){ measure(); addEventListener('scroll',onScroll,{passive:true}); addEventListener('resize',measure); }
  if(img.complete && img.naturalWidth) ready();
  else img.addEventListener('load', ready, {once:true});
}
document.querySelectorAll('.bleed:not(.nopan)').forEach(initHScrollBleed);

// ---- horizontal-pan feature spreads (scroll-pinned, image-only) ----
function initHScrollFeat(feat){
  const par=feat.querySelector('.imgwrap .par');
  const img=par&&par.querySelector('img');
  const imgwrap=feat.querySelector('.imgwrap');
  const hint=feat.querySelector('.feat-hint');
  if(!par||!img||!imgwrap)return;
  let overflow=0;
  function measure(){
    const wrapW=imgwrap.clientWidth;
    overflow=Math.max(0, par.offsetWidth - wrapW);
    feat.style.height=overflow>0 ? (window.innerHeight + overflow)+'px' : '';
    update();
  }
  let raf=null;
  function update(){
    if(overflow<=0){ par.style.transform=''; return; }
    const rect=feat.getBoundingClientRect();
    const progress=Math.max(0, Math.min(1, -rect.top / overflow));
    par.style.transform='translate3d('+(-progress*overflow)+'px,0,0)';
    if(hint){ hint.style.opacity = progress>0.04 ? '0' : ''; }
  }
  function onScroll(){
    if(raf)return;
    raf=requestAnimationFrame(()=>{ update(); raf=null; });
  }
  function ready(){ measure(); addEventListener('scroll',onScroll,{passive:true}); addEventListener('resize',measure); }
  if(img.complete && img.naturalWidth) ready();
  else img.addEventListener('load', ready, {once:true});
}
document.querySelectorAll('.feat:not(.nopan)').forEach(initHScrollFeat);

// ---- studies slider (combined photo carousel) ----
(function(){
  const root=document.getElementById('studySlider'); if(!root)return;
  const track=root.querySelector('.slider-track');
  const slides=[...root.querySelectorAll('.slide')];
  const dotsWrap=root.querySelector('#sDots');
  const cur=root.querySelector('#sCur');
  const n=slides.length; let i=0, timer=null;
  const rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
  slides.forEach((_,k)=>{
    const b=document.createElement('button');
    b.className='s-dot'+(k?'':' on'); b.type='button';
    b.setAttribute('aria-label','Go to study '+(k+1));
    b.addEventListener('click',()=>go(k,true)); dotsWrap.appendChild(b);
  });
  const dots=[...dotsWrap.children];
  function go(k,user){
    i=(k+n)%n;
    track.style.transform='translateX(-'+(i*100)+'%)';
    dots.forEach((d,x)=>d.classList.toggle('on',x===i));
    if(cur) cur.textContent=String(i+1).padStart(2,'0');
    if(user) restart();
  }
  function restart(){ clearInterval(timer); if(!rm) timer=setInterval(()=>go(i+1),5200); }
  root.querySelector('.prev').addEventListener('click',()=>go(i-1,true));
  root.querySelector('.next').addEventListener('click',()=>go(i+1,true));
  root.addEventListener('mouseenter',()=>clearInterval(timer));
  root.addEventListener('mouseleave',restart);
  let sx=null;
  root.addEventListener('touchstart',e=>{sx=e.touches[0].clientX;},{passive:true});
  root.addEventListener('touchend',e=>{ if(sx==null)return; const dx=e.changedTouches[0].clientX-sx; if(Math.abs(dx)>40) go(i+(dx<0?1:-1),true); sx=null; });
  restart();
})();

// ---- parallax + scroll progress (rAF throttled) ----
let ticking=false;
function onScroll(){
  if(ticking)return; ticking=true;
  requestAnimationFrame(()=>{
    const vh=innerHeight, y=scrollY;
    // progress bar
    const max=document.body.scrollHeight-vh;
    document.getElementById('prog').style.width=(y/max*100)+'%';
    // hero parallax (bg drifts down, plaque drifts up + fades)
    const hero=document.getElementById('hero');
    if(y<vh){
      const hb=document.getElementById('heroBg');
      const pl=document.getElementById('plaque');
      if(hb) hb.style.transform='translateY('+(y*0.35)+'px)';
      if(pl){pl.style.transform='translate(-50%,calc(-50% - '+(y*0.22)+'px))'; pl.style.opacity=String(Math.max(0,1-y/(vh*0.7)));}
    }
    // generic parallax layers
    document.querySelectorAll('.study .par').forEach(p=>{
      const r=p.getBoundingClientRect();
      if(r.bottom<-200||r.top>vh+200)return;
      const mid=r.top+r.height/2-vh/2;
      p.style.transform='translateY('+(mid*-0.04)+'px)';
    });
    ticking=false;
  });
}
addEventListener('scroll',onScroll,{passive:true});
addEventListener('resize',onScroll);
onScroll();