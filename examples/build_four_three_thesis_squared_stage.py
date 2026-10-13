"""Render the checked squared-boundary and PC half-lantern disk stages."""

from pathlib import Path

from examples.build_four_three_thesis_first_stage import column_html
from surface_diagrams.thesis_four_three import (
    CONCATENATED_ROWS, HALF_LANTERN_ROWS, PAIRABLE_ROWS, ROTATED_ROWS,
    SQUARED_ROWS,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs' / 'proofs' / 'four-three-thesis-squared-stage.html'


def build_html():
    first = column_html('1 · Concatenate two boundary factorizations',
                        CONCATENATED_ROWS,
                        'Figure 4.7 begins with the third, then second, Figure 4.5 column.',
                        outer_power=2)
    rotated = column_html('2 · Rotate the last row to the top', ROTATED_ROWS,
                          'Inserted exact intermediate: the full exterior-square product is central.',
                          outer_power=2)
    combined = column_html('3 · Combine the top pair', SQUARED_ROWS,
                           'The two T123 factors form T123^2; the two green inverse squares form T45^-4.',
                           outer_power=2)
    pairable = column_html('4 · Place the two inverse squares', PAIRABLE_ROWS,
                           'The T45 correction commutes through these supports; each green square now follows a three-point twist.',
                           outer_power=2)
    halves = column_html('5 · Apply PC half lantern twice', HALF_LANTERN_ROWS,
                         'Each three-point twist followed by its T45 inverse square becomes two positive arc half twists.',
                         outer_power=2)
    return ('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Checked squared-boundary stage · Baykur–Korkmaz (4,3)</title>
<style>
  :root{font:15px/1.45 system-ui,Segoe UI,sans-serif;color:#173149;background:#eaf1f5}*{box-sizing:border-box}body{margin:0}
  header{background:white;padding:20px max(18px,calc((100vw - 1100px)/2));border-bottom:1px solid #c5d4e1}
  h1{font-size:clamp(23px,3vw,34px);margin:4px 0 8px}header p{max-width:980px;margin:6px 0}a{color:#145b91}
  .eyebrow{font-size:11px;letter-spacing:.13em;text-transform:uppercase;color:#33748c;font-weight:700}
  .controls{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:14px}
  button,select{font:inherit;padding:7px 10px;border:1px solid #91aec4;border-radius:6px;background:white;color:#174c73}
  button{cursor:pointer}button:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid #1689bc;outline-offset:2px}
  .strip{display:flex;align-items:flex-start;gap:18px;overflow-x:auto;scroll-snap-type:x mandatory;padding:18px max(18px,calc((100vw - 1100px)/2)) 25px}
  .column{flex:0 0 min(1030px,calc(100vw - 36px));scroll-snap-align:center;background:white;border:1px solid #c6d8e4;border-radius:12px;padding:16px}
  .column h2{margin:0 0 3px;font-size:21px}.column>p{margin:0 0 13px;color:#546a7b}
  .factor-row{border-top:1px solid #d6e1e9;padding:12px 0}.factor-row h3{font-size:16px;margin:0 0 8px}.factor-row p{font-size:12px;color:#587184;margin:6px 0 0}
  .panels{display:grid;grid-template-columns:42% 58%;gap:10px;align-items:center}.support,.cut{min-width:0}.support svg,.cut svg{width:100%;height:225px;display:block}
  .cut-svg[hidden]{display:none}.arrow{flex:0 0 70px;align-self:stretch;display:flex;flex-direction:column;justify-content:center;align-items:center;font-size:34px;color:#216b9a}.arrow small{font-size:12px;text-align:center}
  .notes{max-width:1100px;margin:0 auto 35px;padding:0 18px;color:#415970}.notes p{margin:8px 0}
  @media(max-width:650px){.panels{grid-template-columns:1fr}.arrow{display:none}}
</style>
<header><div class="eyebrow">Surface diagrams · exact five-strand checkpoint</div>
<h1>Baykur–Korkmaz (4,3): square the boundary twist</h1>
<p>The first column of <a href="../figures/four-three-thesis/fig-4-7.png">thesis Figure 4.7</a> concatenates two checked factorizations of the five-point exterior boundary twist. We expose the cyclic rotation and move the negative squares into pairs before applying the puncture-capped half lantern twice. All five columns have the exact disk action of the <strong>squared exterior twist</strong> on all five meridians.</p>
<div class="controls"><button id="previous" type="button">← Previous column</button><button id="next" type="button">Next column →</button>
<label>Cut drawing <select id="projection"><option value="strip">Vertical rays</option><option value="smooth">Smooth curves</option><option value="fan">Fan</option></select></label>
<span id="position" role="status">Column 1 of 5</span></div></header>
<main class="strip" id="strip" tabindex="0" aria-label="Five checked squared-boundary columns">'''
    + first + '<div class="arrow" aria-hidden="true">→<small>cyclic<br>rotation</small></div>'
    + rotated + '<div class="arrow" aria-hidden="true">→<small>combine<br>commuting twists</small></div>'
    + combined + '<div class="arrow" aria-hidden="true">→<small>commute<br>corrections</small></div>'
    + pairable + '<div class="arrow" aria-hidden="true">→<small>PC half<br>lantern ×2</small></div>'
    + halves + '''</main>
<div class="notes"><p><strong>Certificate:</strong> each complete product is checked against T12345 squared as a based five-strand disk action. Every prefix yields five jointly certified cut arcs, including the boundary-to-first arc. The intermediate columns expose the cyclic and correction moves; the two three-point-plus-inverse-square pairs become four positive half twists by checked PC half lantern substitutions. These last two columns give one exact ordering of that step; they are not a factor-by-factor transcription of the thesis's third and fourth drawings. The smooth cut layout preserves the certified crossing order, but has no independent geometric minimality claim.</p>
<p><a href="four-three-thesis-first-stage.html">Review the three Figure 4.5 columns</a> · <a href="four-three-thesis-storyboard.html">See the original thesis storyboard</a>. The subsequent Hurwitz moves in Figure 4.8 remain to be individually certified.</p></div>
<script>
 const strip=document.getElementById('strip'),columns=[...strip.querySelectorAll('.column')],position=document.getElementById('position');
 function current(){const middle=strip.scrollLeft+strip.clientWidth/2;return columns.reduce((best,col,i)=>Math.abs(col.offsetLeft+col.offsetWidth/2-middle)<Math.abs(columns[best].offsetLeft+columns[best].offsetWidth/2-middle)?i:best,0)}
 function go(index){const col=columns[Math.max(0,Math.min(columns.length-1,index))];strip.scrollTo({left:col.getBoundingClientRect().left-strip.getBoundingClientRect().left+strip.scrollLeft-(strip.clientWidth-col.clientWidth)/2,behavior:'smooth'})}
 document.getElementById('previous').onclick=()=>go(current()-1);
 document.getElementById('next').onclick=()=>go(current()+1);
 strip.addEventListener('scroll',()=>{position.textContent=`Column ${current()+1} of ${columns.length}`},{passive:true});
 document.getElementById('projection').onchange=event=>document.querySelectorAll('.cut-svg').forEach(item=>{item.hidden=item.dataset.projection!==event.target.value});
</script></html>''')


if __name__ == '__main__':
    OUTPUT.write_text(build_html(), encoding='utf-8')
    print('Wrote', OUTPUT)
