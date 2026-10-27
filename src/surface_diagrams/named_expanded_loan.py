"""Return the loan as an expanded six-pair PC rose, without a temporary root."""
from dataclasses import replace
from .braid_actions import inverse_word, reduce_word
from .early_boundary_pure import _PositiveReplay, _score
from .early_alternative_transport import _matches
from .factorization_explorer import Factor, product
from .framed_boundary_relations import enclosed_boundaries
from .hyperelliptic_homology import IDENTITY, homology_action
from .mapping_classes import exact_action
from .projected_relations import pc_daisy_terms, pc_rose_terms
from .six_seven_structure import research_hurwitz_move
from .sphere_actions import sphere_chain_certificate


def _inverse_outer_up(replay,name,target):
    """One continuously transported outer, conjugated by each crossed petal.

    The neighboring petal is the fixed side of each retained ordinary
    Hurwitz move. The SAME outer ancestry moves upward at every check.
    This is the inverse orientation of _PositiveReplay.drag's fixed-factor
    transport, not three unrelated moves relabeled as one.
    """
    atoms=[]
    while replay.position(name)>replay.position(target):
        right=replay.position(name);before=replay.factors[right]
        move=research_hurwitz_move(replay.factors,right-1,right)
        factors=list(move['factors']);factors[right-1]=replay.normalize(factors[right-1])
        replay.factors=replay.check(tuple(factors));after=replay.factors[right-1]
        if after.id!=name:raise ValueError('Inverse transport lost the outer ancestry')
        atoms.append(dict(move,factors=replay.factors,transported_before=before,transported_after=after))
    if not atoms:raise ValueError('The inverse outer transport must cross a neighbor')
    replay.record('Inverse Hurwitz transport of the SAME outer past three petals',
        'disk_hurwitz_block',adjacent_moves=len(atoms),atomic_steps=tuple(atoms),
        moving_factor=name,inverse_hurwitz_transport=True)


def _expanded_rose_pattern():
    outer=Factor('pattern.D4',(),1,4)
    daisy=tuple(Factor('pattern.daisy.'+str(i),t.conjugator,t.first,t.points)
        for i,t in enumerate(pc_daisy_terms(outer.mapping_class)))
    canonical_rose=tuple(Factor('pattern.rose.'+str(i),t.conjugator,t.first,t.points)
        for i,t in enumerate(pc_rose_terms(daisy[0].mapping_class)))
    inner_chart=(1,-2,-2)
    inner=tuple(replace(f,conjugator=reduce_word(inner_chart+f.conjugator)) for f in canonical_rose)
    if exact_action(inner_chart+daisy[0].word+inverse_word(inner_chart),5)!=exact_action(daisy[0].word,5):
        raise ValueError('The nested chart changed its three-point outer')
    if exact_action(product(inner),5)!=exact_action(daisy[0].word,5):
        raise ValueError('The nested PC rose failed')
    expanded=inner+daisy[1:]
    if exact_action(product(expanded),5)!=exact_action(outer.word,5):
        raise ValueError('The expanded four-point PC rose failed')
    return dict(outer=outer,parent_daisy=daisy,canonical_inner_rose=canonical_rose,
        inner_chart=inner_chart,inner_outer_preserved=True,expanded=expanded,
        relation='PC daisy whose three-point prefix is expanded by its internally transported PC rose')


def return_expanded_loan(factors):
    """Six positive operations replace the previous seven, with peak20.

    A petal reorder bounds a single inverse outer transport. All SIX actual
    pairs then match an expanded PC rose. No temporary three-point factor
    is constructed. The common chart is delayed until this contraction.
    """
    source=tuple(factors)
    expected=('alternative.second.exterior','alternative.second.I35','alternative.second.I24',
        'alternative.P13','alternative.exterior','alternative.residual.O1234',
        'alternative.residual.I12','alternative.return.2','alternative.second.loan.1',
        'alternative.second.loan.2','alternative.second.loan.3','alternative.P24',
        'alternative.shared.I25','alternative.T12.square','alternative.shared.1','alternative.shared.2')
    if tuple(f.id for f in source)!=expected:raise ValueError('Use the preserved second-exterior endpoint')
    if any(f.half or f.power<1 for f in source):raise ValueError('Use the positive full-twist endpoint')
    r=_PositiveReplay(source);r.stages[0]['title']='The second-exterior endpoint before reconstructing the loan'
    q=source[7]
    r.drag('alternative.exterior','alternative.second.I35',
        title='Commute the exterior out of the three-petal loan')
    r.drag('alternative.P13','alternative.second.I24',
        title='Reorder the actual loan petals to bound the outer transport')
    _inverse_outer_up(r,'alternative.residual.O1234','alternative.second.I35')
    r.drag(q.id,'alternative.second.loan.3',title='Return the12 petal through the three actual loan petals')
    template=_expanded_rose_pattern()
    chart=reduce_word(q.word+(2,3,4,-2,-1,-3))
    pattern=tuple(replace(f,conjugator=reduce_word(chart+f.conjugator)) for f in template['expanded'])
    i=r.position('alternative.P13');actual=r.factors[i:i+6];matches=_matches(actual,pattern)
    raw_outer=replace(template['outer'],conjugator=chart)
    outer=Factor('alternative.returned.N',(1,),2,4)
    output_match=_matches((outer,),(raw_outer,))
    discrepancy=reduce_word(product(actual)+inverse_word(outer.word))
    sphere=sphere_chain_certificate(discrepancy);lift=homology_action(discrepancy)
    if not sphere['certified'] or lift!=IDENTITY:raise ValueError('The disk rose failed its sphere/lift discrepancy')
    r.substitute(i,6,(outer,),
        'Expanded PC ROSE closes six actual pairs without reconstructing the loan root','disk_pc_rose')
    r.stages[-1]['named_pattern_witness']=dict(template=template,common_chart=chart,
        individual_matches=matches,output_presentation_match=output_match,
        disk_discrepancy=discrepancy,sphere_certificate=sphere,chosen_lift_discrepancy=lift,
        actual_temporary_three_point_factor_created=False)
    r.stages[-1]['framed_balance_before_minus_after']=tuple(
        sum(f.power for f in actual if j in enclosed_boundaries(f.mapping_class,5))-
        int(j in enclosed_boundaries(outer.mapping_class,5)) for j in range(1,6))
    frame=(-4,-3,-2);before=r.factors
    r.factors=r.check(tuple(r.normalize(replace(f,conjugator=reduce_word(frame+f.conjugator))) for f in before))
    r.record('Joint chart AFTER contracting the expanded rose','global_conjugation',
        frame=frame,local_before=before,local_after=r.factors,exact_conjugation=True)
    retained=[a for s in r.stages for a in (s,)+s.get('atomic_steps',())]
    certificates=[]
    for s in retained:
        sphere=sphere_chain_certificate(product(s['factors']));lift=homology_action(product(s['factors']))
        if not sphere['certified'] or lift!=IDENTITY:raise ValueError('A retained rose-return state lost its sphere/lift check')
        certificates.append(dict(sphere_certificate=sphere,chosen_lift=lift))
        if any(f.points==3 for f in s['factors']):raise ValueError('A temporary loan root was reconstructed')
    return dict(stages=tuple(r.stages),factors=r.factors,graphical_steps=len(r.stages)-1,
        adjacent_checks=sum(s.get('adjacent_moves',0) for s in r.stages),
        actual_peak_support_word=max(_score(s['factors'])['max_support_word'] for s in retained),
        state_sphere_lift_certificates=tuple(certificates),before_score=_score(source),after_score=_score(r.factors),
        sphere_moves=0,exterior_caps=0,temporary_three_point_factors=0,
        scope='An actual inverse outer transport and one six-pair nested PC rose replace temporary three-point reconstruction. One fewer operation, with one additional adjacent Hurwitz check.')


def shorten_expanded_loan_return(stages):
    """Splice six reached operations into the complete92 proof, producing91."""
    stages=tuple(stages)
    if len(stages)!=74 or stages[57]['title']!='Cabled PC lantern reaches a SECOND visible exterior twist':
        raise ValueError('Use the preserved73-operation named disk tail')
    replacement=return_expanded_loan(stages[57]['factors'])
    if replacement['factors']!=stages[64]['factors']:
        raise ValueError('The expanded rose failed its literal later join')
    result=stages[:58]+replacement['stages'][1:]+stages[65:]
    for i,s in enumerate(result[1:],1):
        before=product(result[i-1]['factors']);after=product(s['factors'])
        if s['kind'] in ('disk_cyclic_start','global_conjugation'):
            g=s['frame'];before=g+before+inverse_word(g)
        if exact_action(before,5)!=exact_action(after,5):raise ValueError('The shortened full disk tail lost an ordered equality')
    retained=[a for s in result for a in (s,)+s.get('atomic_steps',())]
    return dict(stages=result,factors=result[-1]['factors'],graphical_steps=len(result)-1,
        previous_whole_named_steps=92,whole_named_steps=91,operations_removed=1,
        source_interval=(57,64),previous_interval_steps=7,replacement_steps=6,literal_rejoin=True,
        adjacent_checks=sum(s.get('adjacent_moves',0) for s in result),
        previous_adjacent_checks=sum(s.get('adjacent_moves',0) for s in stages),
        actual_peak_support_word=max(_score(s['factors'])['max_support_word'] for s in retained),
        replacement_certificate=replacement,sphere_moves=0,action_only_boundary_recognitions=0,
        scope='One actual operation removed by avoiding a temporary three-point factor, with all six nested-rose input matches and inverse-Hurwitz checks retained.')
