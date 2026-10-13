"""Render the three checked five-point columns of thesis Figure 4.5.

Run with ``PYTHONPATH=src python examples/build_four_three_thesis_first_stage.py``.
The page is static, so GitHub Pages can display its exact cut certificates
without starting the interactive Python worker.
"""

from html import escape
from pathlib import Path

from surface_diagrams.boundary_playground_geometry import support_curve
from surface_diagrams.model import PlanarSurface, Style
from surface_diagrams.normal_cut_preview import render_normal_cut_preview
from surface_diagrams.svg import render_svg
from surface_diagrams.thesis_four_three import (
    CYCLIC_ROWS, FIRST_ROWS, REARRANGED_ROWS, check_stage,
)
from surface_diagrams.visuals import ColoredCurve, PlanarDiagram


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs' / 'proofs' / 'four-three-thesis-first-stage.html'
SURFACE = PlanarSurface.row('PPPPP', spacing=56, height=150, margin=58)
STYLE = Style(curve_width=2.1, marked_point_radius=4)


def support_svg(row):
    curves = tuple(ColoredCurve(factor.name, support_curve(factor.twist, 5),
                                '#188747' if factor.exponent < 0 else '#c218a5')
                   for factor in row)
    return render_svg(PlanarDiagram(SURFACE, curves), style=STYLE,
                      mirror_curve_paths_vertical=True)


def column_html(title, rows, subtitle):
    certificates = check_stage(rows)
    cards = []
    for index, row in enumerate(rows, 1):
        certificate = certificates[index]
        cuts = ''.join(
            f'<div class="cut-svg" data-projection="{projection}"'
            + (' hidden' if projection != 'strip' else '') + '>'
            + render_normal_cut_preview(certificate, projection=projection,
                                        mirror_vertical=True) + '</div>'
            for projection in ('strip', 'smooth', 'fan'))
        names = ' · '.join(factor.name for factor in row)
        count = sum(len(arc.cuts) for arc in certificate.arcs)
        cards.append(f'<article class="factor-row"><h3>After row {index}: '
                     f'{escape(names)}</h3><div class="panels">'
                     f'<div class="support" aria-label="Planar twist supports">'
                     f'{support_svg(row)}</div>'
                     f'<div class="cut" aria-label="Five-arc disk cut complex">'
                     f'{cuts}</div></div><p>{count} cut visit{ "" if count == 1 else "s"} · five jointly '
                     f'certified arcs, including the boundary-to-first arc</p></article>')
    return (f'<section class="column"><h2>{escape(title)}</h2>'
            f'<p>{escape(subtitle)}</p>'
            + ''.join(cards) + '</section>')


def build_html():
    left = column_html('1 · Reduced daisy', FIRST_ROWS,
                       'Top row acts first; green T45^-2 is a negative square.')
    middle = column_html('2 · Cyclic row rotation', CYCLIC_ROWS,
                         'The disjoint top pair moves to the bottom.')
    right = column_html('3 · Rearrange points 1 and 3', REARRANGED_ROWS,
                        'The braid β = σ1 σ2 σ1 changes the chart, not the factor count.')
    return ('''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Checked first stage · Baykur–Korkmaz (4,3)</title>
<style>
  :root{font:15px/1.45 system-ui,Segoe UI,sans-serif;color:#173149;background:#eaf1f5}
  *{box-sizing:border-box}body{margin:0}header{background:white;padding:20px max(18px,calc((100vw - 1100px)/2));border-bottom:1px solid #c5d4e1}
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
<h1>Baykur–Korkmaz (4,3): first checked thesis move</h1>
<p>These are the three columns of <a href="../figures/four-three-thesis/fig-4-5.png">thesis Figure 4.5</a>. A reduced daisy factorization of the five-point disk’s exterior boundary twist is cyclically rotated, then the first and third marked points are rearranged. All three products have the same <strong>exact disk braid action</strong> as the exterior twist, on all five meridians.</p>
<div class="controls"><button id="previous" type="button">← Previous column</button><button id="next" type="button">Next column →</button>
<label>Cut drawing <select id="projection"><option value="strip">Vertical rays</option><option value="smooth">Smooth curves</option><option value="fan">Fan</option></select></label>
<span id="position" role="status">Column 1 of 3</span></div></header>
<main class="strip" id="strip" tabindex="0" aria-label="Three checked columns from thesis Figure 4.5">'''
    + left + '<div class="arrow" aria-hidden="true">→<small>cyclic<br>rotation</small></div>'
    + middle + '<div class="arrow" aria-hidden="true">→<small>chart β</small></div>'
    + right + '''</main>
<div class="notes"><p><strong>Certificate:</strong> every displayed cut complex has a joint normal-strand certificate for the boundary-to-1-to-2-to-3-to-4-to-5 chain. The point-to-point arcs return to their reference positions after four rows; the boundary arc records the remaining exterior twist. The three cut layouts display the same crossing orders. Smooth curves are a presentation choice, not a separate geometric minimality proof.</p>
<p>The green support is <em>T45 inverse squared</em>. The first column’s under-going three-point curves use conjugators −2 and (−1, −2). Products read bottom-to-top algebraically because the thesis’s top row acts first. The cyclic arrow is checked by exact disk action. The third column is the simultaneous conjugation by β = σ1σ2σ1 shown in Figure 4.6; every corresponding factor is checked as a based disk action. The later half-lantern and Hurwitz arrows in <a href="four-three-thesis-storyboard.html">the source storyboard</a> remain unverified. This is separate from the Xiao (4,3) lab.</p></div>
<script>
 const strip=document.getElementById('strip'),columns=[...strip.querySelectorAll('.column')];
 const position=document.getElementById('position');
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
