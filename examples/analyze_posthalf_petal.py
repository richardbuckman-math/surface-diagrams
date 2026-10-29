"""Exact post-half curve improvement and scoped failed common-chart targets."""
from dataclasses import asdict,replace
from hashlib import sha256
from itertools import combinations,permutations
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import equality,matrix
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.disk_intersection import disk_intersection_certificate
from surface_diagrams.early_boundary_pure import _PositiveReplay,_score
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import supported_class
from surface_diagrams.named_powered_cabled import powered_cabled_lantern
from surface_diagrams.outside_half_lantern import _matches
from surface_diagrams.outside_rose_return import _transport
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.posthalf_petal import simplify_posthalf_P13
from surface_diagrams.six_seven_structure import research_hurwitz_move
from surface_diagrams.sphere_actions import sphere_chain_certificate
ROOT=Path(__file__).resolve().parents[1]


def multiply(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(4)) for j in range(4)) for i in range(4))


def triangle_audits(fs):
    by={f.id:f for f in fs};result=[]
    for a,b in (('alternative.P13','alternative.return.2'),('posthalf.supply.1','alternative.return.1')):
        for spare in ('posthalf.supply.0','posthalf.output.1'):
            selected=tuple(by[n] for n in (a,b,spare));orders=[]
            for order in permutations(selected):
                word=product(order);action=homology_action(word);witnesses=[]
                for f in order:
                    m=homology_action(f.word);left,right=multiply(action,m),multiply(m,action)
                    witnesses.append(dict(actual=f,product_lift=action,input_lift=m,left=left,right=right,commutes=left==right))
                if all(w['commutes'] for w in witnesses):raise ValueError('A zero homology commutator is inconclusive; do not claim exclusion')
                orders.append(dict(order=tuple(f.id for f in order),noncentrality_witnesses=tuple(witnesses)))
            result.append(dict(actual_inputs=selected,closed_pairs=tuple(dict(ids=(x.id,y.id),certificate=disk_intersection_certificate(x.mapping_class,y.mapping_class,strands=5)) for x,y in combinations(selected,2)),orders=tuple(orders),scope='Noncommutation in an exact integral representation proves disk noncommutation. These unchanged selected triples in any listed order cannot be an expanded PC rose, even after selected-only Hurwitz/common conjugation. Outside interactions,new curves and sphere changes remain unexcluded.'))
    return tuple(result)


def report():
    path=ROOT/'docs/proofs/six-seven-posthalf-exterior.json';old=json.loads(path.read_text(encoding='utf-8'))
    source=tuple(factor_from_data(f) for f in old['route']['factors']);route=simplify_posthalf_P13(source);fs=route['factors'];by={f.id:f for f in fs}
    before,after=matrix(source),matrix(fs);lookup={p['ids']:p['number'] for p in before['pairs']}
    changed=tuple(dict(ids=p['ids'],before=lookup[p['ids']],after=p['number'],delta=p['number']-lookup[p['ids']]) for p in after['pairs'] if p['number']!=lookup[p['ids']])
    if not changed or any(p['delta']>=0 for p in changed):raise ValueError('The claimed pairwise improvement must be checked entry by entry')
    # The first selected move is reached; the second bounded inverse move is a
    # different, worse endpoint. Stop before the third or the first forward move.
    second_raw=research_hurwitz_move(fs,11,10);helper=_PositiveReplay(fs)
    candidate=second_raw['factors'];normal=helper.normalize(candidate[11]);second=candidate[:11]+(normal,)+candidate[12:]
    helper.check(second);sm=matrix(second)
    rejected_inverse=research_hurwitz_move(second,11,10)['factors'];rejected_forward=research_hurwitz_move(source,10,11)['factors']
    alternative=dict(factors=second,score=_score(second),closed_matrix=sm,raw_move=second_raw,individual_presentations=_matches(second_raw['factors'],second),sphere_certificate=sphere_chain_certificate(product(second)),chosen_lift=homology_action(product(second)),selected=False)
    rejected=tuple(dict(direction=d,factors=state,score=_score(state),applied=False,reason='support maximum exceeds20') for d,state in (('third inverse',rejected_inverse),('first forward',rejected_forward)))
    if any(a['score']['max_support_word']<=20 for a in rejected):raise ValueError('The rejected bound changed')

    a,c,wrong=(by[n] for n in ('posthalf.inner125','posthalf.return.R123','alternative.return.2'));selected=(a,c,wrong)
    old_target_orders=[]
    for order in permutations(selected):
        w=product(order);checks=tuple(equality(w+f.word,f.word+w) for f in order)
        if any(x['equal'] for x in checks):raise ValueError('Retain the precise saved noncentral triple test')
        old_target_orders.append(dict(order=tuple(f.id for f in order),checks=checks))
    g=(-3,-3,-4);unit=powered_cabled_lantern(1,1,1);pattern=_transport(unit['canonical_unit_before'],g);outputs=_transport(unit['unit_outputs'],g)
    root_matches=_matches((a,c),pattern[:2]);missing=pattern[2];simple=Factor('required.Q35',(-3,),4,2)
    _matches((missing,),(simple,));q12=Factor('shared.Q12',(),1,2)
    generators=tuple(dict(actual=f,commutation=equality(f.word+q12.word,q12.word+f.word)) for f in (a,c,q12))
    if not all(t['commutation']['equal'] for t in generators):raise ValueError('The scoped stabilizer obstruction changed')
    wrong_commutation=equality(wrong.word+q12.word,q12.word+wrong.word)
    if wrong_commutation['equal']:raise ValueError('Do not substitute an incidence-only pair for the joint curve')
    d=reduce_word(product(pattern)+inverse_word(product(outputs)));local_sphere=sphere_chain_certificate(d);local_lift=homology_action(d)
    if not local_sphere['certified'] or local_lift!=IDENTITY:raise ValueError('The target retains separate disk/sphere/lift checks')
    splits=[]
    for f in (a,c,wrong)+pattern+outputs:
        s=split_fixed_last_strand(f.word,5)
        if not equality(f.word,s.reconstructed_word)['equal']:raise ValueError('Keep the full joint-chart kernels and shadows')
        splits.append(dict(actual=f,split=s))
    donors=tuple(dict(actual=by[n],required=missing,closed_certificate=disk_intersection_certificate(by[n].mapping_class,missing.mapping_class,strands=5)) for n in ('F8.2','alternative.S1'))
    probes=[]
    for name in ('F8.2','alternative.S1'):
        f=by[name]
        for sign in (1,-1):
            w=f.word if sign==1 else inverse_word(f.word);p=replace(wrong,conjugator=reduce_word(w+wrong.conjugator))
            probes.append(dict(conjugator=f,sign=sign,candidate=p,target=missing,comparison=equality(p.word,missing.word),support_length=len(supported_class(p.mapping_class,5)),applied=False))
    current_matches=tuple(f.id for f in fs if f.points==2 and equality(f.word,missing.word)['equal'])
    ledger={pair:0 for pair in combinations(range(1,6),2)}
    for f in fs[1:]:
        for pair in combinations(enclosed_boundaries(f.mapping_class,5),2):ledger[pair]+=f.power
    return dict(source_file=path.name,source_sha256=sha256(path.read_bytes()).hexdigest(),source_ref='route.factors',route=route,before_closed_matrix=before,after_closed_matrix=after,changed_pairs=changed,
        second_inverse_alternative=alternative,rejected_candidates=rejected,
        previous_cabled_candidate=dict(actual_inputs=selected,closed_pairs=tuple(dict(ids=(x.id,y.id),certificate=disk_intersection_certificate(x.mapping_class,y.mapping_class,strands=5)) for x,y in combinations(selected,2)),orders=tuple(old_target_orders),applied=False),
        correct_cabled_target=dict(common_chart=g,canonical_inputs=unit['canonical_unit_before'],actual_pattern_inputs=pattern,actual_pattern_outputs=outputs,actual_root_matches=root_matches,required_pair=missing,simple_required_pair=simple,existing_pair_matches=current_matches,
            canonical_interchange=unit['retained_unit_interchange'],disk_discrepancy=d,sphere_certificate=local_sphere,chosen_lift=local_lift,
            signed_framed_balance=tuple(sum(f.power for f in pattern if j in enclosed_boundaries(f.mapping_class,5))-sum(f.power for f in outputs if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6)),complete_splits=tuple(splits),actual_inner_stabilizers=generators,wrong_pair_inner_commutation=wrong_commutation,unchanged_triple_supplier_diagnostics=donors,limited_unapplied_root_probes=tuple(probes),applied=False,requires_supply_and_transport=True),
        incidence_only_pair_ledger=tuple(dict(pair=p,value=v) for p,v in ledger.items()),triangle_audits_before=triangle_audits(source),triangle_audits_after=triangle_audits(fs),
        preliminary_based_action_exhaustion=dict(source='before simplification; first135 triangle order',bound=400000,status='UNKNOWN from Artin comparison; no inequality inferred',later_method='Exact integral noncommutation witnesses independently exclude all listed triangle orders; homology identity would have been inconclusive'),
        next_two_neighbor_candidate=dict(moving=by['posthalf.output.1'],target=by['alternative.P13'],crossed_in_order=(by['F10.2'],by['posthalf.supply.1']),closed_pair_certificate=disk_intersection_certificate(by['posthalf.output.1'].mapping_class,by['alternative.P13'].mapping_class,strands=5),applied=False,requires_bounded_transport_and_joint_match=True,scope='This fixed-spare gather alone cannot repair the excluded unchanged135 triangle; a named contraction needs different actual inputs or an outside change.'),
        posthalf_combined_operations=old['route']['graphical_operations']+1,posthalf_combined_adjacent_checks=old['route']['adjacent_checks']+1,research_prefix_operation_count_at_checkpoint=58,preferred_moves=101,preferred_steps=71,public_replay_changed=False,
        scope='The selected ONE positive interchange changes only P13 and improves all9 changed pairwise CLOSED counts; the rest stay equal. No global/common frame,half,sphere move or cap appears. Only a reached research branch changes; there is NO useful complete join to the preferred suffix. Closed counts are not arc crossings or a jointly realizable minimum drawing. Candidate failures are scoped to the exact unchanged records and listed orders, not the whole factorization orbit.')

if __name__=='__main__':
    r=report();p=ROOT/'docs/proofs/six-seven-posthalf-petal.json'
    with p.open('w',encoding='utf-8',newline='\n') as f:json.dump(r,f,default=asdict,separators=(',',':'))
    print('P13',r['route']['P13_support_lengths'],'scores',r['route']['before_score'],r['route']['after_score'])
    print('Closed',r['before_closed_matrix']['total'],r['after_closed_matrix']['total'],'changed',len(r['changed_pairs']),'saved',p.stat().st_size)
