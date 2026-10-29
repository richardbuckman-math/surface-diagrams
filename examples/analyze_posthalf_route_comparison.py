"""Source-exact comparison of two COMPLETE post-half disk tails; no adoption."""
from dataclasses import asdict,replace
from hashlib import sha256
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import matrix
from examples.check_posthalf_route_join import CHAIN
from surface_diagrams.clarity_derivation import factor_from_data,preferred_clarity_source
from surface_diagrams.early_boundary_pure import _score
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.factorization_explorer import Factor
from surface_diagrams.point_pushing import split_fixed_last_strand
ROOT=Path(__file__).resolve().parents[1]
PROOFS=ROOT/'docs/proofs'


def _factor(raw):return factor_from_data(raw) if isinstance(raw,dict) else raw


def _stage(raw,source_file,source_ref,comparison_index):
    return dict(title=raw.get('title',''),kind=raw['kind'],factors=tuple(_factor(f) for f in raw['factors']),atomic_steps=tuple(raw.get('atomic_steps',())),source_file=source_file,source_ref=source_ref,comparison_index=comparison_index)


def _records(stages,include_atomic):
    records=[]
    for stage in stages:
        records.append(dict(source_file=stage['source_file'],source_ref=stage['source_ref'],comparison_index=stage['comparison_index'],record_kind='main',title=stage['title'],factors=stage['factors']))
        if include_atomic:
            for i,a in enumerate(stage['atomic_steps']):
                records.append(dict(source_file=stage['source_file'],source_ref=stage['source_ref']+'.atomic_steps.'+str(i),comparison_index=stage['comparison_index'],record_kind='external_atomic',title=stage['title'],factors=tuple(_factor(f) for f in a['factors'])))
    return tuple(records)


def _summary(records):
    metrics=tuple(dict(source_file=r['source_file'],source_ref=r['source_ref'],comparison_index=r['comparison_index'],record_kind=r['record_kind'],title=r['title'],factor_rows=len(r['factors']),**_score(r['factors'])) for r in records)
    keys=('factor_rows','max_support_word','total_support_word','braid_letters')
    peaks={key:dict(value=max(r[key] for r in metrics),records=tuple(r for r in metrics if r[key]==max(x[key] for x in metrics))) for key in keys}
    return dict(retained_record_count=len(records),unique_exact_factor_tuples=len({r['factors'] for r in records}),unique_exact_ordered_presentations_ignoring_ids=len({tuple((f.conjugator,f.first,f.points,f.power,f.half) for f in r['factors']) for r in records}),peaks=peaks,record_metrics=metrics)


def report():
    archive=PROOFS/'six-seven-fifty-blocks/certificate.json';meeting_path=PROOFS/'six-seven-fixed-half-meeting.json';certificate=json.loads(archive.read_text(encoding='utf-8'));meeting=json.loads(meeting_path.read_text(encoding='utf-8'));preferred=preferred_clarity_source(certificate,meeting)['stages']
    manifest=[dict(source_file='six-seven-fifty-blocks/certificate.json',sha256=sha256(archive.read_bytes()).hexdigest()),dict(source_file=meeting_path.name,sha256=sha256(meeting_path.read_bytes()).hexdigest())]
    old=tuple(_stage(preferred[i],preferred[i].get('_source_file','six-seven-fifty-blocks/certificate.json'),preferred[i]['_source_ref'],i) for i in range(43,84));alternative=[old[0]];joins=[];lookup={}
    for stem,operations in CHAIN+(('residual-closure',6),):
        name='six-seven-posthalf-'+stem+'.json';path=PROOFS/name;data=json.loads(path.read_text(encoding='utf-8'));raw=data['route']['stages']
        if len(raw)!=operations+1 or tuple(_factor(f) for f in raw[0]['factors'])!=alternative[-1]['factors']:raise ValueError('Preserve every literal complete research tuple join')
        joins.append(dict(previous_source_file=alternative[-1]['source_file'],previous_source_ref=alternative[-1]['source_ref'],next_source_file=name,next_source_ref='route.stages.0',literal_complete_factor_tuple_equal=True))
        manifest.append(dict(source_file=name,sha256=sha256(path.read_bytes()).hexdigest(),operations=operations))
        for i,s in enumerate(raw[1:],1):
            stage=_stage(s,name,'route.stages.'+str(i),43+len(alternative));alternative.append(stage);lookup[(name,i)]=stage
    alternative=tuple(alternative)
    if len(old)!=41 or len(alternative)!=62 or old[0]['factors']!=alternative[0]['factors']:raise ValueError('Pin the SAME matched input and the40/61-operation complete tails')
    terminal_map=tuple(dict(actual_id=a.id,preferred_terminal_id=b.id,actual=a,preferred=b,only_id_changed=replace(a,id=b.id)==b,individual_exact_disk_equal=exact_action(a.word,5)==exact_action(b.word,5)) for a,b in zip(alternative[-1]['factors'],old[-1]['factors']))
    if len(terminal_map)!=4 or not all(x['only_id_changed'] and x['individual_exact_disk_equal'] for x in terminal_map):raise ValueError('Keep the complete four-exterior endpoint join explicit')
    route_metrics={}
    for name,stages in (('preferred',old),('alternative',alternative)):
        main=_records(stages,False);all_records=_records(stages,True)
        route_metrics[name]=dict(operations=len(stages)-1,external_adjacent_checks=sum(len(s['atomic_steps']) for s in stages),main=_summary(main),main_and_external_atomic=_summary(all_records),scope='Only retained main and EXTERNAL-atomic factor presentations in this matched post-half interval. Generic named-rule INTERNAL verification work is retained in its source certificates and is NOT counted here. Fewer external checks is NOT a claim of fewer total atomic checks. Unique tuples are exact presentations,not curve-class/orbit/joint-isotopy counts.')
    choices=(('first-preferred','preferred','first',old[50-43],'Preferred: first visible exterior'),('first-alternative','alternative','first',lookup[('six-seven-posthalf-exterior.json',14)],'Alternative: first visible exterior'),('second-preferred','preferred','second',old[73-43],'Preferred: second visible exterior'),('second-alternative','alternative','second',lookup[('six-seven-posthalf-reflected-lantern.json',7)],'Alternative: second visible exterior'),('third-preferred','preferred','third',old[80-43],'Preferred: third visible exterior'),('third-alternative','alternative','third',lookup[('six-seven-posthalf-third-exterior.json',7)],'Alternative: third visible exterior'))
    panels=[]
    for name,route,milestone,s,title in choices:
        factors=s['factors']
        if any(f.half for f in factors):raise ValueError('This finite CLOSED-neighborhood comparison must never accept arcs')
        splits=tuple(dict(actual=f,split=split_fixed_last_strand(f.word,5)) for f in factors)
        for item in splits:
            if exact_action(item['actual'].word,5)!=exact_action(item['split'].reconstructed_word,5):raise ValueError('Retain every selected full NONABELIAN kernel AND B4 shadow')
        target={'first':1,'second':2,'third':3}[milestone];standard=exact_action(Factor('standard.D5',(),1,5).word,5)
        def count_units(state):return sum(f.power==1 and not f.half and exact_action(f.word,5)==standard for f in state['factors'])
        route_stages=old if route=='preferred' else alternative
        first=next(x for x in route_stages if count_units(x)>=target)
        if first['source_file']!=s['source_file'] or first['source_ref']!=s['source_ref'] or count_units(s)!=target:raise ValueError('Use the FIRST actual configuration at each fixed exterior milestone')
        panels.append(dict(name=name,route=route,milestone=milestone,visible_standard_unit_exteriors=target,first_milestone_reach_verified=True,title=title,source_file=s['source_file'],source_ref=s['source_ref'],stage=dict(kind=s['kind'],title=s['title'],factors=factors),score=dict(factor_rows=len(factors),**_score(factors)),closed_matrix=matrix(factors),full_point_pushing=splits))
    return dict(immutable_source_manifest=tuple(manifest),common_input=dict(preferred_source_index=43,source_file=old[0]['source_file'],source_ref=old[0]['source_ref'],factors=old[0]['factors'],literal_complete_factor_tuple_equal=True),literal_research_joins=tuple(joins),terminal_id_ancestry_alignment=terminal_map,literal_terminal_join_after_id_only_alignment=True,route_metrics=route_metrics,panels=tuple(panels),closed_matrices_computed_only_for_selected_panels=6,all_retained_geometry_is_closed=True,preferred_moves=101,preferred_steps=71,alternative_complete_source_operations_plan=106,alternative_refined_listed_moves_plan=122,alternative_parallel_count_claimed=False,adopted=False,public_replay_changed=False,scope='Finite source-exact comparison ONLY. Both complete matched tails have support-word maximum18;the alternative has MOREoperations61vs40,MOREpeakrows19vs18,andMOREpeakstoredbraidletters290vs258,butlowerpeak total-support132vs147. The second-exterior panel has shorter chart-specific support words/fewer rows in the alternative;first/third milestones have tradeoffs and differing inventories. No uniform/readability/entrywise dominance is asserted by these numbers. Support lengths are chart-specific words,CLOSED intersections are pairwise minima,NOT arc crossings,jointly attainable minimum drawings or whole-proof tangle bounds. Individual support panels are not joint-cut/ambient-isotopy certificates. The complete named closure remains SOLVED in both routes;preferred101/71 is UNCHANGED. No mathematical shortening,preferred adoption,new phase or parallel count is claimed.')


if __name__=='__main__':
    result=report();path=PROOFS/'six-seven-posthalf-route-comparison.json'
    with path.open('w',encoding='utf-8',newline='\n') as stream:json.dump(result,stream,default=asdict,separators=(',',':'))
    payload=path.read_bytes();print(json.dumps(dict(bytes=len(payload),sha256=sha256(payload).hexdigest(),panels=len(result['panels']),selected_closed_pairs=sum(len(p['closed_matrix']['pairs']) for p in result['panels']),selected_factor_records=sum(len(p['stage']['factors']) for p in result['panels']),milestones=tuple(dict(name=p['name'],score=p['score'],closed_total=p['closed_matrix']['total'],closed_maximum=p['closed_matrix']['maximum']) for p in result['panels'])),separators=(',',':')))