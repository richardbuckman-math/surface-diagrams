"""Finite, one-way obstructions to specified Hurwitz cluster configurations.

These genus-two homology orbits forget Torelli information. An excluded
intersection rules a configuration out; an allowed residue proves nothing
about the existence of curves, a relation, or a Hurwitz route.
"""
from collections import deque

from .braid_actions import inverse_word
from .hyperelliptic_homology import homology_action
from .mapping_classes import VerificationLimitError


def _intersection(a, b):
    return a[0]*b[2] + a[1]*b[3] - a[2]*b[0] - a[3]*b[1]


def _vector(value):
    value = tuple(value)
    if len(value) != 4 or any(type(x) is not int for x in value):
        raise ValueError('A genus-two homology vector needs four integers')
    return value


def modular_homology_orbit(vector, factor_words, modulus=4, max_states=4096):
    """Compute the complete vector orbit under the supplied braid subgroup.

    Both generators and their inverses act on (Z/modulus)^4. The finite
    closure has at most modulus**4 states. A state bound raises rather than
    returning a partial orbit that could falsely certify an obstruction.
    The exact integral braid action is reduced modulo the stated modulus.
    """
    vector = _vector(vector)
    if type(modulus) is not int or modulus < 2:
        raise ValueError('modulus must be an integer at least two')
    if type(max_states) is not int or max_states < 1:
        raise ValueError('max_states must be a positive integer')
    matrices = set()
    for word in factor_words:
        word = tuple(word)
        for w in (word, inverse_word(word)):
            matrices.add(tuple(tuple(x % modulus for x in row)
                               for row in homology_action(w)))
    matrices = tuple(sorted(matrices))
    start = tuple(x % modulus for x in vector)
    seen, pending = {start}, deque([start])
    while pending:
        current = pending.popleft()
        for matrix in matrices:
            image = tuple(sum(matrix[i][j]*current[j] for j in range(4)) % modulus
                          for i in range(4))
            if image not in seen:
                if len(seen) == max_states:
                    raise VerificationLimitError('Finite homology orbit exceeded its state bound')
                seen.add(image)
                pending.append(image)
    return tuple(sorted(seen))


def modular_pairing_obstruction(left, right, factor_words,
                                target_intersection=2, modulus=4, max_states=4096):
    """Exclude an absolute pairing between two ancestry-labelled factors.

    Under Hurwitz moves confined to this source block, each labelled cycle
    stays in its orbit under the original monodromy subgroup. The Cartesian
    product of the two orbits is an overestimate of the reachable pairs.
    Disjoint target residues therefore give a rigorous obstruction, whereas
    overlap is inconclusive. Both cycle orientations are accounted for.

    A simultaneous global conjugation preserves the symplectic pairings,
    so it cannot remove this obstruction. Substitutions introducing new
    cycles, sphere-only support replacements, or mixing factors from outside
    the chosen block are not covered. Target 2 is necessary for the two
    half twists in the PC half-lantern relation, not sufficient for it.
    """
    if type(target_intersection) is not int or target_intersection < 0:
        raise ValueError('target_intersection must be a nonnegative integer')
    words = tuple(tuple(word) for word in factor_words)
    a = modular_homology_orbit(left, words, modulus, max_states)
    b = modular_homology_orbit(right, words, modulus, max_states)
    residues = tuple(sorted({_intersection(x, y) % modulus for x in a for y in b}))
    targets = tuple(sorted({target_intersection % modulus,
                            (-target_intersection) % modulus}))
    return dict(modulus=modulus, left_orbit=a, right_orbit=b,
                pairing_residues=residues, target_intersection=target_intersection,
                target_residues=targets, complete_orbits=True,
                obstructed=not bool(set(residues).intersection(targets)),
                positive_result_proves_equivalence=False,
                scope='Necessary pairing test for ancestry-labelled factors under block Hurwitz moves and global conjugation only')
