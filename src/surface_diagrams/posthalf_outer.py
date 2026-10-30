"""Individually matched post-half rose/daisy routes; preferred proof unchanged."""
from dataclasses import replace
from .braid_actions import inverse_word,reduce_word
from .early_boundary_pure import _PositiveReplay,_score
from .factorization_explorer import Factor,product
from .hyperelliptic_homology import IDENTITY,homology_action
from .mapping_classes import exact_action
from .outside_half_lantern import _matches
from .outside_rose_return import _terms,_transport,_witness
from .point_pushing import split_fixed_last_strand
from .posthalf_exterior import _cyclic,_outputs
from .projected_relations import pc_daisy_terms,pc_rose_terms
from .six_seven_structure import research_hurwitz_move
from .sphere_actions import sphere_chain_certificate


def _source(factors):
    fs=tuple(factors)
    if len(fs)!=15 or any(f.half or f.power!=1 for f in fs) or tuple(f.id for f in fs[-4:])!=('alternative.P13','posthalf.supply.1','posthalf.output.1','F10.2'):
        raise ValueError('Use the selected first-crossing posthalf-spare endpoint')
    return fs


def _certify(r,exterior_id='posthalf.exterior'):
    states=[];adjacent=[]
    for i,s in enumerate(r.stages):
        for j,a in enumerate((s,)+s.get('atomic_steps',())):
            w=product(a['factors']);sphere=sphere_chain_certificate(w);lift=homology_action(w)
            if not sphere['certified'] or lift!=IDENTITY:raise ValueError('Retain independent complete sphere/+I checks')
            states.append(dict(stage=i,atomic=j,score=_score(a['factors']),sphere_certificate=sphere,chosen_lift=lift))
        state=r.stages[i-1]['factors'] if i else r.stages[0]['factors']
        for a in s.get('atomic_steps',()):
            raw=research_hurwitz_move(state,a['source'],a['target']);adjacent.append(dict(raw_move=raw,individual_presentations=_matches(raw['factors'],a['factors'])));state=a['factors']
    splits=tuple(dict(actual=f,split=split_fixed_last_strand(f.word,5)) for f in r.factors)
    for p in splits:
        if exact_action(p['actual'].word,5)!=exact_action(p['split'].reconstructed_word,5):raise ValueError('Keep full nonabelian kernels AND shadows')
    exterior=next(f for f in r.factors if f.id==exterior_id);minus=tuple(tuple(-x for x in row) for row in IDENTITY)
    if homology_action(exterior.word)!=minus:raise ValueError('Keep the visible odd exterior')
    return dict(stages=tuple(r.stages),factors=r.factors,graphical_operations=len(r.stages)-1,adjacent_checks=len(adjacent),actual_adjacent_certificates=tuple(adjacent),state_sphere_lift_certificates=tuple(states),endpoint_point_pushing=splits,before_score=_score(r.stages[0]['factors']),after_score=_score(r.factors),exterior=exterior,exterior_chosen_lift=minus,peak_support_word=max(s['score']['max_support_word'] for s in states),all_factors_positive=True,disk_action_verified=True,boundary_power=4,half_factors=0,negative_factors=0,sphere_moves=0,exterior_caps=0,public_replay_changed=False,useful_complete_join_reached=False)


def _preview(r,name,target,after=False):
    fs=r.factors;i=r.position(name);j=r.position(target)+int(after);steps=[]
    while i!=j:
        n=i+(1 if i<j else -1);raw=research_hurwitz_move(fs,i,n);score=_score(raw['factors'])
        if score['max_support_word']>20:return dict(bounded=False,applied=False,rejected_move=raw,rejected_score=score,unapplied_preview_prefix=tuple(steps))
        normalized=list(raw['factors']);normalized[i]=r.normalize(normalized[i]);fs=r.check(tuple(normalized));steps.append(dict(raw_move=raw,normalized_factors=fs,individual_presentations=_matches(raw['factors'],fs)));i=n
    return dict(bounded=True,applied=False,steps=tuple(steps),factors=fs)


def contract_posthalf_daisy(factors):
    """Four actual disk moves reach a14-record outer; the12 loan stays explicit."""
    source=_source(factors);r=_PositiveReplay(source);r.stages[0]['title']='Selected simpler-F10 endpoint before the12 loan'
    donor=r.factors[1];canonical_root=Factor('canonical.R123',(),1,3);g=donor.conjugator
    _matches((donor,),_transport((canonical_root,),g));loan=_terms(donor.mapping_class,'outer.loan.',pc_rose_terms)
    _matches(loan[:1],(Factor('round12',(),1,2),))
    r.substitute(1,1,loan,'The actual125 PC rose lends12 and retains its two other petals','disk_pc_rose')
    _witness(r,(canonical_root,),g,canonical_rose=_terms(canonical_root.mapping_class,'canonical.rose.',pc_rose_terms))
    _outputs(r,_terms(canonical_root.mapping_class,'canonical.rose.',pc_rose_terms),g)
    _cyclic(r,'posthalf.supply.1')
    preview=_preview(r,'outer.loan.0','F10.2',after=True)
    if not preview['bounded']:raise ValueError('Reject the short-side12 transport before application')
    r.drag('outer.loan.0','F10.2',after=True,title='Carry12 UP across only the commuting central exterior')
    if r.factors!=preview['factors']:raise ValueError('The applied transport differs from its bounded preview')
    canonical_parent=Factor('canonical.D2345',(),2,4);pattern=_terms(canonical_parent.mapping_class,'canonical.daisy.',pc_daisy_terms);original=pattern;internal=[]
    # Move the SAME canonical root down twice, then interchange the two
    # changed petals forward. The fourth petal is not altered or discarded.
    for a,b in ((0,1),(1,2),(0,1)):
        move=research_hurwitz_move(pattern,a,b);internal.append(move);pattern=move['factors']
    chart=(-1,-1,2,1,2,3,4);_matches(r.factors[:4],_transport(pattern,chart))
    output=Factor('outer.O1245',(-3,-4),1,4);_matches((output,),_transport((canonical_parent,),chart))
    r.substitute(0,4,(output,),'Actual14,15,245,12 contract by the individually matched PC daisy','disk_pc_daisy')
    _witness(r,pattern,chart,canonical_parent=canonical_parent,canonical_daisy=original,retained_internal_adjacent_moves=tuple(internal),internal_adjacent_checks=3)
    _outputs(r,(canonical_parent,),chart)
    normalized=tuple(replace(f,conjugator=reduce_word(inverse_word(chart)+f.conjugator)) for f in r.stages[-1]['local_before'])
    _matches(normalized,pattern)
    r.stages[-1]['named_pattern_witness']['normalized_actual_inputs']=normalized
    r.stages[-1]['named_pattern_witness']['normalized_input_point_pushing']=tuple(split_fixed_last_strand(f.word,5) for f in normalized)
    for f,p in zip(normalized,r.stages[-1]['named_pattern_witness']['normalized_input_point_pushing']):
        if exact_action(f.word,5)!=exact_action(p.reconstructed_word,5):raise ValueError('Retain normalized full kernels/shadows too')
    result=_certify(r);result.update(selected=True,internal_adjacent_checks=3,bounded_transport_preview=preview,round12_loan_returned=False,remaining_donor_petals=tuple(f for f in r.factors if f.id in ('outer.loan.1','outer.loan.2')),original_P13_unchanged=next(f for f in r.factors if f.id=='alternative.P13')==next(f for f in source if f.id=='alternative.P13'),scope='Four positive disk operations reach a four-point outer and keep the odd exterior visible. The125 donor stays expanded into TWO actual petals;12 is consumed in the outer,not returned. This research branch has no useful complete suffix join; preferred101moves/71steps remains solved and unchanged. No action-only outer recognition is used.')
    return result


def reconstruct_posthalf_145(factors,original_parent,original_outputs):
    """Reached3-move comparison using the restored matching spare, not originalW."""
    source=_source(factors);r=_PositiveReplay(source);r.stages[0]['title']='Selected simpler-F10 endpoint before the45 comparison'
    donor=source[-1];canonical_root=Factor('canonical.R345',(),3,3);g=donor.conjugator;loan=_terms(donor.mapping_class,'compare45.',pc_rose_terms)
    _matches((donor,),_transport((canonical_root,),g));_matches(loan[-1:],(Factor('round45',(),4,2),))
    r.substitute(14,1,loan,'Comparison: actual245 rose lends45','disk_pc_rose');_witness(r,(canonical_root,),g);_outputs(r,_terms(canonical_root.mapping_class,'canonical.rose.',pc_rose_terms),g)
    preview=_preview(r,'compare45.2','posthalf.supply.1',after=True)
    if not preview['bounded']:raise ValueError('Reject the45 transport before application')
    r.drag('compare45.2','posthalf.supply.1',after=True,title='Comparison:45 UP3 restores the OTHER15 spare to the originalW class')
    _matches((r.factors[r.position('posthalf.output.1')],),(source[10],))
    rejected=_preview(r,'posthalf.supply.1','alternative.P13')
    if rejected['bounded']:raise ValueError('The saved rejected direct V gather changed')
    canonical=Factor('canonical.R123',(),1,3);rose=_terms(canonical.mapping_class,'canonical.rose.',pc_rose_terms);cyclic=rose[1:]+rose[:1];chart=original_outputs[0].conjugator
    frame=inverse_word(rose[0].word);raw=reduce_word(frame+product(rose)+inverse_word(frame)+inverse_word(product(cyclic)))
    if raw:raise ValueError('Check the INTERNAL raw cyclic equality first')
    invariant=_matches(_transport((canonical,),frame),(canonical,));_matches((original_parent,),_transport((canonical,),chart))
    i=r.position('posthalf.supply.1');_matches(r.factors[i:i+3],_transport(cyclic,chart))
    output=replace(original_parent,id='comparison.R145');r.substitute(i,3,(output,),'Comparison: actual V,45,restoredW contract by a cyclic PC rose','disk_pc_rose')
    _witness(r,cyclic,chart,canonical_rose=rose,internal_cyclic_frame=frame,internal_raw_cyclic_discrepancy=raw,individually_known_output_invariance=invariant,source_parent=original_parent,source_outputs=original_outputs,uses_original_supplier_W=False,consumed_matching_spare_id='posthalf.output.1')
    _outputs(r,(canonical,),chart)
    result=_certify(r);result.update(selected=False,bounded_transport_preview=preview,rejected_direct_V_gather=rejected,round45_loan_returned_to245=False,original_supplier_W_retained=source[10],remaining_donor_petals=tuple(f for f in r.factors if f.id in ('compare45.0','compare45.1')),scope='Reached3-move positive comparison. The145 root uses V,new45,and the restored matching OTHERW copy; original supplierW remains literally fixed. The245 donor stays as TWO actual petals; this is not a return of45 to that donor. No useful complete join or whole-proof improvement claimed.')
    return result
