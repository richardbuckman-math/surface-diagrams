"""The boundary-to-first-point, then adjacent-point chain for a disk braid.

The braid action supplies the six based meridian images. The image of the
first meridian determines the initial boundary-to-point arc. For each pair of
consecutive meridians, the image of their product is the boundary of a small
neighborhood of the corresponding point-to-point arc. Recovering that arc
from the two-point boundary class avoids repeating the long boundary spokes.
"""
from collections import Counter
from functools import lru_cache

from .based_cut_system import based_arc_from_meridian
from .braid_actions import reduce_word
from .curves import Arc, MAX_ROUTE_NODES
from .model import PlanarSurface, Style
from .svg import render_svg
from .twist_supports import arc_from_class
from .visuals import ColoredCurve, PlanarDiagram, RAINBOW


def _puncture(image):
    word = reduce_word(image)
    start, end = 0, len(word)
    while end - start > 1 and word[start] == -word[end - 1]:
        start += 1
        end -= 1
    if end - start != 1 or not 1 <= word[start] <= 6:
        raise ValueError('The chain needs six positive puncture meridian images')
    return word[start]


def chain_words(images):
    """Exact based neighborhood-boundary words for six ordered chain edges."""
    images = tuple(tuple(image) for image in images)
    if len(images) != 6:
        raise ValueError('The six-point chain needs six meridian images')
    punctures = tuple(_puncture(image) for image in images)
    if set(punctures) != set(range(1, 7)):
        raise ValueError('Meridian images must reach each puncture exactly once')
    words = (reduce_word(images[0]),) + tuple(
        reduce_word(images[i] + images[i + 1]) for i in range(5))
    endpoints = ((0, punctures[0]),) + tuple(
        (punctures[i], punctures[i + 1]) for i in range(5))
    return words, endpoints


def chain_arcs(images):
    """Recover the six chain arcs; joint routing is checked only when drawn."""
    words, endpoints = chain_words(images)
    return tuple(_recover_edge(words, endpoints, i) for i in range(6))


def _recover_edge(words, endpoints, index):
    arc = (based_arc_from_meridian(words[0]) if index == 0 else
           arc_from_class(words[index], *endpoints[index]))
    # A zero-cut edge between consecutive objects has a straight representative.
    # Keep the standard reference chain on the symmetry line, including its
    # boundary-to-first-point edge, instead of inventing a small semicircle.
    if not arc.cuts and abs(arc.start - arc.end) == 1:
        return Arc(arc.start, arc.end)
    return arc


def chain_arc(images, index):
    """Recover one edge without requiring the other five to fit their limits."""
    if type(index) is not int or not 0 <= index < 6:
        raise ValueError('Choose one of the six chain arcs')
    words, endpoints = chain_words(images)
    return _recover_edge(words, endpoints, index)


def chain_arc_drawing(images, *, index=0):
    """Draw one exact chain edge, without claiming a joint embedded picture."""
    if type(index) is not int or not 0 <= index < 6:
        raise ValueError('Choose one of the six chain arcs')
    return _cached_arc_drawing(tuple(tuple(image) for image in images), index)


def chain_cut_system_drawing(images):
    """Draw all six chain edges together, or report the finite route limit."""
    return _cached_drawing(tuple(tuple(image) for image in images))


def _surface(arcs):
    visits = max(Counter(cut for arc in arcs for cut in arc.cuts).values(), default=0)
    scale = max(1., ((visits + 1) * 4 + 10) / 50)
    return PlanarSurface.row('PPPPPP', spacing=50 * scale,
                             height=220 * scale, margin=55 * scale)


@lru_cache(maxsize=48)
def _cached_arc_drawing(images, index):
    arc = chain_arc(images, index)
    diagram = PlanarDiagram(_surface((arc,)),
                            (ColoredCurve(f'chain {index + 1}', arc, RAINBOW[index]),))
    return render_svg(diagram, style=Style(curve_width=1.5, marked_point_radius=3.5))


@lru_cache(maxsize=24)
def _cached_drawing(images):
    arcs = chain_arcs(images)
    if sum(len(arc.cuts) + 2 for arc in arcs) > MAX_ROUTE_NODES:
        raise ValueError(f'Combined chain routes exceed {MAX_ROUTE_NODES} nodes; '
                         'the exact words remain available')
    diagram = PlanarDiagram(_surface(arcs), tuple(
        ColoredCurve(f'chain {i + 1}', arc, RAINBOW[i])
        for i, arc in enumerate(arcs)))
    return render_svg(diagram, style=Style(curve_width=1.5, marked_point_radius=3.5))
