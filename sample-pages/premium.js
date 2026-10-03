(() => {
  'use strict';
  const $ = (s, root=document) => root.querySelector(s);
  const $$ = (s, root=document) => [...root.querySelectorAll(s)];
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  let paused = reduce.matches;
  let frame = 0;
  const animators = [];
  const motionButton = $('.motion-control');
  const setMotion = (next) => {
    paused=next;document.body.classList.toggle('motion-paused',paused);document.documentElement.classList.toggle('motion-paused',paused);
    if(motionButton){motionButton.setAttribute('aria-pressed',String(paused));motionButton.setAttribute('aria-label',paused?'Resume motion':'Pause motion');$('.motion-label',motionButton).textContent=reduce.matches?'Reduced motion':paused?'Resume motion':'Pause motion';motionButton.firstElementChild.textContent=paused?'▷':'Ⅱ';motionButton.disabled=reduce.matches;}
    if(paused||document.hidden){if(frame)cancelAnimationFrame(frame);frame=0;}else if(!frame)frame=requestAnimationFrame(tick);
  };
  function tick(t){frame=0;if(paused||document.hidden)return;for(const animate of animators){try{animate(t*.001);}catch(_){}}frame=requestAnimationFrame(tick);}
  if(motionButton)motionButton.addEventListener('click',()=>setMotion(!paused));
  reduce.addEventListener('change',()=>setMotion(reduce.matches));
  document.addEventListener('visibilitychange',()=>setMotion(paused));
  setMotion(paused);
  if('IntersectionObserver' in window){
    try{const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');observer.unobserve(e.target);}}),{threshold:.08});$$('.reveal').forEach(x=>observer.observe(x));document.documentElement.classList.add('js-motion');}catch(_){document.documentElement.classList.remove('js-motion');}
  }
  const menuButton=$('.menu-toggle'), mobileNav=$('.mobile-nav');
  function closeMenu(){if(!menuButton||!mobileNav)return;mobileNav.classList.remove('open');menuButton.setAttribute('aria-expanded','false');menuButton.setAttribute('aria-label','Open navigation');menuButton.textContent='☰';}
  if(menuButton&&mobileNav){menuButton.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')!=='true';mobileNav.classList.toggle('open',open);menuButton.setAttribute('aria-expanded',String(open));menuButton.setAttribute('aria-label',open?'Close navigation':'Open navigation');menuButton.textContent=open?'×':'☰';});$$('a',mobileNav).forEach(a=>a.addEventListener('click',closeMenu));document.addEventListener('keydown',e=>{if(e.key==='Escape'&&mobileNav.classList.contains('open')){closeMenu();menuButton.focus();}});}
  $$('.accordion details').forEach(el=>el.addEventListener('toggle',()=>{if(el.open)$$('details',el.parentElement).forEach(other=>{if(other!==el)other.open=false;});}));
  $$('[data-filter]').forEach(button=>button.addEventListener('click',()=>{
    const key=button.dataset.filter;$$('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
    $$('[data-category]').forEach(item=>item.hidden=key!=='all'&&item.dataset.category!==key);
    const n=$$('[data-category]').filter(x=>!x.hidden).length;
    const status=$('.filter-status');if(status)status.textContent=`${n} ${document.body.classList.contains('noura')?'essentials':'dishes & drinks'}`;
  }));
  const practices={
    commercial:{number:'01',label:'Commercial & business',title:'Make room for informed decisions.',copy:'An introduction to business agreements, commercial questions, and the issues a prospective client may want to discuss. The first conversation helps establish the scope of the enquiry.'},
    employment:{number:'02',label:'Employment matters',title:'Understand the questions around work.',copy:'A clear starting point for enquiries about workplace agreements, responsibilities, and employment-related matters. Specific advice depends on the circumstances and an appropriate professional consultation.'},
    property:{number:'03',label:'Property & agreements',title:'Bring the important details into focus.',copy:'An overview of property-related enquiries and agreements, designed to help visitors identify the subject they want to discuss before sharing documents privately.'},
    private:{number:'04',label:'Private matters',title:'A considered first conversation.',copy:'A discreet introduction for personal legal enquiries. This website preview asks only for a broad topic and does not collect private documents, case details, or identifying information.'}
  };
  $$('[data-practice]').forEach(button=>button.addEventListener('click',()=>{const p=practices[button.dataset.practice];$$('[data-practice]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));$('#practice-panel').innerHTML=`<div><div class="eyebrow">${p.number} / ${p.label}</div><h3>${p.title}</h3><p>${p.copy}</p></div><button class="small-link" data-modal="legal">Prepare for a conversation</button>`;}));
  const dialog=$('#project-dialog'), dialogBody=$('#dialog-body');
  let previousFocus=null;
  const choiceMarkup=(items,group)=>`<div class="options" role="group" aria-label="${group}">${items.map((x,i)=>`<button class="choice" data-choice="${group}" aria-pressed="${i===0}">${x}</button>`).join('')}</div>`;
  const configs={
    clinic:{title:'A clearer first step.',intro:'Choose the service you would like to discuss. This visit-planning preview helps you see the next step without asking for any health information.',options:['General practice','Family care','Dental care'],group:'Service',action:'Show my visit checklist',result:(a)=>`<strong>Your next step: ${a.Service}</strong><br>Make a short list of your questions. Ask the clinic about availability, the right type of appointment, and anything to bring. A real clinic would confirm the details directly.`},
    dental:{title:'Let’s start simply.',intro:'Choose what you would like to ask about. You can explore a first-visit checklist without entering personal or medical details.',options:['Routine care','Restorative care','Cosmetic enquiry'],group:'Interest',action:'Show my first-visit checklist',result:(a)=>`<strong>Your first-visit checklist: ${a.Interest}</strong><br>Write down the questions you want to discuss. Contact the clinic to confirm availability and ask what to bring. Treatment suitability and recommendations would be discussed with a qualified professional.`},
    legal:{title:'A focused first conversation.',intro:'Select a broad topic. Please do not enter private case details or upload documents in this design preview.',options:['Business','Employment','Property','Private matter'],group:'Topic',action:'Prepare my conversation',result:(a)=>`<strong>A starting point for ${a.Topic.toLowerCase()}</strong><br>Prepare a short outline of your questions and the outcome you would like to understand. A real consultancy would confirm scope, availability, conflicts, and any terms before beginning professional work. This preview provides no legal advice.`},
    restaurant:{title:'Make a night of it.',intro:'Try a simple table-enquiry journey. Pick a party size and a preferred part of the evening to see the summary.',options:['2 guests','4 guests','6 guests'],group:'Party size',action:'Preview my enquiry',result:(a)=>`<strong>${a['Party size']} · ${a.Time||'Early evening'}</strong><br>This is how a clear table enquiry could look. The restaurant would confirm the time and availability through its approved contact channel. No table has been reserved.`}
  };
  const productData={
    dawn:{title:'Dawn Serum',type:'FACE / 30 ML',price:'OMR 18.000',copy:'A lightweight texture for a quiet morning ritual. Explore a product page with clear details and room for a brand’s approved information.',image:'assets/noura-editorial-v2.jpg'},
    silk:{title:'Silk Cream',type:'FACE / 50 ML',price:'OMR 22.000',copy:'A soft finishing touch for an unhurried routine. A considered product page can make the essentials easy to discover without overwhelming the experience.',image:'assets/cosmetics.jpg'},
    evening:{title:'Evening Oil',type:'BODY / 100 ML',price:'OMR 16.000',copy:'A considered addition to the quieter part of your day. Product information and approved use details would live alongside this catalogue experience.',image:'assets/cosmetics.jpg'}
  };
  function showDialog(content){previousFocus=document.activeElement;dialogBody.innerHTML=content;if(typeof dialog.showModal==='function')dialog.showModal();else dialog.setAttribute('open','');}
  function openPreview(kind){const c=configs[kind];if(!c)return;showDialog(`<h2 id="dialog-title">${c.title}</h2><p>${c.intro}</p>${choiceMarkup(c.options,c.group)}${kind==='restaurant'?'<p class="eyebrow" style="margin-top:22px">Preferred time</p>'+choiceMarkup(['Early evening','Later evening'],'Time'):''}<button class="button" data-preview-result="${kind}">${c.action}</button><div class="preview-result" hidden aria-live="polite"></div><p class="dialog-disclaimer">Local interactive preview. No information is sent, no appointment or consultation is booked, and no payment is taken.</p>`);}
  function openProduct(key){const p=productData[key];if(!p)return;showDialog(`<div class="product-dialog-grid"><img src="${p.image}" alt="Illustrative beauty campaign imagery"><div><div class="eyebrow" style="margin-bottom:18px">${p.type}</div><h2 id="dialog-title">${p.title}</h2><p>${p.copy}</p><div style="margin-top:22px"><div class="product-spec"><span>Catalogue price</span><strong>${p.price}</strong></div><div class="product-spec"><span>Collection</span><span>The Everyday Edit</span></div></div></div></div><p class="dialog-disclaimer">Illustrative product, price, and campaign imagery. Ingredients and use information would require brand verification before launch. No efficacy claims or checkout are connected.</p>`);}
  document.addEventListener('click',e=>{
    const modalButton=e.target.closest('[data-modal]');if(modalButton){closeMenu();openPreview(modalButton.dataset.modal);return;}
    const productButton=e.target.closest('[data-product]');if(productButton){openProduct(productButton.dataset.product);return;}
    const choice=e.target.closest('[data-choice]');if(choice){$$('[data-choice]',dialogBody).filter(b=>b.dataset.choice===choice.dataset.choice).forEach(b=>b.setAttribute('aria-pressed',String(b===choice)));const r=$('.preview-result',dialogBody);if(r)r.hidden=true;return;}
    const result=e.target.closest('[data-preview-result]');if(result){const selections={};$$('[data-choice][aria-pressed="true"]',dialogBody).forEach(b=>selections[b.dataset.choice]=b.textContent);const r=$('.preview-result',dialogBody);r.innerHTML=configs[result.dataset.previewResult].result(selections);r.hidden=false;return;}
  });
  function closeDialog(){if(typeof dialog.close==='function')dialog.close();else dialog.removeAttribute('open');if(previousFocus?.focus)previousFocus.focus();}
  $('.dialog-close')?.addEventListener('click',closeDialog);
  dialog?.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeDialog();}});
  dialog?.addEventListener('close',()=>{if(previousFocus?.focus)previousFocus.focus();});
  // Subtle pointer-responsive depth, with normal page scrolling on touch.
  $$('[data-tilt]').forEach(el=>{el.addEventListener('pointermove',e=>{if(paused||e.pointerType==='touch')return;const r=el.getBoundingClientRect();el.style.setProperty('--rx',`${-(e.clientY-r.top-r.height/2)/r.height*3}deg`);el.style.setProperty('--ry',`${(e.clientX-r.left-r.width/2)/r.width*3}deg`);});el.addEventListener('pointerleave',()=>{el.style.setProperty('--rx','0deg');el.style.setProperty('--ry','0deg');});});
  // Small, local 3D meshes rendered on a 2D canvas. The same geometry is visible
  // on GPU-less browsers: there is no unrelated shape in a fallback path.
  const vsub=(a,b)=>a.map((v,i)=>v-b[i]);
  const vcross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
  const vnorm=a=>{const n=Math.hypot(...a)||1;return a.map(x=>x/n);};
  function semanticMesh(shape){
    const faces=[];
    const add=(a,b,c,color)=>{const raw=vcross(vsub(b,a),vsub(c,a));if(Math.hypot(...raw)<.0000001)return;const n=vnorm(raw);faces.push({p:[a,b,c],n,color});};
    function surface(fn,U,V,color,flip=false){const ps=[];for(let i=0;i<=U;i++){ps[i]=[];for(let j=0;j<=V;j++)ps[i][j]=fn(i/U,j/V);}for(let i=0;i<U;i++)for(let j=0;j<V;j++){let a=ps[i][j],b=ps[i+1][j],c=ps[i+1][j+1],d=ps[i][j+1];if(flip){add(a,c,b,color);add(a,d,c,color);}else{add(a,b,c,color);add(a,c,d,color);}}}
    function ellipsoid(x,y,z,rx,ry,rz,color){surface((u,v)=>{const t=u*Math.PI,p=v*Math.PI*2;return[x+rx*Math.sin(t)*Math.cos(p),y+ry*Math.cos(t),z+rz*Math.sin(t)*Math.sin(p)];},24,40,color,true);}
    function lathe(profile,color,x=0,z=0){surface((u,v)=>{let f=u*(profile.length-1),i=Math.min(Math.floor(f),profile.length-2),t=f-i;const y=profile[i][0]*(1-t)+profile[i+1][0]*t,r=profile[i][1]*(1-t)+profile[i+1][1]*t,a=v*Math.PI*2;return[x+r*Math.cos(a),y,z+r*Math.sin(a)];},Math.max(12,profile.length*4),48,color);}
    function rod(a,b,r,color){const d=vnorm(vsub(b,a)),n=vnorm(vcross(d,Math.abs(d[1])>.9?[1,0,0]:[0,1,0])),k=vcross(d,n);surface((u,v)=>a.map((x,i)=>x+(b[i]-x)*u+r*(n[i]*Math.cos(v*Math.PI*2)+k[i]*Math.sin(v*Math.PI*2))),1,14,color,true);ellipsoid(...a,r,r,r,color);ellipsoid(...b,r,r,r,color);}
    function box(x,y,z,w,h,d,color){const p=[[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]].map(a=>[x+a[0]*w/2,y+a[1]*h/2,z+a[2]*d/2]);[[0,3,2,1],[4,5,6,7],[0,1,5,4],[3,7,6,2],[0,4,7,3],[1,2,6,5]].forEach(q=>{add(p[q[0]],p[q[1]],p[q[2]],color);add(p[q[0]],p[q[2]],p[q[3]],color);});}
    if(shape==='tooth'){
      const ivory=[245,248,240];
      // A continuous enamel shell: broad crown, soft cusps, and two tapered roots.
      const curves=[[[0,.91],[-.32,1.13],[-.68,1.11],[-.82,.79]],[[-.82,.79],[-1,.44],[-.70,-.02],[-.62,-.38]],[[-.62,-.38],[-.55,-.80],[-.60,-1.48],[-.36,-1.51]],[[-.36,-1.51],[-.19,-1.51],[-.22,-.58],[0,-.51]],[[0,-.51],[.22,-.58],[.20,-1.51],[.40,-1.49]],[[.40,-1.49],[.63,-1.46],[.58,-.81],[.64,-.36]],[[.64,-.36],[.73,.01],[1,.45],[.82,.81]],[[.82,.81],[.64,1.13],[.29,1.11],[0,.91]]];
      const outline=t=>{const f=Math.min(t*curves.length,curves.length-.000001),c=curves[Math.floor(f)],v=f%1;return [0,1].map(k=>(1-v)**3*c[0][k]+3*(1-v)**2*v*c[1][k]+3*(1-v)*v*v*c[2][k]+v**3*c[3][k]);};
      for(const side of [-1,1])surface((u,v)=>{const p=outline(v),r=Math.sin(u*Math.PI/2);return[p[0]*r,.08+(p[1]-.08)*r,side*.47*Math.cos(u*Math.PI/2)];},34,120,ivory,side===-1);
    }else if(shape==='bottle'){
      lathe([[-1.15,0],[-1.15,.44],[-1.10,.50],[.30,.50],[.44,.38],[.49,.23],[.56,.23],[.56,0]],[218,175,208]);
      lathe([[.48,0],[.48,.25],[.9,.25],[.98,.20],[.98,0]],[211,211,223]);
      lathe([[.96,0],[.96,.16],[1.28,.16],[1.38,.11],[1.42,0]],[89,65,93]);
      
    }else if(shape==='scales'){
      const gold=[194,151,89],shadow=[143,109,63];
      ellipsoid(0,-1.25,0,.65,.12,.65,gold);
      lathe([[-1.2,0],[-1.2,.17],[-.99,.13],[.84,.065],[1.03,.15],[1.18,0]],gold);
      rod([-1.08,.73,0],[1.08,.73,0],.055,gold);
      for(const side of [-1,1]){let x=side*.88;for(const z of [-.25,.25]){rod([x,.72,0],[x-.31,-.26,z],.014,gold);rod([x,.72,0],[x+.31,-.26,z],.014,gold);}lathe([[-.51,0],[-.49,.13],[-.38,.33],[-.25,.47],[-.22,.47],[-.24,.40],[-.35,.26],[-.40,0]],gold,x);}
    }else{
      // Bevelled healthcare cross with a quiet enamel finish.
      const c=[122,162,130];
      box(0,0,0,.62,2.04,.46,c);box(0,0,0,2.04,.62,.46,c);

    }
    return faces;
  }
  $$('.sculpture').forEach(canvas=>{
    const ctx=canvas.getContext('2d',{alpha:true});if(!ctx)return;
    const shape=canvas.dataset.shape,mesh=semanticMesh(shape);canvas.dataset.renderer='canvas-3d';
    let tx=0,ty=0,x=0,y=0,last=0,lastDraw=0;
    const react=e=>{if(paused)return;const r=canvas.getBoundingClientRect();tx=((e.clientX-r.left)/r.width-.5)*.8;ty=((e.clientY-r.top)/r.height-.5)*.4;};
    canvas.addEventListener('pointermove',react);canvas.addEventListener('pointerleave',()=>{tx=ty=0;});
    canvas.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Home'].includes(e.key))return;e.preventDefault();if(e.key==='Home')tx=ty=0;else if(e.key==='ArrowLeft')tx-=.14;else if(e.key==='ArrowRight')tx+=.14;else if(e.key==='ArrowUp')ty-=.1;else ty+=.1;tx=Math.max(-.8,Math.min(.8,tx));ty=Math.max(-.4,Math.min(.4,ty));if(paused){x=tx;y=ty;render(last,true);}});
    function render(t,force=false){last=t;if(!force&&t-lastDraw<1/24)return;lastDraw=t;const r=canvas.getBoundingClientRect();if(!r.width||!r.height||(!force&&(r.bottom<0||r.top>innerHeight+100)))return;
      const dpr=Math.min(devicePixelRatio||1,1.5),w=Math.round(r.width*dpr),h=Math.round(r.height*dpr);if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h;}
      ctx.clearRect(0,0,w,h);x+=(tx-x)*.16;y+=(ty-y)*.16;
      const ay=(shape==='tooth'?-.24:shape==='scales'?.08:-.20)+x+(paused?0:Math.sin(t*.38)*.08),ax=(shape==='tooth'?-.19:-.10)+y;
      const cy=Math.cos(ay),sy=Math.sin(ay),cx=Math.cos(ax),sx=Math.sin(ax),scale=Math.min(w,h)/(shape==='scales'?3.3:shape==='tooth'?3.30:3.5);
      const rot=p=>{const a=p[0]*cy+p[2]*sy,b=-p[0]*sy+p[2]*cy;return[a,p[1]*cx-b*sx,p[1]*sx+b*cx];};
      const project=p=>{const q=4.8/(4.8-p[2]);return[w*.5+p[0]*scale*q,h*.49-p[1]*scale*q];};
      const gradient=ctx.createRadialGradient(w*.5,h*.88,0,w*.5,h*.88,w*.27);gradient.addColorStop(0,'rgba(0,0,0,.19)');gradient.addColorStop(1,'rgba(0,0,0,0)');ctx.save();ctx.translate(0,h*.69);ctx.scale(1,.22);ctx.fillStyle=gradient;ctx.fillRect(0,0,w,h);ctx.restore();
      const light=vnorm([-.5,.8,1.8]);const tris=mesh.map(f=>{const ps=f.p.map(rot);return{p:ps,n:rot(f.n),c:f.color,z:(ps[0][2]+ps[1][2]+ps[2][2])/3};}).sort((a,b)=>a.z-b.z);
      for(const f of tris){const n=f.n;if(shape==='tooth')n[2]=Math.abs(n[2]);if(n[2]<-.02&&shape!=="tooth")continue;const diffuse=Math.max(0,n[0]*light[0]+n[1]*light[1]+n[2]*light[2]),spec=Math.pow(Math.max(0,n[0]*-.22+n[1]*.33+n[2]*.92),36),shade=.64+.35*diffuse;const col=f.c.map(v=>Math.min(255,Math.round(v*shade+spec*36)));const ps=f.p.map(project);ctx.beginPath();ctx.moveTo(...ps[0]);ctx.lineTo(...ps[1]);ctx.lineTo(...ps[2]);ctx.closePath();ctx.fillStyle=`rgb(${col})`;ctx.strokeStyle=ctx.fillStyle;ctx.lineWidth=.55;ctx.fill();ctx.stroke();}
      // Restrained packaging label is anchored in the bottle's real 3D plane.
      if(shape==='bottle'){const p=project(rot([0,-.30,.51]));ctx.save();ctx.translate(...p);ctx.fillStyle='#513953';ctx.textAlign='center';ctx.font=`${scale*.11}px Georgia`;ctx.fillText('NOURA',0,0);ctx.font=`${scale*.055}px Arial`;ctx.fillText('DAWN SERUM',0,scale*.13);ctx.restore();}
    }
    render(0,true);animators.push(render);new ResizeObserver(()=>render(last,true)).observe(canvas);
  });
  // Soft, non-flashing ember particles. These are atmosphere, never controls.
  $$('.embers').forEach(canvas=>{try{const ctx=canvas.getContext('2d');if(!ctx)return;const seeds=Array.from({length:22},(_,i)=>({x:((i*73)%101)/101,y:((i*47)%97)/97,s:1+(i%3)*.6,speed:.012+(i%5)*.004}));function draw(t){const r=canvas.getBoundingClientRect();if(r.width<1||r.height<1||r.bottom<0||r.top>innerHeight+100)return;const w=Math.round(r.width),h=Math.round(r.height);if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h;}ctx.clearRect(0,0,w,h);seeds.forEach((p,i)=>{const y=1-((p.y+t*p.speed)%1),x=p.x+Math.sin(t*.3+i)*.03;ctx.globalAlpha=Math.sin(y*Math.PI)*.45;ctx.fillStyle=i%2?'#ffbb67':'#fa6030';ctx.beginPath();ctx.arc(x*w,y*h,p.s,0,Math.PI*2);ctx.fill();});ctx.globalAlpha=1;}draw(0);animators.push(draw);}catch(_){}});
  setMotion(paused);
})();
