"""Third visible exterior,exact positive35 supplier and bounded short-side daisy."""
from dataclasses import asdict,replace
from hashlib import sha256
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import equality,matrix
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.outside_half_lantern import _matches
from surface_diagrams.posthalf_third_exterior import expose_posthalf_third_exterior
ROOT=Path(__file__).resolve().parents[1]


def report():
    path=ROOT/'docs/proofs/six-seven-posthalf-upper-cabled.json';old=json.loads(path.read_text(encoding='utf-8'));source=tuple(factor_from_data(f) for f in old['route']['factors']);by={f.id:f for f in source};route=expose_posthalf_third_exterior(source);target=factor_from_data(old['next_standard_exterior_daisy_target']['needed35']);actor=by['reflected.inner125'];probes=[]
    for sign in (-1,1):
        word=actor.word if sign==1 else inverse_word(actor.word);candidate=replace(by['reflected.output.1'],conjugator=reduce_word(word+by['reflected.output.1'].conjugator));split=split_fixed_last_strand(candidate.word,5)
        if exact_action(candidate.word,5)!=exact_action(split.reconstructed_word,5):raise ValueError('Keep full hypothetical candidate kernel AND shadow')
        probes.append(dict(sign=sign,actual_actor=actor,candidate=candidate,exact_class_comparison=equality(candidate.word,target.word),support_length=len(supported_class(candidate.mapping_class,5)),full_point_pushing=split,applied=sign==1))
    if probes[0]['exact_class_comparison']['equal'] or not probes[1]['exact_class_comparison']['equal']:raise ValueError('Retain exact positive supplier and scoped inverse failure')
    positive_after=next(f for f in route['stages'][1]['factors'] if f.id=='reflected.output.1');positive_match=_matches((positive_after,),(probes[1]['candidate'],))
    for stage in route['stages']:
        w=stage.get('named_pattern_witness')
        if not w:continue
        actual=stage['local_before']+stage['local_after'];normalized=tuple(replace(f,conjugator=reduce_word(inverse_word(w['common_chart'])+f.conjugator)) for f in actual)
        splits=tuple(dict(actual=f,split=split_fixed_last_strand(f.word,5)) for f in actual+normalized)
        for x in splits:
            if exact_action(x['actual'].word,5)!=exact_action(x['split'].reconstructed_word,5):raise ValueError('Keep FULL local/normalized kernels AND shadows')
        w['normalized_actual_inputs_and_outputs']=normalized;w['complete_actual_and_normalized_point_pushing']=splits
    before=matrix(source);interchange=matrix(route['stages'][1]['factors']);lookup={x['ids']:x['number'] for x in before['pairs']};changes=tuple(dict(ids=x['ids'],before=lookup[x['ids']],after=x['number'],delta=x['number']-lookup[x['ids']]) for x in interchange['pairs'] if lookup[x['ids']]!=x['number']);end={f.id:f for f in route['factors']}
    return dict(source_file=path.name,source_sha256=sha256(path.read_bytes()).hexdigest(),source_ref='route.factors',route=route,before_closed_matrix=before,first_interchange_closed_matrix=interchange,first_interchange_changed_pairs=changes,after_closed_matrix=matrix(route['factors']),exact_125_on35_probes=tuple(probes),actual_positive_normalized_match=positive_match,next_ordered_target_only=dict(actual_inputs=tuple(end[n] for n in ('alternative.return.0','alternative.return.1','alternative.return.2','outer.loan.1')),test_performed=False,applied=False,requires_every_actual_ordered_match=True,scope='ActualR134,old45,old35,old15 are adjacent in the residual and have four-point daisy support incidence. FIRST test exact NECESSARY ORDERED relation/common PC chart BEFORE any transport. No chart,substitution,fourth exterior or named residual closure claimed;sets alone are insufficient.'),posthalf_combined_operations=old['posthalf_combined_operations']+7,posthalf_combined_adjacent_checks=old['posthalf_combined_adjacent_checks']+7,research_prefix_operation_count_at_checkpoint=98,preferred_moves=101,preferred_steps=71,public_replay_changed=False,scope='SEVEN positive DISK moves/SEVEN external checks reach THIRD VISIBLE UNIT exterior by actual125 action,an individually matched125 rose,commuting short-side transports andCYCLICD5daisy. The125donor remainsONE12petal;new25/new15 consumed,older125loans explicit. THREE-Iexteriors and residualD1/-I remain. No half,negativefactor,sphere redraw,cap or useful complete suffix join;preferred101/71 staysSOLVED/UNCHANGED. Long-side23failure UNAPPLIED. Inventories differ;totals descriptive,not arc/jointminimum/wholeproofbounds.')


if __name__=='__main__':
    r=report();p=ROOT/'docs/proofs/six-seven-posthalf-third-exterior.json'
    with p.open('w',encoding='utf-8',newline='\n') as f:json.dump(r,f,default=asdict,separators=(',',':'))
    print('Selected',r['route']['graphical_operations'],r['route']['after_score'],r['after_closed_matrix']['total'],r['after_closed_matrix']['maximum'],p.stat().st_size)