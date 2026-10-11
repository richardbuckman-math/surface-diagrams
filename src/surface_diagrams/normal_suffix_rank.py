"""Resolve shared-edge orders by ranking directed, finite strand suffixes.

For a crossing viewed from one incident triangle, the local chord supplies a
partner-side block and either a terminal marker or the next crossing viewed
from its *other* triangle. Reversing the order at the chord partner and again
across the shared edge cancels, so suffix lexicographic order is exactly the
triangle's boundary order. Integer prefix doubling ranks all such suffixes in
O(N log N) time and O(N) space without comparing crossing pairs recursively.
"""

from .normal_gluing import TerminalVisit, _PARTNER_BLOCKS
from .normal_itinerary import arc_local_connections
from .normal_order import _ComparisonResolver, _side_edge, _side_vertices
from .normal_strands import NormalTriangleError


def _counting_sort(indices, keys, maximum):
    """Stable integer-key sort, with keys in 0..maximum."""
    starts = [0] * (maximum + 1)
    for index in indices:
        starts[keys[index]] += 1
    total = 0
    for key, count in enumerate(starts):
        starts[key], total = total, total + count
    result = [0] * len(indices)
    for index in indices:
        key = keys[index]
        result[starts[key]] = index
        starts[key] += 1
    return result


def _suffix_ranks(tokens, successors):
    """Dense lexicographic ranks of finite token strings on a successor graph."""
    size = len(tokens)
    if not size:
        return []
    # The initial token alphabet has two partner blocks and three markers.
    ranks = list(tokens)
    classes = max(ranks) + 1
    jumps = list(successors)
    prefix = 1
    while any(jump >= 0 for jump in jumps):
        if prefix >= size:
            raise NormalTriangleError('directed strand suffix does not terminate')
        first = [rank + 1 for rank in ranks]
        second = [ranks[jump] + 1 if jump >= 0 else 0 for jump in jumps]
        ordered = _counting_sort(range(size), second, classes)
        ordered = _counting_sort(ordered, first, classes)
        next_ranks = [0] * size
        previous = None
        next_class = -1
        for index in ordered:
            pair = (first[index], second[index])
            if pair != previous:
                next_class += 1
                previous = pair
            next_ranks[index] = next_class
        ranks = next_ranks
        classes = next_class + 1
        jumps = [jumps[jump] if jump >= 0 else -1 for jump in jumps]
        prefix *= 2
    return ranks


def _directed_states(resolver):
    states = [(visit, triangle)
              for visit in resolver.numbers
              if not isinstance(visit, TerminalVisit)
              for triangle in resolver.incidences[visit]]
    indices = {state: index for index, state in enumerate(states)}
    tokens = []
    successors = []
    for visit, triangle in states:
        end = resolver.incidences[visit][triangle]
        block = _PARTNER_BLOCKS[end.side][end.partner_side]
        partner = end.partner
        if isinstance(partner, TerminalVisit):
            source, target = _side_vertices(
                triangle, end.partner_side, resolver.points)
            if partner.vertex == target:
                marker = 0
            elif partner.vertex == source:
                marker = 2
            else:
                raise NormalTriangleError('terminal is not on its declared triangle side')
            successor = -1
        else:
            marker = 1
            other_triangles = resolver.incidences[partner].keys() - {triangle}
            if len(other_triangles) != 1:
                raise NormalTriangleError('crossing partner has no other triangle')
            successor = indices[partner, next(iter(other_triangles))]
        tokens.append(3 * block + marker)
        successors.append(successor)
    return indices, tokens, successors


def _edge_orders(resolver, indices, ranks):
    orders = {}
    for edge, visits in resolver.edge_visits.items():
        if not visits:
            continue
        triangles = tuple(resolver.incidences[visits[0]])
        if len(triangles) != 2:
            raise NormalTriangleError('physical edge has incomplete incidences')

        def key(visit):
            uses = resolver.incidences[visit]
            if set(uses) != set(triangles):
                raise NormalTriangleError('physical edge incidences disagree')
            return tuple(_side_edge(triangle, uses[triangle].side,
                                    resolver.points)[1]
                         * ranks[indices[visit, triangle]]
                         for triangle in triangles)

        keyed = sorted(((key(visit), visit) for visit in visits),
                       key=lambda item: item[0])
        # Lexicographic sorting by the two incident ranks is valid only when
        # both triangles' non-tied orders agree. Either side may resolve a tie
        # left by the other; a tie on both sides remains genuinely ambiguous.
        for (before, _), (after, _) in zip(keyed, keyed[1:]):
            if before == after:
                raise NormalTriangleError(
                    f'shared edge has unresolved comparison: {edge!r}')
            if before[1] > after[1]:
                raise NormalTriangleError(
                    f'local comparison constraints conflict on {edge!r}')
        orders[edge] = tuple(visit for _, visit in keyed)
    return orders


def resolve_connection_orders(connections, *, points=6):
    """Resolve all ray and cut orders from labeled local chords, without routes.

    Reject incomplete incidences, unresolved equal suffixes, disagreement
    between incident triangles, and a noncanonical local triangle pairing.
    """
    if type(points) is not int or points < 2:
        raise ValueError('points must be at least two')
    resolver = _ComparisonResolver(tuple(connections), points, max_pairs=0)
    indices, tokens, successors = _directed_states(resolver)
    ranks = _suffix_ranks(tokens, successors)
    orders = _edge_orders(resolver, indices, ranks)
    resolver.check_triangle_orders(orders)
    rays = {(side, point): tuple(visit.crossing for visit in
                                  orders.get(('ray', side, point), ()))
            for side in ('upper', 'lower') for point in range(1, points + 1)}
    cuts = {gap: tuple(visit.crossing for visit in
                       orders.get(('cut', gap), ()))
            for gap in range(points + 1)}
    return rays, cuts


def resolve_arc_orders(arcs, *, owners=None, points=6):
    """Resolve all physical edge orders from exact Arc itineraries."""
    arcs = tuple(arcs)
    owners = tuple(range(1, len(arcs) + 1) if owners is None else owners)
    if (not owners or len(set(owners)) != len(owners)
            or any(type(owner) is not int or not 1 <= owner <= len(arcs)
                   for owner in owners)):
        raise ValueError('owners must be distinct one-based arc labels')
    connections = tuple(connection for owner in owners
                        for connection in arc_local_connections(
                            arcs[owner - 1], points=points, owner=owner))
    return resolve_connection_orders(connections, points=points)
