"""Alternative early PC cluster: preserve the four original half twists.

This positive research branch is NOT a replacement for the complete named
106-step proof. It supplies a different four-point daisy and a T12 square
without creating the four auxiliary K half twists.
"""
from dataclasses import replace

from .braid_actions import inverse_word, reduce_word
from .early_boundary_pure import _PositiveReplay, _score
from .factorization_explorer import Factor, product
from .framed_boundary_relations import enclosed_boundaries
from .mapping_classes import exact_action
from .projected_relations import pc_daisy_terms
from .six_seven_structure import research_hurwitz_move


def expose_alternative_early_daisy(factors):
    """Reach the actual Q14 daisy in seven positive disk operations.

    One cyclic start brings an existing 124 root above the original 34 pair
    and one round 123 root. Their explicit cabled PC lantern gives a routed
    T1234 and T12; combine the latter with the existing round T12. Expand
    that T1234 by its PC daisy. Every original half is retained unchanged.
    No sphere move, negative factor, added half, or route search occurs.
    """
    factors = tuple(factors)
    expected_ids = ('prefix.P45', 'prefix.P12', 'F4', 'F3', 'F5', 'F6',
                    'F8.1', 'F10.1', 'F8.2', 'F9', 'F10.2', 'F11', 'F12', 'F13')
    if tuple(f.id for f in factors) != expected_ids:
        raise ValueError('Use the original fourteen-factor early B5 chart')
    r = _PositiveReplay(factors)
    r.stages[0]['title'] = 'Alternative: the original fourteen-factor early disk chart'
    r.split('F4', 'alternative.R1', 'alternative.R2')
    r.split('F13', 'alternative.S1', 'alternative.S2')
    moved = r.factors[-1]
    before = r.factors
    r.factors = r.check(before[-1:] + before[:-1])
    r.record('Choose the cyclic start at the existing 124 root; its whole common frame is retained',
             'disk_cyclic_start', frame=moved.word, exact_conjugation=True,
             local_before=before, local_after=r.factors)
    r.drag('alternative.R1', 'prefix.P12',
           title='Commute one round T123 root above the round T12')

    # Canonical cabled PC lantern R Q S = O I, with the inner cluster12.
    # A cyclic start gives S R Q. One retained Hurwitz interchange gives
    # S (R Q R^-1) R, exactly the source order in common frame sigma4^-2.
    root = Factor('pattern.R123', (), 1, 3)
    other = Factor('pattern.S124', (-3,), 1, 3)
    pair = Factor('pattern.Q34', (), 3, 2)
    canonical = (other, root, pair)
    interchange = research_hurwitz_move(canonical, 1, 2)
    generic = interchange['factors']
    after = (Factor('pattern.O1234', (), 1, 4), Factor('pattern.T12', (), 1, 2))
    if exact_action(product(canonical), 5) != exact_action(product(after), 5):
        raise ValueError('The canonical cabled PC lantern failed')
    frame = (-4, -4)
    transported = tuple(replace(f, conjugator=reduce_word(frame + f.conjugator)) for f in generic)
    local = r.factors[:3]
    matches = tuple(dict(actual=a, pattern=b, exact_disk_equal=exact_action(a.word, 5) == exact_action(b.word, 5))
                    for a, b in zip(local, transported))
    if not all(c['exact_disk_equal'] for c in matches):
        raise ValueError('The actual source factors do not match the cabled lantern chart')
    witness = dict(canonical_before=canonical, canonical_after=after,
                   retained_interchange=interchange, generic_input=generic,
                   frame=frame, individual_matches=matches, exact_disk_equality=True)
    r.substitute(0, 3, (Factor('alternative.O1234', frame, 1, 4),
                        Factor('alternative.T12', (), 1, 2)),
                 'PC cluster lantern on the ACTUAL 124, 34 and 123 curves', 'disk_cluster_lantern')
    r.stages[-1]['named_pattern_witness'] = witness
    r.combine('alternative.T12', 'prefix.P12', 'alternative.T12.square')
    lantern_end = len(r.stages) - 1

    outer = r.factors[0]
    daisy = pc_daisy_terms(outer.mapping_class)
    terms = tuple(Factor('alternative.daisy.' + str(i), t.conjugator, t.first, t.points)
                  for i, t in enumerate(daisy))
    q = Factor('alternative.target.Q14', (-4, 1, 2, 3), 4, 2)
    if exact_action(terms[-1].word, 5) != exact_action(q.word, 5):
        raise ValueError('The alternative daisy did not expose the actual Q14')
    r.substitute(0, 1, terms,
                 'PC daisy of the new four-point curve supplies EXACT Q14 without extra half twists',
                 'disk_pc_daisy')

    # A second existing root supplies P35, but no half matching route is
    # inferred. The earlier naive F5/S/P35 transport fails in this chart.
    supplier = r.factors[r.position('F8.1')]
    petals = pc_daisy_terms(supplier.mapping_class)
    p35 = Factor('alternative.target.P35', (-4,), 3, 2)
    if exact_action(petals[0].word, 5) != exact_action(p35.word, 5):
        raise ValueError('The original 345 daisy did not supply the exact P35')
    original_halves = tuple(f for f in factors if f.half)
    if tuple(f for f in r.factors if f.half) != original_halves:
        raise ValueError('The alternative chart changed or introduced a half twist')
    retained = tuple(s['factors'] for s in r.stages) + tuple(
        a['factors'] for s in r.stages for a in s.get('atomic_steps', ()))
    peak = max(_score(fs)['max_support_word'] for fs in retained)
    if peak > 16:
        raise ValueError('The alternative lantern exceeded its original support maximum16')
    for stage in r.stages:
        if stage['kind'] in ('disk_cluster_lantern', 'disk_pc_daisy'):
            supports = [[enclosed_boundaries(f.mapping_class, 5) for f in stage[k]]
                        for k in ('local_before', 'local_after')]
            stage['framed_balance_before_minus_after'] = tuple(
                sum(i in b for b in supports[0]) - sum(i in b for b in supports[1]) for i in range(1, 6))
    result = dict(stages=tuple(r.stages), factors=r.factors, graphical_steps=len(r.stages) - 1,
                lantern_operations=lantern_end, adjacent_checks=sum(s.get('adjacent_moves', 0) for s in r.stages),
                named_pattern_interchanges=1, lantern_witness=witness, actual_q14=terms[-1],
                next_p35=dict(source_root=supplier, daisy_terms=petals, actual_p35=p35,
                              exact_disk_equal=True, applied=False, half_match_claimed=False),
                sphere_move_count=0, half_twists_remaining=4, half_twists_introduced=0,
                all_factors_positive=True, actual_peak_support_word=peak,
                before_score=_score(factors), after_score=_score(r.factors),
                complete_named_derivation=False, replacement_for_full_proof=False,
                applied_to_public_replay=False,
                scope='Seven reached positive B5 operations expose a different PC daisy, a round T12 square and actual Q14. All four original halves remain unchanged. This is an alternative research branch, not a shorter complete proof or a sphere move.')

    result['next_half_target'] = _prepare_half_target(result['stages'][lantern_end]['factors'])
    return result


def _prepare_half_target(factors):
    """Retain a checked five-operation preparation, not an applied arc match."""
    r = _PositiveReplay(tuple(factors))
    r.stages[0]['title'] = 'Separate target probe: alternative phase after operation six'
    r.split('F5', 'alternative.prepare.F5.1', 'alternative.prepare.F5.2')
    r.drag('alternative.prepare.F5.1', 'F3', title='One 235 root up over F3')
    i = r.position('F8.1')
    root = r.factors[i]
    terms = tuple(Factor('alternative.prepare.345.' + str(j), t.conjugator, t.first, t.points)
                  for j, t in enumerate(pc_daisy_terms(root.mapping_class)))
    r.substitute(i, 1, terms, 'Original 345 daisy supplies actual P35', 'disk_pc_daisy')
    r.drag('alternative.S1', 'F9', title='Remaining 124 root up over F9')
    r.drag('alternative.prepare.345.0', 'F3', title='Carry P35 up over F3; a Q14 transport is still needed')
    a, b = (r.factors[r.position(name)] for name in ('F3', 'F9'))
    q = Factor('alternative.required.Q14', (-4, 1, 2, 3), 4, 2)
    already = exact_action(a.word, 5) == exact_action(b.word, 5)
    target = exact_action(q.word + a.word + inverse_word(q.word), 5) == exact_action(b.word, 5)
    if already or not target:
        raise ValueError('The alternative half target no longer has the stated exact scope')
    return dict(stages=tuple(r.stages), source_alternative_step=6, preparation_operations=5,
                current_f3=a, current_f9=b, current_already_matched=False,
                required_conjugator=q, exact_disk_target=True, requires_transport=True,
                applied=False, scope='Separate checked preparation. A further positive Q14 conjugation matches F3 to F9 exactly, but no Q14 gathering or arc match is performed. Not part of the published seven-arrow phase or the complete proof.')
