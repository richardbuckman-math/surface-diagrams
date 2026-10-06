"""Certify an explicitly ordered collection of local normal triangle strands.

The caller supplies crossing order on every triangle side.  This module checks
that adjacent triangles use the same physical crossings, joins their local
strands, and reports complete labeled endpoint-to-endpoint paths.  It does not
choose crossing orders or establish minimal position for an arc itinerary.
"""

from dataclasses import dataclass
from typing import Hashable

from .normal_strands import (
    LabeledCutVisit, LabeledRayVisit, NormalTriangleError, StrandVisit,
    arc_side_ray_visits, pair_triangle_sides,
)


@dataclass(frozen=True)
class TerminalVisit(StrandVisit):
    """A formal side slot that actually ends at a puncture or disk boundary.

    ``crossing`` is a stable local identifier, never a physical edge crossing.
    ``vertex`` names the triangle vertex at which the arc ends.  A terminal
    must be the first or last slot of a side incident to that vertex.
    """

    terminal_id: Hashable
    vertex: Hashable
    kind: str = 'puncture'


@dataclass(frozen=True)
class TriangleSide:
    """An oriented triangle side and its visits in boundary traversal order."""

    edge_id: Hashable
    visits: tuple[StrandVisit, ...] = ()


@dataclass(frozen=True)
class NormalTriangle:
    """Sides 0, 1, 2 run vertex 0→1, 1→2, and 2→0."""

    triangle_id: Hashable
    vertices: tuple[Hashable, Hashable, Hashable]
    sides: tuple[TriangleSide, TriangleSide, TriangleSide]


@dataclass(frozen=True)
class ExpectedArc:
    owner: int
    start: TerminalVisit
    end: TerminalVisit


@dataclass(frozen=True)
class GluedArc:
    """Physical crossing IDs in order from the declared start to end."""

    owner: int
    start: TerminalVisit
    end: TerminalVisit
    crossings: tuple[StrandVisit, ...]


def inner_arc_triangles(arcs, ray_orders, cut_orders, *, owners):
    """Build the two normal triangles in each inner gap from supplied orders.

    ``arcs`` use one-based chain owners. The order maps come from a common
    accepted placement, such as ``joint_arc_ray_orders`` and
    ``joint_arc_cut_orders``. Omitted arcs must be straight adjacent chain
    edges. This model deliberately excludes outer regions: it rejects any
    crossing on the first/last ray or outer cut, and endpoints in outer gaps.
    The returned expected arcs can be passed to ``glue_triangles`` with the
    triangles; neither operation derives the supplied crossing orders.
    """
    return _arc_triangles(arcs, ray_orders, cut_orders, owners=owners,
                          include_outer=False)


def arc_triangles(arcs, ray_orders, cut_orders, *, owners):
    """Build upper/lower triangles in every gap, including the outer caps.

    The outer caps have boundary edges meeting the left/right rim tips. A
    boundary endpoint occupies one terminal slot on its incident cap's
    boundary edge. Orders on all rays and cuts must still be supplied from a
    common placement; this does not derive them or prove minimal position.
    """
    return _arc_triangles(arcs, ray_orders, cut_orders, owners=owners,
                          include_outer=True)


def _arc_triangles(arcs, ray_orders, cut_orders, *, owners, include_outer):
    from .curves import Arc

    arcs = tuple(arcs)
    owners = tuple(owners)
    points = len(cut_orders) - 1
    if (points < 2 or not arcs or any(not isinstance(arc, Arc) for arc in arcs)
            or not owners or len(set(owners)) != len(owners)
            or any(type(owner) is not int or not 1 <= owner <= len(arcs)
                   for owner in owners)):
        raise NormalTriangleError('expected arcs and distinct one-based owners')
    if set(cut_orders) != set(range(points + 1)) or set(ray_orders) != {
            (side, point) for side in ('upper', 'lower')
            for point in range(1, points + 1)}:
        raise NormalTriangleError('inner region needs every ray and cut order')

    expected_rays = tuple(LabeledRayVisit(owner, visit)
                          for owner, arc in enumerate(arcs, 1)
                          for side in ('upper', 'lower')
                          for visit in arc_side_ray_visits(arc, side, points))
    actual_rays = tuple(visit for key, visits in ray_orders.items()
                        for visit in visits)
    if (len(actual_rays) != len(expected_rays)
            or set(actual_rays) != set(expected_rays)
            or any(not isinstance(visit, LabeledRayVisit) or visit.ray != key
                   for key, visits in ray_orders.items() for visit in visits)):
        raise NormalTriangleError('ray orders differ from Arc crossing IDs')
    expected_cuts = tuple(LabeledCutVisit(owner, visit_id, gap)
                          for owner, arc in enumerate(arcs, 1)
                          for visit_id, gap in enumerate(arc.cuts, 1))
    actual_cuts = tuple(visit for visits in cut_orders.values()
                        for visit in visits)
    if (len(actual_cuts) != len(expected_cuts)
            or set(actual_cuts) != set(expected_cuts)
            or any(not isinstance(visit, LabeledCutVisit) or visit.gap != gap
                   for gap, visits in cut_orders.items() for visit in visits)):
        raise NormalTriangleError('cut orders differ from Arc visit IDs')

    selected = set(owners)
    for owner, arc in enumerate(arcs, 1):
        if owner not in selected and not (arc.is_straight(points)
                                          and abs(arc.start - arc.end) == 1):
            raise NormalTriangleError('omitted arc is not an edge-parallel chain arc')
    if (not include_outer and (cut_orders[0] or cut_orders[points]
            or any(ray_orders[side, point] for side in ('upper', 'lower')
                   for point in (1, points)))):
        raise NormalTriangleError('outer crossings need outer regions')

    terminals = {}
    expected_arcs = []

    def place_terminal(owner, role, point, neighbor, segment, arc):
        upper = (segment % 2 == 0) == arc.initial_up
        side = 'upper' if upper else 'lower'
        kind = 'puncture'
        if point in (0, points + 1):
            if not include_outer:
                raise NormalTriangleError('arc terminal needs an outer region')
            kind = 'boundary'
            gap = 0 if point == 0 else points
            left = point == 0
            vertex = f'b{point}'
        else:
            gap = point if neighbor > 2 * point else point - 1
            allowed_gap = 0 <= gap <= points if include_outer else 1 <= gap < points
            if not allowed_gap:
                raise NormalTriangleError('arc terminal needs an outer region')
            left = point == gap
            vertex = f'p{point}'
        side_index = (0 if left else 2) if upper else (2 if left else 0)
        at_start = (not left) if upper else left
        terminal_id = (owner, role)
        terminal = TerminalVisit(owner, terminal_id, terminal_id, vertex, kind)
        slot = (side, gap, side_index, at_start)
        if slot in terminals:
            raise NormalTriangleError('terminal order is unresolved')
        terminals[slot] = terminal
        return terminal

    for owner in owners:
        arc = arcs[owner - 1]
        minimum, maximum = (0, points + 1) if include_outer else (1, points)
        if not minimum <= arc.start <= maximum or not minimum <= arc.end <= maximum:
            raise NormalTriangleError('arc terminal needs an outer region')
        if arc.start_side is not None or arc.end_side is not None:
            raise NormalTriangleError('inner boundary rim terminal is unsupported')
        first_neighbor = 2 * arc.cuts[0] + 1 if arc.cuts else 2 * arc.end
        last_neighbor = 2 * arc.cuts[-1] + 1 if arc.cuts else 2 * arc.start
        start = place_terminal(owner, 'start', arc.start, first_neighbor, 0, arc)
        end = place_terminal(owner, 'end', arc.end, last_neighbor,
                             len(arc.cuts), arc)
        expected_arcs.append(ExpectedArc(owner, start, end))

    def side_visits(side, gap, index, crossings):
        begin = terminals.get((side, gap, index, True))
        end = terminals.get((side, gap, index, False))
        return tuple(visit for visit in (begin,) if visit is not None) + tuple(
            crossings) + tuple(visit for visit in (end,) if visit is not None)

    def strand_visits(visits):
        return tuple(StrandVisit(visit.owner, visit) for visit in visits)

    triangles = []
    gaps = range(points + 1) if include_outer else range(1, points)
    for gap in gaps:
        left = 'b0' if gap == 0 else f'p{gap}'
        right = f'b{points + 1}' if gap == points else f'p{gap + 1}'
        upper = NormalTriangle(('upper', gap),
                               ('north', left, right), (
            TriangleSide(('boundary', 'upper', 'left') if gap == 0 else
                         ('ray', 'upper', gap), side_visits(
                'upper', gap, 0, () if gap == 0 else
                strand_visits(reversed(ray_orders['upper', gap])))),
            TriangleSide(('cut', gap), side_visits(
                'upper', gap, 1, strand_visits(cut_orders[gap]))),
            TriangleSide(('boundary', 'upper', 'right') if gap == points else
                         ('ray', 'upper', gap + 1), side_visits(
                'upper', gap, 2, () if gap == points else
                strand_visits(ray_orders['upper', gap + 1]))),
        ))
        lower = NormalTriangle(('lower', gap),
                               ('south', right, left), (
            TriangleSide(('boundary', 'lower', 'right') if gap == points else
                         ('ray', 'lower', gap + 1), side_visits(
                'lower', gap, 0, () if gap == points else
                strand_visits(reversed(ray_orders['lower', gap + 1])))),
            TriangleSide(('cut', gap), side_visits(
                'lower', gap, 1, strand_visits(reversed(cut_orders[gap])))),
            TriangleSide(('boundary', 'lower', 'left') if gap == 0 else
                         ('ray', 'lower', gap), side_visits(
                'lower', gap, 2, () if gap == 0 else
                strand_visits(ray_orders['lower', gap]))),
        ))
        triangles.extend((upper, lower))
    return tuple(triangles), tuple(expected_arcs)


def glue_triangles(triangles, expected_arcs):
    """Join local strands and certify exactly the declared open components.

    A physical crossing must occur on both triangles incident to its edge.
    Their boundary traversals must have opposite directions, and their side
    orders must therefore agree after reversing one list. An outer edge may
    have one incident triangle only if it has no physical crossing.  Terminals
    are not edge crossings and appear in exactly one triangle slot.
    """
    triangles = tuple(triangles)
    expected_arcs = tuple(expected_arcs)
    if not triangles:
        raise NormalTriangleError('at least one triangle is required')

    slots = {}
    adjacent = {}
    edge_uses = {}
    terminal_slots = {}
    physical_edges = {}
    seen_triangles = set()

    for triangle in triangles:
        if not isinstance(triangle, NormalTriangle):
            raise NormalTriangleError('expected NormalTriangle records')
        if triangle.triangle_id in seen_triangles:
            raise NormalTriangleError('triangle IDs must be unique')
        seen_triangles.add(triangle.triangle_id)
        if len(triangle.vertices) != 3 or len(set(triangle.vertices)) != 3:
            raise NormalTriangleError('triangle vertices must be distinct')
        if len(triangle.sides) != 3:
            raise NormalTriangleError('a triangle needs three sides')
        if len({side.edge_id for side in triangle.sides}) != 3:
            raise NormalTriangleError('triangle edge IDs must be distinct')

        for side_index, side in enumerate(triangle.sides):
            if not isinstance(side, TriangleSide):
                raise NormalTriangleError('expected TriangleSide records')
            source = triangle.vertices[side_index]
            target = triangle.vertices[(side_index + 1) % 3]
            visits = tuple(side.visits)
            physical = []
            for slot_index, visit in enumerate(visits):
                if not isinstance(visit, StrandVisit):
                    raise NormalTriangleError('side visits must be StrandVisit records')
                slot = (triangle.triangle_id, side_index, slot_index)
                slots[slot] = visit
                adjacent[slot] = []
                if isinstance(visit, TerminalVisit):
                    if visit.kind not in ('puncture', 'boundary'):
                        raise NormalTriangleError('terminal kind must be puncture or boundary')
                    at_source = (visit.vertex == source and all(
                        isinstance(other, TerminalVisit) and other.vertex == source
                        for other in visits[:slot_index]))
                    at_target = (visit.vertex == target and all(
                        isinstance(other, TerminalVisit) and other.vertex == target
                        for other in visits[slot_index + 1:]))
                    if not (at_source or at_target):
                        raise NormalTriangleError('terminal must occupy its vertex end of a side')
                    if visit.terminal_id in terminal_slots:
                        raise NormalTriangleError('terminal ID occurs more than once')
                    terminal_slots[visit.terminal_id] = (visit, slot)
                else:
                    physical.append((visit, slot))
                    prior_edge = physical_edges.setdefault(visit, side.edge_id)
                    if prior_edge != side.edge_id:
                        raise NormalTriangleError('crossing ID occurs on different edges')
            if len({visit for visit, _ in physical}) != len(physical):
                raise NormalTriangleError('crossing ID repeats on one triangle side')
            edge_uses.setdefault(side.edge_id, []).append(
                (source, target, tuple(physical)))

        local_sides = tuple(side.visits for side in triangle.sides)
        for strand in pair_triangle_sides(local_sides):
            first = (triangle.triangle_id, strand.first_side, strand.first_slot)
            second = (triangle.triangle_id, strand.second_side, strand.second_slot)
            adjacent[first].append(second)
            adjacent[second].append(first)

    for edge_id, uses in edge_uses.items():
        if len(uses) > 2:
            raise NormalTriangleError('a physical edge has more than two triangles')
        source, target, first_slots = uses[0]
        if len(uses) == 1:
            if first_slots:
                raise NormalTriangleError('physical crossing has no neighboring triangle')
            continue
        other_source, other_target, second_slots = uses[1]
        if {source, target} != {other_source, other_target}:
            raise NormalTriangleError('shared edge endpoints disagree')
        if (source, target) != (other_target, other_source):
            raise NormalTriangleError('shared edge orientations must be opposite')
        second_slots = tuple(reversed(second_slots))
        if tuple(visit for visit, _ in first_slots) != tuple(
                visit for visit, _ in second_slots):
            raise NormalTriangleError('shared edge crossing order or owner differs')
        for (_, first_slot), (_, second_slot) in zip(first_slots, second_slots):
            adjacent[first_slot].append(second_slot)
            adjacent[second_slot].append(first_slot)

    expected_by_owner = {}
    expected_terminals = {}
    for expected in expected_arcs:
        if not isinstance(expected, ExpectedArc):
            raise NormalTriangleError('expected ExpectedArc records')
        if expected.owner in expected_by_owner:
            raise NormalTriangleError('each arc owner needs one declared component')
        if (not isinstance(expected.start, TerminalVisit) or
                not isinstance(expected.end, TerminalVisit) or
                expected.start.owner != expected.owner or
                expected.end.owner != expected.owner):
            raise NormalTriangleError('declared terminal owner differs from arc owner')
        if expected.start.terminal_id == expected.end.terminal_id:
            raise NormalTriangleError('arc endpoints need distinct terminal IDs')
        expected_by_owner[expected.owner] = expected
        for terminal in (expected.start, expected.end):
            if terminal.terminal_id in expected_terminals:
                raise NormalTriangleError('declared terminal ID repeats')
            expected_terminals[terminal.terminal_id] = terminal

    if set(terminal_slots) != set(expected_terminals):
        raise NormalTriangleError('terminal slots differ from declared endpoints')
    for terminal_id, (actual, _) in terminal_slots.items():
        if actual != expected_terminals[terminal_id]:
            raise NormalTriangleError('terminal slot differs from declaration')

    for slot, visit in slots.items():
        expected_degree = 1 if isinstance(visit, TerminalVisit) else 2
        if len(adjacent[slot]) != expected_degree:
            raise NormalTriangleError('strand slot has a missing or extra connection')
        if visit.owner not in expected_by_owner:
            raise NormalTriangleError('strand owner has no declared arc')

    seen_slots = set()
    result = []
    for expected in expected_arcs:
        start_slot = terminal_slots[expected.start.terminal_id][1]
        end_slot = terminal_slots[expected.end.terminal_id][1]
        current = start_slot
        previous = None
        path = []
        while True:
            if current in seen_slots:
                raise NormalTriangleError('strand path revisits a slot or component')
            seen_slots.add(current)
            visit = slots[current]
            if visit.owner != expected.owner:
                raise NormalTriangleError('strand path switches arc owner')
            path.append(current)
            if current == end_slot:
                break
            if (isinstance(visit, TerminalVisit) and current != start_slot):
                raise NormalTriangleError('strand path ends at the wrong terminal')
            next_slots = [neighbor for neighbor in adjacent[current]
                          if neighbor != previous]
            if len(next_slots) != 1:
                raise NormalTriangleError('strand path cannot reach its terminal')
            previous, current = current, next_slots[0]

        crossings = []
        for slot in path:
            visit = slots[slot]
            if isinstance(visit, TerminalVisit):
                continue
            if not crossings or crossings[-1] != visit:
                crossings.append(visit)
        result.append(GluedArc(expected.owner, expected.start, expected.end,
                               tuple(crossings)))

    if len(seen_slots) != len(slots):
        raise NormalTriangleError('unlisted strand component or cycle remains')
    return tuple(result)
