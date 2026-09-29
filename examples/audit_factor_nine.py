"""Audit the user's confirmed factor-9 arc against the earlier SVG conjugator."""
from dataclasses import asdict
import json
import re
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

from surface_diagrams import Arc, PlanarSurface, BraidDiagram, Figure, Panel, save_svg, save_tikz
from surface_diagrams.braid_actions import audit_arc_transport, inverse_word, arc_ray_segments


def segment_overlay(svg, count):
    """Overlay the actual exported arc commands, without recomputing its route."""
    ns='http://www.w3.org/2000/svg'
    ET.register_namespace('',ns)
    root=ET.fromstring(svg)
    arcs=[p for p in root.findall(f'{{{ns}}}path') if p.get('class')=='arc']
    if len(arcs)!=1:
        raise ValueError('Expected one exported audit arc')
    arc=arcs[0]
    commands=re.findall(r'[MLA][^MLA]*',arc.get('d',''))
    if len(commands)!=count+1 or not commands[0].startswith('M'):
        raise ValueError('Exported arc does not match the audit segment count')
    previous=commands[0].split()[-2:]
    for i,command in enumerate(commands[1:]):
        overlay=ET.Element(f'{{{ns}}}path',{
            'id':f'segment-{i+1}','class':'audit-segment',
            'd':'M '+' '.join(previous)+' '+command.strip(),
            'fill':'none','stroke':'#b45309','stroke-width':'4',
            'stroke-linecap':'round','pointer-events':'none'})
        root.insert(list(root).index(arc)+1+i,overlay)
        previous=command.split()[-2:]
    return ET.tostring(root,encoding='unicode')


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
    inline=segment_overlay((output/'factor-nine-transport-audit.svg').read_text(encoding='utf-8'),len(report['segments']))
    locations=[f'point {arc.start}']+[f'gap {c}' for c in arc.cuts]+[f'point {arc.end}']
    table=''.join(f'<tr id="row-{i+1}"><td>{i+1}</td><td>{locations[i]} to {locations[i+1]}</td>'
                  f'<td>{"above" if (i%2==0)==arc.initial_up else "below"}</td>'
                  f'<td>{escape(str(letters)) if letters else "no rays"}</td></tr>'
                  for i,letters in enumerate(report['segments']))
    html=f'''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Factor 9: segment-by-segment audit</title>
<style>body{{font:17px/1.5 system-ui;max-width:980px;margin:2rem auto;padding:0 1rem}}
svg{{max-width:100%;height:auto;max-height:520px}}.audit-segment{{display:none}}
.audit-segment.selected{{display:inline}}tr.selected{{background:#fff0cc}}
select{{font:inherit;margin:.5rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #bbb;padding:.5rem;text-align:left}}
pre{{white-space:pre-wrap;overflow-wrap:anywhere}}summary{{cursor:pointer}}</style>
<h1>Factor 9: segment-by-segment audit</h1>
<p>The supplied arc matches the earlier SVG conjugator's endpoint transport.
This does not verify the other PDF factors or reconstruct the arc automatically.</p>
<label for="step">Highlight arc segment:</label><select id="step"><option value="0">None</option>
{''.join(f'<option value="{i+1}">Step {i+1}: {locations[i]} to {locations[i+1]}</option>' for i in range(len(report['segments'])))}</select>
<p id="selection" aria-live="polite">No segment selected.</p>
{inline}
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
<a href="factor-nine-transport-audit.tikz">TikZ drawing</a></p>
<script>
const picker=document.getElementById('step');
picker.addEventListener('change',()=>{{
  document.querySelectorAll('.selected').forEach(el=>el.classList.remove('selected'));
  const n=Number(picker.value);
  if(n){{
    document.getElementById('segment-'+n).classList.add('selected');
    const row=document.getElementById('row-'+n); row.classList.add('selected');
    document.getElementById('selection').textContent='Step '+n+': '+row.cells[1].textContent+
      '; '+row.cells[2].textContent+'; ray letters: '+row.cells[3].textContent;
  }} else document.getElementById('selection').textContent='No segment selected.';
}});
</script></html>'''
    (output/'factor-nine-transport-audit.html').write_text(html,encoding='utf-8')
    print('Factor 9 transport matches; wrote HTML, SVG, TikZ and JSON evidence to .preview')


if __name__=='__main__':
    main()
