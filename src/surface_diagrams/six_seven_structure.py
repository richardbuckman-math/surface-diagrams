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
from .sphere_actions import sphere_curve_action, sphere_inner_certificate, sphere_chain_certificate


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


def three_root_half_transport():
    """C8 C10 C1 transports original F2 to F7 exactly in the disk.

    This is a second original half-twist pair, separate from the F3/F9 route.
    Apply C1 to F2 first; C8 C10 then transports that new simple arc to F7.
    All roots here are the actual supplied routed supports.
    """
    initial = {f.id: f for f in initial_factors()}
    roots = tuple(replace(initial[name], id=name + '.root', power=1)
                  for name in ('F8', 'F10', 'F1'))
    source, target = initial['F2'], initial['F7']
    transport = product(roots)
    transported = replace(source, id='C8C10C1(F2)',
                          conjugator=reduce_word(transport + source.conjugator))
    discrepancy = reduce_word(transported.word + inverse_word(target.word))
    assert exact_action(discrepancy) == tuple((i,) for i in range(1, 7))
    sphere = sphere_inner_certificate(discrepancy)
    assert sphere['certified'] and sphere['disk_identity']
    assert homology_action(discrepancy) == IDENTITY
    # A short representative helps explain the geometry: after applying C1,
    # F2 is sigma3^-1 sigma5^-1 H45 sigma5 sigma3.
    intermediate = Factor('C1(F2)', (-3, -5), 4, 2, half=True)
    assert exact_action(intermediate.word) == exact_action(
        roots[2].word + source.word + inverse_word(roots[2].word))
    assert exact_action(product(roots[:2]) + intermediate.word
                        + inverse_word(product(roots[:2]))) == exact_action(target.word)
    return dict(roots=roots, source=source, target=target, transport=transport,
                transported=transported, intermediate=intermediate,
                disk_discrepancy=discrepancy, sphere_certificate=sphere,
                lift_homology=IDENTITY, scope='Exact disk braid equality, hence sphere and closed genus two')


def three_root_transport_consolidation():
    """A positive, disk-exact replay pairing original F2 and F7.

    One C1 root starts before F2, so move it down across F2 first. This
    turns the source into C1(F2) without incorrectly assuming all three
    original roots are available after the source. The remaining two roots
    may then be extracted from later factors. No sphere rechart is needed.
    """
    state = initial_factors()
    records = [dict(title='Supplied factorization', kind='start', factors=state)]

    def position(name):
        return next(i for i, f in enumerate(state) if f.id == name)

    def move_one(source, target):
        nonlocal state
        moving, crossed = state[source].id, state[target].id
        state = move_factor(state, source, target)
        records.append(dict(title=f'{moving} {"up" if source > target else "down"} past {crossed}',
                            kind='disk_hurwitz', factors=state, source=source, target=target))

    for name in ('F1', 'F8', 'F10'):
        state = split_factor(state, position(name), 'powers')
        records.append(dict(title=f'Split {name} into ordinary roots',
                            kind='disk_split', factors=state))
    move_one(position('F1.2'), position('F2'))
    for name in ('F8.1', 'F10.1'):
        while position(name) > position('F7'):
            index = position(name)
            move_one(index, index - 1)

    before, source = state[position('F7')], state[position('F2')]
    discrepancy = reduce_word(before.word + inverse_word(source.word))
    assert exact_action(discrepancy) == tuple((i,) for i in range(1, 7))
    after = replace(source, id='F7.disk')
    index = position('F7')
    state = state[:index] + (after,) + state[index + 1:]
    records.append(dict(title='Use the exact disk equality of the two simple arcs',
                        kind='disk_rewrite', factors=state,
                        local_before=(before,), local_after=(after,),
                        disk_discrepancy=discrepancy))
    while position('F7.disk') > position('F2') + 1:
        index = position('F7.disk')
        move_one(index, index - 1)
    state = combine_factors(state, position('F2'))
    records.append(dict(title='Combine transported F2 and F7 into a pair twist',
                        kind='disk_combine', factors=state))
    assert exact_action(product(state)) == exact_action(product(initial_factors()))
    sphere = sphere_inner_certificate(product(state))
    assert sphere['certified'] and homology_action(product(state)) == IDENTITY
    # F9/F11 now have zero algebraic intersection, but not disjoint supports.
    # An exact moved-curve witness prevents treating that homology coincidence
    # as another inverse-lantern configuration.
    a, b = (state[position(name)] for name in ('F9', 'F11'))
    vectors = tuple(half_twist_class(f.conjugator, f.first) for f in (a, b))
    boundary = supported_class(b.mapping_class)
    original = sphere_curve_action((), boundary)
    image = sphere_curve_action(a.word, boundary)
    assert intersection(*vectors) == 0 and original != image
    return dict(stages=tuple(records), final_sphere_certificate=sphere,
                final_lift_homology=IDENTITY, all_steps_exact_in_disk=True,
                algebraically_disjoint_pair=dict(ids=('F9', 'F11'), vectors=vectors,
                    algebraic_intersection=0, original_curve=original, image_curve=image,
                    sphere_support_fixed=False),
                complete_structural_derivation_found=False)


def f2_f7_cluster_lantern():
    """A cluster lantern and complementary root behind the F2/F7 route.

    C8 C10 Q2346 = O23456 P34 P26 is an exact PC lantern in B6.
    The residual F8.2 root in the replay has the same sphere curve as C12,
    but differs in the genus-two lift by the deck involution. That sign can
    compensate a peripheral O omission; neither is a separate lift equality.
    """
    transport = three_root_half_transport()
    c8, c10, c1 = transport['roots']
    chart = (-2, -3, 4)
    q = Factor('Q2346', (-2, -3, -5), 2, 4)
    outer = Factor('O23456', (), 2, 5)
    p34 = Factor('P34', chart, 2, 2)
    p26 = Factor('P26', chart, 5, 2)
    left, right = (c8, c10, q), (outer, p34, p26)
    assert exact_action(product(left)) == exact_action(product(right))
    for a, b in combinations((outer, p34, p26, q), 2):
        assert exact_action(a.word + b.word + inverse_word(a.word) + inverse_word(b.word)) == tuple(
            (i,) for i in range(1, 7))
    reduced_transport = reduce_word(p34.word + p26.word + inverse_word(q.word) + c1.word)
    assert exact_action(reduced_transport + transport['source'].word
                        + inverse_word(reduced_transport)) == exact_action(transport['target'].word)

    endpoint = {f.id: f for f in three_root_transport_consolidation()['stages'][-1]['factors']}
    common = inverse_word(transport['intermediate'].word)
    for name, root in zip(('F8.1', 'F10.1'), (c8, c10)):
        assert exact_action(endpoint[name].word) == exact_action(common + root.word + inverse_word(common))
    c12 = replace(next(f for f in initial_factors() if f.id == 'F12'),
                  id='F12.root', power=1)
    before = endpoint['F8.2']
    assert exact_action(before.word) == exact_action(inverse_word(c10.word) + c8.word + c10.word)
    root_discrepancy = reduce_word(before.word + inverse_word(c12.word))
    root_sphere = sphere_inner_certificate(root_discrepancy)
    minus_identity = tuple(tuple(-x for x in row) for row in IDENTITY)
    assert root_sphere['certified'] and not root_sphere['disk_identity']
    assert homology_action(root_discrepancy) == minus_identity
    assert sphere_curve_action((), supported_class(before.mapping_class)) == sphere_curve_action(
        (), supported_class(c12.mapping_class))
    squared_discrepancy = reduce_word(before.word * 2 + inverse_word(c12.word * 2))
    squared_sphere = sphere_inner_certificate(squared_discrepancy)
    assert squared_sphere['certified'] and homology_action(squared_discrepancy) == IDENTITY
    assert homology_action(outer.word) == minus_identity

    # A concrete follow-on, rather than a new broad scan: after the one-Q
    # lantern fork, its complementary negative pair is exactly the pair term
    # of this PC half-lantern on the remaining C13 square.
    from .projected_relations import pc_half_lantern_terms
    c13 = replace(next(f for f in initial_factors() if f.id == 'F13'), power=1)
    c13_complement = Factor('C13.complement',
                           (-5,) + (1, 2, 3, 4, 5) * 2 + (4, 5) * 2, 4, 3)
    c13_discrepancy = reduce_word(c13.word + inverse_word(c13_complement.word))
    c13_sphere = sphere_inner_certificate(c13_discrepancy)
    assert c13_sphere['certified'] and homology_action(c13_discrepancy) == minus_identity
    c13_squared_discrepancy = reduce_word(c13.word * 2 + inverse_word(c13_complement.word * 2))
    assert sphere_inner_certificate(c13_squared_discrepancy)['certified']
    assert homology_action(c13_squared_discrepancy) == IDENTITY
    half_lantern = tuple(Factor(f'C13.HL{index + 1}', term.conjugator, term.first,
                                term.points, term.power, term.half)
                         for index, term in enumerate(pc_half_lantern_terms(c13_complement.mapping_class)))
    assert exact_action(product(half_lantern)) == exact_action(c13_complement.word)
    negative_pair_support = Factor('Q.complement',
        reduce_word(common + (-2, -3, -5) + (1, 2, 3, 4)), 5, 2)
    assert exact_action(negative_pair_support.word) == exact_action(replace(half_lantern[2], power=1).word)
    residual_left, residual_right = (c10, c12, negative_pair_support), (p34, p26)
    residual_discrepancy = reduce_word(product(residual_left) + inverse_word(product(residual_right)))
    residual_sphere = sphere_inner_certificate(residual_discrepancy)
    assert residual_sphere['certified'] and not residual_sphere['disk_identity']
    assert homology_action(residual_discrepancy) == IDENTITY
    return dict(left=left, right=right, framed_point_correction=(5,),
                inner_clusters=((3, 4), (2, 6), (5,)), common_chart_conjugator=chart,
                reduced_transport_word=reduced_transport,
                endpoint_pair_ids=('F8.1', 'F10.1'), endpoint_pair_conjugator=common,
                root_rechart_before=before, root_rechart_after=c12,
                root_disk_discrepancy=root_discrepancy, root_sphere_certificate=root_sphere,
                root_lift_homology=minus_identity, peripheral_lift_homology=minus_identity,
                squared_disk_discrepancy=squared_discrepancy,
                squared_sphere_certificate=squared_sphere, squared_lift_homology=IDENTITY,
                remaining_c13_complement=c13_complement, remaining_c13_half_lantern=half_lantern,
                c13_root_disk_discrepancy=c13_discrepancy, c13_root_sphere_certificate=c13_sphere,
                c13_root_lift_homology=minus_identity,
                c13_squared_disk_discrepancy=c13_squared_discrepancy,
                negative_pair_support=negative_pair_support,
                half_lantern_pair_match_exact_in_disk=True,
                residual_root_lantern=dict(left=residual_left, right=residual_right,
                    disk_discrepancy=residual_discrepancy, sphere_certificate=residual_sphere,
                    lift_homology=IDENTITY, applied_to_endpoint=False),
                applied_to_full_factorization=False)


def three_root_prefix_lantern():
    """Apply a named sphere genus-two lantern to the new mixed prefix.

    Its three factor records multiply exactly to (C1 D)^2 in the disk,
    where D=C1(F2). This pair is a common-chart image of T123 and H34.
    The new boundary pair twists replace the prefix on the sphere and in
    closed genus two, with its nontrivial disk discrepancy recorded.
    Four ordinary roots remain later in the word; this is not yet an (8,6)
    positive Lefschetz factorization or a complete derivation of (6,7).
    """
    state = three_root_transport_consolidation()['stages'][-1]['factors']
    transport = three_root_half_transport()
    c1, d = transport['roots'][2], transport['intermediate']
    before = state[:3]
    assert exact_action(product(before)) == exact_action((c1.word + d.word) * 2)
    common = (-3, 4) + (1, 2, 3, 4, 5) * 2
    standard_c = Factor('standard_C', common, 1, 3)
    standard_h = Factor('standard_H', common, 3, 2, half=True)
    assert exact_action(standard_c.word) == exact_action(c1.word)
    assert exact_action(standard_h.word) == exact_action(d.word)
    local = sphere_genus_two_lantern(common)
    after = tuple(replace(f, id=name) for f, name in zip(local['right'], ('prefix.P45', 'prefix.P12')))
    discrepancy = reduce_word(product(before) + inverse_word(product(after)))
    sphere = sphere_inner_certificate(discrepancy)
    assert sphere['certified'] and not sphere['disk_identity']
    assert homology_action(discrepancy) == IDENTITY
    endpoint = after + state[3:]
    assert sphere_inner_certificate(product(endpoint))['certified']
    assert homology_action(product(endpoint)) == IDENTITY
    return dict(stages=(dict(title='Endpoint with the (C1 D)^2 prefix', kind='start', factors=state),
                        dict(title='Replace that prefix by its two lantern boundary twists',
                             kind='sphere_rewrite', factors=endpoint,
                             local_before=before, local_after=after,
                             disk_discrepancy=discrepancy,
                             sphere_certificate=sphere, lift_homology=IDENTITY)),
                follows='three_root_transport_consolidation', common_conjugator=common,
                complete_structural_derivation_found=False,
                scope='Six-marked sphere and closed genus two; disk discrepancy nontrivial')


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


def three_root_lantern_reduction():
    """Continue the new sphere lantern through one temporary negative twist.

    A transported PC lantern introduces Q^-1. A paired peripheral/root
    rechart keeps the closed lift correct. The remaining C13 square has a
    specific complementary PC half-lantern whose pair term cancels Q^-1
    exactly in the disk. The endpoint is positive again, but two odd
    three-point-root records remain, so this is still a partial derivation.
    """
    state = tuple(SignedResearchFactor(f.id, f.conjugator, f.first, f.points, f.power, f.half)
                  for f in three_root_prefix_lantern()['stages'][-1]['factors'])
    records = [dict(title='After the prefix sphere lantern', kind='start', factors=state)]
    local = f2_f7_cluster_lantern()
    common = local['endpoint_pair_conjugator']

    def position(name):
        return next(i for i, f in enumerate(state) if f.id == name)

    def disk_replace(index, count, replacements, title, kind):
        nonlocal state
        before = state[index:index + count]
        assert exact_action(product(before)) == exact_action(product(replacements))
        state = state[:index] + tuple(replacements) + state[index + count:]
        records.append(dict(title=title, kind=kind, factors=state,
                            local_before=before, local_after=tuple(replacements)))

    def sphere_replace(index, replacement, title):
        nonlocal state
        before = state[index]
        discrepancy = reduce_word(before.word + inverse_word(replacement.word))
        certificate = sphere_inner_certificate(discrepancy)
        assert certificate['certified'] and not certificate['disk_identity']
        assert homology_action(discrepancy) == IDENTITY
        state = state[:index] + (replacement,) + state[index + 1:]
        records.append(dict(title=title, kind='sphere_rewrite', factors=state,
                            local_before=(before,), local_after=(replacement,),
                            disk_discrepancy=discrepancy, sphere_certificate=certificate,
                            lift_homology=IDENTITY))

    index = position('F8.1')
    assert tuple(f.id for f in state[index:index + 2]) == local['endpoint_pair_ids']
    replacements = tuple(SignedResearchFactor('new.' + f.id,
        reduce_word(common + f.conjugator), f.first, f.points, f.power, f.half, sign)
        for f, sign in zip(local['right'] + (local['left'][2],), (1, 1, 1, -1)))
    disk_replace(index, 2, replacements, 'Apply the {34}, {26}, {5} cluster lantern', 'disk_lantern')

    # These two changes must be one lift step: each component has deck sign -I.
    before = state
    peripheral = state[position('new.O23456')]
    root_before = state[position('F8.2')]
    c12 = local['root_rechart_after']
    root_after = SignedResearchFactor(c12.id, c12.conjugator, c12.first, c12.points)
    state = tuple(root_after if f.id == root_before.id else f for f in state
                  if f.id != peripheral.id)
    discrepancy = reduce_word(product(before) + inverse_word(product(state)))
    certificate = sphere_inner_certificate(discrepancy)
    assert certificate['certified'] and not certificate['disk_identity']
    assert homology_action(discrepancy) == IDENTITY
    records.append(dict(title='Pair the peripheral omission with the complementary-root rechart',
                        kind='sphere_rewrite', factors=state, removed_factors=(peripheral,),
                        root_before=root_before, root_after=root_after,
                        component_lift_homology=local['root_lift_homology'],
                        disk_discrepancy=discrepancy, sphere_certificate=certificate,
                        lift_homology=IDENTITY))

    def move_one(source, target):
        nonlocal state
        moving, crossed = state[source].id, state[target].id
        state = move_factor(state, source, target)
        records.append(dict(title=f'{moving} {"up" if source > target else "down"} past {crossed}',
                            kind='disk_hurwitz', factors=state, source=source, target=target))

    while position('F12.root') < position('F12') - 1:
        index = position('F12.root')
        move_one(index, index + 1)
    index = position('F12.root')
    before = state[index:index + 2]
    state = combine_factors(state, index)
    records.append(dict(title='Combine the complementary root with F12 into a cube',
                        kind='disk_combine', factors=state, local_before=before,
                        local_after=(state[index],)))
    pair = local['negative_pair_support']
    sphere_replace(position('new.Q2346'), SignedResearchFactor('new.Q.complement',
        pair.conjugator, pair.first, pair.points, sign=-1),
        'Draw the inverse Q along its complementary {1,5} pair')

    companion = local['remaining_c13_complement']
    sphere_replace(position('F13'), SignedResearchFactor('C13.complement.square',
        companion.conjugator, companion.first, companion.points, power=2),
        'Rechart the whole C13 square along its complementary triple')
    terms = local['remaining_c13_half_lantern']
    replacements = tuple(SignedResearchFactor(f'C13.HL{repeat + 1}.{j + 1}',
        term.conjugator, term.first, term.points, term.power, term.half)
        for repeat in range(2) for j, term in enumerate(terms))
    disk_replace(position('C13.complement.square'), 1, replacements,
                 'Apply the chosen PC half lantern to each C13 unit', 'disk_half_lantern')

    while position('C13.HL2.3') > position('new.Q.complement') + 1:
        index = position('C13.HL2.3')
        move_one(index, index - 1)
    negative = state[position('new.Q.complement')]
    positive = state[position('C13.HL2.3')]
    assert negative.sign == -1 and positive.sign == 1 and positive.power == 2
    replacement = replace(positive, id='P15.after-cancellation', power=1)
    disk_replace(position('new.Q.complement'), 2, (replacement,),
                 'Cancel the inverse pair against one unit of the squared pair', 'disk_cancel')
    assert all(f.sign == 1 for f in state)
    # The accumulated disk point-push exceeds the based disk-action bound.
    # Check the complete sphere action by its five exact arc classes instead;
    # all local disk moves and sphere discrepancies above remain certified.
    final_sphere = sphere_chain_certificate(product(state))
    assert final_sphere['certified'] and homology_action(product(state)) == IDENTITY
    root_chart = inverse_word(local['remaining_c13_half_lantern'][2].word)
    c10, c12 = local['left'][1], local['root_rechart_after']
    root_models = (replace(c10, conjugator=reduce_word(c12.word + c10.conjugator)),
                   replace(c12, power=3))
    root_ids = ('F10.2', 'F12.root+F12')
    for name, model in zip(root_ids, root_models):
        assert exact_action(state[position(name)].word) == exact_action(
            root_chart + model.word + inverse_word(root_chart))
    return dict(stages=tuple(records), follows='three_root_prefix_lantern',
                final_sphere_certificate=final_sphere, final_lift_homology=IDENTITY,
                final_all_factors_positive=True,
                remaining_odd_root_ids=tuple(f.id for f in state if f.points == 3 and f.power % 2),
                residual_root_chart=root_chart, residual_root_models=root_models,
                complete_structural_derivation_found=False,
                scope='Partial sphere/closed-genus-two derivation; not an equivalent disk-only workspace')


def three_root_residual_lantern():
    """Remove the last odd roots using the actual transported root order.

    Write A=C10, B=C12 and let S be the saved endpoint chart. Its roots
    are S(BAB^-1)S^-1 and SB^3S^-1. Move one B unit up across F11;
    the adjacent pair is then S(BA)S^-1. Conjugating the checked relation
    ABP=R1R2 by B gives BA=(BR1B^-1)(BR2B^-1)(BPB^-1)^-1.
    The negative pair can be transported to cancel prefix.P12 on the
    sphere. The resulting positive (24,3) factorization is an intermediate,
    not a complete derivation to a recognized exterior-boundary relation.
    """
    previous = three_root_lantern_reduction()
    state = previous['stages'][-1]['factors']
    records = [dict(title='Positive endpoint with two odd-root records',
                    kind='start', factors=state)]
    local = f2_f7_cluster_lantern()
    relation = local['residual_root_lantern']
    b = local['root_rechart_after']
    common = reduce_word(previous['residual_root_chart'] + b.word)

    def position(name):
        return next(i for i, f in enumerate(state) if f.id == name)

    def disk_replace(index, count, replacements, title, kind):
        nonlocal state
        before = state[index:index + count]
        replacements = tuple(replacements)
        assert exact_action(product(before)) == exact_action(product(replacements))
        state = state[:index] + replacements + state[index + count:]
        records.append(dict(title=title, kind=kind, factors=state,
                            local_before=before, local_after=replacements))

    def move_one(source, target):
        nonlocal state
        moving, crossed = state[source].id, state[target].id
        before = state[min(source, target):max(source, target) + 1]
        state = move_factor(state, source, target)
        after = state[min(source, target):max(source, target) + 1]
        assert exact_action(product(before)) == exact_action(product(after))
        records.append(dict(title=f'{moving} down past {crossed}' if source < target else
                            f'{moving} up past {crossed}', kind='disk_hurwitz',
                            factors=state, source=source, target=target))

    def sphere_replace(index, count, replacements, title):
        nonlocal state
        before = state[index:index + count]
        replacements = tuple(replacements)
        discrepancy = reduce_word(product(before) + inverse_word(product(replacements)))
        certificate = sphere_inner_certificate(discrepancy)
        assert certificate['certified'] and not certificate['disk_identity']
        assert homology_action(discrepancy) == IDENTITY
        state = state[:index] + replacements + state[index + count:]
        records.append(dict(title=title, kind='sphere_rewrite', factors=state,
                            local_before=before, local_after=replacements,
                            disk_discrepancy=discrepancy, sphere_certificate=certificate,
                            lift_homology=IDENTITY))

    index = position('F12.root+F12')
    split = split_factor(state, index, 'powers')
    disk_replace(index, 1, split[index:index + 3], 'Split the C12 cube into three roots',
                 'disk_split')
    move_one(position('F12.root+F12.1'), position('F10.2') + 1)
    index = position('F10.2')
    assert state[index + 1].id == 'F12.root+F12.1'
    replacements = tuple(SignedResearchFactor('residual.' + f.id,
        reduce_word(common + f.conjugator), f.first, f.points, f.power, f.half, sign)
        for f, sign in zip(relation['right'] + (relation['left'][2],), (1, 1, -1)))
    sphere_replace(index, 2, replacements,
                   'Use the residual lantern in the chart S C12, with the roots in their actual order')
    index = position('F12.root+F12.2')
    combined = combine_factors(state, index)
    disk_replace(index, 2, (combined[index],), 'Combine the two unused C12 roots into a square',
                 'disk_combine')

    # Move each intervening neighbor down. The inverse pair travels upward
    # and is conjugated; simply dragging it upward would keep it fixed.
    negative_id = 'residual.Q.complement'
    while position(negative_id) > position('prefix.P12') + 1:
        index = position(negative_id)
        move_one(index - 1, index)
    index = position('prefix.P12')
    positive, negative = state[index:index + 2]
    assert positive.sign == 1 and negative.sign == -1
    assert positive.points == negative.points == 2 and positive.power == negative.power == 1
    assert sphere_curve_action((), supported_class(positive.mapping_class)) == sphere_curve_action(
        (), supported_class(negative.mapping_class))
    inverse = replace(positive, id='residual.inverse.prefix.P12', sign=-1)
    sphere_replace(index + 1, 1, (inverse,),
                   'Rechart the transported inverse pair along the prefix pair on the sphere')
    disk_replace(index, 2, (), 'Cancel the equal positive and negative pair twists', 'disk_cancel')

    assert all(f.sign == 1 and (f.points == 2 or f.points == 3 and f.power % 2 == 0)
               for f in state)
    final_sphere = sphere_chain_certificate(product(state))
    assert final_sphere['certified'] and homology_action(product(state)) == IDENTITY
    counts = (sum(f.power * (1 if f.half else 2) for f in state if f.points == 2),
              sum(f.power // 2 for f in state if f.points == 3))
    assert counts == (24, 3)
    return dict(stages=tuple(records), follows='three_root_lantern_reduction',
                relation_common_conjugator=common, residual_relation=relation,
                final_sphere_certificate=final_sphere, final_lift_homology=IDENTITY,
                final_all_factors_positive=True, final_lefschetz_counts=counts,
                remaining_odd_root_ids=(), complete_structural_derivation_found=False,
                scope='Positive sphere/closed-genus-two intermediate; exterior-boundary derivation still open')


def three_root_half_lantern_compression():
    """Compress the duplicated half-lantern suffix without assuming positivity.

    The earlier P15 unit and the five-term C13 suffix multiply exactly in
    B6 to C13^2 P15^-1. Moving that unit next to the suffix changes five
    intervening factors by checked Hurwitz moves. This gives a shorter
    signed branch of the (24,3) route, with four separating twists and net
    twelve nonseparating units. It is NOT a positive (12,4) factorization:
    its last inverse pair has no direct cancellation with the five positive
    pair factors under the fixed intervening-product transport tested here.
    """
    state = three_root_residual_lantern()['stages'][-1]['factors']
    records = [dict(title='Positive (24,3) endpoint before reverse half-lantern compression',
                    kind='start', factors=state)]

    def position(name):
        return next(i for i, f in enumerate(state) if f.id == name)

    while position('P15.after-cancellation') < position('C13.HL1.1') - 1:
        index = position('P15.after-cancellation')
        moving, crossed = state[index].id, state[index + 1].id
        before = state[index:index + 2]
        state = move_factor(state, index, index + 1)
        assert exact_action(product(before)) == exact_action(product(state[index:index + 2]))
        records.append(dict(title=f'{moving} down past {crossed}', kind='disk_hurwitz',
                            factors=state, source=index, target=index + 1))

    index = position('P15.after-cancellation')
    pair = state[index]
    root = f2_f7_cluster_lantern()['remaining_c13_complement']
    before = state[index:]
    assert len(before) == 6
    after = (SignedResearchFactor('C13.recombined', root.conjugator,
                                 root.first, root.points, power=2),
             replace(pair, id='inverse.P15', sign=-1))
    assert exact_action(product(before)) == exact_action(product(after))
    state = state[:index] + after
    records.append(dict(title='Reverse the two PC half lanterns and retain the inverse pair',
                        kind='disk_half_lantern', factors=state,
                        local_before=before, local_after=after))

    # For a positive candidate before the inverse, fixing intervening
    # neighbors transports the inverse by their entire ordered product.
    # Store the exact unequal classes, not just an unlabelled failed search.
    negative = state[-1]
    attempts = []
    for index, candidate in enumerate(state[:-1]):
        if candidate.half or candidate.points != 2:
            continue
        intervening = product(state[index + 1:-1])
        actual = sphere_curve_action(intervening, supported_class(negative.mapping_class))
        expected = sphere_curve_action((), supported_class(candidate.mapping_class))
        attempts.append(dict(target_id=candidate.id,
                             intervening_ids=tuple(f.id for f in state[index + 1:-1]),
                             transported_inverse_support=actual, positive_support=expected,
                             matches=actual == expected))
    assert len(attempts) == 5 and not any(attempt['matches'] for attempt in attempts)
    final_sphere = sphere_chain_certificate(product(state))
    assert final_sphere['certified'] and homology_action(product(state)) == IDENTITY
    counts = dict(positive_nonseparating=14, negative_nonseparating=2,
                  positive_separating=4, net_nonseparating=12)
    assert sum(f.sign * f.power * (1 if f.half else 2)
               for f in state if f.points == 2) == counts['net_nonseparating']
    assert sum(f.power // 2 for f in state if f.points == 3) == counts['positive_separating']
    target = replace(negative, sign=1)
    target_support = sphere_curve_action((), supported_class(target.mapping_class))
    crossing_factor = state[1]
    assert crossing_factor.id == 'F3'
    crossing_image = sphere_curve_action(crossing_factor.word, target_support)
    assert crossing_image != target_support
    return dict(stages=tuple(records), follows='three_root_residual_lantern',
                final_sphere_certificate=final_sphere, final_lift_homology=IDENTITY,
                final_all_factors_positive=False, signed_counts=counts,
                positive_equation_left=state[:-1], positive_equation_target=target,
                target_crossing_witness=dict(factor_id=crossing_factor.id,
                    target_support=target_support, image_support=crossing_image),
                direct_cancellation_attempts=tuple(attempts),
                complete_structural_derivation_found=False,
                scope='Disk-exact signed compression of the saved sphere intermediate; not a positive (12,4) relation')


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
