"""Infer small shared-edge orders from labeled local triangle connections.

Every comparison follows the two noncrossing rules inside a triangle: chords
to different partner sides occupy fixed blocks, while chords to the same side
have reversed boundary order at their partners. Terminal vertices anchor the
recursion. No route coordinates or owner-based ordering enter the result.

This is a quadratic, deliberately bounded resolver for small arc systems. It
does not establish minimal position or claim to scale to the F11 itineraries.
"""

from collections import defaultdict, deque
from dataclasses import dataclass

from .normal_gluing import TerminalVisit
from .normal_itinerary import LocalTriangleConnection, arc_local_connections
from .normal_strands import (
    LabeledCutVisit, LabeledRayVisit, NormalTriangleError, StrandVisit,
)


@dataclass(frozen=True)
class _End:
    side: int
    partner_side: int
    partner: StrandVisit


def _side_edge(triangle, side_index, points):
    """Return the physical edge and boundary-to-physical orientation sign."""
    hemisphere, gap = triangle
    if hemisphere not in ('upper', 'lower') or not 0 <= gap <= points:
        raise NormalTriangleError('unknown local triangle')
    if side_index not in (0, 1, 2):
        raise NormalTriangleError('unknown local triangle side')
    if side_index == 1:
        return ('cut', gap), 1 if hemisphere == 'upper' else -1
    if hemisphere == 'upper':
        point = gap if side_index == 0 else gap + 1
        orientation = -1 if side_index == 0 else 1
    else:
        point = gap + 1 if side_index == 0 else gap
        orientation = -1 if side_index == 0 else 1
    if not 1 <= point <= points:
        return ('boundary', hemisphere, point), orientation
    return ('ray', hemisphere, point), orientation


def _side_vertices(triangle, side_index, points):
    hemisphere, gap = triangle
    left = 'b0' if gap == 0 else f'p{gap}'
    right = f'b{points + 1}' if gap == points else f'p{gap + 1}'
    vertices = (('north', left, right) if hemisphere == 'upper'
                else ('south', right, left))
    return vertices[side_index], vertices[(side_index + 1) % 3]


def _terminal_boundary_order(first, second, triangle, side_index, points):
    """Return first-before-second on this side, if a vertex anchors it."""
    source, target = _side_vertices(triangle, side_index, points)

    def position(event):
        if not isinstance(event, TerminalVisit):
            return 1
        if event.vertex == source:
            return 0
        if event.vertex == target:
            return 2
        raise NormalTriangleError('terminal is not on its declared triangle side')

    a, b = position(first), position(second)
    if a == b:
        return None
    return 1 if a < b else -1


def _block_boundary_order(side, first_partner, second_partner):
    # Boundary traversal is 0 -> 1 -> 2 -> 0. The block nearest the
    # preceding vertex comes first on each side.
    blocks = ({2: 0, 1: 1}, {0: 0, 2: 1}, {1: 0, 0: 1})[side]
    return 1 if blocks[first_partner] < blocks[second_partner] else -1


class _ComparisonResolver:
    def __init__(self, connections, points):
        self.points = points
        self.incidences = defaultdict(dict)
        self.edge_visits = defaultdict(list)
        self.numbers = {}
        self.cache = {}
        for connection in connections:
            if not isinstance(connection, LocalTriangleConnection):
                raise NormalTriangleError('expected local triangle connections')
            if connection.first_side == connection.second_side:
                raise NormalTriangleError('local chord joins one side to itself')
            for event, side, partner, partner_side in (
                    (connection.first, connection.first_side,
                     connection.second, connection.second_side),
                    (connection.second, connection.second_side,
                     connection.first, connection.first_side)):
                if (not isinstance(event, StrandVisit)
                        or event.owner != connection.owner):
                    raise NormalTriangleError('local connection has inconsistent owner')
                edge, _ = _side_edge(connection.triangle_id, side, points)
                if not isinstance(event, TerminalVisit):
                    crossing = event.crossing
                    if isinstance(crossing, LabeledRayVisit):
                        expected = ('ray', *crossing.ray)
                    elif isinstance(crossing, LabeledCutVisit):
                        expected = ('cut', crossing.gap)
                    else:
                        raise NormalTriangleError('unknown crossing ID')
                    if edge != expected or crossing.owner != event.owner:
                        raise NormalTriangleError('crossing lies on the wrong edge')
                elif event.vertex not in _side_vertices(
                        connection.triangle_id, side, points):
                    raise NormalTriangleError(
                        'terminal is not on its declared triangle side')
                uses = self.incidences[event]
                if connection.triangle_id in uses:
                    raise NormalTriangleError('event repeats in one triangle')
                uses[connection.triangle_id] = _End(side, partner_side, partner)
                if event not in self.numbers:
                    self.numbers[event] = len(self.numbers)
                    if not isinstance(event, TerminalVisit):
                        self.edge_visits[edge].append(event)

        for event, uses in self.incidences.items():
            expected = 1 if isinstance(event, TerminalVisit) else 2
            if len(uses) != expected:
                raise NormalTriangleError('event has incomplete triangle incidences')

    def _pair(self, first, second):
        if first == second:
            raise NormalTriangleError('cannot compare a crossing with itself')
        a, b = self.numbers[first], self.numbers[second]
        return ((first, second), 1) if a < b else ((second, first), -1)

    def compare(self, first, second):
        """Return +1 when first precedes second in physical edge order."""
        root, flip = self._pair(first, second)
        if root in self.cache:
            return flip * self.cache[root]
        # The queue records d_state = parity[state] * d_root. Pair identity
        # numbers merely normalize memo keys; they never choose an order.
        parity = {root: 1}
        queue = deque((root,))
        fixed = None
        while queue:
            pair = queue.popleft()
            a, b = pair
            shared = self.incidences[a].keys() & self.incidences[b].keys()
            if not shared:
                raise NormalTriangleError('two visits have no common triangle')
            for triangle in shared:
                ea, eb = self.incidences[a][triangle], self.incidences[b][triangle]
                if ea.side != eb.side:
                    raise NormalTriangleError('paired visits occupy different sides')
                _, edge_orientation = _side_edge(triangle, ea.side, self.points)
                if ea.partner_side != eb.partner_side:
                    boundary = _block_boundary_order(
                        ea.side, ea.partner_side, eb.partner_side)
                    candidate = parity[pair] * edge_orientation * boundary
                else:
                    partner_a, partner_b = ea.partner, eb.partner
                    anchor = _terminal_boundary_order(
                        partner_a, partner_b, triangle, ea.partner_side,
                        self.points)
                    if anchor is not None:
                        candidate = parity[pair] * -edge_orientation * anchor
                    elif (isinstance(partner_a, TerminalVisit)
                          or isinstance(partner_b, TerminalVisit)):
                        # Two distinct terminals at the same vertex have no
                        # boundary order supplied by their itineraries.
                        continue
                    else:
                        next_pair, next_flip = self._pair(partner_a, partner_b)
                        _, partner_orientation = _side_edge(
                            triangle, ea.partner_side, self.points)
                        relation = (-edge_orientation * partner_orientation
                                    * next_flip)
                        next_parity = parity[pair] * relation
                        if next_pair in parity:
                            if parity[next_pair] != next_parity:
                                raise NormalTriangleError(
                                    'local comparison constraints contain a cycle')
                        elif next_pair in self.cache:
                            candidate = next_parity * self.cache[next_pair]
                            if fixed is not None and fixed != candidate:
                                raise NormalTriangleError(
                                    'local comparison constraints conflict')
                            fixed = candidate
                        else:
                            parity[next_pair] = next_parity
                            queue.append(next_pair)
                        continue
                if fixed is not None and fixed != candidate:
                    raise NormalTriangleError('local comparison constraints conflict')
                fixed = candidate
        if fixed is None:
            raise NormalTriangleError(f'shared edge has unresolved comparison: {root!r}')
        for pair, sign in parity.items():
            result = sign * fixed
            if pair in self.cache and self.cache[pair] != result:
                raise NormalTriangleError('local comparison constraints conflict')
            self.cache[pair] = result
        return flip * fixed


def resolve_connection_orders(connections, *, points=6, max_pairs=10000):
    """Resolve all ray and cut orders from a small set of local chords.

    Ray tuples run outward from their marked point; cut tuples run left to
    right. Every pair must be determined by triangle blocks, transfer, or a
    terminal anchor. Conflicts, cycles, ambiguity, and an oversized quadratic
    comparison workload raise ``NormalTriangleError``.
    """
    if type(points) is not int or points < 2:
        raise ValueError('points must be at least two')
    if type(max_pairs) is not int or max_pairs < 0:
        raise ValueError('max_pairs must be nonnegative')
    resolver = _ComparisonResolver(tuple(connections), points)
    pair_count = sum(len(visits) * (len(visits) - 1) // 2
                     for visits in resolver.edge_visits.values())
    if pair_count > max_pairs:
        raise NormalTriangleError(
            f'{pair_count} shared-edge comparisons exceed max_pairs={max_pairs}')

    def order(visits):
        visits = tuple(visits)
        if len(visits) < 2:
            return visits
        outgoing = {visit: set() for visit in visits}
        indegree = {visit: 0 for visit in visits}
        for i, first in enumerate(visits):
            for second in visits[i + 1:]:
                sign = resolver.compare(first, second)
                before, after = (first, second) if sign == 1 else (second, first)
                outgoing[before].add(after)
                indegree[after] += 1
        result = []
        remaining = set(visits)
        while remaining:
            ready = [visit for visit in remaining if indegree[visit] == 0]
            if not ready:
                raise NormalTriangleError('shared-edge order constraints contain a cycle')
            if len(ready) != 1:
                raise NormalTriangleError('shared edge has unresolved order')
            current = ready[0]
            result.append(current.crossing)
            remaining.remove(current)
            for successor in outgoing[current]:
                indegree[successor] -= 1
        return tuple(result)

    rays = {(side, point): order(resolver.edge_visits['ray', side, point])
            for side in ('upper', 'lower') for point in range(1, points + 1)}
    cuts = {gap: order(resolver.edge_visits['cut', gap])
            for gap in range(points + 1)}
    return rays, cuts


def resolve_arc_orders(arcs, *, owners=None, points=6, max_pairs=10000):
    """Derive complete small-system orders from exact ``Arc`` itineraries.

    ``owners`` selects one-based arc labels in ``arcs``. An F1 chain may select
    its winding owners and leave straight edge-parallel arcs on the triangle
    boundary. No route data is read.
    """
    arcs = tuple(arcs)
    owners = tuple(range(1, len(arcs) + 1) if owners is None else owners)
    if (not owners or len(set(owners)) != len(owners)
            or any(type(owner) is not int or not 1 <= owner <= len(arcs)
                   for owner in owners)):
        raise ValueError('owners must be distinct one-based arc labels')
    connections = tuple(connection for owner in owners
                        for connection in arc_local_connections(
                            arcs[owner - 1], points=points, owner=owner))
    return resolve_connection_orders(connections, points=points,
                                     max_pairs=max_pairs)
