"""Certify an explicitly ordered collection of local normal triangle strands.

The caller supplies crossing order on every triangle side.  This module checks
that adjacent triangles use the same physical crossings, joins their local
strands, and reports complete labeled endpoint-to-endpoint paths.  It does not
choose crossing orders or establish minimal position for an arc itinerary.
"""

from dataclasses import dataclass
from typing import Hashable

from .normal_strands import (
    NormalTriangleError, StrandVisit, pair_triangle_sides,
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
