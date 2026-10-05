"""Support pictures and an aligned braid for a marked-disk playground.

The pictures are recovered from exact support classes and checked by the
shared Arc/Loop router.  The braid is drawn directly from each exact factor
word; neither picture is substituted for a mapping-class equality check.
"""

from collections import Counter
from functools import lru_cache
from html import escape
import re

from .braid_actions import arc_ray_word, free_homotopy_key, inverse_word, loop_ray_word
from .curves import Arc, Loop, MAX_CUT_VISITS
from .mapping_classes import supported_class
from .model import PlanarSurface, Style
from .svg import render_svg
from .twist_supports import _ray_cuts, support_drawing
from .visuals import RAINBOW, _braid_paths


def _check_strands(strands):
    if type(strands) is not int or strands < 2:
        raise ValueError('strands must be an integer at least two')


def _loop_from_class(word, strands):
    word = free_homotopy_key(word)
    if not word:
        raise ValueError('Empty boundary class has no essential loop')
    curve = Loop(tuple(_ray_cuts(word)), start_up=True)
    if free_homotopy_key(loop_ray_word(strands, curve)) != word:
        raise ValueError('Exact loop itinerary failed its boundary-word check')
    return curve


def _arc_from_class(word, start, end, strands):
    """Recover one unframed point arc from its two-point boundary class."""
    word = free_homotopy_key(word)
    if len(word) < 2 or len(word) % 2:
        raise ValueError('Boundary class cannot represent a two-point arc')
    if len(word) > 2 + 2 * (MAX_CUT_VISITS // 2 + 1) * strands:
        raise ValueError(f'Exact arc topology exceeds the shared {MAX_CUT_VISITS}-cut drawing limit')
    size = (len(word) - 2) // 2
    for oriented in (word, inverse_word(word)):
        for index, letter in enumerate(oriented):
            if letter != start:
                continue
            rotated = oriented[index:] + oriented[:index]
            transport = rotated[1:size + 1]
            if rotated[size + 1] != end or rotated[size + 2:] != inverse_word(transport):
                continue
            cuts = _ray_cuts(transport)
            up = False
            while cuts and cuts[0] in (start - 1, start):
                cuts.pop(0)
                up = not up
            while cuts and cuts[-1] in (end - 1, end):
                cuts.pop()
            curve = Arc(start, end, tuple(cuts), direction='up' if up else 'down')
            path = arc_ray_word(strands, curve)
            boundary = (start,) + path + (end,) + inverse_word(path)
            if free_homotopy_key(boundary) == word:
                return curve
    raise ValueError('Exact boundary class has no recovered endpoint path')


@lru_cache(maxsize=128)
def support_curve(twist, strands):
    """Recover an exact-class Arc/Loop proposal; the renderer checks routing."""
    _check_strands(strands)
    if any(type(letter) is not int or not 1 <= abs(letter) < strands
           for letter in twist.conjugator):
        raise ValueError('Support conjugator exceeds the marked disk')
    word = supported_class(twist, strands=strands)
    if not twist.half:
        return _loop_from_class(word, strands)
    start, end = twist.first, twist.first + 1
    # A(uv)=A(u) composed with A(v): the last permutation acts first.
    for crossing in reversed(twist.conjugator):
        index = abs(crossing)
        start = index + 1 if start == index else index if start == index + 1 else start
        end = index + 1 if end == index else index if end == index + 1 else end
    return _arc_from_class(word, start, end, strands)


@lru_cache(maxsize=128)
def support_svg(factor, strands):
    """Render a verified single-factor support, or raise ValueError.

    Six-point factors retain the existing lab renderer and its cache. A failed
    recovery or routing is an unavailable picture, never an inferred curve.
    """
    _check_strands(strands)
    twist = factor.mapping_class
    if strands == 6:
        return support_drawing(twist)
    curve = support_curve(twist, strands)
    visits = max(Counter(curve.cuts).values(), default=0)
    scale = max(1., ((visits + 1) * 4 + 10) / 50)
    surface = PlanarSurface.row('P' * strands, spacing=50 * scale,
                                height=220 * scale, margin=55 * scale).with_curves(curve)
    return render_svg(surface, style=Style(curve_color='#a21caf', curve_width=1.5,
                                           marked_point_radius=3.5))


def row_height(factor):
    return max(210, len(factor.word) * 12 + 36)


def braid_svg(factors, strands):
    """Draw exact words as one continuous braid, with factor row boundaries."""
    _check_strands(strands)
    factors = tuple(factors)
    if not factors:
        raise ValueError('A braid view needs at least one factor')
    levels = [0.]
    letters = []
    boundaries = []
    offset = 0
    for factor in factors:
        height = row_height(factor)
        letters.append(None)
        levels.append(-offset - 18)
        for index, letter in enumerate(factor.word):
            if type(letter) is not int or not 1 <= abs(letter) < strands:
                raise ValueError('Factor braid word exceeds the marked disk')
            letters.append(letter)
            levels.append(-offset - 18 - (index + 1) * 12)
        offset += height
        letters.append(None)
        levels.append(-offset)
        boundaries.append(offset)
    spacing = 28
    width = max(240, (strands - 1) * spacing + 40)
    center = width / 2
    paths, _ = _braid_paths(strands, letters, levels, spacing, RAINBOW,
                            Style(curve_width=1.3), 'smooth')
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{offset}" '
           f'viewBox="0 0 {width} {offset}" role="img" '
           f'aria-label="Continuous {strands}-strand braid">']
    top = 0
    for index, factor in enumerate(factors):
        height = row_height(factor)
        svg.append(f'<rect class="braid-row" data-index="{index}" x="0" y="{top}" '
                   f'width="{width}" height="{height}" fill="none">'
                   f'<title>{escape(factor.id)} braid interval</title></rect>')
        top += height
    for path in paths:
        commands = []
        for op, *values in path.commands:
            coords = [center + value if index % 2 == 0 else -value
                      for index, value in enumerate(values)]
            commands.append(op + ' ' + ' '.join(f'{value:.3f}' for value in coords))
        svg.append(f'<path d="{" ".join(commands)}" stroke="{path.stroke}" '
                   'stroke-width="1.3" fill="none"/>')
    for y in boundaries[:-1]:
        svg.append(f'<path d="M 12 {y} H {width - 12}" stroke="#2563eb" '
                   'stroke-width="1.3" stroke-dasharray="3 5"/>')
    svg.append('</svg>')
    return ''.join(svg)


def factorization_svg(factors, strands):
    """Portable paired export with explicit unavailable-support messages."""
    _check_strands(strands)
    factors = tuple(factors)
    if not factors:
        raise ValueError('A paired view needs at least one factor')
    height = sum(row_height(factor) for factor in factors)
    braid = braid_svg(factors, strands)
    braid_width = max(240, (strands - 1) * 28 + 40)
    body = []
    y = 0
    for factor in factors:
        label = f'{factor.id} · {factor.label}'
        body.append(f'<g transform="translate(0 {y})"><title>{escape(label)}</title>'
                    f'<text x="12" y="20" font-family="sans-serif" font-size="12">'
                    f'{escape(label[:52])}</text>')
        try:
            support = support_svg(factor, strands)
            support = re.sub(r'width="[^"]*"', 'width="340"', support, count=1)
            support = re.sub(r'height="[^"]*"', 'height="166"', support, count=1)
            body.append('<text x="12" y="34" font-family="sans-serif" font-size="10" '
                        'fill="#476b58">Exact support class recovered</text>')
            body.append(f'<g transform="translate(0 38)">{support}</g>')
        except ValueError as error:
            body.append(f'<desc>{escape(str(error))}</desc>'
                        '<text x="12" y="80" fill="#a14b20" font-family="sans-serif" '
                        'font-size="12">Support picture unavailable.</text>'
                        '<text x="12" y="100" font-family="sans-serif" font-size="12">'
                        'Exact braid remains in the right column.</text>')
        body.append('</g>')
        y += row_height(factor)
    body.append(f'<g transform="translate(360 0)">{braid}</g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{360 + braid_width + 20}" '
            f'height="{height + 28}" viewBox="0 0 {360 + braid_width + 20} {height + 28}">'
            '<title>Boundary factorization paired export</title>'
            '<rect width="100%" height="100%" fill="white"/>'
            '<text x="12" y="18" font-family="sans-serif" font-size="12" fill="#526880">'
            'Arc/Loop support pictures · exact braid words</text>'
            '<g transform="translate(0 28)">' + ''.join(body) + '</g></svg>')
