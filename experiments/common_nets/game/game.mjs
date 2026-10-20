import {fold,alignments,sameSurface,snap,clamp,nextStop} from './geometry.mjs';
import {View} from './renderer.mjs';
const $=id=>document.getElementById(id),rad=Math.PI/180;
const basePairs=['qa','ws','ed','rf','tg','yh','uj','ik','ol','pz','xc','vb','nm'];
const pairs=[...basePairs.map(s=>s.split('')),...basePairs.slice(0,4).map(s=>s.toUpperCase().split(''))];
const keyName=k=>k===k.toUpperCase()?'Shift+'+k:k.toUpperCase();
const shortKey=k=>k===k.toUpperCase()?'⇧'+k:k.toUpperCase();
let data,net,target,angles=[],selected=0,candidates=[],history=[],future=[],assisted=false,serial=0;
let paper,goal,solved={},saved={},storage=true,checkTimer,wheelTimer,working=false;
try{
  const read=key=>{const v=JSON.parse(localStorage.getItem(key)||'{}');return v&&typeof v==='object'&&!Array.isArray(v)?v:{};};
  solved=read('tetra-fold-solved-v1');saved=read('tetra-fold-progress-v1');
}catch{storage=false;}
const challengeKey=()=>net.id+'/'+target.id;
function persist(){
  saved[challengeKey()]={angles:[...angles],selected,assisted};
  try{localStorage.setItem('tetra-fold-progress-v1',JSON.stringify(saved));localStorage.setItem('tetra-fold-solved-v1',JSON.stringify(solved));}catch{storage=false;}
}
function progress(){
  const total=data.puzzles.reduce((s,p)=>s+p.targets.length,0);
  $('progress').textContent=Object.values(solved).filter(Boolean).length+' / '+total+' solved'+(storage?'':' (storage unavailable)');
  net.targets.forEach((t,i)=>{$('target').options[i].text=t.id+(solved[net.id+'/'+t.id]?' ✓':'');});
}
function answerColors(){return net.faces.map((_,i)=>{
  const h=((i*137.508+205)%360)/60,c=.59*(1-Math.abs(2*.74-1)),x=c*(1-Math.abs(h%2-1)),m=.74-c/2;
  const a=h<1?[c,x,0]:h<2?[x,c,0]:h<3?[0,c,x]:h<4?[0,x,c]:h<5?[x,0,c]:[c,0,x];return a.map(v=>v+m);
});}
function overlay(){
  if(!paper.faces.length)return;
  const canvas=$('hinge-overlay'),r=Math.min(2,devicePixelRatio||1),ctx=canvas.getContext('2d');canvas.width=canvas.clientWidth*r;canvas.height=canvas.clientHeight*r;ctx.scale(r,r);
  net.hinges.forEach(([a,b,e],i)=>{
    const p=paper.project(paper.faces[a][e]),q=paper.project(paper.faces[a][(e+1)%3]),active=i===selected;
    ctx.beginPath();ctx.moveTo(...p.slice(0,2));ctx.lineTo(...q.slice(0,2));ctx.strokeStyle=active?'#e49a22':'#277f98a0';ctx.lineWidth=active?4:1.2;ctx.setLineDash(active?[]:[4,3]);ctx.stroke();ctx.setLineDash([]);
    if(active||$('labels').checked){
      const x=(p[0]+q[0])/2,y=(p[1]+q[1])/2,label='H'+(i+1);ctx.font='bold 12px system-ui';const w=ctx.measureText(label).width;
      ctx.fillStyle=active?'#fff0c5':'#ffffffdd';ctx.fillRect(x-w/2-5,y-9,w+10,18);ctx.fillStyle='#24434c';ctx.textAlign='center';ctx.fillText(label,x,y+4);
    }
  });
}
function setSelection(i){
  selected=i;$('hinge-name').textContent='Hinge '+(i+1)+' · '+pairs[i].map(keyName).join(' / ');
  $('angle').value=angles[i]/rad;$('angle-value').textContent=(angles[i]/rad).toFixed(1)+'°';
  document.querySelectorAll('.hinge').forEach((b,j)=>{b.setAttribute('aria-pressed',String(j===i));b.querySelector('output').textContent=(angles[j]/rad).toFixed(1)+'°';});
  overlay();
}
function status(){
  const won=sameSurface(paper.faces,candidates);
  const box=$('feedback');box.className='feedback'+(assisted?' answer':won?' solved':'');
  box.textContent=assisted?'Solution revealed. Start flat to solve this challenge yourself.':won?'Solved! Your folded surface matches '+target.id+'.':solved[challengeKey()]?'Previously solved. You can try a different folding.':'Fold the net to match the target. Colors do not need to match.';
  if(won&&!assisted){solved[challengeKey()]=true;persist();progress();}
}
function draw(){
  paper.setMesh(fold(net,angles),assisted?answerColors():net.colors);setSelection(selected);
  clearTimeout(checkTimer);checkTimer=setTimeout(status,90);
  $('undo').disabled=!history.length;$('redo').disabled=!future.length;
}
function record(){history.push([...angles]);if(history.length>200)history.shift();future=[];}
function change(i,value,remember=true){
  if(working)return;if(remember)record();angles[i]=clamp(value);selected=i;draw();persist();
}
function settle(){
  if($('snap').checked)angles=angles.map(a=>snap(a));draw();persist();
}
function nudge(i,direction,remember=true){change(i,$('snap').checked?nextStop(angles[i],direction):angles[i]+direction*2*rad,remember);}
function startTarget(){
  serial++;working=false;clearTimeout(checkTimer);clearTimeout(wheelTimer);
  target=net.targets[Number($('target').value)];const old=saved[challengeKey()];
  angles=Array.isArray(old?.angles)&&old.angles.length===net.hinges.length&&old.angles.every(Number.isFinite)?old.angles.map(clamp):net.hinges.map(()=>0);
  selected=Number.isInteger(old?.selected)?Math.max(0,Math.min(net.hinges.length-1,old.selected)):0;
  assisted=Boolean(old?.assisted);history=[];future=[];
  candidates=alignments(target.faces,net.faces[0]);
  $('feedback').className='feedback';$('feedback').textContent='Fold the net to match the target. Colors do not need to match.';
  $('target-name').textContent=target.id;$('target-caption').textContent=assisted?'Solution colors now match the net panels.':'Warm colors are independent: they give no folding key.';
  goal.setMesh(target.faces,assisted?answerColors():target.colors);draw();progress();
  const hash=net.id+'/'+target.id;window.history.replaceState(null,'','#'+hash);
}
function startNet(index,targetId){
  net=data.puzzles[index];$('net').value=String(index);
  $('target').replaceChildren(...net.targets.map((t,i)=>new Option(t.id+(solved[net.id+'/'+t.id]?' ✓':''),i)));
  $('target').value=String(Math.max(0,net.targets.findIndex(t=>t.id===targetId)));
  $('hinges').replaceChildren(...net.hinges.map((_,i)=>{
    const b=document.createElement('button');b.className='hinge';b.dataset.hinge=i;b.setAttribute('aria-label','Select hinge '+(i+1));
    const label=document.createElement('span');label.textContent='H'+(i+1);const keys=document.createElement('kbd');keys.textContent=pairs[i].map(shortKey).join('/');
    b.append(label,keys,document.createElement('output'));b.onclick=()=>{setSelection(i);persist();};return b;
  }));startTarget();
}
function animateSolution(){
  if(working)return;record();assisted=true;working=true;const ticket=++serial,from=[...angles],start=performance.now();
  goal.setMesh(target.faces,answerColors());$('target-caption').textContent='Solution colors now match the net panels.';
  function frame(now){
    if(ticket!==serial)return;const t=Math.min(1,(now-start)/1100),ease=t*t*(3-2*t);
    angles=from.map((v,i)=>v+(target.angles[i]-v)*ease);draw();
    if(t<1)requestAnimationFrame(frame);else{working=false;status();persist();}
  }requestAnimationFrame(frame);
}
async function init(){
  const response=await fetch('data.json');if(!response.ok)throw Error('Could not load puzzle data ('+response.status+'). Please reload.');data=await response.json();
  paper=new View($('paper'));goal=new View($('goal'));paper.pitch=1.05;paper.onDraw=overlay;
  $('net').replaceChildren(...data.puzzles.map((p,i)=>new Option(p.id+' · '+p.units+' units · '+p.targets.length+' targets',i)));
  const initial=decodeURIComponent(location.hash.slice(1)).split('/');
  startNet(Math.max(0,data.puzzles.findIndex(p=>p.id===initial[0])),initial[1]);
  $('net').onchange=()=>startNet(Number($('net').value));$('target').onchange=startTarget;
  function move(step){$('target').value=String((Number($('target').value)+step+net.targets.length)%net.targets.length);startTarget();}
  $('previous').onclick=()=>move(-1);$('next').onclick=()=>move(1);
  $('random').onclick=()=>{const index=Math.floor(Math.random()*net.targets.length);$('target').value=String(index);startTarget();};
  $('labels').onchange=overlay;
  $('angle').addEventListener('pointerdown',record);
  $('angle').addEventListener('keydown',e=>{if(!e.repeat&&e.key.startsWith('Arrow'))record();});
  $('angle').oninput=()=>change(selected,Number($('angle').value)*rad,false);$('angle').onchange=settle;
  $('increase').onclick=()=>nudge(selected,1);$('decrease').onclick=()=>nudge(selected,-1);
  $('paper').addEventListener('dblclick',e=>{const box=$('paper').getBoundingClientRect(),i=paper.pickHinge(net.hinges,e.clientX-box.left,e.clientY-box.top);if(i>=0){setSelection(i);persist();}});
  $('paper').addEventListener('wheel',e=>{e.preventDefault();if(!wheelTimer)record();nudge(selected,Math.sign(-e.deltaY),false);clearTimeout(wheelTimer);wheelTimer=setTimeout(()=>{wheelTimer=null;settle();},180);},{passive:false});
  window.addEventListener('keydown',e=>{
    if(e.ctrlKey||e.metaKey||e.altKey||e.target.closest('input,select,textarea'))return;
    const key=e.shiftKey?e.key.toUpperCase():e.key.toLowerCase();
    const i=pairs.slice(0,net.hinges.length).findIndex(pair=>pair.includes(key));
    if(i<0)return;e.preventDefault();nudge(i,pairs[i][0]===key?1:-1,!e.repeat);
  });
  window.addEventListener('keyup',e=>{if(pairs.slice(0,net.hinges.length).some(pair=>pair.includes(e.key)||pair.includes(e.key.toLowerCase())))settle();});
  $('undo').onclick=()=>{if(!history.length)return;future.push([...angles]);angles=history.pop();draw();persist();};
  $('redo').onclick=()=>{if(!future.length)return;history.push([...angles]);angles=future.pop();draw();persist();};
  $('flat').onclick=()=>{serial++;working=false;record();angles=angles.map(()=>0);assisted=false;goal.setMesh(target.faces,target.colors);$('target-caption').textContent='Warm colors are independent: they give no folding key.';draw();persist();};
  $('camera').onclick=()=>{paper.yaw=goal.yaw=.7;paper.pitch=1.05;goal.pitch=.65;paper.draw();goal.draw();};
  $('solution').onclick=animateSolution;
  window.addEventListener('resize',()=>{paper.draw();goal.draw();});$('loading').hidden=true;
}
init().catch(error=>{$('loading').replaceChildren();const p=document.createElement('p');p.textContent=error.message+' The puzzle book PDF is also available from the link above.';const close=document.createElement('button');close.textContent='Show PDF link';close.onclick=()=>$('loading').hidden=true;$('loading').append(p,close);console.error(error);});
