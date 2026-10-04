"""Local, deterministic noncrossing strands in a normal triangle.

The three side sequences follow the same orientation around the triangle's
boundary. This module only fills one triangle; it does not infer minimal
intersection counts or normalize a curve relative to a triangulation.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class StrandVisit:
    """An ordered edge crossing belonging to a labeled arc or loop."""

    owner: int
    crossing: int


@dataclass(frozen=True)
class TriangleStrand:
    """A local connection between two ordered crossings."""

    first_side: int
    first_slot: int
    second_side: int
    second_slot: int
    owner: int


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


def arc_side_ray_word(arc, *, points=6, side='upper'):
    """Reduced crossing word against rays on one side of the marked row.

    This includes arcs with a left or right outer-rim endpoint. Positive
    letters cross left-to-right. A reduced ray word is exact for the supplied
    itinerary, but this alone is not a minimal-position certificate for the
    *combined* upper/lower/horizontal triangulation.
    """
    from .braid_actions import reduce_word
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
    letters = []
    for index, (start, end) in enumerate(zip(locations, locations[1:])):
        up = (index % 2 == 0) == arc.initial_up
        if up != (side == 'upper'):
            continue
        crossed = [point for point in range(1, points + 1)
                   if min(start, end) < 2 * point < max(start, end)]
        letters.extend(crossed if start < end else (-point for point in reversed(crossed)))
    return reduce_word(letters)


def arc_side_ray_counts(arc, *, points=6, side='upper'):
    """Crossing count at each auxiliary ray, from the reduced side word."""
    from collections import Counter

    counts = Counter(abs(letter) for letter in arc_side_ray_word(arc, points=points, side=side))
    return tuple(counts[point] for point in range(1, points + 1))
