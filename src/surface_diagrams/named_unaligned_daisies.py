"""Close the two unaligned outer curves by individually matched PC daisies."""
from dataclasses import replace
from .braid_actions import inverse_word, reduce_word
from .early_boundary_pure import _PositiveReplay, _score
from .early_alternative_transport import _matches
from .factorization_explorer import Factor, product
from .framed_boundary_relations import enclosed_boundaries
from .hyperelliptic_homology import IDENTITY, homology_action
from .mapping_classes import exact_action
from .outside_half_lantern import _cyclic_start
from .point_pushing import split_fixed_last_strand
from .projected_relations import pc_daisy_terms
from .six_seven_structure import research_hurwitz_move
from .sphere_actions import sphere_chain_certificate


def _daisy_pattern(moves):
    canonical = tuple(Factor('pattern.daisy.'+str(j),t.conjugator,t.first,t.points)
        for j,t in enumerate(pc_daisy_terms(Factor('pattern.D5',(),1,5).mapping_class)))
    changed=canonical;checks=[]
    for source,target in moves:
        move=research_hurwitz_move(changed,source,target)
        checks.append(move);changed=move['factors']
    return canonical,changed,tuple(checks)


def _contract(replay,index,name,chart,moves,title):
    canonical,changed,checks=_daisy_pattern(moves)
    pattern=tuple(replace(f,conjugator=reduce_word(chart+f.conjugator)) for f in changed)
    actual=replay.factors[index:index+5]
    matches=_matches(actual,pattern)
    discrepancy=reduce_word(product(actual)+inverse_word(Factor(name,(),1,5).word))
    sphere=sphere_chain_certificate(discrepancy);lift=homology_action(discrepancy)
    if not sphere['certified'] or lift!=IDENTITY:raise ValueError('A disk daisy failed its separate sphere/lift check')
    normalized=tuple(replace(f,conjugator=reduce_word(inverse_word(chart)+f.conjugator)) for f in actual)
    splits=tuple(split_fixed_last_strand(f.word,5) for f in normalized[1:])
    for f,s in zip(normalized[1:],splits):
        if s.shadow_word or exact_action(s.reconstructed_word,5)!=exact_action(f.word,5):
            raise ValueError('A normalized petal lost its full nonabelian kernel')
    replay.substitute(index,5,(Factor(name,(),1,5),),title,'disk_pc_daisy')
    replay.stages[-1]['named_pattern_witness']=dict(canonical=canonical,
        common_chart=chart,retained_interchanges=checks,individual_matches=matches,
        normalized_actual=normalized,petal_point_pushing=splits,
        disk_discrepancy=discrepancy,sphere_certificate=sphere,chosen_lift_discrepancy=lift,
        every_actual_input_matched=True)
    replay.stages[-1]['framed_balance_before_minus_after']=tuple(
        sum(f.power for f in actual if j in enclosed_boundaries(f.mapping_class,5))-1 for j in range(1,6))


def close_unaligned_daisies(factors):
    """Eleven positive disk moves replace the previous seventeen-move tail.

    One pair transport rounds the first outer in a joint chart, rather than
    aligning both outers. Four retained internal daisy interchanges match
    its actual petals. The remaining outer stays routed: its four complete
    point-pushing kernels give a seven-interchange daisy, matched in B5.
    Four unit exterior twists remain visible, with no sphere move or cap.
    """
    source=tuple(factors)
    expected=('alternative.second.exterior','alternative.second.I35','alternative.exterior',
        'alternative.residual.O1234','alternative.returned.N','alternative.return.2',
        'alternative.P24','alternative.shared.I25','alternative.T12.square',
        'alternative.shared.1','alternative.shared.2')
    if tuple(f.id for f in source)!=expected:raise ValueError('Use the preserved returned-root endpoint')
    if any(f.half or f.power<1 for f in source):raise ValueError('Use the positive full-twist endpoint')
    r=_PositiveReplay(source);r.stages[0]['title']='The actual returned-root endpoint before outer alignment'
    b=source[5];h=(-4,-3,-2,-1,-1);frame=reduce_word(h+b.word)
    before=r.factors
    r.factors=r.check(tuple(r.normalize(replace(f,conjugator=reduce_word(frame+f.conjugator))) for f in before))
    r.record('Joint hB chart for the FIRST unaligned daisy','global_conjugation',
        frame=frame,local_before=before,local_after=r.factors,exact_conjugation=True)
    r.drag('alternative.second.I35','alternative.residual.O1234',
        title='One actual pair transport makes the first outer round')
    m=r.factors[r.position('alternative.residual.O1234')]
    _matches((m,),(Factor('pattern.D4',(),1,4),))
    r.drag(m.id,'alternative.P24',title='Gather the first outer past four outside neighbors')
    r.split('alternative.T12.square','direct.E1','direct.E2')
    r.drag('alternative.shared.1','direct.E2',title='Keep the23 petal fixed while transporting the extra square unit')
    r.drag('alternative.shared.2','direct.E2',title='Keep the12 petal fixed while returning the extra square unit')
    _contract(r,r.position(m.id),'direct.exterior.3',(),
        ((1,2),(1,2),(4,3),(4,3)),
        'FIRST actual transported PC daisy, before aligning the outer curves')
    _cyclic_start(r,'alternative.returned.N','Cyclic start at the still-routed remaining outer')
    r.drag('direct.exterior.3','alternative.returned.N',title='Commute the third exterior to the front')
    r.drag('alternative.second.I35','direct.E2',after=True,
        title='The final petal passes only the two central exterior twists')
    bh=replace(b,conjugator=reduce_word(h+b.conjugator))
    second_chart=reduce_word(Factor('pattern.D4',(),1,4).word+bh.word)
    _contract(r,r.position('alternative.returned.N'),'direct.exterior.4',second_chart,
        ((1,2),(1,2),(1,2),(1,2),(4,3),(3,2),(2,1)),
        'SECOND actual transported PC daisy, with its outer still routed')
    retained=[a for s in r.stages for a in (s,)+s.get('atomic_steps',())]
    certificates=[]
    for s in retained:
        sphere=sphere_chain_certificate(product(s['factors']));lift=homology_action(product(s['factors']))
        if not sphere['certified'] or lift!=IDENTITY:raise ValueError('A direct closure state lost its sphere/lift check')
        certificates.append(dict(sphere_certificate=sphere,chosen_lift=lift))
    if len(r.stages)!=12 or len(r.factors)!=4 or any(f!=Factor(f.id,(),1,5) for f in r.factors):
        raise ValueError('The direct daisies did not reach four visible standard exteriors')
    return dict(stages=tuple(r.stages),factors=r.factors,graphical_steps=11,
        adjacent_checks=sum(s.get('adjacent_moves',0) for s in r.stages),internal_named_adjacent_checks=11,
        before_score=_score(source),after_score=_score(r.factors),
        actual_peak_support_word=max(_score(s['factors'])['max_support_word'] for s in retained),
        state_sphere_lift_certificates=tuple(certificates),
        common_frame=frame,first_pattern_interchanges=4,second_pattern_interchanges=7,
        four_point_square_created=False,outer_alignment_performed=False,
        sphere_moves=0,exterior_caps=0,action_only_boundary_recognitions=0,
        complete_named_boundary_derivation=True,
        scope='Two individually matched PC daisies close the actual unaligned outers in eleven positive disk operations. All four exterior twists remain visible.')


def shorten_named_daisy_closure(stages):
    """Replace the last17 operations of the98-step proof by11 actual moves."""
    stages=tuple(stages)
    if len(stages)!=80:raise ValueError('Use the preserved79-operation named disk tail')
    positions=[i for i,s in enumerate(stages) if s['title']=='Close the actual returned PC daisy']
    if positions!=[62]:raise ValueError('The returned-root source join changed')
    index=positions[0];closure=close_unaligned_daisies(stages[index]['factors'])
    result=stages[:index+1]+closure['stages'][1:]
    for i,s in enumerate(result[1:],1):
        before=product(result[i-1]['factors']);after=product(s['factors'])
        if s['kind'] in ('global_conjugation','disk_cyclic_start'):
            g=s['frame'];before=g+before+inverse_word(g)
        if exact_action(before,5)!=exact_action(after,5):raise ValueError('The shortened whole disk route failed an ordered transition')
    retained=[a for s in result for a in (s,)+s.get('atomic_steps',())]
    return dict(stages=result,factors=result[-1]['factors'],graphical_steps=len(result)-1,
        previous_whole_named_steps=98,whole_named_steps=92,operations_removed=6,
        previous_remaining_steps=17,replacement_steps=11,preserved_disk_prefix_steps=index,
        adjacent_checks=sum(s.get('adjacent_moves',0) for s in result),
        actual_peak_support_word=max(_score(s['factors'])['max_support_word'] for s in retained),
        direct_closure_certificate=closure,
        sphere_moves=0,action_only_boundary_recognitions=0,
        scope='A six-operation mathematical shortening: two directly matched daisies bypass outer alignment, outer squaring and the old petal-arranging detour.')
