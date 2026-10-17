"""Structural certificates for the supplied (6,7), not its full derivation.

The intersection residues obstruct one specific inverse-lantern strategy.
The rank-two monodromy and the sphere lantern are independently checkable
pieces for the continuing search; neither identifies a Hurwitz equivalence.
"""
from dataclasses import dataclass, replace
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


def root_pair_lantern():
    """The transported PC lantern explaining C10 C13 and its F3/F9 action.

    Inner clusters are {2,5}, {3,4}, {6}; the last is point-capped.
    C10 C13 Q2345 = O23456 P25 P34 is exact in B6. Restoring a framed
    boundary at point 6 requires its boundary twist on the right. Dropping
    O is legal on the sphere but changes the genus-two lift by -I; O² may
    be dropped in the closed lift. The reduced conjugator below is an exact
    disk transport, not merely a same-endpoint or homology match.
    """
    initial = {factor.id: factor for factor in initial_factors()}
    roots = tuple(replace(initial[name], id=name + '.root', power=1)
                  for name in ('F10', 'F13'))
    q = Factor('Q2345', (), 2, 4)
    outer = Factor('O23456', (), 2, 5)
    p25 = Factor('P25', (-2, -3), 4, 2)
    p34 = Factor('P34', (), 3, 2)
    left, right = roots + (q,), (outer, p25, p34)
    assert exact_action(product(left)) == exact_action(product(right))
    identity = tuple((i,) for i in range(1, 7))
    for a, b in combinations((outer, p25, p34, q), 2):
        commutator = a.word + b.word + inverse_word(a.word) + inverse_word(b.word)
        assert exact_action(commutator) == identity
    peripheral = sphere_inner_certificate(outer.word)
    minus_identity = tuple(tuple(-x for x in row) for row in IDENTITY)
    assert peripheral['certified'] and not peripheral['disk_identity']
    assert homology_action(outer.word) == minus_identity

    reduced_transport = reduce_word(p25.word + p34.word + inverse_word(q.word))
    source, target = initial['F3'], initial['F9']
    assert exact_action(reduced_transport + source.word + inverse_word(reduced_transport)) == exact_action(target.word)
    squared_left = roots + roots + (replace(q, power=2),)
    squared_right = (replace(p25, power=2), replace(p34, power=2))
    discrepancy = reduce_word(product(squared_left) + inverse_word(product(squared_right)))
    squared_sphere = sphere_inner_certificate(discrepancy)
    assert squared_sphere['certified'] and not squared_sphere['disk_identity']
    assert homology_action(discrepancy) == IDENTITY
    assert exact_action(discrepancy) == exact_action(outer.word + outer.word)
    return dict(left=left, right=right, inner_clusters=((2, 5), (3, 4), (6,)),
                framed_point_correction=(6,), common_chart_conjugator=(-2, -3),
                disk_equality=True, commuting_multitwists=(outer, p25, p34, q),
                peripheral_sphere_certificate=peripheral, peripheral_lift_homology=minus_identity,
                reduced_transport_word=reduced_transport, reduced_transport_factors=(p25, p34, q),
                reduced_transport_signs=(1, 1, -1), source=source, target=target,
                reduced_transport_disk_equality=True,
                squared_left=squared_left, squared_right=squared_right,
                squared_disk_discrepancy=discrepancy, squared_sphere_certificate=squared_sphere,
                squared_lift_homology=IDENTITY, applied_to_full_factorization=False,
                endpoint_pair_ids=(('F10.1', 'F13.1'), ('F10.2', 'F13.2')),
                endpoint_pair_conjugators=(inverse_word(source.word), inverse_word(roots[1].word)))


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


@dataclass(frozen=True)
class SignedResearchFactor(Factor):
    """A signed twist for research routes, outside the positive lab format.

    ``mapping_class`` describes the positive support for the existing drawing
    code. ``word`` includes the sign. Inverse factors are deliberately not
    accepted by the public positive-factor workspace parser or combine tool.
    """
    sign: int = 1

    def __post_init__(self):
        if type(self.sign) is not int or self.sign not in (-1, 1):
            raise ValueError('A research factor sign must be +1 or -1')
        self.mapping_class  # Validate the underlying positive support record.

    @property
    def word(self):
        word = super().word
        return word if self.sign == 1 else inverse_word(word)


def root_cluster_lantern_route():
    """Apply both transported cluster lanterns to the saved mixed endpoint.

    Each substitution is exact in B6 and introduces one inverse Q twist.
    The two five-point peripheral twists are removed together, with a full
    disk discrepancy and +I lift check. Each separate removal would have
    lift -I. This is a partial signed derivation, not a positive lab session.
    """
    previous = root_transport_consolidation()
    state = tuple(SignedResearchFactor(f.id, f.conjugator, f.first, f.points,
                                       f.power, f.half)
                  for f in previous['stages'][-1]['factors'])
    records = [dict(title='Mixed endpoint of the root-transport route',
                    kind='start', factors=state)]
    lantern = root_pair_lantern()

    def position(name):
        return next(i for i, factor in enumerate(state) if factor.id == name)

    while position('F13.2') > position('F10.2') + 1:
        index = position('F13.2')
        crossed = state[index - 1].id
        state = move_factor(state, index, index - 1)
        records.append(dict(title=f'F13.2 up past {crossed}', kind='disk_hurwitz',
                            factors=state, source=index, target=index - 1))

    for number, (ids, conjugator) in enumerate(zip(
            lantern['endpoint_pair_ids'], lantern['endpoint_pair_conjugators']), 1):
        index = position(ids[0])
        before = state[index:index + 2]
        assert tuple(f.id for f in before) == ids
        replacements = tuple(SignedResearchFactor(
            f'L{number}.{factor.id}', reduce_word(conjugator + factor.conjugator),
            factor.first, factor.points, factor.power, factor.half, sign)
            for factor, sign in zip(lantern['right'] + (lantern['left'][2],),
                                    (1, 1, 1, -1)))
        assert exact_action(product(before)) == exact_action(product(replacements))
        after = state[:index] + replacements + state[index + 2:]
        assert exact_action(product(state)) == exact_action(product(after))
        state = after
        records.append(dict(title=f'Apply transported cluster lantern {number}',
                            kind='disk_lantern', factors=state,
                            local_before=before, local_after=replacements,
                            common_conjugator=conjugator,
                            framed_point_correction=(6,)))

    peripheral_ids = ('L1.O23456', 'L2.O23456')
    peripheral_factors = tuple(f for f in state if f.id in peripheral_ids)
    minus_identity = tuple(tuple(-x for x in row) for row in IDENTITY)
    assert all(sphere_inner_certificate(f.word)['certified']
               and homology_action(f.word) == minus_identity
               for f in peripheral_factors)
    after = tuple(f for f in state if f.id not in peripheral_ids)
    discrepancy = reduce_word(product(state) + inverse_word(product(after)))
    sphere = sphere_inner_certificate(discrepancy)
    assert sphere['certified'] and not sphere['disk_identity']
    assert homology_action(discrepancy) == IDENTITY
    state = after
    records.append(dict(title='Remove both peripheral twists together on the sphere',
                        kind='sphere_rewrite', factors=state,
                        removed_factors=peripheral_factors,
                        disk_discrepancy=discrepancy,
                        sphere_certificate=sphere, lift_homology=IDENTITY))

    # A four-point boundary is the same sphere curve as its complementary
    # two-point boundary. Retain the disk discrepancy and check the lift sign
    # separately, rather than identifying curves from their endpoint sets.
    complementary_pair = Factor('P16', (1, 2, 3, 4), 5, 2)
    q = lantern['left'][2]
    assert sphere_curve_action((), supported_class(q.mapping_class)) == sphere_curve_action(
        (), supported_class(complementary_pair.mapping_class))
    for number, conjugator in enumerate(lantern['endpoint_pair_conjugators'], 1):
        index = position(f'L{number}.Q2345')
        before = state[index]
        after = SignedResearchFactor(
            f'L{number}.Q.complement', reduce_word(conjugator + complementary_pair.conjugator),
            complementary_pair.first, 2, sign=-1)
        discrepancy = reduce_word(before.word + inverse_word(after.word))
        sphere = sphere_inner_certificate(discrepancy)
        assert sphere['certified'] and not sphere['disk_identity']
        assert homology_action(discrepancy) == IDENTITY
        state = state[:index] + (after,) + state[index + 1:]
        records.append(dict(title=f'Draw inverse Q{number} along its complementary pair',
                            kind='sphere_rewrite', factors=state,
                            local_before=(before,), local_after=(after,),
                            disk_discrepancy=discrepancy,
                            sphere_certificate=sphere, lift_homology=IDENTITY))

    # The obvious {1,4}, {4,6}, {1,6} endpoint triangle is NOT a PC lantern.
    # Two algebraic intersections are three, already obstructing a common
    # chart of the three standard pair curves (all intersections one upstairs).
    triangle = tuple(next(f for f in state if f.id == name) for name in (
        'F3+F9.sphere', 'L1.Q.complement', 'L2.Q.complement'))
    vectors = tuple(half_twist_class(f.conjugator, f.first) for f in triangle)
    pairings = tuple(tuple(intersection(a, b) for b in vectors) for a in vectors)
    candidate = dict(ids=tuple(f.id for f in triangle), vectors=vectors,
                     algebraic_intersections=pairings,
                     fits_standard_pair_lantern=all(abs(pairings[i][j]) == 1
                                                    for i, j in combinations(range(3), 2)))
    assert not candidate['fits_standard_pair_lantern']
    final_sphere = sphere_inner_certificate(product(state))
    assert final_sphere['certified']
    assert homology_action(product(state)) == IDENTITY
    return dict(stages=tuple(records), follows='root_transport_consolidation',
                final_sphere_certificate=final_sphere, final_lift_homology=IDENTITY,
                direct_lantern_candidate=candidate,
                complete_structural_derivation_found=False,
                scope='Signed research route on the sphere and in closed genus two; not a positive lab workspace')


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
