"""Reproduce the prepared split-block closure and its scoped alternatives."""
from dataclasses import asdict,replace
from hashlib import sha256
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import equality,matrix
from examples.analyze_posthalf_hybrid_block import pushing
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.early_boundary_pure import _PositiveReplay
from surface_diagrams.factorization_explorer import product
from surface_diagrams.mapping_classes import supported_class
from surface_diagrams.posthalf_split_block import close_hybrid_split_block
from surface_diagrams.six_seven_structure import research_hurwitz_move
ROOT=Path(__file__).resolve().parents[1]


def _peak(route):
    states=route['state_sphere_lift_certificates']
    return dict(max_support_word=max(x['score']['max_support_word'] for x in states),
                total_support_word=max(x['score']['total_support_word'] for x in states),
                braid_letters=max(x['score']['braid_letters'] for x in states))


def report():
    path=ROOT/'docs/proofs/six-seven-posthalf-hybrid-rose.json'
    old=json.loads(path.read_bytes())
    opath=ROOT/'docs/proofs/six-seven-posthalf-opposite-block.json'
    opposite=json.loads(opath.read_bytes())
    source=tuple(factor_from_data(f) for f in old['third_exterior_route']['factors'])
    by={f.id:f for f in source}
    chosen=close_hybrid_split_block(source)
    unprepared=close_hybrid_split_block(source,inverse_preparation=False)
    for route in (chosen,unprepared):
        for stage in route['stages']:
            w=stage.get('named_pattern_witness')
            if not w:continue
            actual=stage['local_before']+stage['local_after']
            norm=tuple(replace(f,conjugator=reduce_word(inverse_word(w['common_chart'])+f.conjugator)) for f in actual)
            w['normalized_actual_inputs_and_outputs']=norm
            w['complete_actual_and_normalized_point_pushing']=pushing(actual+norm)
    right=(by['reflected.loan.2'],by['upper.I24'])
    other35=by['reflected.output.1']
    normalize=_PositiveReplay(source).normalize
    preps=[]
    for name,indices in (('FORWARD',(0,1)),('INVERSE',(1,0))):
        raw=research_hurwitz_move(right,*indices)
        actors=tuple(normalize(f) for f in raw['factors'])
        first=normalize(replace(other35,conjugator=reduce_word(inverse_word(actors[0].word)+other35.conjugator)))
        final=normalize(replace(first,conjugator=reduce_word(inverse_word(actors[1].word)+first.conjugator)))
        support=len(supported_class(first.mapping_class,5))
        preps.append(dict(name=name,raw_preparation=raw,normalized_actors=actors,
            preparation_individual_matches=tuple(equality(a.word,b.word) for a,b in zip(raw['factors'],actors)),
            actor_supports=tuple(len(supported_class(f.mapping_class,5)) for f in actors),
            full_ordered_product_match=equality(product(actors),product(right)),
            hypothetical_first_other35_crossing=first,first_crossing_support=support,
            full_other35_block_output=final,final_support=len(supported_class(final.mapping_class,5)),
            complete_point_pushing=pushing(actors+(first,final)),
            rejected_before_application=support>20,selected=name=='INVERSE',
            scope='Necessary standalone preparation/first35 class comparison. The FORWARD '
                  'first-crossing28 is UNAPPLIED; no forward gather prefix is selected. '
                  'The INVERSE choice is actually replayed with undo in the chosen route.'))
    if not preps[0]['rejected_before_application'] or preps[1]['first_crossing_support']!=6:
        raise ValueError('Retain the scoped forward28 rejection and inverse6 crossing')
    if chosen['stages'][-2]['factors']!=unprepared['stages'][-2]['factors']:
        raise ValueError('Prepared/unprepared late states must join LITERALLY after donor consumption')
    changed={f.id:f for f in chosen['stages'][15]['factors']}
    old_changed={f['id']:factor_from_data(f) for f in old['closure_route']['stages'][13]['factors']}
    op_changed={f['id']:factor_from_data(f) for f in opposite['route']['stages'][13]['factors']}
    comparisons=[]
    for n in ('cyclic135.supply.2','hybrid.first.1','hybrid.first.2','reflected.output.1'):
        records=(by[n],old_changed[n],op_changed[n],changed[n])
        comparisons.append(dict(id=n,source=records[0],old_long=records[1],opposite=records[2],split=records[3],
            support_lengths=tuple(len(supported_class(f.mapping_class,5)) for f in records),
            split_vs_old=equality(records[3].word,records[1].word),
            split_vs_opposite=equality(records[3].word,records[2].word),
            complete_point_pushing=pushing(records)))
    late=matrix(chosen['stages'][-2]['factors'])
    old_matrix=old['late_eight_record_closed_matrix']
    alias={'hybrid.final.O1234':'split.O1234'}
    old_pairs={frozenset(alias.get(n,n) for n in x['ids']):x['number'] for x in old_matrix['pairs']}
    pair_changes=tuple(dict(ids=x['ids'],before=old_pairs[frozenset(x['ids'])],after=x['number'])
                       for x in late['pairs'] if old_pairs[frozenset(x['ids'])]!=x['number'])
    terminal=old['terminal_plan']
    old_four=tuple(factor_from_data(f) for f in terminal['actual_four_units'])
    actual=chosen['factors']
    aligned=tuple(replace(f,id=g.id) for f,g in zip(actual,old_four))
    if len(aligned)!=4 or aligned!=old_four:raise ValueError('Keep the ID-only terminal join')
    fourth=factor_from_data(terminal['combine']['local_after'][0])
    raw=reduce_word(product(actual)+inverse_word(fourth.word))
    if raw or tuple(terminal['full_cap_discrepancy_word'])!=fourth.word:
        raise ValueError('Preserve the actualfour combine and complete historical cap word')
    return dict(source_file=path.name,source_sha256=sha256(path.read_bytes()).hexdigest(),
        source_ref='third_exterior_route.factors',source_factors=source,
        opposite_source_file=opath.name,opposite_source_sha256=sha256(opath.read_bytes()).hexdigest(),
        route=chosen,unprepared_comparison=unprepared,preparation_comparisons=tuple(preps),
        actual_curve_comparisons=tuple(comparisons),prepared_unprepared_late_literal_join=True,
        old_late_stage=old['closure_route']['stages'][14],
        opposite_late_stage=opposite['route']['stages'][16],
        old_peak=_peak(old['closure_route']),opposite_peak=_peak(opposite['route']),
        unprepared_peak=_peak(unprepared),chosen_peak=_peak(chosen),
        old_late_closed_matrix=old_matrix,chosen_late_closed_matrix=late,
        old_to_split_closed_pair_changes=pair_changes,
        closed_outer_id_alignment=dict(old=factor_from_data(old['closure_route']['stages'][14]['factors'][0]),
            new=chosen['stages'][-2]['factors'][3],
            only_id_changed=replace(factor_from_data(old['closure_route']['stages'][14]['factors'][0]),
                id=chosen['stages'][-2]['factors'][3].id)==chosen['stages'][-2]['factors'][3]),
        endpoint_complete_point_pushing=pushing(actual),
        terminal_plan=dict(actual_four_units=actual,
            id_only_alignment=tuple(dict(actual=f,historical=g,only_id_changed=replace(f,id=g.id)==g)
                                    for f,g in zip(actual,old_four)),
            literal_join_after_id_alignment=True,
            combine=dict(local_before=actual,local_after=(fourth,),raw_free_word_discrepancy=raw),
            full_cap_discrepancy_word=tuple(terminal['full_cap_discrepancy_word']),
            combine_applied=False,cap_applied=False),
        posthalf_combined_operations=old['posthalf_combined_operations']-16+chosen['graphical_operations'],
        posthalf_combined_external_checks=old['posthalf_combined_adjacent_checks']-15+chosen['adjacent_checks'],
        complete_source_plan_operations=old['complete_source_plan_operations']-16+chosen['graphical_operations'],
        research_prefix_operations_at_four_exteriors=old['complete_source_plan_operations']-18+chosen['graphical_operations'],
        complete_named_join_reached=True,preferred_moves=101,preferred_steps=71,
        adopted=False,public_replay_changed=False,
        scope='Prepared split-block18moves/18externalchecks closes the SAME third-exterior input '
              'to four standard units. Local main/external-atomic support peak8 instead of18 '
              '(old full-left carry) or12 (full-right carry). The late eight-record state is8/41, '
              '120braid,CLOSED20/2. Three late pair classes match the shorter opposite branch; '
              'other35 matches the shorter old branch. Preparation and undo are explicit moves, '
              'and old23 restores only by individually checked B5 presentation before consumption. '
              'These chart-specific support and closed comparisons are not arc crossings, joint '
              'drawings or whole-proof bounds. No preferred adoption, sphere redraw or cap.')


if __name__=='__main__':
    r=report();p=ROOT/'docs/proofs/six-seven-posthalf-split-block.json'
    p.write_text(json.dumps(r,default=asdict,separators=(',',':')),encoding='utf-8')
    print(json.dumps(dict(bytes=p.stat().st_size,sha256=sha256(p.read_bytes()).hexdigest(),
        chosen=r['chosen_peak'],unprepared=r['unprepared_peak'],
        late=r['route']['stages'][-2]['score'],closed_pair_changes=r['old_to_split_closed_pair_changes'],
        operations=r['route']['graphical_operations'],checks=r['route']['adjacent_checks'],
        complete_plan=r['complete_source_plan_operations'])))
