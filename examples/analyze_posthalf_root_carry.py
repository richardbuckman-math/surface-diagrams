"""Exact root-carry closure, scoped target failures and complete source joins."""
from dataclasses import asdict,replace
from hashlib import sha256
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import equality,matrix
from examples.analyze_posthalf_cyclic_rose import commutators
from examples.analyze_posthalf_hybrid_block import pushing
from examples.analyze_posthalf_split_block import _peak
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.early_boundary_pure import _PositiveReplay
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.outside_half_lantern import _matches
from surface_diagrams.outside_rose_return import _terms,_transport
from surface_diagrams.posthalf_root_carry import close_hybrid_root_carry
from surface_diagrams.projected_relations import pc_daisy_terms
from surface_diagrams.six_seven_structure import research_hurwitz_move
ROOT=Path(__file__).resolve().parents[1]


def report():
    path=ROOT/'docs/proofs/six-seven-posthalf-hybrid-rose.json'
    old=json.loads(path.read_bytes())
    split_path=ROOT/'docs/proofs/six-seven-posthalf-split-block.json'
    split=json.loads(split_path.read_bytes())
    comparison_path=ROOT/'docs/proofs/six-seven-posthalf-route-comparison.json'
    comparison=json.loads(comparison_path.read_bytes())
    preferred=next(p for p in comparison['panels'] if p['name']=='third-preferred')
    source=tuple(factor_from_data(f) for f in old['third_exterior_route']['factors'])
    by={f.id:f for f in source}
    route=close_hybrid_root_carry(source)
    for stage in route['stages']:
        w=stage.get('named_pattern_witness')
        if not w:continue
        actual=stage['local_before']+stage['local_after']
        normalized=tuple(replace(f,conjugator=reduce_word(inverse_word(w['common_chart'])+f.conjugator)) for f in actual)
        w['normalized_actual_inputs_and_outputs']=normalized
        w['complete_actual_and_normalized_point_pushing']=pushing(actual+normalized)
    normalize=_PositiveReplay(source).normalize
    short15=normalize(replace(by['hybrid.first.1'],conjugator=reduce_word(by['hybrid.second.0'].word+by['hybrid.first.1'].conjugator)))
    wrong=(by['hybrid.inner134'],by['cyclic135.supply.2'],short15,by['reflected.output.1'])
    integral=commutators(wrong)
    w=product(wrong)
    faithful=tuple(dict(actual=f,left=exact_action(w+f.word,5),right=exact_action(f.word+w,5),
                        comparison=equality(w+f.word,f.word+w)) for f in wrong)
    if any(x['left']==x['right'] for x in integral) or any(x['comparison']['equal'] for x in faithful):
        raise ValueError('Keep four nonzero witnesses for the initial unchanged ordered target')
    needed=Factor('target.required35',(-4,),3,2)
    actors2=(by['hybrid.second.0'],by['hybrid.first.2'])
    actors3=route['actual_consolidated_inputs']
    probes=[]
    for label,actors in (('round12_then25',actors2),('round12_then15_then25',actors3)):
        block=product(actors)
        for sign in (-1,1):
            f=normalize(replace(by['reflected.output.1'],conjugator=reduce_word((inverse_word(block) if sign<0 else block)+by['reflected.output.1'].conjugator)))
            probes.append(dict(label=label,actual_ordered_actors=actors,sign=sign,candidate=f,
                comparison=equality(f.word,needed.word),support_length=len(supported_class(f.mapping_class,5)),
                complete_point_pushing=pushing((f,)),unit_block_transport_applied=False,
                effect_reached_via_named_root_carry=label=='round12_then15_then25' and sign==1,
                scope='Necessary class/support comparison before transport. The selected positive '
                      'three-unit effect is reached by actual named contraction, ONE root carry, '
                      'and named expansion; it is not an applied three-unit Hurwitz block carry.'))
    if [x['comparison']['equal'] for x in probes]!=[False,False,False,True]:
        raise ValueError('Retain the finite two-unit misses and three-unit inverse miss/positive match')
    actual35=next(f for f in route['stages'][4]['factors'] if f.id=='reflected.output.1')
    raw35=replace(by['reflected.output.1'],conjugator=reduce_word(product(actors3)+by['reflected.output.1'].conjugator))
    effect_matches=_matches((actual35,actual35),(needed,raw35))
    local_parent=route['actual_carried_root']
    parent_identity=equality(product(actors3),local_parent.word)
    if not parent_identity['equal']:raise ValueError('Retain full ordered product/parent B5 equality')
    chartG=tuple(old['closure_route']['stages'][14]['named_pattern_witness']['common_chart'])
    if chartG+(4,)!=route['stages'][-1]['named_pattern_witness']['common_chart']:
        raise ValueError('Retain the explicit G then positive sigma4 chart derivation')
    d5=Factor('canonical.D5',(),1,5)
    canonical=_terms(d5.mapping_class,'canonical.D5.',pc_daisy_terms)
    actual5=route['stages'][-1]['local_before']
    chart_comparisons=[]
    for last in (4,-4):
        for name,pattern in (('BASE',canonical),('UP(2,1)',research_hurwitz_move(canonical,2,1)['factors']),
                             ('DOWN(1,2)',research_hurwitz_move(canonical,1,2)['factors'])):
            transported=_transport(pattern,chartG+(last,))
            chart_comparisons.append(dict(chart=chartG+(last,),pattern=name,canonical_inputs=pattern,
                actual_inputs=actual5,individual_comparisons=tuple(equality(a.word,b.word) for a,b in zip(actual5,transported)),
                chosen=last==4 and name=='UP(2,1)',
                scope='Six specifically derived G/sigma4 chart-order comparisons, not a global-frame scan or orbit exclusion.'))
    late=route['stages'][8]
    preferred_factors=tuple(factor_from_data(f) for f in preferred['stage']['factors'])
    preferred_matches=tuple(dict(actual=f,preferred_matching_ids=tuple(g.id for g in preferred_factors if equality(f.word,g.word)['equal'])) for f in late['factors'])
    old_four=tuple(factor_from_data(f) for f in old['terminal_plan']['actual_four_units'])
    actual=route['factors']
    if len(actual)!=4 or tuple(replace(f,id=g.id) for f,g in zip(actual,old_four))!=old_four:
        raise ValueError('Keep the complete ID-only terminal join')
    fourth=factor_from_data(old['terminal_plan']['combine']['local_after'][0])
    discrepancy=reduce_word(product(actual)+inverse_word(fourth.word))
    if discrepancy or tuple(old['terminal_plan']['full_cap_discrepancy_word'])!=fourth.word:
        raise ValueError('Preserve actual four-unit combination and the entire historical cap word')
    peak=_peak(route)
    if any(peak[k]>route['before_score'][k] for k in peak):
        raise ValueError('The chosen score-component trajectory does not exceed its input values')
    return dict(source_file=path.name,source_sha256=sha256(path.read_bytes()).hexdigest(),
        source_ref='third_exterior_route.factors',source_factors=source,route=route,
        initial_short15_order_failure=dict(ordered_inputs=wrong,exact_integral_commutators=integral,
            faithful_B5_product_input_comparisons=faithful,complete_point_pushing=pushing(wrong),applied=False,
            scope='Only this unchanged ordered unit target fails; selected-only disk Hurwitz/commonframes cannot turn its noncentral product into a PC daisy. Outside/newcurves/substitutions remain unexcluded.'),
        necessary35_probes=tuple(probes),actual_carried35=actual35,required35=needed,
        positive_full_product_effect_matches=effect_matches,full_ordered_parent_match=parent_identity,
        full_ordered_parent_raw_discrepancy=reduce_word(product(actors3)+inverse_word(local_parent.word)),
        complete_source_parent_effect_point_pushing=pushing(actors3+(local_parent,actual35,raw35,needed,short15)),
        final_chart_source_ref='closure_route.stages.14.named_pattern_witness.common_chart',
        final_chart_source_G=chartG,final_chart_G_then_sigma4=chartG+(4,),
        derived_final_chart_order_comparisons=tuple(chart_comparisons),
        new_late_closed_matrix=matrix(late['factors']),chosen_peak=peak,
        score_components_never_exceed_input=True,peak_factor_records=max(len(s['factors']) for s in route['stages']),
        previous_split_source_file=split_path.name,previous_split_source_sha256=sha256(split_path.read_bytes()).hexdigest(),
        previous_split_late_stage=split['route']['stages'][-2],previous_split_peak=split['chosen_peak'],
        previous_split_late_closed_matrix=split['chosen_late_closed_matrix'],
        preferred_comparison_source_file=comparison_path.name,
        preferred_comparison_source_sha256=sha256(comparison_path.read_bytes()).hexdigest(),
        preferred_third_panel=preferred,preferred_individual_class_comparisons=preferred_matches,
        preferred_comparison_scope='Preferred panel is its FIRST third-exterior checkpoint; new late8 state occurs AFTER this branch first reached three exteriors in11records. No false first-milestone comparison or whole-route dominance is claimed.',
        terminal_plan=dict(actual_four_units=actual,
            id_only_alignment=tuple(dict(actual=f,historical=g,only_id_changed=replace(f,id=g.id)==g) for f,g in zip(actual,old_four)),
            literal_join_after_id_alignment=True,
            combine=dict(local_before=actual,local_after=(fourth,),raw_free_word_discrepancy=discrepancy),
            full_cap_discrepancy_word=tuple(old['terminal_plan']['full_cap_discrepancy_word']),
            combine_applied=False,cap_applied=False),
        posthalf_combined_operations=old['posthalf_combined_operations']-16+route['graphical_operations'],
        posthalf_combined_external_checks=old['posthalf_combined_adjacent_checks']-15+route['adjacent_checks'],
        research_prefix_operations_at_four_exteriors=old['complete_source_plan_operations']-18+route['graphical_operations'],
        complete_source_plan_operations=old['complete_source_plan_operations']-16+route['graphical_operations'],
        complete_named_join_reached=True,preferred_moves=101,preferred_steps=71,adopted=False,public_replay_changed=False,
        scope='Eleven-move/twelve-external-check complete root-carry closure has local score peak6/40/108 '
              'and late8-record score5/29/92,CLOSED20/2. All three source12/15/25 records are restored '
              'literally by an actual named expansion; all seven source/late shared records are literal. '
              'Four named substitutions retain every individual input/output,full framing/disk/sphere/lift '
              'and nonabelian kernel/shadow data. The initial four-unit target and finite outside probes '
              'are scoped; the reached route changes35 through an actual consolidated root. No arc/joint '
              'minimum/whole-proof bound, preferred adoption, new sphere move, half or cap.')


if __name__=='__main__':
    r=report();p=ROOT/'docs/proofs/six-seven-posthalf-root-carry.json'
    p.write_text(json.dumps(r,default=asdict,separators=(',',':')),encoding='utf-8')
    print(json.dumps(dict(bytes=p.stat().st_size,sha256=sha256(p.read_bytes()).hexdigest(),
        moves=r['route']['graphical_operations'],checks=r['route']['adjacent_checks'],peak=r['chosen_peak'],
        late=r['route']['stages'][8]['score'],closed=(r['new_late_closed_matrix']['total'],r['new_late_closed_matrix']['maximum']),
        complete_source_plan=r['complete_source_plan_operations'],preferred_class_matches=[x['preferred_matching_ids'] for x in r['preferred_individual_class_comparisons']])))
