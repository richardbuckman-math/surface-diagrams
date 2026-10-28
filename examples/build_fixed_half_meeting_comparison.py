"""Source-exact support panels for the reached midpoint gather, not a proof edit."""
from pathlib import Path
import json
from examples.build_half_neighborhood_comparison import panel,write_utf8
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/proofs/fixed-half-meeting-comparison'

def pictures():
    r=json.loads((ROOT/'docs/proofs/six-seven-fixed-half-meeting.json').read_text(encoding='utf-8'))
    return r,(
        ('input','Common input',r['stages'][0]),
        ('original','Original: fixed F11 UP',dict(factors=r['original_meeting_factors'])),
        ('meeting','Candidate: halves meet lower',r['stages'][2]),
        ('joined','After full-pair carry: complete join',r['stages'][4]))

def picture(stage,title):
    n=sum(f['half'] for f in stage['factors'])
    return panel(stage,title).replace('two actual half twists',str(n)+' actual half twists').replace('Gold = half-twist arc.','Gold row = half-twist factor.')

def build():
    r,items=pictures();OUT.mkdir(exist_ok=True);figures=[]
    for name,title,stage in items:
        filename=name+'.svg';write_utf8(OUT/filename,picture(stage,title))
        figures.append('<figure><figcaption>'+title+'</figcaption><a href="'+filename+'">Open full-size SVG</a><img src="'+filename+'" alt="'+title+'; exact individual factor supports"></figure>')
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fixed-half meeting: exact route comparison</title><style>*{box-sizing:border-box}body{margin:0;background:#eef3f6;color:#18344a;font:16px/1.5 system-ui}main{max-width:1200px;margin:auto;padding:20px}.panels{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:white;padding:10px;min-width:0}img{width:100%;height:auto;display:block}figcaption{font-weight:700}.scope{border-left:5px solid #b9872d;background:#fff3cf;padding:14px}a{color:#086aa2}@media(max-width:850px){.panels{grid-template-columns:1fr}main{padding:12px}}</style><main><h1>Meet the half twists before carrying their full twist</h1><p class="scope">Research route only; the preferred derivation is unchanged. Both original half twists stay literally fixed. Carry F6 down through five neighbors and F11 up across the squared pair; these two edits are independent. Combine the equal halves there, then carry the full twist up. Every factor rejoins the original complete derivation.</p><p>At the meeting, the same 17 records have closed-neighborhood crossing sum 936 instead of 1094, and largest pair 36 instead of 48. Support-word maximum is 18 instead of 17. The half arcs themselves are unchanged. The final full-pair carry restores the original endpoint's geometry after the halves disappear; this is a redistribution of complexity, not a whole-proof tangle improvement.</p><p>The candidate takes four local moves and eleven adjacent checks instead of two and six. The first two moves commute literally in both orders. These are independent factor edits, not a certificate for one simultaneous joint ambient isotopy. Grids are unnumbered, at 24px pitch and 1.68px radius. Closed-neighborhood counts are not arc intersections or a jointly attainable drawing minimum.</p><p><a href="../six-seven-fixed-half-meeting.json">Exact routes, both orders, geometry, kernels and complete join</a> · <a href="../six-seven-fixed-half-meeting.md">Audit explanation</a> · <a href="../six-seven-fifty-blocks/index.html?phase=clearfull&amp;step=0">Unchanged preferred complete derivation</a></p><div class="panels">'''
    write_utf8(OUT/'index.html',html+''.join(figures)+'</div></main></html>')
    print('Saved4 exact comparison panels; preferred proof/PDF unchanged')

if __name__=='__main__':build()
