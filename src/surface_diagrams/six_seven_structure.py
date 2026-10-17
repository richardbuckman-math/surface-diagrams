"""Structural certificates for the supplied (6,7), not its full derivation.

The intersection residues obstruct one specific inverse-lantern strategy.
The rank-two monodromy and the sphere lantern are independently checkable
pieces for the continuing search; neither identifies a Hurwitz equivalence.
"""
from dataclasses import replace
from itertools import combinations
from math import gcd

from .braid_actions import inverse_word, reduce_word
from .factorization_explorer import (
    Factor, combine_factors, initial_factors, move_factor, product, split_factor,
)
from .hyperelliptic_homology import (
    IDENTITY, half_twist_class, homology_action, homology_quotient,
)
from .mapping_classes import ConjugatedTwist, exact_action, supported_class
from .sphere_actions import sphere_curve_action, sphere_inner_certificate


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


def sphere_root_half_transport():
    """C10 C13 transports the original F3 half twist to F9 on the sphere.

    Cj is one ordinary three-point twist whose square is original Fj.
    The full sphere action and +I homology check the lifted equality;
    the nontrivial disk discrepancy is kept explicitly.
    """
    factors = {factor.id: factor for factor in initial_factors()}
    roots = tuple(replace(factors[name], id=name + '.root', power=1)
                  for name in ('F10', 'F13'))
    source, target = factors['F3'], factors['F9']
    transport = product(roots)
    transported = replace(source, id='C10C13(F3)',
                          conjugator=reduce_word(transport + source.conjugator))
    discrepancy = reduce_word(transported.word + inverse_word(target.word))
    sphere = sphere_inner_certificate(discrepancy)
    assert sphere['certified'] and not sphere['disk_identity']
    assert homology_action(discrepancy) == IDENTITY
    return dict(roots=roots, source=source, target=target, transported=transported,
                transport=transport, disk_discrepancy=discrepancy,
                sphere_certificate=sphere, lift_homology=IDENTITY,
                scope='Six-marked sphere and closed genus two; disk discrepancy nontrivial')


def root_transport_consolidation():
    """A replayable partial derivation pairing original F3 and F9.

    Split F10 and F13, move one root of each upward, then apply one explicit
    sphere-only equality. Every other step is an exact disk split/Hurwitz/
    combine move. The result is a mixed fourteen-factor state, not a complete
    structural derivation of (6,7).
    """
    state = initial_factors()
    records = [dict(title='Supplied factorization', kind='start', factors=state)]

    def position(name):
        return next(i for i, factor in enumerate(state) if factor.id == name)

    def move_before(moving_id, target_id):
        nonlocal state
        while position(moving_id) > position(target_id):
            index = position(moving_id)
            crossed = state[index - 1].id
            state = move_factor(state, index, index - 1)
            records.append(dict(title=f'{moving_id} up past {crossed}',
                                kind='disk_hurwitz', factors=state,
                                source=index, target=index - 1))

    for name in ('F10', 'F13'):
        state = split_factor(state, position(name), 'powers')
        records.append(dict(title=f'Split {name} into ordinary roots',
                            kind='disk_split', factors=state))
    move_before('F10.1', 'F9')
    move_before('F13.1', 'F9')
    before, source = state[position('F9')], state[position('F3')]
    discrepancy = reduce_word(before.word + inverse_word(source.word))
    sphere = sphere_inner_certificate(discrepancy)
    assert sphere['certified'] and not sphere['disk_identity']
    assert homology_action(discrepancy) == IDENTITY
    after = replace(source, id='F9.sphere')
    index = position('F9')
    state = state[:index] + (after,) + state[index + 1:]
    records.append(dict(title='Rechart transported F9 as F3 on the sphere',
                        kind='sphere_rewrite', factors=state,
                        local_before=before, local_after=after,
                        disk_discrepancy=discrepancy,
                        sphere_certificate=sphere, lift_homology=IDENTITY))
    # Stop immediately after F3, then combine the now identical disk records.
    while position('F9.sphere') > position('F3') + 1:
        index = position('F9.sphere')
        crossed = state[index - 1].id
        state = move_factor(state, index, index - 1)
        records.append(dict(title=f'F9.sphere up past {crossed}',
                            kind='disk_hurwitz', factors=state,
                            source=index, target=index - 1))
    state = combine_factors(state, position('F3'))
    records.append(dict(title='Combine F3 and transported F9 into a pair twist',
                        kind='disk_combine', factors=state))
    final_sphere = sphere_inner_certificate(product(state))
    assert final_sphere['certified']
    assert homology_action(product(state)) == IDENTITY
    return dict(stages=tuple(records), final_sphere_certificate=final_sphere,
                final_lift_homology=IDENTITY, complete_structural_derivation_found=False)


def six_half_stabilizer_audit():
    """Test standard chain arcs and original supports for a curve stabilizer.

    The product is Torelli, but none of these five curve classes is fixed.
    Every original factor support is moved too. This excludes these specific
    inputs to a stabilizer-based algorithm;
    it does not rule out every possible fixed symmetric curve.
    """
    halves = tuple(factor for factor in initial_factors() if factor.half)
    word = product(halves)
    assert homology_action(word) == IDENTITY
    rows = []
    for index in range(1, 6):
        original = sphere_curve_action((), (index, index + 1))
        image = sphere_curve_action(word, original)
        rows.append(dict(endpoints=(index, index + 1), original=original,
                         image=image, fixed=image == original))
    supports = []
    for factor in initial_factors():
        original = sphere_curve_action((), supported_class(factor.mapping_class))
        image = sphere_curve_action(word, original)
        supports.append(dict(id=factor.id, original=original, image=image,
                             fixed=image == original))
    return dict(word=word, lift_homology=IDENTITY, arcs=tuple(rows),
                original_supports=tuple(supports),
                all_standard_chain_arcs_moved=all(not row['fixed'] for row in rows),
                all_original_supports_moved=all(not row['fixed'] for row in supports),
                scope='Only the tested curve classes; no general irreducibility claim')
