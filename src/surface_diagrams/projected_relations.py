"""Puncture-capped lantern consequences in an ordered disk braid chart.

These are relations in the marked *disk*, where a twist about one puncture is
trivial. They are not substitutions on a surface with framed inner boundaries.
Products use the same left-to-right factor order as ``exact_action``.
"""

from dataclasses import replace

from .braid_actions import inverse_word, reduce_word
from .mapping_classes import ConjugatedTwist


def pc_daisy_terms(twist):
    """Factor one n-point twist as an (n-1)-point twist and under-going petals.

    For n=4 the output is T123, T34, T24_under, T14_under. The final
    conjugator of T(i,n) moves point n under points i+1,...,n-1 in the
    project's vertically reflected planar display convention.
    """
    if not isinstance(twist, ConjugatedTwist) or twist.half or twist.power != 1 or twist.points < 3:
        raise ValueError('PC daisy needs one Dehn twist around at least three marked points')
    last = twist.first + twist.points - 1
    prefix = ConjugatedTwist(twist.conjugator, twist.first, twist.points - 1)
    petals = tuple(
        ConjugatedTwist(twist.conjugator + tuple(-j for j in range(last - 1, i, -1)), i, 2)
        for i in range(last - 1, twist.first - 1, -1)
    )
    return (prefix,) + petals


def pc_rose_terms(twist):
    """Recursively expand an n-point twist into pairwise twists.

    The three-point base uses the same PC lantern ordering already present in
    the boundary playground. Larger steps use ``pc_daisy_terms`` and retain
    their order, giving the pointed-cap rose factorization.
    """
    if not isinstance(twist, ConjugatedTwist) or twist.half or twist.power != 1 or twist.points < 2:
        raise ValueError('PC rose needs one Dehn twist around at least two marked points')
    if twist.points == 2:
        return (twist,)
    if twist.points == 3:
        i, g = twist.first, twist.conjugator
        return (ConjugatedTwist(g, i, 2),
                ConjugatedTwist(g + (i + 1,), i, 2),
                ConjugatedTwist(g, i + 1, 2))
    prefix, *petals = pc_daisy_terms(twist)
    return pc_rose_terms(prefix) + tuple(petals)


def pc_half_lantern_terms(twist):
    """Three-point PC lantern, two half twists, and one squared pair twist.

    This is the exact result of splitting T(i,i+1), moving its second half
    past the next pair twist, moving that twist past the half twist, then
    combining the equal pair twists. It transports through any conjugator.
    """
    if not isinstance(twist, ConjugatedTwist) or twist.half or twist.power != 1 or twist.points != 3:
        raise ValueError('PC half lantern needs one three-point Dehn twist')
    g, i = twist.conjugator, twist.first
    return (ConjugatedTwist(g, i, 2, half=True),
            ConjugatedTwist(g + (i + 1, i + 1), i, 2, half=True),
            ConjugatedTwist(g, i + 1, 2, power=2))



def pc_lantern_petal_cycle_terms(twist):
    """Return the positive two-petal relation realized by three Hurwitz swaps.

    Write the three-point PC lantern as L=R U Q. Put A=R^-1 Q R.
    Centrality gives A U=U Q=L R^-1. Three inverse Hurwitz swaps of
    (A,U) therefore give (R U R^-1, R Q R^-1). Every factor is a
    positive full twist; the inverse words only describe its support.
    The input/output order is essential, and any outer frame transports it.
    """
    if (not isinstance(twist, ConjugatedTwist) or twist.half
            or twist.power != 1 or twist.points != 3):
        raise ValueError('PC petal cycling needs one three-point Dehn twist')
    r, u, q = pc_rose_terms(twist)
    before = (replace(q, conjugator=reduce_word(inverse_word(r.word) + q.conjugator)), u)
    after = tuple(replace(term, conjugator=reduce_word(r.word + term.conjugator))
                  for term in (u, q))
    return before, after
