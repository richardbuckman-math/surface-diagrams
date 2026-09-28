"""Audit the user's confirmed factor-9 arc against the earlier SVG conjugator."""
from dataclasses import asdict
import json
from pathlib import Path

from surface_diagrams import Arc, PlanarSurface, BraidDiagram, Figure, Panel, save_svg, save_tikz
from surface_diagrams.braid_actions import audit_arc_transport, inverse_word


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
                braid_word=word,scope='Anchored endpoint transport only; not full PDF verification')
    (output/'factor-nine-transport-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    save_svg(figure,output/'factor-nine-transport-audit.svg')
    save_tikz(figure,output/'factor-nine-transport-audit.tikz')
    print('Factor 9 transport matches; wrote SVG, TikZ and exact JSON evidence to .preview')


if __name__=='__main__':
    main()
