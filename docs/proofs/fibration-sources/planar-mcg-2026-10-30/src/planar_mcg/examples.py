from __future__ import annotations

from itertools import combinations
from typing import Iterable, Tuple

from .boundary_patterns import BoundaryTwistPattern
from .constructors import outer_boundary_twist, subset_full_twist
from .factorization import Factorization
from .mapping_class import PlanarMappingClass
from .moves import conjugate_factor_preserving_structure
from .surface import SurfaceSpec
from .twists import ArcTwist, DehnTwist


def _normalized_subset(strands: Iterable[int]) -> Tuple[int, ...]:
    subset = tuple(sorted(dict.fromkeys(int(value) for value in strands)))
    if len(subset) < 2:
        raise ValueError("a subset relation needs at least two strands")
    return subset


def pairwise_subset_factorization(
    surface: SurfaceSpec, strands: Iterable[int]
) -> Factorization:
    """Full twist on a subset as the product of its pairwise full twists.

    On three strands this is the standard rose-style relation.
    """

    subset = _normalized_subset(strands)
    factors = [subset_full_twist(surface, pair) for pair in combinations(subset, 2)]
    return Factorization(surface, factors)


def daisy_subset_factorization(
    surface: SurfaceSpec, strands: Iterable[int]
) -> Factorization:
    """Full twist on a subset via one smaller twist plus pairwise petals."""

    subset = _normalized_subset(strands)
    if len(subset) < 3:
        raise ValueError("the daisy relation needs at least three strands")
    last = subset[-1]
    factors = [subset_full_twist(surface, subset[:-1])]
    factors.extend(subset_full_twist(surface, [strand, last]) for strand in subset[:-1])
    return Factorization(surface, factors)


def pairwise_outer_twist_factorization(surface: SurfaceSpec) -> Factorization:
    """Outer twist as the product of all pairwise subset twists.

    This is the standard pure-braid factorization
    `Delta_n^2 = product_{i<j} A_{i,j}` written in increasing lexicographic
    order on pairs.
    """

    return pairwise_subset_factorization(surface, range(1, surface.total_strands + 1))


def daisy_outer_twist_factorization(surface: SurfaceSpec) -> Factorization:
    """A recursive daisy-style factorization of the outer twist.

    For `n >= 3` this returns

    `Delta_n^2 = Delta_{n-1}^2 * A_{1,n} * A_{2,n} * ... * A_{n-1,n}`.
    """

    if surface.total_strands < 3:
        raise ValueError("the daisy factorization needs at least three strands")
    return daisy_subset_factorization(surface, range(1, surface.total_strands + 1))


def six_strand_two_six_factorization() -> Factorization:
    """Factor ``Delta_6^2`` into two triple twists and six half twists.

    In thesis-counting notation, the first two factors are copies of
    ``Delta_3^4`` and the remaining factors are conjugated half twists.
    """

    surface = SurfaceSpec(inner_boundaries=0, marked_points=6)
    diagonal_arcs = ((1, 4), (2, 5), (3, 6))
    factors = [
        DehnTwist(surface, (1, 2, 3), power=2),
        DehnTwist(surface, (4, 5, 6), power=2),
    ]
    factors.extend(
        ArcTwist(surface, start, end)
        for _ in range(2)
        for start, end in diagonal_arcs
    )
    return Factorization(surface, factors)


def six_boundary_three_triple_factorization() -> Factorization:
    """A searched exact ordering for a six-boundary linear pattern.

    The unordered large blocks are ``124``, ``135``, and ``236``. The
    remaining boundary pairs occur as pair twists, and central boundary twists
    supply the split-form correction.
    """

    pattern = BoundaryTwistPattern(
        6,
        [
            (1, 2, 4),
            (1, 3, 5),
            (2, 3, 6),
        ],
    )
    return pattern.factorization_with_support_order(
        (
            (1, 2, 4),
            (3, 4),
            (1, 3, 5),
            (1, 6),
            (2, 3, 6),
            (4, 6),
            (5, 6),
            (2, 5),
            (4, 5),
        )
    )


def six_strand_six_seven_shadow_candidate() -> Factorization:
    """Return a concrete `6,7` candidate passing all abelian-shadow tests.

    This is not yet an exact factorization of ``Delta_6^6``. Its seven squared
    triple twists and six noncanonical half twists have exactly the target
    permutation, exponent sum, and pairwise labeled crossing numbers.
    """

    surface = SurfaceSpec(inner_boundaries=0, marked_points=6)
    triple_supports = (
        (1, 2, 3),
        (1, 4, 5),
        (1, 4, 6),
        (2, 3, 4),
        (2, 4, 6),
        (2, 5, 6),
        (3, 5, 6),
    )
    arc_conjugator_words = (
        (2, 1, -3, -4),
        (2, 3, -1, 2),
        (2, 1, 3, 4),
        (2, -3, -4, 5),
        (-2, 1, -3, -2),
        (-2, -3, -4, -5),
    )
    factors = [
        DehnTwist(surface, support, power=2)
        for support in triple_supports
    ]
    seed_arc = ArcTwist(surface, 1, 2)
    factors.extend(
        conjugate_factor_preserving_structure(
            seed_arc,
            PlanarMappingClass.from_artin_word(surface, word),
        )
        for word in arc_conjugator_words
    )
    return Factorization(surface, factors)


def three_block_dehn_twist(surface: SurfaceSpec, start: int, power: int = 2):
    """The `Delta_3^(2*power)`-style twist on three consecutive strands."""

    return subset_full_twist(surface, [start, start + 1, start + 2], power=power)


def standard_examples_for_n(n_strands: int) -> dict:
    surface = SurfaceSpec(inner_boundaries=0, marked_points=n_strands)
    return {
        "outer_boundary_twist": outer_boundary_twist(surface),
        "pairwise_outer_factorization": pairwise_outer_twist_factorization(surface),
        "daisy_outer_factorization": daisy_outer_twist_factorization(surface)
        if n_strands >= 3
        else None,
    }
