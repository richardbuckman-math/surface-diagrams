"""Complete named residual suffix; preferred graphical derivation unchanged."""
from dataclasses import asdict,replace
from hashlib import sha256
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import matrix
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.posthalf_residual_closure import close_posthalf_residual
ROOT=Path(__file__).resolve().parents[1]


def report():
    path=ROOT/'docs/proofs/six-seven-posthalf-third-exterior.json';old=json.loads(path.read_text(encoding='utf-8'));source=tuple(factor_from_data(f) for f in old['route']['factors']);route=close_posthalf_residual(source)
    for stage in route['stages']:
        w=stage.get('named_pattern_witness')
        if not w:continue
        actual=stage['local_before']+stage['local_after'];normalized=tuple(replace(f,conjugator=reduce_word(inverse_word(w['common_chart'])+f.conjugator)) for f in actual)
        splits=tuple(dict(actual=f,split=split_fixed_last_strand(f.word,5)) for f in actual+normalized)
        for x in splits:
            if exact_action(x['actual'].word,5)!=exact_action(x['split'].reconstructed_word,5):raise ValueError('Keep FULL actual/normalized NONABELIAN kernels AND B4shadows')
        w['normalized_actual_inputs_and_outputs']=normalized;w['complete_actual_and_normalized_point_pushing']=splits
    result=dict(source_file=path.name,source_sha256=sha256(path.read_bytes()).hexdigest(),source_ref='route.factors',source_tail_audit='six-seven-posthalf-residual-targets.json',route=route,before_closed_matrix=matrix(source),after_closed_matrix=matrix(route['factors']),posthalf_combined_operations=old['posthalf_combined_operations']+6,posthalf_combined_adjacent_checks=old['posthalf_combined_adjacent_checks']+2,research_prefix_operation_count_at_checkpoint=104,preferred_moves=101,preferred_steps=71,public_replay_changed=False,scope='Complete named DISK residual closure inSIXpositive moves/TWOexternalchecks/FOURnamedsubstitutions;THREEinternalchecks retained. FOURSTANDARDUNITexteriorsremainvisible;no half,negativefactor,sphere redraw orcap. Complete disk suffix joins the existing terminal combine/fourth-power sphere cap separately;this is NOTshorter/adopted andthe preferred101/71 remainsSOLVED/UNCHANGED. Oldrecords/flags/sourcecharts untouched. Inventorytotalsdescriptive,not arc/jointminimum/wholeproofcomplexitybounds.')
    from examples.check_posthalf_route_join import audit_join
    result['route_join']=audit_join(final_closure_stages=route['stages'],final_closure_factors=route['factors'])
    return result


if __name__=='__main__':
    r=report();p=ROOT/'docs/proofs/six-seven-posthalf-residual-closure.json'
    with p.open('w',encoding='utf-8',newline='\n') as f:json.dump(r,f,default=asdict,separators=(',',':'))
    print('Complete',r['route']['graphical_operations'],r['route']['after_score'],r['route_join'].get('complete_source_operations'),p.stat().st_size)