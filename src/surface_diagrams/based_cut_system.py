"""Based meridian arcs for inspecting a six-point braid's prefix action.

These are arcs from the left outer rim to punctures, with a common basepoint.
Their upper-ray words encode based paths; the enclosing meridian image is
p x_j p^-1. The shared surface router still decides whether a simultaneous
noninterleaving drawing can be made within its stated limits.
"""
from collections import Counter
from functools import lru_cache

from .braid_actions import inverse_word, reduce_word
from .curves import Arc, MAX_ROUTE_NODES
from .model import PlanarSurface, Style
from .svg import render_svg
from .twist_supports import _ray_cuts
from .visuals import ColoredCurve, PlanarDiagram, RAINBOW


def based_arc_ray_word(arc, *, points=6):
    """Read upper-ray crossings of a left-rim-to-puncture Arc."""
    if not isinstance(arc, Arc) or arc.start != 0 or not 1 <= arc.end <= points:
        raise ValueError('Expected a left-rim-to-puncture arc')
    if arc.start_side is not None or arc.end_side is not None or any(c > points for c in arc.cuts):
        raise ValueError('Unsupported based-arc endpoint or cut')
    locations = (0,) + tuple(2*c+1 for c in arc.cuts) + (2*arc.end,)
    letters = []
    for index, (a, b) in enumerate(zip(locations, locations[1:])):
        if (index % 2 == 0) != arc.initial_up:
            continue
        crossed = [j for j in range(1, points+1) if min(a,b) < 2*j < max(a,b)]
        letters.extend(crossed if a < b else (-j for j in reversed(crossed)))
    return reduce_word(letters)


def based_arc_from_meridian(image, *, points=6):
    """Recover a bounded Arc and verify its complete based meridian image."""
    image = reduce_word(image)
    start, end = 0, len(image)
    while end-start > 1 and image[start] == -image[end-1]:
        start += 1
        end -= 1
    if end-start != 1 or not 1 <= image[start] <= points:
        raise ValueError('The image is not a positive based puncture meridian')
    puncture = image[start]
    cuts = _ray_cuts(image[:start])
    candidates = []
    for trim_start in (False, True):
        for trim_end in (False, True):
            proposed = cuts[:]
            if trim_start:
                if not proposed or proposed[0] != 0: continue
                proposed = proposed[1:]
            if trim_end:
                if not proposed or proposed[-1] not in (puncture-1,puncture): continue
                proposed = proposed[:-1]
            for direction in ('down','up'):
                try: arc = Arc(0,puncture,tuple(proposed),direction=direction)
                except ValueError: continue
                path = based_arc_ray_word(arc,points=points)
                if reduce_word(path+(puncture,)+inverse_word(path)) == image:
                    candidates.append(arc)
    if not candidates:
        raise ValueError('No exact based arc fits the shared 768-cut drawing limit')
    return min(candidates,key=lambda arc:(len(arc.cuts),arc.initial_up))


def based_cut_system_drawing(images):
    """Render six exact based arcs together, or report an honest route limit."""
    return _cached_drawing(tuple(tuple(image) for image in images))


@lru_cache(maxsize=24)
def _cached_drawing(images):
    if len(images) != 6:
        raise ValueError('The six-point cut system needs six meridian images')
    arcs = tuple(based_arc_from_meridian(image) for image in images)
    if sum(len(arc.cuts)+2 for arc in arcs) > MAX_ROUTE_NODES:
        raise ValueError('Combined cut-system routes exceed 1024 nodes; the exact words remain available')
    visits = max(Counter(cut for arc in arcs for cut in arc.cuts).values(),default=0)
    scale = max(1.,((visits+1)*4+10)/50)
    surface = PlanarSurface.row('PPPPPP',spacing=50*scale,height=220*scale,margin=55*scale)
    diagram = PlanarDiagram(surface,tuple(ColoredCurve(f'x{i+1}',arc,RAINBOW[i])
                                          for i,arc in enumerate(arcs)))
    return render_svg(diagram,style=Style(curve_width=1.5,marked_point_radius=3.5))
