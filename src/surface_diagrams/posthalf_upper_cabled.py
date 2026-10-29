"""A single petal interchange supplies the actual upper-root cabled lantern."""
from dataclasses import replace
from .braid_actions import inverse_word,reduce_word
from .early_boundary_pure import _PositiveReplay,_score
from .factorization_explorer import Factor,product
from .mapping_classes import exact_action
from .named_powered_cabled import powered_cabled_lantern
from .outside_half_lantern import _matches
from .outside_rose_return import _transport,_witness
from .posthalf_exterior import _cyclic,_outputs
from .posthalf_outer import _certify
from .six_seven_structure import research_hurwitz_move


def upper_cabled_pattern():
    unit=powered_cabled_lantern(1,1,1);delta=(1,2,3,1,2,1)
    generators=tuple(dict(generator=i,conjugated=reduce_word(delta+(i,)+inverse_word(delta)),reflected=(4-i,)) for i in range(1,4))
    if any(exact_action(x['conjugated'],5)!=exact_action(x['reflected'],5) for x in generators):raise ValueError('Retain all three INTERNAL Delta4 generator reflections')
    a=Factor('canonical.Aunder',(-1,),2,3);c=Factor('canonical.C',(),2,3);q=Factor('canonical.Q',(),1,2);outputs=(Factor('canonical.O',(),1,4),Factor('canonical.I',(),3,2));base=(a,c,q)
    reflected_inputs=_matches(_transport(unit['canonical_unit_before'],delta),base);reflected_outputs=_matches(_transport(unit['unit_outputs'],delta),outputs)
    frame=inverse_word(product(base[:2]));cyclic=base[2:]+base[:2];raw=reduce_word(frame+product(base)+inverse_word(frame)+inverse_word(product(cyclic)))
    if raw:raise ValueError('Retain the FULL internal cyclic word BEFORE individual presentations')
    invariant=_matches(_transport(outputs,frame),outputs);move=research_hurwitz_move(cyclic,0,1);upper=Factor('canonical.Aupper',(1,),2,3);interchanged=(upper,q,c);_matches(move['factors'],interchanged)
    frame2=inverse_word(upper.word);actual=interchanged[1:]+interchanged[:1];raw2=reduce_word(frame2+product(interchanged)+inverse_word(frame2)+inverse_word(product(actual)))
    if raw2:raise ValueError('Retain the actual cyclic order FULL internal word')
    invariant2=_matches(_transport(outputs,frame2),outputs)
    return dict(inputs=actual,outputs=outputs,retained_base_named_lantern=unit,internal_reflection_chart=delta,generator_matches=generators,individual_reflected_inputs=reflected_inputs,individual_reflected_outputs=reflected_outputs,internal_cyclic_frames=(frame,frame2),internal_raw_cyclic_discrepancies=(raw,raw2),independently_known_output_invariances=(invariant,invariant2),retained_upper_root_interchange=move,individual_upper_root_interchange_matches=_matches(move['factors'],interchanged))


def contract_posthalf_upper_cabled(factors):
    source=tuple(factors);by={f.id:f for f in source}
    if len(source)!=14 or any(f.half or f.power!=1 for f in source) or tuple(f.id for f in source[4:8])!=('reflected.loan.1','reflected.loan.2','alternative.prepare.F5.1','alternative.prepare.F5.2'):
        raise ValueError('Use the selected TWO-exterior reflected-lantern endpoint')
    r=_PositiveReplay(source);r.stages[0]['title']='Two-exterior endpoint before the actual23 petal interchange'
    raw=research_hurwitz_move(source,5,4)
    if _score(raw['factors'])['max_support_word']>20:raise ValueError('Reject the actual23-UP13 crossing BEFORE application')
    r.drag('reflected.loan.2','reflected.loan.1',title='The SAME23 UP once changes13 to the EXACT needed cabled pair')
    if r.factors[r.position('reflected.loan.2')]!=by['reflected.loan.2']:raise ValueError('The moving23 stays LITERAL')
    _cyclic(r,'reflected.loan.1');pattern=upper_cabled_pattern();chart=(-3,-3,-2);_matches(r.factors[:3],_transport(pattern['inputs'],chart))
    outputs=(Factor('upper.O1234',(),1,4),r.normalize(Factor('upper.I24',chart,3,2)))
    r.substitute(0,3,outputs,'The ACTUAL changed13,234,124 contract by the individually matched upper-root cabled PC lantern','disk_cluster_lantern')
    _witness(r,pattern['inputs'],chart,retained_upper_cabled_pattern=pattern);_outputs(r,pattern['outputs'],chart)
    result=_certify(r);exteriors=tuple(f for f in r.factors if f.id in ('reflected.exterior','posthalf.exterior'))
    if tuple(f for f in source if f.id in ('reflected.exterior','posthalf.exterior'))!=tuple(f for f in r.factors if f.id in ('reflected.exterior','posthalf.exterior')):raise ValueError('Keep both exterior records LITERAL and in their cyclic relative order')
    result.update(named_substitutions=1,selected=True,two_visible_exteriors=exteriors,consumed_source_ids=('reflected.loan.1','alternative.prepare.F5.1','alternative.prepare.F5.2'),remaining_123_donor_petal=by['reflected.loan.2'],scope='THREE reached positive DISK moves/ONE external check: actual23 UP13 supplies the needed13,explicitcyclicstart,then individually matched upper-root cabled lantern reaches STANDARD O1234 andI24. Both unit exteriors and all other donor records stay explicit;no half,negativefactor,sphere redraw,cap or useful complete suffix join. Preferred101/71 stays SOLVED/UNCHANGED.')
    return result