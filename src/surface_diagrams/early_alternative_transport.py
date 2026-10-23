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
    """Remove all original halves and reach one visible exterior in 36 moves.

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

    for stage in r.stages:
        if stage['kind'] in ('disk_cluster_lantern', 'disk_pc_daisy'):
            sets = [[(f.power, enclosed_boundaries(f.mapping_class, 5)) for f in stage[k]]
                    for k in ('local_before', 'local_after')]
            stage['framed_balance_before_minus_after'] = tuple(
                sum(p for p, b in sets[0] if i in b) - sum(p for p, b in sets[1] if i in b) for i in range(1, 6))
    retained = tuple(s['factors'] for s in r.stages) + tuple(a['factors'] for s in r.stages for a in s.get('atomic_steps', ()))
    return dict(stages=tuple(r.stages), factors=r.factors, graphical_steps=len(r.stages) - 1,
                first_pair_step=first_pair_step, all_pure_step=pure_step, all_pure_factors=pure_factors,
                first_half_match=first_match, second_half_match=second_match,
                adjacent_checks=sum(s.get('adjacent_moves', 0) for s in r.stages),
                actual_peak_support_word=max(_score(fs)['max_support_word'] for fs in retained),
                sphere_move_count=0, half_twists_introduced=0, half_twists_remaining=0,
                explicit_exterior_twists=1, exterior_not_capped=True,
                before_score=_score(source), after_score=_score(r.factors),
                boundary_power=4, all_factors_positive=True, replacement_for_full_proof=False,
                applied_to_public_replay=False,
                scope='Reached positive existing-root research route: original halves removed, round square recovered, one exterior kept visible. This has not been joined to a shorter complete proof; the complete named proof remains 106 steps.')
