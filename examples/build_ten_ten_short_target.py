"""Two exact support panels; neither depicts a reached (10,10) gather."""
from pathlib import Path
import json,re
from examples.build_half_neighborhood_comparison import panel,write_utf8

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/proofs/ten-ten-short-target'

def picture(stage,title):
    svg=panel(stage,title).replace('two actual half twists','four positive half twists')
    def stable(m):
        n=format(float(m.group(1)),'.6f').rstrip('0').rstrip('.')
        return '<svg xmlns="http://www.w3.org/2000/svg" width="560" height="'+n+'" viewBox="0 0 560 '+n+'"'
    svg,count=re.subn(r'<svg xmlns="http://www.w3.org/2000/svg" width="560" height="([0-9.]+)" viewBox="0 0 560 [0-9.]+"',stable,svg,count=1)
    if count!=1:raise ValueError('Stabilize only the outer canvas decimals')
    return svg

def pictures():
    r=json.loads((ROOT/'docs/proofs/ten-ten-short-four-three-target.json').read_bytes())
    return r,(('known-c','Known C: standalone (4,3)',dict(factors=r['reference_C_factors'])),
              ('target','Genuine (4,3) target: not extracted',dict(factors=r['target_factors'])))

def build():
    r,items=pictures();OUT.mkdir(exist_ok=True);figures=[]
    for name,title,stage in items:
        write_utf8(OUT/(name+'.svg'),picture(stage,title))
        figures.append('<figure><figcaption>'+title+'</figcaption><a href="'+name+'.svg">Open full-size SVG</a><img src="'+name+'.svg" alt="'+title+'"></figure>')
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>A genuine short (4,3) target</title><style>*{box-sizing:border-box}body{margin:0;background:#eef3f6;color:#18344a;font:16px/1.5 system-ui}main{max-width:1200px;margin:auto;padding:20px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:white;padding:10px;min-width:0}img{width:100%;height:auto;display:block}figcaption{font-weight:700}.scope{border-left:5px solid #b9872d;background:#fff3cf;padding:14px}a{color:#086aa2}@media(max-width:850px){.pair{grid-template-columns:1fr}main{padding:12px}}</style><main><h1>A genuine short (4,3) target</h1><p class="scope">This is a verified seven-factor relation, not an extracted summand of the (10,10). Six curves are copied literally from the published twenty-factor input. Hstar is a desired new half class; it has not been supplied or gathered through moves on that input. The reverse fibration-equivalence question remains open.</p><p>The target is B.1 B.2 B.3 B.4 Hstar C.5 C.6. All seven actual target factors individually match a four-move internal Hurwitz proof from the known C (4,3) block. Every reference state has disk-support maximum at most18. The full product equals D(2..6)^2 faithfully in the disk, with separate marked-sphere identity and chosen+I checks. Complete nonabelian kernels, shadows and reconstructions are retained. The embedded five-point boundary is never assumed central in B6.</p><p>Hstar is sigma5^-4 sigma2^-2 applied to the actual C.5 half. Its exact disk support word has length18. A six-point support-word bound is not an arc-crossing or whole-proof tangle bound. The two panels show individual supports, not a joint-cut diagram or a proposed shorter preferred derivation.</p><p>Gold marks half arcs. The fourteen six-point grids/84 dots are unnumbered, at24px pitch and1.68px radius. No preferred proof, viewer, payload or PDF changes.</p><p><a href="../ten-ten-short-four-three-target.md">Readable proof and exact scope</a> · <a href="../ten-ten-short-four-three-target.json">All words, checks and full kernels</a> · <a href="../fibration-derivations/10-10.html">Published (10,10) derivation</a></p><div class="pair">'''
    html=html.replace('at most18','at most 18').replace('chosen+I','chosen +I').replace('at24px pitch and1.68px','at 24px pitch and 1.68px')
    write_utf8(OUT/'index.html',html+''.join(figures)+'</div></main></html>')
    print('Saved two panels,14 six-point grids,84 unnumbered points')

if __name__=='__main__':build()
