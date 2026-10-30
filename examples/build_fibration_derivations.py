"""Build three source-exact viewers without changing any existing proof/lab."""
from pathlib import Path
from hashlib import sha256
from html import escape
from math import ceil
from dataclasses import asdict
import json,re
from surface_diagrams.small_fibration_derivations import all_derivations
from surface_diagrams.factorization_explorer import Factor
from surface_diagrams.boundary_playground_geometry import support_svg
from surface_diagrams.braid_stack import braid_fragment_svg
from surface_diagrams.visuals import RAINBOW
from examples.build_half_neighborhood_comparison import support_grid,panel,write_utf8
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/proofs/fibration-derivations'
TITLES={'6-2':'(6,2): two triple blocks and six bands','4-3':'(4,3): two cabled daisies and two half lanterns','10-10':'(10,10): three exact blocks and a separated sphere redraw'}
SCOPES={
 'start':'Start from the explicitly stated relation or assembled source. Each drawing is an individual actual support.',
 'disk_named_substitution':'DISK SUBSTITUTION. Every ordered actual input/output and the full named local proof are checked. No sphere redraw or deletion is included.',
 'disk_combine':'DISK COMBINE. The two supported twists are individually matched before their positive powers combine.',
 'disk_hurwitz_block':'DISK TRANSPORT. Every adjacent crossing is raw-reconstructed and bounded20 before the complete carry is applied; all context changes remain recorded.',
 'disk_cyclic_start':'EXPLICIT CYCLIC START. Its full inverse-prefix common word is checked free first, with independently verified output invariance.',
 'disk_parallel_cyclic':'THREE INDEPENDENT DISK CYCLIC STARTS. Each acts on a different seven-factor block from the SAME input. All literal two-order certificates are retained.',
 'construction_embedding':'CONSTRUCTION / CONTEXT CHANGE. Add the sixth point on the LEFT and retain the complete embedded target. This is not an equality between B5 and B6, nor centrality of D5 in B6.',
 'cancel_common_compensation':'LEFT LEDGER CANCELLATION. Cancel the SAME explicit positive Q45^4 prefix from BOTH sides of the proved relation. This is not a sphere cap or deletion from a fixed-product fibration.',
 'sphere_redraw':'SPHERE REDRAW ONLY. The SAME actual curve, factor identity and power are shown from the complementary side. Full local AND complete-context disk discrepancies, marked-sphere action and chosen+I are retained. The following disk substitution has its own step.'}

def padded_braid(word,height):
    q=braid_fragment_svg(word,compact=True);pad=(height-q['height'])/2
    body=q['svg'].split('>',1)[1].rsplit('</svg>',1)[0]
    def leads(order,a,b):return ''.join('<path data-strand="'+str(identity)+'" d="M '+str(13+12*i)+' '+str(a)+' V '+str(b)+'" stroke="'+RAINBOW[identity]+'" stroke-width=".8" fill="none"/>' for i,identity in enumerate(order))
    return '<svg xmlns="http://www.w3.org/2000/svg" width="86" height="'+str(height)+'" viewBox="0 0 86 '+str(height)+'" data-word="'+' '.join(map(str,word))+'">'+leads(range(6),0,pad)+'<g transform="translate(0 '+str(pad)+')">'+body+'</g>'+leads(q['exit_order'],pad+q['height'],height)+'</svg>'

def display_data(slug,r):
    rows=[];supports=[];braids=[];pool={}
    factors={f for s in r['stages'] for q in (s,)+tuple(s.get('atomic_steps',())) for f in q['factors']}
    for s in r['stages']:
        for q in s.get('parallel_cards',()):factors.update(q['after'])
    grids={f:support_grid(support_svg(f,6)) for f in factors}
    support_width=ceil(max(2*g['side']*24 for g in grids.values()))
    def row(f):
        if f in pool:return pool[f]
        grid=grids[f];scale=24/grid['pitch']
        inner=grid['svg'].split('>',1)[1].rsplit('</svg>',1)[0]
        physical_height=ceil(2*grid['vertical']*24)
        raw_width,raw_height=support_width/scale,physical_height/scale
        dx,dy=raw_width/2-grid['cx'],raw_height/2-grid['cy']
        svg='<svg xmlns="http://www.w3.org/2000/svg" width="'+str(support_width)+'" height="'+str(physical_height)+'" viewBox="0 0 '+format(raw_width,'.6f')+' '+format(raw_height,'.6f')+'"><g transform="translate('+format(dx,'.6f')+' '+format(dy,'.6f')+')">'+inner+'</g></svg>'
        height=ceil(max(62,2*grid['vertical']*24+12,braid_fragment_svg(f.word,compact=True)['height']))
        supports.append(svg);braids.append(padded_braid(f.word,height))
        data=dict(id=f.id,label=('H' if f.half else 'T'+str(f.points))+('^'+str(f.power) if f.power>1 else ''),word=f.word,
            half=f.half,points=f.points,power=f.power,height=height,support=len(supports)-1,braid=len(braids)-1,
            compensation=f.id.startswith(('positive.compensation','correction.')),native_factor=asdict(f))
        pool[f]=len(rows);rows.append(data);return pool[f]
    def state(s):
        score=s['score'];calculation=any(not f.half and f.points==3 and f.power%2 for f in s['factors'])
        return dict(title=s.get('title','Actual retained crossing'),kind=s.get('kind','disk_hurwitz'),factors=[row(f) for f in s['factors']],
            caption=str(len(s['factors']))+' actual records; support max/total '+str(score['maximum'])+'/'+str(score['total'])+'. '+('Ordinary triple roots are calculation factors, not final Lefschetz singularities.' if calculation else 'Exact actual curves; support lengths are not arc crossings or a joint minimum.'),
            scope=SCOPES.get(s.get('kind','disk_hurwitz_block'),SCOPES['disk_hurwitz_block']),score=score)
    shown=[]
    for s in r['stages']:
        q=state(s);q['full_disk_discrepancy']=s.get('full_disk_discrepancy');q['atomic']=[]
        for x in s.get('atomic_steps',()):
            raw=x['raw_move'];down=raw['source']<raw['target'];actor=raw['local_before'][0 if down else 1];neighbor=raw['local_before'][1 if down else 0]
            q['atomic'].append(state(dict(x,title=actor.id+(' DOWN across ' if down else ' UP across ')+neighbor.id)))
        q['parallel_cards']=[state(dict(title='Rotate block '+str(x['block']+1),kind='disk_cyclic_start',factors=x['after'],score=s['score'])) for x in s.get('parallel_cards',())]
        shown.append(q)
    return dict(example=slug,title=TITLES[slug],states=shown,rows=rows,supports=supports,braids=braids,
        support_width=support_width,summary={k:r[k] for k in ('profile','operations','listed_operations','adjacent_checks','local_peak','complete')})

def build():
    OUT.mkdir(exist_ok=True)
    for name in ('css','js'):write_utf8(OUT/('viewer.'+name),(ROOT/'examples'/('fibration_derivation_viewer.'+name)).read_text(encoding='utf-8-sig'))
    reports=all_derivations();cards=[]
    for slug,r in reports.items():
        d=display_data(slug,r);path=OUT/(slug+'.display.json');write_utf8(path,json.dumps(d,separators=(',',':')))
        final=panel(dict(factors=[asdict(f) for f in r['factors']]),TITLES[slug].split(':')[0]+' · actual final factorization')
        final=final.replace('two actual half twists',str(sum(f.half for f in r['factors']))+' actual half twists')
        # Only outer-canvas floating serialization is rounded for cross-version stability.
        final=re.sub(r'height="([0-9.]+)" viewBox="0 0 560 [0-9.]+"',lambda m:'height="'+format(float(m.group(1)),'.6f').rstrip('0').rstrip('.')+'" viewBox="0 0 560 '+format(float(m.group(1)),'.6f').rstrip('0').rstrip('.')+'"',final,count=1)
        write_utf8(OUT/(slug+'-final.svg'),final)
        note='<p>The imported original algebraic source is used. Four later drawing edits fail closure and are preserved separately in the certificate. The older dictated20-factor transcription lab remains unchanged.</p>' if slug=='10-10' else '<p>The positive compensation in the (4,3) proof is explicit on BOTH sides. Its cancellation is separate from disk substitutions and sphere redraws.</p>' if slug=='4-3' else '<p>Write A=T123, B=T456, H=H14 H25 H36 and r=sigma5 sigma4 sigma3 sigma2 sigma1. The proof uses r^3=ABH and H exchanging A/B, then retains every actual crossing.</p>'
        head='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+escape(TITLES[slug])+'''</title><link rel="stylesheet" href="viewer.css"><body data-example="'''+slug+'''"><main><p><a href="index.html">All three derivations</a> · <a href="'''+slug+'''.md">Readable proof</a> · <a href="'''+slug+'''.pdf">PDF</a> · <a href="'''+slug+'''.json">Full certificate</a></p><h1>'''+escape(TITLES[slug])+'''</h1><p><span class="pill">Complete sphere identity and separate chosen +I lift</span></p>'''+note+'''<p>'''+str(r['operations'])+' recorded steps / '+str(r['listed_operations'])+' individual operations / '+str(r['adjacent_checks'])+''' external adjacent checks. Internal named-rule checks are retained separately. Gold rows are half-twist arcs; marked points are UNNUMBERED at24px pitch. Individual supports are not a joint cut-system drawing.</p><div class="controls"><button id="previous" type="button">Previous</button><button id="next" type="button">Next</button><select id="step" aria-label="Derivation step"></select><label><input type="checkbox" id="before" checked>Show before</label><span id="position" role="status"></span></div><p id="loading" class="notice" role="status">Loading the precalculated derivation…</p><h2 id="title"></h2><p id="scope" class="notice"></p><section id="columns" class="columns"></section><section id="parallel" hidden></section><details id="atomic" hidden><summary>Show EVERY retained adjacent crossing of this carry</summary><div id="atomic-body" class="columns"></div></details><details id="discrepancy" hidden><summary>FULL disk discrepancy of the same-curve SPHERE redraw</summary><pre id="word"></pre></details><details><summary>Source provenance and original sheets</summary><p>The source files are copied byte-for-byte from Richard's separate Planar Mapping Class Groups project. The native proofs run without that project installed.</p><p><a href="../fibration-sources/planar-mcg-2026-10-30/provenance.json">Exact source manifest</a> · <a href="../fibration-sources/planar-mcg-2026-10-30/docs/assets/tenten-half-lantern.png">Original (10,10) sheet</a> · <a href="../fibration-sources/planar-mcg-2026-10-30/docs/assets/four-three-daisy.png">Original (4,3) sheet</a></p></details><footer>Six sphere points, five consecutive arcs. Construction, exact disk moves, sphere redraws and compensation are distinguished. The preferred (6,7), earlier labs, source charts and archives are preserved.</footer><script src="../six-seven-compact/connected-braid.js"></script><script src="viewer.js"></script></main></body></html>'''
        write_utf8(OUT/(slug+'.html'),head)
        cards.append('<article><h2><a href="'+slug+'.html">('+slug.replace('-',',')+')</a></h2><p>'+escape(TITLES[slug].split(': ',1)[1])+'</p><p>'+str(len(r['factors']))+' final factors; sphere identity and chosen+I checked.</p><p><a href="'+slug+'.html">Follow the diagrams</a> · <a href="'+slug+'.pdf">PDF</a></p></article>')
        print(json.dumps(dict(example=slug,payload_bytes=path.stat().st_size,rows=len(d['rows']),states=len(d['states']),sha256=sha256(path.read_bytes()).hexdigest())),flush=True)
    write_utf8(OUT/'index.html','<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Three complete genus-two derivations</title><link rel="stylesheet" href="viewer.css"><main><h1>The (6,2), (4,3) and (10,10) derivations</h1><p class="notice">Three complete source-pinned constructions, with every actual factor, bounded raw crossing, named relation, framing correction and separate sphere/+I certificate retained. The (10,10) work has been imported from the other project and completed using its original exact algebraic data.</p><div class="cards">'+''.join(cards)+'</div><p><a href="../six-seven-fifty-blocks/index.html?phase=clearfull&amp;step=0">The existing preferred (6,7) derivation</a> · <a href="../../FACTORIZATION_LAB.md">Factorization lab notes</a></p><p>These presentations certify the displayed relations. They do not assert an unproved identification with a particular literature curve chart, a framed section lift, or one jointly minimal drawing.</p></main></html>')
if __name__=='__main__':build()
