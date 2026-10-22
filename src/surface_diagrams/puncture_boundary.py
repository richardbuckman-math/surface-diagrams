"""Rechart a fixed sphere puncture as the boundary of a five-point disk.

Schreier rewriting tracks that strand, rather than searching for a routing.
The chosen framed lift sends sigma5^2 to the positive twist T1234. Central
boundary corrections are retained; a capped puncture is not a framed hole.
"""
from dataclasses import replace
from functools import lru_cache

from .braid_actions import inverse_word, reduce_word
from .factorization_explorer import product
from .hyperelliptic_homology import IDENTITY, homology_action
from .mapping_classes import exact_action, supported_class
from .sphere_actions import sphere_chain_certificate, sphere_supported_class
from .twist_simplify import simplify_twist

BOUNDARY_WORD = (1, 2, 3, 4) * 5
FOUR_POINT_WORD = (1, 2, 3) * 4


def _power(word, exponent):
    return tuple(word) * exponent if exponent >= 0 else inverse_word(word) * -exponent


def _schreier_representative(position):
    # r_j sends j to 6. A prefix has the form h r_j, where h fixes 6.
    return tuple(range(5, position - 1, -1))


def _positive_edge(position, generator):
    if generator == position - 1:
        return ()
    if generator == position:
        g = tuple(-i for i in range(position, 5))
        return g + FOUR_POINT_WORD + inverse_word(g)
    return (generator if generator < position else generator - 1,)


def _rewrite_prefix(word):
    output = []
    position = 6
    for letter in word:
        if type(letter) is not int or not 1 <= abs(letter) <= 5:
            raise ValueError('Use signed six-strand generators 1..5')
        i = abs(letter)
        next_position = i + 1 if position == i else i if position == i + 1 else position
        edge = _positive_edge(position if letter > 0 else next_position, i)
        output.extend(edge if letter > 0 else inverse_word(edge))
        position = next_position
    return reduce_word(output), position


@lru_cache(maxsize=1)
def puncture_chart_generators():
    """All thirty positive Schreier edges, with explicit sphere discrepancies.

    Negative edges are inverses of the corresponding positive edge. Every
    changed edge has a five-arc sphere identity certificate and +I lift.
    These are sphere moves, not asserted equalities of disk braids.
    """
    records = []
    for position in range(1, 7):
        r = _schreier_representative(position)
        for i in range(1, 6):
            end = i + 1 if position == i else i if position == i + 1 else position
            before = reduce_word(r + (i,) + inverse_word(_schreier_representative(end)))
            after = _positive_edge(position, i)
            discrepancy = reduce_word(before + inverse_word(after))
            sphere = sphere_chain_certificate(discrepancy)
            lift = homology_action(discrepancy)
            if not sphere['certified'] or lift != IDENTITY:
                raise ValueError('A fixed-puncture chart generator failed its sphere/lift check')
            disk_equal = exact_action(before) == exact_action(after)
            records.append(dict(position=position, generator=i, before=before,
                after=after, disk_equal=disk_equal, disk_discrepancy=discrepancy,
                sphere_certificate=sphere, lift_homology=lift))
    return tuple(records)


def fixed_puncture_word(word, *, marked_point=6):
    """Return a B5 framed lift of a braid fixing the selected marked point.

    This is a homomorphism on the stabilizer, after the explicit global frame.
    It is not the operation of forgetting a strand. In particular sigma5^2
    becomes T1234, not the identity. Non-fixed endpoints are rejected.
    """
    if type(marked_point) is not int or not 1 <= marked_point <= 6:
        raise ValueError('Choose a marked point numbered 1..6')
    word = tuple(word)
    frame = _schreier_representative(marked_point)
    before = reduce_word(frame + word + inverse_word(frame))
    after, end = _rewrite_prefix(before)
    if end != 6:
        raise ValueError('The braid does not fix the selected marked point')
    discrepancy = reduce_word(before + inverse_word(after))
    sphere = sphere_chain_certificate(discrepancy)
    lift = homology_action(discrepancy)
    if not sphere['certified'] or lift != IDENTITY:
        raise ValueError('The framed puncture chart changed the sphere action or chosen lift')
    return dict(word=after, frame=frame, marked_point=marked_point,
        disk_discrepancy=discrepancy, sphere_certificate=sphere,
        lift_homology=lift, kind='sphere_rechart')


def puncture_to_boundary(factors, *, marked_point=6, simplify=True):
    """Compute supported B5 factors and their central boundary corrections.

    An ordinary k-point twist containing the chosen puncture becomes its
    complementary (6-k)-point twist times boundary^(k-2). This includes the
    odd three-point root's boundary correction, hence its deck sign. Powers
    and inverse research factors retain their signs. An incident odd half
    twist is rejected. The based B5 product is calculated independently.
    """
    factors = tuple(factors)
    if not factors:
        raise ValueError('Supply a nonempty factorization')
    if type(marked_point) is not int or not 1 <= marked_point <= 6:
        raise ValueError('Choose a marked point numbered 1..6')
    frame = _schreier_representative(marked_point)
    framed = tuple(replace(f, conjugator=reduce_word(frame + f.conjugator)) for f in factors)
    output = []
    checks = []
    correction = 0
    for original, f in zip(factors, framed):
        h, j = _rewrite_prefix(f.conjugator)
        a, k, power, half = f.first, f.points, f.power, f.half
        b = a + k - 1
        inside = a <= j <= b
        if inside and half:
            if power % 2:
                raise ValueError('An odd half twist moves the selected puncture: ' + f.id)
            half, power = False, power // 2
        central = (k - 2) * power * getattr(f, 'sign', 1) if inside else 0
        if inside:
            complement = 6 - k
            new = (replace(f, conjugator=reduce_word(h + (1, 2, 3, 4) * (b - 1)),
                           first=1, points=complement, power=power, half=False)
                   if complement >= 2 else None)
        else:
            new = replace(f, conjugator=h, first=a - int(j < a))
        if new is not None and simplify:
            t = simplify_twist(new.mapping_class, strands=5)
            new = replace(new, conjugator=t.conjugator, first=t.first)
        # This based-action equality verifies the complement formula and its
        # framing, rather than inferring equality from a matching endpoint set.
        raw, end = _rewrite_prefix(f.word)
        if end != 6:
            raise ValueError('A factor does not fix the chosen puncture')
        new_word = new.word if new is not None else ()
        expected = _power(BOUNDARY_WORD, central) + new_word
        if exact_action(raw, strands=5) != exact_action(expected, strands=5):
            raise ValueError('A supported puncture chart failed its exact B5 framing')
        discrepancy = reduce_word(f.word + inverse_word(new_word))
        sphere = sphere_chain_certificate(discrepancy)
        lift = homology_action(discrepancy)
        expected_lift = homology_action(_power(BOUNDARY_WORD, central))
        if (not sphere['certified'] or lift != expected_lift or
                (new is not None and sphere_supported_class(f.mapping_class) !=
                 sphere_supported_class(new.mapping_class))):
            raise ValueError('A complementary support changed its sphere curve or lift sign')
        checks.append(dict(id=f.id, source=original, globally_framed=f, factor=new,
            boundary_power=central, complemented=inside, raw_disk_word=raw,
            disk_framing_equal=True, disk_discrepancy=discrepancy,
            sphere_certificate=sphere, lift_homology=lift,
            is_individual_lift_equality=lift == IDENTITY))
        correction += central
        if new is not None:
            output.append(new)
    output = tuple(output)
    word = product(output)
    action = exact_action(word, strands=5)
    writhe = sum(1 if letter > 0 else -1 for letter in word)
    exponent = writhe // 20 if writhe % 20 == 0 else None
    central_equal = (exponent is not None and action ==
                     exact_action(_power(BOUNDARY_WORD, exponent), strands=5))
    discrepancy = reduce_word(product(framed) + inverse_word(word))
    sphere = sphere_chain_certificate(discrepancy)
    lift = homology_action(discrepancy)
    if not sphere['certified'] or lift != homology_action(_power(BOUNDARY_WORD, correction)):
        raise ValueError('The joint boundary correction failed its sphere/lift check')
    lengths = tuple(len(supported_class(f.mapping_class, strands=5)) for f in output)
    return dict(factors=output, marked_point=marked_point, global_frame=frame,
        factor_certificates=tuple(checks), boundary_correction_power=correction,
        normalized_disk_action=action, normalized_writhe=writhe,
        normalized_boundary_power=exponent if central_equal else None,
        normalized_boundary_action_verified=central_equal,
        framed_boundary_power=correction + exponent if central_equal else None,
        joint_disk_discrepancy=discrepancy, joint_sphere_certificate=sphere,
        joint_lift_homology=lift, joint_rechart_preserves_lift=lift == IDENTITY,
        score=dict(max_support_word=max(lengths, default=0),
                   total_support_word=sum(lengths), braid_letters=len(word)),
        complete_named_derivation=False,
        scope='Exact framed puncture-to-boundary chart; based-action equality is not a named lantern derivation.')


def early_boundary_derivation():
    """A 19-operation boundary-action proof avoiding the fifty expansion.

    The last disk relation is independently checked on based meridians. Its
    short named lantern derivation remains open; the numerical move count
    must not be confused with an elementary derivation of that last equality.
    """
    from .fifty_decomposition import working_seed_to_legacy_chart
    from .six_seven_structure import (
        SignedResearchFactor, three_root_prefix_lantern,
    )
    from .sphere_support_compact import reframe_factors
    working = working_seed_to_legacy_chart()
    prefix = three_root_prefix_lantern()
    # Keep both the working global frame and its simpler F4-before-F3
    # order. Undo only the two other adjacent moves needed by the root gather.
    from .factorization_explorer import split_factor, move_factor, combine_factors
    common = working['initial_frame']
    stages = list(working['stages'][:3])
    state = stages[-1]['factors']
    def position(name):
        return next(i for i,f in enumerate(state) if f.id==name)
    def move(source,target):
        nonlocal state
        moving,crossed=state[source].id,state[target].id
        state=move_factor(state,source,target)
        stages.append(dict(kind='disk_hurwitz',factors=state,source=source,target=target,
            title=moving+(' up past ' if source>target else ' down past ')+crossed))
    for name in ('F1','F8','F10'):
        state=split_factor(state,position(name),'powers')
        stages.append(dict(kind='disk_split',title='Split '+name+' into ordinary roots',factors=state))
    move(position('F1.2'),position('F2'))
    for name in ('F8.1','F10.1'):
        while position(name)>position('F7'):
            index=position(name);move(index,index-1)
    index=position('F7');before=state[index]
    after=replace(state[position('F2')],id='F7.disk')
    if exact_action(before.word)!=exact_action(after.word):
        raise ValueError('The working-chart root transport failed its exact half-twist match')
    state=state[:index]+(after,)+state[index+1:]
    stages.append(dict(kind='disk_rewrite',title='Use the exact disk equality of the matched arcs',
        factors=state,local_before=(before,),local_after=(after,)))
    while position('F7.disk')>position('F2')+1:
        index=position('F7.disk');move(index,index-1)
    state=combine_factors(state,position('F2'))
    stages.append(dict(kind='disk_combine',title='Combine the two matched half twists',factors=state))
    before=state[:3]
    after=reframe_factors(prefix['stages'][-1]['factors'][:2],common)['factors']
    discrepancy=reduce_word(product(before)+inverse_word(product(after)))
    sphere=sphere_chain_certificate(discrepancy)
    if not sphere['certified'] or homology_action(discrepancy)!=IDENTITY:
        raise ValueError('The working-chart prefix lantern changed its lifted action')
    state=after+state[3:]
    stages.append(dict(kind='sphere_rewrite',title='SPHERE LANTERN: absorb the matched pair and the two prefix roots',
        factors=state,local_before=before,local_after=after,disk_discrepancy=discrepancy,
        sphere_certificate=sphere,lift_homology=IDENTITY))
    # Unframe only the input to the calculation; no backwards chart change is
    # made in the replay. The one displayed frame below is the composition.
    source=reframe_factors(state,inverse_word(common))['factors']
    chart = puncture_to_boundary(source, marked_point=3)
    combined_frame = reduce_word(chart['global_frame'] + inverse_word(common))
    record = reframe_factors(stages[-1]['factors'], combined_frame)
    state = record['factors']
    stages.append(dict(record, title='Global frame: fixed working point 2 becomes displayed point 6'))
    boundary = SignedResearchFactor('boundary.corrections', (), 1, 5,
                                   power=chart['boundary_correction_power'])
    normalized = chart['factors']
    corrected = (boundary,) + normalized
    discrepancy = reduce_word(product(state) + inverse_word(product(corrected)))
    certificate = sphere_chain_certificate(discrepancy)
    if not certificate['certified'] or homology_action(discrepancy) != IDENTITY:
        raise ValueError('The early fixed-point chart failed its full sphere/lift certificate')
    stages.append(dict(kind='sphere_rewrite',
        title='SPHERE RECHART: use the five-point disk; retain SIX boundary corrections',
        factors=corrected, local_before=state, local_after=corrected,
        disk_equality=False, disk_discrepancy=discrepancy,
        sphere_certificate=certificate, lift_homology=IDENTITY,
        boundary_power=6, caption='Six boundary twists retain the chosen framing; the other fourteen factors remain positive.'))
    cap = sphere_chain_certificate(boundary.word)
    if not cap['certified'] or homology_action(boundary.word) != IDENTITY:
        raise ValueError('The six explicit boundary corrections cannot be capped in this lift')
    stages.append(dict(kind='sphere_rewrite', title='SPHERE MOVE: cap the SIX framing corrections',
        factors=normalized, local_before=(boundary,), local_after=(),
        disk_equality=False, disk_discrepancy=boundary.word,
        sphere_certificate=cap, lift_homology=IDENTITY,
        caption='The corrections are removed here, separately and visibly.'))
    if chart['normalized_boundary_power'] != 4:
        raise ValueError('The early ordered product is not the fourth boundary power')
    final = replace(boundary, id='boundary.five.fourth', power=4)
    stages.append(dict(kind='disk_boundary_relation',
        title='Exact B5 action: the FOURTH outer-boundary twist', factors=(final,),
        local_before=normalized, local_after=(final,), disk_equality=True,
        boundary_power=4, disk_action_certificate=dict(strands=5,
            actual=chart['normalized_disk_action'], expected=exact_action(final.word,5), equal=True),
        caption='Independently checked on five based meridians; a short named derivation of this equality is still open.'))
    cap = sphere_chain_certificate(final.word)
    if not cap['certified'] or homology_action(final.word) != IDENTITY:
        raise ValueError('The fourth boundary power cannot be capped in this lift')
    stages.append(dict(kind='sphere_rewrite', title='SPHERE MOVE: cap the FOURTH boundary power',
        factors=(), local_before=(final,), local_after=(), disk_equality=False,
        disk_discrepancy=final.word, sphere_certificate=cap, lift_homology=IDENTITY))
    if len(stages) != 26:
        raise ValueError('The early boundary route lost an explicit transition')
    atomic_stages=tuple(stages)
    gather=[i for i,s in enumerate(stages) if s['kind']=='disk_hurwitz' and s['title'].startswith('F7.disk up past ')]
    if len(gather)!=7 or gather!=list(range(gather[0],gather[0]+7)):
        raise ValueError('The seven adjacent steps no longer form one continuous Hurwitz drag')
    first,last=gather[0],gather[-1]
    block=dict(stages[last],kind='disk_hurwitz_block',
        title='Drag the matched arc up across SEVEN factors (one Hurwitz drag)',
        source=stages[first]['source'],target=stages[last]['target'],
        adjacent_moves=7,atomic_steps=tuple(stages[first:last+1]),
        caption='One dragged factor stays fixed across seven neighbors. All seven adjacent checks are retained in the certificate.')
    graphical=tuple(stages[:first])+(block,)+tuple(stages[last+1:])
    return dict(stages=graphical, atomic_stages=atomic_stages, chart=chart, atomic_moves=25,
        graphical_steps=19, next_relations=early_boundary_lantern_target(normalized),
        fixed_point_in_working_chart=2, combined_disk_frame=combined_frame,
        sphere_move_count=sum(s['kind']=='sphere_rewrite' for s in graphical),
        independent_boundary_action_identity_certificate=True,
        uses_source_identity_as_hypothesis=False, complete_named_derivation=False,
        scope='Nineteen operations with twenty-five retained adjacent/presentation checks, ending in an independent B5 action check; the named derivation of that last equality remains open.')


def early_boundary_lantern_target(factors):
    """A specific unapplied disk lantern in the new early boundary chart.

    A=C12, B=C13 and Q=T45 satisfy A B Q = O T12. The common chart
    maps the standard three clusters to {1,2}, {4}, {5}; all supports,
    not just those endpoint sets, are checked in the faithful B5 action.
    """
    from .factorization_explorer import Factor
    by_id={f.id:f for f in factors}
    a=replace(by_id['F12'],power=1)
    b=replace(by_id['F13'],power=1)
    q=Factor('early.target.Q45',(),4,2)
    outer=Factor('early.target.O1245',(-4,-4,-3,-4),1,4)
    inner=Factor('early.target.T12',(),1,2)
    left,right=(a,b,q),(outer,inner)
    if exact_action(product(left),5)!=exact_action(product(right),5):
        raise ValueError('The early C12/C13 cluster lantern failed its ordered B5 check')
    shortened=replace(a,conjugator=(-4,-3),first=1)
    moved=inverse_word(b.word)+a.word+b.word
    if exact_action(moved,5)!=exact_action(shortened.word,5):
        raise ValueError('The targeted inverse-root transport failed its short support check')
    return dict(name='PC lantern with clusters {1,2}, {4}, {5}',
        common_chart=(-4,-4,-3,-4),local_before=left,local_after=right,
        exact_disk_equality=True,applied_to_replay=False,
        inverse_substitution_needs_positive_Q45_cancellation=True,
        root_transport=dict(moving_root=b,changed_root=a,shortened_root=shortened,
            before_support_length=len(supported_class(a.mapping_class,5)),
            after_support_length=len(supported_class(shortened.mapping_class,5)),
            exact_disk_equality=True,applied_to_replay=False))
