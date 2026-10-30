"""Six source-exact views of the retained-outer45 loan and return."""
from pathlib import Path
import json
from examples.build_posthalf_hybrid_rose_comparison import picture
from examples.build_half_neighborhood_comparison import write_utf8
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/proofs/preferred-late45-comparison'

def pictures():
    r=json.loads((ROOT/'docs/proofs/six-seven-preferred-late45.json').read_bytes());s=r['route']['stages']
    return r,(('before','Preferred input: two wound pair curves',s[0]),
              ('donor','The retained outer lends round 45',s[1]),
              ('carry','The SAME 45 has crossed all ten neighbors',s[3]),
              ('returned','The SAME source outer returns literally',s[5]),
              ('late','Four short pair curves meet the D5 daisy',s[7]),
              ('after','Four standard unit exteriors remain',s[8]))

def build():
    r,items=pictures();OUT.mkdir(exist_ok=True);figures=[]
    for name,title,stage in items:
        write_utf8(OUT/(name+'.svg'),picture(stage,title))
        figures.append('<figure><figcaption>'+title+'</figcaption><a href="'+name+'.svg">Open full-size SVG</a><img src="'+name+'.svg" alt="'+title+'"></figure>')
    html="""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Return the outer after borrowing 45</title><style>*{box-sizing:border-box}body{margin:0;background:#eef3f6;color:#18344a;font:16px/1.5 system-ui}main{max-width:1200px;margin:auto;padding:20px}.panels{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:white;padding:10px;min-width:0}img{width:100%;height:auto;display:block}figcaption{font-weight:700}.scope{border-left:5px solid #b9872d;background:#fff3cf;padding:14px}a{color:#086aa2}@media(max-width:850px){.panels{grid-template-columns:1fr}main{padding:12px}}</style><main><h1>Return the outer after borrowing 45</h1><p class="scope">This source-exact local route replaces the final three-move/two-check disk closure by eight positive disk moves/fourteen external adjacent checks. The preferred proposal has 90 source operations, 106 listed moves and 75 genuinely independent steps. The previous 101/71 edition is pinned byte-for-byte. This is a clarity choice, not a shorter proof.</p><p>The SAME retained four-point outer uses a checked internal inverse-generator chart to lend the actual round 45 full twist. All new factors remain full positive twists. Two explicit cyclic starts and a bounded carry take that SAME 45 across ALL TEN actual neighbors, including every donor leftover and the three earlier exteriors. The full changed donor daisy then returns the original outer LITERALLY.</p><p>Only two source pair curves change: their support lengths fall from 6 to 2 and 4 to 2. The other SIX source records remain literal; all 28 pairwise minimal CLOSED counts stay unchanged. The returned eight-record state has maximum/total support 5/27 and 88 stored braid letters, versus 6/33 and 96. The final four pair supports all have length 2.</p><p>The temporary donor has 11 rows rather than 8, with total support 42 rather than 33 and peak stored braid length 110. Its largest support word remains 6. The original donor chart gives peak 7; the inverse-full-generator chart also gives 6 but total 48. All three compared charts retain complete proofs and rejoin the same final tuple literally. The chosen inverse-generator chart changes no actual half-twist factor.</p><p>Every actual named input/output, raw adjacent reconstruction, full cyclic common word, signed PC balance, separate disk/sphere/lift certificate and complete nonabelian kernel AND B4 shadow is retained. The final D5 daisy keeps both internal canonical interchanges. Four odd standard unit exteriors remain visible until their separate combine, FOURTH-power sphere redraw and cleanup.</p><p>All 13 sphere-discrepancy words and the separate LEFT framing ledger remain unchanged. Individual supports and CLOSED pair minima are not joint drawings, arc crossings or whole-proof bounds. These 50 six-point grids/300 dots are UNNUMBERED at 24px pitch and 1.68px effective radius.</p><p><a href="../six-seven-preferred-late45.json">Full source certificate</a> · <a href="../six-seven-preferred-late45.md">Explanation and joins</a> · <a href="../six-seven-fifty-blocks/index.html?phase=clearfull&amp;step=0">Preferred graphical proposal</a> · <a href="../six-seven-fifty-blocks/half-meeting.html?phase=clearfull&amp;step=0">Pinned 101/71 edition</a></p><div class="panels">"""
    write_utf8(OUT/'index.html',html+''.join(figures)+'</div></main></html>')
    print('Saved six panels,50 six-point grids,300 unnumbered points')
if __name__=='__main__':build()
