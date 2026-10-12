"""Presentation-only endpoint shaping for a horizontal chain of planar arcs.

The Arc itineraries and the shared route solver remain the source of truth.
This changes SVG path controls after routing so consecutive chain edges meet
each marked point from opposite sides. A disk's first edge can also leave the
leftmost boundary point along the oval's inward normal.
"""

from dataclasses import dataclass, replace
from typing import Optional

from .visuals import PlanarDiagram


def shape_chain_arc(commands, *, outer_start=False):
    if len(commands) < 2:
        return commands
    start = commands[0][1:]
    if len(commands) == 2 and commands[1][0] == 'L':
        end = commands[1][1:]
        if end[0] > start[0]:
            return commands
        handle = min(18., abs(end[0] - start[0]) / 4)
        rise = min(12., abs(end[0] - start[0]) / 6)
        return (commands[0],
                ('C', start[0] + handle, 0., start[0] + handle, rise,
                 start[0], rise),
                ('L', end[0], rise),
                ('C', end[0] - handle, rise, end[0] - handle, 0., *end))
    shaped = [commands[0]]
    current = start
    last = len(commands) - 1
    kappa = 0.5522847498307936
    for index, command in enumerate(commands[1:], 1):
        if command[0] != 'A' or index not in (1, last):
            shaped.append(command)
            current = command[-2:]
            continue
        _, rx, ry, _, _, sweep, end_x, end_y = command
        direction = 1 if end_x > current[0] else -1
        upper = (direction < 0) == bool(sweep)
        sign = 1 if upper else -1
        mid_x = (current[0] + end_x) / 2
        top_y = sign * ry
        handle = min(30., abs(end_x - current[0]) / 3)
        if index == 1 and outer_start:
            stem = (current[0] + min(12., handle / 2), current[1])
            shaped.append(('L', *stem))
            first_control = (stem[0] + handle / 2, stem[1])
        elif index == 1:
            first_control = (current[0] + handle, current[1])
        else:
            first_control = (current[0], sign * kappa * ry)
        last_control = ((end_x - handle, end_y) if index == last
                        else (end_x, sign * kappa * ry))
        shaped.append(('C', *first_control,
                       mid_x - direction * kappa * rx, top_y,
                       mid_x, top_y))
        shaped.append(('C', mid_x + direction * kappa * rx, top_y,
                       *last_control, end_x, end_y))
        current = (end_x, end_y)
    return tuple(shaped)


@dataclass(frozen=True)
class ChainDiagram(PlanarDiagram):
    """Render routed chain arcs with readable boundary and puncture tangents."""

    rim_index: Optional[int] = None

    def drawing(self, style):
        drawing = super().drawing(style)
        arc_index = 0
        paths = []
        for path in drawing.paths:
            if path.role == 'arc':
                paths.append(replace(path, commands=shape_chain_arc(
                    path.commands, outer_start=arc_index == self.rim_index)))
                arc_index += 1
            else:
                paths.append(path)
        return replace(drawing, paths=tuple(paths))
