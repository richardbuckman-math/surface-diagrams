"""Change the starting point in an ordered circular factorization.

If P = A B, reading B then A gives A^-1 P A. This is always an explicit
global change of basepoint; equality with P additionally requires A to
commute with P. No disk centrality or sphere relation is assumed here.
"""
from .braid_actions import inverse_word, reduce_word


def rotate_factors(factors, offset):
    """Move a top block down (positive) or a bottom block up (negative).

    Factors, supports, and powers are unchanged. The short telescoping
    certificate works without expanding a potentially huge Artin action.
    The caller can check its cumulative global frame independently.
    """
    factors = tuple(factors)
    n = len(factors)
    if type(offset) is not int or not 0 < abs(offset) < n:
        raise ValueError('Choose between 1 and one less than the factor count')
    cut = offset % n
    top, bottom = factors[:cut], factors[cut:]
    after = bottom + top
    block = top if offset > 0 else bottom
    # Both A^-1 and B conjugate A B to B A. Retain the shorter word so a
    # rotation of almost all factors does not need an almost-full-product frame.
    candidates = (
        ('inverse_prefix',inverse_word(tuple(x for f in top for x in f.word))),
        ('suffix',reduce_word(tuple(x for f in bottom for x in f.word))))
    frame_source,frame = min(candidates,key=lambda item:(len(item[1]),item[1]))
    before_word = tuple(x for f in factors for x in f.word)
    after_word = tuple(x for f in after for x in f.word)
    discrepancy = reduce_word(after_word + inverse_word(
        frame + before_word + inverse_word(frame)))
    if discrepancy:
        raise ValueError('Cyclic change of basepoint failed its word certificate')
    return dict(kind='cyclic_rotation', offset=offset, factors=after,
                moved_ids=tuple(f.id for f in block), frame=frame,frame_source=frame_source,
                word_certificate=discrepancy,
                disk_discrepancy=reduce_word(after_word + inverse_word(before_word)),
                scope='explicit_global_conjugation', sphere_move=False)
