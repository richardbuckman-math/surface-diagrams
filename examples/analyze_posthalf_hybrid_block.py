"""Reproduce the bounded hybrid candidate and its scoped follow-up obstructions."""
from dataclasses import asdict, replace
from hashlib import sha256
from pathlib import Path
import json

from examples.analyze_fixed_half_gather import equality, matrix
from examples.analyze_posthalf_cyclic_rose import commutators
from surface_diagrams.braid_actions import inverse_word, reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.hyperelliptic_homology import IDENTITY, homology_action
from surface_diagrams.mapping_classes import exact_action, supported_class
from surface_diagrams.outside_half_lantern import _matches
from surface_diagrams.outside_rose_return import _terms, _transport
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.posthalf_hybrid_block import preview_posthalf_hybrid_block
from surface_diagrams.projected_relations import pc_rose_terms
from surface_diagrams.sphere_actions import sphere_chain_certificate

ROOT = Path(__file__).resolve().parents[1]


def pushing(factors):
    records = tuple(dict(actual=f, split=split_fixed_last_strand(f.word, 5)) for f in factors)
    for x in records:
        if exact_action(x['actual'].word, 5) != exact_action(x['split'].reconstructed_word, 5):
            raise ValueError('Retain full nonabelian kernel AND B4 shadow reconstruction')
    return records


def conjugate(factor, word):
    return replace(factor, conjugator=reduce_word(word + factor.conjugator))


def report():
    path = ROOT / 'docs/proofs/six-seven-posthalf-upper-cabled.json'
    old = json.loads(path.read_bytes())
    source = tuple(factor_from_data(f) for f in old['route']['factors'])
    by = {f.id: f for f in source}
    candidate = preview_posthalf_hybrid_block(source)
    end = {f.id: f for f in candidate['factors']}
    target = Factor('target.required25', (-2, -3), 4, 2)
    actors = (by['reflected.loan.2'], by['upper.I24'])
    block = product(actors)
    probes = []
    for sign in (-1, 1):
        f = conjugate(by['outer.loan.2'], inverse_word(block) if sign == -1 else block)
        probes.append(dict(sign=sign, candidate=f, exact_match=equality(f.word, target.word),
                           support_length=len(supported_class(f.mapping_class, 5)),
                           full_point_pushing=pushing((f,)), applied=False))
    if not probes[0]['exact_match']['equal'] or probes[1]['exact_match']['equal']:
        raise ValueError('Keep the saved inverse match and positive miss')

    # The needed15 belongs to the known, hypothetical134/45/35/NEW15 daisy.
    needed15 = Factor('target.needed15', (-4, -3, 1), 2, 2)
    donor = end['reflected.inner125']
    rose_probes = []
    for internal in ((), (3,), (-3,)):
        parent = replace(donor, conjugator=donor.conjugator + internal)
        terms = _terms(parent.mapping_class, 'target.rose.', pc_rose_terms)
        rose_probes.append(dict(internal=internal, parent=parent, terms=terms,
                                parent_matches=_matches((donor,), (parent,)),
                                needed15_matches=tuple(equality(f.word, needed15.word) for f in terms),
                                support_lengths=tuple(len(supported_class(f.mapping_class, 5)) for f in terms),
                                applied=False))
    chosen = rose_probes[1]
    if not chosen['needed15_matches'][2]['equal']:
        raise ValueError('Retain the exact internal(+3) last-petal match')
    canonical = Factor('canonical.R345', (), 3, 3)
    terms = _terms(canonical.mapping_class, 'canonical.rose.', pc_rose_terms)
    chart = chosen['parent'].conjugator
    _matches(chosen['terms'], _transport(terms, chart))
    discrepancy = reduce_word(donor.word + inverse_word(product(chosen['terms'])))
    normalized = tuple(conjugate(f, inverse_word(chart)) for f in (donor,) + chosen['terms'])
    supplier = dict(actual_parent=donor, target_outputs=chosen['terms'],
                    canonical_parent=canonical, canonical_rose=terms, common_chart=chart,
                    individual_parent_match=_matches((donor,), _transport((canonical,), chart)),
                    individual_output_matches=_matches(chosen['terms'], _transport(terms, chart)),
                    disk_discrepancy=discrepancy,
                    sphere_certificate=sphere_chain_certificate(discrepancy),
                    chosen_lift=homology_action(discrepancy),
                    signed_pc_balance=tuple(int(j in enclosed_boundaries(donor.mapping_class, 5)) -
                        sum(f.power for f in chosen['terms'] if j in enclosed_boundaries(f.mapping_class, 5))
                        for j in range(1, 6)),
                    normalized_actual_inputs_and_outputs=normalized,
                    full_point_pushing=pushing((donor,) + chosen['terms'] + normalized + (canonical,) + terms),
                    applied=False)
    if exact_action(donor.word, 5) != exact_action(product(chosen['terms']), 5) or not supplier['sphere_certificate']['certified'] or supplier['chosen_lift'] != IDENTITY:
        raise ValueError('Keep the complete hypothetical supplier certificate')
    n = needed15.word
    block_fixes15 = equality(conjugate(needed15, inverse_word(block)).word, needed15.word)
    if not block_fixes15['equal']:
        raise ValueError('Keep the exact full-block stabilizer match')
    outer = Factor('target.HYPOTHETICAL.O1345', (1,), 2, 4)
    d4 = by['upper.O1234']
    changed_q = conjugate(target, inverse_word(n))
    correct_last_q = conjugate(target, inverse_word(outer.word))
    changed_d4 = conjugate(d4, n)
    following = []
    for direction, hypothetical in (('UP', (d4, outer, changed_q)),
                                     ('DOWN', (changed_d4, outer, target))):
        witnesses = commutators(hypothetical)
        if any(x['left'] == x['right'] for x in witnesses):
            raise ValueError('Keep all three nonzero witnesses for each predicted order')
        following.append(dict(direction=direction, hypothetical_ordered_inputs=hypothetical,
                              exact_integral_commutators=witnesses,
                              full_point_pushing=pushing(hypothetical), applied=False,
                              scope='Necessary class prediction before any NEW15 gather. '
                                    'The second outer is HYPOTHETICAL; no gathering prefix is reached.'))
    changed_old15 = conjugate(by['outer.loan.1'], inverse_word(n))
    repair = []
    for sign in (-1, 1):
        f = conjugate(changed_q, inverse_word(changed_old15.word) if sign == -1 else changed_old15.word)
        miss = equality(f.word, correct_last_q.word)
        if miss['equal']:
            raise ValueError('Retain both scoped hypothetical repair misses')
        repair.append(dict(sign=sign, hypothetical_actor=changed_old15, candidate=f,
                           needed=correct_last_q, exact_match=miss,
                           support_length=len(supported_class(f.mapping_class, 5)),
                           full_point_pushing=pushing((f,)), applied=False))
    before = old['after_closed_matrix']
    after = matrix(candidate['factors'])
    source_counts = {tuple(x['ids']): x['number'] for x in before['pairs']}
    changed_pairs = tuple(dict(ids=x['ids'], before=source_counts[tuple(x['ids'])],
                               after=x['number'], delta=x['number'] - source_counts[tuple(x['ids'])])
                          for x in after['pairs'] if source_counts[tuple(x['ids'])] != x['number'])
    return dict(source_file=path.name, source_sha256=sha256(path.read_bytes()).hexdigest(),
                source_ref='route.factors', source_factors=source,
                retained_preliminary_probe_sha256='bbf8da349868d9ff7c9690694ccf409c0b4b16150278e26aacb2bd05d6c66dec',
                preliminary_sign_comparisons=tuple(probes), bounded_candidate=candidate,
                before_closed_matrix=before, after_candidate_closed_matrix=after,
                changed_closed_pairs=changed_pairs, hypothetical_supplier_internal_probes=tuple(rose_probes),
                hypothetical_named15_supplier=supplier, full_ordered_block_fixes_needed15=block_fixes15,
                hypothetical_followup_order_failures=tuple(following),
                UP_predicted25_vs_needed_last25=equality(changed_q.word, correct_last_q.word),
                hypothetical_changed_old15_repair_misses=tuple(repair),
                selected_source_moves=0, preferred_moves=101, preferred_steps=71,
                adopted=False, public_replay_changed=False,
                scope='Full bounded unselected candidate and scoped necessary failures. '
                      'The selected upper-cabled source is unchanged. No NEW15 supplier '
                      'expansion/gather, hypothetical outer, third exterior or useful complete '
                      'hybrid join is applied. No new graphics or preferred artifact changes. '
                      'Both complete proofs remain SOLVED; fixed-input exclusions stay scoped.')


if __name__ == '__main__':
    result = report()
    path = ROOT / 'docs/proofs/six-seven-posthalf-hybrid-block.json'
    with path.open('w', encoding='utf-8', newline='\n') as handle:
        json.dump(result, handle, default=asdict, separators=(',', ':'))
    print(json.dumps(dict(bytes=path.stat().st_size, sha256=sha256(path.read_bytes()).hexdigest(),
                         operations=result['bounded_candidate']['graphical_operations'],
                         external_checks=result['bounded_candidate']['adjacent_checks'],
                         after=result['bounded_candidate']['after_score'],
                         closed=(result['after_candidate_closed_matrix']['total'],
                                 result['after_candidate_closed_matrix']['maximum']))))
