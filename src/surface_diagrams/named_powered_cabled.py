"""Powered cabled PC lantern with the actual shared inner twist absorbed."""
from dataclasses import replace
from .braid_actions import inverse_word,reduce_word
from .early_alternative_transport import _matches
from .early_boundary_pure import _PositiveReplay,_score
from .factorization_explorer import Factor,product
from .framed_boundary_relations import enclosed_boundaries
from .hyperelliptic_homology import IDENTITY,homology_action
from .mapping_classes import exact_action
from .named_disk_frames import _transport_factor
from .outside_half_lantern import _cyclic_start
from .point_pushing import split_fixed_last_strand
from .six_seven_structure import research_hurwitz_move
from .sphere_actions import sphere_chain_certificate


def powered_cabled_lantern(left_power,right_power,inner_power,*,chart=()):
    """A^m B I^k C^n = A^(m-1) O I^(k+1) C^(n-1).

    The individually matched unit cabled lantern is A B C=O I, and
    the shared inner I commutes with C. Zero remainders are omitted.
    Every power decomposition and the inner/root crossing are retained.
    """
    if any(type(x) is not int or x<1 for x in (left_power,right_power,inner_power)):
        raise ValueError('Use positive integer root and shared-inner multiplicities')
    a=Factor('cabled.A',(-3,),1,3);c=Factor('cabled.C',(),1,3)
    q=Factor('cabled.Q34',(),3,2);outer=Factor('cabled.O',(),1,4);inner=Factor('cabled.I',(),1,2)
    cyclic=(a,c,q);interchange=research_hurwitz_move(cyclic,1,2);a,b,c=interchange['factors']
    if exact_action(product((a,b,c)),5)!=exact_action(outer.word+inner.word,5):
        raise ValueError('The canonical unit cabled PC lantern failed')
    left=replace(a,power=left_power);right=replace(c,power=right_power);shared=replace(inner,power=inner_power)
    canonical_inputs=(left,b,shared,right)
    canonical_outputs=((replace(a,power=left_power-1),) if left_power>1 else ())+(outer,replace(inner,power=inner_power+1))+((replace(c,power=right_power-1),) if right_power>1 else ())
    commute=research_hurwitz_move((shared,c),1,0)
    commute_matches=_matches(commute['factors'],(c,shared))
    left_split=((replace(a,power=left_power-1),) if left_power>1 else ())+(a,)
    right_split=(c,)+((replace(c,power=right_power-1),) if right_power>1 else ())
    inputs=tuple(_transport_factor(f,chart) for f in canonical_inputs)
    outputs=tuple(_transport_factor(f,chart) for f in canonical_outputs)
    if exact_action(product(inputs),5)!=exact_action(product(outputs),5):
        raise ValueError('The powered cabled lantern changed its disk product')
    return dict(common_chart=tuple(chart),canonical_unit_before=cyclic,
        retained_unit_interchange=interchange,unit_inputs=(a,b,c),unit_outputs=(outer,inner),
        canonical_inputs=canonical_inputs,canonical_outputs=canonical_outputs,inputs=inputs,outputs=outputs,
        root_powers=(left_power,right_power),shared_inner_power=inner_power,
        retained_left_decomposition=dict(before=(left,),after=left_split,
            exact_free_word_equality=reduce_word(left.word)==reduce_word(product(left_split))),
        retained_right_decomposition=dict(before=(right,),after=right_split,
            exact_free_word_equality=reduce_word(right.word)==reduce_word(product(right_split))),
        retained_shared_inner_crossing=commute,shared_inner_commutation_matches=commute_matches,
        retained_inner_merge=dict(before=(inner,shared),after=(replace(inner,power=inner_power+1),),
            exact_free_word_equality=reduce_word(inner.word+shared.word)==reduce_word(replace(inner,power=inner_power+1).word)),
        actual_standalone_root_splits=False,actual_standalone_inner_merge=False,
        sphere_moves=0,exterior_caps=0,half_twists=0,inverse_factors=0)


def shorten_powered_cabled_start(stages):
    """Three actual operations replace six, preserving every original half."""
    stages=tuple(stages)
    if len(stages)!=67 or stages[1]['kind']!='disk_split' or stages[6]['kind']!='disk_combine':
        raise ValueError('Use the preserved66-operation early-powered-daisy disk tail')
    source=stages[0]['factors'];by={f.id:f for f in source}
    if by['F13'].power!=2 or by['F4'].power!=2 or by['prefix.P12']!=Factor('prefix.P12',(),1,2):
        raise ValueError('The original squared roots or shared inner factor changed')
    pattern=powered_cabled_lantern(2,2,1,chart=(-4,-4))
    r=_PositiveReplay(source);before=r.factors;moved=before[-1]
    if moved.id!='F13':raise ValueError('The final actual S124 square changed')
    r.factors=r.check(before[-1:]+before[:-1])
    r.record('Cyclic start at the WHOLE original124 square','disk_cyclic_start',
        frame=moved.word,local_before=before,local_after=r.factors,exact_conjugation=True)
    actual=r.factors[:4];input_matches=_matches(actual,pattern['inputs'])
    outputs=(replace(by['F13'],id='alternative.S1',power=1),
        Factor('alternative.O1234',(-4,-4),1,4),Factor('alternative.T12.square',(),1,2,2),
        replace(by['F4'],id='alternative.R2',power=1))
    output_matches=_matches(outputs,pattern['outputs'])
    discrepancy=reduce_word(product(actual)+inverse_word(product(outputs)))
    sphere=sphere_chain_certificate(discrepancy);lift=homology_action(discrepancy)
    if not sphere['certified'] or lift!=IDENTITY:raise ValueError('The powered lantern lost its separate sphere/lift check')
    r.substitute(0,4,outputs,'Powered cabled PC lantern keeps both root squares intact and absorbs12','disk_cluster_lantern')
    normalized=tuple(_transport_factor(f,(4,4)) for f in actual+outputs)
    splits=tuple(split_fixed_last_strand(f.word,5) for f in normalized)
    for f,s in zip(normalized,splits):
        if s.kernel_loop or exact_action(f.word,5)!=exact_action(s.reconstructed_word,5):
            raise ValueError('A normalized actual cabled factor lost its full kernel/shadow')
    r.stages[-1]['named_pattern_witness']=dict(powered_cabled_lantern=pattern,
        individual_matches=input_matches,output_presentation_matches=output_matches,
        every_actual_input_matched=True,normalized_actual_inputs_and_outputs=normalized,
        complete_point_pushing=splits,canonical_normalized_matches=_matches(normalized,pattern['canonical_inputs']+pattern['canonical_outputs']),disk_discrepancy=discrepancy,
        sphere_certificate=sphere,chosen_lift_discrepancy=lift)
    r.stages[-1]['framed_balance_before_minus_after']=tuple(
        sum(f.power for f in actual if j in enclosed_boundaries(f.mapping_class,5))-
        sum(f.power for f in outputs if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6))
    _cyclic_start(r,'alternative.O1234','Cyclic start after the retained actual124 unit')
    if r.factors!=stages[6]['factors']:raise ValueError('The powered prefix failed its literal later join')
    for s in r.stages:
        if tuple(f for f in s['factors'] if f.half)!=tuple(f for f in source if f.half):
            raise ValueError('The powered prefix changed an original half')
    for s in r.stages[1:]:
        if s['kind']=='disk_cyclic_start' and reduce_word(s['frame']+product(s['local_before'])+inverse_word(s['frame']))!=reduce_word(product(s['local_after'])):
            raise ValueError('A cyclic frame failed before presentation changes')
    result=(stages[0],)+tuple(r.stages[1:])+stages[7:]
    for j,s in enumerate(result[1:],1):
        before=product(result[j-1]['factors']);after=product(s['factors'])
        if s['kind'] in ('global_conjugation','disk_cyclic_start'):before=s['frame']+before+inverse_word(s['frame'])
        if exact_action(before,5)!=exact_action(after,5):raise ValueError('A shortened disk transition failed')
    certificates=[]
    for s in r.stages:
        sphere=sphere_chain_certificate(product(s['factors']));lift=homology_action(product(s['factors']))
        if not sphere['certified'] or lift!=IDENTITY:raise ValueError('A retained prefix state lost its chosen lift')
        certificates.append(dict(sphere_certificate=sphere,chosen_lift=lift))
    retained=[a for s in result for a in (s,)+tuple(s.get('atomic_steps',()))]
    return dict(stages=result,factors=result[-1]['factors'],graphical_steps=len(result)-1,
        previous_whole_named_steps=85,whole_named_steps=82,operations_removed=3,
        source_interval=(0,6),replacement_interval=tuple(r.stages),replacement_operations=3,
        previous_operations=6,literal_rejoin=True,original_halves_unchanged=True,
        extension_peak_support_word=max(_score(s['factors'])['max_support_word'] for s in r.stages),
        actual_peak_support_word=max(_score(s['factors'])['max_support_word'] for s in retained),
        adjacent_checks=sum(s.get('adjacent_moves',0) for s in result),
        previous_adjacent_checks=sum(s.get('adjacent_moves',0) for s in stages),
        added_internal_shared_inner_checks=1,state_sphere_lift_certificates=tuple(certificates),
        sphere_moves=0,exterior_caps=0,action_only_boundary_recognitions=0,
        scope='Two explicit cyclic starts surround one powered cabled PC lantern. Both root powers and the shared inner twist enter intact; actual states change and rejoin literally after three operations instead of six. The commuting crossing and power decompositions remain inside the named rule.')
