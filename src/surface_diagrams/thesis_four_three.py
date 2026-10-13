"""Checked first five-point stage of Buckman's Baykur--Korkmaz (4,3) proof.

Figure 4.5 has four drawn rows. Its top row contains two disjoint twists;
the green T45 factor is negative squared. The thesis applies rows top to
bottom, so the corresponding algebraic braid product is written bottom to
top in this package's right-composition convention. This module covers the
three Figure 4.5 columns, the Figure 4.6 chart braid, and one checked
ordering of the two Figure 4.7 PC half-lantern substitutions. It does not
transcribe the later Hurwitz arrows.
"""

from dataclasses import dataclass

from .braid_actions import inverse_word, reduce_word
from .mapping_classes import ConjugatedTwist, exact_action
from .marked_disk_chain import marked_disk_chain
from .normal_cut_engine import calculate_cut_system
from .projected_relations import pc_half_lantern_terms


@dataclass(frozen=True)
class ThesisFactor:
    name: str
    twist: ConjugatedTwist
    exponent: int = 1

    @property
    def word(self):
        if self.exponent == 0:
            raise ValueError('A zero-power thesis factor is not a twist')
        unit = self.twist.word
        return (unit * self.exponent if self.exponent > 0 else
                inverse_word(unit) * -self.exponent)


T123 = ThesisFactor('T123', ConjugatedTwist((), 1, 3))
T45_INVERSE_SQUARE = ThesisFactor('T45^-2', ConjugatedTwist((), 4, 2), -2)
T345 = ThesisFactor('T345', ConjugatedTwist((), 3, 3))
T245_UNDER = ThesisFactor('T245 under 3', ConjugatedTwist((-2,), 3, 3))
T145_UNDER = ThesisFactor('T145 under 2,3', ConjugatedTwist((-1, -2), 3, 3))

# Rows as seen from top to bottom in Figure 4.5. The two first-row curves
# are disjoint and commute. Conjugators -2 and (-1,-2) take the outer
# three-point support under the intervening marked points.
FIRST_ROWS = ((T123, T45_INVERSE_SQUARE),
              (T345,), (T245_UNDER,), (T145_UNDER,))
CYCLIC_ROWS = FIRST_ROWS[1:] + FIRST_ROWS[:1]
# Figure 4.6 drags the first and third marked points around the second.
# In the reflected display convention, this is the three-strand half-turn.
CHART_BRAID = (1, 2, 1)


def _chart_factor(factor, name):
    twist = factor.twist
    return ThesisFactor(name, ConjugatedTwist(
        reduce_word(CHART_BRAID + twist.conjugator),
        twist.first, twist.points, twist.power, twist.half), factor.exponent)


REARRANGED_ROWS = (
    (T123, T45_INVERSE_SQUARE),
    (_chart_factor(T345, 'β(T345) · points 1,4,5'),),
    (_chart_factor(T245_UNDER, 'β(T245) · points 2,4,5'),),
    (T345,),
)
OUTER_WORD = ConjugatedTwist((), 1, 5).word

# The first Figure 4.7 column concatenates Figure 4.5's third and second
# columns. Rotate its last row to the top, then combine the two commuting
# copies of T123 and T45^-2. The middle state records the actual cyclic move
# instead of presenting a product equality as an unexplained arrow.
CONCATENATED_ROWS = REARRANGED_ROWS + CYCLIC_ROWS
ROTATED_ROWS = (CONCATENATED_ROWS[-1],) + CONCATENATED_ROWS[:-1]
SQUARED_ROWS = (
    (ThesisFactor('T123^2', T123.twist, 2),
     ThesisFactor('T45^-4', T45_INVERSE_SQUARE.twist, -4)),
) + ROTATED_ROWS[2:]

# The negative T45 twist commutes with every other support in this state.
# Split its fourth inverse power into two inverse squares and place one
# immediately below each under-going three-point twist. This is a checked
# alternative ordering for applying the two puncture-capped half lanterns.
PAIRABLE_ROWS = (
    (SQUARED_ROWS[0][0],),
    SQUARED_ROWS[1], SQUARED_ROWS[2],
    (ThesisFactor('T345^2', T345.twist, 2),),
    (T245_UNDER,), (T45_INVERSE_SQUARE,),
    (T145_UNDER,), (T45_INVERSE_SQUARE,),
)


def _half_lantern_rows(factor, label):
    first, second, correction = pc_half_lantern_terms(factor.twist)
    if exact_action(correction.word, 5) != exact_action(
            ConjugatedTwist((), 4, 2, power=2).word, 5):
        raise ValueError('Half-lantern correction is not T45 squared')
    # Algebraic H_first H_second acts top-first as H_second, then H_first.
    return ((ThesisFactor(f'{label} second half', second),),
            (ThesisFactor(f'{label} first half', first),))


HALF_LANTERN_ROWS = (PAIRABLE_ROWS[:4]
                     + _half_lantern_rows(T245_UNDER, '245')
                     + _half_lantern_rows(T145_UNDER, '145'))


def chronological_word(rows, count=None):
    """Product of rows applied from the top, reversing algebraic order."""
    selected = rows if count is None else rows[:count]
    return tuple(letter for row in reversed(selected)
                 for factor in row for letter in factor.word)


def check_stage(rows, *, outer_power=1):
    """Check the complete disk action and certify each five-arc prefix."""
    if type(outer_power) is not int or outer_power < 1:
        raise ValueError('Exterior boundary power must be positive')
    if exact_action(chronological_word(rows), 5) != exact_action(OUTER_WORD * outer_power, 5):
        raise ValueError('Thesis column does not equal its exterior boundary twist target')
    certificates = []
    for count in range(len(rows) + 1):
        images = exact_action(chronological_word(rows, count), 5)
        certificates.append(calculate_cut_system(marked_disk_chain(images), points=5))
    return tuple(certificates)
