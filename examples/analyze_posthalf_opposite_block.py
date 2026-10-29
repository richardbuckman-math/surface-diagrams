"""Source-pinned comparison of the actual opposite-block complete closure."""
from dataclasses import asdict, replace
from hashlib import sha256
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import equality, matrix
from examples.analyze_posthalf_hybrid_block import pushing
from surface_diagrams.braid_actions import inverse_word, reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.factorization_explorer import product
from surface_diagrams.mapping_classes import supported_class
from surface_diagrams.posthalf_opposite_block import close_hybrid_opposite_block
ROOT = Path(__file__).resolve().parents[1]


def report():
    path = ROOT / 'docs/proofs/six-seven-posthalf-hybrid-rose.json'
    old = json.loads(path.read_bytes())
    source = tuple(factor_from_data(f) for f in old['third_exterior_route']['factors'])
    route = close_hybrid_opposite_block(source)
    for stage in route['stages']:
        w = stage.get('named_pattern_witness')
        if not w:
            continue
        actual = stage['local_before'] + stage['local_after']
        normalized = tuple(replace(f, conjugator=reduce_word(inverse_word(w['common_chart']) + f.conjugator)) for f in actual)
        w['normalized_actual_inputs_and_outputs'] = normalized
        w['complete_actual_and_normalized_point_pushing'] = pushing(actual + normalized)
    old_block = {f['id']: factor_from_data(f) for f in old['closure_route']['stages'][13]['factors']}
    source_by = {f.id: f for f in source}
    new_block = {f.id: f for f in route['stages'][13]['factors']}
    comparisons = []
    for name in ('cyclic135.supply.2', 'hybrid.first.1', 'hybrid.first.2', 'reflected.output.1'):
        a, b, c = source_by[name], old_block[name], new_block[name]
        comparisons.append(dict(id=name, source=a, old_long_block=b, opposite_block=c,
            source_support=len(supported_class(a.mapping_class, 5)),
            old_support=len(supported_class(b.mapping_class, 5)),
            opposite_support=len(supported_class(c.mapping_class, 5)),
            exact_old_vs_opposite=equality(b.word, c.word),
            complete_point_pushing=pushing((a, b, c))))
    # Check the explanatory B5 product identity; this is NOT a free-word equality.
    actors = route['actual_ordered_actors']
    others = tuple(source_by[n] for n in ('reflected.loan.2', 'upper.I24'))
    d4 = route['stages'][14]['local_after'][0]
    identity = equality(product(actors + others), d4.word)
    if not identity['equal']:
        raise ValueError('Keep the faithful B5 D4 identity separately from raw cyclic identities')
    terminal = old['terminal_plan']
    old_four = tuple(factor_from_data(f) for f in terminal['actual_four_units'])
    aligned = tuple(replace(f, id=g.id) for f,g in zip(route['factors'], old_four))
    if len(aligned) != 4 or aligned != old_four:
        raise ValueError('Keep the complete ID-only terminal join')
    fourth = factor_from_data(terminal['combine']['local_after'][0])
    raw = reduce_word(product(route['factors']) + inverse_word(fourth.word))
    if raw or tuple(terminal['full_cap_discrepancy_word']) != fourth.word:
        raise ValueError('Keep actual four-unit combination and the unchanged full cap word')
    return dict(source_file=path.name, source_sha256=sha256(path.read_bytes()).hexdigest(),
        source_ref='third_exterior_route.factors', source_factors=source, route=route,
        older_route_ref='closure_route', older_operations=16, older_external_checks=15,
        older_peak_support=old['closure_route']['peak_support_word'],
        older_late_stage=old['closure_route']['stages'][14],
        older_late_closed_matrix=old['late_eight_record_closed_matrix'],
        new_late_closed_matrix=matrix(route['stages'][16]['factors']),
        actual_curve_comparisons=tuple(comparisons),
        block_product_identity=dict(actual_first_block=actors, actual_second_block=others,
            actual_D4=d4, faithful_B5_equality=identity,
            raw_word_discrepancy=reduce_word(product(actors + others) + inverse_word(d4.word)),
            scope='Faithful B5 equality only; not a claimed free-word cancellation or applied global frame.'),
        terminal_plan=dict(actual_four_units=route['factors'],
            id_only_alignment=tuple(dict(actual=f, historical=g, only_id_changed=replace(f,id=g.id)==g)
                                    for f,g in zip(route['factors'],old_four)),
            literal_join_after_id_alignment=True,
            combine=dict(local_before=route['factors'],local_after=(fourth,),raw_free_word_discrepancy=raw),
            full_cap_discrepancy_word=tuple(terminal['full_cap_discrepancy_word']),
            combine_applied=False,cap_applied=False),
        posthalf_combined_operations=74,posthalf_combined_external_checks=55,
        research_prefix_operations_at_four_exteriors=117,complete_source_plan_operations=119,
        complete_named_join_reached=True,preferred_moves=101,preferred_steps=71,
        adopted=False,public_replay_changed=False,
        scope='Same reached eleven-record third-exterior input and explicit four-unit terminal join. '
              'New closure17 operations/17 external checks versus16/15; support trajectory peak12 '
              'versus18. Late eight-record total support49 versus51; maximum12 in both. Three '
              'outside curves shorten and one lengthens relative to the older closure. Closed '
              'pair minima and individual support pictures are not jointly minimal diagrams, '
              'arc crossings or whole-proof bounds. No preferred adoption, sphere move or cap.')


if __name__ == '__main__':
    r=report()
    path=ROOT/'docs/proofs/six-seven-posthalf-opposite-block.json'
    path.write_text(json.dumps(r,default=asdict,separators=(',',':')),encoding='utf-8')
    print(json.dumps(dict(bytes=path.stat().st_size,sha256=sha256(path.read_bytes()).hexdigest(),
        moves=r['route']['graphical_operations'],checks=r['route']['adjacent_checks'],
        peak=r['route']['peak_support_word'],late=r['route']['stages'][16]['score'],
        closed=(r['new_late_closed_matrix']['total'],r['new_late_closed_matrix']['maximum']))))
