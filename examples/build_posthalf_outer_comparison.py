"""Source-exact four panels for the reached outer and the45 comparison."""
from pathlib import Path
import json,re
from examples.build_half_neighborhood_comparison import panel,write_utf8
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/proofs/posthalf-outer-comparison'


def pictures():
    r=json.loads((ROOT/'docs/proofs/six-seven-posthalf-outer.json').read_text(encoding='utf-8'))
    return r,(('before','Input: the simpler F10 endpoint',r['route']['stages'][0]),('gathered','Actual four daisy inputs are adjacent',r['route']['stages'][3]),('outer','Selected: one matched four-point outer',r['route']['stages'][4]),('comparison45','Comparison: reconstruct the 145 root',r['round45_comparison']['stages'][3]))


def picture(stage,title):
    svg=panel(stage,title).replace('two actual half twists','no half twists').replace('Gold = half-twist arc.','Highlight = the selected donors and outputs.')
    names={'posthalf.inner125','posthalf.supply.1','posthalf.output.1','F10.2','outer.loan.0','outer.loan.1','outer.loan.2','outer.O1245','comparison.R145','compare45.0','compare45.1'}
    for raw in stage['factors']:
        if raw['id'] in names:
            svg,n=re.subn(r'(<g data-factor="'+re.escape(raw['id'])+r'"><rect[^>]*fill=)"#f4f7fa"',r'\1"#fff3cf"',svg)
            if n!=1:raise ValueError('Highlight each actual selected record once')
    return svg


def build():
    r,items=pictures();OUT.mkdir(exist_ok=True);figures=[]
    for name,title,stage in items:
        write_utf8(OUT/(name+'.svg'),picture(stage,title));figures.append('<figure><figcaption>'+title+'</figcaption><a href="'+name+'.svg">Open full-size SVG</a><img src="'+name+'.svg" alt="'+title+'"></figure>')
    html="""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>A matched post-half daisy reaches a four-point outer</title><style>*{box-sizing:border-box}body{margin:0;background:#eef3f6;color:#18344a;font:16px/1.5 system-ui}main{max-width:1200px;margin:auto;padding:20px}.panels{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:white;padding:10px;min-width:0}img{width:100%;height:auto;display:block}figcaption{font-weight:700}.scope{border-left:5px solid #b9872d;background:#fff3cf;padding:14px}a{color:#086aa2}@media(max-width:850px){.panels{grid-template-columns:1fr}main{padding:12px}}</style><main><h1>A matched daisy contracts to one four-point outer</h1><p class="scope">Reached research continuation only. The preferred complete derivation remains unchanged. Borrow a 12 petal from the actual 125 rose, choose an explicit cyclic start, and carry that petal across only the commuting exterior. The actual ordered 14 petal, transported 15 spare, 245 root and 12 petal then match a PC daisy individually in one common chart. Contract them to the four-point outer shown below. P13 and every other shared record stay literally unchanged.</p><p>This takes four positive disk moves and one external adjacent check. Three internal canonical daisy interchanges are also retained. It leaves 14 records instead of 15, with the odd exterior still visible. The 125 donor remains as two actual petals: the borrowed 12 is consumed in the new outer and has not been returned. No half twist, negative factor, sphere move or cap appears. No useful complete suffix join is yet proved.</p><p>Endpoint support maximum stays 15, total 103 to 85; stored braid letters 232 to 200. CLOSED-neighborhood sum changes 700 to 524, maximum stays 34. Inventories differ, so these are descriptive totals, not entrywise dominance, arc crossings, a jointly minimal drawing or whole-proof complexity bounds.</p><p>The three-move 45 alternative is also reached and shown for comparison. Its cyclic rose reconstructs the 145 root using V, the new 45 and the restored matching OTHER W copy; the original supplier W stays untouched. It leaves 15 records, support total 101 and CLOSED sum 694. Direct V-over-P13 and both further root/P13 carries are rejected before application at 24, 26 and 25. The alternative is not selected.</p><p>All points are unnumbered on the same six-point grid, at 24px pitch and 1.68px radius. These are individual support diagrams. Every named input/output, signed PC balance, full disk discrepancy, separate sphere/+I check, nonabelian kernel and B4 shadow is retained.</p><p><a href="../six-seven-posthalf-outer.json">Exact route, common chart, kernels and comparison</a> · <a href="../six-seven-posthalf-outer.md">Research explanation</a> · <a href="../six-seven-fifty-blocks/index.html?phase=clearfull&amp;step=0">Unchanged preferred derivation</a></p><div class="panels">"""
    write_utf8(OUT/'index.html',html+''.join(figures)+'</div></main></html>');print('Saved four source-exact panels;61 factor grids')


if __name__=='__main__':build()
