"""Source-pinned comparison of one or both spare-UP crossings."""
from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import equality,matrix
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import supported_class
from surface_diagrams.outside_half_lantern import _matches
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.posthalf_spare import gather_posthalf_spare
from surface_diagrams.projected_relations import pc_rose_terms
from surface_diagrams.sphere_actions import sphere_chain_certificate
ROOT=Path(__file__).resolve().parents[1]


def changes(before,after):
    old={p['ids']:p['number'] for p in before['pairs']}
    return tuple(dict(ids=p['ids'],before=old[p['ids']],after=p['number'],delta=p['number']-old[p['ids']]) for p in after['pairs'] if p['number']!=old[p['ids']])


def report():
    path=ROOT/'docs/proofs/six-seven-posthalf-petal.json';old=json.loads(path.read_text(encoding='utf-8'))
    source=tuple(factor_from_data(f) for f in old['route']['factors']);r=gather_posthalf_spare(source)
    selected=r['selected'];full=r['complete_gather_alternative'];by={f.id:f for f in selected['factors']}
    matrices=tuple(matrix(fs) for fs in (source,selected['factors'],full['factors']))
    improved=changes(matrices[0],matrices[1]);alternative=changes(matrices[0],matrices[2])
    if len(improved)!=11 or any(p['delta']>=0 or 'F10.2' not in p['ids'] for p in improved):raise ValueError('Every selected changed pair must decrease, entry by entry')
    lengths=tuple(len(supported_class(next(f for f in fs if f.id=='F10.2').mapping_class,5)) for fs in (source,selected['factors']))
    # Concrete next donor target: the newly simpler245 root has ROUND45 as
    # its final PC rose petal. No expansion or supplier return is applied.
    donor=by['F10.2'];pattern=Factor('target.R245',(-1,-1,2),3,3);_matches((donor,),(pattern,))
    terms=tuple(Factor('target.loan.'+str(i),t.conjugator,t.first,t.points,t.power,t.half) for i,t in enumerate(pc_rose_terms(pattern.mapping_class)))
    round45=Factor('target.round45',(),4,2);_matches(terms[-1:],(round45,))
    local=reduce_word(donor.word+inverse_word(product(terms)));sphere=sphere_chain_certificate(local);lift=homology_action(local)
    if not equality(donor.word,product(terms))['equal'] or not sphere['certified'] or lift!=IDENTITY:raise ValueError('Retain the target named disk relation and separate sphere/+I checks')
    previous=json.loads((ROOT/'docs/proofs/six-seven-posthalf-exterior.json').read_text(encoding='utf-8'))
    supplier=next(s for s in previous['route']['stages'] if s['title']=='The actual145 PC rose lends45 and retains its matched spare petal')
    original=tuple(factor_from_data(f) for f in supplier['local_after']);parent=factor_from_data(supplier['local_before'][0])
    matches=_matches((by['posthalf.supply.0'],by['posthalf.supply.1']),original[:2])
    _matches(original[-1:],(round45,))
    target_splits=tuple(dict(actual=f,split=split_fixed_last_strand(f.word,5)) for f in (donor,)+terms+(parent,)+original)
    for entry in target_splits:
        if not equality(entry['actual'].word,entry['split'].reconstructed_word)['equal']:raise ValueError('Target keeps complete kernels/shadows and reconstructions')
    return dict(source_file=path.name,source_sha256=sha256(path.read_bytes()).hexdigest(),source_ref='route.factors',route=selected,complete_gather_alternative=full,
        before_closed_matrix=matrices[0],selected_closed_matrix=matrices[1],complete_gather_closed_matrix=matrices[2],selected_changed_pairs=improved,complete_gather_changed_pairs=alternative,F10_support_lengths=lengths,
        new_round45_donor_target=dict(actual_donor=donor,common_chart=pattern.conjugator,individually_matched_parent=_matches((donor,),(pattern,)),hypothetical_outputs=terms,round45_match=_matches(terms[-1:],(round45,)),disk_discrepancy=local,sphere_certificate=sphere,chosen_lift=lift,signed_pc_balance=tuple((1 if j in enclosed_boundaries(donor.mapping_class,5) else 0)-sum(t.power for t in terms if j in enclosed_boundaries(t.mapping_class,5)) for j in range(1,6)),original145_parent=parent,original145_source_outputs=original,current_first_two_supplier_matches=matches,complete_point_pushing=target_splits,applied=False,requires_bounded_supply_gather_and_useful_join=True,scope='The selected changed F10 now has a ROUND45 petal. The two original145 supplier petals still match individually but are separated by P13; the transported15 spare also lies between them and the new donor. No donor expansion,45 transport,supplier return or complete join is reached. Do not infer a contraction from the enclosed sets.'),
        posthalf_combined_operations=old['posthalf_combined_operations']+1,posthalf_combined_adjacent_checks=old['posthalf_combined_adjacent_checks']+1,research_prefix_operation_count_at_checkpoint=59,preferred_moves=101,preferred_steps=71,public_replay_changed=False,
        scope=r['scope']+' The full gather does not change the previously excluded unchanged135 triangle into a rose. All CLOSED counts are pairwise minima, not arc intersections or a jointly minimal drawing. Fixed-chart support lengths and stored braid lengths are not whole-proof geometric complexity bounds.')


if __name__=='__main__':
    r=report();p=ROOT/'docs/proofs/six-seven-posthalf-spare.json'
    with p.open('w',encoding='utf-8',newline='\n') as f:json.dump(r,f,default=asdict,separators=(',',':'))
    print('F10',r['F10_support_lengths'],'CLOSED',*[r[k]['total'] for k in ('before_closed_matrix','selected_closed_matrix','complete_gather_closed_matrix')],p.stat().st_size)
