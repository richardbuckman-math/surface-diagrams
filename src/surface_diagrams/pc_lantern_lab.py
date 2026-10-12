"""The puncture-capped lantern lab and its exact three-arc cut-system views.

The braid action and factor edits come from the boundary-twist playground.
Only the displayed arc paths are reflected vertically; the positive braid
generators, twist powers, and exact Arc itineraries retain their usual values.
"""

from dataclasses import dataclass, replace
from typing import Optional
from functools import lru_cache
from html import escape

from .based_cut_system import based_arc_from_meridian
from .boundary_playground import BoundaryProject, new_project
from .boundary_playground_app import BoundaryLab
from .boundary_playground_geometry import (_arc_from_class, factorization_svg,
                                           support_curve)
from .braid_actions import artin_action, reduce_word
from .chain_presentation import ChainDiagram, shape_chain_arc
from .curves import Arc
from .model import PlanarSurface, Style
from .svg import render_svg
from .visuals import ColoredCurve


SURFACE = PlanarSurface.row('PPP', spacing=82, height=180, margin=80)
STYLE = Style(background='#ffffff', curve_width=2.4,
              marked_point_radius=5, curve_height=0.84)
ARC_COLORS = ('#c02648', '#0e7490', '#7c3aed')


_shape_pc_arc = shape_chain_arc


@dataclass(frozen=True)
class _PCCutDiagram(ChainDiagram):
    """The three-edge disk chain has its boundary endpoint in the first arc."""

    rim_index: Optional[int] = 0


def _pc_support_svg(factor, *, mirror_vertical):
    """Use a flat disk for PC support pictures, with the shared exact curve."""
    curve = support_curve(factor.mapping_class, 3)
    surface = PlanarSurface.row('PPP', spacing=50, height=130,
                                margin=55).with_curves(curve)
    return render_svg(surface, style=Style(curve_color='#a21caf',
                                           curve_width=1.5,
                                           marked_point_radius=3.5),
                      mirror_curve_paths_vertical=mirror_vertical)


def pc_project():
    """The checked marked-disk equality T123 = T12 T13 T23."""
    split = new_project(3).split(0, 'lantern')
    factors = tuple(replace(factor, id=name) for factor, name in zip(
        split.factors, ('T12', 'T13', 'T23')))
    return BoundaryProject(3, 1, factors)


def _puncture(image):
    """Recover the positive puncture label of a transported meridian."""
    image = reduce_word(image)
    start, end = 0, len(image)
    while end - start > 1 and image[start] == -image[end - 1]:
        start += 1
        end -= 1
    if end - start != 1 or not 1 <= image[start] <= 3:
        raise ValueError('Expected a positive three-point puncture meridian')
    return image[start]


@lru_cache(maxsize=128)
def chain_arcs(word):
    """Exact boundary→1→2→3 chain image, one arc record per edge."""
    images = artin_action(3, word)
    endpoints = tuple(_puncture(image) for image in images)
    if set(endpoints) != {1, 2, 3}:
        raise ValueError('The action does not permute all three punctures')
    arcs = [based_arc_from_meridian(images[0], points=3)]
    for index in (0, 1):
        boundary = reduce_word(images[index] + images[index + 1])
        arcs.append(_arc_from_class(boundary, endpoints[index],
                                    endpoints[index + 1], 3))
    return tuple(Arc(arc.start, arc.end) if not arc.cuts and
                 abs(arc.start - arc.end) == 1 else arc for arc in arcs)


@lru_cache(maxsize=128)
def cut_system_svg(word, mirrored=True):
    """Draw the exact chain with either visual orientation, never changing its word."""
    arcs = chain_arcs(word)
    labels = ('boundary→1', '1→2', '2→3')
    colored = tuple(ColoredCurve(f'e{index + 1}: {label}', arc,
                                 ARC_COLORS[index])
                    for index, (label, arc) in enumerate(zip(labels, arcs)))
    # Arc names are already present in the column controls. Omitting the SVG
    # legend gives the curves more of each factor row's fixed vertical space.
    diagram = _PCCutDiagram(SURFACE, colored, show_legend=False)
    svg = render_svg(diagram, style=STYLE, title='PC lantern cut system',
                     mirror_curve_paths_vertical=mirrored)
    drawing = diagram.drawing(STYLE)
    points = [item for item in drawing.ellipses if item.role == 'marked-point']
    if len(points) != 3:
        raise ValueError('Expected three marked points')
    if svg.count('class="arc"') != 3 or (mirrored and svg.count('scale(1 -1)') != 3):
        raise ValueError('Could not identify all three arc paths')
    point_labels = []
    for index, point in enumerate(points, 1):
        x = drawing.width / 2 + point.x
        y = drawing.height / 2 - point.y
        point_labels.append(f'<rect x="{x - 9:.3f}" y="{y + 5:.3f}" width="18" '
                            'height="18" rx="3" fill="#ffffff" opacity="0.92"/>')
        point_labels.append(f'<text x="{x:.3f}" y="{y + 19:.3f}" '
                            'font-family="system-ui,sans-serif" font-size="13" '
                            'text-anchor="middle" fill="#111827">'
                            f'{escape(str(index))}</text>')
    return svg.replace('</svg>', '\n'.join(point_labels) + '\n</svg>')


def cut_steps(factors):
    """Every prefix, plus the direct twist target for side-by-side checking."""
    prefix = ()
    rows = []
    for index in range(len(factors) + 1):
        label = ('Start: boundary→1→2→3' if index == 0 else
                 f'After {factors[index-1].id}')
        try:
            svg, svg_unmirrored, warning = (cut_system_svg(prefix),
                                             cut_system_svg(prefix, False), '')
        except ValueError as error:
            svg, svg_unmirrored, warning = '', '', str(error)
        try:
            arcs = tuple(dict(start=arc.start, end=arc.end,
                              cuts=arc.cuts, initial_up=arc.initial_up)
                         for arc in chain_arcs(prefix))
        except ValueError as error:
            arcs = ()
            warning = warning or str(error)
        rows.append(dict(index=index, label=label, word=prefix, svg=svg,
                         svg_unmirrored=svg_unmirrored, warning=warning,
                         arcs=arcs))
        if index < len(factors):
            prefix += factors[index].word
    target = new_project(3).word
    rows.append(dict(index='target', label='Direct T123 target', word=target,
                     svg=cut_system_svg(target),
                     svg_unmirrored=cut_system_svg(target, False), warning='',
                     arcs=tuple(dict(start=arc.start, end=arc.end,
                                     cuts=arc.cuts, initial_up=arc.initial_up)
                                for arc in chain_arcs(target))))
    return rows


class PCLanternLab(BoundaryLab):
    """A fixed three-point target initialized to its three lantern factors."""

    def __init__(self):
        super().__init__()
        self.history = [pc_project()]
        self.operations = ['PC lantern: T12 · T13 · T23']
        self.message = 'Three pairwise twists equal the direct three-point boundary twist.'

    def state(self):
        state = super().state()
        for factor, row in zip(self.project.factors, state['factors']):
            try:
                row['svg_mirrored'] = _pc_support_svg(factor, mirror_vertical=True)
                row['svg_unmirrored'] = _pc_support_svg(factor, mirror_vertical=False)
                row['svg'] = row['svg_mirrored']
            except ValueError as error:
                row['svg_mirrored'] = row['svg_unmirrored'] = ''
                row['svg'] = ''
                row['warning'] = str(error)
        state['cut_steps'] = cut_steps(self.project.factors)
        state['pc_lantern'] = True
        return state

    def restore(self, document):
        if (not isinstance(document, dict) or
                not isinstance(document.get('history'), list) or
                any(not isinstance(row, dict) or
                    (row.get('points'), row.get('power')) != (3, 1)
                    for row in document['history'])):
            raise ValueError('This workspace is not a PC lantern exploration')
        super().restore(document)

    def export_svg(self, *, mirror_vertical=True, compact=False):
        return factorization_svg(self.project.factors, 3,
                                 mirror_vertical=mirror_vertical, compact=compact)

    def mutate(self, payload):
        operation = payload.get('op') if isinstance(payload, dict) else None
        if operation == 'example':
            if payload.get('revision') != self.revision:
                raise ValueError('State changed; reload before editing')
            self._append(pc_project(), 'Restore PC lantern: T12 · T13 · T23')
            self.message = 'Restored the three checked lantern factors.'
            self.revision += 1
            return
        if operation == 'new' and (payload.get('points'), payload.get('power')) != (3, 1):
            raise ValueError('The PC lantern lab has a fixed three-point target')
        if operation == 'import':
            document = payload.get('document', {})
            if not isinstance(document, dict) or (document.get('points'), document.get('power')) != (3, 1):
                raise ValueError('Import a three-point, power-one boundary twist')
        super().mutate(payload)
