"""Exact real-line certificates for some positive planar twist relations.

Hironaka's line-arrangement theorem turns a real arrangement with distinct
slopes and projection-critical values into a positive factorization of an
exterior twist with boundary corrections. Finding such an arrangement is a
*sufficient* certificate, not a decision procedure for arbitrary patterns.
"""

from fractions import Fraction
from itertools import combinations
from random import Random

from .planar_boundary_catalog import lines


def _nullspace(rows, n):
    matrix = [[Fraction(value) for value in row] for row in rows]
    pivots = []
    for column in range(n):
        pivot = next((r for r in range(len(pivots), len(matrix))
                      if matrix[r][column]), None)
        if pivot is None:
            continue
        matrix[len(pivots)], matrix[pivot] = matrix[pivot], matrix[len(pivots)]
        row = matrix[len(pivots)]
        divisor = row[column]
        matrix[len(pivots)] = [value / divisor for value in row]
        row = matrix[len(pivots)]
        for other in range(len(matrix)):
            if other != len(pivots) and matrix[other][column]:
                factor = matrix[other][column]
                matrix[other] = [a-factor*b for a, b in zip(matrix[other], row)]
        pivots.append(column)
    free = [column for column in range(n) if column not in pivots]
    basis = []
    for column in free:
        vector = [Fraction(0) for _ in range(n)]
        vector[column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -matrix[row][column]
        basis.append(tuple(vector))
    return tuple(basis)


def _constraints(n, large, slopes):
    equations = []
    for block in large:
        a, b = block[:2]
        for c in block[2:]:
            row = [0] * n
            row[a-1] = slopes[c-1] - slopes[b-1]
            row[b-1] = slopes[a-1] - slopes[c-1]
            row[c-1] = slopes[b-1] - slopes[a-1]
            equations.append(row)
    return equations


def arrangement_intersections(slopes, intercepts):
    """Return exact intersection blocks in increasing projection order.

    Reject vertical coincidences in the projection and extra concurrencies;
    such arrangements can often be perturbed, but the certificate must be
    directly usable without an implicit perturbation argument.
    """
    n = len(slopes)
    if len(intercepts) != n or len(set(slopes)) != n:
        raise ValueError('Need one line per boundary and distinct slopes')
    points = {}
    x_values = {}
    for i, j in combinations(range(n), 2):
        x = Fraction(intercepts[j] - intercepts[i], slopes[i] - slopes[j])
        y = slopes[i] * x + intercepts[i]
        point = (x, y)
        points.setdefault(point, set()).update((i+1, j+1))
        if x in x_values and x_values[x] != y:
            return None
        x_values[x] = y
    result = []
    for (x, y), members in sorted(points.items()):
        block = tuple(sorted(members))
        result.append((x, y, block))
    return tuple(result)


def _quadrilateral_arrangement(n, large, rng):
    """Realize the six-line, four-triple complete quadrilateral if requested."""
    if n != 6 or len(large) != 4 or any(len(block) != 3 for block in large):
        return None
    incidences = [tuple(k for k, block in enumerate(large) if point in block)
                  for point in range(1, 7)]
    if sorted(incidences) != list(combinations(range(4), 2)):
        return None
    target = lines(n, large)
    for _ in range(2000):
        vertices = tuple((rng.randint(-20, 20), rng.randint(-20, 20)) for _ in range(4))
        if len(set(vertices)) != 4:
            continue
        slopes = []
        intercepts = []
        for a, b in incidences:
            x1, y1 = vertices[a]
            x2, y2 = vertices[b]
            if x1 == x2:
                break
            slope = Fraction(y2-y1, x2-x1)
            slopes.append(slope)
            intercepts.append(y1-slope*x1)
        if len(slopes) != n or len(set(slopes)) != n:
            continue
        intersections = arrangement_intersections(slopes, intercepts)
        if intersections is not None and tuple(sorted((block for _, _, block in intersections),
                                                        key=lambda b: (-len(b), b))) == target:
            return {'slopes': tuple(slopes), 'intercepts': tuple(intercepts),
                    'intersections': intersections}
    return None


def find_real_line_arrangement(n, large, *, slope_tries=32, offset_tries=32):
    """Search reproducibly for an integer/rational arrangement certificate.

    Returns line slopes/intercepts and ordered intersection blocks, or None.
    None means only that this bounded search found no certificate.
    """
    target = lines(n, large)
    seed = sum(sum((i+1)*point for i, point in enumerate(block)) * (k+1)
               for k, block in enumerate(target)) + 7919*n
    rng = Random(seed)
    for attempt in range(slope_tries):
        slopes = tuple(range(n)) if attempt == 0 else tuple(rng.sample(range(-50, 51), n))
        basis = _nullspace(_constraints(n, large, slopes), n)
        for _ in range(offset_tries):
            weights = [rng.randint(-6, 6) for _ in basis]
            intercepts = tuple(sum(weight*vector[i] for weight, vector in zip(weights, basis))
                               for i in range(n))
            intersections = arrangement_intersections(slopes, intercepts)
            if intersections is None:
                continue
            blocks = tuple(sorted((block for _, _, block in intersections),
                                  key=lambda b: (-len(b), b)))
            if blocks == target:
                return {'slopes': slopes, 'intercepts': intercepts,
                        'intersections': intersections}
    return _quadrilateral_arrangement(n, large, rng)
