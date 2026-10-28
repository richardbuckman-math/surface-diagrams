"""Expand a squared root earlier and carry its actual daisy petals together."""
from dataclasses import replace
from .braid_actions import inverse_word, reduce_word
from .early_alternative_transport import _matches, _terms
from .early_boundary_pure import _PositiveReplay, _score
from .factorization_explorer import Factor, product
from .framed_boundary_relations import enclosed_boundaries
from .hyperelliptic_homology import IDENTITY, homology_action
from .mapping_classes import exact_action
from .named_disk_frames import _transport_factor
from .outside_half_lantern import _cyclic_start
from .point_pushing import split_fixed_last_strand
from .sphere_actions import sphere_chain_certificate


def partial_powered_daisy(square, *, internal_frame=(), retained_id='partial.root', prefix='partial.petal.'):
    """Expand one unit of C^m, keeping C^(m-1) as a positive factor.

    An optional internal common frame must preserve the actual unit outer.
    Every parent and output is checked separately; m is not restricted to2.
    """
    if (not isinstance(square,Factor) or square.half or type(square.power) is not int
            or square.power<2 or not 3<=square.points<=5 or square.first+square.points-1>5):
        raise ValueError('Use a positive powered three-to-five-point full twist')
    unit=replace(square,power=1)
    parent=replace(unit,conjugator=reduce_word(tuple(internal_frame)+unit.conjugator))
    parent_match=_matches((parent,),(unit,))
    raw=_terms(parent.mapping_class,prefix)
    petals=tuple(_transport_factor(f,()) for f in raw)
    retained=replace(unit,id=retained_id,power=square.power-1)
    outputs=(retained,)+petals
    if exact_action(square.word,5)!=exact_action(product(outputs),5):
        raise ValueError('The partial daisy changed the powered disk class')
    unit_remainder=replace(unit,id=retained_id,power=square.power-1)
    split_after=(unit_remainder,replace(unit,id='partial.expanded.unit'))
    return dict(input=square,unit_parent=parent,internal_frame=tuple(internal_frame),
        parent_match=parent_match,powered_input_match=_matches((square,),(replace(parent,power=square.power),)),
        outputs=outputs,raw_daisy_terms=raw,individual_petal_matches=_matches(petals,raw),
        retained_power_decomposition=dict(local_before=(square,),local_after=split_after,
            exact_free_word_equality=reduce_word(square.word)==reduce_word(product(split_after))),
        actual_standalone_power_split=False,
        output_point_pushing=tuple(dict(factor=f,split=split_fixed_last_strand(f.word,5)) for f in outputs),
        sphere_moves=0,exterior_caps=0)


def shorten_early_powered_daisy(stages):
    """Replace nine operations by eight, with an exact literal later join."""
    stages=tuple(stages);first,last=20,29
    if len(stages)!=68 or stages[first+1]['kind']!='disk_split' or stages[last]['kind']!='disk_pc_daisy':
        raise ValueError('Use the preserved67-operation repeated-petal disk tail')
    source=stages[first]['factors'];by={f.id:f for f in source}
    square=by['F12'];q=by['alternative.T12.square']
    if square.power!=2 or q!=Factor(q.id,(),1,2,2):
        raise ValueError('The actual F12 square or roundT12 square changed')
    pattern=partial_powered_daisy(square,internal_frame=q.word,
        retained_id='alternative.F12.1',prefix='alternative.next.')
    r=_PositiveReplay(source);i=r.position(square.id)
    r.substitute(i,1,pattern['outputs'],'Partial PC daisy exposes the squared root petals EARLY','disk_pc_daisy')
    stage=r.stages[-1];discrepancy=reduce_word(square.word+inverse_word(product(pattern['outputs'])))
    sphere=sphere_chain_certificate(discrepancy);lift=homology_action(discrepancy)
    if not sphere['certified'] or lift!=IDENTITY:raise ValueError('The partial daisy lost its separate sphere/lift check')
    stage['named_pattern_witness']=dict(partial_powered_daisy=pattern,
        every_actual_input_matched=True,disk_discrepancy=discrepancy,
        sphere_certificate=sphere,chosen_lift_discrepancy=lift)
    stage['framed_balance_before_minus_after']=tuple(
        sum(f.power for f in (square,) if j in enclosed_boundaries(f.mapping_class,5))-
        sum(f.power for f in pattern['outputs'] if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6))
    r.drag('alternative.F12.1','F11',title='One C12 root shortens F11')
    _cyclic_start(r,'alternative.R2','Cyclic start after BOTH the square and its commuting outer')
    r.drag(q.id,'F11',title='One short-side square drag carries ALL THREE early daisy petals')
    if r.stages[-1]['adjacent_moves']!=5:raise ValueError('Retain all five square crossings')
    before=r.factors;frame=(4,)
    r.factors=r.check(tuple(_transport_factor(f,frame) for f in before))
    r.record('The same composed sigma4 common frame','global_conjugation',frame=frame,
        local_before=before,local_after=r.factors,exact_conjugation=True)
    r.drag('alternative.F12.1','F10.2',title='Reorder C12 before the matching-half gather')
    r.drag('F11','F6',after=True,title='Gather the final matching original halves')
    r.combine('F6','F11','alternative.P24')
    late=stages[last]
    late_matches=_matches(tuple(r.factors[r.position(f.id)] for f in pattern['outputs'][1:]),late['local_after'])
    if r.factors!=late['factors']:raise ValueError('The early actual petals failed the literal later join')
    result=stages[:first+1]+tuple(r.stages[1:])+stages[last+1:]
    for j,s in enumerate(result[1:],1):
        before=product(result[j-1]['factors']);after=product(s['factors'])
        if s['kind'] in ('global_conjugation','disk_cyclic_start'):
            before=s['frame']+before+inverse_word(s['frame'])
        if exact_action(before,5)!=exact_action(after,5):raise ValueError('A shortened transition failed its ordered disk check')
    retained=[a for s in r.stages for a in (s,)+tuple(s.get('atomic_steps',()))];certificates=[]
    for s in retained:
        sphere=sphere_chain_certificate(product(s['factors']));lift=homology_action(product(s['factors']))
        if not sphere['certified'] or lift!=IDENTITY:raise ValueError('An early petal state lost its sphere/lift check')
        certificates.append(dict(sphere_certificate=sphere,chosen_lift=lift))
    all_states=[a for s in result for a in (s,)+tuple(s.get('atomic_steps',()))]
    return dict(stages=result,factors=result[-1]['factors'],graphical_steps=len(result)-1,
        previous_whole_named_steps=86,whole_named_steps=85,operations_removed=1,
        source_interval=(first,last),replacement_operations=8,previous_operations=9,
        late_petal_point_pushing=tuple(dict(factor=m['actual'],split=split_fixed_last_strand(m['actual'].word,5)) for m in late_matches),
        replacement_interval=tuple(r.stages),literal_rejoin=True,late_individual_petal_matches=late_matches,
        extension_peak_support_word=max(_score(s['factors'])['max_support_word'] for s in retained),
        actual_peak_support_word=max(_score(s['factors'])['max_support_word'] for s in all_states),
        adjacent_checks=sum(s.get('adjacent_moves',0) for s in result),
        previous_adjacent_checks=sum(s.get('adjacent_moves',0) for s in stages),
        changed_state_sphere_lift_certificates=tuple(certificates),sphere_moves=0,exterior_caps=0,
        action_only_boundary_recognitions=0,
        scope='One partial PC daisy is applied before the square transport. Three actual petals replace the donor root throughout the changed interval; all five square crossings remain, and the tuple rejoins literally. One fewer named operation with two more external adjacent checks.')
