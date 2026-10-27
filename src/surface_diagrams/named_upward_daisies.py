"""Close both daisies from an earlier cyclic cut, keeping the second outer short."""
from dataclasses import replace
from .braid_actions import inverse_word,reduce_word
from .early_boundary_pure import _PositiveReplay,_score
from .early_alternative_transport import _matches
from .factorization_explorer import Factor,product
from .framed_boundary_relations import enclosed_boundaries
from .hyperelliptic_homology import IDENTITY,homology_action
from .mapping_classes import exact_action
from .named_disk_frames import _transport_factor
from .named_expanded_loan import _expanded_rose_pattern,_inverse_outer_up
from .named_unaligned_daisies import _daisy_pattern
from .outside_half_lantern import _cyclic_start
from .point_pushing import split_fixed_last_strand
from .six_seven_structure import research_hurwitz_move
from .sphere_actions import sphere_chain_certificate


def _substitution(replay,index,count,outputs,title,kind,witness):
    actual=replay.factors[index:index+count]
    discrepancy=reduce_word(product(actual)+inverse_word(product(outputs)))
    sphere=sphere_chain_certificate(discrepancy);lift=homology_action(discrepancy)
    if not sphere['certified'] or lift!=IDENTITY:raise ValueError('The disk substitution failed its separate sphere/lift check')
    replay.substitute(index,count,outputs,title,kind)
    replay.stages[-1]['named_pattern_witness']=dict(witness,disk_discrepancy=discrepancy,
        sphere_certificate=sphere,chosen_lift_discrepancy=lift,every_actual_input_matched=True)
    replay.stages[-1]['framed_balance_before_minus_after']=tuple(
        sum(f.power for f in actual if j in enclosed_boundaries(f.mapping_class,5))-
        sum(f.power for f in outputs if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6))


def _daisy(replay,index,chart,moves,shift,name,title):
    canonical,changed,checks=_daisy_pattern(moves)
    rotated=changed[shift:]+changed[:shift]
    internal_frame=inverse_word(product(changed[:shift]))
    if reduce_word(internal_frame+product(changed)+inverse_word(internal_frame))!=reduce_word(product(rotated)):
        raise ValueError('The internal daisy cyclic start failed its free-word equality')
    pattern=tuple(_transport_factor(f,chart) for f in rotated)
    actual=replay.factors[index:index+5];matches=_matches(actual,pattern)
    normalized=tuple(_transport_factor(f,inverse_word(chart)) for f in actual)
    petals=tuple(f for f in normalized if f.points==2)
    splits=tuple(split_fixed_last_strand(f.word,5) for f in petals)
    if len(petals)!=4:raise ValueError('The daisy must retain four actual point-pushing petals')
    for f,s in zip(petals,splits):
        if s.shadow_word or exact_action(s.reconstructed_word,5)!=exact_action(f.word,5):
            raise ValueError('An actual daisy petal lost its complete nonabelian kernel')
    outer=Factor(name,(),1,5)
    if exact_action(internal_frame+outer.word+inverse_word(internal_frame),5)!=exact_action(outer.word,5):
        raise ValueError('The canonical daisy exterior was not central')
    _substitution(replay,index,5,(outer,),title,'disk_pc_daisy',dict(canonical=canonical,
        common_chart=chart,retained_interchanges=checks,individual_matches=matches,
        internal_cyclic_start=dict(shift=shift,frame=internal_frame,local_before=changed,
            local_after=rotated,exact_free_word_conjugation=True,canonical_exterior_preserved=True),
        normalized_actual=normalized,petal_point_pushing=splits))


def close_upward_daisies(factors):
    """Fourteen positive operations replace the previous fifteen, with peak18.

    A positive T45 frame bounds the unreordered loan return. An earlier
    cyclic cut lets the first outer travel UP through its own petals,
    instead of dragging it through the second outer. The second daisy is
    matched in its actual cyclic order. No outside-root spike is hidden.
    """
    source=tuple(factors)
    expected=('alternative.second.exterior','alternative.second.I35','alternative.second.I24',
        'alternative.P13','alternative.exterior','alternative.residual.O1234',
        'alternative.residual.I12','alternative.return.2','alternative.second.loan.1',
        'alternative.second.loan.2','alternative.second.loan.3','alternative.P24',
        'alternative.shared.I25','alternative.T12.square','alternative.shared.1','alternative.shared.2')
    if tuple(f.id for f in source)!=expected or any(f.half or f.power<1 for f in source):
        raise ValueError('Use the preserved positive second-exterior endpoint')
    if source[6]!=Factor(source[6].id,(),4,2):raise ValueError('The actual T45 frame supplier changed')
    frame=source[6].word;old_joint=(-4,-3,-2);b=source[7]
    r=_PositiveReplay(source);r.stages[0]['title']='The second-exterior endpoint before the upward-daisy shortcut'
    r.factors=r.check(tuple(_transport_factor(f,frame) for f in source))
    r.record('Positive T45 common frame bounds the unreordered loan return','global_conjugation',
        frame=frame,local_before=source,local_after=r.factors,exact_conjugation=True)
    r.drag('alternative.exterior','alternative.second.I35',title='Commute the exterior out of the expanded loan')
    _inverse_outer_up(r,'alternative.residual.O1234','alternative.second.I35')
    r.drag(b.id,'alternative.second.loan.3',title='Return the12 petal through the three actual loan petals')
    template=_expanded_rose_pattern();interchange=research_hurwitz_move(template['expanded'][:3],0,1)
    terms=interchange['factors']+template['expanded'][3:]
    rose_chart=reduce_word(frame+b.word+(2,3,4,-2,-1,-3))
    pattern=tuple(_transport_factor(f,rose_chart) for f in terms);i=r.position('alternative.second.I24')
    matches=_matches(r.factors[i:i+6],pattern)
    output=_transport_factor(Factor('alternative.returned.N',(1,),2,4),frame)
    output_match=_matches((output,),(_transport_factor(template['outer'],rose_chart),))
    _substitution(r,i,6,(output,),'Expanded PC rose returns the loan WITHOUT a petal reorder',
        'disk_pc_rose',dict(template=template,retained_interchanges=(interchange,),common_chart=rose_chart,
            individual_matches=matches,output_presentation_match=output_match,
            actual_temporary_three_point_factor_created=False))
    outer=r.factors[r.position('alternative.residual.O1234')]
    chart=reduce_word(inverse_word(outer.word)+frame+inverse_word(old_joint))
    _cyclic_start(r,b.id,'Cyclic start BEFORE gathering the first daisy')
    r.drag(outer.id,'alternative.shared.I25',title='Carry the SAME outer UP through its first-daisy petals')
    r.split('alternative.T12.square','direct.E1','direct.E2')
    r.drag('alternative.shared.1','direct.E2',title='Keep the23 petal fixed while returning the extra square unit')
    r.drag('alternative.shared.2','direct.E2',title='Keep the12 petal fixed while returning the extra square unit')
    _daisy(r,r.position(outer.id),chart,((1,2),(1,2),(4,3),(4,3)),0,'direct.exterior.3',
        'FIRST actual PC daisy after the upward outer transport')
    _cyclic_start(r,'direct.exterior.3','Cyclic start at the NEW visible exterior')
    r.drag('direct.E2','alternative.exterior',title='The extra petal passes DOWN past two central exteriors')
    h=(-4,-3,-2,-1,-1);bh=replace(b,conjugator=reduce_word(h+b.conjugator))
    second_chart=reduce_word(chart+Factor('pattern.D4',(),1,4).word+bh.word)
    _daisy(r,r.position('direct.E2'),second_chart,((1,2),(1,2),(1,2),(1,2),(4,3),(3,2),(2,1)),3,
        'direct.exterior.4','SECOND actual PC daisy in its reached cyclic order')
    retained=[a for s in r.stages for a in (s,)+s.get('atomic_steps',())];certificates=[]
    for s in retained:
        sphere=sphere_chain_certificate(product(s['factors']));lift=homology_action(product(s['factors']))
        if not sphere['certified'] or lift!=IDENTITY:raise ValueError('An upward-daisy state lost its separate sphere/lift check')
        certificates.append(dict(sphere_certificate=sphere,chosen_lift=lift))
    if len(r.stages)!=15 or len(r.factors)!=4 or any(f!=Factor(f.id,(),1,5) for f in r.factors):
        raise ValueError('The upward daisies did not reach four visible standard exteriors')
    return dict(stages=tuple(r.stages),factors=r.factors,graphical_steps=14,
        adjacent_checks=sum(s.get('adjacent_moves',0) for s in r.stages),internal_named_adjacent_checks=12,
        state_sphere_lift_certificates=tuple(certificates),common_frame=frame,
        before_score=_score(source),after_score=_score(r.factors),
        actual_peak_support_word=max(_score(s['factors'])['max_support_word'] for s in retained),
        temporary_three_point_factors=0,four_point_square_created=False,outer_alignment_performed=False,
        sphere_moves=0,exterior_caps=0,action_only_boundary_recognitions=0,
        scope='An earlier cyclic cut and an upward outer transport avoid conjugating the second outer. Both actual daisies match individually, including the second cyclic order. Four exterior units stay visible.')


def shorten_named_upward_daisies(stages):
    """Replace the91-proof's final15 disk operations by14 reached moves."""
    stages=tuple(stages)
    if len(stages)!=73 or stages[57]['title']!='Cabled PC lantern reaches a SECOND visible exterior twist':
        raise ValueError('Use the preserved72-operation named disk tail')
    closure=close_upward_daisies(stages[57]['factors']);result=stages[:58]+closure['stages'][1:]
    for i,s in enumerate(result[1:],1):
        before=product(result[i-1]['factors']);after=product(s['factors'])
        if s['kind'] in ('global_conjugation','disk_cyclic_start'):
            g=s['frame'];before=g+before+inverse_word(g)
        if exact_action(before,5)!=exact_action(after,5):raise ValueError('The shortened disk tail failed an ordered equality')
        if i>57 and s['kind']=='disk_cyclic_start' and reduce_word(before)!=reduce_word(after):
            raise ValueError('An explicit cyclic cut failed its free-word equality')
    retained=[a for s in result for a in (s,)+s.get('atomic_steps',())]
    return dict(stages=result,factors=result[-1]['factors'],graphical_steps=len(result)-1,
        previous_whole_named_steps=91,whole_named_steps=90,operations_removed=1,
        previous_remaining_steps=15,replacement_steps=14,preserved_disk_prefix_steps=57,
        adjacent_checks=sum(s.get('adjacent_moves',0) for s in result),
        previous_adjacent_checks=sum(s.get('adjacent_moves',0) for s in stages),
        actual_peak_support_word=max(_score(s['factors'])['max_support_word'] for s in retained),
        upward_closure_certificate=closure,sphere_moves=0,action_only_boundary_recognitions=0,
        scope='One operation and two external adjacent checks removed by an earlier cyclic start, an upward first outer transport and the second daisy in its actual cyclic order.')
