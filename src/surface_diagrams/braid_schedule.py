"""Optional compact placement of commuting crossings in a braid drawing.

This module changes only the picture.  The signed word remains the source of
truth; a layer may contain several generators only when they use disjoint
pairs of strands.  Such generators commute in the braid group.
"""

from dataclasses import dataclass

from .primitives import Path


@dataclass(frozen=True)
class CrossingLayer:
    """Simultaneous independent letters and their 1-based word positions."""

    letters: tuple[int, ...]
    positions: tuple[int, ...]


def commuting_layers(strands, word):
    """Place each crossing in its earliest safe layer under commutations.

    Relative order is retained for equal or neighboring generators.  Moving a
    letter past a disjoint generator is the only reordering permitted.  The
    returned positions allow the UI to recover the exact supplied word order.
    """
    if type(strands) is not int or strands < 1:
        raise ValueError('strands must be a positive integer')
    word = tuple(word)
    if any(type(letter) is not int or not 1 <= abs(letter) < strands
           for letter in word):
        raise ValueError('each crossing must be a nonzero signed index smaller than strands')

    # A crossing at i conflicts only with the most recent crossings at
    # i-1, i, and i+1.  Keeping their layer numbers makes this O(length).
    last = [-1] * (strands + 1)
    layers = []
    positions = []
    for position, letter in enumerate(word, start=1):
        index = abs(letter)
        level = 1 + max(last[index - 1:index + 2])
        if level == len(layers):
            layers.append([])
            positions.append([])
        layers[level].append(letter)
        positions[level].append(position)
        last[index] = level
    return tuple(CrossingLayer(tuple(letters), tuple(ids))
                 for letters, ids in zip(layers, positions))


def compact_layer_count(word):
    """Count simultaneous levels without needing a factor's ambient strand count."""
    word = tuple(word)
    strands = max((abs(letter) + 1 for letter in word), default=1)
    return len(commuting_layers(strands, word))


def aligned_compact_steps(factors, strands, row_height):
    """Center each compact braid block in its matching support-card row.

    The 18-unit minimum blank area at each end protects factor separators.
    Up to 28 units per crossing level makes sequential adjacent moves less
    steep when a row has room, while the supplied row heights remain aligned.
    """
    steps, ys, boundaries = [], [0.], []
    offset = 0
    for factor in factors:
        layers = commuting_layers(strands, factor.word)
        height = row_height(factor)
        if layers:
            step = min(28., (height - 36.) / len(layers))
            inset = (height - step * len(layers)) / 2
            steps.append(None)
            ys.append(-offset - inset)
            for index, layer in enumerate(layers, start=1):
                steps.append(layer.letters)
                ys.append(-offset - inset - index * step)
            offset += height
            steps.append(None)
            ys.append(-offset)
        else:
            offset += height
            steps.append(None)
            ys.append(-offset)
        boundaries.append(offset)
    return tuple(steps), tuple(ys), tuple(boundaries), offset


def layered_braid_paths(strands, steps, ys, spacing, colors, style,
                        crossing_style='smooth'):
    """Draw one interval per independent crossing layer or straight connector.

    ``steps`` contains tuples of signed letters, or ``None`` for a straight
    connector.  Each nonempty tuple must contain pairwise disjoint crossings.
    Mathematical y coordinates follow the existing ``_braid_paths`` API, so
    positive crossing handedness and strand colors are unchanged.
    """
    if type(strands) is not int or strands < 1:
        raise ValueError('strands must be a positive integer')
    if crossing_style not in ('straight', 'smooth'):
        raise ValueError('crossing_style must be straight or smooth')
    steps = tuple(steps)
    ys = tuple(ys)
    if len(ys) != len(steps) + 1:
        raise ValueError('one more y level than braid steps is required')
    if not colors:
        raise ValueError('at least one strand color is required')
    if spacing <= 0:
        raise ValueError('spacing must be positive')

    order = list(range(strands))
    xs = [(i - (strands - 1) / 2) * spacing for i in range(strands)]
    gap = min(.24, max(.10, style.curve_width * 1.6 / spacing))
    paths = []
    for step, y0, y1 in zip(steps, ys, ys[1:]):
        letters = () if step is None else tuple(step)
        if any(type(letter) is not int or not 1 <= abs(letter) < strands
               for letter in letters):
            raise ValueError('each crossing must be a nonzero signed index smaller than strands')
        if y0 == y1:
            raise ValueError('braid step has zero height')
        if style.curve_width * 4 >= min(spacing, abs(y1 - y0) if letters else spacing):
            raise ValueError('braid strokes are too wide; increase spacing/step or reduce curve_width')
        by_column = {}
        for letter in letters:
            left = abs(letter) - 1
            if left in by_column or left + 1 in by_column:
                raise ValueError('simultaneous crossings must use disjoint strands')
            by_column[left] = (letter, left)
            by_column[left + 1] = (letter, left)

        for pos, identity in enumerate(order):
            crossing = by_column.get(pos)
            dest = pos
            under = False
            if crossing is not None:
                letter, left = crossing
                dest = left + 1 if pos == left else left
                left_over = (letter > 0) == (y0 > y1)
                under = pos == (left + 1 if left_over else left)
            x0, x1 = xs[pos], xs[dest]

            def point(t):
                return x0 + (x1 - x0) * t, y0 + (y1 - y0) * t

            commands = [('M', x0, y0)]
            if crossing_style == 'smooth' and crossing is not None:
                # Match the existing easing and transparent underpass exactly.
                def curve(t):
                    return x0 + (x1 - x0) * (3 * t * t - 2 * t * t * t), y0 + (y1 - y0) * t

                def tangent(t):
                    return (x1 - x0) * 6 * t * (1 - t), y1 - y0

                intervals = ((0, .5 - gap), (.5 + gap, 1)) if under else ((0, 1),)
                for a, b in intervals:
                    p, q = curve(a), curve(b)
                    da, db = tangent(a), tangent(b)
                    scale = (b - a) / 3
                    if a:
                        commands.append(('M', *p))
                    commands.append(('C', p[0] + scale * da[0], p[1] + scale * da[1],
                                     q[0] - scale * db[0], q[1] - scale * db[1], *q))
            else:
                if under:
                    commands.extend((('L', *point(.5 - gap)), ('M', *point(.5 + gap))))
                commands.append(('L', x1, y1))
            paths.append(Path(tuple(commands), colors[identity % len(colors)],
                              style.curve_width, 'braid-strand'))
        for letter in letters:
            left = abs(letter) - 1
            order[left], order[left + 1] = order[left + 1], order[left]
    return tuple(paths), tuple(order)
