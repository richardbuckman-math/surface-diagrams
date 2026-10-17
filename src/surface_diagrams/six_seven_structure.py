"""Structural certificates for the supplied (6,7), not its full derivation.

The intersection residues obstruct one specific inverse-lantern strategy.
The rank-two monodromy and the sphere lantern are independently checkable
pieces for the continuing search; neither identifies a Hurwitz equivalence.
"""
from dataclasses import replace
from itertools import combinations
from math import gcd

from .braid_actions import inverse_word, reduce_word
from .factorization_explorer import Factor, initial_factors, product
from .hyperelliptic_homology import (
    IDENTITY, half_twist_class, homology_action, homology_quotient,
)
from .mapping_classes import ConjugatedTwist, exact_action
from .sphere_actions import sphere_inner_certificate


def intersection(left, right):
    return (left[0]*right[2] + left[1]*right[3]
            - left[2]*right[0] - left[3]*right[1])


def nonseparating_intersection_certificate(factors):
    """Record ancestry-labelled residues modulo the square of their gcd.

    Preconditions make every factor either one positive nonseparating twist
    or a squared three-point twist (a separating twist upstairs). Under a
    Hurwitz move, an oriented vanishing class changes by adding its pairing
    with the crossed class times that class. All pairings divisible by d
    therefore change only by multiples of d^2. Separating factors act as I.
    With transported orientations the signed residues are invariant. Factor
    records may instead reverse a class when simplifying its conjugator; the
    returned unoriented residues identify r with -r and remain invariant then.
    The theorem concerns Hurwitz moves/global conjugation without substitutions
    introducing new nonseparating factors. Zero residues are inconclusive.
    """
    factors = tuple(factors)
    if any(not ((f.half and f.points == 2 and f.power == 1) or
                (not f.half and f.points == 3 and f.power == 2))
           for f in factors):
        raise ValueError('Use unit half twists and squared three-point twists')
    halves = tuple(f for f in factors if f.half)
    vectors = tuple(half_twist_class(f.conjugator, f.first) for f in halves)
    matrix = tuple(tuple(intersection(a,b) for b in vectors) for a in vectors)
    divisor = 0
    for i,j in combinations(range(len(vectors)),2):
        divisor = gcd(divisor,matrix[i][j])
    modulus = divisor * divisor
    residues = (tuple(tuple(value % modulus for value in row) for row in matrix)
                if modulus else None)
    unoriented = (tuple(tuple(min(value,(-value)%modulus) for value in row)
                        for row in residues) if residues else None)
    zero_pairs = (tuple((halves[i].id,halves[j].id)
                        for i,j in combinations(range(len(halves)),2)
                        if residues[i][j] == 0) if residues else None)
    return dict(ids=tuple(f.id for f in halves),vectors=vectors,
                intersection_matrix=matrix,pairing_gcd=divisor,modulus=modulus,
                residues=residues,unoriented_residues=unoriented,zero_residue_pairs=zero_pairs,
                rules_out_disjoint_original_halves=bool(residues and not zero_pairs))


def six_seven_lattice_certificate():
    """Verify the six width-four transvections and their fixed complement."""
    factors=initial_factors()
    halves=tuple(f for f in factors if f.half)
    vectors=tuple(half_twist_class(f.conjugator,f.first) for f in halves)
    a,b=vectors[:2]
    coefficients=((1,0),(0,1),(1,-3),(1,-2),(-2,3),(1,-1))
    assert vectors == tuple(tuple(p*x+q*y for x,y in zip(a,b))
                            for p,q in coefficients)
    assert intersection(a,b)==4
    assert homology_quotient((a,b)) == dict(lattice_rank=2,free_rank=2,torsion=())
    fixed=((0,3,1,0),(-1,2,0,1))
    assert intersection(*fixed)==4
    assert all(intersection(v,w)==0 for v in vectors for w in fixed)
    assert homology_quotient(fixed) == dict(lattice_rank=2,free_rank=2,torsion=())
    restricted=[]
    for f,(p,q) in zip(halves,coefficients):
        m=((1+4*p*q,-4*p*p),(4*q*q,1-4*p*q))
        full=homology_action(f.word)
        for col,vector in enumerate((a,b)):
            actual=tuple(sum(full[i][j]*vector[j] for j in range(4))
                         for i in range(4))
            expected=tuple(m[0][col]*a[i]+m[1][col]*b[i] for i in range(4))
            assert actual==expected
        restricted.append(m)
    result=((1,0),(0,1))
    for m in restricted:
        result=tuple(tuple(sum(result[i][k]*m[k][j] for k in range(2))
                           for j in range(2)) for i in range(2))
    assert result==((1,0),(0,1))
    assert homology_action(product(factors))==IDENTITY
    for f in factors:
        full=homology_action(f.word)
        assert all(tuple(sum(full[i][j]*v[j] for j in range(4))
                         for i in range(4))==v for v in fixed)
    return dict(ids=tuple(f.id for f in halves),basis=(a,b),
                intersection=4,coefficients=coefficients,
                restricted_matrices=tuple(restricted),restricted_product=result,
                fixed_complement=fixed,fixed_complement_intersection=4,
                scope='Homological certificate; no claimed Xiao equivalence or geometric derivation')


def sphere_genus_two_lantern(conjugator=()):
    """H34 (T123 H34 T123^-1) T123^2 = T12 T56 on S^2 with six marks.

    Its genus-two lift is the standard lantern with boundary curves in two
    parallel pairs. It replaces four nonseparating twists by two nonseparating
    and one separating twist. The relation is intentionally NOT asserted in
    B6: the exact disk discrepancy is retained in the certificate. Sphere
    identity plus +I homology distinguishes the lift from the deck involution.
    """
    g=tuple(conjugator)
    root=ConjugatedTwist((),1,3).word
    left=(Factor('H34',g,3,2,half=True),
          Factor('T123(H34)',reduce_word(g+root),3,2,half=True),
          Factor('T123^2',g,1,3,power=2))
    right=(Factor('T12',g,1,2),Factor('T56',g,5,2))
    discrepancy=reduce_word(product(left)+inverse_word(product(right)))
    sphere=sphere_inner_certificate(discrepancy)
    assert sphere['certified']
    assert homology_action(discrepancy)==IDENTITY
    assert exact_action(product(left)) != exact_action(product(right))
    x,y=left[:2]
    assert intersection(half_twist_class(x.conjugator,x.first),
                        half_twist_class(y.conjugator,y.first))==0
    return dict(left=left,right=right,disk_discrepancy=discrepancy,
                sphere_certificate=sphere,lift_homology=IDENTITY,
                scope='Six-marked sphere and closed genus two, not the framed disk')
