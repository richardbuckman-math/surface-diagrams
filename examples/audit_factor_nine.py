"""Audit the user's confirmed factor-9 arc against the earlier SVG conjugator."""
from dataclasses import asdict
import json
from html import escape
from pathlib import Path

from surface_diagrams import Arc, PlanarSurface, BraidDiagram, Figure, Panel, save_svg, save_tikz
from surface_diagrams.braid_actions import audit_arc_transport, inverse_word, arc_ray_segments


def main():
    arc=Arc(1,4,(4,2,1,4,5,1,2,4,2),direction='down')
    conjugator=(-2,-3,4,2,-3,-2,-2)
    audit=audit_arc_transport(6,conjugator,1,arc)
    if not audit.matches:
        raise ValueError('Confirmed factor-9 transport comparison failed')
    word=conjugator+(1,)+inverse_word(conjugator)
    surface=PlanarSurface.row('PPPPPP',spacing=50,height=220,margin=55)
    figure=Figure(((
        Panel(surface.with_curves(arc),'Confirmed factor 9: supplied arc\nEndpoint transport comparison matches'),
        Panel(BraidDiagram(6,word,crossing_style='smooth',show_generators=True),
              'Earlier SVG conjugate half twist\nRead downward'),
    ),))
    output=Path('.preview')
    output.mkdir(exist_ok=True)
    report=dict(asdict(audit),matches=audit.matches,conjugator=conjugator,
                braid_word=word,segments=arc_ray_segments(6,arc),
                scope='Anchored endpoint transport only; not full PDF verification')
    (output/'factor-nine-transport-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    save_svg(figure,output/'factor-nine-transport-audit.svg')
    save_tikz(figure,output/'factor-nine-transport-audit.tikz')
    locations=[f'point {arc.start}']+[f'gap {c}' for c in arc.cuts]+[f'point {arc.end}']
    table=''.join(f'<tr><td>{i+1}</td><td>{locations[i]} to {locations[i+1]}</td>'
                  f'<td>{"above" if (i%2==0)==arc.initial_up else "below"}</td>'
                  f'<td>{escape(str(letters)) if letters else "no rays"}</td></tr>'
                  for i,letters in enumerate(report['segments']))
    html=f'''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Factor 9: segment-by-segment audit</title>
<style>body{{font:17px/1.5 system-ui;max-width:980px;margin:2rem auto;padding:0 1rem}}
img{{max-width:100%}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #bbb;padding:.5rem;text-align:left}}
pre{{white-space:pre-wrap;overflow-wrap:anywhere}}summary{{cursor:pointer}}</style>
<h1>Factor 9: segment-by-segment audit</h1>
<p>The supplied arc matches the earlier SVG conjugator's endpoint transport.
This does not verify the other PDF factors or reconstruct the arc automatically.</p>
<img src="factor-nine-transport-audit.svg" alt="Confirmed factor 9 arc beside its conjugate braid">
<h2>Read the arc from point 1 to point 4</h2>
<p>Gap c is between points c and c+1. Only upper segments cross the upward
puncture rays. Left-to-right crossings contribute positive letters; right-to-left
crossings contribute negative letters. Empty steps are retained below.</p>
<table><thead><tr><th>Step</th><th>From / to</th><th>Side of row</th><th>Ray letters</th></tr></thead><tbody>{table}</tbody></table>
<p>Concatenate the rows and freely cancel adjacent inverse letters to get:</p>
<pre>{escape(str(audit.transport))}</pre>
<details><summary>Inspect actual and expected endpoint words</summary>
<pre>{escape(json.dumps(asdict(audit),indent=2))}</pre></details>
<p><a href="factor-nine-transport-audit.json">Exact JSON evidence</a> ·
<a href="factor-nine-transport-audit.tikz">TikZ drawing</a></p></html>'''
    (output/'factor-nine-transport-audit.html').write_text(html,encoding='utf-8')
    print('Factor 9 transport matches; wrote HTML, SVG, TikZ and JSON evidence to .preview')


if __name__=='__main__':
    main()
