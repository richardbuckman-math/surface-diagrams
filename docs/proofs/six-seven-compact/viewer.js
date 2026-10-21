/* Precalculated mathematical states; only presentation assembly runs here. */
let D,A,index=0,renderRevision=0;
const $=id=>document.getElementById(id),urls={supports:[]},images={supports:[],braids:[]},chunks=new Map();
const word=w=>w.length?w.join(' '):'identity';
const replayUrl=path=>path+'?v='+encodeURIComponent(document.documentElement.dataset.replayVersion||'source');
const simple=()=>$('route').value==='simplification';
const forward=()=>simple()||$('direction').value==='forward';
const current=()=>simple()?D.simplification:(forward()?D.forward:D);
const states=()=>simple()?D.simplification.states:D.states;
const stateAt=n=>states()[simple()||!forward()?n:D.states.length-1-n];
const steps=()=>current()[$('mode').value];
function picture(kind,i){
 if(!urls[kind][i])urls[kind][i]=URL.createObjectURL(new Blob([images[kind][i]],{type:'image/svg+xml'}));
 return urls[kind][i];
}
function ensurePictures(selected){
 const needed=new Set();
 for(const s of selected)for(const i of s.factors){
  const r=D.rows[i];
  for(const [kind,id] of [['supports',r.support],['braids',r.braid]])needed.add(kind+'-'+Math.floor(id/A.chunk_size));
 }
 return Promise.all([...needed].map(key=>{
  if(!chunks.has(key)){
   const split=key.lastIndexOf('-'),kind=key.slice(0,split),n=Number(key.slice(split+1));
   chunks.set(key,fetch(replayUrl('assets/'+key+'.json')).then(r=>{
    if(!r.ok)throw Error('Could not load '+key);return r.json();
   }).then(items=>items.forEach((svg,i)=>{images[kind][n*A.chunk_size+i]=svg;}))
    .catch(error=>{chunks.delete(key);throw error;}));
  }
  return chunks.get(key);
 }));
}
function factorRow(i){
 const r=D.rows[i],support=picture('supports',r.support);
 return `<div class="factor${r.inverse?' inverse':''}" style="height:${r.height}px"><div class="label" title="${r.id}"><b>${r.id}</b> · ${r.label} · ${r.cuts} cut visits ${r.sphere_rechart?'<span class="tag sphere">SPHERE MOVE</span>':''}</div><a href="${support}" target="_blank" rel="noopener"><img class="support" loading="lazy" alt="Support of ${r.id}" src="${support}"></a></div>`;
}
function column(n,title){
 const s=stateAt(n),recharts=s.factors.filter(i=>D.rows[i].sphere_rechart);
 const braid=connectedBraid.assemble(s.factors.map(i=>D.rows[i]),images.braids);
 const frameText=simple()?'The cumulative product is conjugated by g; disk Hurwitz moves and disk support normalizations are also recorded.':'Displayed supports represent g F g inverse. The exact telescoping word check passes.';
 return `<section class="column" data-state="${n}"><h2>${title}</h2><p class="meta">State ${n} · ${s.factors.length} factors · maximum ${s.max_cuts} cut visits</p><details><summary>Global conjugation: ${s.frame.length} letters</summary><pre>g = ${word(s.frame)}</pre><p>${frameText}</p></details><details><summary>${recharts.length} explicit SPHERE support recharts</summary><p>${recharts.length?'Yellow rows identify every sphere replacement; all discrepancies and +I lift checks are retained.':'Each pictured support agrees with its recorded factor in the disk.'}</p></details><button class="save-braid">Save continuous braid SVG</button><div class="aligned-factors"><div class="support-stack">${s.factors.map(factorRow).join('')}</div><div class="braid-stack">${braid.svg}</div></div></section>`;
}
function statistics(){
 if(simple()){
  const s=D.simplification.summary;
  $('statistics').textContent=`Same thirteen-factor (6,7): total conjugator length ${s.initial[0]} → ${s.final[0]}, longest ${s.initial[1]} → ${s.final[1]}, maximum support cut visits ${s.initial[3]} → ${s.final[3]}. ${s.hurwitz_moves} Hurwitz moves, ${s.global_conjugations} explicit global conjugations, and checked disk normalizations. No sphere substitutions in this simplification.`;
 }else{
  const s=D.summary;
  $('statistics').textContent=`${s.chapters} chapters · ${s.grouped_moves} grouped transitions · ${s.atomic_moves} retained atomic moves. All support pictures fit the ${s.max_displayed_cuts}-visit ceiling. The default direction starts from the original (6,7).`;
 }
}
async function render(){
 const revision=++renderRevision,list=steps(),s=list[index],overview=$('overview').checked;
 const points=overview?[0,...current().chapters.map(x=>x.end)]:[s.start,s.end];
 $('previous').disabled=true;$('next').disabled=true;$('loading').textContent='Loading the requested precalculated pictures…';$('loading').hidden=false;
 $('strip').setAttribute('aria-busy','true');
 try{await ensurePictures(points.map(stateAt));}
 catch(e){if(revision===renderRevision){$('loading').textContent='Loading failed: '+e.message;$('loading').className='error';}return;}
 if(revision!==renderRevision)return;
 $('loading').hidden=true;$('strip').setAttribute('aria-busy','false');
 $('previous').disabled=index===0;$('next').disabled=index===list.length-1;
 $('step').value=index;$('position').value=index;$('title').textContent=(index+1)+' / '+list.length+' — '+s.title;
 const atomic=current().atomic,sphere=atomic.slice(s.start,s.end).filter(x=>x.sphere);
 $('scope').className='notice'+(sphere.length?' sphere':'');
 $('scope').textContent=simple()?(s.kind==='global_conjugation'?'EXPLICIT GLOBAL CONJUGATION. Applied to all thirteen factors.':s.kind==='cyclic_hurwitz'?'EXPLICIT CYCLIC BASEPOINT CHANGE, then a disk Hurwitz move. The product is globally conjugated.':'DISK EQUALITY. Hurwitz move or exact support normalization.'):
  (s.end-s.start)+' recorded source moves. '+(sphere.length?sphere.length+' explicit SPHERE MOVES.':'These source moves are disk-exact.')+' Column frames and additional sphere support recharts are listed below.';
 $('explanation').textContent=s.explanation||'';statistics();
 $('strip').className='strip'+(overview?' overview':'');
 $('strip').innerHTML=points.map((n,i)=>(i?'<div class="arrow" aria-label="Recorded moves">→</div>':'')+column(n,overview?(i===0?(simple()||forward()?'Original (6,7)':'Positive fifty-unit source'):current().chapters[i-1].title):(i?'After':'Before'))).join('');
 $('moves').innerHTML=atomic.slice(s.start,s.end).map((m,i)=>`<li value="${s.start+i+1}"><b>${m.sphere?'SPHERE MOVE':m.kind==='cyclic_hurwitz'?'CYCLIC GLOBAL CONJUGATION + HURWITZ':m.kind==='global_conjugation'?'GLOBAL CONJUGATION':'DISK MOVE'}</b> · ${m.title}${m.sphere?'<details><summary>Disk discrepancy for this direction (sphere and +I lift checked)</summary><pre>'+word(m.reverse_disk_discrepancy)+'</pre></details>':''}</li>`).join('');
}
function choose(){
 if(simple())$('direction').value='forward';
 $('direction').disabled=simple();const list=steps();index=0;
 $('step').replaceChildren(...list.map((s,i)=>new Option((i+1)+' — '+s.title,i)));
 $('position').max=list.length-1;render();
}
$('strip').addEventListener('click',event=>{
 const button=event.target.closest('.save-braid');if(!button)return;
 const svg=button.closest('.column').querySelector('.braid-stack svg').outerHTML;
 const url=URL.createObjectURL(new Blob([svg],{type:'image/svg+xml'})),a=document.createElement('a');
 a.href=url;a.download='six-seven-continuous-braid.svg';a.click();setTimeout(()=>URL.revokeObjectURL(url),2000);
});
Promise.all(['display.json','assets-index.json'].map(p=>fetch(replayUrl(p)).then(r=>{
 if(!r.ok)throw Error('Could not load '+p);return r.json();
}))).then(([d,a])=>{
 D=d;A=a;$('content').hidden=false;choose();
 for(const id of ['route','direction','mode'])$(id).onchange=choose;
 $('previous').onclick=()=>{index--;render();};$('next').onclick=()=>{index++;render();};
 $('step').onchange=()=>{index=Number($('step').value);render();};
 $('position').oninput=()=>{index=Number($('position').value);render();};$('overview').onchange=render;
}).catch(e=>{$('loading').textContent='Loading failed: '+e.message;$('loading').className='error';});
