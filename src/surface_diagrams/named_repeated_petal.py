"""PC daisy extraction with a repeated petal kept as one powered factor.

If a daisy is A Q C = D, then A Q^m C = D (C^-1 Q^(m-1) C).
The unit daisy is matched term by term. The spare positive twist is retained;
no boundary cap, half twist, or inverse twist factor is introduced.
"""
from dataclasses import replace
from .braid_actions import inverse_word, reduce_word
from .early_alternative_transport import _matches
from .early_boundary_pure import _PositiveReplay, _score
from .factorization_explorer import Factor, product
from .framed_boundary_relations import enclosed_boundaries
from .hyperelliptic_homology import IDENTITY, homology_action
from .mapping_classes import exact_action
from .named_disk_frames import _transport_factor
from .point_pushing import split_fixed_last_strand
from .projected_relations import pc_daisy_terms
from .six_seven_structure import research_hurwitz_move
from .sphere_actions import sphere_chain_certificate


def repeated_petal_daisy(outer, petal_index, power, *, interchanges=()):
    """A reusable marked-B5 daisy rule, including its explicit expansion.

    This accepts any unit outer with three to five points and any ordered
    Hurwitz presentation of its PC daisy. Only a pair petal may be repeated.
    The remainder is conjugated by the INVERSE complete suffix, in order.
    """
    if (not isinstance(outer,Factor) or outer.half or outer.power!=1
            or not 3<=outer.points<=5 or outer.first+outer.points-1>5):
        raise ValueError('Use a unit three-to-five-point outer in the marked B5 disk')
    if type(power) is not int or power<2 or type(petal_index) is not int:
        raise ValueError('Choose a petal index and an integer multiplicity at least two')
    canonical=tuple(Factor('repeat.pattern.'+str(i),t.conjugator,t.first,t.points)
                    for i,t in enumerate(pc_daisy_terms(outer.mapping_class)))
    basis=canonical;checks=[]
    for source,target in interchanges:
        move=research_hurwitz_move(basis,source,target)
        checks.append(move);basis=move['factors']
    if not 0<=petal_index<len(basis) or basis[petal_index].points!=2:
        raise ValueError('The repeated term must be an actual pair petal')
    if exact_action(product(basis),5)!=exact_action(outer.word,5):
        raise ValueError('The ordered unit template lost its named PC daisy')
    q=basis[petal_index];inputs=basis[:petal_index]+(replace(q,power=power),)+basis[petal_index+1:]
    suffix=product(basis[petal_index+1:])
    spare=replace(q,id='repeat.spare',power=power-1,
                  conjugator=reduce_word(inverse_word(suffix)+q.conjugator))
    spare=_transport_factor(spare,())
    # Keep the full split and same-ancestry inverse transport as the local
    # expansion of this generic rule, rather than new displayed factors.
    rest=replace(q,id='repeat.spare',power=power-1)
    expanded=inputs[:petal_index]+(q,rest)+inputs[petal_index+1:]
    split=dict(local_before=(inputs[petal_index],),local_after=(q,rest),
        exact_free_word_equality=reduce_word(inputs[petal_index].word)==reduce_word(q.word+rest.word))
    position=petal_index+1;transport=[];state=expanded
    while position<len(state)-1:
        move=research_hurwitz_move(state,position+1,position)
        state=move['factors'];transport.append(move);position+=1
    _matches(state[:-1],basis);spare_match=_matches((state[-1],),(spare,))
    outputs=(_transport_factor(outer,()),spare)
    if exact_action(product(inputs),5)!=exact_action(product(outputs),5):
        raise ValueError('The repeated-petal extraction changed the disk braid')
    return dict(canonical=canonical,basis=basis,inputs=inputs,outputs=outputs,
        outer=outer,petal_index=petal_index,multiplicity=power,suffix=suffix,
        retained_daisy_interchanges=tuple(checks),retained_power_split=split,
        retained_spare_transports=tuple(transport),spare_presentation_match=spare_match,
        formula='A Q^m C = D (C^-1 Q^(m-1) C), where the individually matched PC daisy is A Q C = D',
        inverse_twist_factors=0,half_twists=0,sphere_moves=0,exterior_caps=0)


def shorten_repeated_petal_daisy(stages):
    """Replace the actual powered first daisy by its direct named rule.

    No unit split or separate petal carries occurs in the new replay. The
    canonical generic expansion remains fully retained, and the actual
    complete tuple rejoins the old post-daisy state literally.
    """
    stages=tuple(stages);first,last=63,67
    if len(stages)!=71 or stages[first+1]['kind']!='disk_split' or stages[last]['kind']!='disk_pc_daisy':
        raise ValueError('Use the preserved70-operation positive-frame disk tail')
    source=stages[first]['factors'];by={f.id:f for f in source}
    if by.get('alternative.T12.square') is None or by['alternative.T12.square'].power!=2:
        raise ValueError('The actual squared petal changed')
    old=stages[last]['named_pattern_witness'];chart=tuple(old['common_chart'])
    pattern=repeated_petal_daisy(Factor('repeat.outer',chart,1,5),2,2,
        interchanges=((1,2),(1,2),(4,3),(4,3)))
    r=_PositiveReplay(source);i=r.position('alternative.residual.O1234');actual=r.factors[i:i+5]
    matches=_matches(actual,pattern['inputs'])
    outputs=tuple(replace(f,id=name) for f,name in zip(pattern['outputs'],('direct.exterior.3','direct.E2')))
    discrepancy=reduce_word(product(actual)+inverse_word(product(outputs)))
    sphere=sphere_chain_certificate(discrepancy);lift=homology_action(discrepancy)
    if not sphere['certified'] or lift!=IDENTITY:
        raise ValueError('The direct daisy lost its separate sphere/lift check')
    r.substitute(i,5,outputs,'PC daisy extracts the exterior DIRECTLY from the squared petal','disk_pc_daisy')
    normalized=tuple(_transport_factor(f,inverse_word(chart)) for f in actual)
    splits=tuple(split_fixed_last_strand(f.word,5) for f in normalized[1:])
    for f,s in zip(normalized[1:],splits):
        if s.shadow_word or exact_action(s.reconstructed_word,5)!=exact_action(f.word,5):
            raise ValueError('A powered daisy petal lost its complete kernel')
    stage=r.stages[-1]
    stage['named_pattern_witness']=dict(repeated_petal_pattern=pattern,common_chart=chart,
        individual_matches=matches,every_actual_input_matched=True,
        normalized_actual=normalized,petal_point_pushing=splits,
        disk_discrepancy=discrepancy,sphere_certificate=sphere,chosen_lift_discrepancy=lift,
        actual_powered_petal_split=False,actual_extra_petal_transports=0,
        source_unit_daisy_witness=old)
    stage['framed_balance_before_minus_after']=tuple(
        sum(f.power for f in actual if j in enclosed_boundaries(f.mapping_class,5))-
        sum(f.power for f in outputs if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6))
    if r.factors!=stages[last]['factors']:
        raise ValueError('The direct powered daisy failed its literal later join')
    result=stages[:first+1]+(stage,)+stages[last+1:]
    for j,s in enumerate(result[1:],1):
        before=product(result[j-1]['factors']);after=product(s['factors'])
        if s['kind'] in ('global_conjugation','disk_cyclic_start'):
            before=s['frame']+before+inverse_word(s['frame'])
        if exact_action(before,5)!=exact_action(after,5):
            raise ValueError('The shortened route lost an ordered transition')
    retained=[a for s in result for a in (s,)+s.get('atomic_steps',())]
    return dict(stages=result,factors=result[-1]['factors'],graphical_steps=len(result)-1,
        previous_whole_named_steps=89,whole_named_steps=86,operations_removed=3,
        source_interval=(first,last),literal_rejoin=True,repeated_petal_certificate=stage,
        adjacent_checks=sum(s.get('adjacent_moves',0) for s in result),
        previous_adjacent_checks=sum(s.get('adjacent_moves',0) for s in stages),
        added_internal_spare_transports=len(pattern['retained_spare_transports']),
        actual_peak_support_word=max(_score(s['factors'])['max_support_word'] for s in retained),
        sphere_moves=0,exterior_caps=0,action_only_boundary_recognitions=0,
        scope='One generic PC daisy with a repeated petal bypasses forming two unit factors and separately returning them. Every powered input matches individually; the spare positive twist remains visible. Its full generic split/transport expansion is retained.')
