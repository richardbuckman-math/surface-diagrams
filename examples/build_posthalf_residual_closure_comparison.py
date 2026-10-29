"""Exact named residual closure panels; the preferred public proof is unchanged."""
from pathlib import Path
import json,re
from examples.build_half_neighborhood_comparison import panel,write_utf8
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/proofs/posthalf-residual-closure-comparison'


def pictures():
    r=json.loads((ROOT/'docs/proofs/six-seven-posthalf-residual-closure.json').read_text(encoding='utf-8'));s=r['route']['stages']
    return r,(('before','Input: three exteriors and eight residual factors',s[0]),('tail','The actual cyclic tail rose recovers125',s[1]),('loan','The NEW15 crosses only its two donor neighbors',s[3]),('outer','The actual134,45,35,15 daisy reachesO1345',s[4]),('gathered','The FIVE actual final daisy inputs are adjacent',s[5]),('after','FOUR standard unit exteriors remain visible',s[6]))


def picture(stage,title):
    svg=panel(stage,title).replace('two actual half twists','no half twists').replace('Gold = half-twist arc.','Highlight = residual factors.')
    # Only the outer canvas decimal is normalized; source support/grid bodies
    # stay unchanged across the supported Python summation implementations.
    def outer_canvas(match):
        value=format(float(match.group(1)),'.6f').rstrip('0').rstrip('.')
        return '<svg xmlns="http://www.w3.org/2000/svg" width="560" height="'+value+'" viewBox="0 0 560 '+value+'"'
    svg,count=re.subn(r'<svg xmlns="http://www.w3.org/2000/svg" width="560" height="([0-9.]+)" viewBox="0 0 560 [0-9.]+"',outer_canvas,svg,count=1)
    if count!=1:raise ValueError('Stabilize only the outer comparison canvas')
    old_exteriors={'third.exterior','posthalf.exterior','reflected.exterior'}
    for raw in stage['factors']:
        name=raw['id']
        if name not in old_exteriors:
            svg,n=re.subn(r'(<g data-factor="'+re.escape(name)+r'"><rect[^>]*fill=)"#f4f7fa"',r'\1"#fff3cf"',svg)
            if n!=1:raise ValueError('Highlight each selected actual record once')
    return svg


def build():
    r,items=pictures();OUT.mkdir(exist_ok=True);figures=[]
    for name,title,stage in items:
        write_utf8(OUT/(name+'.svg'),picture(stage,title));figures.append('<figure><figcaption>'+title+'</figcaption><a href="'+name+'.svg">Open full-size SVG</a><img src="'+name+'.svg" alt="'+title+'"></figure>')
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Four individually matched named substitutions close the residual</title><style>*{box-sizing:border-box}body{margin:0;background:#eef3f6;color:#18344a;font:16px/1.5 system-ui}main{max-width:1200px;margin:auto;padding:20px}.panels{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:white;padding:10px;min-width:0}img{width:100%;height:auto;display:block}figcaption{font-weight:700}.scope{border-left:5px solid #b9872d;background:#fff3cf;padding:14px}a{color:#086aa2}@media(max-width:850px){.panels{grid-template-columns:1fr}main{padding:12px}}</style><main><h1>The residual now closes by actual named PC roses and daisies</h1><p class="scope">Reached research continuation. Six positive disk moves use four separately matched named substitutions to turn the eight-factor residual into a FOURTH standard unit exterior. Every actual ordered input and output matches individually. The preferred complete public derivation and PDF remain unchanged; this gallery does not claim an adopted or shorter whole derivation.</p><p>The adjacent older15,older25,NEW12 contract by their exact cyclic125 rose. Its three input units retain explicit distinct ancestries; no original consumed12 is silently restored. The recovered125 then expands by its internal(+1) rose to a new12,25,15. The SAME new15 moves upward through only its two donor neighbors, changing those two curves while keeping itself fixed.</p><p>The actual ordered134 root,old45,old35 andNEW15 match a four-point PC daisy in one full chart, producingO1345. Its retained canonical proof includes the actual internal petal interchange and a full internal cyclic common conjugation. A separate explicit cyclic start at old23 then exposes all five actual inputs of the final D5 daisy. That local rule retains TWO internal forward petal interchanges, its full inverse-prefix cyclic frame and independently known standard D5 invariance. Raw free-word checks precede individually normalized presentations.</p><p>All THREE earlier unit exteriors remain visible and literal throughout. The final FOUR standard unit exteriors are distinct actual records, each with chosen lift-I; their combined chosen lift is+I. They are not capped, deleted or silently identified here. There is no sphere redraw, half twist, negative factor or peripheral cleanup. The final standard four-exterior configuration supplies the mathematical join; any later sphere redraw and fourth-power cleanup stay separate.</p><p>All actual named inputs and outputs retain signed PC framing balances, full local disk discrepancies, separate marked-sphere and chosen lift checks, and complete nonabelian point-pushing kernels with shadows and reconstructions. Every external adjacent move is reconstructed before normalized individual presentations. Individual support diagrams are not a simultaneous joint-cut certificate.</p>'''
    before=r['route']['before_score'];after=r['route']['after_score']
    html+='<p>The local route uses6 listed disk moves,2 external adjacent checks and4 named substitutions. It starts with11 records and ends with4. Support maximum'+str(before['max_support_word'])+' to'+str(after['max_support_word'])+', total'+str(before['total_support_word'])+' to'+str(after['total_support_word'])+'; stored braid letters'+str(before['braid_letters'])+' to'+str(after['braid_letters'])+'. Inventories differ, so these descriptive totals are not entrywise dominance, arc intersections, jointly minimal drawings or whole-proof complexity bounds.</p>'
    html+='''<p>All points use the same unnumbered six-point grid at24px pitch and1.68px radius. <a href="../six-seven-posthalf-residual-closure.json">Exact actual moves, common charts and complete certificates</a> &middot; <a href="../six-seven-posthalf-residual-closure.md">Research explanation</a> &middot; <a href="../six-seven-fifty-blocks/index.html?phase=clearfull&amp;step=0">Unchanged preferred derivation</a></p><div class="panels">'''
    write_utf8(OUT/'index.html',html+''.join(figures)+'</div></main></html>');print('Saved six exact panels;51 factor grids')


if __name__=='__main__':build()