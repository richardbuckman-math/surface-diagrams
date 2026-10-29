"""Six source-exact panels for the local benefit and late hybrid tradeoff."""
from pathlib import Path
import json
import re
from examples.build_half_neighborhood_comparison import panel, write_utf8
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/proofs/posthalf-hybrid-rose-comparison'


def pictures():
    r = json.loads((ROOT / 'docs/proofs/six-seven-posthalf-hybrid-rose.json').read_bytes())
    prior = json.loads((ROOT / 'docs/proofs/six-seven-posthalf-third-exterior.json').read_bytes())
    a, b = r['third_exterior_route']['stages'], r['closure_route']['stages']
    return r, (('before', 'Common input: two visible exteriors', a[0]),
               ('outer', 'The actual four-point outer is reached', a[6]),
               ('older-third', 'Earlier route: first third exterior', prior['route']['stages'][7]),
               ('third', 'New route: first third exterior', a[9]),
               ('late', 'Late closure: eight records retangle', b[14]),
               ('after', 'Four standard unit exteriors remain', b[16]))


def picture(stage, title):
    svg = panel(stage, title).replace('two actual half twists', 'no half twists')
    svg = svg.replace('Gold = half-twist arc.', 'Every row is an actual closed-curve support.')
    def stable(match):
        value = format(float(match.group(1)), '.6f').rstrip('0').rstrip('.')
        return '<svg xmlns="http://www.w3.org/2000/svg" width="560" height="' + value + '" viewBox="0 0 560 ' + value + '"'
    svg, count = re.subn(r'<svg xmlns="http://www.w3.org/2000/svg" width="560" height="([0-9.]+)" viewBox="0 0 560 [0-9.]+"', stable, svg, count=1)
    if count != 1:
        raise ValueError('Stabilize only the outer canvas across Python versions')
    return svg


def build():
    r, items = pictures()
    OUT.mkdir(exist_ok=True)
    figures = []
    for name, title, stage in items:
        write_utf8(OUT / (name + '.svg'), picture(stage, title))
        figures.append('<figure><figcaption>' + title + '</figcaption><a href="' + name + '.svg">Open full-size SVG</a><img src="' + name + '.svg" alt="' + title + '"></figure>')
    html = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>A rose-loan hybrid: local benefit and late tradeoff</title><style>*{box-sizing:border-box}body{margin:0;background:#eef3f6;color:#18344a;font:16px/1.5 system-ui}main{max-width:1200px;margin:auto;padding:20px}.panels{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:white;padding:10px;min-width:0}img{width:100%;height:auto;display:block}figcaption{font-weight:700}.scope{border-left:5px solid #b9872d;background:#fff3cf;padding:14px}a{color:#086aa2}@media(max-width:850px){.panels{grid-template-columns:1fr}main{padding:12px}}</style><main><h1>A clearer third-exterior checkpoint, with a longer late closure</h1><p class="scope">Research comparison only. The preferred complete 101-move/71-step derivation stays unchanged. Both third-exterior routes start at the SAME reached upper-cabled 13-record input. The older route takes seven positive disk moves; the new rose-loan route takes nine. Each third-exterior panel is the first actual configuration with three separately visible standard unit exteriors.</p><p>The actual125 rose lends round12 across only the commuting exterior and45. The SAME12 contracts with the older15/25 into a125 root near the residual134 block. Its separate internal(+1) rose supplies the exactNEW15. The matched four-point PC daisy creates actualO1345. CommuteI24 and carry the changed25 once; all three actual1234/1345/25 inputs then match the cabled PC lantern in chart(-2,-3), including its retained internal interchange. The original donor stays two actual15/25 petals, distinct from the older units that were consumed.</p><p>At the third exterior, both routes have11 rows. The older route has maximum/total support7/44,126 stored braid letters,CLOSED118/14. The new route has6/40,108,CLOSED62/6. Inventories and classes differ: these are descriptive comparisons, not entrywise dominance, arc crossings, jointly minimal drawings or whole-proof tangle bounds. All halves were already gone at the common input.</p><p>The new route also has an explicit SIXTEEN-move/FIFTEEN-external-check named closure to four standard exteriors. Its ordered23/I24 block changes all six crossed neighbors, reaches a full four-point daisy, then a modifiedD5daisy. The late eight-record picture retangles several curves: maximum support12, with a transient peak18. This late cost prevents a uniform clarity claim or adoption of the full hybrid. No arbitrary deletion or cap replaces those named steps.</p><p>Every actual named input/output, signed PC balance, full raw cyclic common conjugation, reconstructed adjacent move, separate disk/sphere/lift certificate and complete nonabelian kernel AND shadow remains explicit. All four terminal unit exteriors have chosen lift-I. Their combine, checked FOURTH-power sphere redraw and cleanup remain separate; no unit exterior is capped. All points use the same unnumbered six-point grid at24px pitch and1.68px radius. Individual supports are not a joint-cut drawing.</p><p><a href="../six-seven-posthalf-hybrid-rose.json">Exact route, source hashes and full kernels</a> · <a href="../six-seven-posthalf-hybrid-rose.md">Research explanation</a> · <a href="../six-seven-fifty-blocks/index.html?phase=clearfull&amp;step=0">Unchanged preferred derivation</a></p><div class="panels">'''
    write_utf8(OUT / 'index.html', html + ''.join(figures) + '</div></main></html>')
    print('Saved six panels,59 grids,354 unnumbered points')


if __name__ == '__main__':
    build()
