"""A checked braid-word replacement displayed using supplied support panels."""
from pathlib import Path
from surface_diagrams import (PlanarSurface, Loop, Panel, FactorPanel,
    FactorizationDiagram, Figure, save_svg, save_tikz)
from surface_diagrams.braid_actions import substitute_factors


def example():
    twist=(3,4)*3
    replacement=substitute_factors(6,(twist*2,),0,1,(twist,twist))
    surface=PlanarSurface.row('PPPPPP',spacing=40,height=140,margin=45)
    support=Panel(surface.with_curves(Loop((2,5))),'Support: points 3, 4, 5')
    before=FactorizationDiagram((FactorPanel('F1',support,exponent=2,
        braid_word=twist*2),),strands=6,braid_crossing_style='smooth')
    after=FactorizationDiagram(tuple(FactorPanel(f'F1{chr(97+i)}',support,
        braid_word=word) for i,word in enumerate(replacement)),
        strands=6,braid_crossing_style='smooth')
    return Figure(((Panel(before,'Before: squared twist'),
        Panel(after,'After: two twists; replacement checked independently')),))


if __name__=='__main__':
    output=Path('.preview')
    output.mkdir(exist_ok=True)
    save_svg(example(),output/'verified-twist-split.svg')
    save_tikz(example(),output/'verified-twist-split.tikz')
