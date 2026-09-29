'use strict';
let state,selected=0,busy=false,dragged=null;
const $=id=>document.getElementById(id);
const status=(text,error=false)=>{ $('status').textContent=text; $('status').classList.toggle('error',error); };
function controls(){
 const f=state?.factors[selected];
 $('undo').disabled=busy||!state?.undo; $('redo').disabled=busy||!state?.redo;
 for(const id of ['reset','save','open','svg']) $(id).disabled=busy||!state;
 $('selected').textContent=f?`${f.id} · ${f.label}`:'Select a factor';
 const picker=$('split-kind');picker.replaceChildren();
 for(const [value,label] of f?.splits||[]){const o=document.createElement('option');o.value=value;o.textContent=label;picker.append(o);}
 if(!picker.options.length){const o=document.createElement('option');o.textContent='No available split';picker.append(o);}
 picker.disabled=busy||!f?.splits.length;$('split').disabled=picker.disabled;
 $('combine').disabled=busy||!f||selected>=state.factors.length-1;
 $('inspect').disabled=busy||!f;
}
function choose(index){selected=index;document.querySelectorAll('.factor').forEach((el,i)=>el.classList.toggle('selected',i===selected));controls();}
function paint(){
 $('storage-status').textContent=state.persistent?'Workspace and undo history saved to session file.':'Session is in memory. Save JSON before stopping the server.';
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
  card.append(head,support,word);card.onclick=()=>choose(i);card.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();choose(i);}};
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
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
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
 $('zoom').value='1';inspectZoom();$('inspector').showModal();
 $('inspect-viewport').scrollTo(0,0);
};
$('zoom').onchange=inspectZoom;
$('close-inspector').onclick=()=>$('inspector').close();
$('undo').onclick=()=>action({op:'undo'});$('redo').onclick=()=>action({op:'redo'});$('reset').onclick=()=>action({op:'reset'},0);
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
