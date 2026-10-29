"""Four source-exact panels for the longer, clearer ordered-loan route."""
from pathlib import Path
import json,re
from examples.build_half_neighborhood_comparison import panel,write_utf8
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/proofs/posthalf-block-comparison'


def pictures():
    r=json.loads((ROOT/'docs/proofs/six-seven-posthalf-block.json').read_text(encoding='utf-8'));metrics=r['trajectory_comparisons']
    return r,(('before','Input: four curves still wind',r['route']['stages'][0]),('direct-peak','Direct route: worst closed pair 52',r['direct_comparison']['stages'][metrics['direct']['peak_pair_stage']]),('chosen-peak','Chosen route: worst closed pair 46',r['route']['stages'][metrics['inverse']['peak_pair_stage']]),('after','Endpoint: four actual curves shorten',r['route']['stages'][-1]))


def picture(stage,title):
    svg=panel(stage,title).replace('two actual half twists','no half twists').replace('Gold = half-twist arc.','Highlight = the changed curves and loan petals.')
    for name in ('F8.2','alternative.S1','posthalf.supply.0','alternative.P13','outer.loan.1','outer.loan.2'):
        svg,n=re.subn(r'(<g data-factor="'+re.escape(name)+r'"><rect[^>]*fill=)"#f4f7fa"',r'\1"#fff3cf"',svg)
        if n!=1:raise ValueError('Each highlighted actual record is shown once')
    return svg


def build():
    _,items=pictures();OUT.mkdir(exist_ok=True);figures=[]
    for name,title,stage in items:
        write_utf8(OUT/(name+'.svg'),picture(stage,title));figures.append('<figure><figcaption>'+title+'</figcaption><a href="'+name+'.svg">Open full-size SVG</a><img src="'+name+'.svg" alt="'+title+'"></figure>')
    html="""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>A longer ordered-loan route untangles four curves</title><style>*{box-sizing:border-box}body{margin:0;background:#eef3f6;color:#18344a;font:16px/1.5 system-ui}main{max-width:1200px;margin:auto;padding:20px}.panels{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:white;padding:10px;min-width:0}img{width:100%;height:auto;display:block}figcaption{font-weight:700}.scope{border-left:5px solid #b9872d;background:#fff3cf;padding:14px}a{color:#086aa2}@media(max-width:850px){.panels{grid-template-columns:1fr}main{padding:12px}}</style><main><h1>Two retained loan petals untangle four curves</h1><p class="scope">Reached research continuation only. The preferred complete derivation remains unchanged. Carry the two actual 125-loan petals up as an ordered block across six neighbors, retaining every individual adjacent move. F8 becomes round345; S1, W and P13 also shorten. The endpoint still has the SAME 14 records. Both actual loan records are restored literally; two matching 15 copies remain separate. The odd exterior stays visible.</p><p>All 28 changed pairwise CLOSED-neighborhood counts decrease; 63 stay equal. The total falls 524 to 346 and the largest pair 34 to 20. Support maximum/total fall 15/85 to 9/67; stored braid letters 200 to 152. The four changed support lengths are F8: 9 to 3, S1: 15 to 9, W: 8 to 4, P13: 8 to 6. Ten other actual curves stay literally unchanged apart from row position.</p><p>The selected route takes 15 listed moves and 14 adjacent checks: reorder the donor petals, choose an explicit cyclic start, make twelve individually listed crossings, then restore the donor order. The direct route takes 13 moves and 12 checks. The two extra real interchanges lower the trajectory's worst CLOSED pair from 52 to 46 and peak sum from 536 to 532; word peak stays 17. The forward preparation gives 552/48 and is unselected. The endpoints match individually in B5; one P13 presentation differs, so they are not called literal tuple joins.</p><p>Transient complexity still exceeds the input's 524/34. These are exact pairwise closed-curve minima and chart-specific lengths, not arc crossings, one jointly minimal drawing or whole-proof bounds. No complete suffix join is proved. The next block crossing is rejected before application at support 40.</p><p>The now-round F8 root has an exact required 35 rose petal; that rose remains unexpanded. The old exact 13 supplier remains unchanged, but the required 135 root and 15 petal are still missing. No half twist, negative factor, sphere redraw, cap or named substitution is introduced.</p><p>All points are unnumbered on the same six-point grid, at 24px pitch and 1.68px radius. These are individual support drawings. <a href="../six-seven-posthalf-block.json">Exact routes, geometry, kernels and failed probes</a> · <a href="../six-seven-posthalf-block.md">Research explanation</a> · <a href="../six-seven-fifty-blocks/index.html?phase=clearfull&amp;step=0">Unchanged preferred derivation</a></p><div class="panels">"""
    write_utf8(OUT/'index.html',html+''.join(figures)+'</div></main></html>');print('Saved4 exact14-record panels;56 point grids')


if __name__=='__main__':build()
