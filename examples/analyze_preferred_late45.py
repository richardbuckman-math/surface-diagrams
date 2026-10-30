"""Source-exact late45 loan and return for the preferred derivation."""
from dataclasses import asdict,replace
from hashlib import sha256
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import matrix
from examples.analyze_posthalf_hybrid_block import pushing
from examples.analyze_posthalf_split_block import _peak
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data,preferred_clarity_source
from surface_diagrams.factorization_explorer import product
from surface_diagrams.mapping_classes import supported_class
from surface_diagrams.preferred_late45 import close_preferred_late45
ROOT=Path(__file__).resolve().parents[1]


def report():
    folder=ROOT/'docs/proofs/six-seven-fifty-blocks'
    path=folder/'certificate.json'
    c=json.loads(path.read_bytes())
    meeting_path=folder.parent/'six-seven-fixed-half-meeting.json'
    meeting=json.loads(meeting_path.read_bytes())
    baseline=preferred_clarity_source(c,meeting)
    stages=baseline['stages']
    start=next(i for i,s in enumerate(stages) if s['_source_ref']=='named_full_route.stages.74')
    finish=next(i for i,s in enumerate(stages) if s['_source_ref']=='named_full_route.stages.77')
    source=stages[start]['factors']
    if (len(stages)-1,start,finish)!=(85,80,83):
        raise ValueError('Use the unchanged85-operation lower-meeting source as baseline')
    routes={k:close_preferred_late45(source,internal_power=k) for k in (0,-1,-2)}
    for route in routes.values():
        for stage in route['stages']:
            w=stage.get('named_pattern_witness')
            if not w:continue
            actual=stage['local_before']+stage['local_after']
            norm=tuple(replace(f,conjugator=reduce_word(inverse_word(w['common_chart'])+f.conjugator)) for f in actual)
            w['normalized_actual_inputs_and_outputs']=norm
            w['complete_actual_and_normalized_point_pushing']=pushing(actual+norm)
    chosen=routes[-1]
    late=chosen['stages'][7]
    if any(route['stages'][7]['factors']!=late['factors'] for route in routes.values()):
        raise ValueError('All three checked donor charts rejoin the SAME late tuple literally')
    before={f.id:f for f in source};after={f.id:f for f in late['factors']}
    comparisons=tuple(dict(id=f.id,before=f,after=after[f.id],literal_equal=f==after[f.id],
        before_support=len(supported_class(f.mapping_class,5)),after_support=len(supported_class(after[f.id].mapping_class,5)),
        complete_point_pushing=pushing((f,after[f.id]))) for f in source)
    if any(x['after_support']>x['before_support'] for x in comparisons):
        raise ValueError('Every final source-record support length is nonincreasing')
    m0,m1=matrix(source),matrix(late['factors'])
    lookup={frozenset(x['ids']):x['number'] for x in m0['pairs']}
    changes=tuple(dict(ids=x['ids'],before=lookup[frozenset(x['ids'])],after=x['number'])
                  for x in m1['pairs'] if lookup[frozenset(x['ids'])]!=x['number'])
    if changes:raise ValueError('All28 actual source-ID CLOSED pair counts remain identical')
    actual=chosen['factors'];historical=stages[finish]['factors']
    if len(actual)!=4 or tuple(replace(f,id=g.id) for f,g in zip(actual,historical))!=historical:
        raise ValueError('Retain the explicit ID-only four-unit ancestry comparison')
    fourth=stages[finish+1]['factors'][0]
    raw=reduce_word(product(actual)+inverse_word(fourth.word))
    archive_path=folder/'clarity-half-meeting-certificate.json'
    archive=json.loads(archive_path.read_bytes())
    old_words=tuple(tuple(s['disk_discrepancy']) for s in archive['stages'] if s['kind']=='sphere_redraw')
    if raw or old_words[-1]!=fourth.word:
        raise ValueError('Actual four-unit combine and FULL historical cap word must be unchanged')
    combine=dict(kind='disk_combine',title='Combine the FOUR actual visible standard exterior twists',
        factors=(fourth,),local_before=actual,local_after=(fourth,),raw_free_word_discrepancy=raw,
        exact_disk_equality=True)
    old_trace=[]
    for s in stages[start:finish+1]:
        for a in (s,)+tuple(s.get('atomic_steps',())):
            fs=tuple(factor_from_data(f) if isinstance(f,dict) else f for f in a['factors'])
            lengths=tuple(len(supported_class(f.mapping_class,5)) for f in fs)
            old_trace.append(dict(maximum=max(lengths),total=sum(lengths),braid_letters=len(product(fs)),rows=len(fs)))
    return dict(source_archive_file='six-seven-fifty-blocks/certificate.json',
        source_archive_sha256=sha256(path.read_bytes()).hexdigest(),
        source_input_ref='named_full_route.stages.74',source_terminal_ref='named_full_route.stages.77',
        source_meeting_file=meeting_path.name,source_meeting_sha256=sha256(meeting_path.read_bytes()).hexdigest(),
        source_factors=source,baseline_source_operations=85,baseline_source_input_index=start,
        baseline_source_terminal_index=finish,literal_source_input_join=True,
        route=chosen,unselected_original_chart=routes[0],unselected_inverse_full_chart=routes[-2],
        variant_peaks=tuple(dict(internal_power=k,peak=_peak(v),late_literal_join=v['stages'][7]['factors']==late['factors']) for k,v in routes.items()),
        source_record_comparisons=comparisons,all_eight_source_ids_retained_before_D5=True,
        all_final_individual_support_lengths_nonincreasing=True,
        before_closed_matrix=m0,after_closed_matrix=m1,changed_closed_pairs=changes,
        old_closure_operations=finish-start,old_closure_adjacent_checks=sum(s.get('adjacent_moves',0) for s in stages[start+1:finish+1]),
        old_closure_peak=dict(maximum=max(x['maximum'] for x in old_trace),total=max(x['total'] for x in old_trace),
            braid_letters=max(x['braid_letters'] for x in old_trace),rows=max(x['rows'] for x in old_trace)),
        chosen_peak=_peak(chosen),chosen_peak_rows=max(len(s['factors']) for s in chosen['stages']),
        terminal_plan=dict(actual_four_units=actual,
            id_only_ancestry_alignment=tuple(dict(actual=f,historical=g,only_id_changed=replace(f,id=g.id)==g) for f,g in zip(actual,historical)),
            historical_four_unit_source_ref='named_full_route.stages.77',
            combine=combine,existing_fourth_power=fourth,literal_existing_fourth_power_join=True,
            existing_cap_source_ref='named_full_route.stages.79',
            full_cap_discrepancy_word=old_words[-1],combine_applied=False,cap_applied=False),
        reference_clarity_archive=archive_path.name,reference_clarity_archive_sha256=sha256(archive_path.read_bytes()).hexdigest(),
        retained_thirteen_sphere_discrepancy_words=old_words,
        proposed_complete_source_operations=start+chosen['graphical_operations']+2,
        proposed_source_parts=(start,chosen['graphical_operations'],1,1),
        refined_listed_and_parallel_counts_computed=False,adopted=False,public_replay_changed=False,
        scope='Reached preferred-source late45 loan8moves/14externalchecks,three actual named '
              'substitutions. The same outer returns literally. Two final pair supports fall6->2 '
              'and4->2; all other six source records/curves remain literal,all28 CLOSED pair counts '
              'are unchanged. Localmaximum6 remains6 during the chosen internal inverse-generator '
              'daisy; temporary rows8->11 and total support33->42 are explicit costs. The final '
              'eight-record score is5/27/88 versus6/33/96. More operations,not a shortening or '
              'joint/arc/whole-proof bound. Source report flags/charts stay immutable; an adoption '
              'wrapper separately owns active flags,actual combine and the unchanged cap input.')


if __name__=='__main__':
    r=report();p=ROOT/'docs/proofs/six-seven-preferred-late45.json'
    p.write_text(json.dumps(r,default=asdict,separators=(',',':')),encoding='utf-8')
    print(json.dumps(dict(bytes=p.stat().st_size,sha256=sha256(p.read_bytes()).hexdigest(),
        moves=r['route']['graphical_operations'],checks=r['route']['adjacent_checks'],peak=r['chosen_peak'],
        old=(r['old_closure_operations'],r['old_closure_adjacent_checks']),variants=r['variant_peaks'],
        complete_source_plan=r['proposed_complete_source_operations'])))
