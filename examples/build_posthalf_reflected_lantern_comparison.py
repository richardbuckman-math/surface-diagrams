"""Source-exact reflected cabled lantern panels; preferred proof unchanged."""
from pathlib import Path
import json,re
from examples.build_half_neighborhood_comparison import panel,write_utf8
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/proofs/posthalf-reflected-lantern-comparison'


def pictures():
    r=json.loads((ROOT/'docs/proofs/six-seven-posthalf-reflected-lantern.json').read_text(encoding='utf-8'));s=r['route']['stages']
    return r,(('before','Input: adjacent actual 235 and 135 roots',s[0]),('supply','The 123 rose retains all three actual petals',s[2]),('gathered','The actual 235,135,12 are adjacent',s[3]),('outer','Reflected lantern reaches another outer',s[4]),('exterior-input','Actual 34 and both outer curves are adjacent',s[6]),('after','A second unit exterior stays visible',s[7]))


def picture(stage,title):
    svg=panel(stage,title).replace('two actual half twists','no half twists').replace('Gold = half-twist arc.','Highlight = lantern factors.')
    for raw in stage['factors']:
        name=raw['id']
        if name in ('posthalf.return.R123','alternative.S1','cyclic135.R135','outer.O1245','cyclic135.supply.0') or name.startswith(('reflected.loan.','reflected.output.','reflected.exterior','reflected.inner125')):
            svg,n=re.subn(r'(<g data-factor="'+re.escape(name)+r'"><rect[^>]*fill=)"#f4f7fa"',r'\1"#fff3cf"',svg)
            if n!=1:raise ValueError('Highlight each actual selected record once')
    return svg


def build():
    _,items=pictures();OUT.mkdir(exist_ok=True);figures=[]
    for name,title,stage in items:
        write_utf8(OUT/(name+'.svg'),picture(stage,title));figures.append('<figure><figcaption>'+title+'</figcaption><a href="'+name+'.svg">Open full-size SVG</a><img src="'+name+'.svg" alt="'+title+'"></figure>')
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Two matched cabled lanterns reach a second exterior</title><style>*{box-sizing:border-box}body{margin:0;background:#eef3f6;color:#18344a;font:16px/1.5 system-ui}main{max-width:1200px;margin:auto;padding:20px}.panels{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:white;padding:10px;min-width:0}img{width:100%;height:auto;display:block}figcaption{font-weight:700}.scope{border-left:5px solid #b9872d;background:#fff3cf;padding:14px}a{color:#086aa2}@media(max-width:850px){.panels{grid-template-columns:1fr}main{padding:12px}}</style><main><h1>Two cabled lanterns reach a second visible exterior</h1><p class="scope">Reached research continuation only. The preferred complete derivation stays unchanged. Seven positive disk moves choose an explicit cyclic start, expand the actual returned123 donor, carry its12 petal across two commuting neighbors, and contract the actual235,135,12 cluster. One further bounded outer carry and an explicit cyclic start then expose the individually matched34 and two four-point curves; their second cabled lantern reaches a second visible unit exterior. Every named input and output matches individually in one common chart.</p><p>The exterior and the existing four-point outer remain literally unchanged throughout the short-side12 carry. The later same-outer carry changes only the intervening35 curve; the fresh34 is consumed in the second cabled lantern and the fresh45 stays visible. The12 loan is consumed in the new outer, not returned. The other two actual123 petals stay visible. Both old125 loan petals remain separate records; there is no ancestry deletion. The reflected canonical relation retains every generator identity, its source named relation and internal interchange, full framing balances, nonabelian kernels and separate disk/sphere/lift certificates.</p><p>The intermediate outer endpoint has15 records, support maximum7 and total64. The final endpoint returns to14 records, support maximum9 to7 and total65 to62; stored braid letters146 to148. CLOSED totals320 to240 and maximum20 to14 describe the changed inventories. The inventories differ, so these descriptive totals are not entrywise dominance, arc crossings, jointly minimal drawings or whole-proof bounds. Both odd unit exteriors remain separately visible, each with chosen lift-I. The residual has chosen lift+I and diagnostic boundary-square action; this is not a named residual closure. No half twist, negative factor, sphere redraw or cap is introduced; this is not a shorter or adopted complete proof and no useful complete suffix join is claimed.</p><p>All points use the same unnumbered six-point grid at24px pitch and1.68px radius. These are individual supports. <a href="../six-seven-posthalf-reflected-lantern.json">Exact moves, charts and kernels</a> &middot; <a href="../six-seven-posthalf-reflected-lantern.md">Research explanation</a> &middot; <a href="../six-seven-fifty-blocks/index.html?phase=clearfull&amp;step=0">Unchanged preferred derivation</a></p><div class="panels">'''
    write_utf8(OUT/'index.html',html+''.join(figures)+'</div></main></html>');print('Saved six exact panels;90 factor grids')


if __name__=='__main__':build()
