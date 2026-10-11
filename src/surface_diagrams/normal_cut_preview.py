"""SVG preview of a certified normal-strand cut system.

The certificate supplies all local pairings and exact labeled itineraries.
This module only places those strands in convex cells. It neither changes
their combinatorics nor establishes minimality of the input Arcs.
"""

from collections import defaultdict
from html import escape
from math import hypot

from .normal_cut_engine import CertifiedCutSystem
from .normal_gluing import TerminalVisit
from .normal_strands import NormalTriangleError, StrandVisit
from .visuals import RAINBOW


def _number(value):
    return format(value, '.6f').rstrip('0').rstrip('.') or '0'


def _between(first, second, fraction):
    return (first[0] + (second[0] - first[0]) * fraction,
            first[1] + (second[1] - first[1]) * fraction)


class _FanLayout:
    """One coordinate per physical crossing, shared by incident triangles."""

    def __init__(self, certificate):
        self.certificate = certificate
        points = certificate.points
        busiest_cut = max(map(len, certificate.cut_orders.values()), default=0)
        busiest_ray = max(map(len, certificate.ray_orders.values()), default=0)
        # The seven horizontal gaps and both outer caps need the same clear
        # spacing. The ray height is independent of horizontal cut density.
        self.pitch = 4.0
        self.spacing = max(50.0, (busiest_cut + 1) * self.pitch + 24.0)
        self.apex_height = max(110.0, (busiest_ray + 1) * self.pitch + 24.0)
        self.width = (points + 1) * self.spacing
        self.height = 2 * self.apex_height
        self.xs = tuple((index - (points + 1) / 2) * self.spacing
                        for index in range(points + 2))
        self.vertices = {'north': (0.0, self.apex_height),
                         'south': (0.0, -self.apex_height),
                         'b0': (self.xs[0], 0.0),
                         f'b{points + 1}': (self.xs[-1], 0.0)}
        self.vertices.update({f'p{point}': (self.xs[point], 0.0)
                              for point in range(1, points + 1)})
        self.crossings = {}
        self._place_crossings()

    def _cell_vertices(self, triangle):
        return tuple(self.vertices[name] for name in triangle.vertices)

    def _place_crossings(self):
        for gap, visits in self.certificate.cut_orders.items():
            for index, crossing in enumerate(visits):
                visit = StrandVisit(crossing.owner, crossing)
                if visit in self.crossings:
                    raise NormalTriangleError('a crossing ID occurs on multiple edges')
                fraction = (index + 1) / (len(visits) + 1)
                self.crossings[visit] = _between(
                    self.vertices['b0' if gap == 0 else f'p{gap}'],
                    self.vertices[f'b{self.certificate.points + 1}'
                                  if gap == self.certificate.points else f'p{gap + 1}'],
                    fraction)
        for (side, point), visits in self.certificate.ray_orders.items():
            for index, crossing in enumerate(visits):
                visit = StrandVisit(crossing.owner, crossing)
                if visit in self.crossings:
                    raise NormalTriangleError('a crossing ID occurs on multiple edges')
                fraction = (index + 1) / (len(visits) + 1)
                self.crossings[visit] = _between(
                    self.vertices[f'p{point}'], self.vertices['north' if side == 'upper' else 'south'],
                    fraction)

        self._validate_crossings()

    def _validate_crossings(self):
        # Check the oriented 14-triangle assembler against the canonical
        # physical coordinates. Terminal slots occupy the vertex itself; they
        # do not consume a ray/cut crossing position.
        for triangle in self.certificate.triangles:
            vertices = self._cell_vertices(triangle)
            if any(self._area(vertices[index], vertices[(index + 1) % len(vertices)],
                              vertices[(index + 2) % len(vertices)]) <= 0
                   for index in range(len(vertices))):
                raise NormalTriangleError('normal cell is degenerate or reversed')
            for side_index, side in enumerate(triangle.sides):
                source = vertices[side_index]
                target = vertices[(side_index + 1) % len(vertices)]
                physical = tuple(visit for visit in side.visits
                                 if not isinstance(visit, TerminalVisit))
                for index, visit in enumerate(physical):
                    expected = _between(source, target, (index + 1) / (len(physical) + 1))
                    if visit not in self.crossings or hypot(
                            *(a - b for a, b in zip(self.crossings[visit], expected))) > 1e-7:
                        raise NormalTriangleError('shared crossing coordinate disagrees with side order')
                for terminal in (visit for visit in side.visits
                                 if isinstance(visit, TerminalVisit)):
                    if terminal.vertex not in triangle.vertices:
                        raise NormalTriangleError('terminal is outside its triangle')

    @staticmethod
    def _area(first, second, third):
        return ((second[0] - first[0]) * (third[1] - first[1]) -
                (second[1] - first[1]) * (third[0] - first[0]))

    def coordinate(self, visit):
        return (self.vertices[visit.vertex] if isinstance(visit, TerminalVisit)
                else self.crossings[visit])

    def chord(self, connection):
        """Return line or shallow quadratic, keeping vertex chords interior."""
        first = self.coordinate(connection.first)
        second = self.coordinate(connection.second)
        if first == second:
            raise NormalTriangleError('a local strand has coincident ends')
        triangle = next(triangle for triangle in self.certificate.triangles
                        if triangle.triangle_id == connection.triangle_id)
        vertices = self._cell_vertices(triangle)
        centroid = (sum(point[0] for point in vertices) / len(vertices),
                    sum(point[1] for point in vertices) / len(vertices))
        midpoint = _between(first, second, .5)
        dx, dy = second[0] - first[0], second[1] - first[1]
        length = hypot(dx, dy)
        # A terminal-to-incident-side strand or an edge-parallel chain arc
        # would otherwise lie on a cell edge. A shallow inward bend
        # separates it from that edge while retaining its boundary order.
        if (isinstance(connection.first, TerminalVisit)
                or isinstance(connection.second, TerminalVisit)):
            on_edge = any(
                abs(self._area(vertices[index], vertices[(index + 1) % len(vertices)], first)) < 1e-7
                and abs(self._area(vertices[index], vertices[(index + 1) % len(vertices)], second)) < 1e-7
                for index in range(len(vertices)))
            if on_edge:
                nx, ny = -dy / length, dx / length
                if (centroid[0] - midpoint[0]) * nx + (centroid[1] - midpoint[1]) * ny < 0:
                    nx, ny = -nx, -ny
                bow = min(1.2, .1 * length, .4 * self.pitch)
                return ('Q', midpoint[0] + bow * nx, midpoint[1] + bow * ny,
                        *second)
        return ('L', *second)


class _StripLayout(_FanLayout):
    """Open each apex into an empty top/bottom edge of a rectangular cell.

    The three occupied sides keep their counterclockwise order: upper cells
    run down the left ray, across the cut, then up the right ray; lower cells
    run up the right ray, back across the cut, then down the left ray. Adjacent
    cells use the same vertical ray and crossing coordinates.
    """

    def __init__(self, certificate):
        super().__init__(certificate)
        del self.vertices['north']
        del self.vertices['south']

    def _cell_vertices(self, triangle):
        side, gap = triangle.triangle_id
        left, right = self.xs[gap], self.xs[gap + 1]
        height = self.apex_height
        if side == 'upper':
            return ((left, height), (left, 0.0),
                    (right, 0.0), (right, height))
        return ((right, -height), (right, 0.0),
                (left, 0.0), (left, -height))

    def _place_crossings(self):
        for gap, visits in self.certificate.cut_orders.items():
            for index, crossing in enumerate(visits):
                visit = StrandVisit(crossing.owner, crossing)
                if visit in self.crossings:
                    raise NormalTriangleError('a crossing ID occurs on multiple edges')
                self.crossings[visit] = (
                    self.xs[gap] + (index + 1) * self.spacing / (len(visits) + 1),
                    0.0)
        for (side, point), visits in self.certificate.ray_orders.items():
            sign = 1 if side == 'upper' else -1
            for index, crossing in enumerate(visits):
                visit = StrandVisit(crossing.owner, crossing)
                if visit in self.crossings:
                    raise NormalTriangleError('a crossing ID occurs on multiple edges')
                self.crossings[visit] = (
                    self.xs[point],
                    sign * (index + 1) * self.apex_height / (len(visits) + 1))

        self._validate_crossings()


def render_normal_cut_preview(certificate, *, projection='strip', mirror_vertical=False):
    """Render six colored normal Arcs after their exact-event certificate.

    The SVG is a preview of the certified combinatorial placement. Its local
    chords are drawn in convex cells; no minimal-position assertion is
    made for the supplied Arc itineraries. A vertical mirror changes only
    display coordinates, leaving the certified itineraries untouched.
    """
    if not isinstance(certificate, CertifiedCutSystem):
        raise TypeError('expected a CertifiedCutSystem')
    if projection not in ('strip', 'fan'):
        raise ValueError('projection must be strip or fan')
    if type(mirror_vertical) is not bool:
        raise TypeError('mirror_vertical must be a boolean')
    layout = _StripLayout(certificate) if projection == 'strip' else _FanLayout(certificate)
    connections = defaultdict(list)
    for connection in certificate.connections:
        connections[connection.owner].append(connection)
    if set(connections) != set(certificate.owners):
        raise NormalTriangleError('connections differ from certified owners')

    padding = 13.0
    width, height = layout.width + 2 * padding, layout.height + 2 * padding

    def screen(point):
        return (_number(width / 2 + point[0]),
                _number(height / 2 + (point[1] if mirror_vertical else -point[1])))

    if projection == 'strip':
        corner_radius = max(18.0, min(layout.spacing / 4,
                                      layout.apex_height * .12))
        boundary = (f'<rect class="outer-boundary" x="{_number(padding)}" '
                    f'y="{_number(padding)}" width="{_number(layout.width)}" '
                    f'height="{_number(layout.height)}" '
                    f'rx="{_number(corner_radius)}" fill="none" '
                    'stroke="#000000" stroke-width="1.5" '
                    'vector-effect="non-scaling-stroke"/>')
    else:
        boundary = (f'<ellipse class="outer-boundary" cx="{_number(width / 2)}" '
                    f'cy="{_number(height / 2)}" rx="{_number(layout.width / 2)}" '
                    f'ry="{_number(layout.height / 2)}" fill="none" '
                    'stroke="#000000" stroke-width="1.5"/>')
    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_number(width)} {_number(height)}" '
             f'width="{_number(width)}" height="{_number(height)}" role="img">',
             '<title>Normal-strand cut-system preview</title>',
             '<desc>Joint local strands follow certified exact Arc itineraries; '
             'minimal position is not independently established.</desc>',
             '<rect width="100%" height="100%" fill="white"/>',
             boundary]
    for path in certificate.paths:
        owner = path.owner
        segments = connections[owner]
        if not segments or segments[0].first != path.start or segments[-1].second != path.end:
            raise NormalTriangleError('rendered connection endpoints differ from certificate')
        commands = [('M', *layout.coordinate(path.start))]
        for first, second in zip(segments, segments[1:]):
            if first.second != second.first:
                raise NormalTriangleError('rendered local connections do not join')
        commands.extend(layout.chord(connection) for connection in segments)
        data = []
        for op, *values in commands:
            if op == 'Q':
                control = screen(values[:2])
                target = screen(values[2:])
                data.append(f'Q {control[0]} {control[1]} {target[0]} {target[1]}')
            else:
                target = screen(values)
                data.append(f'{op} {target[0]} {target[1]}')
        lines.append(f'<path class="arc" data-owner="{owner}" '
                     f'd="{escape(" ".join(data), quote=True)}" fill="none" '
                     f'stroke="{RAINBOW[(owner - 1) % len(RAINBOW)]}" '
                     'stroke-width="1.5" vector-effect="non-scaling-stroke" '
                     'stroke-linecap="round" '
                     'stroke-linejoin="round"/>')
    for point in range(1, certificate.points + 1):
        cx, cy = screen(layout.vertices[f'p{point}'])
        lines.append(f'<circle class="marked-point" cx="{cx}" cy="{cy}" '
                     'r="3.5" fill="#006fff" stroke="#006fff" '
                     'stroke-width="2" vector-effect="non-scaling-stroke"/>')
        lines.append(f'<text class="marked-point-label" x="{cx}" '
                     f'y="{_number(float(cy) + 15)}" text-anchor="middle" '
                     'font-family="sans-serif" font-size="10" '
                     f'fill="#183457">{point}</text>')
    lines.append('</svg>')
    return '\n'.join(lines) + '\n'
