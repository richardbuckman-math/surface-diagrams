"""A reflected cabled PC lantern uses the actual adjacent235/135 roots."""
from dataclasses import replace
from .braid_actions import inverse_word,reduce_word
from .early_boundary_pure import _PositiveReplay,_score
from .factorization_explorer import Factor
from .mapping_classes import exact_action
from .named_powered_cabled import powered_cabled_lantern
from .outside_half_lantern import _matches
from .outside_rose_return import _terms,_transport,_witness
from .posthalf_exterior import _cyclic,_outputs
from .posthalf_outer import _certify,_preview
from .projected_relations import pc_rose_terms


def reflected_cabled_pattern():
    base=powered_cabled_lantern(1,1,1)
    delta=(1,2,3,4,1,2,3,1,2,1)
    generators=tuple(dict(generator=i,conjugated=reduce_word(delta+(i,)+inverse_word(delta)),reflected=(5-i,)) for i in range(1,5))
    if any(exact_action(x['conjugated'],5)!=exact_action(x['reflected'],5) for x in generators):raise ValueError('Check every generator of the internal disk reflection')
    inputs=(Factor('reflected.A',(-2,),3,3),Factor('reflected.C',(),3,3),Factor('reflected.Q',(),2,2))
    outputs=(Factor('reflected.O',(),2,4),Factor('reflected.I',(),4,2))
    return dict(base_named_cabled_lantern=base,internal_reflection_chart=delta,generator_matches=generators,inputs=inputs,outputs=outputs,individual_reflected_inputs=_matches(_transport(base['canonical_unit_before'],delta),inputs),individual_reflected_outputs=_matches(_transport(base['unit_outputs'],delta),outputs))


def contract_posthalf_reflected_lantern(factors):
    source=tuple(factors);by={f.id:f for f in source}
    if len(source)!=14 or any(f.half or f.power!=1 for f in source) or tuple(f.id for f in source[10:12])!=('alternative.S1','cyclic135.R135'):
        raise ValueError('Use the selected actual cyclic135 endpoint')
    r=_PositiveReplay(source);r.stages[0]['title']='Actual cyclic135 endpoint before the commuting12 loan'
    _cyclic(r,'alternative.S1')
    donor=by['posthalf.return.R123'];parent=Factor('canonical.R123',(),1,3);canonical=_terms(parent.mapping_class,'canonical.rose.',pc_rose_terms)
    loan=_terms(donor.mapping_class,'reflected.loan.',pc_rose_terms);_matches(loan[:1],(Factor('round12',(),1,2),))
    r.substitute(r.position(donor.id),1,loan,'The ACTUAL returned123 PC rose lends12 and retains its other two petals','disk_pc_rose')
    _witness(r,(parent,),donor.conjugator,canonical_rose=canonical);_outputs(r,canonical,donor.conjugator)
    preview=_preview(r,'reflected.loan.0','cyclic135.R135',after=True)
    if not preview['bounded']:raise ValueError('Reject the12 gather BEFORE application')
    r.drag('reflected.loan.0','cyclic135.R135',after=True,title='Carry the SAME12 UP across only the commuting exterior and four-point outer')
    if r.factors!=preview['factors']:raise ValueError('The applied loan must match its full bounded preview')
    for name in ('outer.O1245','posthalf.exterior'):
        if r.factors[r.position(name)]!=by[name]:raise ValueError('Both crossed neighbors must remain LITERAL')
    pattern=reflected_cabled_pattern();chart=(-3,-1,2,1);_matches(r.factors[:3],_transport(pattern['inputs'],chart))
    raw=_transport(pattern['outputs'],chart);outputs=tuple(r.normalize(replace(f,id='reflected.output.'+str(i))) for i,f in enumerate(raw))
    r.substitute(0,3,outputs,'The ACTUAL235,135,12 contract by the individually matched reflected cabled PC lantern','disk_cluster_lantern')
    _witness(r,pattern['inputs'],chart,retained_reflected_named_pattern=pattern);_outputs(r,pattern['outputs'],chart)
    result=_certify(r);result.update(named_substitutions=2,selected=True,bounded_loan_preview=preview,remaining_123_donor_petals=tuple(f for f in r.factors if f.id in ('reflected.loan.1','reflected.loan.2')),round12_loan_returned=False,consumed_source_ids=('posthalf.return.R123','alternative.S1','cyclic135.R135'),scope='Four positive DISK moves/two adjacent checks reach a second four-point outer and the exact35 pair. The actual123 donor remains TWO petals;12 is consumed,not returned. Both crossed exterior/outer records stay LITERAL. No half,negativefactor,sphere redraw,cap or useful complete suffix join;preferred101/71 remains solved and unchanged.')
    return result

def expose_posthalf_second_exterior(factors):
    """Seven positive disk moves retain TWO visible unit exteriors."""
    from .factorization_explorer import product
    from .hyperelliptic_homology import IDENTITY,homology_action
    from .projected_relations import pc_daisy_terms
    from .puncture_boundary import BOUNDARY_WORD
    from .six_seven_structure import research_hurwitz_move
    outer=contract_posthalf_reflected_lantern(factors);r=_PositiveReplay(tuple(factors));r.factors=outer['factors'];r.stages=list(outer['stages'])
    raw=research_hurwitz_move(r.factors,2,1)
    if _score(raw['factors'])['max_support_word']>20:raise ValueError('Reject the old outer UP across35 BEFORE application')
    r.drag('outer.O1245','reflected.output.1',title='The SAME old four-point outer UP once exposes the two matched outer curves')
    _matches(raw['factors'],r.factors)
    _cyclic(r,'cyclic135.supply.0')
    d4=Factor('canonical.D4',(),1,4);q=Factor('canonical.Q45',(),4,2);minus=Factor('canonical.Ominus',(-4,),1,4);d5=Factor('canonical.D5',(),1,5);inside=Factor('canonical.R123',(),1,3)
    base=(d4,q,minus);canonical=(minus,d4,q);daisy5=_terms(d5.mapping_class,'canonical.D5.',pc_daisy_terms);daisy4=_terms(minus.mapping_class,'canonical.Ominus.',pc_daisy_terms)
    shared=(_matches(daisy5[:2],(d4,q)),_matches(daisy4[:1],(inside,)),_matches(daisy5[2:],daisy4[1:]))
    commutations=tuple(research_hurwitz_move((f,inside),1,0) for f in (d4,q))
    commute_matches=tuple(_matches(move['factors'],(inside,f)) for move,f in zip(commutations,(d4,q)))
    raw_cycle=reduce_word(minus.word+product(base)+inverse_word(minus.word)+inverse_word(product(canonical)))
    if raw_cycle:raise ValueError('Check the full INTERNAL cyclic lantern word BEFORE presentations')
    invariance=_matches(_transport((d5,inside),minus.word),(d5,inside))
    frame=inverse_word(product(canonical[:2]));actual_pattern=canonical[2:]+canonical[:2];raw_second=reduce_word(frame+product(canonical)+inverse_word(frame)+inverse_word(product(actual_pattern)))
    if raw_second:raise ValueError('Check the actual cyclic order BEFORE presentations')
    second_invariance=_matches(_transport((d5,inside),frame),(d5,inside))
    chart=(-3,-4,-3);_matches(r.factors[:3],_transport(actual_pattern,chart))
    outputs=(Factor('reflected.exterior',(),1,5),Factor('reflected.inner125',(-4,-3),1,3))
    r.substitute(0,3,outputs,'The ACTUAL34,new outer,old outer contract by the cyclic cabled PC lantern; keep BOTH exteriors','disk_cluster_lantern')
    _witness(r,actual_pattern,chart,canonical_base=base,canonical_order=canonical,canonical_D5_daisy=daisy5,canonical_Ominus_daisy=daisy4,shared_petal_matches=shared,retained_canonical_commutations=commutations,canonical_commutation_matches=commute_matches,internal_cyclic_frames=(minus.word,frame),internal_raw_cyclic_discrepancies=(raw_cycle,raw_second),independently_known_output_invariances=(invariance,second_invariance));_outputs(r,(d5,inside),chart)
    result=_certify(r);exteriors=tuple(f for f in r.factors if f.id in ('posthalf.exterior','reflected.exterior'));residual=tuple(f for f in r.factors if f.id not in ('posthalf.exterior','reflected.exterior'))
    minus_identity=tuple(tuple(-x for x in row) for row in IDENTITY)
    if len(exteriors)!=2 or any(homology_action(f.word)!=minus_identity for f in exteriors) or homology_action(product(residual))!=IDENTITY or exact_action(product(residual),5)!=exact_action(BOUNDARY_WORD*2,5):raise ValueError('Keep BOTH odd exteriors and the separate residual diagnostic')
    result.update(named_substitutions=3,selected=True,round12_loan_returned=False,remaining_123_donor_petals=outer['remaining_123_donor_petals'],four_move_outer_endpoint=outer['factors'],four_move_outer_score=outer['after_score'],bounded_loan_preview=outer['bounded_loan_preview'],two_visible_exteriors=exteriors,every_exterior_chosen_lift=minus_identity,residual_boundary_power_diagnostic=2,residual_chosen_lift=IDENTITY,residual_named_closure_complete=False,consumed_source_ids=('posthalf.return.R123','alternative.S1','cyclic135.R135','outer.O1245','cyclic135.supply.0'),scope='Seven reached positive DISK moves/three external adjacent checks reach a SECOND VISIBLE standard unit exterior. The remaining ROUND45 donor petal,123 donor two petals,and BOTH older125 loan petals stay explicit. Each odd exterior has-I;their residual has+I and diagnostic boundary-square action,NOT a named closure or complete suffix join. Preferred101/71 stays SOLVED/UNCHANGED;no new sphere redraw or cap.')
    return result