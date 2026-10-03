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
    paused=next;document.body.classList.toggle('motion-paused',paused);
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
  // Real WebGL sculptures. No libraries, network requests, or external models.
  const mul=(a,b)=>{const out=new Float32Array(16);for(let c=0;c<4;c++)for(let r=0;r<4;r++)for(let k=0;k<4;k++)out[c*4+r]+=a[k*4+r]*b[c*4+k];return out;};
  const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
  const norm=a=>{const l=Math.hypot(...a)||1;return a.map(v=>v/l);};
  function makeMesh(shape){
    const pos=[],normal=[],indices=[];const U=112,V=28;
    const center=u=>[(2+Math.cos(3*u))*.43*Math.cos(2*u),(2+Math.cos(3*u))*.43*Math.sin(2*u),Math.sin(3*u)*.48];
    function addSurface(mode,scale=1,rot=0,offset=[0,0,0]){const base=pos.length/3;
      for(let i=0;i<=U;i++){const u=i/U*Math.PI*2;let c,t,n,b;
        if(mode==='knot'){c=center(u);const c2=center(u+.001);t=norm(c2.map((v,k)=>v-c[k]));n=norm(cross(t,Math.abs(t[2])>.9?[0,1,0]:[0,0,1]));b=norm(cross(t,n));}
        for(let j=0;j<=V;j++){const v=j/V*Math.PI*2;let p,nn;
          if(mode==='knot'){nn=n.map((x,k)=>x*Math.cos(v)+b[k]*Math.sin(v));p=c.map((x,k)=>x+.185*nn[k]);}
          else {const tube=.36+(shape==='double'?.025:0);nn=[Math.cos(u)*Math.cos(v),Math.sin(u)*Math.cos(v),Math.sin(v)];p=[(1+tube*Math.cos(v))*Math.cos(u),(1+tube*Math.cos(v))*Math.sin(u),tube*Math.sin(v)];}
          const cr=Math.cos(rot),sr=Math.sin(rot);p=[p[0]*cr+p[2]*sr,p[1],-p[0]*sr+p[2]*cr];nn=[nn[0]*cr+nn[2]*sr,nn[1],-nn[0]*sr+nn[2]*cr];pos.push(...p.map((x,k)=>x*scale+offset[k]));normal.push(...nn);
        }
      }
      for(let i=0;i<U;i++)for(let j=0;j<V;j++){let a=base+i*(V+1)+j,b=a+V+1;indices.push(a,b,a+1,b,b+1,a+1);}
    }
    if(shape==='double'){addSurface('torus',.91,0,[-.22,0,0]);addSurface('torus',.55,1.4,[.6,.3,.2]);}else addSurface(shape==='knot'?'knot':'torus');
    return {pos:new Float32Array(pos),normal:new Float32Array(normal),indices:new Uint16Array(indices)};
  }
  const vertex=`attribute vec3 aPosition;attribute vec3 aNormal;uniform mat4 uMVP;uniform mat4 uModel;varying vec3 vNormal;varying vec3 vPosition;void main(){vNormal=mat3(uModel)*aNormal;vPosition=(uModel*vec4(aPosition,1.0)).xyz;gl_Position=uMVP*vec4(aPosition,1.0);}`;
  const fragment=`precision mediump float;uniform vec3 uColor;varying vec3 vNormal;varying vec3 vPosition;void main(){vec3 n=normalize(vNormal);vec3 view=normalize(-vPosition);vec3 l1=normalize(vec3(-2.5,3.5,4.));vec3 l2=normalize(vec3(3.,-.8,2.));float d1=max(dot(n,l1),0.);float d2=max(dot(n,l2),0.);float spec=pow(max(dot(n,normalize(l1+view)),0.),85.)*1.4+pow(max(dot(n,normalize(l2+view)),0.),40.)*.4;float fres=pow(1.-max(dot(n,view),0.),3.);float band=sin(n.y*7.+n.x*3.)*.06;vec3 base=uColor*(.32+.68*d1+.2*d2+band);vec3 reflection=mix(vec3(.98,.98,1.),uColor,.25);vec3 col=base+reflection*spec+reflection*fres*.24;gl_FragColor=vec4(col,1.);}`;
  $$('.sculpture').forEach(canvas=>{
    const fallback=()=>canvas.parentElement.classList.add('no-webgl');
    try{
      const gl=canvas.getContext('webgl',{alpha:true,antialias:true,powerPreference:'low-power'});if(!gl){fallback();return;}
      const compile=(type,src)=>{const s=gl.createShader(type);gl.shaderSource(s,src);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw new Error('Shader unavailable');return s;};
      const program=gl.createProgram();gl.attachShader(program,compile(gl.VERTEX_SHADER,vertex));gl.attachShader(program,compile(gl.FRAGMENT_SHADER,fragment));gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw new Error('WebGL program unavailable');gl.useProgram(program);
      const mesh=makeMesh(canvas.dataset.shape||'torus');
      const attribute=(name,data)=>{const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,data,gl.STATIC_DRAW);const loc=gl.getAttribLocation(program,name);gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,3,gl.FLOAT,false,0,0);};
      attribute('aPosition',mesh.pos);attribute('aNormal',mesh.normal);const ib=gl.createBuffer();gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,ib);gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,mesh.indices,gl.STATIC_DRAW);
      const mvpLoc=gl.getUniformLocation(program,'uMVP'),modelLoc=gl.getUniformLocation(program,'uModel');const hex=(canvas.dataset.color||'#ddef8d').replace('#','');gl.uniform3fv(gl.getUniformLocation(program,'uColor'),[0,2,4].map(i=>parseInt(hex.slice(i,i+2),16)/255));gl.enable(gl.DEPTH_TEST);gl.clearColor(0,0,0,0);
      let targetX=0,targetY=0,x=0,y=0;let last=0;
      canvas.addEventListener('pointermove',e=>{if(paused)return;const r=canvas.getBoundingClientRect();targetX=(e.clientX-r.left)/r.width-.5;targetY=(e.clientY-r.top)/r.height-.5;});canvas.addEventListener('pointerleave',()=>{targetX=0;targetY=0;});
      function render(t,force=false){last=t;const r=canvas.getBoundingClientRect();if(r.width<1||r.height<1)return;if(!force&&(r.bottom<0||r.top>innerHeight+100))return;const ratio=Math.min(devicePixelRatio||1,1.5),w=Math.round(r.width*ratio),h=Math.round(r.height*ratio);if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h;gl.viewport(0,0,w,h);}x+=(targetX-x)*.045;y+=(targetY-y)*.045;
        const ax=.55+y*.65+Math.sin(t*.18)*.1,ay=t*.16+x*.9+.3;const cx=Math.cos(ax),sx=Math.sin(ax),cy=Math.cos(ay),sy=Math.sin(ay);
        const rx=new Float32Array([1,0,0,0,0,cx,sx,0,0,-sx,cx,0,0,0,0,1]);const ry=new Float32Array([cy,0,-sy,0,0,1,0,0,sy,0,cy,0,0,0,0,1]);const model=mul(ry,rx);model[13]=Math.sin(t*.7)*.07;model[14]=canvas.dataset.shape==='knot'?-6.0:-5.2;
        const f=1/Math.tan(33*Math.PI/360),near=.1,far=30;const proj=new Float32Array([f/(w/h),0,0,0,0,f,0,0,0,0,(far+near)/(near-far),-1,0,0,2*far*near/(near-far),0]);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.uniformMatrix4fv(modelLoc,false,model);gl.uniformMatrix4fv(mvpLoc,false,mul(proj,model));gl.drawElements(gl.TRIANGLES,mesh.indices.length,gl.UNSIGNED_SHORT,0);
      }
      render(0,true);animators.push(render);if('ResizeObserver' in window)new ResizeObserver(()=>render(last,true)).observe(canvas);else window.addEventListener('resize',()=>render(last,true));
      canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();fallback();});
    }catch(_){fallback();}
  });
  // Soft, non-flashing ember particles. These are atmosphere, never controls.
  $$('.embers').forEach(canvas=>{try{const ctx=canvas.getContext('2d');if(!ctx)return;const seeds=Array.from({length:22},(_,i)=>({x:((i*73)%101)/101,y:((i*47)%97)/97,s:1+(i%3)*.6,speed:.012+(i%5)*.004}));function draw(t){const r=canvas.getBoundingClientRect();if(r.width<1||r.height<1||r.bottom<0||r.top>innerHeight+100)return;const w=Math.round(r.width),h=Math.round(r.height);if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h;}ctx.clearRect(0,0,w,h);seeds.forEach((p,i)=>{const y=1-((p.y+t*p.speed)%1),x=p.x+Math.sin(t*.3+i)*.03;ctx.globalAlpha=Math.sin(y*Math.PI)*.45;ctx.fillStyle=i%2?'#ffbb67':'#fa6030';ctx.beginPath();ctx.arc(x*w,y*h,p.s,0,Math.PI*2);ctx.fill();});ctx.globalAlpha=1;}draw(0);animators.push(draw);}catch(_){}});
  setMotion(paused);
})();
