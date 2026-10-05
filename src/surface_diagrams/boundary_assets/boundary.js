'use strict';
let state=null,selected=0,busy=false,dragged=null;
const $=id=>document.getElementById(id);
const showStatus=(message,error=false)=>{
  $('status').textContent=message;
  $('status').classList.toggle('error',error);
};

function controls(){
  const factor=state?.factors[selected];
  for(const id of ['points','power','new','example','save','open','svg'])$(id).disabled=busy||!state;
  $('undo').disabled=busy||!state?.undo;
  $('redo').disabled=busy||!state?.redo;
  $('selected').textContent=factor?`${factor.id} · ${factor.label}`:'Select a factor';
  const picker=$('split-kind');picker.replaceChildren();
  for(const [kind,label] of factor?.splits||[]){
    const option=document.createElement('option');option.value=kind;option.textContent=label;picker.append(option);
  }
  if(!picker.options.length){const option=document.createElement('option');option.textContent='No available substitution';picker.append(option);}
  picker.disabled=busy||!factor?.splits.length;
  $('split').disabled=picker.disabled;
  $('combine').disabled=busy||!factor||selected>=state.factors.length-1;
  document.querySelectorAll('#history-list button').forEach(button=>
    button.disabled=busy||Number(button.dataset.position)===state?.position);
}

function choose(index){
  selected=index;
  document.querySelectorAll('.factor').forEach((card,i)=>card.classList.toggle('selected',i===index));
  document.querySelectorAll('.braid-row').forEach((row,i)=>row.classList.toggle('selected',i===index));
  controls();
}

function paint(){
  selected=Math.max(0,Math.min(selected,state.factors.length-1));
  $('points').value=String(state.points);$('power').value=String(state.power);
  $('count').textContent=`${state.factors.length} factors · ${state.factors.reduce((n,f)=>n+f.word.length,0)} letters`;
  $('target-status').textContent=`Target: boundary twist on ${state.points} marked points, power ${state.power} · exact B${state.points} action verified`;
  $('storage-status').textContent=window.boundaryStorageAvailable?
    'Workspace and undo history are saved in this browser. Export JSON to move the current factorization elsewhere.':
    'Browser storage is unavailable; export JSON before closing this page.';
  $('history-summary').textContent=`Exploration history · step ${state.position+1} of ${state.steps.length}`;
  $('history-list').replaceChildren();
  state.steps.forEach((label,position)=>{
    const item=document.createElement('li');item.classList.toggle('current',position===state.position);
    const button=document.createElement('button');button.textContent=label;
    button.dataset.position=String(position);
    button.onclick=()=>action({op:'seek',position},0);
    item.append(button);$('history-list').append(item);
  });
  $('factors').replaceChildren();
  state.factors.forEach((factor,index)=>{
    const card=document.createElement('article');card.className='factor';card.tabIndex=0;
    card.draggable=true;card.style.height=factor.height+'px';
    card.setAttribute('aria-label',`${factor.id}, ${factor.label}, factor ${index+1}`);
    const head=document.createElement('div');head.className='factor-head';
    const title=document.createElement('span');
    const name=document.createElement('strong');name.textContent=factor.id;
    const kind=document.createElement('span');kind.className='kind';kind.textContent=factor.label;
    title.append(name,kind);
    const arrows=document.createElement('span');arrows.className='row-buttons';
    for(const [label,delta] of [['↑',-1],['↓',1]]){
      const button=document.createElement('button');button.textContent=label;
      button.disabled=index+delta<0||index+delta>=state.factors.length;
      button.setAttribute('aria-label',`Move ${factor.id} ${delta<0?'up':'down'}`);
      button.onclick=event=>{event.stopPropagation();choose(index);
        action({op:'move',index,target:index+delta},index+delta);};
      arrows.append(button);
    }
    head.append(title,arrows);
    const support=document.createElement('div');support.className='support';
    if(factor.svg)support.innerHTML=factor.svg;
    else{const warning=document.createElement('p');warning.className='warning';
      warning.textContent=factor.warning||'Support drawing unavailable';support.append(warning);}
    const word=document.createElement('div');word.className='word';
    word.textContent=factor.word.join(' ');word.title=word.textContent;
    card.append(head,support,word);
    card.onclick=()=>choose(index);
    card.onkeydown=event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();choose(index);}};
    card.ondragstart=event=>{if(busy){event.preventDefault();return;}
      dragged=index;choose(index);event.dataTransfer.setData('text/plain',String(index));
      event.dataTransfer.effectAllowed='move';card.classList.add('dragging');};
    card.ondragover=event=>{if(dragged===null||busy)return;
      event.preventDefault();event.dataTransfer.dropEffect='move';card.classList.add('drop-target');};
    card.ondragleave=()=>card.classList.remove('drop-target');
    card.ondrop=event=>{event.preventDefault();card.classList.remove('drop-target');
      const source=dragged;dragged=null;if(source!==null&&source!==index)
        action({op:'move',index:source,target:index},index);};
    card.ondragend=()=>{dragged=null;document.querySelectorAll('.dragging,.drop-target')
      .forEach(element=>element.classList.remove('dragging','drop-target'));};
    $('factors').append(card);
  });
  $('braid').innerHTML=state.braid;
  choose(selected);showStatus(state.message);
}

async function action(payload,next=selected){
  if(busy||!state)return;
  busy=true;document.body.classList.add('busy');controls();
  showStatus('Checking the complete braid action and redrawing…');
  try{
    const response=await fetch('/api/action',{method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({...payload,revision:state.revision})});
    const data=await response.json();
    if(!response.ok)throw new Error(data.error||'The operation failed');
    state=data;selected=next;paint();
  }catch(error){showStatus(error.message,true);}
  finally{busy=false;document.body.classList.remove('busy');controls();}
}

function download(content,type,name){
  const url=URL.createObjectURL(new Blob([content],{type}));
  const link=document.createElement('a');link.href=url;link.download=name;link.click();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
}

$('new').onclick=()=>action({op:'new',points:Number($('points').value),power:Number($('power').value)},0);
$('example').onclick=()=>action({op:'example'},0);
$('undo').onclick=()=>action({op:'undo'},0);
$('redo').onclick=()=>action({op:'redo'},0);
$('split').onclick=()=>action({op:'split',index:selected,kind:$('split-kind').value},selected);
$('combine').onclick=()=>action({op:'combine',index:selected},selected);
$('save').onclick=()=>download(JSON.stringify(state.export,null,2),'application/json',
  `boundary-twist-${state.points}-points.json`);
$('open').onclick=()=>$('file').click();
$('file').onchange=async event=>{
  const file=event.target.files?.[0];if(!file)return;
  try{const document=JSON.parse(await file.text());await action({op:'import',document},0);}
  catch(error){showStatus(error.message,true);}
  event.target.value='';
};
$('svg').onclick=async()=>{
  try{const response=await fetch('/api/export.svg');
    if(!response.ok){const data=await response.json();throw new Error(data.error);}
    download(await response.text(),'image/svg+xml',`boundary-twist-${state.points}-points.svg`);
  }catch(error){showStatus(error.message,true);}
};

fetch('/api/state').then(async response=>{
  const data=await response.json();if(!response.ok)throw new Error(data.error);
  state=data;paint();
}).catch(error=>showStatus(error.message,true));
