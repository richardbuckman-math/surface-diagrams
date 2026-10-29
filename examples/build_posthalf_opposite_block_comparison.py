"""Four source-exact panels for the complete opposite-block closure."""
from pathlib import Path
import json
from examples.build_posthalf_hybrid_rose_comparison import picture
from examples.build_half_neighborhood_comparison import write_utf8
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/proofs/posthalf-opposite-block-comparison'

def pictures():
    r=json.loads((ROOT/'docs/proofs/six-seven-posthalf-opposite-block.json').read_bytes())
    s=r['route']['stages']
    return r,(('before','Common input: three visible exteriors',s[0]),
              ('older','Older late closure: support peak18',r['older_late_stage']),
              ('opposite','Opposite block: support peak12',s[16]),
              ('after','Four standard unit exteriors remain',s[17]))

def build():
    r,items=pictures();OUT.mkdir(exist_ok=True)
    figures=[]
    for name,title,stage in items:
        write_utf8(OUT/(name+'.svg'),picture(stage,title))
        figures.append('<figure><figcaption>'+title+'</figcaption><a href="'+name+'.svg">Open full-size SVG</a><img src="'+name+'.svg" alt="'+title+'"></figure>')
    html = """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Opposite block: a lower local support peak</title><style>*{box-sizing:border-box}body{margin:0;background:#eef3f6;color:#18344a;font:16px/1.5 system-ui}main{max-width:1200px;margin:auto;padding:20px}.panels{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:white;padding:10px;min-width:0}img{width:100%;height:auto;display:block}figcaption{font-weight:700}.scope{border-left:5px solid #b9872d;background:#fff3cf;padding:14px}a{color:#086aa2}@media(max-width:850px){.panels{grid-template-columns:1fr}main{padding:12px}}</style><main><h1>A lower local support peak, with mixed late curves</h1><p class="scope">Complete research comparison only. The preferred 101-move/71-step derivation remains unchanged. Both closures start at the SAME reached eleven-record third-exterior configuration and end at four separately visible standard unit exteriors.</p><p>The actual ordered R134 then round12 block moves DOWN across six neighbors. For each neighbor, round12 crosses first and R134 second. Both actors remain literal, and both intervening exteriors are explicitly checked. All four actual residual inputs then match a PC daisy. Commute one exterior and the new four-point outer; every input of the final cyclic modified D5 daisy matches in the FULL actual ordered-block chart.</p><p>The new closure takes17 positive disk operations and17 external adjacent checks, versus16 and15 in the saved closure. Its main-and-atomic support-word peak is12 instead of18. The displayed older late state itself has maximum12; its peak18 occurs earlier. The new late eight-record state has maximum/total support12/49 and134 stored braid letters; the older state has12/51 and108 letters. Both have CLOSED sum/maximum20/2.</p><p>The four outside pair curves have old/new support lengths10/6,12/8,6/4,4/12. Three shorten, while the other35 grows substantially. This is not uniform clarity improvement. Individual support words and pairwise minimal CLOSED intersections are not arc crossings, jointly attainable drawings or whole-proof tangle bounds. All halves were already gone.</p><p>Every crossing is bounded before application and reconstructed as a raw word before normalization. Both actual named substitutions retain all inputs/outputs, framing balances, full disk discrepancies, separate sphere/lift checks, and complete nonabelian kernels AND shadows. The internal cyclic daisy retains its full raw common conjugation and independent output invariance. No global frame or sphere move is added. Each terminal unit exterior has lift-I; the checked fourth-power combine, sphere redraw and cleanup remain separate and unapplied.</p><p>All grids have six UNNUMBERED points at24px pitch and1.68px effective radius. These are individual supports, not a joint-cut drawing.</p><p><a href="../six-seven-posthalf-opposite-block.json">Exact proof and full kernels</a> · <a href="../six-seven-posthalf-opposite-block.md">Research explanation</a> · <a href="../six-seven-fifty-blocks/index.html?phase=clearfull&amp;step=0">Unchanged preferred derivation</a></p><div class="panels">"""
    write_utf8(OUT/'index.html',html+''.join(figures)+'</div></main></html>')
    print('Saved four panels,31 six-point grids,186 unnumbered points')
if __name__=='__main__':build()
