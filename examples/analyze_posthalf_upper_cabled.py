"""Actual upper-root cabled contraction and finite source-pinned necessary tests."""
from dataclasses import asdict,replace
from hashlib import sha256
from itertools import permutations
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import equality,matrix
from examples.analyze_posthalf_cyclic_rose import commutators
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.outside_half_lantern import _matches
from surface_diagrams.outside_rose_return import _terms
from surface_diagrams.projected_relations import pc_rose_terms,pc_daisy_terms
from surface_diagrams.posthalf_upper_cabled import contract_posthalf_upper_cabled
from surface_diagrams.sphere_actions import sphere_chain_certificate
from surface_diagrams.hyperelliptic_homology import homology_action,IDENTITY
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
ROOT=Path(__file__).resolve().parents[1]


def report():
    path=ROOT/'docs/proofs/six-seven-posthalf-reflected-lantern.json';old=json.loads(path.read_text(encoding='utf-8'));source=tuple(factor_from_data(f) for f in old['route']['factors']);by={f.id:f for f in source};route=contract_posthalf_upper_cabled(source)
    families=(('prescribed125_124_45',('reflected.inner125','alternative.prepare.F5.2','cyclic135.supply.2')),('unchanged234_124_13',('alternative.prepare.F5.1','alternative.prepare.F5.2','reflected.loan.1')),('unchanged124_134_23',('alternative.prepare.F5.2','alternative.return.0','reflected.loan.2')),('unchanged_new135_triangle',('reflected.loan.1','reflected.output.1','outer.loan.1')),('unchanged125_daisy_changed35',('reflected.inner125','reflected.loan.1','reflected.loan.2','reflected.output.1')),('unchanged125_daisy_old35',('reflected.inner125','reflected.loan.1','reflected.loan.2','alternative.return.2')))
    failed=[]
    for label,names in families:
        orders=tuple(dict(actual_order=tuple(by[n] for n in order),commutators=commutators(tuple(by[n] for n in order))) for order in permutations(names))
        if any(all(x['left']==x['right'] for x in order['commutators']) for order in orders):raise ValueError('A finite necessary exclusion changed;zero matrices would be inconclusive')
        failed.append(dict(label=label,orders=orders,applied=False,scope='ONLY these unchanged UNIT factors under selected-only product-preserving DISK Hurwitz/common frames;outside interactions,new curves,substitutions,splitting and sphere changes are NOT excluded. The reached route changes13 and bypasses the unchanged234/124/13 failure.'))
    hypothetical=[];a=by['reflected.inner125'];c=by['alternative.prepare.F5.2'];q=by['cyclic135.supply.2']
    for sign in (-1,1):
        word=q.word if sign==1 else inverse_word(q.word);candidate=replace(c,conjugator=reduce_word(word+c.conjugator));hypothetical.append(dict(direction='fresh45 on124',sign=sign,candidate=candidate,support_length=len(supported_class(candidate.mapping_class,5)),applied=False))
    block=product((by['reflected.loan.1'],by['reflected.loan.2']));block_probes=[]
    for sign in (1,-1):
        word=block if sign==1 else inverse_word(block)
        for name in ('alternative.prepare.F5.1','alternative.prepare.F5.2','alternative.return.0'):
            candidate=replace(by[name],conjugator=reduce_word(word+by[name].conjugator));block_probes.append(dict(sign=sign,actual=by[name],candidate=candidate,support_length=len(supported_class(candidate.mapping_class,5)),applied=False))
    for stage in route['stages']:
        w=stage.get('named_pattern_witness')
        if not w:continue
        actual=stage['local_before']+stage['local_after'];normalized=tuple(replace(f,conjugator=reduce_word(inverse_word(w['common_chart'])+f.conjugator)) for f in actual)
        splits=tuple(dict(actual=f,split=split_fixed_last_strand(f.word,5)) for f in actual+normalized)
        for x in splits:
            if exact_action(x['actual'].word,5)!=exact_action(x['split'].reconstructed_word,5):raise ValueError('Keep FULL local and normalized kernels AND shadows')
        w['normalized_actual_inputs_and_outputs']=normalized;w['complete_actual_and_normalized_point_pushing']=splits
    end={f.id:f for f in route['factors']};donor=end['reflected.inner125'];rechart=replace(donor,conjugator=donor.conjugator+(1,));parent_match=_matches((donor,),(rechart,));rose=_terms(rechart.mapping_class,'target.new15.',pc_rose_terms);actor=Factor('target.actor15',(1,2,3),4,2);petal_match=_matches(rose[-1:],(actor,));changed=replace(end['alternative.return.0'],conjugator=reduce_word(actor.word+end['alternative.return.0'].conjugator));upper134=Factor('target.upper134',(1,),2,3);root_match=_matches((changed,),(upper134,))
    discrepancy=reduce_word(donor.word+inverse_word(product(rose)));sphere=sphere_chain_certificate(discrepancy);lift=homology_action(discrepancy)
    if not sphere['certified'] or lift!=IDENTITY:raise ValueError('Retain target-only local disk/sphere/+I separately')
    splits=tuple(dict(actual=f,split=split_fixed_last_strand(f.word,5)) for f in (donor,rechart)+rose+(actor,changed,upper134))
    for x in splits:
        if exact_action(x['actual'].word,5)!=exact_action(x['split'].reconstructed_word,5):raise ValueError('Keep every target-only NONABELIAN kernel and shadow')
    normalized=replace(actor,conjugator=reduce_word(inverse_word(donor.conjugator)+actor.conjugator));split5=split_fixed_last_strand(normalized.word,5);split4=split_fixed_last_strand(split5.shadow_word,4)
    if split5.kernel_loop or split4.kernel_loop or exact_action(split4.shadow_word,3)!=exact_action((1,2,2,-1),3):raise ValueError('Both full target actor splits must be retained')
    if exact_action(normalized.word,5)!=exact_action(split5.reconstructed_word,5) or exact_action(split5.shadow_word,4)!=exact_action(split4.reconstructed_word,4):raise ValueError('Retain BOTH exact normalized-actor reconstructions')
    next_target=dict(actual_parent=donor,internal_rechart=rechart,parent_match=parent_match,rose_outputs=rose,needed_actor=actor,individual_last_petal_match=petal_match,actual_R134=end['alternative.return.0'],hypothetical_changed_R134=changed,canonical_upper134=upper134,individual_positive_actor_root_match=root_match,current_pair_matches=tuple(f.id for f in route['factors'] if f.points==2 and equality(f.word,actor.word)['equal']),disk_discrepancy=discrepancy,sphere_certificate=sphere,chosen_lift=lift,signed_pc_balance=tuple((1 if j in enclosed_boundaries(donor.mapping_class,5) else 0)-sum(f.power for f in rose if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6)),full_point_pushing=splits,normalized_actor=normalized,full_split5=split5,full_split4=split4,applied=False,requires_every_transport_crossing_and_actual_context_match=True,scope='Exact internal(+1) PCrose of actualR125 can lend a NEW15 whose POSITIVE action restores actualR134 to upper134. NO expansion,transport,gather,substitution or useful fulljoin is reached. Actor is not either older15 by ancestry;donor otherTWO petals must stay accounted.')
    result=dict(source_file=path.name,source_sha256=sha256(path.read_bytes()).hexdigest(),source_ref='route.factors',route=route,before_closed_matrix=matrix(source),after_closed_matrix=matrix(route['factors']),finite_unchanged_selected_families=tuple(failed),unapplied45_root_probes=tuple(hypothetical),unapplied123_petal_block_probes=tuple(block_probes),next_new15_supplier_target=next_target,posthalf_combined_operations=old['posthalf_combined_operations']+3,posthalf_combined_adjacent_checks=old['posthalf_combined_adjacent_checks']+1,research_prefix_operation_count_at_checkpoint=91,preferred_moves=101,preferred_steps=71,public_replay_changed=False,scope='THREE reached positive DISK moves/ONE adjacent check create needed13 then contract ACTUAL13,234,124 to STANDARD O1234+I24. BOTH standard unit exteriors and ELEVEN shared records stay literal. No half,negativefactor,sphere redraw,cap or useful complete suffix join. Differing endpoint inventories mean totals are descriptive,not arc crossings,joint minima,entrywise dominance or whole-proof bounds. Preferred101/71 remains SOLVED/UNCHANGED.')

    first_matrix=matrix(route['stages'][1]['factors']);lookup={x['ids']:x['number'] for x in result['before_closed_matrix']['pairs']}
    result['first_interchange_closed_matrix']=first_matrix
    result['first_interchange_changed_pairs']=tuple(dict(ids=x['ids'],before=lookup[x['ids']],after=x['number'],delta=x['number']-lookup[x['ids']]) for x in first_matrix['pairs'] if x['number']!=lookup[x['ids']])
    d5=Factor('target.D5',(),1,5);daisy=_terms(d5.mapping_class,'target.D5.',pc_daisy_terms)
    known=tuple(dict(index=i,actual=end[n],individual_match=_matches((end[n],),(daisy[i],))) for i,n in ((0,'upper.O1234'),(1,'cyclic135.supply.2'),(3,'outer.loan.2')))
    missing=tuple(dict(actual=end[n],comparison=equality(end[n].word,daisy[2].word)) for n in ('reflected.output.1','alternative.return.2'))
    if any(x['comparison']['equal'] for x in missing):raise ValueError('Retain both scoped current35 misses')
    result['next_standard_exterior_daisy_target']=dict(canonical_parent=d5,canonical_daisy=daisy,three_current_individual_matches=known,hypothetical_new15_match=_matches((actor,),(daisy[4],)),needed35=daisy[2],current35_misses=missing,unperformed_outside_actor=end['reflected.inner125'],both_actor_signs_tested=False,applied=False,scope='STANDARD O1234,fresh45,older25 individually match D5 inputs0,1,3. An UNEXPANDED actualR125 PCrose can supply the exact needed15. BOTH actual35 records fail the required35. No ordered cluster,gather,D5substitution,thirdexterior or completejoin is reached. FIRST test either sign of actualR125 on CHANGED35 against this precise missing35 before transport.')
    return result

if __name__=='__main__':
    r=report();path=ROOT/'docs/proofs/six-seven-posthalf-upper-cabled.json'
    with path.open('w',encoding='utf-8',newline='\n') as f:json.dump(r,f,default=asdict,separators=(',',':'))
    print('Selected',r['route']['graphical_operations'],r['route']['after_score'],r['after_closed_matrix']['total'],r['after_closed_matrix']['maximum'],path.stat().st_size)