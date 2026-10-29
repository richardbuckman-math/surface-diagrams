"""Unapplied exact lantern/petal targets and scoped new-triangle exclusion."""
from dataclasses import asdict,replace
from hashlib import sha256
from itertools import permutations,combinations
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import equality
from examples.analyze_posthalf_petal import multiply
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.disk_intersection import disk_intersection_certificate
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.named_two_pair_cabled import two_pair_cabled_lantern
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.outside_half_lantern import _matches
from surface_diagrams.outside_rose_return import _terms,_transport
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.projected_relations import pc_rose_terms
from surface_diagrams.sphere_actions import sphere_chain_certificate
from surface_diagrams.twist_simplify import simplify_twist
ROOT=Path(__file__).resolve().parents[1]


def report():
    path=ROOT/'docs/proofs/six-seven-posthalf-outer.json';old=json.loads(path.read_text(encoding='utf-8'));fs=tuple(factor_from_data(f) for f in old['route']['factors']);by={f.id:f for f in fs}
    selected=tuple(by[n] for n in ('alternative.P13','alternative.return.2','outer.loan.1'));orders=[]
    for order in permutations(selected):
        p=homology_action(product(order));witnesses=[]
        for f in order:
            a=homology_action(f.word);left,right=multiply(p,a),multiply(a,p);witnesses.append(dict(actual=f,product_lift=p,input_lift=a,left=left,right=right,commutes=left==right))
        if all(w['commutes'] for w in witnesses):raise ValueError('A zero linear commutator is inconclusive,never an exclusion')
        orders.append(dict(order=tuple(f.id for f in order),noncentrality_witnesses=tuple(witnesses)))
    pairs=tuple(dict(ids=(a.id,b.id),certificate=disk_intersection_certificate(a.mapping_class,b.mapping_class,strands=5)) for a,b in combinations(selected,2))
    chart=(-3,-4,-3,-2);pattern=two_pair_cabled_lantern(chart=chart);actual=(by['outer.O1245'],by['alternative.prepare.F5.1']);matches=_matches(actual,pattern['inputs'][:2]);missing=pattern['inputs'][2]
    normalized=tuple(replace(f,conjugator=reduce_word(inverse_word(chart)+f.conjugator)) for f in actual);_matches(normalized,pattern['canonical_inputs'][:2])
    old_chart=by['outer.O1245'].conjugator;source_normalized=replace(actual[1],conjugator=reduce_word(inverse_word(old_chart)+actual[1].conjugator));source_split=split_fixed_last_strand(source_normalized.word,5)
    required_petals=_terms(missing.mapping_class,'required.',pc_rose_terms);existing=tuple(dict(required=p,matches=tuple(f.id for f in fs if f.points==2 and equality(f.word,p.word)['equal'])) for p in required_petals)
    target_intersections=tuple(dict(actual=f,certificate=disk_intersection_certificate(missing.mapping_class,f.mapping_class,strands=5)) for f in selected+(by['posthalf.supply.0'],))
    # A precise13 supplier is a TARGET ONLY. Its two full normalized kernel
    # loops vanish; the B3 shadow is retained rather than guessed from sets.
    donor=by['posthalf.return.R123'];required13=required_petals[1];n13=replace(required13,conjugator=reduce_word(inverse_word(donor.conjugator)+required13.conjugator));s5=split_fixed_last_strand(n13.word,5);s4=split_fixed_last_strand(s5.shadow_word,4)
    if s5.kernel_loop or s4.kernel_loop:raise ValueError('Keep BOTH normalized supplier kernels')
    if not equality(n13.word,s5.reconstructed_word)['equal']:raise ValueError('Keep the B5 reconstruction')
    if exact_action(s5.shadow_word,4)!=exact_action(s4.reconstructed_word,4):raise ValueError('Keep the B4 reconstruction')
    parent=replace(donor,conjugator=reduce_word(donor.conjugator+(-2,-2)));_matches((donor,),(parent,));donor_petals=_terms(parent.mapping_class,'supplier13.',pc_rose_terms);_matches(donor_petals[1:2],(required13,))
    local=reduce_word(donor.word+inverse_word(product(donor_petals)));sphere=sphere_chain_certificate(local);lift=homology_action(local)
    if not equality(donor.word,product(donor_petals))['equal'] or not sphere['certified'] or lift!=IDENTITY:raise ValueError('The unapplied supplier relation keeps separate exact checks')
    prior_path=ROOT/'docs/proofs/six-seven-posthalf-petal.json';prior=json.loads(prior_path.read_text(encoding='utf-8'));old35=factor_from_data(prior['correct_cabled_target']['required_pair']);_matches(required_petals[2:],(old35,))
    reused=prior['correct_cabled_target']['unchanged_triple_supplier_diagnostics']
    for entry in reused:
        f=factor_from_data(entry['actual'])
        if f!=by[f.id]:raise ValueError('Only reuse the old closed certificate for LITERALLY unchanged donors')
    probes=[];wrong=by['alternative.return.2'];conjugator=actual[1]
    for sign in (1,-1):
        g=conjugator.word if sign==1 else inverse_word(conjugator.word);candidate=replace(wrong,conjugator=reduce_word(g+wrong.conjugator));probes.append(dict(sign=sign,conjugator=conjugator,candidate=candidate,comparison=equality(candidate.word,old35.word),support_length=len(supported_class(candidate.mapping_class,5)),applied=False))
    complete=tuple(dict(actual=f,split=split_fixed_last_strand(f.word,5)) for f in fs+required_petals+(donor,)+donor_petals)
    for x in complete:
        if not equality(x['actual'].word,x['split'].reconstructed_word)['equal']:raise ValueError('Every actual/target full kernel AND shadow reconstructs')
    return dict(source_file=path.name,source_sha256=sha256(path.read_bytes()).hexdigest(),source_ref='route.factors',new15_triangle=dict(actual_inputs=selected,closed_pairs=pairs,orders=tuple(orders),gathered=False,scope='All6 exact integral product/input commutators are noncentral for these listed unchanged UNIT-factor orders. Selected-only disk Hurwitz/common conjugation cannot make an expanded PC rose. Outside changes,other substitutions,half/power splitting and sphere moves are NOT excluded.'),
        two_pair_lantern_target=dict(pattern=pattern,actual_inputs_matched=actual,individual_source_matches=matches,common_chart=chart,source_outer_chart=old_chart,inside_outer_rechart=(-3,-2),source_normalized234=source_normalized,source_normalized234_split=source_split,new_normalized_actual_inputs=normalized,new_normalized_splits=tuple(split_fixed_last_strand(f.word,5) for f in normalized),required_third_root=missing,existing_root_matches=tuple(f.id for f in fs if f.points==3 and equality(f.word,missing.word)['equal']),required_rose_petals=required_petals,existing_petal_matches=existing,actual_pair_root_intersections=target_intersections,applied=False,requires_new_third_root_and_bounded_ordered_gather=True),
        exact13_supplier=dict(actual_donor=donor,new_common_chart=parent.conjugator,internal_frame=(-2,-2),parent_match=_matches((donor,),(parent,)),outputs=donor_petals,exact_required13_match=_matches(donor_petals[1:2],(required13,)),normalized_required13=n13,normalized_split5=s5,normalized_split4=s4,simplified_normalized_required13=simplify_twist(n13.mapping_class,strands=5),disk_discrepancy=local,sphere_certificate=sphere,chosen_lift_discrepancy=lift,signed_pc_balance=tuple((1 if j in enclosed_boundaries(donor.mapping_class,5) else 0)-sum(p.power for p in donor_petals if j in enclosed_boundaries(p.mapping_class,5)) for j in range(1,6)),applied=False,requires_useful_bounded_transport_and_complete_join=True),
        required35_reuses_prior_target=dict(source_file=prior_path.name,source_sha256=sha256(prior_path.read_bytes()).hexdigest(),source_ref='correct_cabled_target',individual_match=_matches(required_petals[2:],(old35,)),unchanged_donor_diagnostics=reused),limited_unapplied_round234_probes=tuple(probes),complete_point_pushing=complete,graphical_operations_added=0,external_adjacent_checks_added=0,new_sphere_moves=0,exterior_caps=0,preferred_moves=101,preferred_steps=71,public_replay_changed=False,useful_complete_join_reached=False,
        scope='Research target/audit ONLY. No source factor changes,no expansion,gather,substitution or phase is applied. The common chart matches two actual lantern inputs,not a reached third root. The13 supplier is individually exact but UNEXPANDED; required35 is the known prior target with unchanged donors crossing it4times. Closed intersections are not arcs/joint minima. All preferred proof,payload,PDF and historical certificates remain unchanged.')


if __name__=='__main__':
    r=report();p=ROOT/'docs/proofs/six-seven-posthalf-lantern-targets.json'
    with p.open('w',encoding='utf-8',newline='\n') as f:json.dump(r,f,default=asdict,separators=(',',':'))
    print('Saved',p.stat().st_size,'bytes;6 noncentral orders;2 actual joint inputs;13 supplier target only')
