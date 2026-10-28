"""Reached fixed-half midpoint route with a complete join; preferred replay unchanged."""
from dataclasses import asdict,replace
from hashlib import sha256
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import equality,matrix,score
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.factorization_explorer import product
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.puncture_boundary import BOUNDARY_WORD
from surface_diagrams.six_seven_structure import research_hurwitz_move
from surface_diagrams.sphere_actions import sphere_chain_certificate
ROOT=Path(__file__).resolve().parents[1]

def source():
    p=ROOT/'docs/proofs/six-seven-fifty-blocks/certificate.json'
    c=json.loads(p.read_text(encoding='utf-8'))['named_cyclic_start_shortening']['replacement_interval']
    return p,tuple(tuple(factor_from_data(f) for f in c[i]['factors']) for i in (4,5,6)),c[5]

def fixed_drag(fs,name,destination):
    """Keep the moving factor fixed; conjugate each crossed neighbor explicitly."""
    state=tuple(fs);start=next(f for f in state if f.id==name);atomic=[]
    while next(i for i,f in enumerate(state) if f.id==name)!=destination:
        i=next(i for i,f in enumerate(state) if f.id==name)
        move=research_hurwitz_move(state,i,i+(1 if i<destination else -1));state=move['factors']
        if score(state)['maximum']>20:raise ValueError('Reject an over-bound crossing before retaining it')
        atomic.append(dict(move,score=score(state)))
    if state[destination]!=start:raise ValueError('The moving half or pair must stay fixed')
    return state,tuple(atomic)

def certificate(fs):
    word=product(fs);sphere=sphere_chain_certificate(word);lift=homology_action(word)
    if exact_action(word,5)!=exact_action(BOUNDARY_WORD*4,5) or not sphere['certified'] or lift!=IDENTITY:raise ValueError('Retain all three complete checks')
    return dict(score=score(fs),sphere_certificate=sphere,chosen_lift=lift,exact_B5_boundary_fourth_power=True)

def neighborhood_splits(fs):
    result=[]
    for f in fs:
        # A half need not fix strand5. Split its CLOSED neighborhood, not an
        # illegally deleted half braid; keep the actual half word separately.
        closed=replace(f,half=False,power=1);split=split_fixed_last_strand(closed.word,5)
        if not equality(closed.word,split.reconstructed_word)['equal']:raise ValueError('Keep full nonabelian kernel AND shadow')
        result.append(dict(actual=f,actual_word=f.word,closed_neighborhood=closed,split=split))
    return tuple(result)

def report():
    p,(before,old_meeting,expected),old_stage=source();i,j=7,14
    if tuple(f.id for f in before[i:j+1])!=('F6','F8.2','alternative.S1','alternative.P13','alternative.F12.1','F10.2','alternative.T12.square','F11'):raise ValueError('Use the saved exact six-neighbor source')
    h=before[i]
    if not equality(h.word,before[j].word)['equal']:raise ValueError('The two original halves must already match')
    # These are FIXED-half carries, unlike the prior failed inverse carries,
    # which fixed the neighbors and changed the half twists.
    cases=[]
    for cut in range(7):
        a,left=fixed_drag(before,'F6',i+cut);b,right=fixed_drag(a,'F11',i+cut+1);m=matrix(b)
        if b[i+cut]!=before[i] or b[i+cut+1]!=before[j]:raise ValueError('Both actual halves stay literally fixed')
        cases.append(dict(cut=cut,score=score(b),closed_total=m['total'],closed_maximum=m['maximum'],factors=b,adjacent_checks=len(left)+len(right)))
    if not all(equality(a.word,b.word)['equal'] for a,b in zip(cases[0]['factors'],old_meeting)):raise ValueError('The cut0 comparison must individually match the original gather')
    cut=5;left_state,left=fixed_drag(before,'F6',i+cut)
    meeting,right=fixed_drag(left_state,'F11',i+cut+1)
    opposite_first,reverse_right=fixed_drag(before,'F11',j-1)
    other_order,reverse_left=fixed_drag(opposite_first,'F6',i+cut)
    if other_order!=meeting:raise ValueError('The disjoint carries must commute literally in both orders')
    pair=replace(h,id=expected[i].id,half=False)
    combined=meeting[:i+cut]+(pair,)+meeting[i+cut+2:]
    if not equality(product(meeting),product(combined))['equal']:raise ValueError('Combine only the same actual two halves')
    raw_join,tail=fixed_drag(combined,pair.id,i)
    matches=tuple(dict(raw=a,presentation=b,exact_B5=equality(a.word,b.word)) for a,b in zip(raw_join,expected))
    if len(raw_join)!=len(expected) or tuple(f.id for f in raw_join)!=tuple(f.id for f in expected) or not all(m['exact_B5']['equal'] for m in matches):raise ValueError('Every actual join factor must match separately')
    # The last transport uses the already checked source presentations. Its raw
    # transport word equality is retained BEFORE these individual B5 normalizations.
    # The combine has a separate B5 equality: the unchanged halves use different
    # raw presentations, so no whole-route free-word equality is asserted.
    raw_full_discrepancy=reduce_word(product(combined)+inverse_word(product(raw_join)))
    if raw_full_discrepancy:raise ValueError('The full-twist transport raw free cancellation must precede presentation matches')
    stages=(dict(kind='start',title='Same input before the fixed-half gather',factors=before),
            dict(kind='disk_hurwitz_block',title='Carry F6 DOWN over the first five neighbors; keep F6 fixed',factors=left_state,atomic_steps=left,adjacent_checks=5),
            dict(kind='disk_hurwitz_block',title='Carry F11 UP over the squared pair; keep F11 fixed',factors=meeting,atomic_steps=right,adjacent_checks=1),
            dict(kind='disk_combine',title='Combine the two unchanged actual half twists HERE',factors=combined),
            dict(kind='disk_hurwitz_block',title='Carry the combined full twist UP over five neighbors; literal complete join',factors=expected,atomic_steps=tail,adjacent_checks=5,raw_join=raw_join,raw_free_discrepancy=raw_full_discrepancy,individual_presentations=matches))
    retained=[]
    for n,s in enumerate(stages):
        retained.append(dict(stage=n,atomic=None,factors=s['factors'],certificate=certificate(s['factors'])))
        for k,a in enumerate(s.get('atomic_steps',())):retained.append(dict(stage=n,atomic=k,factors=a['factors'],certificate=certificate(a['factors'])))
    # Compare all atomic half-present states, not just two favored endpoints.
    new_half_states=(before,)+tuple(a['factors'] for a in left+right)
    old_half_states=(before,)+tuple(tuple(factor_from_data(f) for f in a['factors']) for a in old_stage['atomic_steps'])
    def trajectory(states):
        return tuple(dict(records=len(fs),half_ids=tuple(f.id for f in fs if f.half),score=score(fs),closed_total=(m:=matrix(fs))['total'],closed_maximum=m['maximum']) for fs in states)
    original_trajectory,new_trajectory=trajectory(old_half_states),trajectory(new_half_states)
    original_matrix,new_matrix=matrix(old_meeting),matrix(meeting)
    return dict(source_archive_sha256=sha256(p.read_bytes()).hexdigest(),source_refs=('named_cyclic_start_shortening.replacement_interval.4','named_cyclic_start_shortening.replacement_interval.5','named_cyclic_start_shortening.replacement_interval.6'),preferred_source_indices_at_checkpoint=(40,41,42),
        stages=stages,retained_state_certificates=tuple(retained),fixed_meeting_cut_measurements=tuple(cases),
        independent_carries=dict(first_interval=(7,12),second_interval=(13,14),same_input=before,left_then_right=meeting,right_then_left=other_order,literal_two_order_equality=True,reverse_atomic_steps=(reverse_right,reverse_left)),
        original_half_trajectory=original_trajectory,candidate_half_trajectory=new_trajectory,original_meeting_factors=old_meeting,original_meeting_matrix=original_matrix,candidate_meeting_matrix=new_matrix,
        complete_join=dict(raw=raw_join,target=expected,literal_after_individual_presentations=True,raw_transport_input=combined,raw_transport_free_discrepancy=raw_full_discrepancy,combine_disk_equality=equality(product(meeting),product(combined)),individual_matches=matches),
        neighborhood_kernel_splits=dict(before=neighborhood_splits(before),candidate_meeting=neighborhood_splits(meeting),joined=neighborhood_splits(expected)),
        original_local_moves=2,candidate_local_moves=4,original_adjacent_checks=6,candidate_adjacent_checks=11,sphere_moves=0,new_half_factors=0,public_replay_changed=False,preferred_moves=99,preferred_steps=70,
        scope='Reached positive bounded DISK route and complete join, not an adopted preferred change or a whole-proof tangle improvement. Both actual half classes stay literally unchanged. Same17-record CLOSED-neighborhood meeting counts improve1094/48 to936/36, while support maximum worsens17 to18. The later full-pair transport rejoins the original combined endpoint, so it restores the old geometric burden after the halves disappear. Five extra adjacent checks and two extra listed local moves are retained. The first two disjoint carries are independent in both orders, not a joint ambient-isotopy assertion. Closed-neighborhood counts are not arc crossings or a jointly attainable drawing minimum. Prior failed inverse carries fixed neighbors; this new route fixes the halves and changes neighbors.')

if __name__=='__main__':
    r=report();path=ROOT/'docs/proofs/six-seven-fixed-half-meeting.json'
    with path.open('w',encoding='utf-8',newline='\n') as f:json.dump(r,f,default=asdict,separators=(',',':'))
    print('Meeting',r['original_meeting_matrix']['total'],r['original_meeting_matrix']['maximum'],'->',r['candidate_meeting_matrix']['total'],r['candidate_meeting_matrix']['maximum'])
    print('Half-present trajectory peaks',max(s['closed_total'] for s in r['original_half_trajectory']),max(s['closed_total'] for s in r['candidate_half_trajectory']))
    print('Saved',path.stat().st_size,'bytes; preferred proof unchanged')
