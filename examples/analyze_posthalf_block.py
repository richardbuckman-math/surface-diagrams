"""Exact ordered-block geometry improvement with honest transient comparisons."""
from dataclasses import asdict,replace
from hashlib import sha256
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import matrix,equality
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.disk_intersection import disk_intersection_certificate
from surface_diagrams.early_boundary_pure import _score
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import supported_class
from surface_diagrams.outside_half_lantern import _matches
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.posthalf_block import transport_posthalf_loan_block
from surface_diagrams.projected_relations import pc_rose_terms
from surface_diagrams.six_seven_structure import research_hurwitz_move
from surface_diagrams.sphere_actions import sphere_chain_certificate
ROOT=Path(__file__).resolve().parents[1]


def trajectory(route):
    matrices=[matrix(s['factors']) for s in route['stages']];word=max(s['score']['max_support_word'] for s in route['stages']);si=max(range(len(matrices)),key=lambda i:matrices[i]['total']);pi=max(range(len(matrices)),key=lambda i:(matrices[i]['maximum'],matrices[i]['total']))
    return dict(entries=tuple(dict(stage=i,score=s['score'],closed_total=m['total'],closed_maximum=m['maximum']) for i,(s,m) in enumerate(zip(route['stages'],matrices))),peak_support_word=word,peak_closed_sum=matrices[si]['total'],peak_closed_pair=matrices[pi]['maximum'],peak_sum_stage=si,peak_pair_stage=pi,peak_sum_certificate=matrices[si],peak_pair_certificate=matrices[pi])


def report():
    p=ROOT/'docs/proofs/six-seven-posthalf-outer.json';old=json.loads(p.read_text(encoding='utf-8'));source=tuple(factor_from_data(f) for f in old['route']['factors']);routes={k:transport_posthalf_loan_block(source,preparation=k) for k in ('direct','forward','inverse')};chosen=routes['inverse'];metrics={k:trajectory(r) for k,r in routes.items()};before,after=matrix(source),matrix(chosen['factors']);lookup={x['ids']:x['number'] for x in before['pairs']};changes=tuple(dict(ids=x['ids'],before=lookup[x['ids']],after=x['number'],delta=x['number']-lookup[x['ids']]) for x in after['pairs'] if lookup[x['ids']]!=x['number'])
    if len(changes)!=28 or any(x['delta']>=0 for x in changes):raise ValueError('Every changed CLOSED pair must improve,not just the total')
    joins=tuple(dict(route=k,individual_matches=_matches(r['factors'],chosen['factors']),literal_before_presentation_match=r['factors']==chosen['factors'],different_presentations=tuple(dict(id=a.id,left=a,right=b) for a,b in zip(r['factors'],chosen['factors']) if a!=b)) for k,r in routes.items())
    by={f.id:f for f in chosen['factors']};oldby={f.id:f for f in source};lengths=tuple(dict(id=n,before=len(supported_class(oldby[n].mapping_class,5)),after=len(supported_class(by[n].mapping_class,5))) for n in chosen['changed_record_ids'])
    target_path=ROOT/'docs/proofs/six-seven-posthalf-lantern-targets.json';saved=json.loads(target_path.read_text(encoding='utf-8'));required35=factor_from_data(saved['two_pair_lantern_target']['required_rose_petals'][2]);root=by['F8.2'];petals=tuple(Factor('round.supplier.'+str(i),t.conjugator,t.first,t.points) for i,t in enumerate(pc_rose_terms(root.mapping_class)));_matches(petals[1:2],(required35,));d=reduce_word(root.word+inverse_word(product(petals)));sphere=sphere_chain_certificate(d);lift=homology_action(d)
    if not equality(root.word,product(petals))['equal'] or not sphere['certified'] or lift!=IDENTITY:raise ValueError('The35 supplier remains a separately certified UNAPPLIED named target')
    actor=oldby['outer.loan.2'];wrong=oldby['alternative.return.2'];pair_probes=[]
    for sign in (1,-1):
        w=actor.word if sign==1 else inverse_word(actor.word);f=replace(wrong,conjugator=reduce_word(w+wrong.conjugator));pair_probes.append(dict(sign=sign,actor=actor,candidate=f,target=required35,comparison=equality(f.word,required35.word),support_length=len(supported_class(f.mapping_class,5)),applied=False))
    q13=factor_from_data(saved['two_pair_lantern_target']['required_rose_petals'][1]);failed13=[]
    for n in ('F8.2','alternative.S1'):
        for sign in (1,-1):
            w=q13.word if sign==1 else inverse_word(q13.word);f=replace(oldby[n],conjugator=reduce_word(w+oldby[n].conjugator));failed13.append(dict(source=oldby[n],conjugator=q13,sign=sign,candidate=f,support_length=len(supported_class(f.mapping_class,5)),required35_intersection=disk_intersection_certificate(f.mapping_class,required35.mapping_class,strands=5),applied=False))
    # The very next ordered-block crossing is rejected BEFORE any extension.
    i=next(i for i,f in enumerate(chosen['factors']) if f.id=='outer.loan.1');reject=research_hurwitz_move(chosen['factors'],i,i-1);score=_score(reject['factors'])
    if score['max_support_word']<=20:raise ValueError('The saved rejected extension changed')
    q12=Factor('round12',(),1,2);block_word=product(source[2:4]);block12=equality(block_word+q12.word,q12.word+block_word);wrong12=equality(wrong.word+q12.word,q12.word+wrong.word);target12=equality(required35.word+q12.word,q12.word+required35.word)
    if not block12['equal'] or wrong12['equal'] or not target12['equal']:raise ValueError('Keep the precise block/12 stabilizer scope')
    unchanged13=factor_from_data(saved['exact13_supplier']['actual_donor'])
    if by[unchanged13.id]!=unchanged13:raise ValueError('The old exact13 supplier remains literal')
    splits=tuple(dict(actual=f,split=split_fixed_last_strand(f.word,5)) for f in (root,)+petals)
    for x in splits:
        if not equality(x['actual'].word,x['split'].reconstructed_word)['equal']:raise ValueError('Keep complete supplier kernels/shadows')
    return dict(source_file=p.name,source_sha256=sha256(p.read_bytes()).hexdigest(),source_ref='route.factors',route=chosen,direct_comparison=routes['direct'],forward_comparison=routes['forward'],trajectory_comparisons=metrics,endpoint_presentation_joins=joins,before_closed_matrix=before,after_closed_matrix=after,changed_pairs=changes,changed_support_lengths=lengths,
        exact35_supplier=dict(actual_parent=root,canonical_outputs=petals,required_match=_matches(petals[1:2],(required35,)),disk_discrepancy=d,sphere_certificate=sphere,chosen_lift=lift,signed_pc_balance=tuple((1 if j in enclosed_boundaries(root.mapping_class,5) else 0)-sum(f.power for f in petals if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6)),complete_point_pushing=splits,applied=False,requires_bounded_gather_and_useful_named_payoff=True),
        unchanged13_supplier_reference=dict(source_file=target_path.name,source_sha256=sha256(target_path.read_bytes()).hexdigest(),source_ref='exact13_supplier',actual_donor=unchanged13,source_record_literal=True,applied=False),failed_new25_probes=tuple(pair_probes),failed_required13_preconditioners=tuple(failed13),rejected_next_block_extension=dict(crossed=chosen['factors'][i-1],raw_move=reject,score=score,applied=False),remaining_R135_target=dict(source_file=target_path.name,required_root=factor_from_data(saved['two_pair_lantern_target']['required_third_root']),required_petals=tuple(factor_from_data(f) for f in saved['two_pair_lantern_target']['required_rose_petals']),existing_root_matches=tuple(f.id for f in chosen['factors'] if f.points==3 and equality(f.word,factor_from_data(saved['two_pair_lantern_target']['required_third_root']).word)['equal']),existing_petal_matches=tuple(tuple(f.id for f in chosen['factors'] if f.points==2 and equality(f.word,factor_from_data(p).word)['equal']) for p in saved['two_pair_lantern_target']['required_rose_petals']),applied=False),block12_stabilizer=dict(actual_block=source[2:4],block_commutation=block12,wrong35_commutation=wrong12,required35_commutation=target12,scope='This block cannot conjugate oldwrong35 into the required curve because it fixes12. The reached transport instead changes the PARENT345 and supplies a DIFFERENT35 through an unapplied rose; no scope contradiction.'),
        posthalf_combined_operations=old['posthalf_combined_operations']+chosen['graphical_operations'],posthalf_combined_adjacent_checks=old['posthalf_combined_adjacent_checks']+chosen['adjacent_checks'],research_prefix_operation_count_at_checkpoint=63+chosen['graphical_operations'],preferred_moves=101,preferred_steps=71,public_replay_changed=False,
        scope='Same14 actual records at endpoints:four curves shorten and all28 changed CLOSED pairs decrease,63equal. Selected15moves/14checks has lower CLOSED trajectory peak532/46 than direct13moves/12checks536/52,wordpeak17both. Forward15 variant552/48 is unselected. Transient complexity still exceeds input524/34; no whole-proof bound or jointly minimal drawing is claimed. Endpoints have individually exact ordered presentations; direct/forward P13 presentations differ and are not called literal joins. Both actual15copies stay separate. No useful complete join or preferred proof change.')


if __name__=='__main__':
    r=report();p=ROOT/'docs/proofs/six-seven-posthalf-block.json'
    with p.open('w',encoding='utf-8',newline='\n') as f:json.dump(r,f,default=asdict,separators=(',',':'))
    print('Selected',r['route']['graphical_operations'],r['route']['adjacent_checks'],r['route']['after_score'],'CLOSED',r['after_closed_matrix']['total'],p.stat().st_size)
