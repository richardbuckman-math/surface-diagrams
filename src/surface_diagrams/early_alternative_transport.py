"""Reached existing-root research route; not a shorter complete (6,7) proof."""
from dataclasses import replace

from .braid_actions import inverse_word, reduce_word
from .early_alternative import expose_alternative_early_daisy
from .early_boundary_pure import _PositiveReplay, _score
from .factorization_explorer import Factor, product
from .framed_boundary_relations import enclosed_boundaries
from .mapping_classes import exact_action
from .projected_relations import pc_daisy_terms
from .six_seven_structure import research_hurwitz_move


def _terms(twist, prefix, frame=()):
    return tuple(Factor(prefix + str(j), reduce_word(frame + t.conjugator),
                        t.first, t.points, t.power, t.half)
                 for j, t in enumerate(pc_daisy_terms(twist)))


def _matches(actual, pattern):
    if len(actual) != len(pattern):
        raise ValueError('The named-pattern term counts differ')
    result = tuple(dict(actual=a, pattern=b,
                        exact_disk_equal=exact_action(a.word, 5) == exact_action(b.word, 5))
                   for a, b in zip(actual, pattern))
    if not all(c['exact_disk_equal'] for c in result):
        raise ValueError('An actual factor does not match the named pattern')
    return result


def transport_alternative_roots(factors):
    """Remove original halves and simplify the positive residual in 51 moves.

    Borrow the actual Q14 from the existing four-point daisy. A transported
    daisy replaces Q14 and the remaining 345 petals by O1345. Carry O1345 up
    over F6 before gathering the now matching F3/F9; this order is essential
    to the support bound. Return Q14 and close its original daisy, recovering
    the round T12 square. A short cyclic transport matches F6/F11.

    The resulting sixteen full twists admit a second four-point contraction
    and an actual supplied 45 petal, giving a cabled exterior lantern. This
    reaches a new research endpoint; no shorter complete proof is claimed.
    All local named patterns retain individual disk matches. No sphere move,
    inverse factor, extra half twist, or route search occurs.
    """
    source = tuple(factors)
    alternative = expose_alternative_early_daisy(source)
    preparation = alternative['next_half_target']
    r = _PositiveReplay(preparation['stages'][-1]['factors'])
    r.stages = list(alternative['stages'][:7]) + list(preparation['stages'][1:])
    i = r.position('alternative.O1234')
    initial_outer = r.factors[i]
    first_daisy = _terms(initial_outer.mapping_class, 'alternative.qdaisy.')
    q = first_daisy[-1]
    r.substitute(i, 1, first_daisy, 'PC daisy lends its actual Q14 petal', 'disk_pc_daisy')
    r.drag(q.id, 'F10.1', title='Carry Q14 down across F3 and the remaining 345 petals')

    # Common chart h fixes O1345. Its canonical daisy, followed by two
    # retained inverse petal interchanges and a cyclic start, matches EVERY
    # actual input; a product action alone is not the named recognition.
    outer = Factor('alternative.O1345', (1,), 2, 4)
    h = reduce_word(q.word + (-4,))
    canonical = _terms(outer.mapping_class, 'pattern.daisy.', h)
    changed, interchanges = canonical, []
    for src, dst in ((3, 2), (2, 1)):
        move = research_hurwitz_move(changed, src, dst)
        interchanges.append(move)
        changed = move['factors']
    i = r.position('alternative.prepare.345.1')
    actual = r.factors[i:i + 4]
    cyclic = actual[2:] + actual[:2]
    witness = dict(canonical=canonical, frame=h, retained_interchanges=tuple(interchanges),
                   cyclic_offset=2, individual_matches=_matches(cyclic, changed),
                   outer_preserved=exact_action(h + outer.word + inverse_word(h), 5) == exact_action(outer.word, 5))
    if not witness['outer_preserved']:
        raise ValueError('The transported daisy frame does not preserve its outer curve')
    r.substitute(i, 4, (outer,), 'PC daisy contracts the ACTUAL transported petals to O1345', 'disk_pc_daisy')
    r.stages[-1]['named_pattern_witness'] = witness
    r.drag(outer.id, 'F6', title='Carry O1345 up across F6 before the matching-half gather')
    a, b = (r.factors[r.position(name)] for name in ('F3', 'F9'))
    first_match = _matches((a,), (b,))
    r.drag('F3', r.factors[r.position('F9') - 1].id,
           title='Carry the matched F3 down to F9; F6 unwinds')
    r.combine('F3', 'F9', 'alternative.P13')
    first_pair_step = len(r.stages) - 1

    i = r.position(outer.id)
    returned = _terms(r.factors[i].mapping_class, 'alternative.return.', (-4,))
    _matches((returned[-1],), (q,))
    r.substitute(i, 1, returned, 'The O1345 daisy returns EXACTLY the borrowed Q14', 'disk_pc_daisy')
    r.drag(returned[-1].id, 'alternative.T12.square',
           title='Return Q14 up to restore the round T12 square and T123')
    _matches(r.factors[:4], first_daisy)
    r.substitute(0, 4, (initial_outer,), 'Close the original daisy after its actual Q14 returns', 'disk_pc_daisy')
    if r.factors[r.position('alternative.T12.square')] != Factor('alternative.T12.square', (), 1, 2, 2):
        raise ValueError('The round T12 square was not recovered')

    r.split('F12', 'alternative.F12.1', 'alternative.F12.2')
    r.drag('alternative.F12.1', 'F11', title='One C12 root shortens F11')
    r.drag('alternative.T12.square', initial_outer.id, title='Commute the recovered round square to the top')
    moved, before = r.factors[0], r.factors
    r.factors = r.check(before[1:] + before[:1])
    r.record('Choose the cyclic start just after the round square', 'disk_cyclic_start',
             frame=inverse_word(moved.word), exact_conjugation=True,
             local_before=before, local_after=r.factors)
    r.drag('alternative.T12.square', 'F11', title='Carry the square up the short side; F11 matches F6')
    a, b = (r.factors[r.position(name)] for name in ('F6', 'F11'))
    second_match = _matches((a,), (b,))
    frame = (3, 4, 4)
    before = r.factors
    r.factors = r.check(tuple(r.normalize(replace(f, conjugator=reduce_word(frame + f.conjugator))) for f in before))
    r.record('Common disk frame makes the first four-point curve round', 'global_conjugation',
             frame=frame, local_before=before, local_after=r.factors, exact_conjugation=True)
    r.drag('alternative.F12.1', 'F10.2', title='Reorder C12 before the final matching-half gather')
    r.drag('F11', 'F6', after=True, title='Gather the final matching original halves')
    r.combine('F6', 'F11', 'alternative.P24')
    pure_step = len(r.stages) - 1
    pure_factors = r.factors

    frame = (-4, -3)
    supplier = r.factors[-1]
    before = r.factors
    r.factors = r.check(tuple(r.normalize(replace(f, conjugator=reduce_word(frame + f.conjugator))) for f in before))
    r.record('Common disk frame for the next actual Q15 supplier', 'global_conjugation',
             frame=frame, local_before=before, local_after=r.factors, exact_conjugation=True)
    terms = tuple(r.normalize(f) for f in _terms(supplier.mapping_class, 'alternative.next.', frame))
    r.substitute(r.position(supplier.id), 1, terms, 'C12 daisy supplies the actual Q15', 'disk_pc_daisy')
    moved, before = r.factors[-1], r.factors
    r.factors = r.check(before[-1:] + before[:-1])
    r.record('Choose the cyclic start at the actual Q15', 'disk_cyclic_start',
             frame=moved.word, local_before=before, local_after=r.factors, exact_conjugation=True)
    r.drag('alternative.next.2', 'alternative.prepare.F5.1', title='Carry Q15 through the combined four-point prefix and the two roots')
    index = r.position('alternative.R2')
    chart = (-3, -2)
    canonical = (Factor('pattern.A134', (1,), 2, 3),
                 Factor('pattern.B234', (1, 1), 2, 3), Factor('pattern.Q12', (), 1, 2))
    pattern = tuple(replace(f, conjugator=reduce_word(chart + f.conjugator)) for f in canonical)
    cluster_matches = _matches(r.factors[index:index + 3], pattern)
    canonical_after = (Factor('pattern.O1234', (), 1, 4), Factor('pattern.I34', (), 3, 2))
    if exact_action(product(canonical), 5) != exact_action(product(canonical_after), 5):
        raise ValueError('The canonical inner-34 cabled PC lantern failed')
    r.substitute(index, 3,
                 (Factor('alternative.round.O1234', (), 1, 4), Factor('alternative.T23', (), 2, 2)),
                 'PC cluster lantern gives the second four-point twist', 'disk_cluster_lantern')
    r.stages[-1]['named_pattern_witness'] = dict(canonical=canonical, canonical_after=canonical_after,
        frame=chart, individual_matches=cluster_matches, exact_disk_equality=True)
    r.drag('alternative.return.1', 'alternative.T23', title='Gather the ACTUAL missing 45 petal by the short side')
    g = (-3, 1, 2, 2, 3)
    canonical = (Factor('pattern.S1235', reduce_word(g + (-4,)), 1, 4),
                 Factor('pattern.R1234', g, 1, 4), Factor('pattern.Q45', g, 4, 2))
    actual = r.factors[:3]
    matches = _matches(actual, canonical)
    after = (Factor('alternative.exterior', (), 1, 5), Factor('alternative.inner123', g, 1, 3))
    r.substitute(0, 3, after, 'Cabled PC lantern on the ACTUAL two four-point curves and supplied 45 petal', 'disk_cluster_lantern')
    r.stages[-1]['named_pattern_witness'] = dict(frame=g, canonical=canonical, individual_matches=matches,
        canonical_relation='Cyclic cabled PC lantern S R Q = exterior T123', exact_disk_equality=True)

    exterior_step = len(r.stages) - 1
    exterior_score = _score(r.factors)
    # Reuse the same fixed square on the NEW residual, keeping all five
    # adjacent checks. The newly exposed prefix is a cabled lantern in
    # h=Q45^-1 R234^-1, not in the tempting but incorrect round B4 chart.
    r.drag('alternative.T12.square', 'F8.2',
           title='Unwind five actual residual curves with the fixed positive square')
    r.drag('alternative.inner123', 'alternative.T23',
           title='Commute the 123 root past T23 to its actual 34 and 124 companions')
    q45 = Factor('pattern.borrowed45', g, 4, 2)
    round234 = Factor('pattern.R234', (), 2, 3)
    h = reduce_word(inverse_word(q45.word) + inverse_word(round234.word))
    canonical = (Factor('pattern.R123', (), 1, 3), Factor('pattern.Q34', (), 3, 2),
                 Factor('pattern.S124', (-3,), 1, 3))
    pattern = tuple(replace(f, conjugator=reduce_word(h + f.conjugator)) for f in canonical)
    index = r.position('alternative.inner123')
    prefix_matches = _matches(r.factors[index:index + 3], pattern)
    raw_after = (Factor('alternative.residual.O1234', h, 1, 4),
                 Factor('alternative.residual.I12', h, 1, 2))
    after = tuple(r.normalize(f) for f in raw_after)
    presentations = _matches(raw_after, after)
    r.substitute(index, 3, after,
                 'Cabled PC lantern contracts the ACTUAL 123, 34 and 124 curves', 'disk_cluster_lantern')
    r.stages[-1]['named_pattern_witness'] = dict(canonical=canonical, frame=h,
        frame_decomposition=(inverse_word(q45.word), inverse_word(round234.word)),
        individual_matches=prefix_matches, raw_after=raw_after,
        presentation_matches=presentations, exact_disk_equality=True)


    residual_lantern_step = len(r.stages) - 1
    # The actual 345 daisy lends round34.  The 245 root can cross the
    # neighboring 145 and 13 factors without changing this named target.
    supplier = r.factors[r.position('F8.2')]
    terms = tuple(r.normalize(f) for f in _terms(supplier.mapping_class, 'alternative.shared.'))
    _matches((terms[0],), (Factor('pattern.round34', (), 3, 2),))
    r.substitute(r.position(supplier.id), 1, terms,
                 'The actual 345 daisy lends its round 34 petal', 'disk_pc_daisy')
    r.drag('F10.2', 'alternative.P13',
           title='Carry the 245 root up across the 145 root and the 13 pair')
    r.drag(terms[0].id, terms[2].id,
           title='Carry round 34 down through its own two remaining petals')
    # R Q S = O I is the canonical cabled lantern. Its cyclic Q S R
    # presentation has the SAME outputs: R commutes with O and I.
    h = (-1, -4, -3, -2, 3, 4, -3)
    canonical = (Factor('pattern.Q34', (), 3, 2),
                 Factor('pattern.S124', (-3,), 1, 3), Factor('pattern.R123', (), 1, 3))
    canonical_after = (Factor('pattern.O1234', (), 1, 4), Factor('pattern.I12', (), 1, 2))
    if exact_action(product(canonical), 5) != exact_action(product(canonical_after), 5):
        raise ValueError('The cyclic shared-inner-pair cabled lantern failed')
    pattern = tuple(replace(f, conjugator=reduce_word(h + f.conjugator)) for f in canonical)
    index = r.position(terms[0].id)
    matches = _matches(r.factors[index:index + 3], pattern)
    raw_after = (Factor('alternative.shared.O2345', h, 1, 4),
                 Factor('alternative.shared.I25', h, 1, 2))
    after = tuple(r.normalize(f) for f in raw_after)
    r.substitute(index, 3, after,
                 'Cabled PC lantern closes the actual 34, 235 and 245 cluster', 'disk_cluster_lantern')
    r.stages[-1]['named_pattern_witness'] = dict(frame=h, canonical=canonical,
        canonical_after=canonical_after, canonical_cyclic_order='Q S R',
        individual_matches=matches, raw_after=raw_after,
        presentation_matches=_matches(raw_after, after), exact_disk_equality=True)
    shared_petal_step = len(r.stages) - 1
    r.drag('alternative.return.2', 'alternative.return.0',
           title='The actual 35 pair unwinds the 134 root to a short chart')
    _matches((r.factors[r.position('alternative.return.0')],),
             (Factor('pattern.short134', (1,), 2, 3),))
    r.drag('alternative.shared.I25', 'alternative.T12.square',
           title='Carry the shared 25 pair up; unwind the square and its two petals')
    _matches((r.factors[r.position('alternative.T12.square')],),
             (Factor('pattern.under15.square', (-4, -3, -2), 1, 2, 2),))

    shared_unwinding_step = len(r.stages) - 1
    # In the old chart, the same daisy gathering reaches support30. The
    # common B4 frame (3,2), followed by the root-first route, keeps EVERY
    # retained state within18. Gathering the three pair petals first in
    # this frame instead reaches40; the order here is essential.
    h = (3, 2)
    before = r.factors
    r.factors = r.check(tuple(r.normalize(replace(f, conjugator=reduce_word(h + f.conjugator))) for f in before))
    r.record('Common disk frame keeps the inside-four daisy readable', 'global_conjugation',
             frame=h, local_before=before, local_after=r.factors, exact_conjugation=True)
    before = r.factors
    index = r.position('alternative.return.0')
    tail = before[index:]
    r.factors = r.check(tail + before[:index])
    r.record('Choose the cyclic start at the actual three-point root', 'disk_cyclic_start',
             frame=product(tail), local_before=before, local_after=r.factors, exact_conjugation=True)
    r.drag('alternative.return.0', r.factors[r.position('alternative.next.0') - 1].id,
           title='Carry the three-point root down through the eight residual factors')
    r.drag('alternative.T23', 'alternative.exterior',
           title='Commute the final pair petal past the visible exterior')
    chart = h + (1, 1, 2, 3)
    canonical = _terms(Factor('pattern.inside.D4', chart, 1, 4).mapping_class, 'pattern.inside.')
    changed, interchanges = canonical, []
    for src, dst in ((3, 2), (2, 1)):
        move = research_hurwitz_move(changed, src, dst)
        interchanges.append(move)
        changed = move['factors']
    index = r.position('alternative.return.0')
    matches = _matches(r.factors[index:index + 4], changed)
    outer_preserved = exact_action(Factor('pattern.inside.D4', chart, 1, 4).word, 5) == exact_action(Factor('pattern.roundD4', (), 1, 4).word, 5)
    if not outer_preserved:
        raise ValueError('The transported inside daisy did not preserve the round four-point boundary')
    r.substitute(index, 4, (Factor('alternative.inside.D4', (), 1, 4),),
                 'Transported PC daisy closes the actual root and its three pair petals', 'disk_pc_daisy')
    r.stages[-1]['named_pattern_witness'] = dict(frame=chart, canonical=canonical,
        retained_interchanges=tuple(interchanges), individual_matches=matches,
        outer_preserved=outer_preserved, exact_disk_equality=True)
    inside_daisy_step = len(r.stages) - 1
    r.drag('alternative.inside.D4', 'alternative.P24',
           title='Carry the new round four-point twist up to unwind the residual block')

    for stage in r.stages:
        if stage['kind'] in ('disk_cluster_lantern', 'disk_pc_daisy'):
            sets = [[(f.power, enclosed_boundaries(f.mapping_class, 5)) for f in stage[k]]
                    for k in ('local_before', 'local_after')]
            stage['framed_balance_before_minus_after'] = tuple(
                sum(p for p, b in sets[0] if i in b) - sum(p for p, b in sets[1] if i in b) for i in range(1, 6))
    outer_daisy = _terms(r.factors[r.position('alternative.shared.O2345')].mapping_class, 'target.outer.')
    triple_daisy = _terms(r.factors[r.position('alternative.F12.1')].mapping_class, 'target.triple.')
    next_daisy_targets = dict(outer_daisy=outer_daisy, triple_daisy=triple_daisy,
        shared_35_match=_matches((outer_daisy[2],), (triple_daisy[2],)),
        existing_45_match=_matches((r.factors[r.position('alternative.shared.I25')],), (outer_daisy[1],)),
        existing_25_match=_matches((r.factors[r.position('alternative.return.2')],), (outer_daisy[3],)),
        existing_15_unit_match=_matches((replace(r.factors[r.position('alternative.T12.square')], power=1),), (triple_daisy[1],)),
        applied=False, requires_transport=True,
        scope='Exact shared petal targets only; neither daisy has been expanded or gathered here.')
    retained = tuple(s['factors'] for s in r.stages) + tuple(a['factors'] for s in r.stages for a in s.get('atomic_steps', ()))
    return dict(stages=tuple(r.stages), factors=r.factors, graphical_steps=len(r.stages) - 1,
                first_pair_step=first_pair_step, all_pure_step=pure_step, all_pure_factors=pure_factors,
                first_exterior_step=exterior_step, first_exterior_score=exterior_score,
                residual_lantern_step=residual_lantern_step, shared_petal_step=shared_petal_step,
                shared_unwinding_step=shared_unwinding_step, inside_daisy_step=inside_daisy_step,
                next_daisy_targets=next_daisy_targets,
                first_half_match=first_match, second_half_match=second_match,
                adjacent_checks=sum(s.get('adjacent_moves', 0) for s in r.stages),
                actual_peak_support_word=max(_score(fs)['max_support_word'] for fs in retained),
                sphere_move_count=0, half_twists_introduced=0, half_twists_remaining=0,
                explicit_exterior_twists=1, exterior_not_capped=True,
                before_score=_score(source), after_score=_score(r.factors),
                boundary_power=4, all_factors_positive=True, replacement_for_full_proof=False,
                applied_to_public_replay=False,
                scope='Reached positive existing-root research route: original halves removed, round square recovered, one exterior kept visible, two bounded cabled lanterns, shared-petal transports and an inside-four daisy reduce its residual curve intersections. This has not been joined to a shorter complete proof; the complete named proof remains 106 steps.')
