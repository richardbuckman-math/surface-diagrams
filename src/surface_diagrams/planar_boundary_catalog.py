"""Combinatorial candidates for framed planar boundary-twist factorizations.

Each block is the set of *inner boundaries* enclosed by one positive twist.
We record unordered blocks and identify relabelings of the inner boundaries.
This is only an abelianized incidence catalog: it neither orders factors nor
chooses isotopy classes for their supporting curves.
"""

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations


def lines(n, large=()):
    """Complete every missing pair by its two-boundary block."""
    if type(n) is not int or not 1 <= n <= 10:
        raise ValueError('The catalog supports 1 through 10 inner boundaries')
    large = tuple(tuple(block) for block in large)
    covered = set()
    for block in large:
        if len(block) < 3 or tuple(sorted(set(block))) != block or any(
                type(point) is not int or not 1 <= point <= n for point in block):
            raise ValueError('Large blocks must be sorted distinct boundary numbers')
        for pair in combinations(block, 2):
            if pair in covered:
                raise ValueError('Two blocks enclose the same pair of boundaries')
            covered.add(pair)
    if len(set(large)) != len(large):
        raise ValueError('Duplicate large block')
    return tuple(sorted(large + tuple(pair for pair in combinations(range(1, n+1), 2)
                                    if pair not in covered), key=lambda b: (-len(b), b)))


def incidence(n, large=(), *, inner_power=0):
    """Check pair counts and solve for the required singleton twist exponents.

    For target T_outer times every inner boundary twist to inner_power,
    each pair occurs once and the signed incidence at each hole is
    1 + inner_power. Only the outer-power-one catalog is generated here.
    """
    if type(inner_power) is not int:
        raise ValueError('Inner boundary power must be an integer')
    blocks = lines(n, large)
    counts = Counter(point for block in blocks for point in block)
    pair_counts = Counter(pair for block in blocks for pair in combinations(block, 2))
    if any(pair_counts[pair] != 1 for pair in combinations(range(1, n+1), 2)):
        raise ValueError('Pair multiplicities do not match the target')
    singleton_powers = tuple(1 + inner_power - counts[point]
                             for point in range(1, n+1))
    assert all(counts[point] + singleton_powers[point-1] == 1 + inner_power
               for point in range(1, n+1))
    return blocks, singleton_powers


def pattern_sort_key(n, large):
    """Largest twist sizes first, comparing counts from size n down to 2."""
    counts = Counter(map(len, lines(n, large)))
    return tuple(-counts[size] for size in range(n, 1, -1)), tuple(large)


@lru_cache(maxsize=200000)
def _signature(n, large):
    blocks = lines(n, large)
    colors = tuple(tuple(sorted(Counter(len(block) for block in blocks
                                        if point in block).items()))
                   for point in range(1, n+1))
    # Two rounds of incidence-graph color refinement. This is an isomorphism
    # invariant, never an isomorphism verdict; the exact check remains below.
    for _ in range(2):
        block_colors = tuple((len(block), tuple(sorted(colors[point-1]
                                                   for point in block)))
                             for block in blocks)
        colors = tuple((colors[point-1], tuple(sorted(
            block_colors[index] for index, block in enumerate(blocks)
            if point in block))) for point in range(1, n+1))
    return tuple(sorted(map(len, blocks))), tuple(sorted(colors))


def _pair_line_ids(n, large):
    result = [[-1] * n for _ in range(n)]
    for index, block in enumerate(lines(n, large)):
        for a, b in combinations(block, 2):
            result[a-1][b-1] = result[b-1][a-1] = index
    return result


def _isomorphic(n, left, right):
    """Exact hypergraph isomorphism, with point signatures and collinearity pruning."""
    if _signature(n, left) != _signature(n, right):
        return False
    left_lines, right_lines = lines(n, left), lines(n, right)
    left_ids, right_ids = _pair_line_ids(n, left), _pair_line_ids(n, right)
    def point_profile(blocks, point):
        return tuple(sorted(Counter(len(block) for block in blocks if point in block).items()))
    lp = [point_profile(left_lines, i+1) for i in range(n)]
    rp = [point_profile(right_lines, i+1) for i in range(n)]
    options = [tuple(j for j in range(n) if lp[i] == rp[j]) for i in range(n)]
    order = sorted(range(n), key=lambda i: (len(options[i]), lp[i], i))
    assigned = {}
    used = set()

    def visit(depth):
        if depth == n:
            return True
        a = order[depth]
        for b in options[a]:
            if b in used:
                continue
            if any(len(left_lines[left_ids[a][old_a]]) !=
                   len(right_lines[right_ids[b][old_b]])
                   for old_a, old_b in assigned.items()):
                continue
            if any((left_ids[a][x] == left_ids[a][y]) !=
                   (right_ids[b][assigned[x]] == right_ids[b][assigned[y]])
                   for x, y in combinations(assigned, 2)):
                continue
            assigned[a] = b
            used.add(b)
            if visit(depth+1):
                return True
            used.remove(b)
            del assigned[a]
        return False

    return visit(0)


def _extensions(n, large):
    """Add one boundary through a disjoint family of existing lines."""
    old_lines = lines(n, large)
    choices = tuple(tuple(index for index, block in enumerate(old_lines)
                          if point in block) for point in range(1, n+1))
    full = (1 << n) - 1
    masks = tuple(sum(1 << (point-1) for point in block) for block in old_lines)
    selected = []

    def visit(done):
        if done == full:
            chosen = {old_lines[index] for index in selected}
            result = [block for block in large if block not in chosen]
            result.extend(tuple(sorted(block + (n+1,))) for block in chosen)
            yield tuple(sorted(result))
            return
        bit = (~done & full) & -(~done & full)
        point = bit.bit_length()
        yield from visit(done | bit)  # the new boundary makes only a pair here
        for index in choices[point-1]:
            if not masks[index] & done:
                selected.append(index)
                yield from visit(done | masks[index])
                selected.pop()

    yield from visit(0)


@lru_cache(maxsize=10)
def structural_types(n):
    """All pair-once block systems up to boundary relabeling and row order."""
    if type(n) is not int or not 1 <= n <= 10:
        raise ValueError('Choose 1 through 10 inner boundaries')
    if n <= 2:
        return ((),)
    buckets = defaultdict(list)
    for parent in structural_types(n-1):
        for candidate in _extensions(n-1, parent):
            key = _signature(n, candidate)
            if not any(_isomorphic(n, candidate, old) for old in buckets[key]):
                buckets[key].append(candidate)
    return tuple(sorted((candidate for group in buckets.values() for candidate in group),
                        key=lambda blocks: (len(blocks), blocks)))
