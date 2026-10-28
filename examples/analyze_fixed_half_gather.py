"""Exact, source-pinned audit of the final half gather; no replay is changed."""
from dataclasses import asdict,replace
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.disk_intersection import disk_intersection_certificate
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.projected_relations import pc_daisy_terms,pc_half_lantern_terms
from surface_diagrams.six_seven_structure import research_hurwitz_move
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.hyperelliptic_homology import homology_action,IDENTITY
from surface_diagrams.sphere_actions import sphere_chain_certificate
ROOT=Path(__file__).resolve().parents[1]

def equality(a,b):
    aa,bb=exact_action(a,5),exact_action(b,5)
    return dict(equal=aa==bb,first_difference=next((dict(meridian=i+1,left=x,right=y) for i,(x,y) in enumerate(zip(aa,bb)) if x!=y),None))

def score(fs):
    ns=[len(supported_class(f.mapping_class,5)) for f in fs];return dict(maximum=max(ns),total=sum(ns))

def matrix(fs):
    pairs=[]
    for a,b in combinations(sorted(fs,key=lambda f:f.id),2):
        cert=disk_intersection_certificate(replace(a.mapping_class,half=False,power=1),replace(b.mapping_class,half=False,power=1),strands=5)
        pairs.append(dict(ids=(a.id,b.id),number=cert['intersection_number'],certificate=cert))
    return dict(pairs=tuple(pairs),total=sum(p['number'] for p in pairs),maximum=max(p['number'] for p in pairs))

def report():
    path=ROOT/'docs/proofs/six-seven-fifty-blocks/certificate.json';c=json.loads(path.read_text(encoding='utf-8'))
    source=c['named_cyclic_start_shortening']['replacement_interval'];before,after=[tuple(factor_from_data(f) for f in source[i]['factors']) for i in (4,5)]
    by_after={f.id:f for f in after};i=next(i for i,f in enumerate(before) if f.id=='F6');j=next(i for i,f in enumerate(before) if f.id=='F11');a,b=before[i],before[j];block=before[i+1:j];k=product(block)
    if len(before)!=17 or len(block)!=6 or not equality(a.word,b.word)['equal']:raise ValueError('Use the exact saved matching-half source')
    comm=reduce_word(k+b.word+inverse_word(k)+inverse_word(b.word));split=split_fixed_last_strand(comm,5)
    if not equality(comm,split.reconstructed_word)['equal']:raise ValueError('The full commutator kernel/shadow reconstruction failed')
    cuts=[]
    for n in range(7):
        l,r=product(block[:n]),product(block[n:]);left=replace(a,conjugator=reduce_word(inverse_word(l)+a.conjugator));right=replace(b,conjugator=reduce_word(r+b.conjugator))
        fs=before[:i]+block[:n]+(left,right)+block[n:]+before[j+1:]
        discrepancy=reduce_word(product(before)+inverse_word(product(fs)))
        if discrepancy:raise ValueError('The hypothetical two-sided inverse transport lost its free-word equality')
        cuts.append(dict(cut=n,left=left,right=right,half_equality=equality(left.word,right.word),support_lengths=(len(supported_class(left.mapping_class,5)),len(supported_class(right.mapping_class,5))),free_word_discrepancy=discrepancy,applied=False))
    neighbors=[]
    for f in block:
        negative=replace(f,conjugator=reduce_word(inverse_word(b.word)+f.conjugator));positive=replace(f,conjugator=reduce_word(b.word+f.conjugator))
        match=equality(negative.word,by_after[f.id].word)
        if not match['equal']:raise ValueError('An actual gathered neighbor lost its individual match')
        neighbors.append(dict(actual_before=f,actual_after=by_after[f.id],exact_negative_half_conjugation=match,
            half_commutation=equality(f.word+b.word,b.word+f.word),half_neighborhood_intersection=disk_intersection_certificate(replace(b.mapping_class,half=False),f.mapping_class,strands=5),
            support_before=len(supported_class(f.mapping_class,5)),support_after=len(supported_class(negative.mapping_class,5)),unapplied_positive_sign_support=len(supported_class(positive.mapping_class,5))))
    m0,m1=matrix(before),matrix(after);old={p['ids']:p['number'] for p in m0['pairs']};changes=tuple(dict(ids=p['ids'],before=old[p['ids']],after=p['number'],delta=p['number']-old[p['ids']]) for p in m1['pairs'] if p['number']!=old[p['ids']])
    # The complementary cyclic-side fixed-half route has only this bounded prefix.
    state=before[j:]+before[:j];frame=inverse_word(product(before[:j]));cyclic=reduce_word(frame+product(before)+inverse_word(frame)+inverse_word(product(state)))
    if cyclic:raise ValueError('The cyclic start needs its complete raw common frame')
    partial=[dict(factors=state,score=score(state))];position=0;rejected=None
    while state[position+1].id!='F6':
        move=research_hurwitz_move(state,position,position+1);candidate=move['factors'];entry=dict(crossed=state[position+1].id,move=move,score=score(candidate))
        if entry['score']['maximum']>20:rejected=entry;break
        state=candidate;partial.append(dict(entry,factors=state));position+=1
    for entry in partial:
        word=product(entry['factors']);entry['sphere_certificate']=sphere_chain_certificate(word);entry['chosen_lift']=homology_action(word)
        if not entry['sphere_certificate']['certified'] or entry['chosen_lift']!=IDENTITY:raise ValueError('A retained partial state lost its sphere/lift check')
    # A jointly certified new root can be lent by the ACTUAL four-point outer.
    outer=next(f for f in before if f.id=='alternative.O1234');chart=a.conjugator+(a.first,);parent=Factor('target.parent',chart,1,4);terms=pc_daisy_terms(parent.mapping_class)
    parent_match=equality(outer.word,parent.word)
    if not parent_match['equal'] or not equality(outer.word,tuple(x for t in terms for x in t.word))['equal']:raise ValueError('The donor PC daisy failed its joint chart')
    root=Factor('target.R125',terms[0].conjugator,terms[0].first,terms[0].points);half_pattern=pc_half_lantern_terms(root.mapping_class);square=block[-1]
    local=reduce_word(outer.word+inverse_word(tuple(x for t in terms for x in t.word)));local_sphere=sphere_chain_certificate(local);local_lift=homology_action(local)
    if not local_sphere['certified'] or local_lift!=IDENTITY:raise ValueError('Retain the donor disk relation and its separate sphere/lift check')
    for t in (parent.mapping_class,)+terms:
        if not equality(t.word,split_fixed_last_strand(t.word,5).reconstructed_word)['equal']:raise ValueError('Retain the donor full kernel and shadow')
    donor=dict(disk_discrepancy=local,sphere_certificate=local_sphere,chosen_lift=local_lift,actual_outer=outer,common_chart=chart,parent_match=parent_match,canonical_daisy_outputs=terms,
        root=root,root_actual_unit_matches=tuple(f.id for f in before if not f.half and equality(replace(f,power=1).word,root.word)['equal']),
        half_lantern_pattern=half_pattern,first_half_match=equality(b.word,half_pattern[0].word),actual_square_match=equality(square.word,half_pattern[2].word),
        second_half_existing_matches=tuple(f.id for f in before if f.half and equality(f.word,half_pattern[1].word)['equal']),
        full_daisy_splits=tuple(split_fixed_last_strand(t.word,5) for t in (parent.mapping_class,)+terms),
        framed_balance_before_minus_after=tuple((1 if z in enclosed_boundaries(outer.mapping_class,5) else 0)-sum(t.power for t in terms if z in enclosed_boundaries(t,5)) for z in range(1,6)),
        applied=False,requires_transport_and_useful_join=True)
    q=replace(square,power=1);kunit=product(block[:-1])+q.word;cut5=cuts[5];wrong=(cut5['left'],cut5['right'],square);wrong_product=product(wrong)
    if a.first!=1 or not donor['first_half_match']['equal'] or not donor['actual_square_match']['equal']:raise ValueError('Retain the canonical first-half chart and actual square match')
    unit_probe=dict(block_with_one_square_unit=kunit,centralization=equality(kunit+b.word,b.word+kunit),hypothetical_half_lantern_inputs=wrong,product_centralizes_inputs=tuple(equality(wrong_product+f.word,f.word+wrong_product) for f in wrong),applied=False)
    return dict(unit_square_probe=unit_probe,source_archive_sha256=sha256(path.read_bytes()).hexdigest(),source_refs=('named_cyclic_start_shortening.replacement_interval.4','named_cyclic_start_shortening.replacement_interval.5'),preferred_source_indices_at_checkpoint=(40,41),
        before=before,after=after,actual_half_equality=equality(a.word,b.word),ordered_block=block,block_word=k,block_half_commutation=equality(k+b.word,b.word+k),
        full_commutator=comm,commutator_split=split,inverse_gather_cuts=tuple(cuts),neighbor_changes=tuple(neighbors),closed_matrix_before=m0,closed_matrix_after=m1,changed_pairs=changes,
        actual_scores=(score(before),score(after)),unapplied_common_H_chart_score=score(tuple(replace(f,conjugator=reduce_word(b.word+f.conjugator)) for f in after)),complementary_side=dict(frame=frame,raw_cyclic_discrepancy=cyclic,retained_prefix=tuple(partial),rejected_candidate=rejected,reached_matching_gather=False),donor_target=donor,
        public_replay_changed=False,scope='This audits the saved fixed gather and excludes only seven direct two-sided inverse carries that keep the ordered intervening factors unchanged. Other Hurwitz loops, outside interactions, substitutions and sphere redraws are not excluded. All intersection numbers concern CLOSED neighborhood curves, not arcs or a jointly minimal drawing. Hypothetical inverse endpoints and the new donor target are UNAPPLIED; the complementary-side prefix stops before its rejected sixth crossing.')

if __name__=='__main__':
    r=report();p=ROOT/'docs/proofs/six-seven-fixed-half-gather.json'
    with p.open('w',encoding='utf-8',newline='\n') as f:json.dump(r,f,default=asdict,separators=(',',':'))
    print('Block centralizes half:',r['block_half_commutation']['equal'],'cuts',[c['half_equality']['equal'] for c in r['inverse_gather_cuts']])
    print('Closed crossings',r['closed_matrix_before']['total'],'->',r['closed_matrix_after']['total'],'max',r['closed_matrix_before']['maximum'],'->',r['closed_matrix_after']['maximum'],'changed pairs',len(r['changed_pairs']))
    print('Saved',p.name,p.stat().st_size,'bytes; preferred proof/PDF unchanged')
