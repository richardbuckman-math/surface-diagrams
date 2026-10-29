"""Source-exact third-exterior panels; the preferred complete proof is unchanged."""
from pathlib import Path
import json,re
from examples.build_half_neighborhood_comparison import panel,write_utf8
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/proofs/posthalf-third-exterior-comparison'


def pictures():
    r=json.loads((ROOT/'docs/proofs/six-seven-posthalf-third-exterior.json').read_text(encoding='utf-8'));s=r['route']['stages']
    return r,(('before','Input: two exteriors and the125 donor',s[0]),('changed','The SAME125 DOWN supplies the exact35',s[1]),('loan','Actual125 rose supplies both25 and15',s[2]),('shortside','The cyclic start chooses the short side',s[5]),('gathered','All FIVE actual D5 inputs are adjacent',s[6]),('after','A THIRD unit exterior remains visible',s[7]))


def picture(stage,title):
    svg=panel(stage,title).replace('two actual half twists','no half twists').replace('Gold = half-twist arc.','Highlight = daisy factors.')
    # Stabilize only the outer canvas across supported Python float sums.
    def outer_canvas(match):
        value=format(float(match.group(1)),'.6f').rstrip('0').rstrip('.')
        return '<svg xmlns="http://www.w3.org/2000/svg" width="560" height="'+value+'" viewBox="0 0 560 '+value+'"'
    svg,count=re.subn(r'<svg xmlns="http://www.w3.org/2000/svg" width="560" height="([0-9.]+)" viewBox="0 0 560 [0-9.]+"',outer_canvas,svg,count=1)
    if count!=1:raise ValueError('Stabilize only the outer comparison canvas')
    for raw in stage['factors']:
        name=raw['id']
        if name in ('reflected.inner125','reflected.output.1','upper.O1234','cyclic135.supply.2') or name.startswith('third.'):
            svg,n=re.subn(r'(<g data-factor="'+re.escape(name)+r'"><rect[^>]*fill=)"#f4f7fa"',r'\1"#fff3cf"',svg)
            if n!=1:raise ValueError('Highlight each selected actual record once')
    return svg


def build():
    r,items=pictures();OUT.mkdir(exist_ok=True);figures=[]
    for name,title,stage in items:
        write_utf8(OUT/(name+'.svg'),picture(stage,title));figures.append('<figure><figcaption>'+title+'</figcaption><a href="'+name+'.svg">Open full-size SVG</a><img src="'+name+'.svg" alt="'+title+'"></figure>')
    before=r['route']['before_score'];after=r['route']['after_score'];mb=r['before_closed_matrix'];ma=r['after_closed_matrix']
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>A matched cyclic daisy reaches a third exterior</title><style>*{box-sizing:border-box}body{margin:0;background:#eef3f6;color:#18344a;font:16px/1.5 system-ui}main{max-width:1200px;margin:auto;padding:20px}.panels{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:white;padding:10px;min-width:0}img{width:100%;height:auto;display:block}figcaption{font-weight:700}.scope{border-left:5px solid #b9872d;background:#fff3cf;padding:14px}a{color:#086aa2}@media(max-width:850px){.panels{grid-template-columns:1fr}main{padding:12px}}</style><main><h1>The actual cyclic D5 daisy reaches a third visible exterior</h1><p class="scope">Reached research continuation only. The preferred complete derivation stays unchanged. Seven positive disk moves carry the SAME125 root down across35, expand its individually matched internal rose, retain the new12, and gather by the commuting short side. Every actual ordered input of the final CYCLIC D5 daisy matches separately. Its output is a THIRD visible standard unit exterior.</p><p>The root carry changes35 to the exact required daisy petal and keeps the125 root literally fixed until its separate rose expansion. Both actual new25 and new15 match their required canonical petals. The new12 stays visible; it is not consumed or silently returned. The older125 loan petals remain separate positive units. All seven external adjacent checks are reconstructed before individual normalized presentations.</p><p>The final four petals followed by the1234 outer form the cyclic daisy. Its full internal inverse-prefix common conjugation is checked by raw free-word equality first; the standard D5 output invariance is independently verified. Both old unit exteriors remain visible and literal. Each of the THREE unit exteriors has chosen lift-I. The residual has boundary-one action and chosen lift-I, a diagnostic rather than a named residual closure. No half twist, negative factor, sphere redraw or cap is introduced.</p><p>A longer attempted gather through the winding134 curve rejects a candidate at support23 before application. That failed whole gather is not a reached partial route. The selected short-side gather crosses only the commuting23 pair and exterior, retaining both literally. Full signed PC balances, local disk/sphere/lift certificates, and complete nonabelian kernels and shadows remain explicit. This is not a shorter or adopted complete proof and no useful complete suffix join is claimed.</p>'''
    html+='<p>The initial35 change shortens its support6 to2, while three CLOSED pair counts increase and75 stay equal; total170 to182. This is a tradeoff, not entrywise untangling or a joint minimum.</p>'
    html+='<p>The input has13 records and the endpoint11. Support maximum '+str(before['max_support_word'])+' to'+str(after['max_support_word'])+', total'+str(before['total_support_word'])+' to'+str(after['total_support_word'])+'; stored braid letters'+str(before['braid_letters'])+' to'+str(after['braid_letters'])+'. CLOSED sum'+str(mb['total'])+' to'+str(ma['total'])+', maximum'+str(mb['maximum'])+' to'+str(ma['maximum'])+'. Inventories differ, so these descriptive totals are not entrywise dominance, arc crossings, jointly minimal drawings or whole-proof bounds.</p>'
    html+='''<p>All points use the same unnumbered six-point grid at24px pitch and1.68px radius. These are individual supports. <a href="../six-seven-posthalf-third-exterior.json">Exact moves, charts and kernels</a> &middot; <a href="../six-seven-posthalf-third-exterior.md">Research explanation</a> &middot; <a href="../six-seven-fifty-blocks/index.html?phase=clearfull&amp;step=0">Unchanged preferred derivation</a></p><div class="panels">'''
    write_utf8(OUT/'index.html',html+''.join(figures)+'</div></main></html>');print('Saved six exact panels;82 factor grids')


if __name__=='__main__':build()