"""Local, deterministic noncrossing strands in a normal triangle.

The three side sequences follow the same orientation around the triangle's
boundary. This module only fills one triangle; it does not infer minimal
intersection counts or normalize a curve relative to a triangulation.
"""

from dataclasses import dataclass
from collections import Counter
from heapq import heappop, heappush
from math import isclose, isfinite, sqrt
from typing import Hashable


@dataclass(frozen=True)
class StrandVisit:
    """An ordered edge crossing belonging to a labeled arc or loop."""

    owner: int
    crossing: Hashable


@dataclass(frozen=True)
class ArcRayVisit:
    """One signed crossing of a marked-point ray by an Arc segment.

    ``crossing_id`` is stable within the supplied Arc itinerary. A joint
    drawing must also supply the arc owner and derive an order along the ray;
    itinerary order alone gives neither geometric ray order nor minimality.
    """

    side: str
    segment: int
    point: int
    sign: int

    @property
    def crossing_id(self):
        return self.segment, self.point

    @property
    def letter(self):
        return self.sign * self.point


@dataclass(frozen=True)
class LabeledRayVisit:
    """A stable ray crossing ID together with its arc owner."""

    owner: int
    visit: ArcRayVisit

    @property
    def ray(self):
        return self.visit.side, self.visit.point


@dataclass(frozen=True)
class LabeledCutVisit:
    """A horizontal cut endpoint, labeled by its 1-based arc and visit IDs."""

    owner: int
    cut_visit_id: int
    gap: int


@dataclass(frozen=True)
class TriangleStrand:
    """A local connection between two ordered crossings."""

    first_side: int
    first_slot: int
    second_side: int
    second_slot: int
    owner: int


@dataclass(frozen=True)
class ArcGapTriangleCounts:
    """One inner gap's side counts, retaining puncture endpoints separately.

    A terminal is a vertex of the triangle, not a crossing of its vertical
    ray. It occupies a formal slot on that side only when testing numerical
    admissibility. An eventual gluer must still attach the strand to the
    vertex rather than to a ray crossing.
    """

    gap: int
    side: str
    left_ray: int
    chain_cut: int
    right_ray: int
    left_terminal: int = 0
    right_terminal: int = 0

    def formal_pair_counts(self):
        """Test parity and triangle inequalities with terminal vertex slots."""
        return triangle_pair_counts(self.left_ray + self.left_terminal,
                                    self.chain_cut,
                                    self.right_ray + self.right_terminal)


class NormalTriangleError(ValueError):
    """Counts or labels cannot be realized by this normal triangle."""


def resolve_ray_order(visits, precedences):
    """Resolve supplied strict precedences on one physical ray, if unique.

    Each ``(before, after)`` pair uses the caller's chosen ray direction.
    These constraints must come from certified geometry, terminal anchors, or
    local strand arguments; this function does not derive them from itineraries.
    A partial order has a unique linear extension exactly when every step of
    topological sorting has one available visit. Ambiguity is reported rather
    than broken by owner or segment number.
    """
    visits = tuple(visits)
    if any(not isinstance(visit, LabeledRayVisit) or
           not isinstance(visit.visit, ArcRayVisit) for visit in visits):
        raise NormalTriangleError('ray order needs labeled ray visits')
    if len(set(visits)) != len(visits):
        raise NormalTriangleError('ray order repeats a visit')
    if len({(visit.owner, visit.visit.segment, visit.visit.point)
            for visit in visits}) != len(visits):
        raise NormalTriangleError('ray order repeats a crossing ID')
    if len({visit.ray for visit in visits}) > 1:
        raise NormalTriangleError('ray order combines different rays')

    positions = {visit: index for index, visit in enumerate(visits)}
    successors = [set() for _ in visits]
    indegree = [0] * len(visits)
    for before, after in precedences:
        if before not in positions or after not in positions:
            raise NormalTriangleError('ray precedence names an unknown visit')
        source, target = positions[before], positions[after]
        if target not in successors[source]:
            successors[source].add(target)
            indegree[target] += 1

    available = []
    for index, degree in enumerate(indegree):
        if degree == 0:
            heappush(available, index)
    order = []
    first_tie = None
    while available:
        if len(available) > 1 and first_tie is None:
            first_tie = tuple(visits[index] for index in sorted(available))
        index = heappop(available)
        order.append(visits[index])
        for successor in successors[index]:
            indegree[successor] -= 1
            if indegree[successor] == 0:
                heappush(available, successor)
    if len(order) != len(visits):
        raise NormalTriangleError('ray precedence constraints contain a cycle')
    if first_tie is not None:
        raise NormalTriangleError(f'ray order has unresolved ties: {first_tie!r}')
    return tuple(order)


def triangle_pair_counts(a, b, c):
    """Return counts joining sides 0–1, 1–2, and 2–0, respectively."""
    if any(type(value) is not int or value < 0 for value in (a, b, c)):
        raise NormalTriangleError('side crossing counts must be nonnegative integers')
    if (a + b + c) % 2 or a + b < c or b + c < a or c + a < b:
        raise NormalTriangleError('triangle crossings violate parity or triangle inequalities')
    return ((a + b - c) // 2, (b + c - a) // 2, (c + a - b) // 2)


def pair_triangle_sides(sides):
    """Fill a triangle without crossings, preserving each strand's owner.

    ``sides`` contains three crossing sequences in cyclic boundary order.
    Crossings on neighboring sides closest to their shared vertex pair first;
    successive pairs nest around them. A label mismatch is an inconsistent
    proposed joint placement, never permission to reconnect different arcs.
    """
    if len(sides) != 3:
        raise NormalTriangleError('a triangle needs three side sequences')
    sides = tuple(tuple(side) for side in sides)
    if any(not isinstance(visit, StrandVisit) for side in sides for visit in side):
        raise NormalTriangleError('each crossing needs an arc owner and ID')
    n01, n12, n20 = triangle_pair_counts(*(len(side) for side in sides))
    strands = []

    def connect(first_side, first_slot, second_side, second_slot):
        first = sides[first_side][first_slot]
        second = sides[second_side][second_slot]
        if first.owner != second.owner:
            raise NormalTriangleError('normal pairing would reconnect different arcs')
        strands.append(TriangleStrand(first_side, first_slot,
                                      second_side, second_slot, first.owner))

    for offset in range(n01):
        connect(0, len(sides[0]) - 1 - offset, 1, offset)
    for offset in range(n12):
        connect(1, len(sides[1]) - 1 - offset, 2, offset)
    for offset in range(n20):
        connect(2, len(sides[2]) - 1 - offset, 0, offset)
    return tuple(strands)


def _reduce_ray_visits(visits):
    """Freely reduce signed visits while retaining the surviving event IDs."""
    result = []
    for visit in visits:
        if result and result[-1].letter == -visit.letter:
            result.pop()
        else:
            result.append(visit)
    return tuple(result)


def arc_side_ray_visits(arc, side='upper', points=6):
    """Reduced signed ray visits, each tied to its source segment and point.

    This includes arcs with a left or right outer-rim endpoint. Positive
    signs cross left-to-right. Reduction removes inverse visits even when
    their source segments differ. The surviving ``crossing_id`` values are
    identifiers, not a claimed order of crossings on any physical ray.
    """
    from .curves import Arc

    if not isinstance(arc, Arc) or type(points) is not int or points < 1:
        raise ValueError('Expected an Arc and a positive marked-point count')
    if side not in ('upper', 'lower'):
        raise ValueError("side must be 'upper' or 'lower'")
    if max(arc.start, arc.end) > points + 1 or any(cut > points for cut in arc.cuts):
        raise ValueError('arc endpoint or cut exceeds the marked row')
    if arc.start_side is not None or arc.end_side is not None:
        raise ValueError('inner-boundary rim endpoints need a separate convention')

    locations = (2 * arc.start,) + tuple(2 * cut + 1 for cut in arc.cuts) + (2 * arc.end,)
    visits = []
    for index, (start, end) in enumerate(zip(locations, locations[1:])):
        up = (index % 2 == 0) == arc.initial_up
        if up != (side == 'upper'):
            continue
        crossed = [point for point in range(1, points + 1)
                   if min(start, end) < 2 * point < max(start, end)]
        sign = 1 if start < end else -1
        visits.extend(ArcRayVisit(side, index, point, sign)
                      for point in (crossed if sign > 0 else reversed(crossed)))
    return _reduce_ray_visits(visits)


def arc_side_ray_word(arc, *, points=6, side='upper'):
    """Reduced crossing word against rays on one side of the marked row.

    A reduced ray word is exact for the supplied itinerary, but this alone is
    not a minimal-position certificate for the combined triangulation.
    """
    return tuple(visit.letter for visit in arc_side_ray_visits(
        arc, side=side, points=points))


def arc_side_ray_counts(arc, *, points=6, side='upper'):
    """Crossing count at each auxiliary ray, from the reduced side word."""
    counts = Counter(abs(letter) for letter in arc_side_ray_word(arc, points=points, side=side))
    return tuple(counts[point] for point in range(1, points + 1))


def _ray_height(piece, x):
    """Distance from the marked row to a half-ellipse at an interior x."""
    radius = abs(piece.end - piece.start) / 2
    middle = (piece.start + piece.end) / 2
    unit = (x - middle) / radius
    return radius * piece.aspect * sqrt(max(0., 1 - unit * unit))


def _validate_arc_layout(arc, pieces, xs):
    """Check that route pieces follow one Arc and retain each declared cut."""
    from .curves import HalfEllipse

    points = len(xs) - 2
    if (max(arc.start, arc.end) > points + 1
            or any(cut > points for cut in arc.cuts)
            or arc.start_side is not None or arc.end_side is not None):
        raise ValueError('arc endpoint or cut exceeds the marked row, or uses a rim endpoint')
    if len(pieces) != len(arc.cuts) + 1 or any(
            not isinstance(piece, HalfEllipse) for piece in pieces):
        raise NormalTriangleError('layout does not contain the Arc segments')
    straight = arc.is_straight(points)
    for index, piece in enumerate(pieces):
        expected_up = (index % 2 == 0) == arc.initial_up
        if (piece.up != (None if straight else expected_up)
                or not all(isfinite(value) for value in
                           (piece.start, piece.end, piece.aspect))
                or piece.start == piece.end
                or (not straight and piece.aspect <= 0)):
            raise NormalTriangleError('layout segment disagrees with Arc side or geometry')
        if index and (piece.start != pieces[index - 1].end
                      or piece.start_node != pieces[index - 1].end_node
                      or piece.owner != pieces[index - 1].owner):
            raise NormalTriangleError('layout segments do not join in itinerary order')
    if pieces[0].start != xs[arc.start] or pieces[-1].end != xs[arc.end]:
        raise NormalTriangleError('layout endpoints disagree with the Arc')
    for index, cut in enumerate(arc.cuts):
        if not xs[cut] < pieces[index].end < xs[cut + 1]:
            raise NormalTriangleError('layout cut visit lies outside its gap')


def single_arc_ray_orders(arc, pieces, reference_xs):
    """Read surviving crossing IDs from one already accepted Arc layout.

    ``reference_xs`` lists the left outer tip, marked points, and right outer
    tip in increasing x order. Each returned tuple runs from the marked point
    outward along its upper or lower vertical ray. Half-ellipse heights are
    evaluated analytically at that x coordinate. This only orders visits of
    this one arc; separate layouts provide no order between different arcs.
    """
    from .curves import Arc

    xs = tuple(reference_xs)
    pieces = tuple(pieces)
    points = len(xs) - 2
    if (not isinstance(arc, Arc) or points < 1
            or any(not isinstance(x, (int, float)) or not isfinite(x) for x in xs)
            or any(left >= right for left, right in zip(xs, xs[1:]))):
        raise ValueError('expected an Arc and increasing finite reference coordinates')
    # This also checks point/cut bounds and the endpoint convention.
    visits = tuple(arc_side_ray_visits(arc, side=side, points=points)
                   for side in ('upper', 'lower'))
    _validate_arc_layout(arc, pieces, xs)

    orders = {}
    for side, side_visits in zip(('upper', 'lower'), visits):
        for point in range(1, points + 1):
            ray = []
            x = xs[point]
            for visit in side_visits:
                if visit.point != point:
                    continue
                piece = pieces[visit.segment]
                if not min(piece.start, piece.end) < x < max(piece.start, piece.end):
                    raise NormalTriangleError('ray visit disagrees with layout geometry')
                ray.append((_ray_height(piece, x), visit))
            ray.sort(key=lambda item: item[0])
            if any(isclose(first[0], second[0], rel_tol=1e-12, abs_tol=1e-10)
                   for first, second in zip(ray, ray[1:])):
                raise NormalTriangleError('ray crossings have indistinguishable heights')
            orders[side, point] = tuple(visit for _, visit in ray)
    return orders


def joint_arc_ray_orders(arcs, pieces, reference_xs):
    """Read common physical ray orders from one already accepted joint layout.

    ``arcs`` are the route's Arc curves in owner order; ``pieces`` are its
    complete, unsplit HalfEllipse sequence. Route owners are zero-based, while
    returned LabeledRayVisit owners are one-based chain-arc labels. Each tuple
    runs from its marked point outward (up on upper rays, down on lower rays).
    The caller supplies a jointly accepted placement; this reader does not
    construct or certify a noncrossing placement from the itineraries.
    """
    from .curves import Arc, HalfEllipse

    arcs = tuple(arcs)
    pieces = tuple(pieces)
    xs = tuple(reference_xs)
    if not arcs or any(not isinstance(arc, Arc) for arc in arcs):
        raise ValueError('expected one or more Arc curves in route owner order')
    if any(not isinstance(piece, HalfEllipse) for piece in pieces):
        raise NormalTriangleError('joint layout needs HalfEllipse segments')
    if len(pieces) != sum(len(arc.cuts) + 1 for arc in arcs):
        raise NormalTriangleError('joint layout does not contain every Arc segment')

    grouped = []
    offset = 0
    for owner, arc in enumerate(arcs):
        count = len(arc.cuts) + 1
        owned = pieces[offset:offset + count]
        if any(piece.owner != owner for piece in owned):
            raise NormalTriangleError('joint layout segment owner disagrees with Arc route order')
        grouped.append(owned)
        offset += count

    orders = {('upper', point): [] for point in range(1, len(xs) - 1)}
    orders.update({('lower', point): [] for point in range(1, len(xs) - 1)})
    for owner, (arc, owned) in enumerate(zip(arcs, grouped), 1):
        individual = single_arc_ray_orders(arc, owned, xs)
        for (side, point), visits in individual.items():
            x = xs[point]
            orders[side, point].extend(
                (_ray_height(owned[visit.segment], x), LabeledRayVisit(owner, visit))
                for visit in visits)

    result = {}
    for ray, crossings in orders.items():
        crossings.sort(key=lambda item: item[0])
        if any(isclose(first[0], second[0], rel_tol=1e-12, abs_tol=1e-10)
               for first, second in zip(crossings, crossings[1:])):
            raise NormalTriangleError('joint ray crossings have indistinguishable heights')
        result[ray] = tuple(visit for _, visit in crossings)
    return result


def joint_arc_cut_orders(arcs, pieces, reference_xs):
    """Read x orders of labeled cut visits from an accepted joint Arc route.

    ``reference_xs`` runs from the left outer tip through the marked row to
    the right outer tip. Result keys are gaps 0..n, including empty gaps;
    tuples run left to right. Route owners are zero-based, while the returned
    arc owner and cut-visit ID are one-based. This reads a supplied placement;
    it does not construct one from itineraries.
    """
    from .curves import Arc, HalfEllipse

    arcs = tuple(arcs)
    pieces = tuple(pieces)
    xs = tuple(reference_xs)
    if not arcs or any(not isinstance(arc, Arc) for arc in arcs):
        raise ValueError('expected one or more Arc curves in route owner order')
    if (len(xs) < 3
            or any(not isinstance(x, (int, float)) or not isfinite(x) for x in xs)
            or any(left >= right for left, right in zip(xs, xs[1:]))):
        raise ValueError('expected increasing finite reference coordinates')
    if (len(pieces) != sum(len(arc.cuts) + 1 for arc in arcs)
            or any(not isinstance(piece, HalfEllipse) for piece in pieces)):
        raise NormalTriangleError('joint layout does not contain every Arc segment')

    orders = {gap: [] for gap in range(len(xs) - 1)}
    offset = 0
    for owner, arc in enumerate(arcs):
        count = len(arc.cuts) + 1
        owned = pieces[offset:offset + count]
        if any(piece.owner != owner for piece in owned):
            raise NormalTriangleError('joint layout segment owner disagrees with Arc route order')
        _validate_arc_layout(arc, owned, xs)
        for index, gap in enumerate(arc.cuts):
            orders[gap].append((owned[index].end,
                                LabeledCutVisit(owner + 1, index + 1, gap)))
        offset += count

    result = {}
    for gap, visits in orders.items():
        visits.sort(key=lambda item: item[0])
        if any(isclose(first[0], second[0], rel_tol=1e-12, abs_tol=1e-10)
               for first, second in zip(visits, visits[1:])):
            raise NormalTriangleError('joint cut visits have indistinguishable x positions')
        result[gap] = tuple(visit for _, visit in visits)
    return result


def arc_gap_triangle_counts(arc, *, points=6, side='upper'):
    """Return inner-gap counts from one exact Arc itinerary.

    Each cut at gap j meets both the upper and lower triangle's chain side.
    The first and last segments determine which triangle contains each
    puncture endpoint. Outer-rim endpoints and cuts belong to outer regions,
    not these ``points - 1`` inner triangles. Counts alone do not certify a
    joint normal drawing or the order of different arcs along shared rays.
    """
    rays = arc_side_ray_counts(arc, points=points, side=side)
    cuts = Counter(arc.cuts)
    locations = ((2 * arc.start,) + tuple(2 * cut + 1 for cut in arc.cuts)
                 + (2 * arc.end,))
    terminals = [[0, 0] for _ in range(points - 1)]
    for point, neighbor, segment_index in (
            (arc.start, locations[1], 0),
            (arc.end, locations[-2], len(locations) - 2)):
        if not 1 <= point <= points:
            continue
        segment_upper = (segment_index % 2 == 0) == arc.initial_up
        if segment_upper != (side == 'upper'):
            continue
        gap = point if neighbor > 2 * point else point - 1
        if 1 <= gap < points:
            terminals[gap - 1][0 if point == gap else 1] += 1
    return tuple(ArcGapTriangleCounts(
        gap, side, rays[gap - 1], cuts[gap], rays[gap],
        *terminals[gap - 1]) for gap in range(1, points))
