"""Source-exact upper-root cabled lantern panels; preferred proof unchanged."""
from pathlib import Path
import json,re
from examples.build_half_neighborhood_comparison import panel,write_utf8
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/proofs/posthalf-upper-cabled-comparison'


def pictures():
    r=json.loads((ROOT/'docs/proofs/six-seven-posthalf-upper-cabled.json').read_text(encoding='utf-8'));s=r['route']['stages']
    return r,(('before','Input: actual 13,23,234,124 records',s[0]),('interchange','The SAME23 UP changes only the13 curve',s[1]),('gathered','Actual13,234,124 match the cyclic lantern',s[2]),('after','Named lantern reaches round1234 and24',s[3]))


def picture(stage,title):
    svg=panel(stage,title).replace('two actual half twists','no half twists').replace('Gold = half-twist arc.','Highlight = lantern factors.')
    # Python3.12 uses compensated float summation; keep this new panel's
    # OUTER canvas dimension byte-stable with older supported runtimes.
    # Every inner source support/grid remains unchanged.
    def outer_canvas(match):
        value=format(float(match.group(1)),'.6f').rstrip('0').rstrip('.')
        return '<svg xmlns="http://www.w3.org/2000/svg" width="560" height="'+value+'" viewBox="0 0 560 '+value+'"'
    svg,count=re.subn(r'<svg xmlns="http://www.w3.org/2000/svg" width="560" height="([0-9.]+)" viewBox="0 0 560 [0-9.]+"',outer_canvas,svg,count=1)
    if count!=1:raise ValueError('Stabilize only the outer comparison canvas')
    for raw in stage['factors']:
        name=raw['id']
        if name in ('reflected.loan.1','reflected.loan.2','alternative.prepare.F5.1','alternative.prepare.F5.2') or name.startswith('upper.'):
            svg,n=re.subn(r'(<g data-factor="'+re.escape(name)+r'"><rect[^>]*fill=)"#f4f7fa"',r'\1"#fff3cf"',svg)
            if n!=1:raise ValueError('Highlight each actual selected record once')
    return svg


def build():
    r,items=pictures();OUT.mkdir(exist_ok=True);figures=[]
    for name,title,stage in items:
        write_utf8(OUT/(name+'.svg'),picture(stage,title));figures.append('<figure><figcaption>'+title+'</figcaption><a href="'+name+'.svg">Open full-size SVG</a><img src="'+name+'.svg" alt="'+title+'"></figure>')
    before=r['route']['before_score'];after=r['route']['after_score'];mb=r['before_closed_matrix'];ma=r['after_closed_matrix']
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>An actual upper-root cabled lantern contracts</title><style>*{box-sizing:border-box}body{margin:0;background:#eef3f6;color:#18344a;font:16px/1.5 system-ui}main{max-width:1200px;margin:auto;padding:20px}.panels{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:white;padding:10px;min-width:0}img{width:100%;height:auto;display:block}figcaption{font-weight:700}.scope{border-left:5px solid #b9872d;background:#fff3cf;padding:14px}a{color:#086aa2}@media(max-width:850px){.panels{grid-template-columns:1fr}main{padding:12px}}</style><main><h1>The actual13,234,124 cabled lantern contracts</h1><p class="scope">Reached research continuation only. The preferred complete derivation stays unchanged. Three positive disk moves carry the SAME23 upward once across13, choose an explicit cyclic start at the changed13, and contract the actual adjacent13,234,124 by their individually matched cabled PC lantern. The output is a round1234 outer and its actual24 pair.</p><p>The23 record stays literally fixed. Its one crossing changes only13; no intermediate gather is assumed. The common internal chart fixes the actual round234 root, and every ordered input and output matches separately. The retained canonical proof includes the Delta4 reflection, every generator identity, its source named unit relation, full cyclic common conjugations and an internal positive interchange. Raw free-word equalities precede normalized individual presentations. Full signed PC balances, local disk/sphere/lift checks and nonabelian kernels with shadows stay retained.</p><p>Both existing UNIT exteriors remain separate and visible, each with chosen lift-I. All remaining donor petals are explicit; the source125 root stays intact. No half twist, negative factor, sphere redraw or cap appears. This is not a shorter or adopted complete proof, and no useful complete suffix join is claimed.</p>'''
    html+='<p>The input has14 records and the endpoint13. Support maximum stays'+str(before['max_support_word'])+' to'+str(after['max_support_word'])+', total'+str(before['total_support_word'])+' to'+str(after['total_support_word'])+'; stored braid letters'+str(before['braid_letters'])+' to'+str(after['braid_letters'])+'. CLOSED sum'+str(mb['total'])+' to'+str(ma['total'])+', maximum'+str(mb['maximum'])+' to'+str(ma['maximum'])+'. The actual inventories differ, so these descriptive totals are not entrywise dominance, arc crossings, jointly minimal drawings or whole-proof bounds.</p>'
    html+='''<p>All points use the same unnumbered six-point grid at24px pitch and1.68px radius. These are individual supports. <a href="../six-seven-posthalf-upper-cabled.json">Exact moves, charts and kernels</a> &middot; <a href="../six-seven-posthalf-upper-cabled.md">Research explanation</a> &middot; <a href="../six-seven-fifty-blocks/index.html?phase=clearfull&amp;step=0">Unchanged preferred derivation</a></p><div class="panels">'''
    write_utf8(OUT/'index.html',html+''.join(figures)+'</div></main></html>');print('Saved four exact panels;55 factor grids')


if __name__=='__main__':build()