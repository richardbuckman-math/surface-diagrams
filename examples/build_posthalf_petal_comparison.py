"""Source-exact before/after diagrams for the selected post-half petal move."""
from pathlib import Path
import json,re
from examples.build_half_neighborhood_comparison import panel,write_utf8
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/proofs/posthalf-petal-comparison'


def pictures():
    r=json.loads((ROOT/'docs/proofs/six-seven-posthalf-petal.json').read_text(encoding='utf-8'))
    return r,(('before','Before: P13 support length 18',r['route']['stages'][0]),('after','After: P13 support length 8',r['route']['stages'][1]))


def picture(stage,title):
    svg=panel(stage,title).replace('two actual half twists','no half twists').replace('Gold = half-twist arc.','Highlight = the changed P13 curve.')
    svg,count=re.subn(r'(<g data-factor="alternative\.P13"><rect[^>]*fill=)"#f4f7fa"',r'\1"#fff3cf"',svg)
    if count!=1:raise ValueError('Highlight exactly the actual changed P13 record')
    return svg


def build():
    r,items=pictures();OUT.mkdir(exist_ok=True);figures=[]
    for name,title,stage in items:
        filename=name+'.svg';write_utf8(OUT/filename,picture(stage,title));figures.append('<figure><figcaption>'+title+'</figcaption><a href="'+filename+'">Open full-size SVG</a><img src="'+filename+'" alt="'+title+'; highlighted actual P13 record"></figure>')
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>A shorter P13 curve on the research branch</title><style>*{box-sizing:border-box}body{margin:0;background:#eef3f6;color:#18344a;font:16px/1.5 system-ui}main{max-width:1200px;margin:auto;padding:20px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:white;padding:10px;min-width:0}img{width:100%;height:auto;display:block}figcaption{font-weight:700}.scope{border-left:5px solid #b9872d;background:#fff3cf;padding:14px}a{color:#086aa2}@media(max-width:850px){.pair{grid-template-columns:1fr}main{padding:12px}}</style><main><h1>One petal moves up; P13 becomes less tangled</h1><p class="scope">Verified research continuation only. The preferred complete derivation remains unchanged. Move the W petal up one neighbor while keeping W fixed. This positive disk Hurwitz move changes P13 to W<sup>-1</sup> P13 W. Every other actual curve stays fixed; the two adjacent records exchange positions. No half twist, sphere move or cap is introduced. The visible unit exterior retains its odd lift.</p><p>The highlighted P13 support word shortens from 18 to 8 in this same chart. Across the same 15 records, all nine changed pairwise closed-neighborhood intersection counts decrease and all others stay equal. The sum falls 862 to 770 and the largest pair 36 to 34. Support maximum/total fall 18/119 to 15/109; braid letters fall 258 to 240. These are closed-curve counts, not arc intersections or one jointly minimal drawing.</p><p>Each factor uses the same unnumbered six-point grid, at 24px pitch and 1.68px radius. These are individual support diagrams. No useful complete join from this research branch to the preferred suffix has yet been proved; no new preferred move count or shortening is claimed.</p><p><a href="../six-seven-posthalf-petal.json">Exact move, pair certificates, kernels and scoped target failures</a> · <a href="../six-seven-posthalf-petal.md">Research explanation</a> · <a href="../six-seven-fifty-blocks/index.html?phase=clearfull&amp;step=0">Unchanged preferred complete derivation</a></p><div class="pair">'''
    write_utf8(OUT/'index.html',html+''.join(figures)+'</div></main></html>')
    print('Saved two exact15-record panels; preferred proof/PDF unchanged')

if __name__=='__main__':build()
