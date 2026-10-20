"""Publish a small graphical replay of standard-block untwisting."""
from dataclasses import asdict
from html import escape
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from surface_diagrams.standard_block_routes import standard_block_untwisting
from surface_diagrams.boundary_playground_geometry import support_svg
from surface_diagrams.mapping_classes import supported_class
from surface_diagrams.visuals import BraidDiagram


def changed_interval(before,after):
    key=lambda f:(f.id,f.word)
    left=0
    while left<min(len(before),len(after)) and key(before[left])==key(after[left]):left+=1
    right=0
    while right<min(len(before)-left,len(after)-left) and key(before[-right-1])==key(after[-right-1]):right+=1
    return left,right,before[left:len(before)-right if right else len(before)],after[left:len(after)-right if right else len(after)]


def build():
    destination=ROOT/'docs/proofs/standard-block-untwisting'
    destination.mkdir(parents=True,exist_ok=True)
    support_cache={};braid_cache={};routes={};display={};factor_cache={};markup=[]

    def factor_rows(factors):
        rows=[]
        for f in factors:
            factor_key=(f.id,f.word)
            if factor_key in factor_cache:
                rows.append(factor_cache[factor_key]);continue
            key=supported_class(f.mapping_class)
            if key not in support_cache:
                filename='support-%d.svg'%len(support_cache)
                (destination/filename).write_text(support_svg(f,6,mirror_vertical=True),encoding='utf-8')
                support_cache[key]=filename
            if f.word not in braid_cache:
                filename='braid-%d.svg'%len(braid_cache)
                (destination/filename).write_text(BraidDiagram(6,f.word,spacing=22,step=22,crossing_style='smooth',show_generators=True)._repr_svg_(),encoding='utf-8')
                braid_cache[f.word]=filename
            factor_cache[factor_key]=len(markup);rows.append(len(markup))
            markup.append('<div class="factor"><div><b>'+escape(f.id)+'</b><a href="'+support_cache[key]+'"><img alt="Half-twist arc '+escape(f.id)+'" src="'+support_cache[key]+'"></a></div>'
                '<a href="'+braid_cache[f.word]+'"><img class="braid" alt="Exact disk braid '+escape(f.id)+'" src="'+braid_cache[f.word]+'"></a></div>')
        return rows

    for name,generator in (('W0',1),('W1',5)):
        route=standard_block_untwisting(name,generator);routes[name]=route;entries=[]
        for i,stage in enumerate(route['stages']):
            before=route['stages'][i-1]['factors'] if i else stage['factors'];after=stage['factors']
            left,right,local_before,local_after=changed_interval(before,after)
            entries.append(dict(title=stage['title'],kind=stage['kind'],phase=stage['phase'],
                before=factor_rows(local_before),after=factor_rows(local_after),
                full_before=factor_rows(before),full_after=factor_rows(after),prefix=left,suffix=right,
                discrepancy=' '.join(map(str,stage.get('disk_discrepancy',()))),
                source=stage.get('source'),target=stage.get('target')))
        display[name]=dict(stages=entries,sphere_moves=route['sphere_move_count'],units=len(route['reference']),generator=generator)
    (destination/'certificate.json').write_text(json.dumps(routes,default=asdict,separators=(',',':')),encoding='utf-8')
    (destination/'display.json').write_text(json.dumps(dict(routes=display,factors=markup),separators=(',',':')),encoding='utf-8')
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Untwisting a standard block</title><style>
*{box-sizing:border-box}body{margin:0;background:#f4f7fa;color:#1c354a;font:16px/1.5 system-ui}main{max-width:1250px;margin:auto;padding:24px}h1{font-size:30px;margin:0 0 12px}a{color:#17628d}.notice{padding:14px 18px;border-left:5px solid #5686a3;background:#e8f0f7}.sphere{background:#fff1d2;border-color:#c38415}.controls{display:flex;flex-wrap:wrap;gap:14px;align-items:center;position:sticky;top:0;background:#f4f7faf5;padding:15px 0;z-index:1}select,button{font:inherit;padding:7px}#step{max-width:600px}#position{width:100%}.columns{display:grid;grid-template-columns:minmax(0,1fr) 42px minmax(0,1fr);gap:12px;align-items:start}.stack{background:white;padding:16px;border:1px solid #cad6df;border-radius:10px}.arrow{font-size:28px;padding-top:65px}.factor{display:grid;grid-template-columns:minmax(0,1fr) 140px;align-items:center;padding:10px 0;border-top:1px dotted #70a4cb;gap:10px}.factor img{display:block;width:100%;height:auto}.factor b{font-size:12px}.factor .braid{width:140px}.quiet{font-size:14px;color:#567}pre{white-space:pre-wrap;word-break:break-word}#loading{font-weight:bold}h2{font-size:20px}details{margin:20px 0}@media(max-width:650px){main{padding:12px}.columns{grid-template-columns:1fr}.arrow{padding:0;text-align:center}.factor{grid-template-columns:minmax(0,1fr) 120px}.factor .braid{width:120px}.controls{position:static}}
</style><main><h1>Untwisting a standard block</h1>
<p class="notice"><b>This is a checked reusable move, not a completed (6,7) derivation.</b> It starts with an already isolated standard block, globally conjugated by an inverse standard generator. Every subsequent arrow is a performed, checked operation. The extraction of W0 from the positive fifty-twist (6,7) intermediate remains open.</p>
<p>Each factor shows its half-twist support beside its exact disk braid. The planar picture uses a disk chart of the sphere. These are individual support pictures, not cumulative joint cut-complex certificates.</p>
<div class="controls"><label>Example <select id="block"><option value="W0">W0: 20 units, conjugated by sigma1 inverse</option><option value="W1">W1: 30 units, conjugated by sigma5 inverse</option></select></label><button id="previous">Previous</button><button id="next">Next</button><select id="step" aria-label="Move"></select><input id="position" aria-label="Move position" type="range" min="0"><label><input id="full" type="checkbox">Show entire factorizations</label></div>
<p id="loading" role="status">Loading the checked graphical replay...</p><h2 id="title"></h2><p id="scope" class="notice"></p><p id="context"></p>
<div class="columns"><section class="stack"><h2>Before</h2><div id="before"></div></section><div class="arrow" aria-label="Checked move">&#8594;</div><section class="stack"><h2>After</h2><div id="after"></div></section></div>
<details id="discrepancy"><summary>Exact disk discrepancy for this rechart</summary><p>Before braid times inverse after braid. A sphere move is not asserted to be disk equality. The full certificate includes its five-arc sphere check and genus-two lift.</p><pre id="word"></pre></details>
<details><summary>What this does</summary><ol><li>Expose the chosen half twist at the start.</li><li>Slide it through the conjugated block to remove the conjugations.</li><li>Cycle the remaining factors across it.</li><li>Restore the transported support using centrality. Check whether that equality holds in the disk; if it does not, label it as a sphere move and check the lift.</li><li>Undo the exposing moves.</li></ol><p>The W0 example needs one sphere move. The W1 example uses disk equalities throughout. T is the ten-unit palindromic block; W0=T squared and W1=(sigma1 ... sigma5) to the sixth power. T itself lifts to the deck involution, while W0 and W1 lift to identity.</p></details>
<p><a href="certificate.json">Exact replay certificate</a> | <a href="https://arxiv.org/pdf/math/0204285#page=4">Auroux, Lemmas 6-7, page 4</a></p>
<script>
let data,markup,index=0;const $=id=>document.getElementById(id),rows=ids=>ids.map(i=>markup[i]).join('')||'<p class="quiet">No factor word changes in this presentation step.</p>';function render(){const r=data[$('block').value],s=r.stages[index],full=$('full').checked; $('step').value=String(index);$('position').value=index;$('title').textContent=index+' / '+(r.stages.length-1)+' - '+s.title;const sphere=s.kind==='sphere_rewrite';$('scope').className='notice'+(sphere?' sphere':'');$('scope').textContent=sphere?'SPHERE MOVE. Exact sphere action and genus-two lift checked; disk equality fails.':s.kind==='start'?'Starting factorization. No move has been performed.':s.kind==='disk_hurwitz'?'DISK HURWITZ MOVE. The dragged factor is fixed; its neighbor changes by conjugation.':'DISK EQUALITY. The exact disk action is unchanged.';$('context').textContent=full?r.units+' factors shown on each side.':s.prefix+' unchanged factors above; '+s.suffix+' unchanged factors below. Only the changed interval is shown.';$('before').innerHTML=rows(full?s.full_before:s.before);$('after').innerHTML=rows(full?s.full_after:s.after);$('previous').disabled=index===0;$('next').disabled=index===r.stages.length-1;$('discrepancy').hidden=!s.discrepancy;$('word').textContent=s.discrepancy;}
function choose(){const r=data[$('block').value];$('step').replaceChildren(...r.stages.map((s,i)=>new Option(i+' - '+s.phase+(s.kind==='sphere_rewrite'?' - SPHERE MOVE':''),i)));$('position').max=r.stages.length-1;index=r.stages.findIndex(s=>s.phase==='centrality');render();}fetch('display.json').then(r=>{if(!r.ok)throw Error('Could not load the replay');return r.json();}).then(v=>{data=v.routes;markup=v.factors;$('loading').hidden=true;choose();$('block').onchange=choose;$('step').onchange=()=>{index=Number($('step').value);render();};$('position').oninput=()=>{index=Number($('position').value);render();};$('full').onchange=render;$('previous').onclick=()=>{index--;render();};$('next').onclick=()=>{index++;render();};}).catch(e=>{$('loading').textContent=e.message;});
</script></main></html>'''
    (destination/'index.html').write_text(html,encoding='utf-8')
    print('Saved',destination,'routes:',{k:len(v['stages']) for k,v in routes.items()},'supports:',len(support_cache),'braids:',len(braid_cache))
    return destination


if __name__=='__main__':build()
