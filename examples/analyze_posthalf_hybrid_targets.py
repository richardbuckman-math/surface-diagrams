"""A source-pinned two-outer cabled target; no hybrid move is applied."""
from dataclasses import asdict,replace
from hashlib import sha256
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import equality
from examples.analyze_posthalf_cyclic_rose import commutators
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.outside_half_lantern import _matches
from surface_diagrams.outside_rose_return import _transport
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.sphere_actions import sphere_chain_certificate
ROOT=Path(__file__).resolve().parents[1]


def report():
    path=ROOT/'docs/proofs/six-seven-posthalf-upper-cabled.json';old=json.loads(path.read_text(encoding='utf-8'));source=tuple(factor_from_data(f) for f in old['route']['factors']);by={f.id:f for f in source};hyp=Factor('target.HYPOTHETICAL.O1345',(1,),2,4);proposed=(by['upper.O1234'],hyp,by['outer.loan.2']);noncentral=commutators(proposed)
    if any(x['left']==x['right'] for x in noncentral):raise ValueError('Keep all three exact nonzero ordered-target witnesses')
    proof_path=ROOT/'docs/proofs/six-seven-posthalf-exterior.json';proof=json.loads(proof_path.read_text(encoding='utf-8'));w=proof['route']['stages'][-1]['named_pattern_witness'];base=tuple(factor_from_data(f) for f in w['canonical_base']);outputs=(Factor('canonical.D5',(),1,5),Factor('canonical.R123',(),1,3))
    if not equality(product(base),product(outputs))['equal']:raise ValueError('Keep the retained named canonical-base order')
    chart=(-2,-3);inputs=_transport(base,chart);after=_transport(outputs,chart);outer_matches=_matches((by['upper.O1234'],hyp),(inputs[0],inputs[2]));pair_miss=equality(by['outer.loan.2'].word,inputs[1].word)
    if pair_miss['equal']:raise ValueError('The required25 must stay distinct from actual older25')
    opposite=(2,3);opposite_inputs=_transport(base,opposite);opposite_pair_matches=_matches((by['upper.O1234'],by['outer.loan.2']),opposite_inputs[:2]);opposite_outer_miss=equality(hyp.word,opposite_inputs[2].word)
    if opposite_outer_miss['equal']:raise ValueError('The opposite chart does not match the hypothetical outer')
    discrepancy=reduce_word(product(inputs)+inverse_word(product(after)));sphere=sphere_chain_certificate(discrepancy);lift=homology_action(discrepancy)
    if not sphere['certified'] or lift!=IDENTITY:raise ValueError('Retain target-only separate sphere/+I discrepancy')
    normalized=tuple(replace(f,conjugator=reduce_word(inverse_word(chart)+f.conjugator)) for f in inputs+after)
    split_items=source+(hyp,)+inputs+after+normalized;splits=tuple(dict(actual=f,split=split_fixed_last_strand(f.word,5)) for f in split_items)
    for x in splits:
        if exact_action(x['actual'].word,5)!=exact_action(x['split'].reconstructed_word,5):raise ValueError('Keep FULL source/target NONABELIAN kernels AND B4 shadows')
    return dict(source_file=path.name,source_sha256=sha256(path.read_bytes()).hexdigest(),source_ref='route.factors',source_factors=source,failed_proposed_order=dict(actual_outer=by['upper.O1234'],hypothetical_outer=hyp,actual_older25=by['outer.loan.2'],proposed_hypothetical_order=proposed,exact_integral_commutators=noncentral,faithful_output_miss=equality(product(proposed),product(after)),applied=False,scope='HYPOTHETICAL target test only;the second outer is NOT a reached source factor. Only this prescribed unchanged ordered product is excluded,not outside transports,new patterns or sphere changes.'),two_outer_named_target=dict(common_chart=chart,canonical_base=base,canonical_outputs=outputs,inputs=inputs,outputs=after,individual_two_outer_matches=outer_matches,required25=inputs[1],actual_older25_miss=pair_miss,correct_order='actualO1234,REQUIRED25,hypotheticalO1345',retained_source_named_witness=w,source_witness_file=proof_path.name,source_witness_ref='route.stages.14.named_pattern_witness',source_witness_sha256=sha256(proof_path.read_bytes()).hexdigest(),disk_discrepancy=discrepancy,sphere_certificate=sphere,chosen_lift=lift,signed_pc_balance=tuple(sum(f.power for f in inputs if j in enclosed_boundaries(f.mapping_class,5))-sum(f.power for f in after if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6)),applied=False,scope='Both outer curves separately match in the complete chart,but the needed25 is not actual older25 and correct named order isO,Q,O,notO,O,Q. No three-input cluster,gather,substitution or hybrid is reached. Source witness charts/flags remainSOURCE data,separate from this target chart.'),opposite_chart_probe=dict(chart=opposite,individual_actualO_and_older25_matches=opposite_pair_matches,hypothetical_outer_miss=opposite_outer_miss,applied=False),full_source_target_normalized_point_pushing=splits,next_available_pair_product_target=dict(actual_ordered_members=(by['reflected.loan.2'],by['upper.I24']),source_positions=(source.index(by['reflected.loan.2']),source.index(by['upper.I24'])),actual_older25=by['outer.loan.2'],precise_required25=inputs[1],both_signs_tested=False,block_gathered=False,applied=False,scope='FIRST compare both signs of the FULL ordered old23,I24 product on actual older25 against this precise required25,with class/support BEFORE any gather. The two actors are NOT currently adjacent;no product transport or supply is reached.'),actual_source_moves=0,sphere_moves=0,exterior_caps=0,preferred_moves=101,preferred_steps=71,adopted=False,public_replay_changed=False,scope='Exact target/obstruction audit only. ZERO source moves or new graphics. Preferred101/71 and the complete alternative remainSOLVED/UNCHANGED. All three purported inputs are never described as a reached cluster;the second outer remainsHYPOTHETICAL. Full source kernels/shadows are retained;no ancestry/set inference or negative factor introduced.')


if __name__=='__main__':
    r=report();p=ROOT/'docs/proofs/six-seven-posthalf-hybrid-targets.json'
    with p.open('w',encoding='utf-8',newline='\n') as f:json.dump(r,f,default=asdict,separators=(',',':'))
    print('Target only',p.stat().st_size)