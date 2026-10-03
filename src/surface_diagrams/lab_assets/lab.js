'use strict';
let state,selected=0,busy=false,dragged=null,prefixExport=null,sphereExport=null,prefixSvgs={},sphereChartSvg='',prefixIndex=null,prefixRequest=0,prefixFit=true,prefixHighlight=null,arcRequest=0,arcSvg='',arcSelection=null,arcFit=true;
const prefixColors=['#d73027','#e08214','#b59b00','#23964f','#168aad','#5254c8'];
const $=id=>document.getElementById(id);
const status=(text,error=false)=>{ $('status').textContent=text; $('status').classList.toggle('error',error); };
const prefixSystem=$('prefix-system');
prefixSystem.onchange=()=>{if(prefixIndex!==null)showPrefix(prefixIndex);};
const arcDialog=document.createElement('dialog');arcDialog.id='arc-inspector';
arcDialog.innerHTML='<div class="inspect-heading"><h2 id="arc-title">Individual based arc</h2><button id="close-arc">Close</button></div><p>This is one exact based meridian arc. Its ray word is checked against the full meridian image. A single-arc drawing does not verify that all six arcs are jointly disjoint or form a cut system.</p><p id="arc-status" role="status"></p><div class="toolbar"><button id="arc-previous">← Previous arc</button><button id="arc-next">Next arc →</button><button id="arc-toggle">Show before</button></div><div class="toolbar"><button id="arc-fit">Show detail</button><button id="arc-start">Start</button><button id="arc-middle">Middle</button><button id="arc-end">End</button><span>Fit shows the whole arc; detail shows its original size.</span></div><div id="arc-drawing" class="prefix-drawing"></div><details><summary id="arc-word-summary">Full based image</summary><p id="arc-word" class="full-word"></p></details><button id="save-arc" disabled>Save SVG</button>';
document.body.append(arcDialog);
const compareDialog=document.createElement('dialog');compareDialog.id='compare-inspector';
compareDialog.innerHTML='<div class="inspect-heading"><h2 id="compare-title">Compare one based arc</h2><button id="close-compare">Close</button></div><p>These are two individually routed exact meridian arcs. Their full based images are checked separately; the pair does not depict or check a joint six-arc placement.</p><p id="compare-status" role="status"></p><div class="toolbar"><button id="compare-fit">Show detail</button><button id="compare-start">Start</button><button id="compare-middle">Middle</button><button id="compare-end">End</button><span>Fit shows both whole arcs; detail shows their original size.</span></div><div class="prefix-drawings"><figure><figcaption>Before <button id="save-compare-before" disabled>Save SVG</button></figcaption><div id="compare-before" class="prefix-drawing"></div></figure><figure><figcaption>After <button id="save-compare-after" disabled>Save SVG</button></figcaption><div id="compare-after" class="prefix-drawing"></div></figure></div><p id="compare-diff" class="full-word"></p>';
document.body.append(compareDialog);
let compareRequest=0,compareFit=true,compareSvgs={};
$('close-compare').onclick=()=>{compareRequest++;compareDialog.close();};
for(const side of ['before','after'])$(`save-compare-${side}`).onclick=()=>{
 if(compareSvgs[side])download(compareSvgs[side],'image/svg+xml',`individual-arc-${side}.svg`);
};
function positionCompare(fraction){
 if(compareFit)setCompareFit(false);
 for(const side of ['before','after']){
  const drawing=$(`compare-${side}`);drawing.scrollTop=(drawing.scrollHeight-drawing.clientHeight)/2;
  drawing.scrollLeft=(drawing.scrollWidth-drawing.clientWidth)*fraction;
 }
}
function setCompareFit(fit){
 compareFit=fit;$('compare-fit').textContent=fit?'Show detail':'Fit both arcs';
 for(const side of ['before','after']){
  const drawing=$(`compare-${side}`),svg=drawing.querySelector('svg');
  if(svg){svg.style.width=fit?'100%':'';svg.style.height=fit?'auto':'';svg.classList.toggle('fit-overview',fit);}
  if(fit)drawing.scrollTo(0,0);
 }
 if(!fit)positionCompare(.5);
}
$('compare-fit').onclick=()=>setCompareFit(!compareFit);
for(const [id,fraction] of [['compare-start',0],['compare-middle',.5],['compare-end',1]])
 $(id).onclick=()=>positionCompare(fraction);
$('close-arc').onclick=()=>{arcRequest++;arcDialog.close();};
$('save-arc').onclick=()=>{if(arcSvg)download(arcSvg,'image/svg+xml','individual-based-arc.svg');};
function positionArc(fraction){
 if(arcFit)setArcFit(false);
 const drawing=$('arc-drawing');drawing.scrollTop=(drawing.scrollHeight-drawing.clientHeight)/2;
 drawing.scrollLeft=(drawing.scrollWidth-drawing.clientWidth)*fraction;
}
function setArcFit(fit){
 arcFit=fit;$('arc-fit').textContent=fit?'Show detail':'Fit whole arc';
 const drawing=$('arc-drawing'),svg=drawing.querySelector('svg');
 if(svg){svg.style.width=fit?'100%':'';svg.style.height=fit?'auto':'';svg.classList.toggle('fit-overview',fit);}
 if(fit)drawing.scrollTo(0,0);
 else positionArc(.5);
}
$('arc-fit').onclick=()=>setArcFit(!arcFit);
for(const [id,fraction] of [['arc-start',0],['arc-middle',.5],['arc-end',1]])$(id).onclick=()=>positionArc(fraction);
for(const [id,delta] of [['arc-previous',-1],['arc-next',1]])$(id).onclick=()=>{
 if(arcSelection)showArc(arcSelection.side,arcSelection.arcIndex+delta,arcSelection.index,arcSelection.revision);
};
$('arc-toggle').onclick=()=>{
 if(arcSelection)showArc(arcSelection.side==='before'?'after':'before',arcSelection.arcIndex,arcSelection.index,arcSelection.revision);
};
function controls(){
 const f=state?.factors[selected];
 $('undo').disabled=busy||!state?.undo; $('redo').disabled=busy||!state?.redo;
 document.querySelectorAll('#history-list button').forEach(button=>button.disabled=busy||Number(button.dataset.position)===state?.position);
 for(const id of ['reset','save','open','svg','simplify','sphere','conjugate','global-word']) $(id).disabled=busy||!state;
 $('selected').textContent=f?`${f.id} · ${f.label}`:'Select a factor';
 const picker=$('split-kind');picker.replaceChildren();
 for(const [value,label] of f?.splits||[]){const o=document.createElement('option');o.value=value;o.textContent=label;picker.append(o);}
 if(!picker.options.length){const o=document.createElement('option');o.textContent='No available split';picker.append(o);}
 picker.disabled=busy||!f?.splits.length;$('split').disabled=picker.disabled;
 $('combine').disabled=busy||!f||selected>=state.factors.length-1;
 $('inspect').disabled=busy||!f;
 $('prefix').disabled=busy||!f;
}
function choose(index){
 selected=index;
 document.querySelectorAll('.factor').forEach((el,i)=>el.classList.toggle('selected',i===selected));
 document.querySelectorAll('.braid-row').forEach((el,i)=>el.classList.toggle('selected',i===selected));
 controls();
}
function paint(){
 $('history-summary').textContent=`Exploration history · step ${state.position+1} of ${state.steps.length}`;
 $('history-list').replaceChildren();
 state.steps.forEach((label,i)=>{
  const item=document.createElement('li');item.classList.toggle('current',i===state.position);
  const button=document.createElement('button');button.textContent=label;button.dataset.position=i;
  button.setAttribute('aria-label',`Open history step ${i+1}: ${label}`);
  button.onclick=()=>action({op:'seek',position:i},0);
  item.append(button);$('history-list').append(item);
 });
 $('storage-status').textContent=window.surfaceLabPublic?(window.surfaceLabStorageAvailable?'Workspace and undo history are saved in this browser. Export JSON to move them to another device.':'Browser storage is unavailable or full. Export JSON before closing or refreshing this page.'):state.persistent?'Workspace and undo history saved to session file.':'Session is in memory. Save JSON before stopping the server.';
 $('frame-status').textContent=state.frame?.length?`Global frame g = ${state.frame.join(' ')}`:'Global frame g = identity';
 $('frame-status').title=$('frame-status').textContent;
 selected=Math.min(selected,state.factors.length-1);
 $('count').textContent=`${state.factors.length} factors · ${state.factors.reduce((n,f)=>n+f.word.length,0)} letters`;
 $('factors').replaceChildren();
 state.factors.forEach((f,i)=>{
  const card=document.createElement('article');card.className='factor';card.draggable=true;card.tabIndex=0;card.style.height=f.height+'px';card.dataset.index=i;card.setAttribute('aria-label',`${f.id}, ${f.label}, position ${i+1}`);
  const head=document.createElement('div');head.className='factor-head';
  const title=document.createElement('span');const name=document.createElement('strong');name.textContent=f.id;const kind=document.createElement('span');kind.className='kind';kind.textContent=f.label;title.append(name,kind);
  const buttons=document.createElement('span');buttons.className='row-buttons';
  for(const [label,delta] of [['↑',-1],['↓',1]]){const b=document.createElement('button');b.textContent=label;b.setAttribute('aria-label',`Move ${f.id} ${delta<0?'up':'down'}`);b.disabled=i+delta<0||i+delta>=state.factors.length;b.onclick=e=>{e.stopPropagation();choose(i);action({op:'move',index:i,target:i+delta},i+delta);};buttons.append(b);}
  head.append(title,buttons);const support=document.createElement('div');support.className='support';
  if(f.svg)support.innerHTML=f.svg;else{const warning=document.createElement('p');warning.className='warning';warning.textContent=f.warning;support.append(warning);}
  const word=document.createElement('div');word.className='word';word.textContent=f.word.join(' ');word.title=word.textContent;
  const audit=document.createElement('div');audit.className='support-check '+(f.audit?.status||'unavailable');
  audit.textContent=f.audit?.matches===true?'Boundary word agrees':f.audit?.matches===false?'Preview check failed':'Preview check unavailable';
  if(f.audit?.matches===true&&f.audit.cut_visits>64) audit.textContent+=` · ${f.audit.cut_visits} cuts — zoom to inspect`;
  audit.title=f.audit?.message||'No support audit available';
  card.append(head,audit,support,word);card.onclick=()=>choose(i);card.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();choose(i);}};
  card.ondragstart=e=>{if(busy){e.preventDefault();return;}dragged=i;choose(i);e.dataTransfer.setData('text/plain',String(i));e.dataTransfer.effectAllowed='move';card.classList.add('dragging');};
  card.ondragover=e=>{if(dragged===null||busy)return;e.preventDefault();e.dataTransfer.dropEffect='move';card.classList.add('drop-target');};
  card.ondragleave=()=>card.classList.remove('drop-target');
  card.ondrop=e=>{e.preventDefault();card.classList.remove('drop-target');const from=dragged;dragged=null;if(from!==null&&from!==i)action({op:'move',index:from,target:i},i);};
  card.ondragend=()=>{dragged=null;document.querySelectorAll('.dragging,.drop-target').forEach(el=>el.classList.remove('dragging','drop-target'));};
  $('factors').append(card);
 });
 $('braid').innerHTML=state.braid;choose(selected);status(state.message);
}
async function action(payload,next=selected){
 if(busy)return;busy=true;document.body.classList.add('busy');controls();status('Checking exact braid actions and redrawing affected supports…');
 try{const r=await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json','X-Surface-Token':state.token},body:JSON.stringify({...payload,revision:state.revision})});const data=await r.json();if(!r.ok)throw new Error(data.error);state=data;selected=next;paint();}
 catch(e){status(e.message,true);}finally{busy=false;document.body.classList.remove('busy');controls();}
}
function download(content,type,name){const url=URL.createObjectURL(new Blob([content],{type}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
function inspectZoom(){
 const viewport=$('inspect-viewport'),drawing=$('inspect-drawing');
 const cx=drawing.offsetWidth>viewport.clientWidth?(viewport.scrollLeft+viewport.clientWidth/2)/drawing.offsetWidth:.5;
 const cy=drawing.offsetHeight>viewport.clientHeight?(viewport.scrollTop+viewport.clientHeight/2)/drawing.offsetHeight:.5;
 const scale=Number($('zoom').value);
 drawing.style.width=(680*scale)+'px';drawing.style.height=(352*scale)+'px';
 viewport.scrollTo(cx*drawing.offsetWidth-viewport.clientWidth/2,cy*drawing.offsetHeight-viewport.clientHeight/2);
}
$('inspect').onclick=()=>{
 const f=state.factors[selected];
 $('inspect-title').textContent=`${f.id} · ${f.label}`;
 $('inspect-drawing').replaceChildren();
 if(f.svg){$('inspect-drawing').innerHTML=f.svg;$('inspect-drawing').querySelectorAll('path').forEach(p=>{p.setAttribute('vector-effect','non-scaling-stroke');p.setAttribute('stroke-width','1');});}
 else $('inspect-drawing').textContent=f.warning;
 $('inspect-word').textContent='Braid: '+f.word.join(' ');
 $('inspect-conjugator').textContent='Conjugator: '+(f.conjugator.join(' ')||'identity');
 $('inspect-core').textContent='Standard core (including power): '+f.core.join(' ');
 $('inspect-audit').textContent=f.audit?.message||'No support audit available.';
 $('inspect-itinerary').textContent=f.audit?.itinerary||'No accepted shared itinerary available.';
 $('inspect-actual').textContent='Itinerary boundary class: '+(f.audit?.actual?.join(' ')||'unavailable');
 $('inspect-expected').textContent='Exact transported class: '+(f.audit?.expected?.join(' ')||'unavailable');
 $('zoom').value='1';inspectZoom();$('inspector').showModal();
 $('inspect-viewport').scrollTo(0,0);
};
$('prefix').onclick=()=>showPrefix(selected);
function positionPrefix(fraction){
 if(prefixFit)setPrefixFit(false);
 for(const side of ['before','after']){
  const drawing=$(`prefix-${side}`);
  drawing.scrollTop=(drawing.scrollHeight-drawing.clientHeight)/2;
  drawing.scrollLeft=(drawing.scrollWidth-drawing.clientWidth)*fraction;
 }
}
function setPrefixFit(fit){
 prefixFit=fit;$('prefix-fit').textContent=fit?'Show detail':'Fit whole diagrams';
 for(const side of ['before','after']){
  const drawing=$(`prefix-${side}`),svg=drawing.querySelector('svg');
  if(drawing.classList.contains('arc-gallery-host'))continue;
  if(svg){svg.style.width=fit?'100%':'';svg.style.height=fit?'auto':'';svg.classList.toggle('fit-overview',fit);}
  if(fit)drawing.scrollTo(0,0);
 }
 if(!fit)positionPrefix(.5);
}
function tracePrefix(index){
 prefixHighlight=prefixHighlight===index?null:index;
 for(const side of ['before','after']){
  const drawing=$(`prefix-${side}`);
  if(drawing.classList.contains('arc-gallery-host')){
   drawing.querySelectorAll('.arc-gallery-card').forEach(card=>
    card.classList.toggle('muted',prefixHighlight!==null&&Number(card.dataset.arc)!==prefixHighlight));
   continue;
  }
  const svg=drawing.querySelector('svg');
  if(!svg)continue;
  svg.classList.toggle('tracing',prefixHighlight!==null);
  svg.querySelectorAll('path.arc').forEach(path=>
   path.classList.toggle('traced',path.getAttribute('stroke')===prefixColors[prefixHighlight]));
 }
 $('prefix-rows').querySelectorAll('.trace-arc').forEach((button,i)=>{
  const pressed=i===prefixHighlight;
  button.setAttribute('aria-pressed',String(pressed));
  button.title=pressed?'Show all six arcs':`Trace ${prefixExport?.system==='chain'?'e':'x'}${i+1} in both drawings`;
 });
}
function prefixWordChange(before,after){
 let prefix=0,suffix=0;
 while(prefix<Math.min(before.length,after.length)&&before[prefix]===after[prefix])prefix++;
 while(suffix<Math.min(before.length,after.length)-prefix&&
       before[before.length-suffix-1]===after[after.length-suffix-1])suffix++;
 if(prefix===before.length&&prefix===after.length)return 'Exact word unchanged.';
 const middle=word=>word.slice(prefix,word.length-suffix);
 const excerpt=word=>{
  const part=middle(word);
  return part.length<=14?part.join(' ')||'∅':
   `${part.slice(0,7).join(' ')} … ${part.slice(-7).join(' ')}`;
 };
 return `Shared prefix ${prefix}, suffix ${suffix} letters. Changed middle: before ${excerpt(before)} (${middle(before).length} letters) → after ${excerpt(after)} (${middle(after).length} letters).`;
}
function offerArcGallery(side,index,revision,request,warning){
 const drawing=$(`prefix-${side}`);drawing.replaceChildren();
 const note=document.createElement('p');note.textContent=`Joint drawing unavailable: ${warning}`;
 const button=document.createElement('button');button.textContent='Show six arcs separately';
 button.onclick=()=>showArcGallery(side,index,revision,request);
 drawing.append(note,button);
}
async function showArcGallery(side,index,revision,request){
 if(request!==prefixRequest||state.revision!==revision)return;
 const drawing=$(`prefix-${side}`);drawing.replaceChildren();drawing.classList.add('arc-gallery-host');
 const note=document.createElement('p');
 note.textContent='Each available preview is exact and routed separately; unavailable arcs report their limit. This gallery does not show or check their joint planar placement.';
 const progress=document.createElement('p');progress.setAttribute('role','status');
 const grid=document.createElement('div');grid.className='arc-gallery';
 const cards=[];
 for(let i=0;i<6;i++){
  const card=document.createElement('div');card.className='arc-gallery-card';card.dataset.arc=String(i);
  card.classList.toggle('muted',prefixHighlight!==null&&prefixHighlight!==i);
  const head=document.createElement('div');head.className='arc-gallery-head';
  const label=document.createElement('strong');
  const endpoints=prefixExport[`${side}_endpoints`][i];
  label.textContent=prefixExport.system==='chain'?`e${i+1}: ${endpoints[0]||'rim'} → ${endpoints[1]}`:
   `x${i+1} → ${endpoints[1]}`;
  const inspect=document.createElement('button');inspect.textContent='Inspect';
  inspect.setAttribute('aria-label',`Inspect ${side} arc ${prefixExport.system==='chain'?'e':'x'}${i+1} after ${state.factors[index].id}`);
  inspect.onclick=()=>showArc(side,i,index,revision);
  head.append(label,inspect);
  const preview=document.createElement('div');preview.className='arc-gallery-preview';
  preview.textContent='Routing exact arc…';card.append(head,preview);grid.append(card);cards.push(preview);
 }
 drawing.append(note,progress,grid);
 for(let i=0;i<6;i++){
  progress.textContent=`Routing ${i+1} of 6 exact arcs…`;
  try{
   const response=await fetch(`/api/prefix-arc?index=${index}&side=${side}&arc=${i}&revision=${revision}&system=${prefixExport.system}`);
   const data=await response.json();
   if(request!==prefixRequest||state.revision!==revision)return;
   if(!response.ok)throw new Error(data.error);
   if(data.svg)cards[i].innerHTML=data.svg;
   else cards[i].textContent=`Drawing unavailable: ${data.warning}`;
  }catch(error){if(request!==prefixRequest)return;cards[i].textContent=error.message;}
 }
 progress.textContent='All six arc previews attempted. Open Inspect for a full route; unavailable cards show their limits.';
}
async function showPrefix(index){
 if(!state||index<0||index>=state.factors.length)return;
 const revision=state.revision,request=++prefixRequest,system=prefixSystem.value;
 prefixIndex=index;choose(index);
 $('prefix-inspector').querySelector('p').textContent=system==='chain'?
  'The colored chain runs from the left boundary to its first puncture, then from each puncture to the next. The first edge is checked by its based meridian; each later edge is recovered from the exact image of the boundary around an adjacent puncture pair. Joint routing checks their simultaneous drawing.':
  'The six colored spokes run from one left-boundary basepoint to the punctures. Each ray word reproduces its complete based meridian image; joint routing checks their simultaneous drawing.';
 $('prefix-inspector').querySelectorAll('p')[1].textContent=system==='chain'?
  'The edge labels e1–e6 follow the original order, while the colored endpoint numbers show where the braid moves them. The exact neighborhood-boundary words retain winding; click an edge label to trace it in both drawings. This is the six-point disk action.':
  'Colored puncture numbers show only the permutation; the words retain winding and base paths. Click x1–x6 below to trace one arc in both drawings. This is the six-point disk action, without imposing the sphere relation.';
 $('prefix-title').textContent=`After ${state.factors[index].id} · exact prefix action`;
 $('prefix-position').textContent=`Factor ${index+1} of ${state.factors.length}`;
 $('prefix-previous').disabled=index===0;
 $('prefix-next').disabled=index===state.factors.length-1;
 prefixExport=null;prefixSvgs={};prefixHighlight=null;$('save-prefix').disabled=true;
 $('save-prefix-before').disabled=true;$('save-prefix-after').disabled=true;
 $('prefix-rows').replaceChildren();
 for(const side of ['before','after']){
  const drawing=$(`prefix-${side}`);drawing.classList.remove('arc-gallery-host');drawing.replaceChildren();
 }
 $('prefix-status').textContent=`Computing exact ${system==='chain'?'chain-edge':'based meridian'} images and routing the cut system…`;
 if(!$('prefix-inspector').open)$('prefix-inspector').showModal();
 try{
  const response=await fetch(`/api/prefix?index=${index}&revision=${revision}&system=${system}`);
  const data=await response.json();
  if(request!==prefixRequest)return;
  if(!response.ok)throw new Error(data.error);
  if(state.revision!==revision)throw new Error('The factorization changed; reopen this inspector.');
  prefixExport={factor:data.factor,index:data.index,revision:data.revision,system:data.system,
    word_kind:data.word_kind,before:data.before,after:data.after,
    before_meridians:data.before_meridians,after_meridians:data.after_meridians,
    before_punctures:data.before_punctures,after_punctures:data.after_punctures,
    before_endpoints:data.before_endpoints,after_endpoints:data.after_endpoints};
  $('save-prefix').disabled=false;
  const changed=data.before.filter((word,i)=>word.length!==data.after[i].length||
   word.some((letter,j)=>letter!==data.after[i][j])).length;
  $('prefix-status').textContent=`Prefix through ${data.factor}; all six ${system==='chain'?'chain-edge boundary words':'based meridian images'} computed exactly. ${changed} of 6 changed.`;
  for(const side of ['before','after']){
   const drawing=$(`prefix-${side}`);
   if(data[`${side}_svg`]){prefixSvgs[side]=data[`${side}_svg`];drawing.innerHTML=prefixSvgs[side];$(`save-prefix-${side}`).disabled=false;}
   else offerArcGallery(side,index,revision,request,data[`${side}_warning`]);
  }
  setPrefixFit(prefixFit);
  for(let i=0;i<6;i++){
   const row=document.createElement('div');row.className='prefix-row';
   const label=document.createElement('button');label.className='trace-arc';
   label.textContent=`${system==='chain'?'e':'x'}${i+1}`;label.style.borderColor=prefixColors[i];
   label.title=`Trace ${label.textContent} in both drawings`;label.setAttribute('aria-pressed','false');
   label.onclick=()=>tracePrefix(i);row.append(label);
   for(const side of ['before','after']){
    const cell=document.createElement('div');cell.className='prefix-cell';
    const dot=document.createElement('span');dot.className='prefix-dot';dot.style.background=prefixColors[i];
    dot.textContent=String(data[`${side}_punctures`][i]);
    const word=data[side][i],shown=word.slice(0,64).join(' '),endpoints=data[`${side}_endpoints`][i];
    const copy=document.createElement('span');copy.className='full-word';
    const wordLabel=system==='chain'?`${side} ${endpoints[0]||'rim'}→${endpoints[1]}`:side;
    copy.textContent=`${wordLabel}: ${shown}${word.length>64?' …':''} (${word.length} letters)`;
    const view=document.createElement('button');view.textContent='View arc';
    view.setAttribute('aria-label',`View ${side} arc ${system==='chain'?'e':'x'}${i+1} after ${data.factor}`);
    view.onclick=()=>showArc(side,i,index,revision);
    cell.append(dot,copy,view);row.append(cell);
   }
   const difference=document.createElement('div');difference.className='prefix-diff';
   difference.textContent=prefixWordChange(data.before[i],data.after[i]);
   const compare=document.createElement('button');compare.textContent='Compare arcs';
   compare.setAttribute('aria-label',`Compare before and after arc ${system==='chain'?'e':'x'}${i+1} after ${data.factor}`);
   compare.onclick=()=>showCompareArc(i,index,revision);
   difference.append(compare);row.append(difference);
   $('prefix-rows').append(row);
  }
 }catch(error){if(request===prefixRequest)$('prefix-status').textContent=error.message;}
}
async function showCompareArc(arcIndex,index,revision){
 if(!prefixExport||prefixExport.index!==index||prefixExport.revision!==revision)return;
 const request=++compareRequest;compareSvgs={};
 const factor=prefixExport.factor;
 const chain=prefixExport.system==='chain',edge=`${chain?'e':'x'}${arcIndex+1}`;
 $('compare-title').textContent=`${factor} · exact arc ${edge} before and after`;
 compareDialog.querySelector('p').textContent=chain?
  'These are individually routed images of one chain edge before and after the factor. Each edge is checked against its exact two-point neighborhood-boundary class (the first edge uses its based meridian). The pair does not check a joint six-edge placement.':
  'These are two individually routed exact meridian arcs. Their full based images are checked separately; the pair does not depict or check a joint six-arc placement.';
 $('compare-diff').textContent=prefixWordChange(prefixExport.before[arcIndex],prefixExport.after[arcIndex]);
 for(const side of ['before','after']){
  $(`compare-${side}`).textContent='Routing exact arc…';
  $(`save-compare-${side}`).disabled=true;
 }
 $('compare-status').textContent='Routing two individual exact arcs…';
 if(!compareDialog.open)compareDialog.showModal();
 let drawn=0;
 for(const side of ['before','after']){
  try{
   const response=await fetch(`/api/prefix-arc?index=${index}&side=${side}&arc=${arcIndex}&revision=${revision}&system=${prefixExport.system}`);
   const data=await response.json();
   if(request!==compareRequest)return;
   if(!response.ok)throw new Error(data.error);
   if(state.revision!==revision)throw new Error('The factorization changed; reopen the prefix inspector.');
   if(data.svg){
    compareSvgs[side]=data.svg;$(`compare-${side}`).innerHTML=data.svg;
    $(`save-compare-${side}`).disabled=false;drawn++;
    setCompareFit(compareFit);
   }else $(`compare-${side}`).textContent=`Drawing unavailable: ${data.warning}`;
  }catch(error){
   if(request!==compareRequest)return;
   $(`compare-${side}`).textContent=`Drawing unavailable: ${error.message}`;
  }
  $('compare-status').textContent=`${drawn} of 2 individual exact arcs drawn. Exact ${chain?'neighborhood-boundary words':'based images'}: before ${prefixExport.before[arcIndex].length} letters, after ${prefixExport.after[arcIndex].length} letters. Joint placement is a separate check.`;
 }
}
async function showArc(side,arcIndex,index,revision){
 if(arcIndex<0||arcIndex>=6)return;
 const chain=prefixExport?.system==='chain',edge=`${chain?'e':'x'}${arcIndex+1}`;
 arcSelection={side,arcIndex,index,revision};
 const request=++arcRequest;arcSvg='';$('save-arc').disabled=true;
 $('arc-title').textContent=`${side} ${state.factors[index].id} · individual arc ${edge}`;
 arcDialog.querySelector('p').textContent=chain?
  'This chain edge is recovered from its exact two-point neighborhood-boundary class (the first edge uses a based meridian). Its individual drawing does not check joint six-edge placement.':
  'This is one exact based meridian arc. Its ray word is checked against the full meridian image. A single-arc drawing does not verify that all six arcs are jointly disjoint or form a cut system.';
 $('arc-previous').disabled=arcIndex===0;$('arc-next').disabled=arcIndex===5;
 $('arc-toggle').textContent=`Show ${side==='before'?'after':'before'}`;
 $('arc-status').textContent='Routing one exact arc…';
 $('arc-word').textContent='';$('arc-word-summary').textContent='Full based image';
 $('arc-drawing').replaceChildren();if(!arcDialog.open)arcDialog.showModal();
 try{
  const response=await fetch(`/api/prefix-arc?index=${index}&side=${side}&arc=${arcIndex}&revision=${revision}&system=${prefixExport.system}`);
  const data=await response.json();if(request!==arcRequest)return;
  if(!response.ok)throw new Error(data.error);
  if(state.revision!==revision)throw new Error('The factorization changed; reopen the prefix inspector.');
  $('arc-word-summary').textContent=`Full ${chain?'neighborhood-boundary word':'based image'} ${edge} (${data.image.length} letters)`;
  $('arc-word').textContent=`${edge} → ${data.image.join(' ')}`;
  if(data.svg){arcSvg=data.svg;$('arc-drawing').innerHTML=arcSvg;$('save-arc').disabled=false;
   setArcFit(arcFit);
   $('arc-status').textContent='Exact individual arc drawn. Joint cut-system routing remains a separate check.';}
  else{$('arc-drawing').textContent=`Drawing unavailable: ${data.warning}`;
   $('arc-status').textContent='The exact based image is still available below.';}
 }catch(error){if(request===arcRequest)$('arc-status').textContent=error.message;}
}
$('prefix-previous').onclick=()=>showPrefix(prefixIndex-1);
$('prefix-next').onclick=()=>showPrefix(prefixIndex+1);
$('prefix-fit').onclick=()=>setPrefixFit(!prefixFit);
$('prefix-start').onclick=()=>positionPrefix(0);
$('prefix-middle').onclick=()=>positionPrefix(.5);
$('prefix-end').onclick=()=>positionPrefix(1);
$('save-prefix').onclick=()=>{if(prefixExport)download(JSON.stringify(prefixExport,null,2),'application/json','prefix-action.json');};
for(const side of ['before','after'])$(`save-prefix-${side}`).onclick=()=>{if(prefixSvgs[side])download(prefixSvgs[side],'image/svg+xml',`cut-system-${side}.svg`);};
$('close-prefix').onclick=()=>{prefixRequest++;$('prefix-inspector').close();};
$('sphere').onclick=async()=>{
 const revision=state.revision;sphereExport=null;sphereChartSvg='';$('save-sphere').disabled=true;$('save-sphere-chart').disabled=true;
 $('sphere-status').textContent='Computing the exact sphere-quotient action…';
 $('sphere-disk').textContent='';$('sphere-whisker').textContent='';$('sphere-equations').replaceChildren();$('sphere-chart').replaceChildren();
 $('sphere-inspector').showModal();
 try{
  const response=await fetch(`/api/sphere?revision=${revision}`),data=await response.json();
  if(!response.ok)throw new Error(data.error);
  if(state.revision!==revision)throw new Error('The factorization changed; reopen this check.');
  sphereExport={certified:data.certified,conjugator:data.conjugator,images:data.images,
    expected:data.expected,disk_identity:data.disk_identity,revision:data.revision};
  $('save-sphere').disabled=false;
  $('sphere-status').textContent=data.certified?
   'Certified: all six sphere meridian images are one common inner conjugation. The sphere outer action is the identity.':
   'No common inner-action certificate was found; this check makes no identity claim.';
  $('sphere-disk').textContent=data.disk_identity?
   'The six-point disk action is also the identity.':
   'The six-point disk action is not the identity; the sphere relation changes the result.';
  $('sphere-whisker').textContent=data.certified?`Common whisker w (${data.conjugator.length} letters): ${data.conjugator.join(' ')||'identity'}`:'';
  if(data.chart_svg){sphereChartSvg=data.chart_svg;$('sphere-chart').innerHTML=sphereChartSvg;$('save-sphere-chart').disabled=false;}
  else $('sphere-chart').textContent=`Identity chart unavailable: ${data.chart_warning}`;
  for(let i=0;i<6;i++){
   const row=document.createElement('p');row.className='full-word';
   const word=data.images[i],core=i<5?`x${i+1}`:'(x1 x2 x3 x4 x5)⁻¹';
   row.textContent=`x${i+1} → ${word.slice(0,48).join(' ')}${word.length>48?' …':''} (${word.length} letters)`+
    (data.certified?` = w · ${core} · w⁻¹ ✓`:'');
   $('sphere-equations').append(row);
  }
 }catch(error){$('sphere-status').textContent=error.message;}
};
$('save-sphere').onclick=()=>{if(sphereExport)download(JSON.stringify(sphereExport,null,2),'application/json','sphere-action-certificate.json');};
$('save-sphere-chart').onclick=()=>{if(sphereChartSvg)download(sphereChartSvg,'image/svg+xml','sphere-identity-cut-system.svg');};
$('close-sphere').onclick=()=>$('sphere-inspector').close();
$('zoom').onchange=inspectZoom;
$('close-inspector').onclick=()=>$('inspector').close();
$('undo').onclick=()=>action({op:'undo'});$('redo').onclick=()=>action({op:'redo'});$('reset').onclick=()=>action({op:'reset'},0);
$('simplify').onclick=()=>action({op:'simplify'});
$('conjugate').onclick=async()=>{
 const raw=$('global-word').value.trim(),parts=raw?raw.split(/[\s,]+/):[];
 if(parts.length>80||parts.some(part=>!/^[-+]?[1-5]$/.test(part))){status('Enter at most 80 signed braid generators from 1 to 5.',true);return;}
 const revision=state.revision;
 await action({op:'conjugate',word:parts.map(Number)});
 if(state.revision!==revision)$('global-word').value='';
};
$('global-word').onkeydown=event=>{if(event.key==='Enter')$('conjugate').click();};
$('split').onclick=()=>action({op:'split',index:selected,kind:$('split-kind').value});$('combine').onclick=()=>action({op:'combine',index:selected});
$('save').onclick=()=>download(JSON.stringify(state.export,null,2),'application/json','six-seven-factorization.json');
$('open').onclick=()=>$('file').click();
$('file').onchange=async()=>{try{const file=$('file').files[0];if(!file)return;if(file.size>250000)throw new Error('Choose a JSON file smaller than 250 KB');const document=JSON.parse(await file.text());await action({op:'import',document},0);}catch(e){status(e.message,true);}finally{$('file').value='';}};
$('svg').onclick=async()=>{
 if(busy||!state)return;
 try{const response=await fetch('/api/export.svg?revision='+state.revision);
  if(!response.ok){const data=await response.json();throw new Error(data.error);}
  download(await response.text(),'image/svg+xml','six-seven-factorization.svg');
 }catch(error){status(error.message,true);}
};
fetch('/api/state').then(r=>{if(!r.ok)throw new Error('Could not load the lab');return r.json();}).then(data=>{state=data;paint();}).catch(e=>status(e.message,true));
