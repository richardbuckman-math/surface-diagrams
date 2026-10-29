"""A clearer third-exterior checkpoint and an explicit longer complete suffix."""
from dataclasses import asdict, replace
from hashlib import sha256
from pathlib import Path
import json

from examples.analyze_fixed_half_gather import matrix
from surface_diagrams.braid_actions import inverse_word, reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.factorization_explorer import product
from surface_diagrams.hyperelliptic_homology import IDENTITY, homology_action
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.posthalf_hybrid_rose import expose_hybrid_third_exterior, close_hybrid_residual

ROOT = Path(__file__).resolve().parents[1]


def report():
    source_path = ROOT / 'docs/proofs/six-seven-posthalf-upper-cabled.json'
    old = json.loads(source_path.read_bytes())
    source = tuple(factor_from_data(f) for f in old['route']['factors'])
    named_path = ROOT / 'docs/proofs/six-seven-posthalf-exterior.json'
    saved = json.loads(named_path.read_bytes())['route']['stages'][-1]['named_pattern_witness']
    witness = dict(saved, canonical_base=tuple(factor_from_data(f) for f in saved['canonical_base']))
    third = expose_hybrid_third_exterior(source, witness)
    closure = close_hybrid_residual(third['factors'])
    for part in (third, closure):
        for stage in part['stages']:
            w = stage.get('named_pattern_witness')
            if not w:
                continue
            actual = stage['local_before'] + stage['local_after']
            frame = inverse_word(w['common_chart'])
            normalized = tuple(replace(f, conjugator=reduce_word(frame + f.conjugator)) for f in actual)
            records = tuple(dict(actual=f, split=split_fixed_last_strand(f.word, 5)) for f in actual + normalized)
            for x in records:
                if exact_action(x['actual'].word, 5) != exact_action(x['split'].reconstructed_word, 5):
                    raise ValueError('Keep full actual/normalized nonabelian kernels AND shadows')
            w['normalized_actual_inputs_and_outputs'] = normalized
            w['complete_actual_and_normalized_point_pushing'] = records
    before = {f.id: f for f in source}
    after = {f.id: f for f in third['factors']}
    shared = tuple(n for n in before if n in after)
    if len(shared) != 6 or any(before[n] != after[n] for n in shared):
        raise ValueError('All SIX shared source/third records stay literally unchanged')
    exteriors = tuple(f for f in third['factors'] if f.points == 5)
    minus = tuple(tuple(-x for x in row) for row in IDENTITY)
    if len(exteriors) != 3 or any(homology_action(f.word) != minus for f in exteriors):
        raise ValueError('Keep three distinct visible odd unit exteriors')
    if any(sum(f.points == 5 for f in stage['factors']) != 2 for stage in third['stages'][:-1]):
        raise ValueError('The third-exterior picture must be its FIRST reached checkpoint')
    if tuple(third['factors']) != tuple(closure['stages'][0]['factors']):
        raise ValueError('The new suffix joins literally')
    closure_path = ROOT / 'docs/proofs/six-seven-posthalf-residual-closure.json'
    historical = json.loads(closure_path.read_bytes())['route_join']['terminal_plan']
    actual = closure['factors']
    old_four = tuple(factor_from_data(f) for f in historical['combine']['local_before'])
    aligned = tuple(replace(f, id=old_four[i].id) for i, f in enumerate(actual))
    if aligned != old_four:
        raise ValueError('Keep the explicit ID-only complete terminal join')
    fourth = factor_from_data(historical['existing_fourth_power'])
    raw = reduce_word(product(actual) + inverse_word(fourth.word))
    if raw or homology_action(fourth.word) != IDENTITY:
        raise ValueError('Combine the ACTUAL four identical words only to the checked fourth power')
    if tuple(historical['cap']['disk_discrepancy']) != reduce_word(fourth.word):
        raise ValueError('Keep the entire historical terminal cap word unchanged')
    terminal = dict(actual_four_units=actual,
                    id_only_alignment=tuple(dict(actual=f, aligned=g, only_id_changed=replace(f, id=g.id) == g)
                                            for f, g in zip(actual, old_four)),
                    literal_join_after_id_alignment=True,
                    combine=dict(local_before=actual, local_after=(fourth,), raw_free_word_discrepancy=raw),
                    existing_cap_source_file=closure_path.name,
                    existing_cap_source_ref='route_join.terminal_plan.cap',
                    existing_cap_source_sha256=sha256(closure_path.read_bytes()).hexdigest(),
                    full_cap_discrepancy_word=tuple(historical['cap']['disk_discrepancy']),
                    combine_applied=False, cap_applied=False)
    old_third_path = ROOT / 'docs/proofs/six-seven-posthalf-third-exterior.json'
    old_third = json.loads(old_third_path.read_bytes())
    late = closure['stages'][14]
    return dict(source_file=source_path.name, source_sha256=sha256(source_path.read_bytes()).hexdigest(),
                source_ref='route.factors', source_factors=source,
                retained_named_source_file=named_path.name,
                retained_named_source_ref='route.stages.14.named_pattern_witness',
                retained_named_source_sha256=sha256(named_path.read_bytes()).hexdigest(),
                third_exterior_route=third, closure_route=closure,
                shared_source_third_ids=shared, three_visible_exteriors=exteriors,
                before_closed_matrix=old['after_closed_matrix'],
                third_closed_matrix=matrix(third['factors']),
                late_eight_record_closed_matrix=matrix(late['factors']),
                terminal_closed_matrix=matrix(actual),
                older_third_source_file=old_third_path.name,
                older_third_source_sha256=sha256(old_third_path.read_bytes()).hexdigest(),
                older_third_score=old_third['route']['after_score'],
                older_third_closed_matrix=old_third['after_closed_matrix'],
                literal_part_join=True, terminal_plan=terminal,
                new_source_operations=third['graphical_operations'] + closure['graphical_operations'],
                new_external_adjacent_checks=third['adjacent_checks'] + closure['adjacent_checks'],
                posthalf_combined_operations=old['posthalf_combined_operations'] + 25,
                posthalf_combined_adjacent_checks=old['posthalf_combined_adjacent_checks'] + 21,
                research_prefix_operations_at_four_exteriors=116,
                complete_source_plan_operations=118,
                complete_named_join_reached=True, preferred_moves=101, preferred_steps=71,
                adopted=False, public_replay_changed=False,
                scope='A NINE-move/SIX-external-check third-exterior route has simpler '
                      'checkpoint curves than the older seven-move alternative. A separate '
                      'SIXTEEN-move/FIFTEEN-external-check named suffix reaches four standard '
                      'units but visibly retangles late curves. The full25/21 continuation '
                      'is longer; no uniform geometry dominance, shortening, lower full-proof '
                      'bound, new preferred phase or adoption is claimed. All earlier source '
                      'charts/flags/archives remain immutable. Terminal combine, fourth-power '
                      'sphere redraw and cleanup remain separate and unapplied here.')


if __name__ == '__main__':
    result = report()
    path = ROOT / 'docs/proofs/six-seven-posthalf-hybrid-rose.json'
    with path.open('w', encoding='utf-8', newline='\n') as handle:
        json.dump(result, handle, default=asdict, separators=(',', ':'))
    print(json.dumps(dict(bytes=path.stat().st_size, sha256=sha256(path.read_bytes()).hexdigest(),
                         operations=result['new_source_operations'],
                         checks=result['new_external_adjacent_checks'],
                         third=result['third_exterior_route']['after_score'],
                         third_closed=(result['third_closed_matrix']['total'], result['third_closed_matrix']['maximum']),
                         late_closed=(result['late_eight_record_closed_matrix']['total'], result['late_eight_record_closed_matrix']['maximum']))))
