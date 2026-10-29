"""Read-only adoption-plan audit for the complete post-half research join.

This does not rebuild preferred artifacts, apply a global frame, or cap a curve.
Historical source witnesses are read by immutable address rather than copied.
"""
from dataclasses import asdict,replace
from hashlib import sha256
from pathlib import Path
import json
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data,preferred_clarity_source
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import exact_action

ROOT=Path(__file__).resolve().parents[1]
PROOFS=ROOT/'docs/proofs'
CLOSURE='six-seven-posthalf-residual-closure.json'
CHAIN=(('exterior',14),('petal',1),('spare',1),('outer',4),('block',15),('cyclic-rose',3),('reflected-lantern',7),('upper-cabled',3),('third-exterior',7))


def _factor(raw):return factor_from_data(raw) if isinstance(raw,dict) else raw


def _stage(raw,source_file,source_ref):
    result=dict(raw,_source_file=source_file,_source_ref=source_ref)
    for key in ('factors','local_before','local_after'):
        if key in result:result[key]=tuple(_factor(f) for f in result[key])
    return result


def _address(stage):return stage['_source_file']+':'+stage['_source_ref']


def audit_join(final_closure_stages=None,final_closure_factors=None):
    """Certify literal research joins and a106-operation terminal adoption plan.

    Live stages/factors may be supplied before the closure JSON exists. An
    endpoint alone never substitutes for the actual six closure operations.
    The caller may embed this result as its report's ``route_join`` field.
    """
    archive=PROOFS/'six-seven-fifty-blocks/certificate.json';meeting_path=PROOFS/'six-seven-fixed-half-meeting.json'
    c=json.loads(archive.read_text(encoding='utf-8'));meeting=json.loads(meeting_path.read_text(encoding='utf-8'))
    if meeting['source_archive_sha256']!=sha256(archive.read_bytes()).hexdigest():raise ValueError('Use the immutable meeting/source archive pair')
    preferred=preferred_clarity_source(c,meeting)['stages']
    if len(preferred)!=86 or tuple(i for i,s in enumerate(preferred) if s['kind']=='sphere_rewrite')!=(14,16,17,85):raise ValueError('Pin the existing85-operation clarity source before planning adoption')
    stages=[]
    for s in preferred[:44]:
        owner=s.get('_source_file','six-seven-fifty-blocks/certificate.json');stages.append(_stage(s,owner,s['_source_ref']))
    joins=[];manifest=[dict(source_file='six-seven-fifty-blocks/certificate.json',sha256=sha256(archive.read_bytes()).hexdigest()),dict(source_file=meeting_path.name,sha256=sha256(meeting_path.read_bytes()).hexdigest())]
    for stem,operations in CHAIN:
        name='six-seven-posthalf-'+stem+'.json';path=PROOFS/name;report=json.loads(path.read_text(encoding='utf-8'));route=report['route'];raw=route['stages'];source=tuple(_factor(f) for f in raw[0]['factors'])
        if len(raw)!=operations+1 or route['graphical_operations']!=operations or source!=stages[-1]['factors']:raise ValueError('A selected research report lost its complete literal source join: '+name)
        if report.get('source_file') and report.get('source_sha256') and sha256((PROOFS/report['source_file']).read_bytes()).hexdigest()!=report['source_sha256']:raise ValueError('An immutable research dependency changed: '+name)
        joins.append(dict(previous_source_ref=_address(stages[-1]),next_source_ref=name+':route.stages.0',literal_complete_factor_tuple_equal=True,factor_records=len(source)))
        manifest.append(dict(source_file=name,sha256=sha256(path.read_bytes()).hexdigest(),operations=operations,source_ref='route.stages',dependency_source_file=report.get('source_file'),dependency_sha256=report.get('source_sha256')))
        for i,s in enumerate(raw[1:],1):stages.append(_stage(s,name,'route.stages.'+str(i)))
    if len(stages)-1!=98:raise ValueError('The prefix43 plus reached research55 must total98 operations')
    if final_closure_stages is None:
        path=PROOFS/CLOSURE
        if not path.exists():raise ValueError('Supply all seven actual closure states until the closure JSON exists')
        report=json.loads(path.read_text(encoding='utf-8'));final_closure_stages=report['route']['stages']
    if isinstance(final_closure_stages,dict):
        record=final_closure_stages.get('route',final_closure_stages);final_closure_stages=record['stages']
    closure=tuple(_stage(s,CLOSURE,'route.stages.'+str(i)) for i,s in enumerate(final_closure_stages))
    if len(closure)!=7 or closure[0]['factors']!=stages[-1]['factors']:raise ValueError('The actual six-move residual closure needs its literal complete input join')
    if final_closure_factors is not None and closure[-1]['factors']!=tuple(_factor(f) for f in final_closure_factors):raise ValueError('The supplied closure endpoint differs from its actual final stage')
    joins.append(dict(previous_source_ref=_address(stages[-1]),next_source_ref=CLOSURE+':route.stages.0',literal_complete_factor_tuple_equal=True,factor_records=len(closure[0]['factors'])))
    stages.extend(closure[1:])
    transitions=[];frames=[]
    for i,s in enumerate(stages[1:],1):
        before=stages[i-1]['factors'];after=s['factors'];kind=s['kind'];entry=dict(source_index=i,source_ref=_address(s),kind=kind)
        if kind=='sphere_rewrite':
            if i not in (14,16,17):raise ValueError('The research join introduced a new raw sphere change')
            entry['unchanged_historical_sphere_witness']=True
        elif kind in ('disk_cyclic_start','global_conjugation'):
            frame=tuple(s['frame']);raw=reduce_word(frame+product(before)+inverse_word(frame)+inverse_word(product(after)))
            if kind=='disk_cyclic_start' and raw:raise ValueError('A FULL cyclic raw word failed BEFORE normalized presentations')
            if exact_action(frame+product(before)+inverse_word(frame),6)!=exact_action(product(after),6):raise ValueError('An explicit common frame lost its complete B6 equality')
            checks=()
            if kind=='global_conjugation':
                checks=tuple(dict(id=a.id,exact_disk_equal=a.id==b.id and exact_action(frame+a.word+inverse_word(frame),6)==exact_action(b.word,6)) for a,b in zip(before,after))
                if len(before)!=len(after) or not all(x['exact_disk_equal'] for x in checks):raise ValueError('A common frame lost an individual factor match')
            f=dict(source_index=i,source_ref=_address(s),kind=kind,frame=frame,raw_cyclic_discrepancy=raw if kind=='disk_cyclic_start' else None,faithful_complete_frame_equal=True,individual_global_matches=checks,source_centrality_assumed=False,tail_B5_frame=i>17)
            frames.append(f);entry['explicit_frame_verified']=True
        else:
            if exact_action(product(before),6)!=exact_action(product(after),6):raise ValueError('A stitched actual disk transition failed: '+_address(s))
            entry['faithful_complete_disk_equal']=True
        transitions.append(entry)
    actual=stages[-1]['factors'];standard=Factor('canonical.standard.D5',(),1,5)
    if len(actual)!=4 or any(f.conjugator or f.first!=1 or f.points!=5 or f.power!=1 or f.half for f in actual):raise ValueError('Keep FOUR separately visible STANDARD unit exteriors before combining')
    individual=tuple(dict(actual=f,standard_word=standard.word,exact_disk_equal=exact_action(f.word,6)==exact_action(standard.word,6),chosen_lift=homology_action(f.word)) for f in actual)
    minus=tuple(tuple(-x for x in row) for row in IDENTITY)
    if not all(x['exact_disk_equal'] and x['chosen_lift']==minus for x in individual):raise ValueError('Each terminal unit must retain its separately checked-I lift')
    old_four=preferred[-3]['factors'];fourth=preferred[-2]['factors'][0];aligned=tuple(replace(a,id=b.id) for a,b in zip(actual,old_four))
    ancestry=tuple(dict(actual_id=a.id,historical_terminal_id=b.id,actual=a,aligned=b,only_id_changed=replace(a,id=b.id)==b) for a,b in zip(actual,aligned))
    if aligned!=old_four or not all(x['only_id_changed'] for x in ancestry):raise ValueError('Historical terminal join needs explicit ID-only alignment')
    raw_combine=reduce_word(product(actual)+inverse_word(fourth.word))
    if raw_combine or homology_action(fourth.word)!=IDENTITY:raise ValueError('Combine actual four identical unit words to their checked FOURTH power')
    combine=dict(kind='disk_combine',title='Combine the FOUR actual identical visible exterior twists',factors=(fourth,),local_before=actual,local_after=(fourth,),exact_disk_equality=True,raw_free_word_discrepancy=raw_combine,not_an_action_recognition=True,_source_file=CLOSURE,_source_ref='route_join.terminal_plan.combine',canonical_source_witness_ref='six-seven-fifty-blocks/certificate.json:named_full_route.stages.78')
    cap=_stage(preferred[-1],'six-seven-fifty-blocks/certificate.json','named_full_route.stages.79')
    if cap['local_before']!=(fourth,) or cap['factors'] or cap['local_after']:raise ValueError('Reuse the historical cap only after its complete literal FOURTH-power input')
    if tuple(cap['disk_discrepancy'])!=reduce_word(fourth.word):raise ValueError('Keep the FULL terminal disk-discrepancy word identical')
    centrality=[]
    for f in frames:
        if not f['tail_B5_frame']:continue
        if any(abs(x)>4 for x in f['frame']) or exact_action(f['frame']+fourth.word+inverse_word(f['frame']),6)!=exact_action(fourth.word,6):raise ValueError('Only recorded B5 tail frames use terminal boundary centrality')
        centrality.append(dict(source_ref=f['source_ref'],terminal_fourth_power_fixed=True,source_centrality_assumed=False))
    actual_operations=len(stages)-1;complete_operations=actual_operations+2
    if actual_operations!=104 or complete_operations!=106:raise ValueError('Retain43+55+6+combine+cap operation accounting')
    return dict(immutable_source_manifest=tuple(manifest),source_refs=tuple(dict(source_index=i,source_ref=_address(s),kind=s['kind']) for i,s in enumerate(stages)),literal_joins=tuple(joins),actual_transition_audits=tuple(transitions),explicit_full_frame_certificates=tuple(frames),tail_terminal_centrality_certificates=tuple(centrality),terminal_standard_unit_matches=individual,terminal_id_ancestry_alignment=ancestry,literal_terminal_join_after_id_alignment=aligned==old_four,terminal_plan=dict(combine=combine,cap=cap,cap_applied=False,combine_applied=False,existing_fourth_power=fourth,complete_cap_input_join=True,full_terminal_disk_discrepancy_unchanged=True),actual_reached_source_operations=actual_operations,actual_reached_disk_operations=actual_operations-3,actual_reached_raw_sphere_changes=3,complete_source_operations=complete_operations,route_parts=(43,55,6,1,1),new_global_frames_added=0,new_raw_sphere_changes_added=0,existing_raw_sphere_indices=(14,16,17),planned_raw_sphere_indices=(14,16,17,106),expected_genuine_sphere_redraws_after_refinement=13,expected_listed_moves_after_refinement=122,parallel_step_count_claimed=False,adoption_plan=dict(first_posthalf_source_index=44,first_posthalf_source_ref='six-seven-posthalf-exterior.json:route.stages.1',parallel_barrier=True,parallel_barrier_reason='Keep the first root expansion AFTER the final original halves combine; presentation preference,not algebraic noncommutation.',historical_reports_modified=False,refinement_guard_requires_generalization=True,early_lantern_match_guard_requires_generalization=True),closure_owner_digest_excluded_to_avoid_self_reference=True,scope='Read-only exact integration/adoption PLAN. Prefix43 and all selected research55 plus actual closure6 join literally. FOUR standard unit exteriors remain explicit. Combine/cap are only planned,not applied here;the historic cap input/word is exact after the planned combine. No new preferred source,payload,PDF,parallel count,global frame or sphere move is claimed. EarlyB6frames remain explicit;only B5tailframes use terminal centrality,never assumed source centrality.')


if __name__=='__main__':
    audit=audit_join();print(json.dumps(dict(complete_source_operations=audit['complete_source_operations'],literal_joins=len(audit['literal_joins']),terminal_units=len(audit['terminal_standard_unit_matches']),parallel_step_count_claimed=False),separators=(',',':')))