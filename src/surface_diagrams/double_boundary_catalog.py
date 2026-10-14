"""Small exact incidence catalog for a double exterior-boundary twist.

This counts *candidate* unordered positive twist supports. A necessary
condition for T_outer^2 is that every pair of inner boundaries occurs in
exactly two supports. It is not a mapping-class equality certificate.
"""

from collections import Counter
from itertools import combinations, permutations


def canonical_blocks(n, blocks):
    """Identify row order and simultaneous relabeling of inner boundaries."""
    rows = tuple(tuple(sorted(block)) for block in blocks)
    if any(len(row) < 2 or len(row) != len(set(row)) or
           any(point not in range(1, n + 1) for point in row)
           for row in rows):
        raise ValueError('Each support must contain distinct valid boundaries')
    return min(
        tuple(sorted((tuple(sorted(relabel[point - 1] for point in row))
                      for row in rows), key=lambda row: (-len(row), row)))
        for relabel in permutations(range(1, n + 1))
    )


def double_outer_types(n):
    """All pair-multiplicity-two types for up to five inner boundaries.

    Enumerate copies of supports of size at least three, then fill every
    remaining pair with the required number (zero, one, or two) of pair
    twists. This avoids searching pair rows explicitly.
    """
    if type(n) is not int or not 2 <= n <= 5:
        raise ValueError('Exact double catalog currently supports n=2..5')
    pairs = tuple(combinations(range(1, n + 1), 2))
    large = tuple(block for size in range(n, 2, -1)
                  for block in combinations(range(1, n + 1), size))
    capacities = {pair: 2 for pair in pairs}
    selected = []
    types = set()

    def visit(index):
        if index == len(large):
            rows = selected + [pair for pair in pairs
                               for _ in range(capacities[pair])]
            types.add(canonical_blocks(n, rows))
            return
        block = large[index]
        contained = tuple(combinations(block, 2))
        maximum = min(capacities[pair] for pair in contained)
        for count in range(maximum + 1):
            for pair in contained:
                capacities[pair] -= count
            selected.extend([block] * count)
            visit(index + 1)
            del selected[len(selected) - count:]
            for pair in contained:
                capacities[pair] += count

    visit(0)
    def key(rows):
        counts = Counter(map(len, rows))
        return tuple(-counts[size] for size in range(n, 1, -1)), rows
    return tuple(sorted(types, key=key))


def inner_boundary_powers(n, blocks):
    """Nonnegative corrections on the T_outer^2 side of a candidate."""
    if any(sum(pair[0] in block and pair[1] in block for block in blocks) != 2
           for pair in combinations(range(1, n + 1), 2)):
        raise ValueError('Every pair must occur exactly twice')
    powers = tuple(sum(point in block for block in blocks) - 2
                   for point in range(1, n + 1))
    if any(power < 0 for power in powers):
        raise ValueError('Negative inner-boundary correction')
    return powers
