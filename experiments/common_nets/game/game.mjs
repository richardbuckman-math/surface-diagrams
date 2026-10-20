import {fold,alignments,sameSurface,snap,clamp,nextStop,stopsFor} from './geometry.mjs?v=2';
import {View} from './renderer.mjs?v=2';
const $=id=>document.getElementById(id),rad=Math.PI/180;
const basePairs=['qa','ws','ed','rf','tg','yh','uj','ik','ol','pz','xc','vb','nm'];
const pairs=[...basePairs.map(s=>s.split('')),...basePairs.map(s=>s.toUpperCase().split('')),...['12','34','56','78','90','-=','[]'].map(s=>s.split(''))];
const shifted=k=>/[A-Z]/.test(k);
const keyName=k=>shifted(k)?'Shift+'+k:k.toUpperCase();
const shortKey=k=>shifted(k)?'⇧'+k:k.toUpperCase();
let data,net,target,angles=[],selected=0,candidates=[],history=[],future=[],assisted=false,serial=0;
let paper,goal,solved={},saved={},storage=true,checkTimer,wheelTimer,working=false;
let family='tetrahedra',familyTicket=0,netTicket=0;
const families=new Map(),netCache=new Map();
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
  const ids=new Set(data.puzzles.map(p=>p.id));
  const total=data.puzzles.reduce((s,p)=>s+(p.targets?.length??p.targetCount),0);
  const completed=Object.entries(solved).filter(([key,v])=>v&&ids.has(key.split('/')[0])).length;
  $('progress').textContent=completed+' / '+total+' solved'+(storage?'':' (storage unavailable)');
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
    const p=paper.project(paper.faces[a][e]),q=paper.project(paper.faces[a][(e+1)%paper.faces[a].length]),active=i===selected;
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
  if(working||!$('loading').hidden)return;
  if($('snap').checked)angles=angles.map(a=>snap(a,4*rad,stopsFor(net)));draw();persist();
}
function nudge(i,direction,remember=true){change(i,$('snap').checked?nextStop(angles[i],direction,stopsFor(net)):angles[i]+direction*2*rad,remember);}
function startTarget(){
  serial++;working=false;clearTimeout(checkTimer);clearTimeout(wheelTimer);
  target=net.targets[Number($('target').value)];const old=saved[challengeKey()];
  angles=Array.isArray(old?.angles)&&old.angles.length===net.hinges.length&&old.angles.every(Number.isFinite)?old.angles.map(clamp):net.hinges.map(()=>0);
  selected=Number.isInteger(old?.selected)?Math.max(0,Math.min(net.hinges.length-1,old.selected)):0;
  assisted=Boolean(old?.assisted);history=[];future=[];
  candidates=alignments(target.faces,net.faces[0],net.allowMirrors!==false);
  $('feedback').className='feedback';$('feedback').textContent='Fold the net to match the target. Colors do not need to match.';
  $('target-name').textContent=target.id;$('target-caption').textContent=assisted?'Solution colors now match the net panels.':'Warm colors are independent: they give no folding key.';
  goal.setMesh(target.faces,assisted?answerColors():target.colors);draw();progress();
  const hash=net.id+'/'+target.id;window.history.replaceState(null,'','#'+hash);
}
async function startNet(index,targetId){
  const ticket=++netTicket,descriptor=data.puzzles[index];serial++;working=false;clearTimeout(checkTimer);
  clearTimeout(wheelTimer);wheelTimer=null;
  $('net').value=String(index);
  $('loading').hidden=false;
  try{
    if(descriptor.file&&!netCache.has(descriptor.id)){
      const r=await fetch(descriptor.file);if(!r.ok)throw Error('Could not load this net. Please reload.');netCache.set(descriptor.id,await r.json());
    }
    if(ticket!==netTicket)return;
    net=descriptor.file?netCache.get(descriptor.id):descriptor;
  }catch(error){showError(error);return;}
  $('target').replaceChildren(...net.targets.map((t,i)=>new Option(t.id+(solved[net.id+'/'+t.id]?' ✓':''),i)));
  $('target').value=String(Math.max(0,net.targets.findIndex(t=>t.id===targetId)));
  $('hinges').replaceChildren(...net.hinges.map((_,i)=>{
    const b=document.createElement('button');b.className='hinge';b.dataset.hinge=i;b.setAttribute('aria-label','Select hinge '+(i+1));
    const label=document.createElement('span');label.textContent='H'+(i+1);const keys=document.createElement('kbd');keys.textContent=pairs[i].map(shortKey).join('/');
    b.append(label,keys,document.createElement('output'));b.onclick=()=>{setSelection(i);persist();};return b;
  }));
  $('net-note').textContent=net.note||'Fixed equilateral-triangle panels. Only the listed targets are claimed.';
  $('net-source').hidden=!net.source;if(net.source)$('net-source').href=net.source;
  startTarget();$('loading').hidden=true;
}
async function startFamily(kind,netId,targetId){
  const ticket=++familyTicket;netTicket++;serial++;clearTimeout(checkTimer);working=false;$('loading').hidden=false;
  try{
    if(!families.has(kind)){
      const r=await fetch(kind==='cubes'?'cubes-index.json':'data.json');if(!r.ok)throw Error('Could not load this puzzle family. Please reload.');families.set(kind,await r.json());
    }
    if(ticket!==familyTicket)return;
    family=kind;data=families.get(kind);$('family').value=kind;
    $('family-title').textContent=kind==='cubes'?' / Cubes & Cubigami':' / Tetrahedra';
    const groups=new Map();data.puzzles.forEach((p,i)=>{
      if(!groups.has(p.units)){const group=document.createElement('optgroup');group.label=p.units+' '+(kind==='cubes'?'cube':'tetrahedron')+(p.units===1?'':'s');groups.set(p.units,group);}
      groups.get(p.units).append(new Option(p.id+' · '+(p.label||p.units+' units')+' · '+(p.targetCount??p.targets.length)+' targets',i));
    });$('net').replaceChildren(...groups.values());
    $('family-note').textContent=kind==='cubes'?'Cubes, 1–8 units. Across these nets, every planar tree-shaped cluster through eight is available, plus selected spatial clusters. Each net has its own target list; no universal larger net is claimed. Chiral cube shapes count separately.':
      '11 fixed-cut nets · 321 checked challenges · 1–8 tetrahedra. The PDF also includes all 523 catalog shapes. The five-unit cobra net is known from Rick Mabry. Mirrors count once.';
    await startNet(Math.max(0,data.puzzles.findIndex(p=>p.id===(netId||(kind==='cubes'?'C4A':'P1A')))),targetId);
  }catch(error){showError(error);}
}
function downloadNet(){
  const points=net.faces.flat(),lo=[0,1].map(i=>Math.min(...points.map(p=>p[i]))),hi=[0,1].map(i=>Math.max(...points.map(p=>p[i]))),s=36;
  const xy=p=>[20+(p[0]-lo[0])*s,20+(hi[1]-p[1])*s],edgeKey=(a,b)=>JSON.stringify([a.slice(0,2),b.slice(0,2)].sort((p,q)=>p[0]-q[0]||p[1]-q[1]));
  const hinges=new Set(net.hinges.map(([a,b,e])=>edgeKey(net.faces[a][e],net.faces[a][(e+1)%net.faces[a].length]))),edges=new Map();
  const colors=assisted?answerColors():net.colors;
  let body='';net.faces.forEach((face,i)=>{
    body+='<polygon points="'+face.map(p=>xy(p).join(',')).join(' ')+'" fill="rgb('+colors[i].map(v=>Math.round(255*v)).join(',')+')"/>';
    const c=[0,1].map(j=>face.reduce((v,p)=>v+xy(p)[j],0)/face.length);body+='<text x="'+c[0]+'" y="'+(c[1]+3)+'" text-anchor="middle" font-size="9">'+(i+1)+'</text>';
    face.forEach((a,j)=>{const b=face[(j+1)%face.length],key=edgeKey(a,b),old=edges.get(key);edges.set(key,{a,b,count:(old?.count||0)+1});});
  });
  for(const [key,{a,b,count}]of edges){const p=xy(a),q=xy(b),hinge=hinges.has(key);body+='<line x1="'+p[0]+'" y1="'+p[1]+'" x2="'+q[0]+'" y2="'+q[1]+'" stroke="'+(hinge?'#1876b8':count===2?'#cc382a':'#172c3f')+'" stroke-width="'+(hinge?.8:1.1)+'"'+(hinge?' stroke-dasharray="3 2"':'')+'/>';}
  const width=40+(hi[0]-lo[0])*s,height=65+(hi[1]-lo[1])*s;
  body+='<text x="20" y="'+(height-12)+'" font-size="10">'+net.id+': black/red = cut; blue dashed = hinge.</text>';
  const url=URL.createObjectURL(new Blob(['<svg xmlns="http://www.w3.org/2000/svg" width="'+Math.max(320,width)+'" height="'+height+'" viewBox="0 0 '+Math.max(320,width)+' '+height+'"><title>Net '+net.id+'</title>'+body+'</svg>'],{type:'image/svg+xml'}));
  const a=document.createElement('a');a.href=url;a.download='fold-'+net.id+'.svg';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
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
  paper=new View($('paper'));goal=new View($('goal'));paper.pitch=1.05;paper.onDraw=overlay;
  const initial=decodeURIComponent(location.hash.slice(1)).split('/');
  await startFamily(initial[0].startsWith('C')?'cubes':'tetrahedra',initial[0],initial[1]);
  $('family').onchange=()=>startFamily($('family').value);
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
  $('paper').addEventListener('wheel',e=>{if(working||!e.deltaY)return;e.preventDefault();if(!wheelTimer)record();nudge(selected,Math.sign(-e.deltaY),false);clearTimeout(wheelTimer);wheelTimer=setTimeout(()=>{wheelTimer=null;settle();},180);},{passive:false});
  window.addEventListener('keydown',e=>{
    if(!$('loading').hidden||e.ctrlKey||e.metaKey||e.altKey||e.target.closest('input,select,textarea'))return;
    const key=e.shiftKey?e.key.toUpperCase():e.key.toLowerCase();
    const i=pairs.slice(0,net.hinges.length).findIndex(pair=>pair.includes(key));
    if(i<0)return;e.preventDefault();nudge(i,pairs[i][0]===key?1:-1,!e.repeat);
  });
  window.addEventListener('keyup',e=>{if(pairs.slice(0,net.hinges.length).some(pair=>pair.includes(e.key)||pair.includes(e.key.toLowerCase())))settle();});
  $('undo').onclick=()=>{if(!history.length)return;serial++;working=false;future.push([...angles]);angles=history.pop();draw();persist();};
  $('redo').onclick=()=>{if(!future.length)return;serial++;working=false;history.push([...angles]);angles=future.pop();draw();persist();};
  $('flat').onclick=()=>{serial++;working=false;record();angles=angles.map(()=>0);assisted=false;goal.setMesh(target.faces,target.colors);$('target-caption').textContent='Warm colors are independent: they give no folding key.';draw();persist();};
  $('camera').onclick=()=>{paper.yaw=goal.yaw=.7;paper.pitch=1.05;goal.pitch=.65;paper.draw();goal.draw();};
  $('solution').onclick=animateSolution;
  $('download-net').onclick=downloadNet;
  window.addEventListener('resize',()=>{paper.draw();goal.draw();});
}
function showError(error){$('loading').hidden=false;$('loading').replaceChildren();const p=document.createElement('p');p.textContent=error.message+' The tetrahedra book PDF is also available from the link above.';const close=document.createElement('button');close.textContent='Show PDF link';close.onclick=()=>$('loading').hidden=true;$('loading').append(p,close);console.error(error);}
init().catch(showError);
