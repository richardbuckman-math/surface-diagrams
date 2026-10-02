"""Identity cut-system chart for a certified six-punctured sphere action.

The sixth puncture is at infinity. Removing the certified common inner
conjugation changes the common basepoint path. The resulting five based
meridian images are checked to be standard before their arcs are routed by
the shared noninterleaving planar renderer.
"""
from collections import Counter
from functools import lru_cache

from .based_cut_system import based_arc_from_meridian
from .braid_actions import inverse_word,reduce_word
from .curves import MAX_ROUTE_NODES
from .model import PlanarSurface,Style
from .svg import render_svg
from .sphere_actions import sphere_inner_certificate
from .visuals import ColoredCurve,PlanarDiagram,RAINBOW


def sphere_chart_drawing(braid):
    """Return (SVG, removed common whisker), or a precise chart limitation."""
    return _cached_chart(tuple(braid))


@lru_cache(maxsize=24)
def _cached_chart(braid):
    certificate=sphere_inner_certificate(braid)
    if not certificate['certified']:
        raise ValueError('The sphere outer action has no identity certificate for this chart')
    images=certificate['images'][:5]
    whisker=certificate['conjugator']
    normalized=tuple(reduce_word(inverse_word(whisker)+image+whisker) for image in images)
    if normalized!=tuple((i,) for i in range(1,6)):
        raise ValueError('Normalized sphere action did not recover the standard meridians')
    arcs=tuple(based_arc_from_meridian(image,points=5) for image in normalized)
    if sum(len(arc.cuts)+2 for arc in arcs)>MAX_ROUTE_NODES:
        raise ValueError('Normalized five-arc chart exceeds the 1024-node route limit')
    visits=max(Counter(cut for arc in arcs for cut in arc.cuts).values(),default=0)
    scale=max(1.,((visits+1)*4+10)/50)
    surface=PlanarSurface.row('PPPPP',spacing=50*scale,height=220*scale,margin=55*scale)
    diagram=PlanarDiagram(surface,tuple(ColoredCurve(f'x{i+1}',arc,RAINBOW[i])
                                        for i,arc in enumerate(arcs)))
    return render_svg(diagram,style=Style(curve_width=1.5,marked_point_radius=3.5)),whisker
