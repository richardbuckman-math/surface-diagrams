"""Reached cyclic135 rose and exact, scoped subsequent order gaps."""
from dataclasses import asdict,replace
from hashlib import sha256
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import equality,matrix
from examples.analyze_posthalf_petal import multiply
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.early_boundary_pure import _PositiveReplay,_score
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.hyperelliptic_homology import homology_action,IDENTITY
from surface_diagrams.mapping_classes import supported_class
from surface_diagrams.named_powered_cabled import powered_cabled_lantern
from surface_diagrams.outside_half_lantern import _matches
from surface_diagrams.outside_rose_return import _transport
from surface_diagrams.posthalf_cyclic_rose import contract_posthalf_cyclic_rose,cyclic_pattern
from surface_diagrams.posthalf_outer import _certify
from surface_diagrams.projected_relations import pc_daisy_terms
from surface_diagrams.six_seven_structure import research_hurwitz_move
from surface_diagrams.sphere_actions import sphere_chain_certificate
ROOT=Path(__file__).resolve().parents[1]


def commutators(fs):
    p=homology_action(product(fs));return tuple(dict(actual=f,left=multiply(p,homology_action(f.word)),right=multiply(homology_action(f.word),p)) for f in fs)


def report():
    path=ROOT/'docs/proofs/six-seven-posthalf-block.json';old=json.loads(path.read_text(encoding='utf-8'));source=tuple(factor_from_data(f) for f in old['route']['factors']);by={f.id:f for f in source};route=contract_posthalf_cyclic_rose(source);end={f.id:f for f in route['factors']}
    a,q,c=(by[n] for n in ('alternative.prepare.F5.1','outer.loan.2','F8.2'));old_order=(a,q,c);correct=(a,c,q);d4=Factor('canonical.O2345',(),2,4);i34=Factor('canonical.I34',(),3,2);db=tuple(Factor('pc.'+str(i),t.conjugator,t.first,t.points) for i,t in enumerate(pc_daisy_terms(c.mapping_class)));rot,cycle=cyclic_pattern(c,db,1);expand=(a,)+rot+(q,);commute=research_hurwitz_move(expand,3,4);daisy=tuple(Factor('D4.'+str(i),t.conjugator,t.first,t.points) for i,t in enumerate(pc_daisy_terms(d4.mapping_class)));_matches(commute['factors'],daisy+(i34,));right=(d4,i34)
    if not equality(product(correct),product(right))['equal']:raise ValueError('Keep the canonical named round-root relation')
    needed25=replace(q,id='required.above25',conjugator=reduce_word(c.word+q.conjugator));same=replace(q,conjugator=reduce_word(inverse_word(a.word)+q.conjugator));_matches((needed25,),(same,))
    helper=_PositiveReplay(source);helper.drag('F8.2','alternative.S1',title='Unselected bounded comparison: round345 DOWN once overS1');alt=_certify(helper);alt['selected']=False
    before,after,altm=matrix(source),matrix(route['factors']),matrix(alt['factors']);lookup={x['ids']:x['number'] for x in before['pairs']};alt_changes=tuple(dict(ids=x['ids'],before=lookup[x['ids']],after=x['number'],delta=x['number']-lookup[x['ids']]) for x in altm['pairs'] if lookup[x['ids']]!=x['number'])
    unit=powered_cabled_lantern(1,1,1);base=unit['canonical_unit_before'];parent_outputs=unit['unit_outputs'];p2=2;frame=inverse_word(product(base[:p2]));cyclic=base[p2:]+base[:p2];raw_cycle=reduce_word(frame+product(base)+inverse_word(frame)+inverse_word(product(cyclic)));_matches(_transport(parent_outputs,frame),parent_outputs)
    upmove=research_hurwitz_move(cyclic,0,1);upper=Factor('canonical.Aupper',(3,),1,3);upper_order=(upper,base[2],base[1]);_matches(upmove['factors'],upper_order)
    frame2=inverse_word(product(upper_order[:2]));upper_cyclic=upper_order[2:]+upper_order[:2];raw2=reduce_word(frame2+product(upper_order)+inverse_word(frame2)+inverse_word(product(upper_cyclic)));_matches(_transport(parent_outputs,frame2),parent_outputs)
    chart=(-3,-3,2,-4);actual_wrong=(end['posthalf.return.R123'],end['outer.loan.2'],end['cyclic135.R135']);canonical_wrong=(base[1],base[2],upper);matches=_matches(actual_wrong,_transport(canonical_wrong,chart));expected=_transport(upper_cyclic,chart);outputs=_transport(parent_outputs,chart)
    if not equality(product(expected),product(outputs))['equal'] or raw_cycle or raw2:raise ValueError('Retain full named cyclic/interchange proof')
    needed_frame=inverse_word(product(upper_cyclic[:2]));needed_cyclic=upper_cyclic[2:]+upper_cyclic[:2];needed_raw=reduce_word(needed_frame+product(upper_cyclic)+inverse_word(needed_frame)+inverse_word(product(needed_cyclic)));needed_invariance=_matches(_transport(parent_outputs,needed_frame),parent_outputs);needed_move=research_hurwitz_move(needed_cyclic,0,1)
    desired_first=replace(actual_wrong[0],conjugator=reduce_word(actual_wrong[1].word+actual_wrong[0].conjugator));needed_order=(desired_first,actual_wrong[1],actual_wrong[2])
    needed_matches=_matches(needed_order,_transport(needed_move['factors'],chart))
    if needed_raw or not equality(product(needed_order),product(outputs))['equal']:raise ValueError('The precise outside-preconditioner target failed')
    failed=[];wanted_under=_transport((base[0],),chart)[0];fresh45=end['cyclic135.supply.2'];fresh34=end['cyclic135.supply.0']
    for name,w in (('45+',fresh45.word),('45-',inverse_word(fresh45.word)),('34+',fresh34.word),('34-',inverse_word(fresh34.word)),('45/34+',fresh45.word+fresh34.word)):
        f=replace(actual_wrong[2],conjugator=reduce_word(w+actual_wrong[2].conjugator));failed.append(dict(direction=name,candidate=f,target=wanted_under,comparison=equality(f.word,wanted_under.word),support_length=len(supported_class(f.mapping_class,5)),applied=False))
    extra=[]
    for label,word in (('R124 inverse',by['alternative.prepare.F5.2'].word),('ordered R124/R134 inverse',product((by['alternative.prepare.F5.2'],by['alternative.return.0'])))):
        candidate=replace(a,conjugator=reduce_word(inverse_word(word)+a.conjugator));extra.append(dict(direction=label,candidate=candidate,support_length=len(supported_class(candidate.mapping_class,5)),ordered_cluster_noncentrality=commutators((candidate,q,c)),applied=False))
    rejected_donor=research_hurwitz_move(source,3,2)
    return dict(source_file=path.name,source_sha256=sha256(path.read_bytes()).hexdigest(),source_ref='route.factors',route=route,before_closed_matrix=before,after_closed_matrix=after,
        original_round_cluster_order_gap=dict(actual_order=old_order,noncentrality_witnesses=commutators(old_order),wrong_product=equality(product(old_order),product(right)),correct_order=correct,correct_outputs=right,canonical345_daisy=db,internal_cyclic_certificate=cycle,retained_commuting_move=commute,canonicalO2345_daisy=daisy,correct25_before345=needed25,applied=False),
        unselected_S1_interchange=dict(route=alt,closed_matrix=altm,changed_pairs=alt_changes,scope='Reached1move/1check,onlyS1changes;5 CLOSED entries decrease,one2->4 increases. Total346->334,max20->18;word9/67 unchanged,braid152->150. Needed25 still NOT insideS1;unselected,no usefulcompletejoin.'),
        new_R123_25_R135_order_gap=dict(actual_order=actual_wrong,common_chart=chart,individual_curve_matches=matches,actual_noncentrality_witnesses=commutators(actual_wrong),correct_canonical_order=upper_cyclic,correct_actual_order=expected,correct_outputs=outputs,retained_base_cabled_lantern=unit,internal_cyclic_frames=(frame,frame2),internal_raw_discrepancies=(raw_cycle,raw2),retained_upper_root_interchange=upmove,needed_first_root=desired_first,needed_actual_order=needed_order,needed_internal_cyclic_frame=needed_frame,needed_internal_raw_discrepancy=needed_raw,needed_output_invariance=needed_invariance,needed_root_interchange=needed_move,needed_individual_matches=needed_matches,applied=False,scope='AllTHREE actual curves individually match a cyclic upper-root PC cabled lantern,but their actual cyclic ORDER is wrong. Current selected-only Hurwitz/commonframes cannot fix its noncentral product. Positive outside25 conjugation of the123 root would give the required ordered relation;that root is hypothetical and no bounded outside transport is reached.'),
        failed_source_root_preconditioners=tuple(extra),rejected12_donor_preconditioner=dict(raw_move=rejected_donor,score=_score(rejected_donor['factors']),applied=False),failed_new_round_petal_preconditioners=tuple(failed),next_outside_target=dict(needed_first_root=desired_first,actual_first_root=actual_wrong[0],available_ordered_block=(fresh45,fresh34),inverse_block_test_performed=False,applied=False,requires_exact_class_support_test_before_ordered_transport=True),posthalf_combined_operations=old['posthalf_combined_operations']+3,posthalf_combined_adjacent_checks=old['posthalf_combined_adjacent_checks']+1,research_prefix_operation_count_at_checkpoint=81,preferred_moves=101,preferred_steps=71,public_replay_changed=False,
        scope='Selected3move cyclic rose is REACHED with every actual named input/output separately matched. Endpoint14records,9/65,braid146,CLOSED320/20;source14,9/67,152,346/20. Inventories differ;totals are descriptive,not entrywise dominance/arc/jointminimum/wholeproofbounds. Both donor34/45 petals stay;oneWcopy consumed,other15 retained. NewR135 is DIFFERENT from the earlier missingR135 target. No new sphere move,cap,half,second exterior or complete suffix join;preferred101/71 stays SOLVED/UNCHANGED.')


if __name__=='__main__':
    r=report();p=ROOT/'docs/proofs/six-seven-posthalf-cyclic-rose.json'
    with p.open('w',encoding='utf-8',newline='\n') as f:json.dump(r,f,default=asdict,separators=(',',':'))
    print('Selected',r['route']['graphical_operations'],r['route']['after_score'],r['after_closed_matrix']['total'],p.stat().st_size)
