"""Source records for proposed genus-two factorization labs.

Only Xiao's (4,3) relation has disk-braid factors here. The other entries
record literature leads, not executable factorizations. A paper's braid for a
3+3 degeneration need not itself lift to the positive separating Dehn twist;
``raw_disk_words`` and ``factors`` deliberately retain that distinction.
"""

from dataclasses import dataclass

from .factorization_explorer import Factor


@dataclass(frozen=True)
class FibrationLabSeed:
    slug: str
    title: str
    status: str
    source_urls: tuple[str, ...]
    source_note: str
    section_note: str
    factors: tuple[Factor, ...] = ()
    raw_disk_words: tuple[tuple[int, ...], ...] = ()
    involution_corrections: tuple[int, ...] = ()


# Akhmedov, arXiv:2609.17634, Section 8 and Appendix B. The Artin-chain lift
# of this braid is the hyperelliptic involution on the closed genus-two fiber.
HYPERELLIPTIC_INVOLUTION_BRAID = (1, 2, 3, 4, 5, 5, 4, 3, 2, 1)

_BD = (-5, -4, -3, 1, -5, -2, -3)
_BR = (5, 4, 3, 2, 1, -4, -5, -2, -1, -2, -4)
_BU = (5, 4, -1, 5, -4, -3)
_BL = (2, 1, 2, 5, 4, 5)
_K1 = (5, 4, 3, 2, 1)
_K_INFINITY = (
    5, 4, 5, -1, -4, -3, -2, -5, -4, -3, -5, -4, -5,
    -3, -4, -5, -2, -3, -4,
)


XIAO_FOUR_THREE = FibrationLabSeed(
    slug='4-3',
    title="Xiao's (4,3) genus-two factorization",
    status='source-backed closed genus-two identity; exact checks in tests',
    source_urls=(
        'https://arxiv.org/pdf/2609.17634',
        'https://arxiv.org/pdf/2602.20451',
    ),
    source_note=(
        'Akhmedov Section 8 and Appendices B.1-B.2 give the ordered Artin '
        'words D, 1, R, U, infinity, L, 0. The printed words at 1 and 0 '
        'lift to the involution times a separating twist; equations (18)-(20) '
        'correct them. The Factor records use the equivalent positive '
        'three-point twist squared. This equivalence is upstairs in the '
        'closed genus-two mapping class group, not equality of disk braids. '
        'The source obtains the words from numerical branch continuation '
        'and checks the resulting algebraic braid identities exactly.'
    ),
    section_note=(
        'Huang, Remark 4.1, gives a three-boundary lift, hence three '
        'disjoint sections of square -1 for the equivalent Baykur-Korkmaz, '
        'Hamada, and Xiao (4,3) fibrations.'
    ),
    factors=(
        Factor('D', _BD, 4, 2, half=True),
        Factor('1', _K1, 1, 3, power=2),
        Factor('R', _BR, 3, 2, half=True),
        Factor('U', _BU, 2, 2, half=True),
        Factor('infinity', _K_INFINITY, 2, 3, power=2),
        Factor('L', _BL, 3, 2, half=True),
        Factor('0', (), 1, 3, power=2),
    ),
    raw_disk_words=(
        (-5, -4, -3, 1, -5, -2, -3, 4, 3, 2, 5, -1, 3, 4, 5),
        (5, 4, 3, 2, 1, 2, 1, 2, 4, 5, 4, 2, 1, 2, 4, 5, 4, -1, -2, -3, -4, -5),
        (5, 4, 3, 2, 1, -4, -5, -2, -1, -2, -4, 3, 4, 2, 1, 2, 5, 4, -1, -2, -3, -4, -5),
        (5, 4, -1, 5, -4, -3, 2, 3, 4, -5, 1, -4, -5),
        (5, 4, 5, -1, -4, -3, -2, -5, -4, -3, -5, -4, -5, -3, -4, -5, -2, -3, -4,
         3, 2, 3, 3, 2, -1, 3, -2, -3, 2, 1, 2, 3, 2, 1, 3, 2, 3, 4, 3, 2,
         5, 4, 3, 5, 4, 5, 3, 4, 5, 2, 3, 4, 1, -5, -4, -5),
        (2, 1, 2, 5, 4, 5, 3, -5, -4, -5, -2, -1, -2),
        (2, 1, 2, 5, 4, 5, 2, 1, 2, 5, 4, 5),
    ),
    involution_corrections=(1, 6),
)


MATSUMOTO_SIX_TWO = FibrationLabSeed(
    slug='6-2',
    title="Matsumoto's (6,2) genus-two factorization",
    status='literature relation; disk-braid encoding pending',
    source_urls=(
        'https://arxiv.org/pdf/1510.00089',
        'https://arxiv.org/pdf/1610.08458',
    ),
    source_note=(
        'Baykur-Korkmaz Section 3.3 states '
        '(t_B0 t_B1 t_B2 t_c)^2 = t_delta in Mod(Sigma_2^1). '
        'The curve diagram has not been encoded here as exact six-strand factors.'
    ),
    section_note=(
        'The one-boundary relation gives a section of square -1. Hamada, '
        'Theorem 2, gives four disjoint sections of square -1 for genus two.'
    ),
)


NAKAMURA_TEN_TEN = FibrationLabSeed(
    slug='10-10',
    title="Nakamura's (10,10) genus-two factorization",
    status='literature relation; disk-braid encoding pending',
    source_urls=('https://arxiv.org/pdf/1811.03708',),
    source_note=(
        'Nakamura Section 3 obtains a 20-factor closed-surface relation '
        'from three (4,3) copies and a lantern substitution. Its explicit '
        'curve factors have not been encoded or verified as disk braids here.'
    ),
    section_note=(
        'No section is certified by this seed. Nakamura proves the total '
        'space minimal, excluding sections of square -1.'
    ),
)


SEEDS = (XIAO_FOUR_THREE, MATSUMOTO_SIX_TWO, NAKAMURA_TEN_TEN)


def seed_for(slug: str) -> FibrationLabSeed:
    for seed in SEEDS:
        if seed.slug == slug:
            return seed
    raise KeyError(slug)
