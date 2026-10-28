"""Post-combine positive branch: two actual rose loans reach a visible exterior.

This is a separate research route, not a replacement for the solved clarity
presentation. It does not cap or silently discard the exterior's -I lift.
"""
from dataclasses import replace
from .braid_actions import inverse_word,reduce_word
from .early_boundary_pure import _PositiveReplay,_score
from .factorization_explorer import Factor,product
from .framed_boundary_relations import enclosed_boundaries
from .hyperelliptic_homology import IDENTITY,homology_action
from .mapping_classes import exact_action
from .named_repeated_petal import repeated_petal_daisy
from .named_powered_cabled import powered_cabled_lantern
from .outside_rose_return import _terms,_transport,_witness
from .outside_half_lantern import _matches
from .point_pushing import split_fixed_last_strand
from .projected_relations import pc_rose_terms,pc_daisy_terms
from .puncture_boundary import BOUNDARY_WORD
from .six_seven_structure import research_hurwitz_move
from .sphere_actions import sphere_chain_certificate


def _cyclic(r,name):
    before=r.factors;i=r.position(name);frame=inverse_word(product(before[:i]))
    r.factors=r.check(before[i:]+before[:i])
    raw=reduce_word(frame+product(before)+inverse_word(frame)+inverse_word(product(r.factors)))
    if raw:raise ValueError('Retain the complete raw cyclic common conjugation')
    r.record('Cyclic start at '+name,'disk_cyclic_start',frame=frame,raw_cyclic_discrepancy=raw)


def _outputs(r,canonical,chart=()):
    r.stages[-1]['named_pattern_witness']['individual_output_matches']=_matches(r.stages[-1]['local_after'],_transport(canonical,chart))


def expose_posthalf_exterior(factors):
    """Fourteen reached positive disk operations; no new half or sphere move.

    The actual combined pair and squared pair enter a repeated-petal PC rose.
    A second actual R145 rose supplies45; its first petal matches the spare.
    Two matched cabled lanterns and return of the original12 loan reach one
    standard exterior. The45 supplier is still expanded at the endpoint.
    """
    source=tuple(factors);r=_PositiveReplay(source)
    if len(source)!=16 or any(f.half for f in source) or source[0]!=Factor('alternative.R2',(),1,3):
        raise ValueError('Use the saved source85 index43, after the actual half combine')
    if tuple(f.id for f in source[12:14])!=('alternative.P24','alternative.T12.square'):
        raise ValueError('The actual adjacent combined pair and square changed')
    r.stages[0]['title']='Post-combine lower meeting, before the old full-pair carry'
    canonical_root=Factor('pattern.R123',(),1,3)
    donor=source[0];loan=_terms(donor.mapping_class,'posthalf.loan.',pc_rose_terms)
    root=Factor('posthalf.R125',(-4,-3,-1,2,1),1,3)
    repeated=repeated_petal_daisy(root,1,2,interchanges=((1,2),))
    _matches(source[12:14],repeated['inputs'][:2]);_matches(loan[:1],repeated['inputs'][2:])
    r.substitute(0,1,loan,'Actual round123 PC rose lends the missing round12','disk_pc_rose')
    _witness(r,(canonical_root,),canonical_rose=pc_rose_terms(canonical_root.mapping_class))
    _outputs(r,pc_rose_terms(canonical_root.mapping_class))
    _cyclic(r,'posthalf.loan.1')
    r.drag('posthalf.loan.0','alternative.T12.square',after=True,title='Carry12 UP past two commuting roots to the actual repeated petals')
    i=r.position('alternative.P24');_matches(r.factors[i:i+3],repeated['inputs'])
    outputs=tuple(replace(t,id='posthalf.output.'+str(j)) for j,t in enumerate(repeated['outputs']))
    r.substitute(i,3,outputs,'Actual combined pair and squared pair contract by the repeated-petal PC rose','disk_pc_daisy')
    _witness(r,repeated['inputs'],repeated_petal_certificate=repeated,pattern_chart=root.conjugator)
    _outputs(r,repeated['outputs'])
    repeated_endpoint=r.factors

    supplier=r.factors[r.position('alternative.F12.1')]
    q45=Factor('pattern.round45',(),4,2)
    normalized_q=replace(q45,conjugator=inverse_word(supplier.conjugator))
    split5=split_fixed_last_strand(normalized_q.word,5);split4=split_fixed_last_strand(split5.shadow_word,4)
    if split5.kernel_loop or split4.kernel_loop or exact_action(split4.shadow_word,3)!=exact_action((-1,-1,2,2,1,1),3):
        raise ValueError('Keep BOTH full splits locating the supplier petal in B3')
    if exact_action(split5.reconstructed_word,5)!=exact_action(normalized_q.word,5) or exact_action(split4.reconstructed_word,4)!=exact_action(split5.shadow_word,4):
        raise ValueError('The normalized45 must retain both exact reconstructions')
    chart=reduce_word(supplier.conjugator+(-1,-1));parent=replace(supplier,conjugator=chart)
    _matches((supplier,),(parent,))
    supplied=_terms(parent.mapping_class,'posthalf.supply.',pc_rose_terms)
    spare=r.factors[r.position('posthalf.output.1')]
    _matches(supplied[:1],(spare,));_matches(supplied[2:],(q45,))
    r.substitute(r.position(supplier.id),1,supplied,'The actual145 PC rose lends45 and retains its matched spare petal','disk_pc_rose')
    _witness(r,(canonical_root,),chart,canonical_rose=pc_rose_terms(canonical_root.mapping_class),actual_supplier=supplier,internal_parent_match=_matches((supplier,),(parent,)),matched_spare=_matches(supplied[:1],(spare,)),normalized45=normalized_q,normalized45_split5=split5,normalized45_split4=split4)
    _outputs(r,pc_rose_terms(canonical_root.mapping_class),chart)
    r.drag('posthalf.supply.2','alternative.F12.2',title='Carry supplied45 DOWN through four neighbors')
    r.drag('posthalf.output.0','posthalf.output.1',title='Commute the changed125 root past its interior spare')
    unit=powered_cabled_lantern(1,1,1);g=(4,4,-3,-4);i=r.position('posthalf.output.0')
    _matches(r.factors[i:i+3],_transport(unit['canonical_unit_before'],g))
    outputs=(Factor('posthalf.O1245',(-3,-4),1,4),Factor('posthalf.inner12',(),1,2))
    r.substitute(i,3,outputs,'Actual125,124,45 cabled PC lantern returns the round12 loan','disk_cluster_lantern')
    _witness(r,unit['canonical_unit_before'],g,canonical_unit_interchange=unit['retained_unit_interchange'],canonical_outputs=unit['unit_outputs'])
    _outputs(r,unit['unit_outputs'],g)
    _cyclic(r,'posthalf.inner12')
    r.drag('posthalf.inner12','alternative.O1234',title='Return12 across its commuting old outer')
    i=r.position('posthalf.inner12');restored=Factor('posthalf.return.R123',(),1,3)
    restore=pc_rose_terms(restored.mapping_class);_matches(r.factors[i:i+3],restore)
    r.substitute(i,3,(restored,),'The SAME12 loan restores its original123 donor','disk_pc_rose')
    _witness(r,restore,restored_original_donor=_matches((restored,),(donor,)))
    _outputs(r,(canonical_root,))
    _cyclic(r,'posthalf.O1245')
    r.drag('alternative.prepare.345.0','alternative.O1234',after=True,title='Gather actual round34 UP across two roots')

    d4=Factor('pattern.D4',(),1,4);e45=Factor('pattern.E45',(),4,2);minus=Factor('pattern.Ominus',(-4,),1,4)
    d5=Factor('pattern.D5',(),1,5);inside=Factor('pattern.R123',(),1,3)
    base=(d4,e45,minus);canonical=(minus,d4,e45);g=(-4,-3)
    daisy5=pc_daisy_terms(d5.mapping_class);daisy4=pc_daisy_terms(minus.mapping_class)
    _matches(daisy5[:2],(d4,e45));_matches(daisy4[:1],(inside,));_matches(daisy5[2:],daisy4[1:])
    commutations=tuple(research_hurwitz_move((f,inside),1,0) for f in (d4,e45))
    for move,f in zip(commutations,(d4,e45)):_matches(move['factors'],(inside,f))
    raw_cyclic=reduce_word(minus.word+product(base)+inverse_word(minus.word)+inverse_word(product(canonical)))
    if raw_cyclic:raise ValueError('The INTERNAL cyclic lantern needs its full raw frame')
    output_frame_matches=_matches(_transport((d5,inside),minus.word),(d5,inside))
    _matches(r.factors[:3],_transport(canonical,g))
    outputs=(Factor('posthalf.exterior',(),1,5),Factor('posthalf.inner125',(-4,-3),1,3))
    r.substitute(0,3,outputs,'Actual cyclic cabled PC lantern reaches ONE visible unit exterior','disk_cluster_lantern')
    _witness(r,canonical,g,canonical_base=base,canonical_daisy5=daisy5,canonical_daisy4=daisy4,canonical_commutations=commutations,internal_cyclic_frame=minus.word,internal_raw_cyclic_discrepancy=raw_cyclic,individually_known_output_frame_matches=output_frame_matches)
    _outputs(r,(d5,inside),g)

    certificates=[];adjacent=[]
    for stage_index,s in enumerate(r.stages):
        for atomic_index,a in enumerate((s,)+s.get('atomic_steps',())):
            word=product(a['factors']);sphere=sphere_chain_certificate(word);lift=homology_action(word)
            if not sphere['certified'] or lift!=IDENTITY:raise ValueError('Retain the independent complete sphere/lift certificates')
            certificates.append(dict(stage=stage_index,atomic=atomic_index,score=_score(a['factors']),sphere_certificate=sphere,chosen_lift=lift))
        if s.get('atomic_steps'):
            state=r.stages[stage_index-1]['factors']
            for a in s['atomic_steps']:
                move=research_hurwitz_move(state,a['source'],a['target']);matches=_matches(move['factors'],a['factors'])
                adjacent.append(dict(stage=stage_index,source=a['source'],target=a['target'],raw_certificate=move['disk_word_certificate'],individual_presentations=matches));state=a['factors']
    kernels=tuple(dict(factor=f,split=split_fixed_last_strand(f.word,5)) for f in r.factors)
    for entry in kernels:
        if exact_action(entry['factor'].word,5)!=exact_action(entry['split'].reconstructed_word,5):raise ValueError('Retain every endpoint nonabelian kernel AND shadow')
    exterior=r.factors[0];residual=r.factors[1:];negative=tuple(tuple(-x for x in row) for row in IDENTITY)
    if homology_action(exterior.word)!=negative or homology_action(product(residual))!=negative or exact_action(product(residual),5)!=exact_action(BOUNDARY_WORD*3,5):
        raise ValueError('The visible odd exterior and its residual action/lift cannot be omitted')
    return dict(stages=tuple(r.stages),factors=r.factors,graphical_operations=len(r.stages)-1,adjacent_checks=len(adjacent),actual_adjacent_certificates=tuple(adjacent),state_sphere_lift_certificates=tuple(certificates),endpoint_point_pushing=kernels,
        repeated_rose_endpoint=repeated_endpoint,before_score=_score(source),after_score=_score(r.factors),peak_support_word=max(c['score']['max_support_word'] for c in certificates),
        exterior=exterior,exterior_chosen_lift=negative,residual_chosen_lift=negative,residual_boundary_power_diagnostic=3,residual_named_closure_complete=False,
        first_round12_loan_returned=True,round45_supplier_still_expanded=True,half_factors_introduced=0,negative_factors_introduced=0,sphere_moves=0,exterior_caps=0,
        public_replay_changed=False,preferred_moves=101,preferred_steps=71,complete_shorter_derivation=False,
        scope='A separate reached14-operation positive disk route after source85 index43. It uses two individually matched rose loans and two cabled lanterns. The original12 loan is returned; the45 supplier is still expanded. One exterior remains VISIBLE with-I lift; total lift is+I. No useful complete join to the preferred suffix is claimed, and the main101-move/71-step derivation stays SOLVED and unchanged.')
