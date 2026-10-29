"""Source-exact selected cyclic 135 rose panels; preferred proof is unchanged."""
from pathlib import Path
import json,re
from examples.build_half_neighborhood_comparison import panel,write_utf8
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/proofs/posthalf-cyclic-rose-comparison'


def pictures():
    r=json.loads((ROOT/'docs/proofs/six-seven-posthalf-cyclic-rose.json').read_text(encoding='utf-8'));s=r['route']['stages']
    return r,(('before','Input: round 345 and two actual petals',s[0]),('supply','Cyclic 345 rose retains all three petals',s[1]),('gathered','The actual 35,15,13 are adjacent',s[2]),('after','Actual cyclic 135 rose has contracted',s[3]))


def picture(stage,title):
    svg=panel(stage,title).replace('two actual half twists','no half twists').replace('Gold = half-twist arc.','Highlight = rose factors.')
    for raw in stage['factors']:
        name=raw['id']
        if name in ('F8.2','posthalf.supply.0','alternative.P13') or name.startswith('cyclic135.'):
            svg,n=re.subn(r'(<g data-factor="'+re.escape(name)+r'"><rect[^>]*fill=)"#f4f7fa"',r'\1"#fff3cf"',svg)
            if n!=1:raise ValueError('Highlight each actual selected record once')
    return svg


def build():
    _,items=pictures();OUT.mkdir(exist_ok=True);figures=[]
    for name,title,stage in items:
        write_utf8(OUT/(name+'.svg'),picture(stage,title));figures.append('<figure><figcaption>'+title+'</figcaption><a href="'+name+'.svg">Open full-size SVG</a><img src="'+name+'.svg" alt="'+title+'"></figure>')
    html="""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>An actual cyclic 135 rose reaches its root</title><style>*{box-sizing:border-box}body{margin:0;background:#eef3f6;color:#18344a;font:16px/1.5 system-ui}main{max-width:1200px;margin:auto;padding:20px}.panels{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:white;padding:10px;min-width:0}img{width:100%;height:auto;display:block}figcaption{font-weight:700}.scope{border-left:5px solid #b9872d;background:#fff3cf;padding:14px}a{color:#086aa2}@media(max-width:850px){.panels{grid-template-columns:1fr}main{padding:12px}}</style><main><h1>The actual cyclic35,15,13 rose contracts</h1><p class="scope">Reached research continuation only. The preferred complete derivation stays unchanged. Three positive disk moves expand the actual round345 in a certified cyclic PC rose, carry its35 petal across a commuting neighbor, then contract the actual adjacent35,15,13 into the new135 root. Every input and output matches individually in one common chart. Both other donor petals, round34 and round45, remain visible.</p><p>The two matching15 copies are distinct records: W is consumed in the new root; the other125-loan15 remains. Eleven shared actual records stay literally unchanged. Both internal cyclic starts retain their full raw inverse-prefix conjugation and separately checked output invariance. No half twist, negative factor, sphere redraw or cap appears; the odd exterior remains visible.</p><p>The endpoint still has14 records. Support maximum stays9, total67 to65; stored braid letters152 to146. CLOSED sum346 to320, maximum20 stays. Inventories differ, so these are descriptive totals, not entrywise dominance, arc crossings, a jointly minimal drawing or whole-proof bounds. No complete suffix join is proved.</p><p>This135 root is different from the previously missing135 target. It does individually match another cabled-lantern chart with the returned123 root and25 petal, but their actual order is wrong and its product is noncentral. No next lantern, second exterior or complete proof shortening is claimed. The exact order gap and an unselected one-move S1 comparison remain in the research report.</p><p>All points use the same unnumbered six-point grid at 24px pitch and 1.68px radius. These are individual supports. <a href="../six-seven-posthalf-cyclic-rose.json">Exact moves, common charts, kernels and order witnesses</a> Ã‚Â· <a href="../six-seven-posthalf-cyclic-rose.md">Research explanation</a> Ã‚Â· <a href="../six-seven-fifty-blocks/index.html?phase=clearfull&amp;step=0">Unchanged preferred derivation</a></p><div class="panels">"""
    write_utf8(OUT/'index.html',html+''.join(figures)+'</div></main></html>');print('Saved four exact panels;60 factor grids')


if __name__=='__main__':build()
