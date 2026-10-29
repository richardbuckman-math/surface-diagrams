"""Fixed-milestone visual comparison of two complete positive post-half routes."""
from pathlib import Path
import json,re
from examples.build_half_neighborhood_comparison import panel,write_utf8
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/proofs/posthalf-route-comparison'


def pictures():
    r=json.loads((ROOT/'docs/proofs/six-seven-posthalf-route-comparison.json').read_text(encoding='utf-8'))
    return r,tuple((p['name'],p['title'],p['stage']) for p in r['panels'])


def picture(stage,title):
    svg=panel(stage,title).replace('two actual half twists','no half twists').replace('Gold = half-twist arc.','Gold = standard exterior.')
    def stable(match):
        v=format(float(match.group(1)),'.6f').rstrip('0').rstrip('.')
        return '<svg xmlns="http://www.w3.org/2000/svg" width="560" height="'+v+'" viewBox="0 0 560 '+v+'"'
    svg,n=re.subn(r'<svg xmlns="http://www.w3.org/2000/svg" width="560" height="([0-9.]+)" viewBox="0 0 560 [0-9.]+"',stable,svg,count=1)
    if n!=1:raise ValueError('Keep only the outer canvas decimal stable')
    for f in stage['factors']:
        if f['points']==5 and not f['half']:
            svg,n=re.subn(r'(<g data-factor="'+re.escape(f['id'])+r'"><rect[^>]*fill=)"#f4f7fa"',r'\1"#fff3cf"',svg)
            if n!=1:raise ValueError('Highlight each separately visible standard exterior')
    return svg


def build():
    r,items=pictures();OUT.mkdir(exist_ok=True);figures=[]
    for name,title,s in items:
        write_utf8(OUT/(name+'.svg'),picture(s,title));figures.append('<figure><figcaption>'+title+'</figcaption><a href="'+name+'.svg">Open full-size SVG</a><img src="'+name+'.svg" alt="'+title+'"></figure>')
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Compare the complete post-half routes</title><style>*{box-sizing:border-box}body{margin:0;background:#eef3f6;color:#18344a;font:16px/1.5 system-ui}main{max-width:1200px;margin:auto;padding:20px}.panels{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:white;padding:10px;min-width:0}img{width:100%;height:auto;display:block}figcaption{font-weight:700}.scope{border-left:5px solid #b9872d;background:#fff3cf;padding:14px}a{color:#086aa2}table{border-collapse:collapse;width:100%;background:white}th,td{padding:8px;border:1px solid #bccad4;text-align:left}@media(max-width:850px){.panels{grid-template-columns:1fr}main{padding:12px}}</style><main><h1>Two complete routes, compared at the same milestones</h1><p class="scope">The preferred derivation stays unchanged. Both routes start from the SAME actual post-half tuple and end at FOUR individually matched standard unit exteriors. This comparison fixes the first configuration with one, two and three visible standard exteriors on each route; it does not select favorable intermediate snapshots.</p><p>The alternative's second-exterior configuration is substantially less crowded and its longest support word is7 instead of18. The preferred route has fewer rows and shorter words at the third exterior. The first-exterior comparison is mixed. There is no uniform dominance and no half-arc simplification: all halves have already disappeared at the common input.</p><table><tr><th>Matched-tail quantity</th><th>Preferred</th><th>Alternative</th></tr><tr><td>Listed source operations</td><td>40</td><td>61</td></tr><tr><td>External adjacent checks</td><td>67</td><td>41</td></tr><tr><td>Peak factor rows</td><td>18</td><td>19</td></tr><tr><td>Peak individual support word</td><td>18</td><td>18</td></tr><tr><td>Peak total support word</td><td>147</td><td>132</td></tr><tr><td>Peak stored braid letters</td><td>258</td><td>290</td></tr></table><p>Support words and stored braid presentations are chart-specific. Total support length is unweighted across actual factor records: a square occupies one curve row. It is not an arc or interaction count. External adjacent checks exclude the internal checks retained inside every named rule, so this is not a claim of less total atomic verification work. Unique exact tuples in the report count retained presentations, not geometric classes.</p><p><strong>Current decision:</strong> keep the preferred presentation while seeking a hybrid. The alternative improves the middle configuration, but its late configuration has more rows and more visible winding. This is a clarity decision based on the panels and their tradeoffs, not a preference for fewer step labels.</p><p>The selected CLOSED-neighborhood matrices retain full exact normal-form certificates. Their differing inventories prevent entrywise dominance claims. Pairwise minimum intersections are not arc crossings or a jointly attainable minimum drawing. Individual support panels are not simultaneous joint-cut certificates. Both complete proofs remain solved; no new preferred payload, PDF or parallel-step count is claimed here.</p><p>The six panels use identical unnumbered six-point grids at24px pitch and1.68px radius, with unchanged curve style. Gold highlights each separately visible standard exterior. <a href="../six-seven-posthalf-route-comparison.json">Exact source addresses, metrics, full kernels and CLOSED matrices</a> &middot; <a href="../six-seven-posthalf-route-comparison.md">Comparison notes</a> &middot; <a href="../six-seven-fifty-blocks/index.html?phase=clearfull&amp;step=0">Unchanged preferred derivation</a></p><div class="panels">'''
    write_utf8(OUT/'index.html',html+''.join(figures)+'</div></main></html>');print('Saved six fixed-milestone panels')


if __name__=='__main__':build()