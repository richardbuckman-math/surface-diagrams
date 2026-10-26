"""Return an outside rose loan and reach an actual exterior PC lantern.

This separate positive disk continuation does not shorten the complete99 proof.
Every named substitution retains individual common-chart matches.
"""
from dataclasses import replace

from .braid_actions import inverse_word, reduce_word
from .disk_intersection import disk_curve_intersection
from .early_boundary_pure import _PositiveReplay, _score
from .factorization_explorer import Factor, product
from .framed_boundary_relations import enclosed_boundaries
from .hyperelliptic_homology import IDENTITY, homology_action
from .mapping_classes import exact_action
from .outside_half_lantern import _cyclic_start, _matches
from .point_pushing import split_fixed_last_strand
from .projected_relations import pc_daisy_terms, pc_rose_terms
from .six_seven_structure import research_hurwitz_move
from .sphere_actions import sphere_chain_certificate


def _terms(twist, prefix, relation):
    return tuple(Factor(prefix+str(j), t.conjugator, t.first, t.points, t.power, t.half)
                 for j, t in enumerate(relation(twist)))


def _transport(factors, chart):
    return tuple(replace(f, conjugator=reduce_word(chart+f.conjugator)) for f in factors)


def _witness(replay, canonical, chart=(), **extra):
    stage = replay.stages[-1]
    matches = _matches(stage['local_before'], _transport(canonical, chart))
    discrepancy = reduce_word(product(stage['local_before'])+inverse_word(product(stage['local_after'])))
    sphere = sphere_chain_certificate(discrepancy)
    lift = homology_action(discrepancy)
    if not sphere['certified'] or lift != IDENTITY:
        raise ValueError('The local disk substitution failed its separate sphere/lift check')
    stage['named_pattern_witness'] = dict(canonical=canonical, common_chart=chart,
        individual_matches=matches, disk_discrepancy=discrepancy,
        sphere_certificate=sphere, chosen_lift_discrepancy=lift, applied=True, **extra)
    stage['framed_balance_before_minus_after'] = tuple(
        sum(f.power for f in stage['local_before'] if j in enclosed_boundaries(f.mapping_class,5))-
        sum(f.power for f in stage['local_after'] if j in enclosed_boundaries(f.mapping_class,5))
        for j in range(1,6))


def return_outside_rose(factors):
    """Nine positive disk operations, retaining seven adjacent transports.

    The source is the preferred round-chart outside-half-lantern endpoint.
    A cyclic PC rose returns its Q12 loan; the actual125 daisy supplies15.
    Two individually matched cabled lanterns then reach one visible exterior.
    """
    source = tuple(factors)
    by_id = {f.id:f for f in source}
    required = ('outside.half.root','outside.rose.1','outside.rose.2',
                'alternative.F12.2','alternative.O1234','alternative.return.1','one.unit.Q1')
    if len(source) != 17 or any(name not in by_id for name in required):
        raise ValueError('Use the preferred outside-half-lantern endpoint')
    if by_id['outside.half.root'] != Factor('outside.half.root',(),1,3):
        raise ValueError('The actual new root must be the round preferred-chart R123')
    if any(f.half or f.power != 1 for f in source):
        raise ValueError('The source must consist of positive unit full twists')
    r = _PositiveReplay(source)
    r.stages[0]['title'] = 'Preferred outside-half-lantern endpoint before returning its loan'

    i = r.position('outside.half.root'); root = r.factors[i]
    internal = replace(root, conjugator=(-1,-1))
    _matches((root,), (internal,))
    rose = _terms(internal.mapping_class, 'return.', pc_rose_terms)
    _matches((by_id['one.unit.Q1'],), (rose[1],))
    cyclic = rose[1:]+rose[:1]
    r.substitute(i,1,cyclic,'Cyclic PC rose lends Q12 and retains the actual Q1 duplicate','disk_pc_rose')
    _witness(r,(root,),canonical_rose=rose,cyclic_offset=1,
             internal_outer_match=_matches((root,),(internal,)), cyclic_terms=cyclic)
    _cyclic_start(r,'return.0','Cyclic start at the actual return Q12')
    r.drag('return.0','alternative.O1234',title='Return Q12 across the commuting125 root and four-point outer')
    restored = Factor('return.restored.R124',(3,),1,3)
    restore_rose = _terms(restored.mapping_class,'restore.pattern.',pc_rose_terms)
    i = r.position('return.0')
    r.substitute(i,3,(restored,),'The actual three donor petals restore their R124 root','disk_pc_rose')
    _witness(r,restore_rose,actual_restored_root=restored)

    i = r.position('alternative.F12.2'); donor = r.factors[i]
    petals = _terms(donor.mapping_class,'return.125.',pc_daisy_terms)
    r.substitute(i,1,petals,'Actual125 PC daisy supplies the exact15 petal','disk_pc_daisy')
    _witness(r,(donor,),canonical_daisy=petals)
    p15 = petals[-1]
    r.drag(p15.id,'alternative.O1234',title='Carry the actual15 petal past the four-point outer')

    chart = (-2,-1,-1)
    outer = Factor('pattern.O1345',(1,),2,4)
    daisy = _terms(outer.mapping_class,'pattern.daisy.',pc_daisy_terms)
    r134 = Factor('pattern.R134',(1,),2,3)
    r345 = Factor('pattern.R345',(),3,3)
    canonical = (daisy[-1],r134,r345)
    canonical_after = (outer,Factor('pattern.I34',(),3,2))
    _matches((daisy[0],),(r134,))
    r345_daisy = _terms(r345.mapping_class,'pattern.R345.',pc_daisy_terms)
    _matches(daisy[1:3],r345_daisy[1:])
    if exact_action(product(canonical),5) != exact_action(product(canonical_after),5):
        raise ValueError('The cyclic cabled PC lantern failed')
    i = r.position(p15.id)
    _matches(r.factors[i:i+3],_transport(canonical,chart))
    raw = (Factor('return.O1245',chart+(1,),2,4),Factor('return.inner24',chart,3,2))
    outputs = tuple(r.normalize(f) for f in raw)
    r.substitute(i,3,outputs,'Actual15,124,245 contract by their joint cabled PC lantern','disk_cluster_lantern')
    _witness(r,canonical,chart,canonical_after=canonical_after,
             canonical_outer_daisy=daisy,canonical_R345_daisy=r345_daisy,
             canonical_relation='P15 R134 R345 = O1345 T34: two PC daisies, internal T34 commutation, cyclic start',
             output_presentations=_matches(outputs,_transport(canonical_after,chart)))

    # The positive complement is essential: actual O1245 is sigma3 sigma4 D4,
    # not sigma3 sigma4^-1 D4. The needed transported35 is already present.
    h = reduce_word(p15.word+(3,))
    d4 = Factor('pattern.D4',(),1,4)
    e45 = Factor('pattern.E45',(),4,2)
    minus = Factor('pattern.Ominus',(-4,),1,4)
    plus = Factor('pattern.Oplus',(4,),1,4)
    base = (d4,e45,minus)
    interchange = research_hurwitz_move(base,1,2)
    canonical = (d4,plus,e45)
    interchange_matches = _matches(interchange['factors'],canonical)
    canonical_after = (Factor('return.exterior',(),1,5),Factor('return.inner123',(),1,3))
    if exact_action(product(base),5) != exact_action(product(canonical_after),5):
        raise ValueError('The groups123/4/5 cabled PC lantern failed')
    pair_match = _matches((r.factors[r.position('alternative.return.1')],),_transport(canonical[2:],h))
    r.drag('alternative.return.1','return.O1245',after=True,
           title='Gather the actual transported35 petal along the four-neighbor side')
    i = r.position('alternative.O1234')
    _matches(r.factors[i:i+3],_transport(canonical,h))
    raw = _transport(canonical_after,h)
    outputs = tuple(r.normalize(f) for f in raw)
    r.substitute(i,3,outputs,'Actual two outers and35 petal reach one visible exterior','disk_cluster_lantern')
    _witness(r,canonical,h,canonical_after=canonical_after,
             canonical_cabled_lantern=base,internal_interchange=interchange,
             internal_interchange_matches=interchange_matches,existing_pair_match=pair_match,
             output_presentations=_matches(outputs,raw),
             canonical_relation='Cabled PC lantern D4 E45 Ominus = D5 R123; one retained interchange gives D4 Oplus E45')

    retained = [s for stage in r.stages for s in (stage,)+stage.get('atomic_steps',())]
    checks = []
    for stage in retained:
        fs = stage['factors']
        if any(f.half or f.power != 1 for f in fs):
            raise ValueError('A returned-loan state lost unit positive full twists')
        sphere = sphere_chain_certificate(product(fs)); lift = homology_action(product(fs))
        if not sphere['certified'] or lift != IDENTITY:
            raise ValueError('A retained state lost its sphere/lift certificate')
        checks.append(dict(sphere_certificate=sphere,chosen_lift=lift))
    values = [disk_curve_intersection(a.mapping_class,b.mapping_class,strands=5)
              for i,a in enumerate(r.factors) for b in r.factors[i+1:]]
    kernels = tuple(dict(factor=f,split=split_fixed_last_strand(f.word,5)) for f in r.factors)
    for k in kernels:
        if exact_action(k['factor'].word,5) != exact_action(k['split'].reconstructed_word,5):
            raise ValueError('An endpoint nonabelian reconstruction failed')
    inner = next(f for f in r.factors if f.id=='return.inner123')
    inner_rose = _terms(inner.mapping_class,'next.inner.rose.',pc_rose_terms)
    inner_daisy = _terms(inner.mapping_class,'next.inner.daisy.',pc_daisy_terms)
    current_pair = next(f for f in r.factors if f.id=='return.inner24')
    next_target = dict(actual_root=inner,canonical_rose=inner_rose,canonical_daisy=inner_daisy,
        actual_pair_matches=_matches((current_pair,current_pair),(inner_rose[2],inner_daisy[1])),
        applied=False,requires_transport=True,
        scope='One actual shared petal only. The other petals have not been gathered or substituted; no residual closure follows from this match.')
    return dict(stages=tuple(r.stages),factors=r.factors,graphical_operations=len(r.stages)-1,
        adjacent_checks=sum(s.get('adjacent_moves',0) for s in r.stages),
        internal_named_adjacent_checks=1,source_working_operations=50,working_prefix_operations=59,
        before_score=_score(source),after_score=_score(r.factors),
        peak_support_word=max(_score(s['factors'])['max_support_word'] for s in retained),
        curve_intersections=dict(maximum=max(values),total=sum(values),pairs=len(values)),
        state_sphere_lift_certificates=tuple(checks),endpoint_point_pushing=kernels,
        next_inner_root=next_target,
        source_rose_return_applied=True,visible_exteriors=1,sphere_moves=0,exterior_caps=0,
        complete_proof_steps=99,complete_shorter_derivation=False,public_replay_changed=False,
        scope='Reached outside-loan return and exterior lantern. The working prefix is59, longer than the older first-exterior prefix53. No shorter complete proof or graphical/PDF change is claimed.')
