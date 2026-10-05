"""Local, deterministic noncrossing strands in a normal triangle.

The three side sequences follow the same orientation around the triangle's
boundary. This module only fills one triangle; it does not infer minimal
intersection counts or normalize a curve relative to a triangulation.
"""

from dataclasses import dataclass
from collections import Counter


@dataclass(frozen=True)
class StrandVisit:
    """An ordered edge crossing belonging to a labeled arc or loop."""

    owner: int
    crossing: int


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
