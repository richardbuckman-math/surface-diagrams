"""Extract labeled local triangle connections from one Arc itinerary.

This records which events meet inside each upper or lower gap triangle. It
does not order visits along a shared edge or certify a joint drawing.
"""

from dataclasses import dataclass

from .normal_gluing import TerminalVisit
from .normal_strands import (
    ArcRayVisit, LabeledCutVisit, LabeledRayVisit, NormalTriangleError,
    StrandVisit, arc_side_ray_visits,
)


@dataclass(frozen=True)
class LocalTriangleConnection:
    """One itinerary-directed connection in triangle ``(side, gap)``.

    Side indices use the oriented convention of ``NormalTriangle``:
    upper sides are left ray, cut, right ray; lower sides are right ray,
    cut, left ray. ``first`` and ``second`` retain their labeled event IDs.
    """

    owner: int
    triangle_id: tuple[str, int]
    first_side: int
    first: StrandVisit
    second_side: int
    second: StrandVisit


def _triangle_side(side, gap, coordinate):
    if coordinate == 2 * gap + 1:
        return 1
    if coordinate == 2 * gap:
        return 0 if side == 'upper' else 2
    if coordinate == 2 * gap + 2:
        return 2 if side == 'upper' else 0
    raise NormalTriangleError('consecutive itinerary events skip a triangle')


def arc_local_connections(arc, *, points=6, owner=1):
    """Derive all triangle connections in one unreduced Arc itinerary.

    Marked points are 1..``points``; 0 and ``points + 1`` are outer boundary
    tips. The result is in start-to-end path order. A physical ray or cut
    crossing occurs at the end of one connection and start of the next, while
    each terminal occurs once. Ray cancellation is rejected because it would
    discard source event IDs and disagree with ``arc_gap_triangle_counts``.
    """
    if type(owner) is not int or owner < 1:
        raise ValueError('owner must be a positive one-based arc label')

    # Validate the same Arc domain and retain the reduced visits used by the
    # triangle count API, without changing this itinerary's event identities.
    reduced = {side: arc_side_ray_visits(arc, side=side, points=points)
               for side in ('upper', 'lower')}
    locations = ((2 * arc.start,) + tuple(2 * gap + 1 for gap in arc.cuts)
                 + (2 * arc.end,))
    cut_visits = tuple(StrandVisit(
        owner, LabeledCutVisit(owner, visit_id, gap))
        for visit_id, gap in enumerate(arc.cuts, 1))

    def terminal(role, point):
        terminal_id = (owner, role)
        boundary = point in (0, points + 1)
        return TerminalVisit(owner, terminal_id, terminal_id,
                             f'{"b" if boundary else "p"}{point}',
                             'boundary' if boundary else 'puncture')

    start = terminal('start', arc.start)
    end = terminal('end', arc.end)
    raw_rays = {'upper': [], 'lower': []}
    connections = []
    for segment, (begin, finish) in enumerate(zip(locations, locations[1:])):
        side = 'upper' if (segment % 2 == 0) == arc.initial_up else 'lower'
        events = [(begin, start if segment == 0 else cut_visits[segment - 1])]
        crossed = [point for point in range(1, points + 1)
                   if min(begin, finish) < 2 * point < max(begin, finish)]
        sign = 1 if begin < finish else -1
        for point in crossed if sign > 0 else reversed(crossed):
            ray = ArcRayVisit(side, segment, point, sign)
            raw_rays[side].append(ray)
            events.append((2 * point, StrandVisit(
                owner, LabeledRayVisit(owner, ray))))
        events.append((finish, end if segment == len(arc.cuts)
                       else cut_visits[segment]))

        for (first_x, first), (second_x, second) in zip(events, events[1:]):
            gap = min(first_x, second_x) // 2
            if not 0 <= gap <= points:
                raise NormalTriangleError('itinerary event lies outside the marked row')
            connections.append(LocalTriangleConnection(
                owner, (side, gap), _triangle_side(side, gap, first_x), first,
                _triangle_side(side, gap, second_x), second))

    if any(tuple(raw_rays[side]) != reduced[side]
           for side in ('upper', 'lower')):
        raise NormalTriangleError(
            'ray reduction discards itinerary crossing IDs; '
            'local connections require an unreduced normal itinerary')
    return tuple(connections)
