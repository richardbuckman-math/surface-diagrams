"""Source-exact panels for the selected F10 improvement and full-gather alternative."""
from pathlib import Path
import json,re
from examples.build_half_neighborhood_comparison import panel,write_utf8
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/proofs/posthalf-spare-comparison'


def pictures():
    r=json.loads((ROOT/'docs/proofs/six-seven-posthalf-spare.json').read_text(encoding='utf-8'))
    return r,(('before','Before: F10 support length 13',r['route']['stages'][0]),('selected','Selected: one crossing, F10 support length 7',r['route']['stages'][1]),('full-gather','Comparison: the full gather winds the 14 petal',r['complete_gather_alternative']['stages'][1]))


def picture(stage,title):
    svg=panel(stage,title).replace('two actual half twists','no half twists').replace('Gold = half-twist arc.','Highlight = F10 and the 14 petal.')
    for name in ('F10.2','posthalf.supply.1'):
        svg,n=re.subn(r'(<g data-factor="'+re.escape(name)+r'"><rect[^>]*fill=)"#f4f7fa"',r'\1"#fff3cf"',svg)
        if n!=1:raise ValueError('Highlight each actual changed record once')
    return svg


def build():
    r,items=pictures();OUT.mkdir(exist_ok=True);figures=[]
    for name,title,stage in items:
        write_utf8(OUT/(name+'.svg'),picture(stage,title));figures.append('<figure><figcaption>'+title+'</figcaption><a href="'+name+'.svg">Open full-size SVG</a><img src="'+name+'.svg" alt="'+title+'"></figure>')
    html="""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>A simpler F10 root on the research branch</title><style>*{box-sizing:border-box}body{margin:0;background:#eef3f6;color:#18344a;font:16px/1.5 system-ui}main{max-width:1500px;margin:auto;padding:20px}.panels{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}figure{margin:0;background:white;padding:10px;min-width:0}img{width:100%;height:auto;display:block}figcaption{font-weight:700}.scope{border-left:5px solid #b9872d;background:#fff3cf;padding:14px}a{color:#086aa2}@media(max-width:1000px){.panels{grid-template-columns:1fr}main{padding:12px}}</style><main><h1>One spare crossing simplifies F10</h1><p class="scope">Research continuation only; the preferred complete derivation remains unchanged. Carry the same 15 spare up across F10, keeping the spare fixed. Only F10 changes curve: its support word shortens 13 to 7 in this same chart. P13 and every other actual curve stay unchanged. No half twist, sphere move or cap is introduced. The odd exterior remains visible.</p><p>Across the same 15 records, all 11 changed pairwise CLOSED-neighborhood counts decrease; all others stay equal. Their total falls 770 to 700, while the largest pair stays 34. Support maximum stays 15, total 109 to 103; stored braid letters 240 to 232. These are pairwise closed-curve minima, not arc crossings or a jointly minimal drawing. The research prefix retains its earlier peaks; no whole-proof improvement or useful complete suffix join is claimed.</p><p>The full two-neighbor gather is also bounded and reached. Its second crossing changes the 14 petal, adding winding: support total 107, CLOSED total 764. Relative to the input, 11 counts decrease and 10 increase. It stays an unselected comparison. The adjacent13/15 pair alone does not establish a named pattern or repair the previously excluded unchanged135 triangle.</p><p>The simpler245 root has an individually matched ROUND45 rose petal, a concrete possible loan for returning the original145 supplier. That expansion, transport and return have not been performed. Each panel uses the same unnumbered six-point grid at 24px pitch and 1.68px radius; the pictures are individual supports.</p><p><a href="../six-seven-posthalf-spare.json">Exact routes, kernels and comparison</a> Â· <a href="../six-seven-posthalf-spare.md">Research explanation</a> Â· <a href="../six-seven-fifty-blocks/index.html?phase=clearfull&amp;step=0">Unchanged preferred derivation</a></p><div class="panels">"""
    write_utf8(OUT/'index.html',html+''.join(figures)+'</div></main></html>');print('Saved three source-exact15-record panels')


if __name__=='__main__':build()
