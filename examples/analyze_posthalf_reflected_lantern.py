"""Actual reflected cabled lantern; donor petals and the odd exterior stay visible."""
from dataclasses import asdict,replace
from hashlib import sha256
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import equality,matrix
from examples.analyze_posthalf_cyclic_rose import commutators
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.factorization_explorer import product
from surface_diagrams.mapping_classes import supported_class,exact_action
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.posthalf_reflected_lantern import expose_posthalf_second_exterior
ROOT=Path(__file__).resolve().parents[1]


def report():
    path=ROOT/'docs/proofs/six-seven-posthalf-cyclic-rose.json';old=json.loads(path.read_text(encoding='utf-8'));source=tuple(factor_from_data(f) for f in old['route']['factors']);by={f.id:f for f in source}
    first=by['posthalf.return.R123'];q=by['outer.loan.2'];target=replace(first,conjugator=reduce_word(q.word+first.conjugator));block=(by['cyclic135.supply.2'],by['cyclic135.supply.0']);candidate=replace(first,conjugator=reduce_word(inverse_word(product(block))+first.conjugator));comparison=equality(candidate.word,target.word)
    if comparison['equal']:raise ValueError('The retained scoped inverse-block failure changed')
    inverse_probe=dict(actual_first_root=first,ordered_block=block,precise_needed_first_root=target,candidate=candidate,support_length=len(supported_class(candidate.mapping_class,5)),exact_class_comparison=comparison,full_candidate_point_pushing=split_fixed_last_strand(candidate.word,5),applied=False)
    route=expose_posthalf_second_exterior(source);end={f.id:f for f in route['factors']};before,after=matrix(source),matrix(route['factors'])
    for stage in route['stages']:
        witness=stage.get('named_pattern_witness')
        if not witness:continue
        actual=stage['local_before']+stage['local_after'];chart=witness['common_chart'];normalized=tuple(replace(f,conjugator=reduce_word(inverse_word(chart)+f.conjugator)) for f in actual)
        splits=tuple(dict(actual=f,split=split_fixed_last_strand(f.word,5)) for f in actual+normalized)
        for x in splits:
            if exact_action(x['actual'].word,5)!=exact_action(x['split'].reconstructed_word,5):raise ValueError('Retain full local AND normalized kernels/shadows')
        witness['normalized_actual_inputs_and_outputs']=normalized;witness['complete_actual_and_normalized_point_pushing']=splits
    result=dict(source_file=path.name,source_sha256=sha256(path.read_bytes()).hexdigest(),source_ref='route.factors',route=route,before_closed_matrix=before,after_closed_matrix=after,failed_inverse_fresh_block_probe=inverse_probe,posthalf_combined_operations=old['posthalf_combined_operations']+7,posthalf_combined_adjacent_checks=old['posthalf_combined_adjacent_checks']+3,research_prefix_operation_count_at_checkpoint=88,preferred_moves=101,preferred_steps=71,public_replay_changed=False,
        scope='Seven reached positive DISK moves/three external adjacent checks reach a SECOND VISIBLE unit exterior by THREE individually matched named substitutions. The123 donor stays TWO petals;12 is consumed,not returned. Fresh34 is consumed in the second exterior;fresh45 and BOTH older125 loan petals stay. Both exteriors have-I lift;their residual has+I and diagnostic boundary-square action,NOT a named closure or complete suffix join. Intermediate15records,7/64;final14records and all CLOSED totals separately retained. Inventories differ,so descriptive totals are NOT entrywise dominance,arc crossings,joint-minimum or whole-proof bounds. No half,negativefactor,sphere redraw or cap. Preferred101moves/71steps remains SOLVED/UNCHANGED.')

    result['next_ordered_target_only']=dict(actual_inputs=tuple(end[n] for n in ('reflected.inner125','alternative.prepare.F5.2','cyclic135.supply.2')),test_performed=False,requires_exact_ordered_relation_and_individual_common_chart_before_transport=True,applied=False,scope='Actual125 root,current124 root,and freshROUND45 have the support incidence of a four-point cabled lantern. No necessary ordered relation,common chart,gather or substitution is claimed. Test BEFORE any transport;sets alone are insufficient.')
    return result

if __name__=='__main__':
    r=report();path=ROOT/'docs/proofs/six-seven-posthalf-reflected-lantern.json'
    with path.open('w',encoding='utf-8',newline='\n') as f:json.dump(r,f,default=asdict,separators=(',',':'))
    print('Selected',r['route']['graphical_operations'],r['route']['after_score'],r['after_closed_matrix']['total'],r['after_closed_matrix']['maximum'],path.stat().st_size)