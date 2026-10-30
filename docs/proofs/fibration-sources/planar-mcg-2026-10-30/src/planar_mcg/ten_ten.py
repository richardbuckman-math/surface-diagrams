from __future__ import annotations

from functools import lru_cache
from typing import Union

from .constructors import artin_generator
from .context import ConsecutiveStrandEmbedding
from .curves import CutIntersectionLoop, PlanarArc
from .derivation import ExactFactorizationDerivation
from .factorization import Factorization
from .mapping_class import PlanarMappingClass
from .moves import concatenate_factorizations
from .surface import SurfaceSpec
from .twists import (
    ArcTwist,
    ConjugatedArcTwist,
    ConjugatedCutIntersectionArcTwist,
    ConjugatedDehnTwist,
    CutIntersectionArcTwist,
    DehnTwist,
)

TenTenDiagramCurve = Union[PlanarArc, CutIntersectionLoop]


def four_three_a_factorization() -> Factorization:
    """Return the user-supplied seven-factor ``A`` presentation of ``Delta_5^4``."""

    surface = SurfaceSpec(inner_boundaries=0, marked_points=5)
    factor_3_curve_action = PlanarMappingClass.from_artin_word(
        surface,
        (-2, 3, 4, 4, 3, 2),
    )
    return Factorization(
        surface,
        (
            DehnTwist(surface, (1, 2, 3), power=2),
            ConjugatedDehnTwist(
                surface,
                (3, 4, 5),
                conjugator=PlanarMappingClass.from_artin_word(surface, (2, 1)),
                power=2,
                label="A2",
            ),
            # The drawn arc is obtained by applying this word to the base arc.
            # Our algebraic conjugation convention stores x^c = c^-1 x c, so
            # c x c^-1 is represented by using c^-1 as the stored conjugator.
            ConjugatedArcTwist(
                surface,
                1,
                2,
                conjugator=factor_3_curve_action.inverse(),
                label="A3",
            ),
            DehnTwist(surface, (3, 4, 5), power=2),
            CutIntersectionArcTwist(
                surface,
                2,
                5,
                start_above=False,
            ),
            ConjugatedArcTwist(
                surface,
                1,
                2,
                conjugator=PlanarMappingClass.from_artin_word(
                    surface,
                    (2, 3, 3, -2),
                ),
                label="A6",
            ),
            CutIntersectionArcTwist(
                surface,
                1,
                5,
                cut_intersections=(3,),
                start_above=False,
            ),
        ),
    )


def four_three_b_factorization() -> Factorization:
    """Globally conjugate ``A`` by ``sigma_4``."""

    factorization = four_three_a_factorization()
    return factorization.global_conjugate(
        artin_generator(factorization.surface, 4)
    )


def four_three_c_factorization() -> Factorization:
    """Globally conjugate ``B`` by ``sigma_4``."""

    factorization = four_three_b_factorization()
    return factorization.global_conjugate(
        artin_generator(factorization.surface, 4)
    )


def tentenstart_factorization() -> Factorization:
    """Return the 21-factor starting stack ``B`` followed by ``A`` then ``C``."""

    return concatenate_factorizations(
        four_three_b_factorization(),
        four_three_a_factorization(),
        four_three_c_factorization(),
    )


def tentenone_derivation() -> ExactFactorizationDerivation:
    """Apply the three parallel central-block rotations to ``tentenstart``.

    The first, middle, and last seven-factor blocks are ``B``, ``A``, and
    ``C``. Each multiplies to the central element ``Delta_5^4``, so each may
    be cyclically rotated without changing the full product.
    """

    start = tentenstart_factorization()
    first_block = Factorization(
        start.surface,
        start.factors[:7],
    )
    middle_block = Factorization(
        start.surface,
        start.factors[7:14],
    )
    last_block = Factorization(
        start.surface,
        start.factors[14:21],
    )
    result = concatenate_factorizations(
        first_block.cyclic_shift_right(1),
        middle_block.cyclic_shift_left(3),
        last_block.cyclic_shift_left(2),
    )
    return ExactFactorizationDerivation(start).append(
        "rotate_three_central_blocks",
        result,
        parameters={
            "first_block_right_shift": 1,
            "middle_block_left_shift": 3,
            "last_block_left_shift": 2,
        },
    )


def tentenone_factorization() -> Factorization:
    """Return ``tentenstart`` after the three parallel block rotations."""

    return tentenone_derivation().current


def tententwo_derivation() -> ExactFactorizationDerivation:
    """Rotate the full central 21-factor product three places to the right."""

    derivation = tentenone_derivation()
    result = derivation.current.cyclic_shift_right(3)
    return derivation.append(
        "rotate_full_central_product",
        result,
        parameters={"right_shift": 3},
    )


def tententwo_factorization() -> Factorization:
    """Return ``tentenone`` after moving its last three factors to the front."""

    return tententwo_derivation().current


def tentenstart_diagram_curves() -> tuple[TenTenDiagramCurve, ...]:
    """Return the user-reviewed geometric start for the three-column preview.

    These curve corrections are kept separate from the exact factorization
    until the complete corrected word has been algebraically certified.
    """

    from .rendering import _factor_curve

    return tuple(
        _factor_curve(factor)[0]
        for factor in tentenstart_diagram_factorization().factors
    )


@lru_cache(maxsize=1)
def tentenstart_diagram_factorization() -> Factorization:
    """Return the structured factors underlying the reviewed start diagram."""

    start = tentenstart_factorization()
    factors = list(start.factors)

    sixth = PlanarArc(
        start.surface,
        1,
        2,
        cut_intersections=(5, 4),
        start_above=False,
    )
    factors[5] = sixth.half_twist()
    factors[12] = sixth.acted_on_by_generator(-4).half_twist()

    from .rendering import _factor_curve

    nineteenth, power = _factor_curve(factors[18])
    factors[18] = nineteenth.acted_on_by_generator(-1).half_twist(power)
    factors[19] = sixth.acted_on_by_generator(4).half_twist()
    return Factorization(start.surface, factors)


def tentenone_diagram_curves() -> tuple[TenTenDiagramCurve, ...]:
    """Apply the three reviewed seven-factor rotations to the diagram curves."""

    start = tentenstart_diagram_curves()
    return (
        start[6:7]
        + start[0:6]
        + start[10:14]
        + start[7:10]
        + start[16:21]
        + start[14:16]
    )


@lru_cache(maxsize=1)
def tentenone_diagram_factorization() -> Factorization:
    """Apply the reviewed block rotations to the structured diagram factors."""

    start = tentenstart_diagram_factorization()
    return Factorization(
        start.surface,
        start.factors[6:7]
        + start.factors[0:6]
        + start.factors[10:14]
        + start.factors[7:10]
        + start.factors[16:21]
        + start.factors[14:16],
    )


def tententwo_diagram_curves() -> tuple[TenTenDiagramCurve, ...]:
    """Move the last three ``tentenone`` curves to the front."""

    one = tentenone_diagram_curves()
    return one[-3:] + one[:-3]


@lru_cache(maxsize=1)
def tententwo_diagram_factorization() -> Factorization:
    """Apply the whole-word rotation to the structured diagram factors."""

    one = tentenone_diagram_factorization()
    return Factorization(one.surface, one.factors[-3:] + one.factors[:-3])


@lru_cache(maxsize=1)
def tententhree_factorization() -> Factorization:
    """Perform the two reviewed pulls starting from ``tententwo``."""

    result = tententwo_diagram_factorization()
    return (
        result.hurwitz_right(0)
        .hurwitz_right(1)
        .hurwitz_left(10)
        .hurwitz_left(9)
    )


@lru_cache(maxsize=1)
def tentenfour_factorization() -> Factorization:
    """Pull position 4 up to 3 and position 9 down to 10."""

    result = tententhree_factorization().hurwitz_left(2).hurwitz_right(8)
    factors = list(result.factors)
    sigma_four = ArcTwist(result.surface, 4, 5)
    if not factors[8].is_equivalent_to(sigma_four):
        raise AssertionError("step four factor 9 should represent sigma_4")
    factors[8] = sigma_four
    return Factorization(result.surface, factors)


@lru_cache(maxsize=1)
def tentenfive_factorization() -> Factorization:
    """Pull position 9 down to 16, then position 4 down to 15."""

    result = tentenfour_factorization()
    for index in range(8, 15):
        result = result.hurwitz_right(index)
    for index in range(3, 14):
        result = result.hurwitz_right(index)
    return result


@lru_cache(maxsize=1)
def tentenmerged_factorization() -> Factorization:
    """Merge the equal pairs in positions 15-16 and 17-18."""

    first_merge = tentenfive_factorization().combine_matching_arc_twists(14)
    return first_merge.combine_matching_arc_twists(15)


@lru_cache(maxsize=1)
def tentenembedded_factorization() -> Factorization:
    """Add a sixth marked point on the left of the merged factorization."""

    merged = tentenmerged_factorization()
    embedding = ConsecutiveStrandEmbedding(
        merged.surface,
        SurfaceSpec(inner_boundaries=0, marked_points=6),
        offset=1,
    )
    return embedding.map_factorization(merged)


@lru_cache(maxsize=1)
def tentenhalf_lantern_standard_left_factorization() -> Factorization:
    """Return the disjoint pair in the capped six-point half lantern."""

    surface = tentenembedded_factorization().surface
    return Factorization(
        surface,
        (
            DehnTwist(surface, (5, 6)),
            DehnTwist(surface, (1, 2)),
        ),
    )


@lru_cache(maxsize=1)
def tentenhalf_lantern_conversion_mapping_class() -> PlanarMappingClass:
    """Return the reviewed word carrying the merged pair to standard position."""

    surface = tentenembedded_factorization().surface
    return PlanarMappingClass.from_artin_word(
        surface,
        (-3, 4, 5, 5, 4, 3, 1, 2),
    )


@lru_cache(maxsize=1)
def tentenhalf_lantern_standard_right_factorization() -> Factorization:
    """Return the sphere-moved three-factor side of the half lantern."""

    surface = tentenembedded_factorization().surface
    return Factorization(
        surface,
        (
            DehnTwist(surface, (4, 5, 6), power=2),
            CutIntersectionArcTwist(
                surface,
                3,
                4,
                cut_intersections=(6,),
                start_above=False,
            ),
            ArcTwist(surface, 3, 4),
        ),
    )


@lru_cache(maxsize=1)
def tentenhalf_lantern_factorization() -> Factorization:
    """Apply the transported half-lantern substitution to positions 15-16.

    The reviewed word

    ``sigma_3^-1 sigma_4 sigma_5^2 sigma_4 sigma_3 sigma_1 sigma_2``

    carries the merged pair exactly to ``t_(56) t_(12)``. On the sphere this
    is the capped half-lantern input. After a sphere move, replace it by the
    triple represented by ``(curve 3 6)^2``,
    ``(arc start 3 down 6 stop 4)``, and ``(arc start 3 stop 4)``, then undo
    the reviewed conversion to obtain the final three factors.
    """

    embedded = tentenembedded_factorization()
    source = Factorization(embedded.surface, embedded.factors[14:16])
    conversion = tentenhalf_lantern_conversion_mapping_class()
    standard_left = tentenhalf_lantern_standard_left_factorization()
    converted_source = source.global_conjugate(conversion)
    if not all(
        converted.is_equivalent_to(standard)
        for converted, standard in zip(
            converted_source.factors,
            standard_left.factors,
        )
    ):
        raise AssertionError("reviewed word does not produce the standard pair")

    transported = tentenhalf_lantern_standard_right_factorization().global_conjugate(
        conversion.inverse()
    )
    explicit_alpha = CutIntersectionArcTwist(
        embedded.surface,
        1,
        4,
        cut_intersections=(3, 4, 6, 2, 3, 6),
        start_above=False,
    )
    explicit_beta = CutIntersectionArcTwist(
        embedded.surface,
        1,
        4,
        cut_intersections=(),
        start_above=False,
    )
    if not explicit_alpha.is_equivalent_to(transported.factors[1]):
        raise AssertionError("explicit transported alpha route is not exact")
    if not explicit_beta.is_equivalent_to(transported.factors[2]):
        raise AssertionError("explicit transported beta route is not exact")
    replacement = (
        transported.factors[0],
        explicit_alpha,
        explicit_beta,
    )
    return Factorization(
        embedded.surface,
        embedded.factors[:14]
        + replacement
        + embedded.factors[16:],
    )


def tentenhalf_lantern_preview_factorization() -> Factorization:
    """Compatibility alias for the checked half-lantern factorization."""

    return tentenhalf_lantern_factorization()


def tentenstart() -> Factorization:
    """Short alias for :func:`tentenstart_factorization`."""

    return tentenstart_factorization()


def tentenone() -> Factorization:
    """Short alias for :func:`tentenone_factorization`."""

    return tentenone_factorization()


def tententwo() -> Factorization:
    """Short alias for :func:`tententwo_factorization`."""

    return tententwo_factorization()
